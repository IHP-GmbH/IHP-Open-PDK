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
Milestone M3 -- MOS error EDA: feature extraction, ML clustering, cluster/outlier
labeling, and Markdown+figure reporting.

Mirrors the HBT MQA "valid window" methodology for MOS, but data-driven: instead of a
fixed bias table transcribed from a datasheet, this package derives candidate valid
bias windows per (metric, region) from where the model already agrees well with silicon
measurements, and flags clusters/points where it does not.

Submodules:
    error_features  -- per-point sim-vs-measurement error features (tidy DataFrame).
    cluster         -- StandardScaler + KMeans/DBSCAN clustering (silhouette-selected)
                       and IsolationForest/IQR/z-score outlier-measurement detection.
    llm_labeler     -- cluster naming / valid-range proposal / outlier explanation,
                       with a deterministic offline rule-based fallback (default) and an
                       optional (env-gated, default OFF) real LLM call.
    report          -- renders `eda_report/<device>/report.md` + PNG figures.
    run             -- CLI entry point: `python -m models_verifier.eda.run --device <d>`.
"""
