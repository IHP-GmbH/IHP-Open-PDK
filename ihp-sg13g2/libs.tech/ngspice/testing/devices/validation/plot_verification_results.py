#!/usr/bin/env python3
"""
Plot Device Verification Results (Batch CSVs)

This script generates comparison plots between measured silicon data and
simulation results for SG13G2 device models.

Usage:
    python3 plot_verification_results.py <csv_dir> <fig_output_dir>

Example:
    python3 plot_verification_results.py models_results/nmos_lv/combined_results nmos_lv_figs/
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple
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

def format_panel_title(block: pd.DataFrame, out_name: str, device_type_hint: str) -> str:
    """Generate a descriptive panel title."""
    parts = []
    cols = {
        'mos': ['w','l','nf','m'],
        'pnpmpa': ['a','p'],
        'hbt': ['ve','vs','l','w','m','nx']
    }.get(device_type_hint.lower(), [])
    row = block.iloc[0]
    for c in cols:
        if c in block.columns and pd.notna(row.get(c, np.nan)):
            parts.append(f"{c}={row[c]:.4g}" if isinstance(row[c], float) else f"{c}={row[c]}")
    t_str = f"T={row['temp']}°C" if 'temp' in block.columns and pd.notna(row.get('temp', np.nan)) else ""
    src_str = str(row['input_data']) if 'input_data' in block.columns and pd.notna(row.get('input_data', np.nan)) else ""
    left = " — ".join(filter(None, [out_name.upper(), f"[{src_str}]" if src_str else None]))
    right = " — " + " | ".join(filter(None, [t_str] + parts)) if (t_str or parts) else ""
    return left + right

# ---------------------------
# Main Plotting Routine
# ---------------------------

def plot_single_block(args):
    block_id, out_name, block, fig_dir, device_type_hint = args
    COLORS = {
        "range_fill": "#5a4543",
        "typ": "#1f78b4",
        "meas": "#33a02c",
        "outside_tt": "#e31a1c",
        "outside_meas": "#ff7f00"
    }

    sweep_var = str(block["sweep_var"].iloc[0])
    block_sorted = block.sort_values(sweep_var)
    x = block_sorted[sweep_var].to_numpy()

    meas_col = f"{out_name}_meas"
    sim_cols, typ_col, other_cols = split_sim_columns(block_sorted, out_name)

    # Envelope bounds
    y_lo = y_hi = None
    if other_cols:
        sims = block_sorted[other_cols].to_numpy(dtype=float)
        y_lo = np.min(sims, axis=1)
        y_hi = np.max(sims, axis=1)

    # TT and Measured outside masks
    tt_mask = np.zeros_like(x, dtype=bool)
    if typ_col is not None and y_lo is not None and y_hi is not None:
        tt_vals = block_sorted[typ_col].to_numpy(dtype=float)
        tt_mask = outside_mask(tt_vals, y_lo, y_hi)

    meas_mask = np.zeros_like(x, dtype=bool)
    if meas_col in block_sorted.columns and y_lo is not None and y_hi is not None:
        y_meas = block_sorted[meas_col].to_numpy(dtype=float)
        meas_mask = outside_mask(y_meas, y_lo, y_hi)

    # Determine output folder
    status = "passed" if not (tt_mask.any() or meas_mask.any()) else "failed"
    block_fig_dir = fig_dir / status
    if status == "failed":
        if tt_mask.any() and not meas_mask.any():
            block_fig_dir = block_fig_dir / "tt"
        elif meas_mask.any() and not tt_mask.any():
            block_fig_dir = block_fig_dir / "meas"
        else:
            block_fig_dir = block_fig_dir / "both"
    block_fig_dir.mkdir(parents=True, exist_ok=True)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))

    # Envelope fill
    if y_lo is not None and y_hi is not None:
        ax.fill_between(x, y_lo, y_hi, alpha=0.3, color=COLORS["range_fill"], label="Envelope (FF/SS)")

    # TT simulation
    if typ_col is not None:
        ax.plot(x, block_sorted[typ_col].to_numpy(dtype=float), "--", color=COLORS["typ"], linewidth=2, label="TT Simulation")
        ax.scatter(x[tt_mask], block_sorted[typ_col].to_numpy(dtype=float)[tt_mask],
                   color=COLORS["outside_tt"], marker="x", s=64, linewidths=2, label="TT Outside")

    # Measured
    if meas_col in block_sorted.columns:
        y_meas = block_sorted[meas_col].to_numpy(dtype=float)
        ax.plot(x, y_meas, "-o", color=COLORS["meas"], linewidth=1.8, markersize=4, label="Measured")
        ax.scatter(x[meas_mask], y_meas[meas_mask],
                   color=COLORS["outside_meas"], marker="x", s=64, linewidths=2, label="Measured Outside")

    # --- Annotations for outside points (show X and Y) ---
    # TT outside → left, Meas outside → right
    if typ_col is not None and tt_mask.any():
        tt_vals = block_sorted[typ_col].to_numpy(dtype=float)
        for xi, yi in zip(x[tt_mask], tt_vals[tt_mask]):
            ax.annotate(f"({xi:.2e}, {yi:.2e})", xy=(xi, yi), xytext=(-10, 0),
                        textcoords="offset points", ha="right", va="center", fontsize=5)

    if meas_col in block_sorted.columns and meas_mask.any():
        y_meas = block_sorted[meas_col].to_numpy(dtype=float)
        for xi, yi in zip(x[meas_mask], y_meas[meas_mask]):
            ax.annotate(f"({xi:.2e}, {yi:.2e})", xy=(xi, yi), xytext=(10, 0),
                        textcoords="offset points", ha="left", va="center", fontsize=5)

    # Title, axes, grid
    ax.set_title(format_panel_title(block, out_name, device_type_hint), fontsize=9)
    style_axes(ax, sweep_var, out_name)
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # Deduplicate legend
    handles, labels = ax.get_legend_handles_labels()
    seen = set()
    H, L = [], []
    for h, l in zip(handles, labels):
        if l not in seen:
            seen.add(l)
            H.append(h)
            L.append(l)
    ax.legend(H, L, fontsize=8, frameon=False, loc="best")

    # Save figure
    fig_name = f"{block_id}_{out_name}_{sweep_var}.png".replace(" ", "_")
    fig_path = block_fig_dir / fig_name
    fig.tight_layout()
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)
    return fig_path


def plot_blocks_comparison(df: pd.DataFrame, fig_dir: Path, device_type_hint: str = "mos", max_workers: int = 8):
    # Prepare list of tasks
    tasks = []
    for block_id in pd.unique(df["block_id"]):
        block = df[df["block_id"] == block_id]
        if block.empty:
            continue
        for out_name in parse_block_outputs(block):
            tasks.append((block_id, out_name, block.copy(), fig_dir, device_type_hint))

    saved_files = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for fig_path in tqdm(executor.map(plot_single_block, tasks), total=len(tasks), desc="Generating figures"):
            saved_files.append(fig_path)

    print(f"\nTotal figures saved: {len(saved_files)}")

# ---------------------------
# CLI Entry Point
# ---------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 plot_verification_results.py <csv_dir> <fig_output_dir>")
        sys.exit(1)

    csv_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    if not csv_dir.exists() or not csv_dir.is_dir():
        print(f"[ERROR] CSV input directory not found: {csv_dir}")
        sys.exit(1)

    # Loop over CSVs in directory
    for csv_file in sorted(csv_dir.glob("*.csv")):
        print(f"\n📂 Processing CSV: {csv_file.name}")
        df = pd.read_csv(csv_file)
        csv_fig_dir = output_dir / csv_file.stem
        csv_fig_dir.mkdir(parents=True, exist_ok=True)
        plot_blocks_comparison(df, csv_fig_dir)

    print("\nAll plots generated successfully.")

if __name__ == "__main__":
    main()
