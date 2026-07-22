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
Milestone M3 -- cluster naming, valid-range proposal, and outlier explanation.

Offline-first by design: the default (and CI/acceptance) path is a deterministic,
seed-free RULE-BASED labeler (`_rule_based_name_cluster` / `_rule_based_explain_outlier`
/ `propose_valid_ranges`) that derives everything from the numeric cluster
centroids/outlier rows already computed by `eda/cluster.py` -- no network, no API key,
100% reproducible given the same input data.

A real LLM call is fully optional and OFF by default; it is only attempted when BOTH
`EDA_USE_LLM=1` is set in the environment AND an API key is present, and any failure
(missing package, no network, timeout, ...) silently falls back to the rule-based
labeler so the pipeline never hard-depends on network access.

All results (rule-based or LLM) are cached to `eda_report/<device>/labels.json`. On a
re-run, if that cache file exists (and `EDA_FORCE_RELABEL` is not set), labels are
loaded straight from it instead of recomputed -- this is what `make eda-<device>` run
twice offline is checked against (see GOAL_DEV_VER.md M3 acceptance).
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

NOISE_CLUSTER_NAME = "Unclustered / miscellaneous (DBSCAN noise)"

# Bias-window ("region") vocabulary the naming templates key off of.
_LEAKAGE_METRICS = {"ig", "ib"}


# ---------------------------------------------------------------------------------
# Cluster summarization + rule-based naming
# ---------------------------------------------------------------------------------


def summarize_clusters(df: pd.DataFrame) -> pd.DataFrame:
    """One row per cluster_id: size + centroid summary of the features that matter for
    naming (dominant metric/region, mean bias, mean error, envelope/outlier fractions)."""

    def _mode(s: pd.Series) -> str:
        m = s.mode()
        return str(m.iloc[0]) if not m.empty else ""

    agg = df.groupby("cluster_id").agg(
        size=("cluster_id", "size"),
        dominant_metric=("metric", _mode),
        dominant_region=("region", _mode),
        dominant_device=("device", _mode),
        mean_vgs=("vgs", "mean"),
        mean_vds=("vds", "mean"),
        mean_vbs=("vbs", "mean"),
        mean_temp=("temp", "mean"),
        mean_abs_error=("abs_error", "mean"),
        mean_rel_error=("rel_error", "mean"),
        median_rel_error=("rel_error", "median"),
        mean_log_error=("log_error", "mean"),
        frac_outside_envelope=("meas_outside_envelope", "mean"),
        frac_is_outlier=("is_outlier", "mean") if "is_outlier" in df.columns else ("cluster_id", "size"),
    )
    if "is_outlier" not in df.columns:
        agg["frac_is_outlier"] = 0.0
    agg = agg.sort_values("size", ascending=False).reset_index()
    return agg


def _rule_based_name_cluster(row: pd.Series) -> str:
    """Deterministic physical-theme name from a cluster's centroid summary row."""
    if int(row["cluster_id"]) == -1:
        return NOISE_CLUSTER_NAME

    metric = row["dominant_metric"]
    region = row["dominant_region"]
    rel_err = row["mean_rel_error"]
    vds = row["mean_vds"]
    outside_frac = row["frac_outside_envelope"]

    severity = "severe" if rel_err > 1.0 else ("moderate" if rel_err > 0.2 else "minor")

    if region.startswith("diode"):
        which = "drain-bulk" if region == "diode_bd" else "source-bulk"
        return f"{which} diode measurement mismatch ({severity}, mean|rel_err|={rel_err:.2g})"

    if metric in _LEAKAGE_METRICS and rel_err > 0.5:
        return f"{metric.upper()} leakage-current measurement noise ({region}, {severity})"

    if region == "subthreshold":
        return f"subthreshold {metric.upper()} leakage deviation ({severity}, mean_Vgs={row['mean_vgs']:.2f}V)"

    if region == "saturation" and abs(vds) >= 1.0:
        return f"high-|Vds| saturation deviation ({metric.upper()}, {severity}, mean_Vds={vds:.2f}V)"

    if region == "saturation":
        return f"saturation-region {metric.upper()} deviation ({severity})"

    if region == "linear":
        return f"linear-region {metric.upper()} deviation ({severity}, mean_Vds={vds:.2f}V)"

    if outside_frac > 0.5:
        return f"{metric.upper()} corner-envelope excursion ({region}, {severity})"

    return f"{region}-region {metric.upper()} deviation ({severity})"


