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
        self.device_type: str = self.config["device_type"]

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
        config.setdefault("max_workers", max(1, os.cpu_count() or 4))
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
            netlists_dir=(
                self.output_dir / "netlists"
                if (self.config.get("generate_netlists") and create_csvs)
                else None
            ),
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
        """Construct and configure the range checker."""
        threshold_percent = self.config.get("threshold_percent_oob")
        threshold_count = self.config.get("threshold_count_oob")

        default_threshold = (
            Threshold(max_out_of_range_percent=float(threshold_percent))
            if threshold_percent is not None
            else Threshold(max_out_of_range_count=int(threshold_count or 5))
        )

        metrics = [
            MetricSpec(
                name=m["name"],
                meas=m["meas"],
                tt=m["tt"],
                ss=m["ss"],
                ff=m["ff"],
                tolerance=Tolerance(
                    abs=float(self.config["tolerance_abs"]),
                    rel=float(self.config["tolerance_rel"]),
                ),
            )
            for m in self.config["metrics"]
        ]

        return RangeChecker(metrics=metrics, default_threshold=default_threshold)

    # -------------------------------------------------------------------------
    # Outputs
    # -------------------------------------------------------------------------

    def _save_results(self, dataframes: List[pd.DataFrame]) -> None:
        """
        Save one CSV file per run setup type.
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

            try:
                df.to_csv(fpath, index=False)
                logging.debug("Saved %d rows for setup '%s' → %s", len(df), setup_type, fpath)
            except Exception as e:
                logging.error("Failed to save results for setup '%s': %s", setup_type, e)

    def print_summary_statistics(
        self,
        report_df: pd.DataFrame,
        detailed_failures_df: pd.DataFrame,
        threshold_percent: float | None = None,
        threshold_count: int | None = None,
        targets: List[str] | None = None,
    ) -> Dict:
        """
        Print summary statistics for range check results.

        Args:
            report_df: Summary DataFrame with columns ['target', 'percentage_oob', 'n_out_of_bounds'].
            detailed_failures_df: DataFrame with detailed failure points (subset of report_df).
            threshold_percent: Threshold for percentage-based out-of-bound detection.
            threshold_count: Threshold for count-based out-of-bound detection.
            targets: List of targets to include (defaults to ["meas", "tt"]).

        Returns:
            Dictionary containing overall statistics and per-target breakdown.
        """
        if targets is None:
            targets = ["meas", "tt"]

        # Validation
        use_percent = threshold_percent is not None
        if not use_percent and threshold_count is None:
            raise ValueError("Either threshold_percent or threshold_count must be provided.")

        # Filter only requested targets
        target_report = report_df[report_df["target"].isin(targets)].copy()

        # Identify failing rows
        if use_percent:
            failing = target_report[target_report["percentage_oob"] > float(threshold_percent)]
        else:
            failing = target_report[target_report["n_out_of_bounds"] > int(threshold_count)]

        # Overall stats
        total_cases = len(target_report)
        total_fail = len(failing)
        total_pass = total_cases - total_fail

        total_failed_points = (
            len(detailed_failures_df[detailed_failures_df["target"].isin(targets)])
            if not detailed_failures_df.empty
            else 0
        )

        # Per-target stats
        target_stats = {}
        for target in targets:
            subset = target_report[target_report["target"] == target]
            if use_percent:
                failing_subset = subset[subset["percentage_oob"] > float(threshold_percent)]
            else:
                failing_subset = subset[subset["n_out_of_bounds"] > int(threshold_count)]

            target_stats[target] = {
                "total": len(subset),
                "pass": len(subset) - len(failing_subset),
                "fail": len(failing_subset),
            }

        # ---------- Logging ----------
        logging.info("\n================= SUMMARY =================")
        logging.info(f"Total cases (block_id × metric × target): {total_cases}")

        name_map = {"meas": "Measured", "tt": "Typical"}
        for target, stats in target_stats.items():
            target_name = name_map.get(target, target.upper())
            logging.info(
                f"  {target_name:8s} → TOTAL: {stats['total']:4d}, "
                f"PASS: {stats['pass']:4d}, FAIL: {stats['fail']:4d}"
            )

        logging.info(f"\nOverall PASS: {total_pass}")
        if use_percent:
            logging.info(f"Overall FAIL: {total_fail} "
                        f"(threshold: > {threshold_percent:.2f}% out-of-range)")
        else:
            logging.info(f"Overall FAIL: {total_fail} "
                        f"(threshold: > {int(threshold_count)} points out-of-range)")

        logging.info(f"Total failed points: {total_failed_points}")
        logging.info("==========================================================\n")

        # ---------- Return structured stats ----------
        return {
            "total_cases": total_cases,
            "total_pass": total_pass,
            "total_fail": total_fail,
            "total_failed_points": total_failed_points,
            "target_stats": target_stats,
            "threshold_type": "percent" if use_percent else "count",
            "threshold_value": threshold_percent if use_percent else threshold_count,
        }

    # -------------------------------------------------------------------------
    # Main runner
    # -------------------------------------------------------------------------

    def _filter_results(self, dataframes: List[pd.DataFrame]) -> List[pd.DataFrame]:
        return dataframes

    def run_verification(self) -> int:
        """
        Run the full verification pipeline.

        Returns:
            Exit code (0 = success, 1 = failures detected).
        """
        logging.info("Starting MDM block verification ...")
        logging.debug(f"Configuration: {self.config}")

        merged_dfs = self._aggregate_and_simulate()
        self._save_results(merged_dfs)

        # PreProcessing for merged results
        merged_df = pd.concat(merged_dfs, ignore_index=True)
        print(merged_df.columns.tolist())
        # merged_df = self._filter_results(merged_df)

        range_checker = self._build_range_checker()

        logging.info("Running range analysis ...")
        report, detailed_failures = range_checker.analyze(merged_df)

        reports_dir = self.output_dir / "final_reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        full_report = reports_dir / "full_report.csv"
        summary_csv = reports_dir / "summary.csv"
        failures_csv = reports_dir / "detailed_failures.csv"

        report.to_csv(full_report, index=False)
        range_checker.summarize_to_csv(
            report, detailed_failures, summary_csv, failures_csv
        )

        stats = self.print_summary_statistics(
            report,
            detailed_failures,
            threshold_percent=(
                float(self.config["threshold_percent_oob"])
                if self.config.get("threshold_percent_oob") is not None
                else None
            ),
            threshold_count=(
                int(self.config["threshold_count_oob"])
                if self.config.get("threshold_count_oob") is not None
                else None
            ),
            targets=["meas", "tt"],
        )

        if self.config.get("generate_netlists"):
            range_checker.cleanup_passed_netlists(
                self.output_dir / "netlists", report, dry_run=False
            )

        logging.info(f"- Full report: {full_report}")
        logging.info(f"- Summary    : {summary_csv}")
        if not detailed_failures.empty:
            logging.info(f"- Detailed failures: {failures_csv}")

        # Return non-zero if there are failing cases
        return 1 if stats["total_fail"] > 0 else 0


# -------------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MDM block verification (aggregate → simulate → range-check)."
    )
    parser.add_argument("--config", "-c", type=Path, required=True, help="Path to YAML config")
    args = parser.parse_args()

    try:
        verifier = MdmVerifier(args.config)
        return verifier.run_verification()
    except (ConfigError, VerificationError) as e:
        logging.error(str(e))
        return 2
    except Exception as e:
        logging.exception("Unexpected error during verification")
        return 3


if __name__ == "__main__":
    sys.exit(main())
