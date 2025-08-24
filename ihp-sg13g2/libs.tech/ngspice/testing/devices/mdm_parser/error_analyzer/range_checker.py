from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union
from mdm_parser.error_analyzer.config import MetricSpec, Threshold, Tolerance
import numpy as np
import pandas as pd


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

    def _ensure_dataframe(self, data: Union[str, Path, pd.DataFrame]) -> pd.DataFrame:
        if isinstance(data, (str, Path)):
            df = pd.read_csv(data)
            return df
        return data

    @staticmethod
    def _apply_tolerance_to_bounds(
        lower_bound: pd.Series, upper_bound: pd.Series, tolerance: Tolerance
    ) -> Tuple[pd.Series, pd.Series]:
        if tolerance.abs == 0.0 and tolerance.rel == 0.0:
            return lower_bound, upper_bound
        adjusted_lower = lower_bound - tolerance.abs - tolerance.rel * lower_bound.abs()
        adjusted_upper = upper_bound + tolerance.abs + tolerance.rel * upper_bound.abs()
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
        """Determine which metrics are applicable for this group based on output_vars column"""
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

    def _create_detailed_failure_report(
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
        if not out_of_bounds_mask.any():
            return []

        mask = valid_mask.copy()
        mask.loc[mask] = out_of_bounds_mask

        vals = target_values[mask]
        lo = lower_bound[mask]
        hi = upper_bound[mask]

        dev = np.where(vals > hi, vals - hi, lo - vals)

        data = {
            "block_id": group_tuple[0],
            "metric": spec.name,
            "target": target_type,
            "value": vals.astype(float).to_numpy(),
            "lower_bound": lo.astype(float).to_numpy(),
            "upper_bound": hi.astype(float).to_numpy(),
            "deviation": dev.astype(float),
        }

        if "source_file" in group_dataframe.columns:
            data["source_file"] = np.full(
                vals.shape[0], group_dataframe["source_file"].iloc[0]
            )
        if "block_index" in group_dataframe.columns:
            data["block_index"] = group_dataframe.loc[mask, "block_index"].to_numpy()

        return pd.DataFrame(data).to_dict("records")

    def analyze(
        self, data: Union[str, Path, pd.DataFrame]
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns:
            - report_df: Summary report with one row per (group, metric, target)
            - detailed_failures_df: Detailed failure report with one row per failed point
        """
        df = self._ensure_dataframe(data)
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        report_rows = []
        detailed_failures = []

        def _process_target(
            group_df, group_tuple, spec, target_type, target_col, bounds, threshold
        ):
            """Process a single target (tt or meas) and return report data."""
            if not target_col or target_col not in group_df.columns:
                if target_col:
                    raise KeyError(
                        f"{target_type.upper()} column '{target_col}' missing for '{spec.name}'"
                    )
                return None

            lower_bound, upper_bound = bounds
            target_values = pd.to_numeric(group_df[target_col], errors="coerce")
            valid_mask = (
                lower_bound.notna() & upper_bound.notna() & target_values.notna()
            )
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
                }

            oob_mask = ~target_values[valid_mask].between(
                lower_bound[valid_mask], upper_bound[valid_mask]
            )
            oob_count = int(oob_mask.sum())
            percent_oob = 100.0 * oob_count / total_count
            passed = threshold.check(oob_count, total_count)

            failure_records = self._create_detailed_failure_report(
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
            detailed_failures.extend(failure_records)

            return {
                **extras,
                "block_id": group_tuple[0],
                "metric": spec.name,
                "target": target_type,
                "n_points": total_count,
                "n_out_of_bounds": oob_count,
                "percentage_oob": percent_oob,
                "passed": bool(passed),
            }

        for group_key, group_df in df.groupby("block_id", dropna=False, sort=False):
            group_tuple = group_key if isinstance(group_key, tuple) else (group_key,)
            extras = {
                k: (
                    group_df[k].dropna().iloc[0]
                    if k in group_df.columns and not group_df[k].dropna().empty
                    else None
                )
                for k in ("source_file", "block_index")
            }
            applicable_metrics = self._get_applicable_metrics(group_df)

            for spec in self.metrics:
                if spec.name not in applicable_metrics:
                    continue

                bounds = self._get_metric_bounds(group_df, spec)
                if bounds is None:
                    raise KeyError(f"bounds missing for metric '{spec.name}'")

                lower_bound, upper_bound = self._apply_tolerance_to_bounds(
                    *bounds, spec.tolerance
                )

                for target_type, target_col in [("tt", spec.tt), ("meas", spec.meas)]:
                    result = _process_target(
                        group_df,
                        group_tuple,
                        spec,
                        target_type,
                        target_col,
                        (lower_bound, upper_bound),
                        self.default_threshold,
                    )
                    if result:
                        report_rows.append(result)

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
        csv_path: Union[str, Path] = "report.csv",
        detailed_csv_path: Union[str, Path] = "detailed_failures.csv",
    ) -> None:
        """
        Save both summary and detailed failure reports to CSV files.
        """
        if report_df.empty:
            empty_df = pd.DataFrame(
                columns=[
                    "metric",
                    "target",
                    "n_points",
                    "n_out_of_bounds",
                    "percentage_oob",
                ]
            )
            empty_df.to_csv(csv_path, index=False)
            return

        report_df.to_csv("report_df.csv", index=False)

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

        summary["percentage_oob"] = summary["percentage_oob"].round(2)
        summary.to_csv(csv_path, index=False)

        if not detailed_failures_df.empty:
            detailed_failures_df_sorted = detailed_failures_df.sort_values(
                "block_id", ascending=True
            )
            detailed_failures_df_sorted.to_csv(detailed_csv_path, index=False)
            print(f"Detailed failure report saved to: {detailed_csv_path}")

    def assert_all_pass(
        self,
        report_df: pd.DataFrame,
        targets: Iterable[str] = ("meas", "tt"),
    ) -> None:
        """Raise AssertionError if any (metric, target) group fails.
        Summary includes totals + per-metric breakdown; details show only source_file & block_index.
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
        if "source_file" in failed.columns:
            summary_lines.append(
                f"  Affected files : {failed['source_file'].dropna().nunique()}"
            )
        if "block_index" in failed.columns:
            summary_lines.append(
                f"  Affected blocks: {failed['block_index'].dropna().nunique()}"
            )

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

        has_source = "source_file" in failed.columns
        has_block = "block_index" in failed.columns

        def _fmt(row):
            src_val = getattr(row, "source_file", None) if has_source else None
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
        with ThreadPoolExecutor(max_workers=max(1, os.cpu_count() or 4)) as ex:
            detail_lines = list(ex.map(_fmt, rows_iter))

        raise AssertionError(
            "check failed:\n" + "\n".join(detail_lines + [""] + summary_lines)
        )


if __name__ == "__main__":
    metrics = [
        MetricSpec(  # IC
            "ic",
            meas="ic_meas",
            tt="ic_sim_hbt_typ",
            ss="ic_sim_hbt_bcs",
            ff="ic_sim_hbt_Wcs",
            # tolerance=Tolerance(abs=0.0, rel=0.0)  # optional
        ),
        MetricSpec(  # IE
            "ie",
            meas="ie_meas",
            tt="ie_sim_hbt_typ",
            ss="ie_sim_hbt_bcs",
            ff="ie_sim_hbt_Wcs",
        ),
        MetricSpec(  # VB
            "vb",
            meas="vb_meas",
            tt="vb_sim_hbt_typ",
            ss="vb_sim_hbt_bcs",
            ff="vb_sim_hbt_Wcs",
        ),
    ]
    analyzer = RangeChecker(
        metrics=metrics,
        default_threshold=Threshold(max_out_of_range_count=27),
    )

    report, detailed_failures = analyzer.analyze(
        "/home/marwan/Desktop/IHP-Open-PDK-Private/ihp-sg13g2/libs.tech/ngspice/testing/devices/all_measurements/results.csv"
    )

    analyzer.summarize_to_csv(
        report, detailed_failures, "summary.csv", "detailed_failures.csv"
    )
    try:
        analyzer.assert_all_pass(report, targets=("meas",))
    except Exception as e:
        print(e)
        pass
