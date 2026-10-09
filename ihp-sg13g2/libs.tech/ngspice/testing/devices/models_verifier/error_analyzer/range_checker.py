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
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union
from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance
import numpy as np
import pandas as pd
import logging
from tqdm import tqdm


# -------------------------------------------------------------------------------------
# MQA bias-window support
# -------------------------------------------------------------------------------------
# Bias values recorded in the merged DataFrames are NODE voltages (e.g. vb, vc, ve for
# HBT; vg, vd, vs, vb for MOS), not the derived two-terminal quantities used by the MQA
# windows (vbe/vce/vcb, vgs/vds/vbs). Map each derived name to the pair of node columns
# used to compute it: derived = df[pos] - df[neg].
_NODE_BIAS_PAIRS: Dict[str, Tuple[str, str]] = {
    "vbe": ("vb", "ve"),
    "vce": ("vc", "ve"),
    "vcb": ("vc", "vb"),
    "vgs": ("vg", "vs"),
    "vds": ("vd", "vs"),
    "vbs": ("vb", "vs"),
}

# Strip a trailing MDM extension/suffix to obtain the "characteristic" stem used to key
# `RangeChecker.mqa_ranges`, e.g. "fg_vcb0_RF.mdm" -> "fg_vcb0". Matched exactly (not a
# prefix match) so "fg_vcb0" never matches "fg_vcb05".
_MDM_EXT_RE = re.compile(r"\.mdm$", re.IGNORECASE)
_MDM_RF_SUFFIX_RE = re.compile(r"_RF$", re.IGNORECASE)


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
    # Optional MQA bias-window gating, keyed by characteristic (normalized `input_data`
    # stem) -> metric name (or "_all") -> {bias_var: [min, max]}. e.g.:
    #   {"fg_vcb0": {"ib": {"vbe": [0.7, 0.8]}, "ic": {"vbe": [0.6, 0.96]}},
    #    "fo_vb": {"_all": {"vce": [0.2, 1.5], "vbe": [0.7, 0.9]}}}
    # When None (default) or when a group's characteristic/metric has no entry, NO
    # filtering happens and behavior is identical to before this feature existed.
    mqa_ranges: Optional[Dict[str, Dict[str, Dict[str, list]]]] = None

    def __post_init__(self) -> None:
        # Transient per-analyze() bookkeeping used only to emit a single summary log
        # line naming applied windows + excluded-point counts. Not part of the public
        # dataclass contract.
        self._window_defs: Dict[Tuple[str, str], dict] = {}
        self._window_excluded: Dict[Tuple[str, str], int] = {}

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

        # Fixed-limit fallback: metrics with no usable ss/ff envelope columns (e.g. a
        # limit-only metric such as a future S-param check) can instead declare fixed
        # min_limit/max_limit bounds. Returns constant Series so analyze() doesn't hit
        # the "Bounds missing" KeyError for these metrics.
        if spec.min_limit is not None or spec.max_limit is not None:
            lower_val = spec.min_limit if spec.min_limit is not None else float("-inf")
            upper_val = spec.max_limit if spec.max_limit is not None else float("inf")
            return (
                pd.Series(lower_val, index=group_dataframe.index),
                pd.Series(upper_val, index=group_dataframe.index),
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

    # -------------------------------------------------------------------------
    # MQA bias-window gating helpers
    # -------------------------------------------------------------------------
    @staticmethod
    def _normalize_characteristic(input_data: object) -> Optional[str]:
        """
        Normalize an `input_data` MDM filename to its characteristic stem, e.g.
        "fg_vcb0_RF.mdm" -> "fg_vcb0". Strips a trailing ".mdm" extension and then a
        trailing "_RF" suffix (both case-insensitive). Used for an EXACT dict-key
        lookup into `mqa_ranges`, so "fg_vcb0" never matches "fg_vcb05"/"fg_vcbm05".
        """
        if input_data is None or (isinstance(input_data, float) and pd.isna(input_data)):
            return None
        stem = _MDM_EXT_RE.sub("", str(input_data).strip())
        stem = _MDM_RF_SUFFIX_RE.sub("", stem)
        return stem or None

    def _resolve_characteristic_window(
        self, characteristic: Optional[str], metric_name: str
    ) -> Optional[Dict[str, list]]:
        """
        Look up the bias window for (characteristic, metric) in `mqa_ranges`, falling
        back to the characteristic's "_all" entry (applies to every metric of that
        characteristic). Returns None if `mqa_ranges` is unset or no key matches, which
        means "no filtering" (preserves current behavior exactly).
        """
        if not self.mqa_ranges or not characteristic:
            return None
        char_windows = self.mqa_ranges.get(characteristic)
        if not char_windows:
            return None
        return char_windows.get(metric_name) or char_windows.get("_all")

    @staticmethod
    def _derive_bias_series(group_df: pd.DataFrame, var_name: str) -> Optional[pd.Series]:
        """
        Derive a bias variable (e.g. "vbe") from NODE voltage columns already present
        in the merged DataFrame (e.g. "vb" - "ve"). HBT: VBE=vb-ve, VCE=vc-ve,
        VCB=vc-vb. MOS: VGS=vg-vs, VDS=vd-vs, VBS=vb-vs. If `var_name` is itself an
        existing column, it is used directly. Returns None if the needed column(s) are
        not present (caller treats that as "cannot filter on this var").
        """
        key = str(var_name).strip().lower()
        if key in group_df.columns:
            return pd.to_numeric(group_df[key], errors="coerce")

        pair = _NODE_BIAS_PAIRS.get(key)
        if pair is None:
            return None
        pos, neg = pair
        if pos not in group_df.columns or neg not in group_df.columns:
            return None
        return pd.to_numeric(group_df[pos], errors="coerce") - pd.to_numeric(
            group_df[neg], errors="coerce"
        )

    def _build_window_mask(
        self, group_df: pd.DataFrame, window: Dict[str, list]
    ) -> Tuple[pd.Series, List[str]]:
        """
        Build a boolean "in-window" mask (True = keep) over `group_df.index` from a
        window dict {bias_var: [min, max]}, ANDing across all listed bias vars. Bias
        vars whose columns cannot be derived are skipped (reported back in `missing`)
        rather than filtering everything out.
        """
        mask = pd.Series(True, index=group_df.index)
        missing: List[str] = []
        for var_name, bounds in window.items():
            series = self._derive_bias_series(group_df, var_name)
            if series is None:
                missing.append(var_name)
                continue
            lo, hi = bounds
            mask &= series.between(lo, hi)
        return mask, missing

    def _get_window_mask(
        self, group_df: pd.DataFrame, input_data: object, spec: MetricSpec
    ) -> Tuple[Optional[pd.Series], Optional[Dict[str, list]], Optional[str]]:
        """
        Resolve and build the combined bias-window mask for this group/metric, merging
        (a) the per-characteristic `mqa_ranges` window (keyed by normalized
        `input_data`) and (b) the metric's own flat `spec.valid_range`, if any. Returns
        (mask, window_dict, characteristic) or (None, None, characteristic) when
        neither source declares a window for this group/metric (no filtering).
        """
        characteristic = self._normalize_characteristic(input_data)
        combined_window: Dict[str, list] = {}

        char_window = self._resolve_characteristic_window(characteristic, spec.name)
        if char_window:
            combined_window.update(char_window)
        if spec.valid_range:
            combined_window.update(spec.valid_range)

        if not combined_window:
            return None, None, characteristic

        mask, missing = self._build_window_mask(group_df, combined_window)
        if missing:
            logging.warning(
                "MQA window for characteristic=%s metric=%s references bias var(s) %s "
                "that could not be derived from available columns; skipped for those "
                "var(s) only.",
                characteristic,
                spec.name,
                missing,
            )
        return mask, combined_window, characteristic

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
        pre_window_mask = lower_bound.notna() & upper_bound.notna() & target_values.notna()

        # MQA bias-window pre-filter: restrict comparison to points whose derived bias
        # values (vbe/vce/... from NODE voltages) fall inside the applicable window, if
        # any. Excluded points are neither counted nor failed. When no window applies
        # (mqa_ranges unset / no matching characteristic+metric / no spec.valid_range),
        # `window_mask` is None and behavior is identical to before this feature.
        window_mask, window, characteristic = self._get_window_mask(
            group_df, extras.get("input_data"), spec
        )
        if window_mask is not None:
            valid_mask = pre_window_mask & window_mask
            n_excluded = int((pre_window_mask & ~window_mask).sum())
            if n_excluded and target_type == "meas":
                key = (characteristic or "?", spec.name)
                self._window_defs[key] = window
                self._window_excluded[key] = self._window_excluded.get(key, 0) + n_excluded
        else:
            valid_mask = pre_window_mask
            n_excluded = 0

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
                "n_excluded": n_excluded,
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
            "n_excluded": n_excluded,
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

        # Milestone M2 (point-level granularity, consumed by M3): attach the failing
        # points' NODE-voltage bias coordinates, whichever of these columns exist for
        # this device type -- MOS: vg, vd, vb, vs; HBT: ve, vs, vc, vb. Both device
        # families may have "vs"; MOS additionally has "vg" (which HBT never does), so
        # simply checking column presence naturally attaches the right set without
        # needing a device_type flag here.
        for bias_col in ("vg", "vd", "vb", "vs", "vc", "ve"):
            if bias_col in group_dataframe.columns:
                failure_data[bias_col] = pd.to_numeric(
                    group_dataframe.loc[mask, bias_col], errors="coerce"
                ).astype(float).to_numpy()

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

        # Reset per-run MQA window bookkeeping (see __post_init__) so repeated calls to
        # analyze() on the same RangeChecker instance don't accumulate stale counts.
        self._window_defs = {}
        self._window_excluded = {}

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

        self._log_window_summary()

        return report_df, detailed_failures_df

    def _log_window_summary(self) -> None:
        """
        Emit a single INFO summary (once per analyze() run) naming every applied MQA
        bias window (characteristic/metric -> window) and its excluded-point count
        (measured target only, to avoid double-counting tt+meas for the same points).
        No-op if no windows were configured/applied.
        """
        if not self.mqa_ranges and not any(m.valid_range for m in self.metrics):
            return
        if not self._window_defs:
            logging.info(
                "MQA bias-window gating: configured but no group matched a "
                "characteristic/metric window (0 points excluded)."
            )
            return

        total_excluded = sum(self._window_excluded.values())
        logging.info(
            "MQA bias-window gating applied (characteristic/metric -> window : "
            "excluded points, measured target):"
        )
        for key in sorted(self._window_defs, key=lambda k: (k[0], k[1])):
            characteristic, metric_name = key
            window = self._window_defs[key]
            n_excluded = self._window_excluded.get(key, 0)
            logging.info(f"  {characteristic}/{metric_name} -> {window} : {n_excluded} excluded")
        logging.info(f"Total points excluded by MQA bias windows: {total_excluded}")

    def summarize_to_csv(
        self,
        report_df: pd.DataFrame,
        detailed_failures_df: pd.DataFrame,
        results_summary_path: Union[str, Path],
        failed_results_path: Union[str, Path],
    ) -> None:
        """
        Save both summary and detailed failure reports to CSV files.

        Milestone M2: when `report_df` carries a `status` column (`Passed` /
        `Passed (Waived)` / `Failed`, set by
        `models_verifier.py::MdmVerifier._apply_waivers`), the per (metric, target)
        summary additionally reports `n_passed` / `n_waived` / `n_failed` sweep
        counts. Absent `status` (e.g. a caller using `RangeChecker` standalone),
        behavior is identical to before Milestone M2.
        """
        if report_df.empty:
            return

        summary = report_df.groupby(["metric", "target"], as_index=False).agg(
            n_points=("n_points", "sum"),
            n_out_of_bounds=("n_out_of_bounds", "sum"),
        )

        if "status" in report_df.columns:
            status_counts = (
                report_df.groupby(["metric", "target", "status"])
                .size()
                .unstack(fill_value=0)
                .reset_index()
            )
            for col in ("Passed", "Passed (Waived)", "Failed"):
                if col not in status_counts.columns:
                    status_counts[col] = 0
            status_counts = status_counts.rename(
                columns={
                    "Passed": "n_passed",
                    "Passed (Waived)": "n_waived",
                    "Failed": "n_failed",
                }
            )
            summary = summary.merge(
                status_counts[["metric", "target", "n_passed", "n_waived", "n_failed"]],
                on=["metric", "target"],
                how="left",
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