def label_clusters_rule_based(cluster_summary: pd.DataFrame) -> Dict[str, dict]:
    labels: Dict[str, dict] = {}
    for _, row in cluster_summary.iterrows():
        cid = int(row["cluster_id"])
        labels[str(cid)] = {
            "name": _rule_based_name_cluster(row),
            "size": int(row["size"]),
            "dominant_metric": row["dominant_metric"],
            "dominant_region": row["dominant_region"],
            "centroid": {
                "mean_vgs": round(float(row["mean_vgs"]), 6),
                "mean_vds": round(float(row["mean_vds"]), 6),
                "mean_vbs": round(float(row["mean_vbs"]), 6),
                "mean_temp": round(float(row["mean_temp"]), 3),
                "mean_rel_error": round(float(row["mean_rel_error"]), 6),
                "median_rel_error": round(float(row["median_rel_error"]), 6),
                "mean_log_error": round(float(row["mean_log_error"]), 6),
                "frac_outside_envelope": round(float(row["frac_outside_envelope"]), 6),
                "frac_is_outlier": round(float(row["frac_is_outlier"]), 6),
            },
        }
    return labels


# ---------------------------------------------------------------------------------
# Proposed valid-range table (per metric/region) -- data-driven analogue of the HBT
# MQA bias-window table, derived from where the model already agrees with silicon.
# ---------------------------------------------------------------------------------


def propose_valid_ranges(df: pd.DataFrame, good_quantile: float = 0.75) -> pd.DataFrame:
    """
    For each (metric, region) group: take the "well-modeled" subset (rel_error <= that
    group's `good_quantile` and not flagged `is_outlier`), then propose a valid bias
    window as the [5th, 95th] percentile of VGS/VDS/VBS within that subset -- i.e. the
    bias range where the model-vs-silicon agreement is already good, mirroring the MQA
    "valid window" methodology (M1/Reference Data) but derived from data instead of a
    datasheet transcription.
    """
    rows = []
    for (metric, region), g in df.groupby(["metric", "region"]):
        if g.empty:
            continue
        thresh = g["rel_error"].quantile(good_quantile)
        good = g[(g["rel_error"] <= thresh) & (~g.get("is_outlier", pd.Series(False, index=g.index)))]
        if good.empty:
            good = g
        rows.append(
            {
                "metric": metric,
                "region": region,
                "n_points": int(len(g)),
                "n_good_points": int(len(good)),
                "vgs_min": round(float(good["vgs"].quantile(0.05)), 4),
                "vgs_max": round(float(good["vgs"].quantile(0.95)), 4),
                "vds_min": round(float(good["vds"].quantile(0.05)), 4),
                "vds_max": round(float(good["vds"].quantile(0.95)), 4),
                "vbs_min": round(float(good["vbs"].quantile(0.05)), 4),
                "vbs_max": round(float(good["vbs"].quantile(0.95)), 4),
                "mean_rel_error_good": round(float(good["rel_error"].mean()), 6),
                "mean_rel_error_all": round(float(g["rel_error"].mean()), 6),
            }
        )
    result = pd.DataFrame(rows).sort_values(["metric", "region"]).reset_index(drop=True)
    return result


# ---------------------------------------------------------------------------------
# Outlier explanations
# ---------------------------------------------------------------------------------


def _rule_based_explain_outlier(row: pd.Series) -> str:
    parts = []
    if abs(row["meas"]) <= 1.05e-11:
        parts.append("measured value pinned at/near the noise floor/clip")
    if row.get("meas_outside_envelope"):
        parts.append("measurement falls outside the SS/FF corner envelope")
    if row["region"].startswith("diode") and row["meas"] < row.get("sim_tt", 0):
        parts.append("measured diode current far below simulated forward conduction (likely floor-clipped measurement)")
    if row["log_error"] > 2:
        parts.append(f"simulated value is >{10**int(row['log_error'])}x measurement (log-domain gap={row['log_error']:.1f} decades)")
    elif row["log_error"] < -2:
        parts.append(f"measured value is >{10**int(-row['log_error'])}x simulated (log-domain gap={row['log_error']:.1f} decades)")
    if not parts:
        parts.append(f"relative error {row['rel_error']:.2f} exceeds the statistical threshold for its ({row['metric']}, {row['region']}) group")
    return "; ".join(parts)


def _outlier_key(row: pd.Series) -> str:
    return "|".join(
        [
            str(row.get("input_data")),
            str(row.get("block_index")),
            row["metric"],
            f"{row['vgs']:.4f}",
            f"{row['vds']:.4f}",
            f"{row['vbs']:.4f}",
        ]
    )


def explain_outliers_rule_based(outlier_rows: pd.DataFrame) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    for _, row in outlier_rows.iterrows():
        key = _outlier_key(row)
        out[key] = {
            "input_data": str(row.get("input_data")),
            "block_index": int(row.get("block_index")) if pd.notna(row.get("block_index")) else None,
            "metric": str(row["metric"]),
            "region": str(row["region"]),
            "vgs": round(float(row["vgs"]), 4),
            "vds": round(float(row["vds"]), 4),
            "vbs": round(float(row["vbs"]), 4),
            "temp": float(row["temp"]) if pd.notna(row["temp"]) else None,
            "meas": float(row["meas"]) if pd.notna(row["meas"]) else None,
            "sim_tt": float(row["sim_tt"]) if pd.notna(row["sim_tt"]) else None,
            "rel_error": round(float(row["rel_error"]), 6),
            "cluster_id": int(row["cluster_id"]) if "cluster_id" in row and pd.notna(row["cluster_id"]) else None,
            "explanation": _rule_based_explain_outlier(row),
        }
    return out


