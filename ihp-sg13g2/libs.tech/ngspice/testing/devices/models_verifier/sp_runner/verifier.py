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

"""
Milestone M4 -- S-parameter verification orchestrator (CjE / CjC / fT).

Reuses the existing DC verification machinery as much as possible: it subclasses
`MdmVerifier` to inherit the M1 range-check bounds/window logic (`RangeChecker`), the
exact-value exceptions (`_apply_waivers`, `ExceptionStore`, key
`(input_data, block_index, metric, target)`), the `new_failures.csv` writer, the
CSV report writers and the Markdown summary generator. Only the *ingestion + build* of the
merged measured/simulated table is new (frequency-domain S-param -> scalar CjE/CjC/fT per
bias point), because the DC aggregate/simulate path does not apply to S-parameters.

Outputs are written under `<output_dir>/sparam/` (combined_results/, final_reports/) so the
DC results in `<output_dir>/` are left completely untouched.
"""

from __future__ import annotations

import logging
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from models_verifier.dc_runner.helper import CORNERS_BJT
from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance
from models_verifier.error_analyzer.range_checker import RangeChecker
from models_verifier.mdm_processing.sparam_parser import SparamData, parse_sparam_mdm
from models_verifier.models_verifier import MdmVerifier, VerificationError
from models_verifier.sp_runner.deembed import dummy_y, open_short
from models_verifier.sp_runner.extract import extract_metric, s_to_y
from models_verifier.sp_runner.sp_sweep_runner import SparamSweepRunner

# Default measured file stem per metric (overridable via config `sparam_files`).
_DEFAULT_FILES = {"cje": "spar_vb", "cjc": "spar_vc", "ft": "spar_vcb025"}
# Default MQA windows per characteristic (overridable via config `sparam_mqa_ranges`).
# CjC window is expressed as vcb=[-0.5,1.5], i.e. VBC in [-1.5,0.5].
_DEFAULT_MQA = {
    "spar_vb": {"cje": {"vbe": [-1.5, 0.5]}},
    "spar_vc": {"cjc": {"vcb": [-0.5, 1.5]}},
    "spar_vcb025": {"ft": {"vbe": [0.7, 0.96]}},
    "spar_vcb05": {"ft": {"vbe": [0.75, 0.83]}},
}


