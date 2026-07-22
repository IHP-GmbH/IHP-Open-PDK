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
Milestone M3 -- renders `eda_report/<device>/report.md` (cluster table, proposed
valid-range table, outlier-measurement list) plus PNG figures (matplotlib/seaborn,
Agg backend -- headless, no display) from the error-feature/cluster/label bundle
produced by `error_features.py` + `cluster.py` + `llm_labeler.py`.
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Dict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)

MAX_SCATTER_POINTS = 8000
FIG_DPI = 130


def _sample(df: pd.DataFrame, n: int, seed: int = 42) -> pd.DataFrame:
    if len(df) <= n:
        return df
    return df.sample(n=n, random_state=seed)


def _fmt(x, nd=4) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "n/a"
    return f"{x:.{nd}g}"


def make_figures(df: pd.DataFrame, out_dir: Path) -> Dict[str, Path]:
    sns.set_theme(style="whitegrid")
    figs: Dict[str, Path] = {}

    # 1) Error distribution (log10(rel_error+eps)) per metric.
    fig, ax = plt.subplots(figsize=(8, 5))
    plot_df = df.copy()
    plot_df["log10_rel_error"] = np.log10(plot_df["rel_error"].clip(lower=1e-9))
    sns.histplot(
        data=plot_df, x="log10_rel_error", hue="metric", element="step",
        stat="density", common_norm=False, bins=60, ax=ax,
    )
    ax.set_xlabel("log10(relative error)")
    ax.set_title("Error distribution by metric")
    fig.tight_layout()
    p = out_dir / "error_distribution.png"
    fig.savefig(p, dpi=FIG_DPI)
    plt.close(fig)
    figs["error_distribution"] = p

    # 2) Error vs bias (VGS, colored by region), one panel per metric.
    sample_df = _sample(df, MAX_SCATTER_POINTS)
    metrics = sorted(sample_df["metric"].unique())
    n = len(metrics)
    fig, axes = plt.subplots(1, n, figsize=(4.5 * n, 4.5), sharey=True)
    if n == 1:
        axes = [axes]
    for ax, metric in zip(axes, metrics):
        sub = sample_df[sample_df["metric"] == metric]
        sns.scatterplot(
            data=sub, x="vgs", y="rel_error", hue="region", s=10, alpha=0.5, ax=ax, legend=(ax is axes[-1])
        )
        ax.set_yscale("symlog", linthresh=1e-3)
        ax.set_title(metric.upper())
        ax.set_xlabel("VGS (V)")
    axes[0].set_ylabel("relative error")
    fig.suptitle("Error vs VGS by region (sampled)")
    fig.tight_layout()
    p = out_dir / "error_vs_bias.png"
    fig.savefig(p, dpi=FIG_DPI)
    plt.close(fig)
    figs["error_vs_bias"] = p

    # 3) Cluster scatter in (VGS, VDS) colored by cluster_id.
    fig, ax = plt.subplots(figsize=(7, 6))
    cluster_sample = _sample(df, MAX_SCATTER_POINTS)
    palette = sns.color_palette("tab20", n_colors=max(cluster_sample["cluster_id"].nunique(), 1))
    sns.scatterplot(
        data=cluster_sample, x="vgs", y="vds", hue="cluster_id", palette=palette,
        s=10, alpha=0.6, ax=ax, legend=False,
    )
    ax.set_xlabel("VGS (V)")
    ax.set_ylabel("VDS (V)")
    ax.set_title("Error-pattern clusters in (VGS, VDS) space (sampled)")
    fig.tight_layout()
    p = out_dir / "cluster_scatter.png"
    fig.savefig(p, dpi=FIG_DPI)
    plt.close(fig)
    figs["cluster_scatter"] = p

    return figs


def _cluster_table_md(bundle: dict) -> str:
    clusters = bundle["clusters"]
    # numeric sort with -1 (noise) last.
    ids = sorted(clusters.keys(), key=lambda k: (int(k) == -1, int(k)))
    lines = [
        "| Cluster ID | Name | Size | Metric | Region | Mean Vgs | Mean Vds | Mean Vbs | Mean Temp | Mean rel_err | Outside-Envelope Frac |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for cid in ids:
        c = clusters[cid]
        cen = c.get("centroid", {})
        lines.append(
            "| {cid} | {name} | {size} | {metric} | {region} | {vgs} | {vds} | {vbs} | {temp} | {rel} | {env} |".format(
                cid=cid,
                name=c.get("name", ""),
                size=c.get("size", ""),
                metric=c.get("dominant_metric", ""),
                region=c.get("dominant_region", ""),
                vgs=_fmt(cen.get("mean_vgs")),
                vds=_fmt(cen.get("mean_vds")),
                vbs=_fmt(cen.get("mean_vbs")),
                temp=_fmt(cen.get("mean_temp"), 3),
                rel=_fmt(cen.get("mean_rel_error")),
                env=_fmt(cen.get("frac_outside_envelope")),
            )
        )
    return "\n".join(lines)


def _valid_range_table_md(bundle: dict) -> str:
    rows = bundle["valid_ranges"]
    lines = [
        "| Metric | Region | N (all) | N (good) | Vgs range (V) | Vds range (V) | Vbs range (V) | Mean rel_err (good) | Mean rel_err (all) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            "| {metric} | {region} | {n} | {ng} | [{vgl}, {vgh}] | [{vdl}, {vdh}] | [{vbl}, {vbh}] | {relg} | {rela} |".format(
                metric=r["metric"],
                region=r["region"],
                n=r["n_points"],
                ng=r["n_good_points"],
                vgl=_fmt(r["vgs_min"]),
                vgh=_fmt(r["vgs_max"]),
                vdl=_fmt(r["vds_min"]),
                vdh=_fmt(r["vds_max"]),
                vbl=_fmt(r["vbs_min"]),
                vbh=_fmt(r["vbs_max"]),
                relg=_fmt(r["mean_rel_error_good"]),
                rela=_fmt(r["mean_rel_error_all"]),
            )
        )
    return "\n".join(lines)


