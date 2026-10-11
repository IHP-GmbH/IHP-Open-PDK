# =========================================================================================
# Copyright 2025 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================================

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import yaml

from models_verifier.dc_runner.dc_sweep_runner import DcSweepRunner
from models_verifier.dc_runner.helper import SIM_TYPE_MAP, expand_env, ngspice_binary
from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance
from models_verifier.error_analyzer.range_checker import RangeChecker
from models_verifier.mdm_processing.aggregator import MdmDirectoryAggregator
from models_verifier.run_record import (
    exception_toolchain,
    ngspice_version,
    osdi_files_in,
    toolchain_id,
    toolchain_mismatch,
    write_toolchain_txt,
)
from models_verifier.waivers.waiver import (
    FAILED_NEW,
    NO_POINTS,
    NOT_SIMULATED,
    PASSED,
    UNWAIVED_STATUSES,
    ExceptionStore,
    curve_key,
    index_failing_points,
    points_fingerprint,
)


class ConfigError(Exception):
    """Raised when configuration loading or validation fails."""


def read_config(config_path: Path) -> Dict:
    """
    Read a device config YAML and expand ${VAR} and ~ in its strings.

    A config may name a `base_config` (path relative to the framework root): the base is read
    first and the config's own top-level keys replace the base's. A key is replaced as a whole,
    e.g. `design_param_overrides: {}` drops the base's overrides. Used for the HBT test-structure
    variants, which differ from their device config only in a few keys.
    """
    config = yaml.safe_load(Path(config_path).read_text()) or {}
    base = config.pop("base_config", None)
    if base:
        merged = read_config(Path(base))
        merged.update(config)
        config = merged
    return expand_env(config)


def resolve_output_dir(raw: str) -> Path:
    """
    `output_dir` from the config, with $RESULTS_ROOT (set by the Makefile, one folder per
    toolchain) replacing a leading "models_results" folder, e.g. "models_results/nmos_lv" +
    RESULTS_ROOT=models_results/ng47-ovr-b4517ad -> models_results/ng47-ovr-b4517ad/nmos_lv.
    """
    path = Path(raw)
    root = os.environ.get("RESULTS_ROOT")
    if root and path.parts and path.parts[0] == "models_results":
        path = Path(root).joinpath(*path.parts[1:])
    return path


class VerificationError(Exception):
    """Raised when verification encounters a fatal error."""


