from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Dict, List

import pandas as pd
import yaml

from models_verifier.dc_runner.dc_sweep_runner import DcSweepRunner
from models_verifier.dc_runner.helper import SIM_TYPE_MAP, expand_env
from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance
from models_verifier.error_analyzer.range_checker import RangeChecker
from models_verifier.mdm_aggregator import MdmDirectoryAggregator


class MdmVerifier:
    """MDM block verification system that aggregates, simulates, and performs range checks."""

    def __init__(self, config_path: Path):
        """Initialize the verifier with configuration."""
        self.config = self._load_config(config_path)
        self.device_type = self.config["device_type"]
        self.output_dir = Path(
            self.config.get("output_dir", Path.cwd() / "verification_reports")
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: Path) -> Dict:
        """Load and validate configuration from YAML file."""
        if not config_path or not config_path.exists():
            print(f"ERROR: Config YAML '{config_path}' not found.", file=sys.stderr)
            sys.exit(2)

        config = yaml.safe_load(config_path.read_text())
        config = expand_env(config)

        required_keys = [
            "mdm_dir",
            "dc_template_path",
            "corner_lib_path",
            "device_type",
            "device_name",
            "metrics",
        ]

        missing = [
            k for k in required_keys if k not in config or config[k] in (None, "")
        ]
        if missing:
            print(
                f"ERROR: Missing required config keys in {config_path}: {missing}",
                file=sys.stderr,
            )
            sys.exit(2)

        config.setdefault("max_workers", max(1, os.cpu_count() or 4))
        config.setdefault("tolerance_abs", 0.0)
        config.setdefault("tolerance_rel", 0.0)
        config.setdefault("output_dir", str(Path.cwd() / "verification_reports"))

        return config

    def _clean_mkdir(self, path: Path) -> Path:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _build_merged_dataframes(self) -> List[pd.DataFrame]:
        """Build merged dataframes from MDM data and simulations."""
        mdm_dir = Path(self.config["mdm_dir"])
        if not mdm_dir.exists():
            print(f"ERROR: MDM directory not found: {mdm_dir}", file=sys.stderr)
            sys.exit(3)
        csv_stage_dir = self._clean_mkdir(self.output_dir.parent / "per_setup_mdm_csvs")
        aggregator = MdmDirectoryAggregator(
            input_dir=mdm_dir,
            recursive=True,
            output_dir=csv_stage_dir,
            create_csvs=True,
            device_type=self.device_type,
        )
        full_by_type, compact_by_type = aggregator.aggregate()
        if not compact_by_type:
            print("ERROR: No sweeps discovered in MDM directory.", file=sys.stderr)
            sys.exit(4)

        netlists_dir = None
        if "netlists_dir" in self.config and self.config["netlists_dir"]:
            netlists_dir = Path(self.config["netlists_dir"])
        runner = DcSweepRunner(
            template_path=Path(self.config["dc_template_path"]),
            corner_lib_path=Path(self.config["corner_lib_path"]),
            osdi_path=(
                Path(self.config["osdi_path"]) if self.device_type == "mos" else None
            ),
            device_name=self.config["device_name"],
            max_workers=int(self.config["max_workers"]),
            device_type=self.config["device_type"],
            netlists_dir=netlists_dir,
        )

        merged_parts = []
        with tempfile.TemporaryDirectory(prefix="ngspice_runs_") as work_dir:
            work_dir = Path(work_dir)
            for setup_type, compact_df in compact_by_type.items():
                sim_type = SIM_TYPE_MAP.get(setup_type, "current")
                if sim_type == "cap":
                    # print(f"======={setup_type}=======")
                    # print(
                    #     f"Skipping (master_setup_type: '{setup_type}') as it is a capacitance simulation."
                    # )
                    continue
                print(f"======={setup_type}=======")
                
                if compact_df is None or compact_df.empty:
                    continue

                full_df = full_by_type.get(setup_type)
                if full_df is None or full_df.empty:
                    continue

                try:
                    sim_df, errors = runner.run(compact_df)
                    print("errors", errors)
                    merged = runner.merge_with_clean(sim_df, full_df)
                    if not merged.empty:
                        merged_parts.append(merged)
                except Exception as e:
                    print("Error : ", setup_type, str(e))
                    continue

        if not merged_parts:
            print("ERROR: No merged sim-vs-measured rows produced.", file=sys.stderr)
            sys.exit(5)

        return merged_parts

    def _build_range_checker(self) -> RangeChecker:
        """Build and configure the range checker."""
        threshold_percent = self.config.get("threshold_percent_oob")
        threshold_count = self.config.get("threshold_count_oob")

        default_threshold = (
            Threshold(max_out_of_range_percent=float(threshold_percent))
            if threshold_percent is not None
            else Threshold(
                max_out_of_range_count=(
                    int(threshold_count) if threshold_count is not None else 5
                )
            )
        )

        metrics = [
            MetricSpec(
                name=metric["name"],
                meas=metric["meas"],
                tt=metric["tt"],
                ss=metric["ss"],
                ff=metric["ff"],
                tolerance=Tolerance(
                    abs=float(self.config["tolerance_abs"]),
                    rel=float(self.config["tolerance_rel"]),
                ),
            )
            for metric in self.config["metrics"]
        ]

        return RangeChecker(
            metrics=metrics,
            default_threshold=default_threshold,
        )

    def _save_individual_csvs(self, dataframes: List[pd.DataFrame]) -> None:
        """Save individual CSV files for each setup type."""
        output_dir = self.output_dir.parent / "per_setup_sim_vs_meas"
        output_dir.mkdir(parents=True, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        for df in dataframes:
            setup_type = str(df.loc[df.index[0], "master_setup_type"])
            filename = f"{setup_type}.csv".replace(" ", "_").replace("/", "-")
            filepath = os.path.join(output_dir, filename)
            df.to_csv(filepath, index=False)
            print(f"Saved {filepath}")

    def print_summary_statistics(
        self,
        report_df: pd.DataFrame,
        detailed_failures_df: pd.DataFrame,
        threshold_percent: float,
        targets: List[str] = None,
    ) -> Dict:
        """Print summary statistics for range check results."""
        if targets is None:
            targets = ["meas", "tt"]

        target_report = report_df[report_df["target"].isin(targets)].copy()
        failing = target_report[
            target_report["percentage_oob"] > threshold_percent
        ].copy()

        total_cases = int(len(target_report))
        total_fail = int(len(failing))
        total_pass = total_cases - total_fail
        total_failed_points = (
            int(
                detailed_failures_df[
                    detailed_failures_df["target"].isin(targets)
                ].shape[0]
            )
            if not detailed_failures_df.empty
            else 0
        )

        target_stats = {}
        for target in targets:
            target_data = report_df[report_df["target"] == target].copy()
            target_failing = target_data[
                target_data["percentage_oob"] > threshold_percent
            ].copy()

            target_stats[target] = {
                "total": int(len(target_data)),
                "pass": int(len(target_data)) - int(len(target_failing)),
                "fail": int(len(target_failing)),
            }

        print("\n================= SUMMARY =================")
        print(f"Total cases (block_id x metric x target): {total_cases}")

        for target in targets:
            stats = target_stats[target]
            target_name = (
                "Measured"
                if target == "meas"
                else "Typical" if target == "tt" else target.upper()
            )
            print(
                f"  {target_name} cases: {stats['total']} (PASS: {stats['pass']}, FAIL: {stats['fail']})"
            )

        print(f"  Overall PASS: {total_pass}")
        print(f"  Overall FAIL: {total_fail}  (limit = {threshold_percent:.2f}% OOB)")
        print(f"Total failed points: {total_failed_points}")
        print("==========================================================\n")

        return {
            "total_cases": total_cases,
            "total_pass": total_pass,
            "total_fail": total_fail,
            "total_failed_points": total_failed_points,
            "target_stats": target_stats,
            "threshold_percent": threshold_percent,
        }

    def run_verification(self) -> int:
        """Run the complete MDM block verification process."""
        print("Loading & merging data ...")
        merged_dataframes = self._build_merged_dataframes()

        self._save_individual_csvs(merged_dataframes)

        merged_df = pd.concat(merged_dataframes, ignore_index=True)

        print("Analyzing with RangeChecker ...")
        range_checker = self._build_range_checker()
        report, detailed_failures = range_checker.analyze(merged_df)

        full_report_path = self.output_dir / "full_report.csv"
        summary_path = self.output_dir / "summary.csv"
        detailed_failures_path = self.output_dir / "detailed_failures.csv"

        report.to_csv(full_report_path, index=False)
        range_checker.summarize_to_csv(
            report, detailed_failures, summary_path, detailed_failures_path
        )

        stats = self.print_summary_statistics(
            report,
            detailed_failures,
            float(self.config["threshold_percent_oob"]),
            targets=["meas", "tt"],
        )
        if self.config.get("netlists_dir"):
            range_checker.cleanup_passed_netlists(
                self.config["netlists_dir"], report, dry_run=False
            )

        print("Artifacts:")
        print(f"  - Full report     : {full_report_path}")
        print(f"  - Summary         : {summary_path}")
        if not detailed_failures.empty:
            print(f"  - Detailed failures: {detailed_failures_path}")

        # Return non-zero if there are failing cases
        return 1 if stats["total_fail"] > 0 else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run MDM block verification (aggregate → simulate → range-check)."
    )
    parser.add_argument("--config", "-c", help="Path to YAML config", required=True)
    args = parser.parse_args()

    verifier = MdmVerifier(Path(args.config))
    return verifier.run_verification()


if __name__ == "__main__":
    sys.exit(main())