# ---------------------------------------------------------------------------------
# Optional real-LLM hook (OFF by default; env-gated; never required for acceptance).
# ---------------------------------------------------------------------------------


def _llm_enabled() -> bool:
    return os.environ.get("EDA_USE_LLM", "0").strip().lower() in {"1", "true", "yes"}


def _try_llm_label_clusters(cluster_summary: pd.DataFrame) -> Optional[Dict[str, dict]]:
    """Best-effort real LLM cluster naming. Returns None (caller falls back to the
    rule-based labeler) unless EDA_USE_LLM=1 AND an API key is present AND the call
    succeeds. Never raises."""
    if not _llm_enabled():
        return None
    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.info("EDA_USE_LLM=1 but no API key found in environment; using rule-based labeler")
        return None
    try:  # pragma: no cover - network path, not exercised in CI/offline acceptance
        import anthropic  # type: ignore

        client = anthropic.Anthropic(api_key=api_key)
        labels: Dict[str, dict] = {}
        for _, row in cluster_summary.iterrows():
            cid = int(row["cluster_id"])
            if cid == -1:
                labels[str(cid)] = {"name": NOISE_CLUSTER_NAME}
                continue
            prompt = (
                "Name this MOSFET model-vs-measurement error cluster with a short "
                "physical failure theme (<=6 words). Centroid: "
                f"metric={row['dominant_metric']}, region={row['dominant_region']}, "
                f"mean_Vgs={row['mean_vgs']:.3f}, mean_Vds={row['mean_vds']:.3f}, "
                f"mean_rel_error={row['mean_rel_error']:.3g}, size={row['size']}."
            )
            resp = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=32,
                messages=[{"role": "user", "content": prompt}],
            )
            name = resp.content[0].text.strip() if resp.content else _rule_based_name_cluster(row)
            labels[str(cid)] = {"name": name}
        return labels
    except Exception:
        logger.exception("Real LLM cluster labeling failed; falling back to rule-based labeler")
        return None


# ---------------------------------------------------------------------------------
# Top-level cached orchestrator
# ---------------------------------------------------------------------------------


def label_device(
    df: pd.DataFrame,
    outlier_rows: pd.DataFrame,
    device: str,
    cache_path: Path,
    max_outliers_cached: int = 200,
) -> dict:
    """
    Produce (and cache to `cache_path`) the full labeling bundle for one device:
    cluster names + centroids, proposed valid ranges, and outlier explanations.

    If `cache_path` already exists (and `EDA_FORCE_RELABEL` is unset), it is loaded
    verbatim instead of recomputed -- this is the offline-determinism path exercised by
    the M3 acceptance check ("run make eda-<device> TWICE, second run loads cache").
    """
    force = os.environ.get("EDA_FORCE_RELABEL", "0").strip().lower() in {"1", "true", "yes"}
    if cache_path.exists() and not force:
        logger.info("device=%s: loading cached labels from %s (offline, no recompute)", device, cache_path)
        with open(cache_path, "r") as fh:
            return json.load(fh)

    cluster_summary = summarize_clusters(df)
    llm_names = _try_llm_label_clusters(cluster_summary)
    if llm_names is not None:
        rule_labels = label_clusters_rule_based(cluster_summary)
        for cid, entry in rule_labels.items():
            if cid in llm_names and "name" in llm_names[cid]:
                entry["name"] = llm_names[cid]["name"]
        cluster_labels = rule_labels
        source = "llm (anthropic, with rule-based centroid metadata)"
    else:
        cluster_labels = label_clusters_rule_based(cluster_summary)
        source = "rule_based"

    valid_ranges = propose_valid_ranges(df)

    outliers_sorted = outlier_rows.sort_values("rel_error", ascending=False).head(max_outliers_cached)
    outlier_explanations = explain_outliers_rule_based(outliers_sorted)

    bundle = {
        "device": device,
        "labeler": source,
        "n_clusters": int(len([c for c in cluster_labels if c != "-1"])),
        "n_outliers_total": int(len(outlier_rows)),
        "n_outliers_cached": int(len(outlier_explanations)),
        "clusters": cluster_labels,
        "valid_ranges": valid_ranges.to_dict(orient="records"),
        "outliers": outlier_explanations,
    }

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w") as fh:
        json.dump(bundle, fh, indent=2, sort_keys=True, default=str)
    logger.info("device=%s: labeled via %s, cached to %s", device, source, cache_path)
    return bundle
