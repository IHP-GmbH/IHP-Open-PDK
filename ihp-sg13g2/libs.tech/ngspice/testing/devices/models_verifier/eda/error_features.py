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
Milestone M3 -- per-point MOS error feature extraction.

Reads `models_results/<device>/combined_results/*.csv` (schema documented in
`$DEV/README.md` under "combined_results/") and, for every metric present
(`id`/`is`/`ib`/`ig`), computes a tidy per-point error record vs the TT (typical)
simulation corner: absolute error, relative error (clipped, matching the verifier
pipeline's own `clip_curr`), log-domain error, and the point's containment inside the
SS/FF corner envelope (`outside_mask` / `split_sim_columns`, reused from
`validation/plot_verification_results.py` -- no metric of this kind exists anywhere
else in the pipeline today, it is computed fresh here).

Each point is also tagged with contextual features used by `eda/cluster.py`:
device, table (characteristic), region (subthreshold/linear/saturation/diode, from a
VGS/VDS/threshold heuristic -- see `estimate_vt0`), VGS/VDS/VBS (derived from the node
voltages per `ENV_BRIEF.md`'s "CRITICAL data gotchas"), temp (kept as a feature; NOT
filtered to 27 C -- see module docstring note below), and W/L.

Per the GOAL_DEV_VER.md M3 acceptance and ENV_BRIEF.md guidance: the PDF/global
convention analyzes T = 27 C only, but MOS measurement data spans
[-40, 27, 70, 125] C. This module KEEPS ALL temperatures as rows (so cross-temperature
outliers remain visible to the clustering/outlier stages) but always retains `temp` as
an explicit feature/column so a reader can filter to 27 C if they want the PDF-convention
subset. `eda/report.py` states in its header which temperatures were included.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import yaml

from validation.plot_verification_results import outside_mask, split_sim_columns

logger = logging.getLogger(__name__)

# $DEV root (two levels up from this file: models_verifier/eda/error_features.py -> $DEV).
DEV_ROOT = Path(__file__).resolve().parents[2]

# Metrics the MOS combined_results tables carry (see README §combined_results).
MOS_METRICS: List[str] = ["id", "is", "ib", "ig"]

# Makefile-target device key -> config YAML (kept in sync with the Makefile's
# `*_CONFIG` variables and `models_verifier/waivers/generate.py::DEVICE_CONFIGS`).
DEVICE_CONFIGS: Dict[str, Path] = {
    "nmos_lv": DEV_ROOT / "configs/mos/nmos_lv/sg13_lv_nmos.yaml",
    "pmos_lv": DEV_ROOT / "configs/mos/pmos_lv/sg13_lv_pmos.yaml",
    "nmos_hv": DEV_ROOT / "configs/mos/nmos_hv/sg13_hv_nmos.yaml",
    "pmos_hv": DEV_ROOT / "configs/mos/pmos_hv/sg13_hv_pmos.yaml",
}

# Fallback current clip (A) if a device config doesn't define `clip_curr` -- matches the
# default in `models_verifier.py:64` (`self.clip_curr = float(self.config.get("clip_curr",
# 1e-12))`). Each MOS config currently sets `clip_curr: 1e-11`, which is what's actually
# used per-device (read from the YAML below).
DEFAULT_CLIP_CURR = 1e-12

# Constant-current VT0 heuristic reference current density (A per unit W/L), used only
# to bucket points into subthreshold/linear/saturation "regions" for EDA clustering --
# NOT a physical parameter extraction (c.f. M4's real S-param extraction) and NOT used
# anywhere in pass/fail gating (M1/M2 windows are untouched).
VT_REF_CURRENT_DENSITY = 100e-9  # 100 nA * (W/L)


def load_device_config(device: str) -> dict:
    """Load a MOS device's YAML config (for clip_curr/output_dir/device_name)."""
    cfg_path = DEVICE_CONFIGS[device]
    with open(cfg_path, "r") as fh:
        return yaml.safe_load(fh)


def _polarity(device: str) -> int:
    """+1 for NMOS (VT > 0), -1 for PMOS (VT < 0), inferred from the device key."""
    return -1 if device.lower().startswith("pmos") else 1


def estimate_vt0(df_idvg: pd.DataFrame, polarity: int) -> Optional[float]:
    """
    Rough constant-current VT0 estimate (heuristic only -- see module docstring).

    Uses the Id-Vg sweep's minimum-|VDS| bin (the "linear region" measurement bin that
    is already present in the data, e.g. VDS=0.05 V for LV, VDS=0.1 V for HV) and finds
    where the pooled median current density |Id|/(W/L) crosses `VT_REF_CURRENT_DENSITY`,
    via linear interpolation between the two straddling VGS bins of a coarse histogram.
    Returns None if extraction isn't possible (too few points) -- callers fall back to a
    conservative default.
    """
    df = df_idvg[(df_idvg.get("sweep_var") == "vg")].copy()
    if df.empty or "id_meas" not in df.columns:
        return None
    df["vds"] = df["vd"] - df["vs"]
    df["vgs"] = df["vg"] - df["vs"]
    # pick the linear-region bin: smallest |vds| present (rounded, to bin together
    # nominally-identical bias points across different sweep blocks).
    df["abs_vds_r"] = df["vds"].abs().round(3)
    min_abs_vds = df["abs_vds_r"].min()
    lin = df[df["abs_vds_r"] == min_abs_vds]
    if lin.empty or (lin["w"] <= 0).all() or (lin["l"] <= 0).all():
        return None

    wl = (lin["w"] / lin["l"]).replace([np.inf, -np.inf], np.nan)
    idens = (lin["id_meas"].abs() / wl).replace([np.inf, -np.inf], np.nan)
    vgs_eff = polarity * lin["vgs"]

    valid = idens.notna() & vgs_eff.notna() & (wl > 0)
    if valid.sum() < 10:
        return None
    vgs_eff = vgs_eff[valid].to_numpy()
    idens = idens[valid].to_numpy()

    # Coarse binned median current density vs effective VGS, then find the first
    # crossing of the reference density via linear interpolation. Bin edges are fixed
    # (not data-order-dependent) so this is fully deterministic.
    lo, hi = np.floor(vgs_eff.min() * 20) / 20, np.ceil(vgs_eff.max() * 20) / 20
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return None
    edges = np.arange(lo, hi + 0.05, 0.05)
    if len(edges) < 3:
        return None
    bin_idx = np.digitize(vgs_eff, edges) - 1
    n_bins = len(edges) - 1
    centers = (edges[:-1] + edges[1:]) / 2.0
    medians = np.full(n_bins, np.nan)
    for b in range(n_bins):
        sel = idens[bin_idx == b]
        if sel.size:
            medians[b] = np.median(sel)

    ok = np.isfinite(medians)
    if ok.sum() < 2:
        return None
    centers_ok = centers[ok]
    medians_ok = medians[ok]
    order = np.argsort(centers_ok)
    centers_ok = centers_ok[order]
    medians_ok = medians_ok[order]

    ref = VT_REF_CURRENT_DENSITY
    above = medians_ok >= ref
    if not above.any() or above.all():
        # never crosses within the swept range -> fall back to the point closest to ref
        idx = int(np.argmin(np.abs(medians_ok - ref)))
        return float(centers_ok[idx])
    first_above = int(np.argmax(above))
    if first_above == 0:
        return float(centers_ok[0])
    x0, x1 = centers_ok[first_above - 1], centers_ok[first_above]
    y0, y1 = medians_ok[first_above - 1], medians_ok[first_above]
    if y1 == y0:
        return float(x1)
    frac = (ref - y0) / (y1 - y0)
    return float(x0 + frac * (x1 - x0))


_DEFAULT_VT0 = {"nmos_lv": 0.45, "pmos_lv": 0.45, "nmos_hv": 0.65, "pmos_hv": 0.65}


def classify_region(vgs_eff: pd.Series, vds_eff: pd.Series, vt0: float) -> pd.Series:
    """
    Bucket points into subthreshold/linear/saturation from a VGS/VDS/VT heuristic
    (in the device's own "effective" polarity-normalized bias space, i.e. VGS/VDS
    already multiplied by +1 for NMOS / -1 for PMOS so VT0 > 0 in both cases).
    """
    ov = vgs_eff - vt0
    region = np.where(
        ov <= 0.0,
        "subthreshold",
        np.where(vds_eff < ov, "linear", "saturation"),
    )
    return pd.Series(region, index=vgs_eff.index)


def _table_region(table: str) -> Optional[str]:
    """Diode area/perimeter characteristics aren't MOSFET-channel sweeps (VG=0 always)
    -- label them directly rather than running the VGS/VDS heuristic on them."""
    t = table.lower()
    if t.startswith("di_bd"):
        return "diode_bd"
    if t.startswith("di_bs"):
        return "diode_bs"
    return None


def compute_error_features(device: str) -> pd.DataFrame:
    """
    Build the tidy per-point error-feature DataFrame for one MOS device.

    One row per (original combined_results row, metric) pair, for every metric that has
    both a `<metric>_meas` and `<metric>_sim_mos_tt` column in that table.
    """
    cfg = load_device_config(device)
    clip_curr = float(cfg.get("clip_curr", DEFAULT_CLIP_CURR))
    out_dir = DEV_ROOT / cfg["output_dir"]
    combined_dir = out_dir / "combined_results"
    if not combined_dir.is_dir():
        raise FileNotFoundError(
            f"combined_results not found for device={device!r}: {combined_dir} "
            "(regenerate with `python -m models_verifier.models_verifier --config ...`)"
        )

    csv_files = sorted(combined_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No combined_results/*.csv for device={device!r} in {combined_dir}")

    polarity = _polarity(device)

    # Estimate VT0 once from the Id-Vg table (heuristic; falls back to a fixed default).
    vt0 = None
    idvg_path = combined_dir / "dc_idvg.csv"
    if idvg_path.exists():
        try:
            idvg_df = pd.read_csv(idvg_path)
            vt0 = estimate_vt0(idvg_df, polarity)
        except Exception:  # pragma: no cover - defensive; heuristic only
            logger.exception("VT0 estimation failed for %s; using default", device)
    if vt0 is None:
        vt0 = _DEFAULT_VT0.get(device, 0.5)
        logger.info("device=%s: using default VT0 heuristic=%.3f V (extraction unavailable)", device, vt0)
    else:
        logger.info("device=%s: estimated VT0 heuristic=%.3f V (constant-current, Iref=%.1e A*(W/L))",
                     device, vt0, VT_REF_CURRENT_DENSITY)

    frames = []
    for csv_path in csv_files:
        table = csv_path.stem
        df = pd.read_csv(csv_path)
        if df.empty:
            continue

        # Derived two-terminal biases from node voltages (ENV_BRIEF "CRITICAL data
        # gotchas": vs/vd/vg/vb are NODE voltages).
        for col in ("vs", "vd", "vg", "vb"):
            if col not in df.columns:
                df[col] = 0.0
        vgs = df["vg"] - df["vs"]
        vds = df["vd"] - df["vs"]
        vbs = df["vb"] - df["vs"]

        forced_region = _table_region(table)
        if forced_region is None:
            vgs_eff = polarity * vgs
            vds_eff = polarity * vds
            region = classify_region(vgs_eff, vds_eff, vt0)
        else:
            region = pd.Series(forced_region, index=df.index)

        wl_ratio = (df["w"] / df["l"]).replace([np.inf, -np.inf], np.nan) if "w" in df.columns and "l" in df.columns else np.nan

        for metric in MOS_METRICS:
            meas_col = f"{metric}_meas"
            if meas_col not in df.columns:
                continue
            sim_cols, tt_col, other_cols = split_sim_columns(df, metric)
            if tt_col is None:
                continue

            meas = pd.to_numeric(df[meas_col], errors="coerce")
            sim_tt = pd.to_numeric(df[tt_col], errors="coerce")
            valid = meas.notna() & sim_tt.notna()
            if not valid.any():
                continue

            abs_error = (meas - sim_tt).abs()
            denom = np.maximum(meas.abs(), clip_curr)
            rel_error = abs_error / denom
            log_error = np.log10(np.maximum(meas.abs(), clip_curr)) - np.log10(
                np.maximum(sim_tt.abs(), clip_curr)
            )

            meas_outside = pd.Series(False, index=df.index)
            tt_outside = pd.Series(False, index=df.index)
            if other_cols:
                sims = df[other_cols].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
                y_lo = np.nanmin(sims, axis=1)
                y_hi = np.nanmax(sims, axis=1)
                meas_outside = pd.Series(outside_mask(meas.to_numpy(dtype=float), y_lo, y_hi), index=df.index)
                tt_outside = pd.Series(outside_mask(sim_tt.to_numpy(dtype=float), y_lo, y_hi), index=df.index)

            block_key = df["block_id"].astype(str) + "|" + df["block_index"].astype(str) + "|" + metric
            rms_error_sweep = rel_error.groupby(block_key).transform(
                lambda s: float(np.sqrt(np.mean(np.square(s.to_numpy(dtype=float)))))
            )

            part = pd.DataFrame(
                {
                    "device": device,
                    "table": table,
                    "input_data": df.get("input_data"),
                    "block_id": df.get("block_id"),
                    "block_index": df.get("block_index"),
                    "metric": metric,
                    "sweep_var": df.get("sweep_var"),
                    "temp": pd.to_numeric(df.get("temp"), errors="coerce"),
                    "w": pd.to_numeric(df.get("w"), errors="coerce"),
                    "l": pd.to_numeric(df.get("l"), errors="coerce"),
                    "wl_ratio": wl_ratio,
                    "vg": df["vg"],
                    "vd": df["vd"],
                    "vb": df["vb"],
                    "vs": df["vs"],
                    "vgs": vgs,
                    "vds": vds,
                    "vbs": vbs,
                    "region": region,
                    "meas": meas,
                    "sim_tt": sim_tt,
                    "abs_error": abs_error,
                    "rel_error": rel_error,
                    "log_error": log_error,
                    "rms_error_sweep": rms_error_sweep,
                    "meas_outside_envelope": meas_outside,
                    "tt_outside_envelope": tt_outside,
                }
            )
            frames.append(part[valid.to_numpy()])

    if not frames:
        raise ValueError(f"No usable metric columns found for device={device!r}")

    result = pd.concat(frames, ignore_index=True)
    result = result.replace([np.inf, -np.inf], np.nan).dropna(subset=["abs_error", "rel_error"])
    return result.reset_index(drop=True)
