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
Milestone M3 -- CLI entry point for the MOS error EDA pipeline.

    python -m models_verifier.eda.run --device nmos_lv
    python -m models_verifier.eda.run --device all      # nmos_lv, pmos_lv, nmos_hv, pmos_hv

Wired to the Makefile's `eda-<device>` / `eda-mos` targets. Fully offline: no network
access is required or attempted unless a caller explicitly sets `EDA_USE_LLM=1` with an
API key present (see `eda/llm_labeler.py`); the default/CI path is the deterministic
rule-based labeler, cached to `eda_report/<device>/labels.json`.

Pipeline per device (extend, don't rewrite -- reads the existing
`models_results/<device>/combined_results/*.csv`, writes only under the new,
gitignored `eda_report/<device>/`):
    error_features.compute_error_features -> cluster.cluster_error_patterns
        -> cluster.flag_outlier_measurements -> llm_labeler.label_device (cached)
        -> report.build_report
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from models_verifier.eda import cluster, error_features, llm_labeler, report

logger = logging.getLogger(__name__)

DEV_ROOT = error_features.DEV_ROOT
MOS_DEVICES = ["nmos_lv", "pmos_lv", "nmos_hv", "pmos_hv"]


def run_one(device: str) -> Path:
    logger.info("=== EDA: device=%s ===", device)

    df = error_features.compute_error_features(device)
    logger.info("device=%s: %d error-feature rows computed", device, len(df))

    cluster_ids, cluster_info = cluster.cluster_error_patterns(df)
    df = df.copy()
    df["cluster_id"] = cluster_ids

    df = cluster.flag_outlier_measurements(df)
    n_outliers = int(df["is_outlier"].sum())
    logger.info("device=%s: %d/%d points flagged as outlier measurements", device, n_outliers, len(df))

    out_dir = DEV_ROOT / "eda_report" / device
    cache_path = out_dir / "labels.json"

    outlier_rows = df[df["is_outlier"]]
    bundle = llm_labeler.label_device(df, outlier_rows, device, cache_path)

    temps_included = sorted(df["temp"].dropna().unique().tolist())
    report_path = report.build_report(device, df, bundle, cluster_info, out_dir, temps_included)

    logger.info("device=%s: EDA complete -> %s", device, report_path)
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="MOS model-vs-measurement error EDA (M3)")
    parser.add_argument(
        "--device", required=True, choices=MOS_DEVICES + ["all"],
        help="MOS device to analyze, or 'all' for all 4 MOS devices.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    devices = MOS_DEVICES if args.device == "all" else [args.device]
    failures = []
    for device in devices:
        try:
            run_one(device)
        except Exception:
            logger.exception("device=%s: EDA failed", device)
            failures.append(device)

    if failures:
        logger.error("EDA failed for: %s", ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
