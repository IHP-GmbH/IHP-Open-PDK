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
Milestone M2 -- waiver generator.

Snapshots a device's CURRENT (non-waived) `Failed` range-check rows into
`waivers/<device_name>.yaml`, so a subsequent `make test-<device>` treats today's known
sim-vs-measurement gaps as baselined (`Passed (Waived)`) while any NEW or WORSE
deviation still fails (see `models_verifier/waivers/waiver.py`).

Reuses the full aggregate -> simulate -> range-check -> waiver-apply pipeline via
`MdmVerifier._run_pipeline()` (see `models_verifier/models_verifier.py`) -- no
simulation/parsing logic is duplicated here.

Usage (from `$DEV`, with `PYTHONPATH=$PWD`):
    python -m models_verifier.waivers.generate --device nmos_lv
    python -m models_verifier.waivers.generate --device all   # all 8 devices

Also wired to `make waive-all` in the Makefile.
"""

from __future__ import annotations

import argparse
import logging
import math
import sys
from datetime import date
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import yaml

from models_verifier.waivers.waiver import DEFAULT_MARGIN_PP

# $DEV root (two levels up from this file: models_verifier/waivers/generate.py -> $DEV).
_DEV_ROOT = Path(__file__).resolve().parents[2]

# Maps the Makefile-style device key (matches `ALL_DEVICES` in the Makefile) to its
# config YAML. Kept in sync with the Makefile's `*_CONFIG` variables.
DEVICE_CONFIGS: Dict[str, Path] = {
    "nmos_lv": _DEV_ROOT / "configs/mos/nmos_lv/sg13_lv_nmos.yaml",
    "pmos_lv": _DEV_ROOT / "configs/mos/pmos_lv/sg13_lv_pmos.yaml",
    "nmos_hv": _DEV_ROOT / "configs/mos/nmos_hv/sg13_hv_nmos.yaml",
    "pmos_hv": _DEV_ROOT / "configs/mos/pmos_hv/sg13_hv_pmos.yaml",
    "pnp_mpa": _DEV_ROOT / "configs/pnp_mpa/pnpmpa.yaml",
    "npn13g2": _DEV_ROOT / "configs/hbt/npn13g2/npn13g2.yaml",
    "npn13g2l": _DEV_ROOT / "configs/hbt/npn13g2l/npn13g2l.yaml",
    "npn13g2v": _DEV_ROOT / "configs/hbt/npn13g2v/npn13g2v.yaml",
}

DEFAULT_WAIVERS_DIR = _DEV_ROOT / "waivers"


def _max_deviation(
    detailed_failures_df: pd.DataFrame,
    input_data: object,
    block_index: object,
    metric: object,
    target: object,
) -> float:
    """Max |deviation| among point-level failures matching this row's key, or 0.0."""
    if detailed_failures_df is None or detailed_failures_df.empty or "deviation" not in detailed_failures_df.columns:
        return 0.0

    df = detailed_failures_df
    mask = (df["metric"].astype(str) == str(metric)) & (df["target"].astype(str) == str(target))
    if "input_data" in df.columns:
        mask &= df["input_data"].astype(str) == ("" if pd.isna(input_data) else str(input_data))
    if "block_index" in df.columns:
        mask &= df["block_index"].astype(str) == ("" if pd.isna(block_index) else str(block_index))

    sub = df[mask]
    if sub.empty:
        return 0.0
    return float(sub["deviation"].abs().max())


def _round_sig(value: float, sig: int = 10) -> float:
    """
    Round to `sig` significant figures (not decimal places): plain `round(x, 6)` would
    zero out small-magnitude current deviations (e.g. ~1e-9 A), which are common here
    since `metric` values are frequently currents. 0.0 rounds to 0.0.
    """
    if value == 0.0 or not math.isfinite(value):
        return float(value)
    return float(round(value, -int(math.floor(math.log10(abs(value)))) + (sig - 1)))