def _outlier_table_md(bundle: dict, max_rows: int = 40) -> str:
    outliers = bundle["outliers"]
    # Sort by severity (rel_error desc); ties broken by the outlier key itself so
    # ordering is fully deterministic regardless of dict/JSON insertion order (matters
    # for the offline-cache-reload determinism check: a freshly computed `outliers`
    # dict and one reloaded from `labels.json` can have different insertion order for
    # tied rel_error values, e.g. symmetric di_bd_area/di_bd_perim duplicates).
    items = sorted(outliers.items(), key=lambda kv: (-kv[1].get("rel_error", 0.0), kv[0]))[:max_rows]
    lines = [
        "| input_data | block_index | metric | region | Vgs | Vds | Vbs | Temp | meas | sim_tt | rel_err | cluster | explanation |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for _key, o in items:
        lines.append(
            "| {inp} | {bi} | {metric} | {region} | {vgs} | {vds} | {vbs} | {temp} | {meas} | {sim} | {rel} | {cid} | {expl} |".format(
                inp=o.get("input_data", ""),
                bi=o.get("block_index", ""),
                metric=o.get("metric", ""),
                region=o.get("region", ""),
                vgs=_fmt(o.get("vgs")),
                vds=_fmt(o.get("vds")),
                vbs=_fmt(o.get("vbs")),
                temp=_fmt(o.get("temp"), 3),
                meas=_fmt(o.get("meas")),
                sim=_fmt(o.get("sim_tt")),
                rel=_fmt(o.get("rel_error")),
                cid=o.get("cluster_id"),
                expl=o.get("explanation", ""),
            )
        )
    return "\n".join(lines), len(outliers), bundle.get("n_outliers_total", len(outliers))


def build_report(
    device: str,
    df: pd.DataFrame,
    bundle: dict,
    cluster_info: dict,
    out_dir: Path,
    temps_included,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    figs = make_figures(df, out_dir)

    outlier_table, n_outliers_shown, n_outliers_total = _outlier_table_md(bundle)

    n_points = len(df)
    n_metrics = df["metric"].nunique()
    temps_str = ", ".join(f"{t:g}" for t in sorted(temps_included))

    md = []
    md.append(f"# MOS Error EDA Report -- {device}")
    md.append("")
    md.append(f"Generated: {date.today().isoformat()}")
    md.append("")
    md.append(
        "This report analyzes model-vs-measurement error patterns for the "
        f"**{device}** MOS device across `combined_results/` sweeps, mirroring the "
        "HBT MQA \"valid window\" methodology but data-driven (no fixed datasheet "
        "table -- valid ranges below are derived from where the model already "
        "agrees with silicon)."
    )
    md.append("")
    md.append(
        f"- Points analyzed: **{n_points}** (point x metric rows), metrics: **{n_metrics}** (id/is/ib/ig, as present)."
    )
    md.append(
        f"- Temperatures included: **{temps_str} degC** (per-point `temp` is kept as an explicit "
        "feature/column; the PDF/global convention analyzes T=27 degC only -- filter to "
        "`temp == 27` for the PDF-convention subset; all temperatures are retained here "
        "so cross-temperature outliers stay visible)."
    )
    md.append(
        f"- Clustering: **{cluster_info.get('method')}** selected by silhouette score "
        f"(silhouette={cluster_info.get('silhouette'):.4f}, n_clusters={cluster_info.get('n_clusters')}, "
        f"fit on a deterministic seeded subsample of {cluster_info.get('n_fit_sample')} points, "
        "then applied to the full point set)."
    )
    md.append(f"- Labeler: **{bundle.get('labeler')}** (rule-based unless `EDA_USE_LLM=1` + API key are set).")
    md.append(
        f"- Outlier measurements flagged (IsolationForest AND [IQR or z-score]): "
        f"**{n_outliers_total}** / {n_points} points; top {n_outliers_shown} listed below."
    )
    md.append("")

    md.append("## Error-pattern clusters")
    md.append("")
    md.append(_cluster_table_md(bundle))
    md.append("")

    md.append("## Proposed valid-range table (per metric / region)")
    md.append("")
    md.append(
        "Derived from the \"well-modeled\" subset per (metric, region) group "
        "(`rel_error` at/below its group's 75th percentile and not a flagged outlier); "
        "range = [5th, 95th] percentile of the derived bias in that subset. This is a "
        "**proposal**, not an enforced M1 `valid_range` -- it is not wired into pass/fail "
        "gating."
    )
    md.append("")
    md.append(_valid_range_table_md(bundle))
    md.append("")

    md.append(f"## Outlier measurements (top {n_outliers_shown} of {n_outliers_total} flagged)")
    md.append("")
    md.append("Keyed to `input_data` + bias coordinates (Vgs/Vds/Vbs derived from node voltages).")
    md.append("")
    md.append(outlier_table)
    md.append("")

    md.append("## Figures")
    md.append("")
    for name, path in figs.items():
        md.append(f"### {name.replace('_', ' ').title()}")
        md.append(f"![{name}]({path.name})")
        md.append("")

    report_path = out_dir / "report.md"
    report_path.write_text("\n".join(md) + "\n")
    logger.info("device=%s: report written to %s", device, report_path)
    return report_path
