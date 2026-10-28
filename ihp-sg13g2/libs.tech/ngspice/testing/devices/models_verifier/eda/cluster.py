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
Milestone M3 -- ML clustering of error patterns + statistical outlier-measurement flags.

Two independent scikit-learn stages, both fully deterministic (explicit
`random_state`, no implicit multithreaded nondeterminism from `n_jobs` beyond what
scikit-learn guarantees to be order-stable for a fixed input):

1. `cluster_error_patterns`: StandardScaler + KMeans (several k, `n_init` fixed) and
   DBSCAN (a small deterministic eps grid), scored by silhouette; the higher-scoring
   labeling wins. Clusters "error patterns" -- i.e. points sharing similar
   error-magnitude + bias/region context -- across the WHOLE per-point error-feature
   table (`error_features.compute_error_features`), not per-sweep, so a cluster can
   name a cross-cutting theme (e.g. "subthreshold leakage" spanning many sweeps).
   To keep KMeans/DBSCAN + silhouette tractable on the largest devices
   (up to ~330k point-metric rows), fitting/scoring uses a deterministic seeded
   subsample (`MAX_CLUSTER_SAMPLE`); the fitted KMeans model (or DBSCAN's nearest-seen
   labeling) is then applied back to the FULL point set so every row still gets a
   cluster id.

2. `flag_outlier_measurements`: per (metric) group, IsolationForest (seeded) plus
   IQR and z-score thresholds on `rel_error`/`log_error`; a point is a flagged
   "outlier measurement" if IsolationForest AND at least one statistical rule agree
   (reduces false positives from any single method).
"""

from __future__ import annotations

import logging
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

RANDOM_STATE = 42
MAX_CLUSTER_SAMPLE = 20000  # cap for KMeans/DBSCAN fit + silhouette (deterministic subsample)
SILHOUETTE_SAMPLE = 5000  # sklearn silhouette_score sample_size (avoids O(n^2) on the full fit set)

FEATURE_COLUMNS: List[str] = [
    "log_error",
    "rel_error_clipped",
    "vgs",
    "vds",
    "vbs",
    "temp",
    "log_wl",
    "meas_outside_envelope_i",
]
REGION_LEVELS = ["subthreshold", "linear", "saturation", "diode_bd", "diode_bs"]
METRIC_LEVELS = ["id", "is", "ib", "ig"]


def build_feature_matrix(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Derive the numeric feature columns (+ one-hot region/metric) used for clustering."""
    feat = pd.DataFrame(index=df.index)
    feat["log_error"] = df["log_error"].clip(-15, 15)
    feat["rel_error_clipped"] = df["rel_error"].clip(upper=df["rel_error"].quantile(0.99))
    feat["vgs"] = df["vgs"]
    feat["vds"] = df["vds"]
    feat["vbs"] = df["vbs"]
    feat["temp"] = df["temp"]
    wl = df["wl_ratio"].replace(0, np.nan)
    feat["log_wl"] = np.log10(wl.clip(lower=1e-6))
    feat["meas_outside_envelope_i"] = df["meas_outside_envelope"].astype(int)

    cols = list(FEATURE_COLUMNS)
    for level in REGION_LEVELS:
        col = f"region_{level}"
        feat[col] = (df["region"] == level).astype(int)
        cols.append(col)
    for level in METRIC_LEVELS:
        col = f"metric_{level}"
        feat[col] = (df["metric"] == level).astype(int)
        cols.append(col)

    feat = feat.fillna(0.0).replace([np.inf, -np.inf], 0.0)
    return feat, cols


def _fit_kmeans_grid(X: np.ndarray, k_values: List[int]) -> Tuple[np.ndarray, str, float]:
    best_labels, best_desc, best_score = None, "", -1.0
    n = X.shape[0]
    for k in k_values:
        if k < 2 or k >= n:
            continue
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(X)
        if len(set(labels)) < 2:
            continue
        score = silhouette_score(
            X, labels, sample_size=min(SILHOUETTE_SAMPLE, n), random_state=RANDOM_STATE
        )
        if score > best_score:
            best_labels, best_desc, best_score = labels, f"KMeans(k={k})", score
    return best_labels, best_desc, best_score


def _fit_dbscan_grid(X: np.ndarray, eps_values: List[float]) -> Tuple[np.ndarray, str, float]:
    best_labels, best_desc, best_score = None, "", -1.0
    n = X.shape[0]
    for eps in eps_values:
        db = DBSCAN(eps=eps, min_samples=10)
        labels = db.fit_predict(X)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        if n_clusters < 2:
            continue
        # silhouette_score requires >=2 labels present in the (sub)sample; DBSCAN noise
        # (-1) is kept as its own "cluster" for scoring purposes.
        score = silhouette_score(
            X, labels, sample_size=min(SILHOUETTE_SAMPLE, n), random_state=RANDOM_STATE
        )
        if score > best_score:
            best_labels, best_desc, best_score = labels, f"DBSCAN(eps={eps})", score
    return best_labels, best_desc, best_score