class SparamVerifier(MdmVerifier):
    """Extract + range-check HBT CjE/CjC/fT (measured vs simulated) within MQA windows."""

    def __init__(self, config_path: Path):
        super().__init__(config_path)

        self.sparam_metrics_cfg: List[Dict] = self.config.get("sparam_metrics", [])
        if not self.sparam_metrics_cfg:
            raise VerificationError(
                "No 'sparam_metrics' defined in config -- S-param verification needs "
                "cje/cjc/ft metric definitions."
            )
        self.sparam_mqa_ranges = self.config.get("sparam_mqa_ranges") or _DEFAULT_MQA
        # metric -> measured file stem, or a list of stems (e.g. fT at every measured VCB; each
        # file is its own curve, judged in its own `sparam_mqa_ranges` window).
        self.sparam_files: Dict[str, object] = self.config.get("sparam_files") or dict(_DEFAULT_FILES)
        # How a file's measured 2-port is taken (see `_measured_y`):
        #   sparam_self_deembed {stem: {open: <stem>, short: <stem>}}: de-embed the raw S again with
        #       these dummies (the file's S_deemb is a copy of another file's);
        #   sparam_copied_deemb [stems]: files whose S_deemb is known to be a copy; they are left
        #       out of the copy check of the other files;
        #   sparam_allow_raw [stems]: files without S_deemb whose raw S may be judged.
        self.self_deembed: Dict[str, Dict[str, str]] = self.config.get("sparam_self_deembed") or {}
        self.copied_deemb = set(self.config.get("sparam_copied_deemb") or []) | set(self.self_deembed)
        self.allow_raw = set(self.config.get("sparam_allow_raw") or [])
        self._sdeemb_cache: Dict[Path, Optional[np.ndarray]] = {}
        self.sp_template_path = Path(
            self.config.get("sp_template_path", "configs/hbt/hbt_sp.spice.j2")
        )
        self.corners = list(self.config.get("sparam_corners") or CORNERS_BJT)
        self.ac_dec = int(self.config.get("sparam_ac_dec", 20))
        self.f_start = float(self.config.get("sparam_f_start", 1e8))
        self.f_stop = float(self.config.get("sparam_f_stop", 65e9))
        self.subckt_name = self.config.get("sparam_subckt", self.device_name)

        # S-param exceptions live in a SEPARATE directory from the DC ones (the file name is the
        # device name in both); same schema and code (waivers/waiver.py).
        self.sparam_waivers_dir = Path(self.config.get("sparam_waivers_dir", "waivers/sparam"))

        # Redirect all S-param outputs to a dedicated subdir so DC results are untouched.
        self.dc_output_dir = self.output_dir
        self.output_dir = self.output_dir / "sparam"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # Ingestion + build of the merged measured/simulated table
    # -------------------------------------------------------------------------
    @staticmethod
    def _geom_from_design(design: Dict[str, object]) -> Dict[str, float]:
        def num(key, default):
            try:
                return float(design.get(key, default))
            except (TypeError, ValueError):
                return float(default)
        return {
            "W": num("W", 0.07),
            "L": num("L", 0.90),
            "Nx": num("Nx", 1),
            "M": num("M", 1),
        }

    def _files_of(self, metric: str) -> List[str]:
        """The measured file stems of a metric (`sparam_files` holds one stem or a list)."""
        files = self.sparam_files.get(metric)
        if not files:
            raise VerificationError(f"No S-param file mapped for metric '{metric}'.")
        return [files] if isinstance(files, str) else [str(f) for f in files]

    def _mdm(self, stem: str) -> Path:
        path = Path(self.config["mdm_dir"]) / f"{stem}.mdm"
        if not path.exists():
            raise VerificationError(f"Measured S-param file missing: {path}")
        return path

    def _sdeemb_of(self, path: Path) -> Optional[np.ndarray]:
        """All S_deemb values of a file as one array (None without S_deemb); cached."""
        if path not in self._sdeemb_cache:
            data = parse_sparam_mdm(path)
            self._sdeemb_cache[path] = (
                np.concatenate([bp.s.ravel() for bp in data.bias_points])
                if data.bias_points[0].s_source == "S_deemb" else None
            )
        return self._sdeemb_cache[path]

    def _check_not_a_copy(self, path: Path) -> None:
        """Stop when this file's S_deemb equals another spar_* file's of the same folder (copied data)."""
        mine = self._sdeemb_of(path)
        for other in sorted(path.parent.glob("spar_*.mdm")):
            if other == path or other.stem in self.copied_deemb:
                continue
            theirs = self._sdeemb_of(other)
            if theirs is not None and theirs.shape == mine.shape and np.array_equal(theirs, mine):
                raise VerificationError(
                    f"{path.name}: S_deemb is identical to {other.name}'s (copied data). Judge the "
                    f"genuine file; list a copy in sparam_copied_deemb, or in sparam_self_deembed to "
                    f"de-embed its raw S with the dummies."
                )

    def _measured_y(self, stem: str) -> Tuple[SparamData, List[np.ndarray], str]:
        """
        The measured 2-port Y of every bias point of one file, and where it comes from:
          "S_deemb"            IC-CAP's de-embedded S (normal case; checked not to be a copy);
          "S self-de-embedded" the raw S de-embedded again with the folder's open/short dummies
                               (files in `sparam_self_deembed`);
          "S"                  the raw S, only for files in `sparam_allow_raw`.
        """
        path = self._mdm(stem)
        if stem in self.self_deembed:
            data = parse_sparam_mdm(path, s_column="S")
            freq = data.bias_points[0].freq
            dummies = self.self_deembed[stem]
            y_open = dummy_y(self._mdm(dummies["open"]), freq)
            y_short = dummy_y(self._mdm(dummies["short"]), freq)
            ys = [open_short(s_to_y(bp.freq, bp.s), y_open, y_short) for bp in data.bias_points]
            return data, ys, "S self-de-embedded"

        if stem in self.copied_deemb:
            raise VerificationError(f"{path.name} is declared a copy (sparam_copied_deemb): its S_deemb is not "
                                    f"judged; list it in sparam_self_deembed to de-embed its raw S instead.")
        data = parse_sparam_mdm(path)
        source = data.bias_points[0].s_source
        if source == "S_deemb":
            self._check_not_a_copy(path)
        elif stem not in self.allow_raw:
            raise VerificationError(
                f"{path.name} has no de-embedded S (S_deemb); list it in sparam_allow_raw to judge its raw S."
            )
        return data, [s_to_y(bp.freq, bp.s) for bp in data.bias_points], source

    def _build_characteristic(
        self, metric: str, file_stem: str, runner: SparamSweepRunner
    ) -> pd.DataFrame:
        """
        Read one measured S-param file, extract measured `metric` per bias point, run the
        matching AC sim per corner, and merge into a long-format table the RangeChecker
        understands (node voltages + `<metric>_meas` + `<metric>_sim_<corner>`).
        """
        data, ys, source = self._measured_y(file_stem)
        geom = self._geom_from_design(data.design_params)
        # Same config-declared design-parameter overrides as the DC path (e.g. Nx).
        overrides = self.config.get("design_param_overrides") or {}
        for name, value in overrides.items():
            if name in geom:
                logging.warning("S-param %s: overriding %s=%s -> %s (design_param_overrides)",
                                metric, name, geom[name], value)
                geom[name] = float(value)
        temp = data.temp

        meas_rows: List[Dict] = []
        bias_records: List[Dict] = []
        for bp, y in zip(data.bias_points, ys):
            val = extract_metric(metric, bp.freq, y)
            node = {"vb": round(bp.vb, 9), "vc": round(bp.vc, 9),
                    "ve": round(bp.ve, 9), "vs": round(bp.vs, 9)}
            meas_rows.append({**node, f"{metric}_meas": val})
            bias_records.append(node)

        meas_df = pd.DataFrame(meas_rows)
        sim_df = runner.run(metric, bias_records, geom, temp=temp)
        for c in ("vb", "vc", "ve", "vs"):
            sim_df[c] = sim_df[c].round(9)

        # every measured bias point stays; one the simulation did not give counts as n_missing
        merged = meas_df.merge(sim_df, on=["vb", "vc", "ve", "vs"], how="left")
        if merged.empty:
            raise VerificationError(
                f"Meas/sim merge produced no rows for metric '{metric}' ({file_stem})."
            )

        merged["block_id"] = f"{self.device_name}_{file_stem}"
        merged["block_index"] = 0
        merged["input_data"] = f"{file_stem}.mdm"
        merged["output_vars"] = metric
        merged["master_setup_type"] = file_stem
        merged["temp"] = temp
        merged["deembedded"] = source
        return merged

    def _build_merged(self) -> List[pd.DataFrame]:
        import shutil

        work_dir = Path(tempfile.mkdtemp(prefix="ngspice_sp_"))
        try:
            runner = SparamSweepRunner(
                template_path=self.sp_template_path,
                corner_lib_path=Path(self.config["corner_lib_path"]),
                device_subckt=self.subckt_name,
                work_dir=work_dir,
                corners=self.corners,
                max_workers=int(self.config.get("max_workers", 8)),
                ac_dec=self.ac_dec,
                f_start=self.f_start,
                f_stop=self.f_stop,
            )
            frames: List[pd.DataFrame] = []
            for mspec in self.sparam_metrics_cfg:
                metric = mspec["name"]
                for stem in self._files_of(metric):
                    logging.info("Extracting S-param characteristic: %s (%s)", metric, stem)
                    frames.append(self._build_characteristic(metric, stem, runner))
            return frames
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

    def _build_sparam_range_checker(self) -> RangeChecker:
        threshold_percent = float(self.config.get("threshold_percent_oob", 0))
        tolerance_rel = float(self.config.get("corner_tolerance_percent", 0.0))
        metrics = [
            MetricSpec(
                name=m["name"],
                meas=m.get("meas"),
                tt=m.get("tt"),
                ss=m.get("ss"),
                ff=m.get("ff"),
                tolerance=Tolerance(abs=float(self.config["tolerance_abs"]), rel=tolerance_rel),
                valid_range=m.get("valid_range"),
                min_limit=m.get("min"),
                max_limit=m.get("max"),
            )
            for m in self.sparam_metrics_cfg
        ]
        return RangeChecker(
            metrics=metrics,
            default_threshold=Threshold(max_out_of_range_percent=threshold_percent),
            mqa_ranges=self.sparam_mqa_ranges,
        )

    # -------------------------------------------------------------------------
    # Pipeline
    # -------------------------------------------------------------------------
    def _run_sparam_pipeline(
        self, waivers_dir: Optional[Path] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, float]]:
        """
        Extract -> range-check -> exceptions -> reports and return
        `(full_res, detailed_failures, stats)` (mirrors `MdmVerifier._run_pipeline`).
        """
        self._start_run()
        frames = self._build_merged()
        full_res, detailed_failures, stats = self._check_and_report(
            frames, self._build_sparam_range_checker(), waivers_dir or self.sparam_waivers_dir,
            threshold=self.config.get("threshold_percent_oob", 0),
            tolerance_rel=self.config.get("corner_tolerance_percent", 0.0),
        )
        self._log_physical_sanity(frames)
        return full_res, detailed_failures, stats

    def run_verification(self) -> int:
        logging.info("Starting S-parameter verification of device: %s", self.device_name)
        _full_res, _detailed, stats = self._run_sparam_pipeline()
        return self._exit_code(stats)

    # -------------------------------------------------------------------------
    # Physical-sanity report (Acceptance b)
    # -------------------------------------------------------------------------
    def _log_physical_sanity(self, frames: List[pd.DataFrame]) -> None:
        logging.info("========== S-PARAM PHYSICAL-SANITY (device=%s) ==========", self.device_name)
        for df in frames:
            metric = str(df["output_vars"].iloc[0])
            stem = str(df["input_data"].iloc[0]).replace(".mdm", "")
            meas_col = f"{metric}_meas"
            if meas_col not in df.columns:
                continue
            vbe = (df["vb"] - df["ve"])
            vcb = (df["vc"] - df["vb"])
            win = (self.sparam_mqa_ranges.get(stem, {}) or {}).get(metric, {})
            mask = pd.Series(True, index=df.index)
            for var, (lo, hi) in win.items():
                series = {"vbe": vbe, "vcb": vcb, "vce": df["vc"] - df["ve"]}.get(var)
                if series is not None:
                    mask &= series.between(lo, hi)
            sub = df[mask]
            meas = pd.to_numeric(sub[meas_col], errors="coerce").dropna()
            if meas.empty:
                continue
            if metric == "ft":
                pk_i = meas.idxmax()
                logging.info(
                    "  fT  (%s): peak = %.1f GHz at VBE=%.3f V  [window %s, n=%d]",
                    stem, meas.loc[pk_i] / 1e9, float(vbe.loc[pk_i]), win, len(meas),
                )
            else:
                logging.info(
                    "  %s (%s): %.2f - %.2f fF over %s  [n=%d]",
                    metric.upper(), stem, meas.min() * 1e15, meas.max() * 1e15, win, len(meas),
                )
        logging.info("=========================================================")


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="sp_verifier",
        description="Run HBT S-parameter (CjE/CjC/fT) meas-vs-sim verification.",
    )
    parser.add_argument("--config", "-c", type=Path, required=True,
                        help="Path to the HBT YAML config (with sparam_metrics).")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    try:
        if not args.config.exists():
            logging.error("Configuration file not found: %s", args.config)
            return 2
        verifier = SparamVerifier(args.config)
        return verifier.run_verification()
    except VerificationError as e:
        logging.error("S-param verification failed: %s", e)
        return 2
    except Exception as e:  # pragma: no cover
        logging.exception("Unexpected error during S-param verification: %s", e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
