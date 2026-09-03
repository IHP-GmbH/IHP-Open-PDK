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
Milestone M2 -- per-device waiver ("known failure baseline") store.

Design mirrors the DRC regression waiver mechanism in
`ihp-sg13g2/libs.tech/klayout/tech/drc/testing/run_regression_cells.py`
(`WAIVER_PROFILES` / `WAIVED_GROUPS` / `build_waived_tests()`, verdict
`actual violations subset-of allowed -> "Passed (Waived)"`, else `"Failed"`
-- see that module's ~lines 76-175 and the verdict logic at ~lines 532-554).

Here the "actual" is a single range-check report row's `percentage_oob` and the
"allowed" set is the `snapshot_percentage_oob` (+ `margin`) recorded when the waiver
was generated: a row that is no worse than its snapshot is waived; a row that regressed
beyond the snapshot + margin is rejected (kept `Failed`) even though a waiver entry
exists for that key, exactly like an out-of-profile DRC rule would fail the cell.

Stable waiver key: `(device, input_data, block_index, metric, target)`.
`block_id` (a per-run `uuid4`, see `mdm_processing/parser.py::_generate_block_id`) is
UNSTABLE across runs and is deliberately NOT part of the key.

Each device gets its own YAML file at `waivers/<device>.yaml` (device name taken from
the device's config `device_name`, e.g. "sg13_lv_nmos", "npn13g2", "pnpMPA" -- NOT the
Makefile target name), so `device` does not need to be repeated inside every entry; it
is still accepted as the first element of the lookup key for parity with the spec and
as a defensive sanity check (a mismatch only logs a warning, it never raises).

YAML shape (see `generate.py` for the writer):

    device: sg13_lv_nmos
    generated: "2026-07-09"
    margin_default: 1.0
    waivers:
      - input_data: SG13_nmos~...~300K.mdm
        block_index: 0
        metric: ib
        target: meas
        reason: "baseline snapshot 2026-07-09"
        snapshot_percentage_oob: 51.485
        snapshot_deviation_max: 0.00023
        margin: 1.0
        date: "2026-07-09"
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Tuple

import yaml

# Default margin, in percentage points of `percentage_oob`, added on top of the
# snapshotted value when deciding whether a currently observed row is still covered by
# its waiver. A row whose current `percentage_oob` exceeds
# `snapshot_percentage_oob + margin` is a WORSE regression than what was baselined and
# is intentionally NOT waived (see GOAL_DEV_VER.md M2 "Waiver staleness" risk note).
DEFAULT_MARGIN_PP: float = 1.0

# Full, spec-mandated lookup key: (device, input_data, block_index, metric, target).
WaiverKey = Tuple[str, str, str, str, str]

# Internal per-file key (device is implicit -- one file per device): the trailing 4
# elements of WaiverKey.
_EntryKey = Tuple[str, str, str, str]


def _norm(value: object) -> str:
    """Normalize a key component to a stable string: None/NaN -> "" ."""
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value)


def make_key(device: object, input_data: object, block_index: object, metric: object, target: object) -> WaiverKey:
    """Build the stable 5-tuple waiver key from raw (possibly NaN/None) values."""
    return (_norm(device), _norm(input_data), _norm(block_index), _norm(metric), _norm(target))


@dataclass
class WaiverEntry:
    """One baselined (device, input_data, block_index, metric, target) failure."""

    reason: str = ""
    snapshot_percentage_oob: float = 0.0
    snapshot_deviation_max: float = 0.0
    margin: float = DEFAULT_MARGIN_PP
    date: str = ""

    def allows(self, percentage_oob: float) -> bool:
        """
        True when `percentage_oob` is no worse than the snapshot (+ margin). A WORSE
        regression than the baseline is rejected -- the waiver does not apply.
        """
        return float(percentage_oob) <= self.snapshot_percentage_oob + self.margin


@dataclass
class WaiverStore:
    """Loaded waiver entries for exactly one device."""

    device: str
    entries: Dict[_EntryKey, WaiverEntry] = field(default_factory=dict)
    path: Optional[Path] = None

    @staticmethod
    def _entry_key(input_data: object, block_index: object, metric: object, target: object) -> _EntryKey:
        return (_norm(input_data), _norm(block_index), _norm(metric), _norm(target))

    @classmethod
    def load(cls, device: str, waivers_dir: Path | str) -> "WaiverStore":
        """
        Load `waivers/<device>.yaml`. Missing file / empty `waivers:` list -> an empty
        store (nothing waived), so devices with no waiver file behave exactly as before
        Milestone M2 existed.
        """
        path = Path(waivers_dir) / f"{device}.yaml"
        store = cls(device=device, path=path)

        if not path.exists():
            logging.info(
                "No waiver file for device '%s' (%s not found) -- 0 waivers loaded.",
                device, path,
            )
            return store

        try:
            raw = yaml.safe_load(path.read_text()) or {}
        except Exception as e:
            logging.error("Failed to parse waiver file %s: %s -- treating as empty.", path, e)
            return store

        for item in raw.get("waivers", []) or []:
            try:
                key = cls._entry_key(
                    item["input_data"], item["block_index"], item["metric"], item["target"]
                )
                store.entries[key] = WaiverEntry(
                    reason=str(item.get("reason", "")),
                    snapshot_percentage_oob=float(item["snapshot_percentage_oob"]),
                    snapshot_deviation_max=float(item.get("snapshot_deviation_max", 0.0) or 0.0),
                    margin=float(item.get("margin", DEFAULT_MARGIN_PP)),
                    date=str(item.get("date", "")),
                )
            except (KeyError, TypeError, ValueError) as e:
                logging.warning("Skipping malformed waiver entry in %s: %r (%s)", path, item, e)

        logging.info("Loaded %d waiver(s) for device '%s' from %s", len(store.entries), device, path)
        return store

    def is_waived(self, key: WaiverKey, percentage_oob: float) -> bool:
        """
        True only if `key` (the full 5-tuple `(device, input_data, block_index, metric,
        target)`) has a matching waiver entry AND `percentage_oob` is no worse than
        that entry's snapshot (+ margin). A device mismatch only warns (defensive; the
        store is always loaded for a single device) and still looks the entry up.
        """
        device, input_data, block_index, metric, target = key
        if device and self.device and device != self.device:
            logging.warning(
                "WaiverStore for '%s' queried with key for device '%s' -- ignoring "
                "device mismatch and matching on (input_data, block_index, metric, "
                "target) only.",
                self.device, device,
            )
        entry = self.entries.get(self._entry_key(input_data, block_index, metric, target))
        if entry is None:
            return False
        return entry.allows(percentage_oob)

    def get(self, key: WaiverKey) -> Optional[WaiverEntry]:
        _device, input_data, block_index, metric, target = key
        return self.entries.get(self._entry_key(input_data, block_index, metric, target))

    def __len__(self) -> int:
        return len(self.entries)
