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
Unit check for the Milestone M2 waiver / baseline system (`models_verifier/waivers/`).

Covers, without touching disk (except a temp dir) or running any simulation:
  - a waived key with percentage_oob <= snapshot + margin is waived;
  - the SAME key with percentage_oob > snapshot + margin (a WORSE regression) is NOT
    waived, even though a waiver entry exists for it;
  - an unknown key (not present in the waiver file) is NOT waived;
  - `block_id` (uuid4) is irrelevant to the match -- only
    (device, input_data, block_index, metric, target) matters;
  - `MdmVerifier._apply_waivers` end-to-end: sets `status` and flips `passed` only for
    genuinely-waived rows, leaving a worse-than-baseline row `Failed`.

No pytest dependency is required. Run standalone:
    python models_verifier/tests/test_waivers.py
(from $DEV, with PYTHONPATH=$PWD). Also collectible by pytest if installed.
"""

from __future__ import annotations

import sys
import tempfile
import uuid
from pathlib import Path

import pandas as pd
import yaml

_DEV_ROOT = Path(__file__).resolve().parents[2]
if str(_DEV_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEV_ROOT))

from models_verifier.waivers.waiver import WaiverStore, make_key  # noqa: E402


def _write_waiver_file(tmp_dir: Path, device: str) -> Path:
    doc = {
        "device": device,
        "generated": "2026-07-09",
        "margin_default": 1.0,
        "waivers": [
            {
                "input_data": "fg_vcb0_RF.mdm",
                "block_index": 0,
                "metric": "ic",
                "target": "meas",
                "reason": "baseline snapshot 2026-07-09",
                "snapshot_percentage_oob": 40.0,
                "snapshot_deviation_max": 0.002,
                "margin": 1.0,
                "date": "2026-07-09",
            }
        ],
    }
    waivers_dir = tmp_dir / "waivers"
    waivers_dir.mkdir(parents=True, exist_ok=True)
    (waivers_dir / f"{device}.yaml").write_text(yaml.safe_dump(doc, sort_keys=False))
    return waivers_dir


def test_waived_key_within_margin_is_waived():
    with tempfile.TemporaryDirectory() as td:
        waivers_dir = _write_waiver_file(Path(td), "npn13g2")
        store = WaiverStore.load("npn13g2", waivers_dir)
        assert len(store) == 1

        key = make_key("npn13g2", "fg_vcb0_RF.mdm", 0, "ic", "meas")
        assert store.is_waived(key, 40.0) is True   # exactly the snapshot
        assert store.is_waived(key, 40.9) is True   # within +margin (1.0 pp)
        assert store.is_waived(key, 41.0) is True   # exactly at the margin boundary


def test_worse_regression_is_not_waived():
    with tempfile.TemporaryDirectory() as td:
        waivers_dir = _write_waiver_file(Path(td), "npn13g2")
        store = WaiverStore.load("npn13g2", waivers_dir)

        key = make_key("npn13g2", "fg_vcb0_RF.mdm", 0, "ic", "meas")
        assert store.is_waived(key, 41.01) is False  # just over snapshot + margin
        assert store.is_waived(key, 99.0) is False   # badly worse


def test_unknown_key_is_not_waived():
    with tempfile.TemporaryDirectory() as td:
        waivers_dir = _write_waiver_file(Path(td), "npn13g2")
        store = WaiverStore.load("npn13g2", waivers_dir)

        other_metric = make_key("npn13g2", "fg_vcb0_RF.mdm", 0, "ib", "meas")
        other_block = make_key("npn13g2", "fg_vcb0_RF.mdm", 1, "ic", "meas")
        other_file = make_key("npn13g2", "fg_vce_RF.mdm", 0, "ic", "meas")
        assert store.is_waived(other_metric, 1.0) is False
        assert store.is_waived(other_block, 1.0) is False
        assert store.is_waived(other_file, 1.0) is False


def test_block_id_is_irrelevant_to_the_match():
    """Two rows with different (unstable) block_id but the same stable key both waive."""
    with tempfile.TemporaryDirectory() as td:
        waivers_dir = _write_waiver_file(Path(td), "npn13g2")
        store = WaiverStore.load("npn13g2", waivers_dir)

        key = make_key("npn13g2", "fg_vcb0_RF.mdm", 0, "ic", "meas")
        # block_id never enters make_key/is_waived at all -- simulate two different
        # runs (different uuid4 block_ids) producing the identical stable key.
        _run1_block_id = str(uuid.uuid4())
        _run2_block_id = str(uuid.uuid4())
        assert _run1_block_id != _run2_block_id
        assert store.is_waived(key, 39.0) is True
        assert store.is_waived(key, 39.0) is True  # unaffected by block_id churn


def test_missing_waiver_file_means_zero_waivers():
    with tempfile.TemporaryDirectory() as td:
        store = WaiverStore.load("nmos_lv_does_not_exist", Path(td) / "waivers")
        assert len(store) == 0
        key = make_key("nmos_lv_does_not_exist", "any.mdm", 0, "id", "meas")
        assert store.is_waived(key, 0.0) is False


def test_apply_waivers_end_to_end_flips_only_genuinely_waived_rows():
    """
    `MdmVerifier._apply_waivers`: a row within the waived margin flips to
    `Passed (Waived)` / passed=True; a WORSE row with the SAME key stays `Failed`; an
    already-passing row is untouched (`Passed`).
    """
    with tempfile.TemporaryDirectory() as td:
        waivers_dir = _write_waiver_file(Path(td), "npn13g2")

        # Minimal stand-in that only exercises _apply_waivers (avoids constructing a
        # full MdmVerifier, which requires a real config/output dir).
        from models_verifier.models_verifier import MdmVerifier

        class _Fake(MdmVerifier):
            def __init__(self):
                self.device_name = "npn13g2"

        verifier = _Fake()
        report_df = pd.DataFrame(
            [
                # Same key as the waiver entry, still within margin -> waived.
                {
                    "block_id": "blk-a", "input_data": "fg_vcb0_RF.mdm", "block_index": 0,
                    "metric": "ic", "target": "meas", "n_points": 52, "n_out_of_bounds": 20,
                    "percentage_oob": 38.46, "passed": False, "n_excluded": 0,
                },
                # Same key, but WORSE than snapshot+margin -> stays Failed.
                {
                    "block_id": "blk-b", "input_data": "fg_vcb0_RF.mdm", "block_index": 0,
                    "metric": "ic", "target": "meas", "n_points": 52, "n_out_of_bounds": 52,
                    "percentage_oob": 100.0, "passed": False, "n_excluded": 0,
                },
                # Different metric/key entirely -- no waiver -- already passing.
                {
                    "block_id": "blk-c", "input_data": "fg_vcb0_RF.mdm", "block_index": 0,
                    "metric": "ib", "target": "meas", "n_points": 52, "n_out_of_bounds": 0,
                    "percentage_oob": 0.0, "passed": True, "n_excluded": 0,
                },
            ]
        )

        from models_verifier.waivers.waiver import WaiverStore as _WS
        store = _WS.load("npn13g2", waivers_dir)
        result = verifier._apply_waivers(report_df, store)

        row_a = result[result["block_id"] == "blk-a"].iloc[0]
        row_b = result[result["block_id"] == "blk-b"].iloc[0]
        row_c = result[result["block_id"] == "blk-c"].iloc[0]

        assert row_a["status"] == "Passed (Waived)", row_a.to_dict()
        assert bool(row_a["passed"]) is True

        assert row_b["status"] == "Failed", row_b.to_dict()
        assert bool(row_b["passed"]) is False

        assert row_c["status"] == "Passed", row_c.to_dict()
        assert bool(row_c["passed"]) is True


def _run_all() -> None:
    tests = [
        test_waived_key_within_margin_is_waived,
        test_worse_regression_is_not_waived,
        test_unknown_key_is_not_waived,
        test_block_id_is_irrelevant_to_the_match,
        test_missing_waiver_file_means_zero_waivers,
        test_apply_waivers_end_to_end_flips_only_genuinely_waived_rows,
    ]
    for t in tests:
        t()
        print(f"PASS: {t.__name__}")
    print(f"\nAll {len(tests)} waiver unit checks passed.")


if __name__ == "__main__":
    _run_all()