def cluster_error_patterns(df: pd.DataFrame) -> Tuple[pd.Series, dict]:
    """
    Cluster error patterns over the full point-level error-feature table.

    Returns (cluster_id per row [Int64, -1 for noise/unassigned], info dict with
    keys: method, silhouette, n_clusters, n_fit_sample).
    """
    feat, cols = build_feature_matrix(df)
    n = len(feat)

    rng = np.random.RandomState(RANDOM_STATE)
    if n > MAX_CLUSTER_SAMPLE:
        sample_idx = np.sort(rng.choice(n, size=MAX_CLUSTER_SAMPLE, replace=False))
    else:
        sample_idx = np.arange(n)

    scaler = StandardScaler()
    X_sample = scaler.fit_transform(feat.iloc[sample_idx].to_numpy(dtype=float))

    k_values = [3, 4, 5, 6, 8]
    km_labels, km_desc, km_score = _fit_kmeans_grid(X_sample, k_values)

    eps_values = [0.5, 0.75, 1.0, 1.5, 2.0]
    db_labels, db_desc, db_score = _fit_dbscan_grid(X_sample, eps_values)

    if km_labels is None and db_labels is None:
        logger.warning("clustering: neither KMeans nor DBSCAN produced >=2 clusters; assigning single cluster 0")
        full_labels = pd.Series(0, index=df.index, dtype="int64")
        return full_labels, {"method": "none (single cluster)", "silhouette": float("nan"),
                              "n_clusters": 1, "n_fit_sample": len(sample_idx)}

    if km_score >= db_score:
        chosen_labels, chosen_desc, chosen_score = km_labels, km_desc, km_score
        chosen_model = KMeans(
            n_clusters=int(chosen_desc.split("=")[1].rstrip(")")), random_state=RANDOM_STATE, n_init=10
        ).fit(X_sample)
        X_full = scaler.transform(feat.to_numpy(dtype=float))
        full_label_values = chosen_model.predict(X_full)
    else:
        chosen_labels, chosen_desc, chosen_score = db_labels, db_desc, db_score
        # DBSCAN has no .predict(); assign the rest of the points to the nearest fitted
        # sample's label (1-NN in the scaled feature space) so every row still gets a
        # cluster id, deterministically (ties broken by lowest index via argmin).
        X_full = scaler.transform(feat.to_numpy(dtype=float))
        from sklearn.neighbors import NearestNeighbors

        nn = NearestNeighbors(n_neighbors=1).fit(X_sample)
        _, nn_idx = nn.kneighbors(X_full)
        full_label_values = chosen_labels[nn_idx[:, 0]]

    full_labels = pd.Series(full_label_values, index=df.index, dtype="int64")
    n_clusters = len(set(full_label_values)) - (1 if -1 in full_label_values else 0)
    info = {
        "method": chosen_desc,
        "silhouette": float(chosen_score),
        "n_clusters": n_clusters,
        "n_fit_sample": len(sample_idx),
    }
    logger.info(
        "device clustering: method=%s silhouette=%.4f n_clusters=%d (fit sample=%d/%d)",
        chosen_desc, chosen_score, n_clusters, len(sample_idx), n,
    )
    return full_labels, info


def flag_outlier_measurements(df: pd.DataFrame, contamination: float = 0.02) -> pd.DataFrame:
    """
    Flag outlier MEASUREMENTS (not clusters) via IsolationForest (seeded) + IQR +
    z-score on `rel_error`/`log_error`, computed per-metric so metrics with very
    different error scales don't swamp each other.

    Adds columns: is_outlier_iforest, is_outlier_iqr, is_outlier_zscore, is_outlier
    (the last is the consensus: IsolationForest AND at least one statistical rule).
    """
    out = df.copy()
    out["is_outlier_iforest"] = False
    out["is_outlier_iqr"] = False
    out["is_outlier_zscore"] = False

    for metric, idx in out.groupby("metric").groups.items():
        sub = out.loc[idx, ["rel_error", "log_error"]].fillna(0.0)
        if len(sub) < 20:
            continue

        X = sub.to_numpy(dtype=float)
        iso = IsolationForest(
            n_estimators=200, contamination=contamination, random_state=RANDOM_STATE
        )
        iso_labels = iso.fit_predict(X)  # -1 = outlier
        out.loc[idx, "is_outlier_iforest"] = iso_labels == -1

        rel = sub["rel_error"]
        q1, q3 = rel.quantile(0.25), rel.quantile(0.75)
        iqr = q3 - q1
        iqr_hi = q3 + 1.5 * iqr
        out.loc[idx, "is_outlier_iqr"] = (rel > iqr_hi).to_numpy()

        log_e = sub["log_error"]
        mu, sigma = log_e.mean(), log_e.std(ddof=0)
        if sigma > 0:
            z = (log_e - mu).abs() / sigma
            out.loc[idx, "is_outlier_zscore"] = (z > 3.0).to_numpy()

    out["is_outlier"] = out["is_outlier_iforest"] & (out["is_outlier_iqr"] | out["is_outlier_zscore"])
    return out
