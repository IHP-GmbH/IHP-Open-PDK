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
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union
from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance
import numpy as np
import pandas as pd
import logging
from tqdm import tqdm


@dataclass
class RangeChecker:
    """
    Check metrics against range per group (sweep/curve).
    """

    metrics: Sequence[MetricSpec]
    default_threshold: Threshold = field(
        default_factory=lambda: Threshold(max_out_of_range_count=5)
    )
    output_vars_column: str = "output_vars"

    @staticmethod
    def _apply_tolerance_to_bounds(
        lower_bound: pd.Series, upper_bound: pd.Series, tolerance: Tolerance
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Apply absolute and relative tolerance adjustments to the given bounds.
        """
        if tolerance.abs == 0.0 and tolerance.rel == 0.0:
            return lower_bound, upper_bound

        rel = tolerance.rel / 100.0  # interpret as percentage
        adjusted_lower = lower_bound - tolerance.abs - rel * lower_bound.abs()
        adjusted_upper = upper_bound + tolerance.abs + rel * upper_bound.abs()
        return adjusted_lower, adjusted_upper

    def _get_metric_bounds(
        self, group_dataframe: pd.DataFrame, spec: MetricSpec
    ) -> Optional[Tuple[pd.Series, pd.Series]]:
        if (
            spec.ss
            and spec.ff
            and spec.ss in group_dataframe.columns
            and spec.ff in group_dataframe.columns
        ):
            lower_raw = pd.to_numeric(group_dataframe[spec.ss], errors="coerce")
            upper_raw = pd.to_numeric(group_dataframe[spec.ff], errors="coerce")
            lower_bound = np.minimum(lower_raw, upper_raw)
            upper_bound = np.maximum(lower_raw, upper_raw)
            return pd.Series(lower_bound, index=group_dataframe.index), pd.Series(
                upper_bound, index=group_dataframe.index
            )

        return None

    def _get_applicable_metrics(self, group_dataframe: pd.DataFrame) -> set:
        """
        Determine which metrics are applicable for this group based on output_vars column
        """
        default_metrics = {spec.name for spec in self.metrics}

        if (
            self.output_vars_column not in group_dataframe.columns
            or group_dataframe[self.output_vars_column].dropna().empty
        ):
            return default_metrics

        vars_str = group_dataframe[self.output_vars_column].dropna().iloc[0]
        if isinstance(vars_str, str):
            return set(v.strip() for v in vars_str.strip('"').split(","))

        return default_metrics

    def _process_target(
        self,
        group_df: pd.DataFrame,
        group_tuple: tuple,
        spec,
        target_type: str,
        target_col: str,
        bounds: Tuple[pd.Series, pd.Series],
        threshold,
        extras: dict,
    ):
        """
        Process a single target (tt or meas) and return summary + failure details.

        Parameters
        ----------
        group_df : pd.DataFrame
            DataFrame for the current block_id group.
        group_tuple : tuple
            Group identifier tuple.
        spec : MetricSpec
            Metric specification object with name, tolerance, etc.
        target_type : str
            Target type ("tt" or "meas").
        target_col : str
            Column in DataFrame containing target values.
        bounds : Tuple[pd.Series, pd.Series]
            (lower_bound, upper_bound) series.
        threshold : Threshold
            Threshold object used to check pass/fail.
        extras : dict
            Extra identifying information (e.g., input_data, block_index).

        Returns
        -------
        Tuple[dict, List[dict]]
            - report_row: Summary info for the metric/target.
            - failure_records: Detailed failure records for failing entries.
        """
        if not target_col or target_col not in group_df.columns:
            if target_col:
                raise KeyError(
                    f"{target_type.upper()} column '{target_col}' missing for '{spec.name}'"
                )
            return None, []

        lower_bound, upper_bound = bounds
        target_values = pd.to_numeric(group_df[target_col], errors="coerce")
        valid_mask = lower_bound.notna() & upper_bound.notna() & target_values.notna()
        total_count = int(valid_mask.sum())

        if total_count == 0:
            return {
                **extras,
                "block_id": group_tuple[0],
                "metric": spec.name,
                "target": target_type,
                "n_points": 0,
                "n_out_of_bounds": 0,
                "percentage_oob": 0.0,
                "passed": True,
            }, []

        # Identify out-of-bounds points
        oob_mask = ~target_values[valid_mask].between(
            lower_bound[valid_mask], upper_bound[valid_mask]
        )
        oob_count = int(oob_mask.sum())
        percent_oob = 100.0 * oob_count / total_count
        passed = threshold.check(oob_count, total_count)

        # Generate detailed failure records
        failure_records = self._get_failure_rep(
            group_df,
            group_tuple,
            spec,
            target_type,
            target_values,
            lower_bound,
            upper_bound,
            valid_mask,
            oob_mask,
        )

        report_row = {
            **extras,
            "block_id": group_tuple[0],
            "metric": spec.name,
            "target": target_type,
            "n_points": total_count,
            "n_out_of_bounds": oob_count,
            "percentage_oob": percent_oob,
            "passed": bool(passed),
        }

        return report_row, failure_records

    def _get_failure_rep(
        self,
        group_dataframe: pd.DataFrame,
        group_tuple: tuple,
        spec: MetricSpec,
        target_type: str,
        target_values: pd.Series,
        lower_bound: pd.Series,
        upper_bound: pd.Series,
        valid_mask: pd.Series,
        out_of_bounds_mask: pd.Series,
    ) -> List[Dict]:
        """
        Build a detailed failure report for metrics that fall outside their allowed bounds.

        Parameters
        ----------
        group_dataframe : pd.DataFrame
            DataFrame containing grouped evaluation data (one block/metric group).
            May contain optional columns such as 'input_data' and 'block_index'.
        group_tuple : tuple
            Identifier tuple for the current group (typically includes block_id, etc.).
        spec : MetricSpec
            Specification object describing the metric being evaluated.
        target_type : str
            Type of the evaluated target (e.g., "meas", "tt", etc.).
        target_values : pd.Series
            Series of evaluated metric values.
        lower_bound : pd.Series
            Series of lower bounds for the metric values.
        upper_bound : pd.Series
            Series of upper bounds for the metric values.
        valid_mask : pd.Series (bool)
            Boolean mask marking valid entries among the target values.
        out_of_bounds_mask : pd.Series (bool)
            Boolean mask marking which entries are outside the allowed bounds.

        Returns
        -------
        List[Dict]
            A list of dictionaries, each describing a failing entry.
            Returns an empty list if no values are out of bounds.
        """

        # Fast exit if nothing is out of bounds
        if not out_of_bounds_mask.any():
            return []

        # Restrict mask to valid entries only
        mask = valid_mask & out_of_bounds_mask

        # Select only failing entries
        vals = target_values[mask]
        lb = lower_bound[mask]
        ub = upper_bound[mask]

        # Compute deviation: positive distance beyond the nearest violated bound
        deviation = np.where(vals > ub, vals - ub, lb - vals)

        # Base failure data
        failure_data = {}

        # Attach optional column first
        if "input_data" in group_dataframe.columns:
            failure_data["input_data"] = np.full(
                vals.shape[0], group_dataframe["input_data"].iloc[0]
            )
        failure_data["block_id"] = group_tuple[0]
        if "block_index" in group_dataframe.columns:
            failure_data["block_index"] = group_dataframe.loc[mask, "block_index"].to_numpy()

        # Adding failure details
        failure_data.update({
            "metric": spec.name,
            "target": target_type,
            "value": vals.astype(float).to_numpy(),
            "lower_bound": lb.astype(float).to_numpy(),
            "upper_bound": ub.astype(float).to_numpy(),
            "deviation": deviation.astype(float),
        })

        # Return as list of dicts (records format)
        return pd.DataFrame(failure_data).to_dict("records")

    def analyze(self, data: Union[str, Path, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Analyze design metrics and generate reports.

        Parameters
        ----------
        data : Union[str, Path, pd.DataFrame]

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame]
            - report_df: Summary report with one row per (block_id, metric, target)
            - detailed_failures_df: Detailed failure report with one row per failed data point
        """
        # Load data if a path is provided
        if isinstance(data, (str, Path)):
            df = pd.read_csv(data)
        else:
            df = data

        # Validate input DataFrame
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        report_rows = []
        detailed_failures = []

        # Process each block_id group
        for group_key, group_df in df.groupby("block_id", dropna=False, sort=False):
            group_tuple = group_key if isinstance(group_key, tuple) else (group_key,)

            # Extract extra identifying fields if available
            extras = {
                k: (
                    group_df[k].dropna().iloc[0]
                    if k in group_df.columns and not group_df[k].dropna().empty
                    else None
                )
                for k in ("input_data", "block_index")
            }

            applicable_metrics = self._get_applicable_metrics(group_df)

            for spec in self.metrics:
                if spec.name not in applicable_metrics:
                    continue

                # Retrieve and adjust metric bounds
                bounds = self._get_metric_bounds(group_df, spec)
                if bounds is None:
                    raise KeyError(f"Bounds missing for metric '{spec.name}'")

                lower_bound, upper_bound = self._apply_tolerance_to_bounds(
                    *bounds, spec.tolerance
                )

                # Process both targets (tt, meas)
                for target_type, target_col in [("tt", spec.tt), ("meas", spec.meas)]:
                    result, failures = self._process_target(
                        group_df,
                        group_tuple,
                        spec,
                        target_type,
                        target_col,
                        (lower_bound, upper_bound),
                        self.default_threshold,
                        extras,
                    )
                    if result:
                        report_rows.append(result)
                    if failures:
                        detailed_failures.extend(failures)

        if not report_rows:
            raise ValueError("No valid metrics/columns to analyze.")

        report_df = pd.DataFrame(report_rows)
        detailed_failures_df = (
            pd.DataFrame(detailed_failures) if detailed_failures else pd.DataFrame()
        )

        return report_df, detailed_failures_df

    def summarize_to_csv(
        self,
        report_df: pd.DataFrame,
        detailed_failures_df: pd.DataFrame,
        results_summary_path: Union[str, Path],
        failed_results_path: Union[str, Path],
    ) -> None:
        """
        Save both summary and detailed failure reports to CSV files.
        """
        if report_df.empty:
            return

        summary = report_df.groupby(["metric", "target"], as_index=False).agg(
            n_points=("n_points", "sum"),
            n_out_of_bounds=("n_out_of_bounds", "sum"),
        )

        summary["percentage_oob"] = np.where(
            summary["n_points"] > 0,
            100.0 * summary["n_out_of_bounds"] / summary["n_points"],
            0.0,
        )

        summary = summary.sort_values(
            by=["percentage_oob", "n_out_of_bounds"],
            ascending=[False, False],
            kind="mergesort",
        )

        summary["percentage_oob"] = summary["percentage_oob"].round(3)
        logging.info(f"Summary report saved to: {results_summary_path}")
        summary.to_csv(results_summary_path, index=False)

        if not detailed_failures_df.empty:
            detailed_failures_df_sorted = detailed_failures_df.sort_values(
                "block_id", ascending=True
            )
            detailed_failures_df_sorted.to_csv(failed_results_path, index=False)
            logging.info(f"Detailed failure report saved to: {failed_results_path}")

    def assert_all_pass(
        self,
        report_df: pd.DataFrame,
        targets: Iterable[str] = ("meas", "tt"),
    ) -> None:
        """Raise AssertionError if any (metric, target) group fails.
        Summary includes totals + per-metric breakdown; details show only input_data & block_index.
        """
        if report_df.empty:
            return

        considered = report_df[report_df["target"].isin(list(targets))]
        if considered.empty:
            return

        failed = considered[~considered["passed"].astype(bool)]
        if failed.empty:
            return

        total_cases = int(considered.shape[0])
        total_failed = int(failed.shape[0])
        pass_rate = 100.0 * (total_cases - total_failed) / max(1, total_cases)

        summary_lines = [
            f"STATUS: {total_failed}/{total_cases} groups FAILED "
            f"({100.0 * total_failed / max(1, total_cases):.2f}%); "
            f"pass rate = {pass_rate:.2f}%"
        ]

        if {"metric", "target"}.issubset(failed.columns):
            counts = (
                failed.groupby(["metric", "target"])
                .size()
                .reset_index(name="fail_count")
                .sort_values(
                    ["fail_count", "metric", "target"], ascending=[False, True, True]
                )
            )
            for _, r in counts.iterrows():
                summary_lines.append(
                    f"  - {r['metric']}/{r['target']}: {int(r['fail_count'])} fails"
                )

        has_source = "input_data" in failed.columns
        has_block = "block_index" in failed.columns

        def _fmt(row):
            src_val = getattr(row, "input_data", None) if has_source else None
            blk_val = getattr(row, "block_index", None) if has_block else None
            src = (
                str(src_val) if src_val is not None and pd.notna(src_val) else "unknown"
            )
            blk = (
                str(blk_val) if blk_val is not None and pd.notna(blk_val) else "unknown"
            )
            return (
                f"[{row.metric}/{row.target}] "
                f"(FAIL file={src}, block_index={blk}) "
                f"n={int(row.n_points)} "
                f"out_of_bounds={int(row.n_out_of_bounds)} "
                f"({float(row.percentage_oob):.2f}%)"
            )

        rows_iter = failed.itertuples(index=False, name="Row")
        with ThreadPoolExecutor(max_workers=max(1, os.cpu_count())) as ex:
            detail_lines = list(ex.map(_fmt, rows_iter))

        raise AssertionError(
            "check failed:\n" + "\n".join(detail_lines + [""] + summary_lines)
        )

    def cleanup_passed_netlists(
        self,
        netlists_dir: Union[str, Path],
        report_df: pd.DataFrame,
        targets: Iterable[str] = ("meas", "tt"),
        dry_run: bool = False,
    ) -> Dict[str, int]:
        """
        Remove netlist files for block IDs that passed all their checks.

        Args:
            netlists_dir: Directory containing the saved netlists
            report_df: Report dataframe from analyze() method
            targets: Target types to consider (default: ("meas", "tt"))
            dry_run: If True, only report what would be deleted without actually deleting

        Returns:
            Dictionary with statistics: {'removed': count, 'kept': count, 'not_found': count}
        """
        netlists_path = Path(netlists_dir)
        if not netlists_path.exists():
            logging.warning(f"Netlists directory not found: {netlists_path}")
            return {"removed": 0, "kept": 0, "not_found": 0}

        # Identify passed blocks
        passed_blocks = self.get_passed_block_ids(report_df, targets)
        if not passed_blocks:
            logging.info("No passed blocks detected — keeping all netlists.")
            return {"removed": 0, "kept": 0, "not_found": 0}

        # Gather all .cir files
        netlist_files = sorted(netlists_path.glob("*.cir"))
        if not netlist_files:
            logging.warning(f"No .cir files found in directory: {netlists_path}")
            return {"removed": 0, "kept": 0, "not_found": 0}

        # Initialize statistics
        removed_count = 0
        kept_count = 0
        not_found_count = 0

        # Iterate with progress bar
        action_label = "Simulating removal" if dry_run else "Removing"
        logging.info(f"{action_label} of passed netlists in {netlists_path} ...")

        for netlist_file in tqdm(
            netlist_files,
            desc="Netlist Cleanup Progress",
            unit="file",
        ):
            filename = netlist_file.name

            # Extract block_id from filename convention: *_block-<id>.cir
            if "_block-" not in filename:
                logging.warning(f"Could not extract block_id from filename: {filename}")
                kept_count += 1
                continue

            block_id = filename.split("_block-")[1].replace(".cir", "")
            if block_id not in passed_blocks:
                kept_count += 1
                continue

            # Passed block → remove or simulate
            if dry_run:
                removed_count += 1
                continue

            try:
                netlist_file.unlink()
                removed_count += 1
            except FileNotFoundError:
                logging.error(f"File not found (already removed?): {netlist_file}")
                not_found_count += 1
            except Exception as e:
                logging.error(f"Error removing {netlist_file}: {e}")
                not_found_count += 1

        # Final statistics and summary
        stats = {
            "removed": removed_count,
            "kept": kept_count,
            "not_found": not_found_count,
        }

        logging.info("================ NETLIST CLEANUP SUMMARY ================")
        logging.info(f"  Directory      : {netlists_path}")
        logging.info(f"  Removed        : {removed_count} netlists for passed blocks")
        logging.info(f"  Kept           : {kept_count} netlists (failed/unrelated)")
        if not_found_count > 0:
            logging.error(f"  Not processed  : {not_found_count} files (errors or missing)")
        logging.info("=========================================================\n")

        return stats

    def get_passed_block_ids(
        self, report_df: pd.DataFrame, targets: Iterable[str] = ("meas", "tt")
    ) -> set:
        """
        Get set of block IDs that passed all metrics for the specified targets.

        Args:
            report_df: Report dataframe from analyze() method
            targets: Target types to consider (default: ("meas", "tt"))

        Returns:
            Set of block IDs that passed all metrics
        """
        if report_df.empty:
            return set()

        considered = report_df[report_df["target"].isin(list(targets))]
        if considered.empty:
            return set()

        block_status = considered.groupby("block_id")["passed"].all()
        passed_blocks = set(block_status[block_status].index)

        return passed_blocks
