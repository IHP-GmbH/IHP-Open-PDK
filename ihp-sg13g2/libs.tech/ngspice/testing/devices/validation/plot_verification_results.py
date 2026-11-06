#!/usr/bin/env python3
"""
Plot Device Verification Results (Batch CSVs)

This script generates comparison plots between measured silicon data and
simulation results for the device models.

Usage:
    python3 plot_verification_results.py --results <device results dir> --out <fig dir>
        plots <results>/combined_results/*.csv into <out>/<group>/<status>/ and, when present,
        <results>/cv/combined_results/*.csv into <out>/cv/ and <results>/sparam/combined_results/*.csv
        into <out>/sparam/ (each with the verdicts of its own final_reports). The status folder (passed,
        failed_new, failed_waived, informative, no_points) and the out-of-band markers come from the verifier's
        final_reports of that run, the acceptance band and the judged points (bias windows) from the
        <metric>_band_lo / _band_hi / _judged columns the verifier writes into combined_results;
        file names are <structure>_<group>_b<block>_<output>_<sweep>.png
    python3 plot_verification_results.py <csv_dir> <fig_output_dir>      (legacy positional form)

Example:
    python3 plot_verification_results.py --results models_results/<toolchain>/<case> --out figures/<case>
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import ScalarFormatter

# ---------------------------
# Helper Functions
# ---------------------------


MAX_POINT_LABELS = 5


def _worst_points(xs, ys, ref):
    """Return up to MAX_POINT_LABELS (x, y) pairs: the ones furthest from `ref` (relative), at least
    n / (2 * MAX_POINT_LABELS) sweep points apart.

    Without a reference the points are thinned evenly along the sweep instead.
    """
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n = len(xs)
    if n <= MAX_POINT_LABELS:
        return list(zip(xs, ys))
    if ref is not None:
        ref = np.asarray(ref, dtype=float)
        with np.errstate(divide="ignore", invalid="ignore"):
            dev = np.abs(ys - ref) / np.maximum(np.abs(ref), 1e-30)
        # Worst first, but keep the labelled points apart along the sweep so the labels do not overlap.
        gap = max(1, n // (2 * MAX_POINT_LABELS))
        chosen = []
        for k in np.argsort(np.nan_to_num(dev, nan=-1.0))[::-1]:
            if all(abs(int(k) - c) >= gap for c in chosen):
                chosen.append(int(k))
            if len(chosen) == MAX_POINT_LABELS:
                break
        idx = np.array(chosen)
    else:
        idx = np.linspace(0, n - 1, MAX_POINT_LABELS).round().astype(int)
    return [(xs[k], ys[k]) for k in sorted(set(idx.tolist()))]

def style_axes(ax: plt.Axes, sweep_var: str, output_var: str) -> None:
    """Standardize axes styling and auto-adjust limits with a clean grid."""
    ax.set_xlabel(str(sweep_var))
    ax.set_ylabel(str(output_var))

    ax.grid(which="major", linestyle="-", linewidth=0.8, alpha=0.6, color="#aaaaaa")
    ax.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.4, color="#bbbbbb")
    ax.minorticks_on()

    sf = ScalarFormatter(useMathText=True)
    sf.set_powerlimits((-3, 3))
    ax.yaxis.set_major_formatter(sf)

def outside_mask(y: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> np.ndarray:
    """Boolean mask for points outside bounds."""
    return (y < lo) | (y > hi)

def split_sim_columns(df: pd.DataFrame, out_first: str) -> Tuple[List[str], Optional[str], List[str]]:
    """Identify simulation columns for a particular output variable."""
    prefix = f"{out_first}_sim_"
    sim_cols = [c for c in df.columns if c.startswith(prefix)]
    if not sim_cols:
        return [], None, []
    typ_candidates = [c for c in sim_cols if c.split("_")[-1].lower() in {"typ", "tt", "typical"}]
    typ_col = typ_candidates[0] if typ_candidates else None
    others = [c for c in sim_cols if c != typ_col]
    return sim_cols, typ_col, others

def parse_block_outputs(block: pd.DataFrame) -> List[str]:
    """Extract output variable names from 'output_vars' column."""
    if "output_vars" not in block.columns or pd.isna(block["output_vars"].iloc[0]):
        return []
    return [s.strip() for s in str(block["output_vars"].iloc[0]).split(",") if s.strip()]


# ---------------------------
# Verdicts from the verifier's final reports
# ---------------------------
# Status of a row (models_verifier/waivers/waiver.py) -> figure folder. Waived curves are failures
# too: they go to failed_waived (reviewed, not good), new failures to failed_new.
_STATUS_FOLDER = {"Failed (not simulated)": "failed_not_simulated", "Failed (new)": "failed_new",
                  "Failed (waived, auto, pending review)": "failed_waived",
                  "Failed (waived, approved)": "failed_waived", "Passed": "passed",
                  "Informative": "informative", "No points": "no_points"}
# When aliases of one output (e.g. "<output>_sub") have different statuses, the figure takes the worst.
_STATUS_RANK = {"Failed (not simulated)": 6, "Failed (new)": 5, "Failed (waived, auto, pending review)": 4,
                "Failed (waived, approved)": 3, "Passed": 2, "Informative": 1, "No points": 0}
_BIAS_COL_RE = re.compile(r"^v[a-z0-9]*$")


class Verdicts:
    """Per-block verdicts of the measured target, read from ``final_reports/full_results.csv`` and
    ``final_reports/failed_results.csv`` of a verification run. A metric that aliases an output variable
    (``<output>_sub`` judging the same column in another bias window) is folded into that output: a block is
    "failed" for an output when any metric on it failed, and every out-of-band point of every such
    metric is marked."""

    def __init__(self, results_dir: Path):
        fr = results_dir / "final_reports"
        self.status: Dict[Tuple[str, int, str], str] = {}
        # failing points per (file, block, metric): (bias dict, simulated?) -- a measured point the
        # simulation did not give is listed with an empty band
        self.oob: Dict[Tuple[str, int, str], List[Tuple[dict, bool]]] = defaultdict(list)
        full = fr / "full_results.csv"
        if full.exists():
            f = pd.read_csv(full)
            f = f[f["target"].astype(str) == "meas"]
            for r in f.itertuples(index=False):
                self.status[(str(r.input_data), int(r.block_index), str(r.metric))] = str(r.status)
        failed = fr / "failed_results.csv"
        if failed.exists() and failed.stat().st_size > 0:
            try:
                d = pd.read_csv(failed)
            except pd.errors.EmptyDataError:
                d = pd.DataFrame()
            if not d.empty and "target" in d.columns:
                d = d[d["target"].astype(str) == "meas"]
                bias_cols = [c for c in d.columns if _BIAS_COL_RE.match(str(c))]
                for r in d.itertuples(index=False):
                    key = (str(r.input_data), int(r.block_index), str(r.metric))
                    bias = {c: round(float(getattr(r, c)), 9) for c in bias_cols if pd.notna(getattr(r, c))}
                    self.oob[key].append((bias, pd.notna(getattr(r, "lower_bound", np.nan))))

    def _metrics_for(self, out_name: str) -> List[str]:
        return sorted({m for (_, _, m) in self.status if m == out_name or m.startswith(out_name + "_")})

    def lookup(self, input_data: str, block_index: int, out_name: str, sweep_var: str):
        """(status, out-of-band sweep values, not-simulated sweep values) of one block and output;
        (None, set(), set()) when the reports do not have it."""
        best, oob_x, missing_x = None, set(), set()
        for m in self._metrics_for(out_name):
            st = self.status.get((input_data, block_index, m))
            if st is None:
                continue
            if best is None or _STATUS_RANK.get(st, 0) > _STATUS_RANK.get(best, 0):
                best = st
            for bias, simulated in self.oob.get((input_data, block_index, m), []):
                if sweep_var in bias:
                    (oob_x if simulated else missing_x).add(bias[sweep_var])
        return best, oob_x, missing_x


def figure_stem(block: pd.DataFrame, block_id: str) -> str:
    """
    Readable, run-independent and unique file stem: ``<structure>_<group>_<temp>_b<block_index>`` for
    IC-CAP names ``<device>~<structure>~<group>~<temp>.mdm`` (the same structure is measured at several
    temperatures), ``<file stem>_b<block_index>`` for other names, the block id only without a source file.
    """
    src = str(block["input_data"].iloc[0]) if "input_data" in block.columns else ""
    parts = src.replace(".mdm", "").split("~")
    idx = int(block["block_index"].iloc[0]) if "block_index" in block.columns else 0
    if len(parts) >= 3:
        return f"{'_'.join(parts[1:])}_b{idx}"
    if src:
        return f"{parts[0]}_b{idx}"
    return str(block_id)


# Geometry columns shown in a figure title when the table has them (header values of the block).
TITLE_COLUMNS = ("w", "l", "nf", "nx", "ny", "m", "a", "p", "ac", "pc")


def format_panel_title(block: pd.DataFrame, out_name: str) -> str:
    """Figure title: output, source file, temperature and the block's geometry columns."""
    row = block.iloc[0]
    parts = [f"{c}={row[c]:.4g}" if isinstance(row[c], float) else f"{c}={row[c]}"
             for c in TITLE_COLUMNS if c in block.columns and pd.notna(row.get(c, np.nan))]
    t_str = f"T={row['temp']}°C" if 'temp' in block.columns and pd.notna(row.get('temp', np.nan)) else ""
    src_str = str(row['input_data']) if 'input_data' in block.columns and pd.notna(row.get('input_data', np.nan)) else ""
    left = " — ".join(filter(None, [out_name.upper(), f"[{src_str}]" if src_str else None]))
    right = " — " + " | ".join(filter(None, [t_str] + parts)) if (t_str or parts) else ""
    return left + right


