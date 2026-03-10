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
from typing import Dict, List, Optional
import pandas as pd
import yaml

from models_verifier.dc_runner.dc_sweep_runner import DcSweepRunner
from models_verifier.dc_runner.helper import SIM_TYPE_MAP, expand_env
from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance
from models_verifier.error_analyzer.range_checker import RangeChecker
from models_verifier.mdm_processing.aggregator import MdmDirectoryAggregator


class ConfigError(Exception):
    """Raised when configuration loading or validation fails."""


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

        self.output_dir = Path(self.config["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._configure_logging()

    # -------------------------------------------------------------------------
    # Setup helpers
    # -------------------------------------------------------------------------

    def _configure_logging(self) -> None:
        """Configure logging to both console and file."""
        timestamp = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H_%M_%S")
        log_path = self.output_dir / f"models_verifier_{timestamp}.log"

        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler(sys.stdout),
            ],
            format="%(asctime)s | %(levelname)-7s | %(message)s",
            datefmt="%d-%b-%Y %H:%M:%S",
        )

    def _load_config(self, config_path: Path) -> Dict:
        """Load YAML config and validate required fields."""
        if not config_path or not config_path.exists():
            raise ConfigError(f"Config YAML '{config_path}' not found.")

        config = yaml.safe_load(config_path.read_text())
        config = expand_env(config)

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
        )
        full_by_type, compact_by_type = aggregator.aggregate()
        if not compact_by_type:
            raise VerificationError("No sweep data discovered in MDM directory.")

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
                # TODO: Support capacitor sims for FETs
                if sim_type == "cap":
                    continue

                logging.info(f"Processing simulation setup: {setup_type}")
                if compact_df.empty or full_by_type.get(setup_type) is None:
                    continue

                try:
                    sim_df, errors = runner.run(compact_df)
                    if errors:
                        logging.warning(f"Simulation errors for {setup_type}: {errors}")

                    merged = runner.merge_with_clean(sim_df, full_by_type[setup_type])
                    if not merged.empty:
                        merged_parts.append(merged)

                except Exception as e:
                    logging.error(f"Failed setup {setup_type}: {e}", exc_info=True)

        if not merged_parts:
            raise VerificationError("No merged sim-vs-measured rows produced.")

        return merged_parts

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
            )
            for m in self.config["metrics"]
        ]
        return RangeChecker(metrics=metrics, default_threshold=default_threshold)

    # -------------------------------------------------------------------------
    # Outputs
    # -------------------------------------------------------------------------

    def clean_results(self, dataframes: List[pd.DataFrame]) -> None:
        """
        Save one CSV file per run setup type, dropping the master_setup_type column,
        and clip current values for columns starting with 'i' and containing '_sim' or '_meas'.
        Mutates the original DataFrames in place.
        """
        output_dir = self.output_dir / "combined_results"
        output_dir.mkdir(parents=True, exist_ok=True)

        for df in dataframes:
            if df.empty:
                logging.warning("Skipping empty DataFrame in results saving.")
                continue

            setup_type = str(df.at[df.index[0], "master_setup_type"])
            safe_name = setup_type.replace(" ", "_").replace("/", "-")
            fpath = output_dir / f"{safe_name}.csv"

            # Drop metadata column in-place
            if "master_setup_type" in df.columns:
                df.drop(columns=["master_setup_type"], inplace=True)

            # Clip currents for all matching columns (in-place)
            current_cols = [
                col for col in df.columns
                if col.startswith("i") and ("_sim" in col or "_meas" in col)
            ]
            for col in current_cols:
                df[col] = df[col].clip(lower=self.clip_curr)
            logging.debug(f"Clipped currents are: {current_cols}")
            try:
                df.to_csv(fpath, index=False)
            except Exception as e:
                logging.error("Failed to save results for setup '%s': %s", setup_type, e)

    def gen_summary_stats(
        self,
        report_df: pd.DataFrame,
        detailed_failures_df: pd.DataFrame,
        threshold: float = 0.0,
        tolerance_rel: float = 0.0,
        targets: Optional[List[str]] = None,
        final_summary_path: str = None,
    ) -> Dict[str, float]:
        """
        Generate overall failure statistics from range-check results and optionally
        write a Markdown summary file.

        Args:
            report_df: DataFrame with columns
                ['target', 'percentage_oob', 'n_out_of_bounds', 'passed', 'n_points'].
            detailed_failures_df: DataFrame with detailed failure points.
            threshold: Threshold for percentage-based out-of-bound detection.
            targets: List of targets to include (defaults to ["meas", "tt"]).
            final_summary_path:Path to write summary file.

        Returns:
            Dictionary with:
                - total_fail_rate_cases_pct: overall % of failed sweeps
                - total_fail_rate_points_pct: overall % of failed simulation points
        """
        if report_df.empty:
            raise ValueError("`report_df` is empty — cannot generate summary statistics.")

        if targets is None:
            targets = ["meas", "tt"]

        logging.info("\n========== RANGE-CHECK SUMMARY ANALYSIS STARTED ==========")
        logging.info(f"Targets included: {targets}")
        logging.info(f"OOB detection threshold: {threshold:.2f}%")
        # Log the relative corner tolerance used to expand FF/SS bounds
        logging.info(
            f"Applying corner tolerance margin: ±{tolerance_rel:.2f}% "
            f"(expands FF/SS simulation envelopes)"
        )
        logging.info(f"Clipped current threshold: {self.clip_curr:.2e} A\n")

        # Filter for selected targets
        target_report = report_df[report_df["target"].isin(targets)].copy()
        if target_report.empty:
            logging.warning(f"No matching entries found for targets {targets}")
            return {
                "total_fail_rate_cases_pct": 0.0,
                "total_fail_rate_points_pct": 0.0,
            }

        # Initialize accumulators
        total_sweeps_all = 0
        total_failed_sweeps_all = 0
        total_points_all = 0
        total_failed_points_all = 0
        name_map = {"meas": "Measured", "tt": "Typical"}

        # Prepare Markdown output
        md_lines = []
        md_lines.append("# 📊 Summary Report\n")
        md_lines.append(f"- **Targets analyzed:** {', '.join(targets)}")
        md_lines.append(f"- **Out-of-bound threshold:** {threshold:.2f}%")
        md_lines.append(f"- **Corner tolerance margin:** ±{tolerance_rel:.2f}% (expands FF/SS simulation envelopes)")
        md_lines.append(f"- **Clipped current threshold:** {self.clip_curr:.2e} A\n")
        md_lines.append(
            "| Target | Sweeps | Pass | Fail | Total Points | Failed Points "
            "| Fail % (Cases) | Fail % (Points) |"
        )
        md_lines.append(
            "|:--------|--------:|------:|------:|--------------:|---------------:"
            "|----------------:|----------------:|"
        )

        # Console header
        header = (
            f"{'Target':<10} {'Sweeps':>8} {'Pass':>8} {'Fail':>8} "
            f"{'TotPts':>10} {'FailPts':>10} {'Fail%Cases':>12} {'Fail%Pts':>10}"
        )
        logging.info(header)
        logging.info("-" * len(header))

        for target in targets:
            subset = target_report[target_report["target"] == target]
            if subset.empty:
                logging.warning(f"No data for target '{target}' — skipping.")
                continue

            total_sweeps = len(subset)
            passed_sweeps = int(subset["passed"].sum())
            failed_sweeps = total_sweeps - passed_sweeps
            total_points_t = int(subset["n_points"].sum())
            failed_points_t = int(subset["n_out_of_bounds"].sum())

            if not detailed_failures_df.empty:
                failed_points_t += len(detailed_failures_df[detailed_failures_df["target"] == target])

            fail_rate_cases = (failed_sweeps / total_sweeps) * 100 if total_sweeps else 0
            fail_rate_points = (failed_points_t / total_points_t) * 100 if total_points_t else 0

            # Log to console
            tname = name_map.get(target, target.upper())
            logging.info(
                f"{tname:<10} "
                f"{total_sweeps:>8d} "
                f"{passed_sweeps:>8d} "
                f"{failed_sweeps:>8d} "
                f"{total_points_t:>10d} "
                f"{failed_points_t:>10d} "
                f"{fail_rate_cases:>12.2f} "
                f"{fail_rate_points:>10.2f}"
            )

            # Add to Markdown table
            md_lines.append(
                f"| {tname} | {total_sweeps} | {passed_sweeps} | {failed_sweeps} | "
                f"{total_points_t} | {failed_points_t} | {fail_rate_cases:.2f}% | {fail_rate_points:.2f}% |"
            )

            # Totals
            total_sweeps_all += total_sweeps
            total_failed_sweeps_all += failed_sweeps
            total_points_all += total_points_t
            total_failed_points_all += failed_points_t

        # Compute overall rates
        total_fail_rate_cases_pct = (
            (total_failed_sweeps_all / total_sweeps_all) * 100 if total_sweeps_all else 0
        )
        total_fail_rate_points_pct = (
            (total_failed_points_all / total_points_all) * 100 if total_points_all else 0
        )
        final_summary_path.write_text("\n".join(md_lines))
        logging.info(f"Summary written to: {final_summary_path}")

        # Return minimal metrics
        return {
            "total_fail_rate_cases_pct": total_fail_rate_cases_pct,
            "total_fail_rate_points_pct": total_fail_rate_points_pct,
        }

    # -------------------------------------------------------------------------
    # Main runner
    # -------------------------------------------------------------------------

    def run_verification(self) -> int:
        """
        Run the full verification pipeline.

        Returns:
            Exit code (0 = success, 1 = failures detected).
        """
        logging.info("Starting verification of device: %s", self.device_name)

        # Aggregate and simulate
        logging.info("Aggregating MDM data and running DC simulations ...")
        merged_dfs = self._aggregate_and_simulate()
        self.clean_results(merged_dfs)

        # PreProcessing for merged results
        merged_df = pd.concat(merged_dfs, ignore_index=True)
        range_checker = self._build_range_checker()

        logging.info("Running range checking on merged results ...")
        full_res, detailed_failures = range_checker.analyze(merged_df)

        reports_dir = self.output_dir / "final_reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        full_results = reports_dir / "full_results.csv"
        results_summary = reports_dir / "results_summary.csv"
        final_summary = reports_dir / "final_summary.md"
        failed_results = reports_dir / "failed_results.csv"

        logging.info(f"- Full report: {full_results}")
        full_res.to_csv(full_results, index=False)

        # Summary and failures
        range_checker.summarize_to_csv(
            full_res, detailed_failures, results_summary, failed_results
        )

        stats = self.gen_summary_stats(
            full_res,
            detailed_failures,
            threshold=self.config.get("threshold_percent_oob", 0),
            tolerance_rel=self.config.get("corner_tolerance_percent", 0.0),
            targets=["meas", "tt"],
            final_summary_path=final_summary,
        )
        # Cleanup netlists
        range_checker.cleanup_passed_netlists(
            self.output_dir / "netlists", full_res, dry_run=False
        )

        # Return non-zero if there are failing cases
        if stats["total_fail_rate_cases_pct"] > 0:
            logging.warning("Verification completed with FAILURES detected.")
            return 1
        else:
            logging.info("Verification completed successfully with NO FAILURES.")
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