class MdmVerifier:
    """
    MDM block verification system.

    Responsibilities:
    - Load and validate YAML configuration
    - Aggregate MDM simulation data
    - Run DC sweep simulations
    - Perform range checking on results
    - Save CSV reports and summaries
    """

    def __init__(self, config_path: Path):
        """Initialize the verifier with configuration and logging."""
        self.config = self._load_config(config_path)
        self.device_name: str = self.config["device_name"]
        self.device_type: str = self.config["device_type"]
        self.clip_curr: float = float(self.config.get("clip_curr", 1e-12))

        self.output_dir = resolve_output_dir(self.config["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Toolchain of this run (tools/toolchain.py, exported by the Makefile). Devices with
        # Verilog-A models (`osdi_path`) keep exceptions per full toolchain ID, the others per
        # ngspice version only (see run_record.py).
        self.toolchain: str = toolchain_id()
        self.exception_key: str = exception_toolchain(self.toolchain, bool(self.config.get("osdi_path")))
        self.ngspice_bin: str = ngspice_binary()
        # Exceptions no failing row of the run used (filled by _apply_waivers, listed for review).
        self.stale_exceptions: List[Tuple[str, str, str, str]] = []
        self.absent_exceptions: List[Tuple[str, str, str, str]] = []   # their curve is not in the run
        # Blocks whose simulation failed completely: (group, block index, message). Any makes the
        # run exit 1 (a framework error is never waived).
        self.simulation_errors: List[Tuple[str, int, str]] = []

        self._configure_logging()

    # -------------------------------------------------------------------------
    # Setup helpers
    # -------------------------------------------------------------------------

    def _configure_logging(self) -> None:
        """Configure logging to both console and file."""
        timestamp = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H_%M_%S")
        log_path = self.output_dir / f"models_verifier_{timestamp}.log"

        # force: main() configured the console already; without it the log file stayed empty
        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler(),          # stderr, as configured by main()
            ],
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,
        )

    def _load_config(self, config_path: Path) -> Dict:
        """Load YAML config and validate required fields."""
        if not config_path or not config_path.exists():
            raise ConfigError(f"Config YAML '{config_path}' not found.")

        config = read_config(config_path)

        required = [
            "mdm_dir",
            "dc_template_path",
            "corner_lib_path",
            "device_type",
            "device_name",
            "metrics",
            "output_dir",
        ]
        missing = [k for k in required if not config.get(k)]
        if missing:
            raise ConfigError(f"Missing required config keys: {missing}")
        for group, template in (config.get("setup_templates") or {}).items():
            if not Path(template).exists():
                raise ConfigError(f"setup_templates: template of '{group}' not found: {template}")
        if "$" in str(config.get("osdi_path", "")):
            raise ConfigError(
                f"osdi_path '{config['osdi_path']}' uses an unset environment variable: run through "
                "the Makefile (make test-<case> TOOLCHAIN=<id>), which exports OSDI_DIR."
            )

        # Defaults
        config.setdefault("max_workers", max(1, os.cpu_count()))
        config.setdefault("tolerance_abs", 0.0)
        config.setdefault("tolerance_rel", 0.0)
        config.setdefault("output_dir", str(Path.cwd() / "final_reports"))

        return config

    @staticmethod
    def _clean_mkdir(path: Path) -> Path:
        """Delete and recreate a directory."""
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    # -------------------------------------------------------------------------
    # Core pipeline
    # -------------------------------------------------------------------------

    def _aggregate_and_simulate(self, create_csvs: bool = True) -> List[pd.DataFrame]:
        """
        Aggregate MDM data and run DC sweep simulations.

        Args:
            create_csvs: Whether to save intermediate CSVs.

        Returns:
            List of merged DataFrames combining measurements and simulations.
        """
        mdm_dir = Path(self.config["mdm_dir"])
        if not mdm_dir.exists():
            raise VerificationError(f"MDM directory does not exist: {mdm_dir}")

        csv_stage_dir = None
        if create_csvs:
            csv_stage_dir = self._clean_mkdir(self.output_dir / "clean_measured_data")

        aggregator = MdmDirectoryAggregator(
            input_dir=mdm_dir,
            recursive=True,
            output_dir=csv_stage_dir,
            create_csvs=create_csvs,
            device_type=self.device_type,
            exclude_patterns=self.config.get("exclude_patterns") or [],
        )
        full_by_type, compact_by_type = aggregator.aggregate()
        if not compact_by_type:
            raise VerificationError("No sweep data discovered in MDM directory.")

        # Optional config-declared design-parameter overrides (e.g. `Nx: 4` when the MDM
        # REMARKS disagree with the documented MQA variant). Applied to BOTH the compact
        # (simulation) and full (measured/merge) tables so results stay self-consistent.
        overrides = self.config.get("design_param_overrides") or {}
        if overrides:
            logging.warning("Applying design_param_overrides from config: %s", overrides)
            for by_type in (full_by_type, compact_by_type):
                for key in list(by_type):
                    by_type[key] = self._apply_design_overrides(by_type[key], overrides)

        # Optional netlist template per measurement group (config `setup_templates`), e.g. the
        # MOS junction diodes, which need a different circuit than the transistor sweeps.
        setup_templates = {k: Path(v) for k, v in (self.config.get("setup_templates") or {}).items()}

        # Configure DC runner
        runner = DcSweepRunner(
            template_path=Path(self.config["dc_template_path"]),
            corner_lib_path=Path(self.config["corner_lib_path"]),
            osdi_path=Path(self.config["osdi_path"])
            if self.device_type == "mos"
            else None,
            device_name=self.config["device_name"],
            max_workers=int(self.config["max_workers"]),
            device_type=self.config["device_type"],
            output_dir=Path(self.output_dir),
            netlists_dir=self.output_dir / "netlists",
        )

        merged_parts: List[pd.DataFrame] = []
        with tempfile.TemporaryDirectory(prefix="ngspice_runs_") as work_dir:
            work_dir = Path(work_dir)

            for setup_type, compact_df in compact_by_type.items():
                sim_type = SIM_TYPE_MAP.get(setup_type, "current")
                if sim_type == "cap":       # judged by the C-V tier (make test-<case>-cv)
                    logging.info("Capacitance group %s: judged by the C-V tier, not here", setup_type)
                    continue

                logging.info(f"Processing simulation setup: {setup_type}")
                if compact_df.empty or full_by_type.get(setup_type) is None:
                    continue

                try:
                    sim_df, errors = runner.run(compact_df, setup_templates.get(setup_type))
                    if errors:
                        logging.error(f"Simulation errors for {setup_type}: {errors}")
                        self.simulation_errors += [(str(setup_type), int(i), str(m)) for i, m in errors]

                    merged = runner.merge_with_clean(sim_df, full_by_type[setup_type])
                    if not merged.empty:
                        merged_parts.append(merged)

                except Exception as e:
                    logging.error(f"Failed setup {setup_type}: {e}", exc_info=True)
                    self.simulation_errors.append((str(setup_type), -1, f"whole group failed: {e}"))

        if not merged_parts:
            raise VerificationError("No merged sim-vs-measured rows produced.")

        return merged_parts

    @staticmethod
    def _apply_design_overrides(df: pd.DataFrame, overrides: Dict[str, object]) -> pd.DataFrame:
        """
        Force device design parameters (columns such as `Nx`, `W`, `L`, `M`) to the values
        declared under `design_param_overrides` in the config. Column names are matched
        case-insensitively; a missing column is created.
        """
        if df is None or df.empty or not overrides:
            return df
        df = df.copy()
        lower_map = {str(c).lower(): c for c in df.columns}
        for name, value in overrides.items():
            col = lower_map.get(str(name).lower(), str(name))
            df[col] = value
        return df

    @staticmethod
    def _clip_current_sign_preserving(values: pd.Series, clip_curr: float) -> pd.Series:
        """
        Floor |I| at `clip_curr` while KEEPING the sign: -3e-13 -> -clip_curr, +2e-3 -> +2e-3.

        A plain `clip(lower=clip_curr)` collapsed every NEGATIVE current (PMOS drain
        current, NMOS source current, pnp base/collector currents, HBT reverse-mode base
        current) to the floor on BOTH the measured and the simulated side, so those
        comparisons passed vacuously. NaN is preserved.
        """
        vals = pd.to_numeric(values, errors="coerce")
        sign = np.where(vals < 0, -1.0, 1.0)
        return pd.Series(sign * np.maximum(vals.abs(), clip_curr), index=values.index)

    def _build_range_checker(self) -> RangeChecker:
        """
        Construct and configure the range checker.
        Uses only threshold_percent_oob from the config.
        """
        threshold_percent = float(self.config.get("threshold_percent_oob", 0))
        default_threshold = Threshold(max_out_of_range_percent=threshold_percent)
        tolerance_rel = float(self.config.get("corner_tolerance_percent", 0.0))

        metrics = [
            MetricSpec(
                name=m["name"],
                meas=m["meas"],
                tt=m["tt"],
                ss=m["ss"],
                ff=m["ff"],
                tolerance=Tolerance(
                    abs=float(self.config["tolerance_abs"]),
                    rel=tolerance_rel,
                ),
                valid_range=m.get("valid_range"),
                min_limit=m.get("min"),
                max_limit=m.get("max"),
                # Currents are floored at clip_curr (sign-preserving, see clean_results):
                # give the checker the same floor so meas/model agreement "both below
                # the floor" is not scored as a sign mismatch.
                noise_floor=self.clip_curr if str(m["name"]).lower().startswith("i") else None,
            )
            for m in self.config["metrics"]
        ]
        return RangeChecker(
            metrics=metrics,
            default_threshold=default_threshold,
            mqa_ranges=self.config.get("mqa_ranges"),
        )

    # -------------------------------------------------------------------------
    # Outputs
    # -------------------------------------------------------------------------

    def clean_results(self, dataframes: List[pd.DataFrame]) -> None:
        """
        Floor every current column (name starting with "i", measured or simulated) at clip_curr,
        keeping its sign, in place. Runs before the range check, so the check and the written
        combined_results see the same values.
        """
        for df in dataframes:
            current_cols = [col for col in df.columns
                            if col.startswith("i") and ("_sim" in col or "_meas" in col)]
            for col in current_cols:
                df[col] = self._clip_current_sign_preserving(df[col], self.clip_curr)
            logging.debug(f"Clipped currents are: {current_cols}")

    def write_combined_results(self, frames: List[pd.DataFrame], bands: pd.DataFrame) -> None:
        """
        Write combined_results/<group>.csv, one per frame (= measurement group): the measured and
        simulated columns plus, for every metric judged in the group, the band and the judged flag
        the range checker used (<metric>_band_lo, <metric>_band_hi, <metric>_judged). `bands` is
        aligned with pd.concat(frames, ignore_index=True).
        """
        output_dir = self.output_dir / "combined_results"
        output_dir.mkdir(parents=True, exist_ok=True)
        start = 0
        for df in frames:
            part = bands.iloc[start:start + len(df)]
            start += len(df)
            metrics = [c[: -len("_band_lo")] for c in part.columns
                       if c.endswith("_band_lo") and part[c].notna().any()]
            band_cols = [f"{m}{suffix}" for m in metrics for suffix in ("_band_lo", "_band_hi", "_judged")]
            table = pd.concat([df.reset_index(drop=True), part[band_cols].reset_index(drop=True)], axis=1)
            group = str(table["master_setup_type"].iloc[0])
            path = output_dir / f"{group.replace(' ', '_').replace('/', '-')}.csv"
            table.drop(columns=["master_setup_type"]).to_csv(path, index=False)

    # -------------------------------------------------------------------------
    # Exceptions (waivers/waiver.py) and reports
    # -------------------------------------------------------------------------

    def _start_run(self) -> None:
        """
        Begin a pipeline run: remove the results of an earlier run (so a crash never leaves old
        reports or tables behind for the generator, the figures or the EDA), reset the error list,
        record the toolchain.
        """
        for folder in ("final_reports", "combined_results", "run_data", "netlists"):
            shutil.rmtree(self.output_dir / folder, ignore_errors=True)
        self.simulation_errors = []
        self._record_toolchain()

    def _record_toolchain(self) -> None:
        """
        Check that the ngspice binary and the OSDI model belong to the toolchain ID, then write
        `<output_dir>/toolchain.txt`: toolchain ID, exception key, ngspice, OSDI files.
        """
        osdi_path = self.config.get("osdi_path")
        version = ngspice_version(self.ngspice_bin)
        problem = toolchain_mismatch(self.toolchain, version, osdi_path)
        if problem:
            raise VerificationError(problem)
        osdi_files = osdi_files_in(str(Path(osdi_path).parent)) if osdi_path else []
        path = write_toolchain_txt(self.output_dir, self.device_name, self.toolchain, self.exception_key,
                                   self.ngspice_bin, version, osdi_files)
        logging.info("Toolchain %s (exception key %s) recorded in %s", self.toolchain, self.exception_key, path)

    def _apply_waivers(
        self, report_df: pd.DataFrame, detailed_failures: pd.DataFrame, store: ExceptionStore
    ) -> pd.DataFrame:
        """
        Set the `status` of every judged row (see waivers/waiver.py):

            Passed                                  the row passed the band check
            Failed (waived, auto, pending review)   failed; the run reproduces its exception exactly
            Failed (waived, approved)               the same, for an exception the reviewer approved
            Failed (new)                            failed without an exactly matching exception
            Failed (not simulated)                  measured points but no simulated values (error)
            No points                               no measured point in the bias window: not judged

        `passed` stays as the band check decided: waived rows remain failures in every report.
        The fingerprint of each failing row's points goes into `points_sha256` (the generator
        copies it). Exceptions no failing row used are kept in `self.stale_exceptions`.
        """
        report_df = report_df.copy()
        keys = ["input_data", "block_index", "metric", "target"]
        if set(keys) <= set(report_df.columns) and report_df.duplicated(subset=keys).any():
            dup = report_df[report_df.duplicated(subset=keys, keep=False)][keys].head(5).to_dict("records")
            raise VerificationError(f"two rows share a curve key (file names must be unique per case): {dup}")
        points = index_failing_points(detailed_failures)
        statuses: List[str] = []
        fingerprints: List[str] = []
        self._n_changed_logged = 0
        for row in report_df.itertuples(index=False):
            fingerprint = ""
            if int(row.n_points) == 0 and int(getattr(row, "n_missing", 0) or 0) > 0:
                status = NOT_SIMULATED
            elif int(row.n_points) == 0:
                # no measured point inside the bias window of this metric: nothing was judged
                status = NO_POINTS
            elif bool(row.passed):
                status = PASSED
            else:
                key = curve_key(getattr(row, "input_data", None), getattr(row, "block_index", None),
                                row.metric, row.target)
                fingerprint = points_fingerprint(points.get(key, []), store.sig_digits)
                status = store.status_of(key, self.exception_key, int(row.n_points),
                                         int(row.n_out_of_bounds), fingerprint)
                if status == FAILED_NEW:
                    self._log_changed_exception(store, key, row, fingerprint, points.get(key, []))
            statuses.append(status)
            fingerprints.append(fingerprint)
        report_df["status"] = pd.Series(statuses, index=report_df.index, dtype=object)
        report_df["points_sha256"] = pd.Series(fingerprints, index=report_df.index, dtype=object)
        self.stale_exceptions = store.stale_keys(report_df, self.exception_key)
        self.absent_exceptions = store.absent_keys(report_df, self.exception_key)

        n_failed = sum(s.startswith("Failed") for s in statuses)
        n_new = sum(s in UNWAIVED_STATUSES for s in statuses)
        logging.info(
            "Exceptions (%s, key %s): %d failing row(s), %d waived by an exact match, %d new; "
            "%d stale exception(s); %d loaded.",
            store.path, self.exception_key, n_failed, n_failed - n_new, n_new,
            len(self.stale_exceptions), len(store),
        )
        return report_df

    def _log_changed_exception(self, store: ExceptionStore, key, row, fingerprint: str, points: List[dict],
                               max_rows: int = 10, max_points: int = 12) -> None:
        """
        A failing row that has an exception for this toolchain but does not match it: log what
        changed and its failing points (bias and tt / ss / ff with 12 significant digits), so the
        difference can be read from a CI log. At most `max_rows` rows per run.
        """
        why = store.difference(key, self.exception_key, int(row.n_points), int(row.n_out_of_bounds), fingerprint)
        if why is None or self._n_changed_logged >= max_rows:
            return
        self._n_changed_logged += 1
        logging.warning("Curve %s no longer matches its exception (%s): %s", "/".join(key), self.exception_key, why)
        for p in points[:max_points]:
            sim = " ".join(f"{k}={float(v):.12g}" for k, v in p["sim"].items() if v is not None and pd.notna(v))
            bias = " ".join(f"{k}={float(v):.12g}" for k, v in sorted(p["bias"].items()))
            logging.warning("    point %s: %s", bias, sim)

    def _write_new_failures(self, report_df: pd.DataFrame, path: Path) -> None:
        """
        Write `final_reports/new_failures.csv` (rows "Failed (new)" / "Failed (not simulated)", the
        ones that make the run exit 1) and, next to it, `stale_exceptions.csv` (exceptions no
        failing row used) and `simulation_errors.csv` (blocks whose simulation failed). All are
        always written, with headers only when empty.
        """
        cols = [
            "device", "input_data", "block_index", "metric", "target", "block_id",
            "n_points", "n_out_of_bounds", "percentage_oob", "n_excluded", "status",
        ]
        if report_df.empty or "status" not in report_df.columns:
            new = pd.DataFrame(columns=cols)
        else:
            new = report_df[report_df["status"].isin(UNWAIVED_STATUSES)].copy()
            new.insert(0, "device", self.device_name)
            new = new.reindex(columns=cols)
        path.parent.mkdir(parents=True, exist_ok=True)
        new.to_csv(path, index=False)

        stale = pd.DataFrame(self.stale_exceptions, columns=["input_data", "block_index", "metric", "target"])
        stale.insert(0, "toolchain", self.exception_key)
        absent = set(map(tuple, self.absent_exceptions))
        stale["reason"] = ["curve not in this run (exit 1)" if tuple(map(str, k)) in absent
                           else "passes or not judged now" for k in self.stale_exceptions]
        stale.to_csv(path.parent / "stale_exceptions.csv", index=False)
        # row: row of the group's compact table (-1: the whole group or file)
        pd.DataFrame(self.simulation_errors, columns=["group", "row", "message"]).to_csv(
            path.parent / "simulation_errors.csv", index=False)

        if new.empty:
            logging.info(f"No new failures -- {path} written with headers only.")
        else:
            logging.warning(f"{len(new)} new failure row(s) written to {path}")
        if self.absent_exceptions:
            logging.error("%d exception(s) name a curve that is not in this run (lost coverage): %s",
                          len(self.absent_exceptions), "; ".join("/".join(k) for k in self.absent_exceptions[:5]))
        if self.stale_exceptions:
            logging.warning("%d exception(s) no longer needed (row passes): %s", len(self.stale_exceptions),
                            path.parent / "stale_exceptions.csv")

    def gen_summary_stats(
        self,
        report_df: pd.DataFrame,
        detailed_failures_df: pd.DataFrame,
        threshold: float = 0.0,
        tolerance_rel: float = 0.0,
        targets: Optional[List[str]] = None,
        final_summary_path: Optional[Path] = None,
    ) -> Dict[str, float]:
        """
        Count the judged curves per target, log the table and write `final_summary.md`.

        A waiver means "reviewed", not "good": waived curves are counted as FAILED. The column
        "of which waived" shows how many failures have an exactly matching exception and "new"
        how many do not (including rows that were not simulated); only those make the run exit 1
        (`n_failed_new` in the result).
        Rows with any other status (e.g. "Informative", "No points") are not judged: they are
        left out of the curve counts and shown in their own column.
        """
        targets = targets or ["meas", "tt"]
        rows = report_df[report_df["target"].isin(targets)]
        names = {"meas": "Measured", "tt": "Typical"}

        md = [
            "# Summary report\n",
            f"- **Device:** {self.device_name}",
            f"- **Toolchain:** {self.toolchain} (exceptions key `{self.exception_key}`)",
            f"- **Targets analyzed:** {', '.join(targets)}",
            f"- **Out-of-bound threshold:** {threshold:.2f}% of the points of a curve",
            f"- **Corner tolerance margin:** ±{tolerance_rel:.2f}% (widens the ss..ff band)",
            f"- **Clipped current threshold:** {self.clip_curr:.2e} A",
            "- **Waived curves count as failures** (a waiver means reviewed, not good).\n",
            "| Target | Curves | Passed | Failed | of which waived | new | Not judged | Points "
            "| Failed points | Fail % (curves) | Fail % (points) |",
            "|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
        ]
        logging.info("%-10s %8s %8s %8s %8s %8s %10s %10s %10s", "Target", "Curves", "Passed", "Failed",
                     "Waived", "New", "NotJudged", "Points", "FailPts")

        totals = {"n_curves": 0, "n_failed": 0, "n_waived": 0, "n_failed_new": 0, "n_not_judged": 0,
                  "n_points": 0, "n_oob": 0, "n_missing": 0}
        per_target: Dict[str, Dict[str, int]] = {}
        for target in targets:
            sub = rows[rows["target"] == target]
            if sub.empty:
                continue
            judged = sub["status"].astype(str).eq(PASSED) | sub["status"].astype(str).str.startswith("Failed")
            not_judged = int((~judged).sum())
            sub = sub[judged]
            status = sub["status"].astype(str)
            t = {
                "n_curves": len(sub),
                "n_failed": int(status.str.startswith("Failed").sum()),
                "n_waived": int(status.str.startswith("Failed (waived").sum()),
                "n_failed_new": int(status.isin(UNWAIVED_STATUSES).sum()),
                "n_not_judged": not_judged,
                "n_points": int(sub["n_points"].sum()),
                "n_oob": int(sub["n_out_of_bounds"].sum()),
                # measured points the simulation did not give (their curves are failed); counted
                # on the measured target only, so a point is not counted again for the tt target
                "n_missing": (int(sub["n_missing"].fillna(0).sum())
                              if "n_missing" in sub and target == "meas" else 0),
            }
            per_target[target] = t
            for k in totals:
                totals[k] += t[k]
            pct_curves = 100.0 * t["n_failed"] / t["n_curves"] if t["n_curves"] else 0.0
            pct_points = 100.0 * t["n_oob"] / t["n_points"] if t["n_points"] else 0.0
            name = names.get(target, target.upper())
            md.append(
                f"| {name} | {t['n_curves']} | {t['n_curves'] - t['n_failed']} | {t['n_failed']} | "
                f"{t['n_waived']} | {t['n_failed_new']} | {t['n_not_judged']} | {t['n_points']} | "
                f"{t['n_oob']} | {pct_curves:.2f}% | {pct_points:.2f}% |"
            )
            logging.info("%-10s %8d %8d %8d %8d %8d %10d %10d %10d", name, t["n_curves"],
                         t["n_curves"] - t["n_failed"], t["n_failed"], t["n_waived"], t["n_failed_new"],
                         t["n_not_judged"], t["n_points"], t["n_oob"])

        # The verification result is the measured target; the typical target (tt inside the ss..ff
        # band) is a check of the model corners and is reported on its own.
        m = per_target.get("meas", {k: 0 for k in totals})
        tt = per_target.get("tt")
        md.append(
            f"\n**Totals (measured target):** {m['n_curves']} curves, {m['n_curves'] - m['n_failed']} passed, "
            f"{m['n_failed']} failed ({m['n_waived']} of them waived, {m['n_failed_new']} new); "
            f"{m['n_not_judged']} not judged; {m['n_missing']} measured point(s) not simulated (per judged metric)."
            + (f" Typical target: {tt['n_failed']} of {tt['n_curves']} curves failed ({tt['n_failed_new']} new)."
               if tt else "")
            + f" Exceptions: {len(self.stale_exceptions)} stale, {len(self.absent_exceptions)} for curves not in this run."
        )
        logging.info("TOTALS: %d curves | passed %d | failed %d (waived %d, new %d) | stale exceptions %d",
                     totals["n_curves"], totals["n_curves"] - totals["n_failed"], totals["n_failed"],
                     totals["n_waived"], totals["n_failed_new"], len(self.stale_exceptions))
        if final_summary_path is not None:
            Path(final_summary_path).write_text("\n".join(md) + "\n")
            logging.info(f"Summary written to: {final_summary_path}")

        result = {k: float(v) for k, v in totals.items()}
        result["total_fail_rate_cases_pct"] = (
            100.0 * totals["n_failed"] / totals["n_curves"] if totals["n_curves"] else 0.0
        )
        return result

    # -------------------------------------------------------------------------
    # Main runner
    # -------------------------------------------------------------------------

    def _run_pipeline(
        self, waivers_dir: Optional[Path] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, float]]:
        """
        Run aggregate -> simulate -> range-check -> exceptions -> reports, and return
        `(full_res, detailed_failures, stats)`.

        Args:
            waivers_dir: Directory containing the `<device_name>.yaml` exception files.
                Defaults to `config["waivers_dir"]` or `./waivers` (relative to cwd,
                i.e. `$DEV/waivers` under the documented run recipe).
        """
        logging.info("Starting verification of device: %s", self.device_name)
        self._start_run()

        # Aggregate and simulate
        logging.info("Aggregating MDM data and running DC simulations ...")
        merged_dfs = self._aggregate_and_simulate()
        self.clean_results(merged_dfs)

        range_checker = self._build_range_checker()
        full_res, detailed_failures, stats = self._check_and_report(
            merged_dfs, range_checker,
            waivers_dir or Path(self.config.get("waivers_dir", "waivers")),
            threshold=self.config.get("threshold_percent_oob", 0),
            tolerance_rel=self.config.get("corner_tolerance_percent", 0.0),
        )
        # Remove the netlists of passing blocks (failing ones, waived or not, are kept).
        range_checker.cleanup_passed_netlists(
            self.output_dir / "netlists", full_res, dry_run=False
        )

        return full_res, detailed_failures, stats

    def _check_and_report(
        self, frames: List[pd.DataFrame], checker: RangeChecker, waivers_dir: Path,
        threshold: float, tolerance_rel: float,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, float]]:
        """
        The common end of every pipeline (DC, S-parameters, C-V): range-check the frames, write
        combined_results with the band columns, apply the exceptions of `waivers_dir`, and write
        final_reports (full_results, new_failures, stale_exceptions, simulation_errors,
        results_summary, failed_results, final_summary). Returns (full_res, detailed_failures, stats).
        """
        logging.info("Running range checking ...")
        full_res, detailed_failures = checker.analyze(pd.concat(frames, ignore_index=True))
        self.write_combined_results(frames, checker.bands)

        # Exceptions: a failing row is waived only on an exact reproduction (waivers/waiver.py).
        store = ExceptionStore.load(self.device_name, waivers_dir)
        full_res = self._apply_waivers(full_res, detailed_failures, store)

        reports_dir = self.output_dir / "final_reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        full_res.to_csv(reports_dir / "full_results.csv", index=False)
        self._write_new_failures(full_res, reports_dir / "new_failures.csv")
        checker.summarize_to_csv(full_res, detailed_failures,
                                 reports_dir / "results_summary.csv", reports_dir / "failed_results.csv")
        stats = self.gen_summary_stats(full_res, detailed_failures, threshold=threshold,
                                       tolerance_rel=tolerance_rel, targets=["meas", "tt"],
                                       final_summary_path=reports_dir / "final_summary.md")
        return full_res, detailed_failures, stats

    def run_verification(self) -> int:
        """
        Run the full verification pipeline.

        Returns:
            Exit code: 1 when any row is "Failed (new)" or "Failed (not simulated)" or a block
            could not be simulated, else 0. Waived rows are still failures in the reports, but
            they do not change the exit code.
        """
        _full_res, _detailed_failures, stats = self._run_pipeline()
        return self._exit_code(stats)

    def _exit_code(self, stats: Dict[str, float]) -> int:
        """1 if the run has new failures (no exactly matching exception) or simulation errors, else 0."""
        if self.simulation_errors:
            logging.error("%d block(s) could not be simulated (final_reports/simulation_errors.csv).",
                          len(self.simulation_errors))
            return 1
        if self.absent_exceptions:
            logging.error("%d exception(s) name a curve missing from this run (final_reports/stale_exceptions.csv).",
                          len(self.absent_exceptions))
            return 1
        if stats["n_failed_new"] > 0:
            logging.warning("Verification finished with %d NEW failure(s) (%d failure(s) in total).",
                            int(stats["n_failed_new"]), int(stats["n_failed"]))
            return 1
        logging.info("Verification finished: no new failures (%d failure(s) in total, all waived).",
                     int(stats["n_failed"]))
        return 0


# -------------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------------

def main() -> int:
    """
    Entry point for the MDM block verification flow.
    """
    parser = argparse.ArgumentParser(
        prog="mdm_verifier",
        description="Run MDM block verification (aggregate → simulate → range-check)."
    )
    parser.add_argument(
        "--config", "-c",
        type=Path,
        required=True,
        help="Path to the YAML configuration file for the verification flow."
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting MDM verification process...")
    logging.debug(f"Using configuration file: {args.config}")

    try:
        if not args.config.exists():
            logging.error(f"Configuration file not found: {args.config}")
            return 2

        verifier = MdmVerifier(args.config)
        result_code = verifier.run_verification()

        if result_code == 0:
            logging.info("MDM verification completed successfully.")
        else:
            logging.warning(f"MDM verification completed with non-zero exit code: {result_code}")

        return result_code

    except (ConfigError, VerificationError) as e:
        logging.error(f"Verification failed: {e}")
        return 2

    except KeyboardInterrupt:
        logging.warning("Verification interrupted by user.")
        return 130  # Conventional exit code for SIGINT

    except Exception as e:
        logging.exception(f"Unexpected error during verification: {e}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
