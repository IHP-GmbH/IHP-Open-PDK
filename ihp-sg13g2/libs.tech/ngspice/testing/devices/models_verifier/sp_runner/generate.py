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
Milestone M4 -- S-parameter waiver generator.

Snapshots a device's CURRENT (non-waived) `Failed` S-param range-check rows (cje/cjc/ft)
into `waivers/sparam/<device_name>.yaml`, so a subsequent `make test-<device>-sparam`
treats today's known model-vs-measurement RF gaps as baselined (`Passed (Waived)`) while
any NEW or WORSE deviation still fails.

Reuses the exact same pipeline via `SparamVerifier._run_sparam_pipeline()` and the M2
generator's YAML/serialisation helpers (imported, not modified). S-param waivers are kept
in a SEPARATE directory (`waivers/sparam/`) from the DC waivers (`waivers/`) so that the
DC `make waive-all` (which rewrites `waivers/<device>.yaml` wholesale) never clobbers them.

Usage (from `$DEV`, with `PYTHONPATH=$PWD`):
    python -m models_verifier.sp_runner.generate --device npn13g2l
    python -m models_verifier.sp_runner.generate --device all      # all 3 HBT devices
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

import yaml

from models_verifier.sp_runner.verifier import SparamVerifier
from models_verifier.waivers.generate import (
    DEVICE_CONFIGS,
    _DEV_ROOT,
    _max_deviation,
    _round_sig,
    _yaml_value,
)
from models_verifier.waivers.waiver import DEFAULT_MARGIN_PP

# The three HBT devices carry S-parameter characteristics.
SPARAM_DEVICES = ["npn13g2", "npn13g2l", "npn13g2v"]

DEFAULT_SPARAM_WAIVERS_DIR = _DEV_ROOT / "waivers" / "sparam"


def snapshot_device(
    device: str,
    waivers_dir: Path = DEFAULT_SPARAM_WAIVERS_DIR,
    margin: float = DEFAULT_MARGIN_PP,
) -> Path:
    """Run the S-param pipeline for `device` and write its Failed rows to YAML."""
    if device not in DEVICE_CONFIGS:
        raise SystemExit(f"Unknown device '{device}'. Known: {sorted(DEVICE_CONFIGS)}")

    verifier = SparamVerifier(DEVICE_CONFIGS[device])
    full_res, detailed_failures, _stats = verifier._run_sparam_pipeline(waivers_dir=waivers_dir)

    if "status" in full_res.columns:
        failed = full_res[full_res["status"] == "Failed"]
    else:  # defensive; pipeline always adds "status"
        failed = full_res[~full_res["passed"].astype(bool)]

    today = date.today().isoformat()
    entries = []
    for row in failed.itertuples(index=False):
        input_data = getattr(row, "input_data", None)
        block_index = getattr(row, "block_index", None)
        entries.append({
            "input_data": _yaml_value(input_data),
            "block_index": _yaml_value(block_index),
            "metric": str(row.metric),
            "target": str(row.target),
            "reason": f"S-param baseline snapshot {today}",
            "snapshot_percentage_oob": _round_sig(float(row.percentage_oob), 10),
            "snapshot_deviation_max": _round_sig(
                _max_deviation(detailed_failures, input_data, block_index, row.metric, row.target), 10
            ),
            "margin": margin,
            "date": today,
        })

    waivers_dir = Path(waivers_dir)
    waivers_dir.mkdir(parents=True, exist_ok=True)
    out_path = waivers_dir / f"{verifier.device_name}.yaml"
    doc = {
        "device": verifier.device_name,
        "generated": today,
        "margin_default": margin,
        "waivers": entries,
    }
    out_path.write_text(yaml.safe_dump(doc, sort_keys=False, default_flow_style=False))
    logging.info("Wrote %d S-param waiver entr%s to %s", len(entries),
                 "y" if len(entries) == 1 else "ies", out_path)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="models_verifier.sp_runner.generate",
        description="Snapshot a device's current Failed S-param rows into waivers/sparam/<device>.yaml.",
    )
    parser.add_argument("--device", "-d", required=True,
                        help=f"Device key, one of {SPARAM_DEVICES} or 'all'.")
    parser.add_argument("--waivers-dir", type=Path, default=DEFAULT_SPARAM_WAIVERS_DIR)
    parser.add_argument("--margin", type=float, default=DEFAULT_MARGIN_PP)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    devices = list(SPARAM_DEVICES) if args.device == "all" else [args.device]
    for dev in devices:
        snapshot_device(dev, waivers_dir=args.waivers_dir, margin=args.margin)
    return 0


if __name__ == "__main__":
    sys.exit(main())