def _yaml_value(v: object) -> Optional[object]:
    """Coerce a pandas scalar to a plain, YAML-safe Python value (or None)."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, (int,)) or (hasattr(v, "item") and not isinstance(v, str)):
        try:
            item = v.item() if hasattr(v, "item") else v
            if isinstance(item, float) and item.is_integer():
                return int(item)
            return item
        except Exception:
            return v
    return v


def snapshot_device(
    device: str,
    waivers_dir: Path = DEFAULT_WAIVERS_DIR,
    margin: float = DEFAULT_MARGIN_PP,
) -> Path:
    """
    Run the full verification pipeline for `device` and write its current `Failed`
    rows into `waivers/<device_name>.yaml`. Returns the written path.
    """
    if device not in DEVICE_CONFIGS:
        raise SystemExit(
            f"Unknown device '{device}'. Known devices: {sorted(DEVICE_CONFIGS)}"
        )

    # Local import to avoid a circular import at module load time (models_verifier.py
    # also lives in this package and does not import waivers/generate.py).
    from models_verifier.models_verifier import MdmVerifier

    config_path = DEVICE_CONFIGS[device]
    verifier = MdmVerifier(config_path)
    full_res, detailed_failures, _stats = verifier._run_pipeline(waivers_dir=waivers_dir)

    if "status" in full_res.columns:
        failed = full_res[full_res["status"] == "Failed"]
    else:  # defensive; _run_pipeline always adds "status"
        failed = full_res[~full_res["passed"].astype(bool)]

    today = date.today().isoformat()
    waiver_entries = []
    for row in failed.itertuples(index=False):
        input_data = getattr(row, "input_data", None)
        block_index = getattr(row, "block_index", None)
        metric = row.metric
        target = row.target
        percentage_oob = float(row.percentage_oob)
        deviation_max = _max_deviation(detailed_failures, input_data, block_index, metric, target)

        waiver_entries.append(
            {
                "input_data": _yaml_value(input_data),
                "block_index": _yaml_value(block_index),
                "metric": str(metric),
                "target": str(target),
                "reason": f"baseline snapshot {today}",
                "snapshot_percentage_oob": _round_sig(percentage_oob, 10),
                "snapshot_deviation_max": _round_sig(deviation_max, 10),
                "margin": margin,
                "date": today,
            }
        )

    waivers_dir = Path(waivers_dir)
    waivers_dir.mkdir(parents=True, exist_ok=True)
    out_path = waivers_dir / f"{verifier.device_name}.yaml"

    doc = {
        "device": verifier.device_name,
        "generated": today,
        "margin_default": margin,
        "waivers": waiver_entries,
    }
    out_path.write_text(yaml.safe_dump(doc, sort_keys=False, default_flow_style=False))

    logging.info(
        "Wrote %d waiver entr%s to %s (device key '%s' -> device_name '%s')",
        len(waiver_entries), "y" if len(waiver_entries) == 1 else "ies",
        out_path, device, verifier.device_name,
    )
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="models_verifier.waivers.generate",
        description="Snapshot a device's current Failed range-check rows into waivers/<device>.yaml.",
    )
    parser.add_argument(
        "--device", "-d",
        required=True,
        help=f"Device key, one of: {sorted(DEVICE_CONFIGS)} or 'all'.",
    )
    parser.add_argument(
        "--waivers-dir",
        type=Path,
        default=DEFAULT_WAIVERS_DIR,
        help="Directory to write waivers/<device>.yaml into (default: $DEV/waivers).",
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=DEFAULT_MARGIN_PP,
        help=f"Margin in percentage points added on top of the snapshot (default: {DEFAULT_MARGIN_PP}).",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    devices = list(DEVICE_CONFIGS) if args.device == "all" else [args.device]
    for dev in devices:
        snapshot_device(dev, waivers_dir=args.waivers_dir, margin=args.margin)

    return 0


if __name__ == "__main__":
    sys.exit(main())