def ensure_sweep_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    DC `combined_results/*.csv` carry `sweep_var`, `output_vars` and `block_id`. The C-V tables
    have no `sweep_var` but list the swept bias first in `input_vars` (e.g. "vbc,ve"). The
    S-parameter tables (cje / cjc / ft versus bias) have neither; there the sweep is the
    bias column (v...) that changes the most, so those files plot exactly like the DC ones.
    """
    df = df.copy()
    if "sweep_var" not in df.columns:
        first = (str(df["input_vars"].dropna().iloc[0]).split(",")[0].strip()
                 if "input_vars" in df.columns and df["input_vars"].notna().any() else "")
        bias = [c for c in df.columns if _BIAS_COL_RE.match(str(c)) and pd.api.types.is_numeric_dtype(df[c])]
        if first in df.columns:
            df["sweep_var"] = first
        elif bias:
            df["sweep_var"] = max(bias, key=lambda c: df[c].nunique())
    if "output_vars" not in df.columns:
        df["output_vars"] = ",".join(sorted(c[:-5] for c in df.columns if c.endswith("_meas")))
    if "block_id" not in df.columns:
        src = df["input_data"].astype(str) if "input_data" in df.columns else pd.Series(["block"] * len(df))
        idx = df["block_index"].astype(str) if "block_index" in df.columns else pd.Series(["0"] * len(df))
        df["block_id"] = src + "_" + idx
    return df

# ---------------------------
# Main Plotting Routine
# ---------------------------

COLORS = {"band": "#9DB7D5", "window": "#E8E8E8", "tt": "#000000", "meas": "#4D4D4D", "fail": "#D55E00"}


def acceptance_bands(block: pd.DataFrame, out_name: str) -> List[Tuple[str, np.ndarray, np.ndarray, np.ndarray]]:
    """
    The band of every metric judged on this output, as the range checker used it: the verifier
    writes <metric>_band_lo, <metric>_band_hi and <metric>_judged into combined_results. A metric
    belongs to the output when its name is the output's or starts with it plus "_" (an alias metric
    such as "<output>_sub" judges the same column in another bias window). Returns [(metric, lo, hi, judged)].
    """
    bands = []
    for col in block.columns:
        if not col.endswith("_band_lo"):
            continue
        metric = col[: -len("_band_lo")]
        if metric == out_name or metric.startswith(out_name + "_"):
            judged = block[f"{metric}_judged"].astype(str).str.lower().eq("true").to_numpy()
            bands.append((metric, block[col].to_numpy(dtype=float), block[f"{metric}_band_hi"].to_numpy(dtype=float), judged))
    return bands


def _spans(x: np.ndarray, mask: np.ndarray) -> List[Tuple[float, float]]:
    """x ranges of the runs of consecutive True values of `mask` (x sorted), extended halfway to the neighbours."""
    spans, n, i = [], len(x), 0
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and mask[j + 1]:
            j += 1
        left = (x[i - 1] + x[i]) / 2 if i > 0 else x[i]
        right = (x[j] + x[j + 1]) / 2 if j < n - 1 else x[j]
        spans.append((left, right))
        i = j + 1
    return spans


def plot_single_block(args):
    """
    One figure: the measured points, the typical (tt) simulation, the acceptance band of every
    metric on this output where it was judged, grey spans over points no metric judged (outside
    the bias windows), the out-of-band measured points of the verdict (filled) and the measured points
    the simulation did not give (crosses). The figure goes to the folder of the block's status
    (failed_not_simulated, failed_new, failed_waived, passed, ...).
    """
    block_id, out_name, block, fig_dir, verdict = args
    sweep_var = str(block["sweep_var"].iloc[0])
    block_sorted = block.sort_values(sweep_var)
    x = block_sorted[sweep_var].to_numpy(dtype=float)
    meas_col = f"{out_name}_meas"
    _sim_cols, typ_col, _others = split_sim_columns(block_sorted, out_name)
    y_meas = block_sorted[meas_col].to_numpy(dtype=float) if meas_col in block_sorted.columns else None
    bands = acceptance_bands(block_sorted, out_name)

    verdict_status, verdict_oob, verdict_missing = verdict if verdict is not None else (None, set(), set())
    missing_mask = np.isin(np.round(x, 9), list(verdict_missing))
    if verdict_status is not None:
        meas_mask = np.isin(np.round(x, 9), list(verdict_oob))
        folder = _STATUS_FOLDER.get(verdict_status, verdict_status.lower().replace(" ", "_"))
    else:   # no final_reports: mark measured points outside a band where it was judged
        meas_mask = np.zeros(len(x), dtype=bool)
        if y_meas is not None:
            for _m, lo, hi, judged in bands:
                meas_mask |= judged & outside_mask(y_meas, lo, hi)
        folder = "failed" if meas_mask.any() else "passed"
    block_fig_dir = fig_dir / folder
    block_fig_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    judged_any = np.zeros(len(x), dtype=bool)
    for _metric, lo, hi, judged in bands:
        ax.fill_between(x, lo, hi, where=judged, color=COLORS["band"], alpha=0.6, linewidth=0,
                        label="acceptance band (judged points)")
        judged_any |= judged
    if bands:
        for left, right in _spans(x, ~judged_any):
            ax.axvspan(left, right, color=COLORS["window"], zorder=0, linewidth=0, label="not judged")
    if typ_col is not None:
        ax.plot(x, block_sorted[typ_col].to_numpy(dtype=float), "-", color=COLORS["tt"], linewidth=1.4,
                label="typical (tt) simulation")
    if y_meas is not None:
        ax.plot(x, y_meas, "o", mfc="none", mec=COLORS["meas"], markersize=4, label="measured")
        ax.plot(x[meas_mask], y_meas[meas_mask], "o", color=COLORS["fail"], markersize=5,
                label=f"measured out of band ({int(meas_mask.sum())} points)")
        if missing_mask.any():
            ax.plot(x[missing_mask], y_meas[missing_mask], "x", color=COLORS["fail"], markersize=6,
                    markeredgewidth=1.4, label=f"measured, not simulated ({int(missing_mask.sum())} points)")
        # Only the MAX_POINT_LABELS points furthest from the typical simulation are labelled.
        ref = block_sorted[typ_col].to_numpy(dtype=float)[meas_mask] if typ_col is not None else None
        for xi, yi in _worst_points(x[meas_mask], y_meas[meas_mask], ref):
            ax.annotate(f"({xi:.2e}, {yi:.2e})", xy=(xi, yi), xytext=(10, 0),
                        textcoords="offset points", ha="left", va="center", fontsize=6)

    ax.set_title(format_panel_title(block, out_name), fontsize=9)
    style_axes(ax, sweep_var, out_name)
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))        # one legend entry per label
    ax.legend(unique.values(), unique.keys(), fontsize=8, frameon=False, loc="best")

    fig_path = block_fig_dir / f"{figure_stem(block, block_id)}_{out_name}_{sweep_var}.png".replace(" ", "_")
    fig.tight_layout()
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)
    return fig_path


def plot_blocks_comparison(df: pd.DataFrame, fig_dir: Path, max_workers: int = 8,
                           verdicts: Optional[Verdicts] = None):
    # Prepare list of tasks
    tasks = []
    for block_id in pd.unique(df["block_id"]):
        block = df[df["block_id"] == block_id]
        if block.empty:
            continue
        for out_name in parse_block_outputs(block):
            verdict = None
            if verdicts is not None and "input_data" in block.columns and "block_index" in block.columns:
                verdict = verdicts.lookup(str(block["input_data"].iloc[0]), int(block["block_index"].iloc[0]),
                                         out_name, str(block["sweep_var"].iloc[0]))
                if verdict[0] is None:
                    verdict = None
            tasks.append((block_id, out_name, block.copy(), fig_dir, verdict))

    saved_files = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for fig_path in tqdm(executor.map(plot_single_block, tasks), total=len(tasks), desc="Generating figures"):
            saved_files.append(fig_path)

    print(f"\nTotal figures saved: {len(saved_files)}")

# ---------------------------
# CLI Entry Point
# ---------------------------

def plot_csv_dir(csv_dir: Path, output_dir: Path, max_workers: int,
                 verdicts: Optional[Verdicts] = None) -> int:
    """Plot every CSV of one combined_results directory; returns the number of CSVs processed."""
    output_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for csv_file in sorted(csv_dir.glob("*.csv")):
        print(f"\nProcessing CSV: {csv_file}")
        df = pd.read_csv(csv_file)
        if df.empty:
            print("  (empty, skipped)")
            continue
        df = ensure_sweep_columns(df)
        csv_fig_dir = output_dir / csv_file.stem
        csv_fig_dir.mkdir(parents=True, exist_ok=True)
        plot_blocks_comparison(df, csv_fig_dir, max_workers=max_workers,
                               verdicts=verdicts)
        n += 1
    return n


def main():
    ap = argparse.ArgumentParser(description="Measured-vs-simulated figures from combined_results CSVs.")
    ap.add_argument("--results", type=Path, default=None,
                    help="device results directory (uses <results>/combined_results, <results>/cv/... and <results>/sparam/...)")
    ap.add_argument("--out", type=Path, default=None, help="figure output directory")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("positional", nargs="*", help="legacy form: <csv_dir> <fig_output_dir>")
    args = ap.parse_args()

    if args.results is not None:
        if args.out is None:
            ap.error("--out is required with --results")
        jobs = []
        dc = args.results / "combined_results"
        if dc.is_dir():
            jobs.append((dc, args.out, Verdicts(args.results)))
        for tier in ("cv", "sparam"):
            tier_dir = args.results / tier / "combined_results"
            if tier_dir.is_dir():
                jobs.append((tier_dir, args.out / tier, Verdicts(args.results / tier)))
        if not jobs:
            ap.error(f"no combined_results under {args.results} (nor cv/ or sparam/)")
    elif len(args.positional) == 2:
        jobs = [(Path(args.positional[0]), Path(args.positional[1]), None)]
    else:
        ap.error("give --results <dir> --out <dir>, or <csv_dir> <fig_output_dir>")

    total = 0
    for csv_dir, out_dir, verdicts in jobs:
        if not csv_dir.is_dir():
            print(f"[ERROR] CSV input directory not found: {csv_dir}")
            sys.exit(1)
        total += plot_csv_dir(csv_dir, out_dir, args.workers, verdicts)

    print(f"\nAll plots generated successfully ({total} CSV file(s)).")

if __name__ == "__main__":
    main()
