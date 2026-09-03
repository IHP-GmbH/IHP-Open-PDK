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
Unit check for the Milestone M1 MQA bias-window pre-filter.

Builds a small synthetic DataFrame with sweep points inside and outside a configured
`mqa_ranges` bias window (VBE derived from NODE voltages vb/ve, mirroring a real
"fg_vcb0_RF.mdm" forward-Gummel-at-VCB=0 block) and asserts:
  - the in-window mask built by RangeChecker._build_window_mask flags exactly the
    expected points (unit level), and
  - RangeChecker.analyze() reports the correct post-window `n_points`/`n_excluded` for
    the metric/target pair (end-to-end / pipeline level), and
  - when no window is configured (mqa_ranges=None / no matching characteristic), NO
    filtering happens at all (regression guard for MOS/PNP configs), and
  - the characteristic-stem normalization is an EXACT match, not a prefix match
    (e.g. "fg_vcb0" must never match "fg_vcb05").

No pytest dependency is required. Run standalone:
    python models_verifier/tests/test_mqa_window.py
(from $DEV, with PYTHONPATH=$PWD — see $DEV/README.md "How to run"). Also collectible by
pytest if/when it is installed in the environment.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Make `python models_verifier/tests/test_mqa_window.py` work even if PYTHONPATH was not
# exported first (the documented recipe is `export PYTHONPATH=$PWD` from $DEV).
_DEV_ROOT = Path(__file__).resolve().parents[2]
if str(_DEV_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEV_ROOT))

from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance  # noqa: E402
from models_verifier.error_analyzer.range_checker import RangeChecker  # noqa: E402


def _make_group_df() -> pd.DataFrame:
    """
    Synthetic single-block sweep modeled after "fg_vcb0_RF.mdm": VCB=0 (vc == vb),
    ve=0, so VBE = vb - ve = vb. 7 points; a window of vbe in [0.7, 0.8] keeps 3
    (0.70/0.75/0.80) and excludes 4 (0.60/0.65/0.85/0.90).
    """
    vb = [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90]
    n = len(vb)
    ib_meas = [1e-9 * (i + 1) for i in range(n)]
    return pd.DataFrame(
        {
            "block_id": ["blk0"] * n,
            "block_index": [0] * n,
            "input_data": ["fg_vcb0_RF.mdm"] * n,
            "output_vars": ["ib"] * n,
            "vb": vb,
            "vc": vb,  # VCB = vc - vb = 0
            "ve": [0.0] * n,  # VBE = vb - ve = vb
            "ib_meas": ib_meas,
            # Wide envelope so every point is trivially in-bounds; isolates the test to
            # the window mechanism rather than the separate OOB pass/fail logic.
            "ib_sim_hbt_typ": ib_meas,
            "ib_sim_hbt_bcs": [v - 1e-9 for v in ib_meas],
            "ib_sim_hbt_Wcs": [v + 1e-9 for v in ib_meas],
        }
    )


def _make_ib_spec() -> MetricSpec:
    return MetricSpec(
        name="ib",
        meas="ib_meas",
        tt="ib_sim_hbt_typ",
        ss="ib_sim_hbt_bcs",
        ff="ib_sim_hbt_Wcs",
        tolerance=Tolerance(),
    )


def test_window_mask_matches_expected_points():
    """Unit level: _build_window_mask flags exactly the expected in/out points."""
    df = _make_group_df()
    checker = RangeChecker(metrics=[])
    window = {"vbe": [0.7, 0.8]}

    mask, missing = checker._build_window_mask(df, window)

    assert missing == [], f"unexpected missing bias vars: {missing}"
    expected = [False, False, True, True, True, False, False]
    assert mask.tolist() == expected, f"mask={mask.tolist()} expected={expected}"


def test_analyze_reports_correct_n_points_and_n_excluded():
    """End-to-end: analyze() restricts n_points to the window and reports n_excluded."""
    df = _make_group_df()
    checker = RangeChecker(
        metrics=[_make_ib_spec()],
        default_threshold=Threshold(max_out_of_range_percent=100.0),
        mqa_ranges={"fg_vcb0": {"ib": {"vbe": [0.7, 0.8]}}},
    )

    report_df, _ = checker.analyze(df)
    meas_row = report_df[report_df["target"] == "meas"].iloc[0]

    assert int(meas_row["n_points"]) == 3, meas_row.to_dict()
    assert int(meas_row["n_excluded"]) == 4, meas_row.to_dict()
    assert int(meas_row["n_out_of_bounds"]) == 0, meas_row.to_dict()  # envelope covers all


def test_no_window_configured_means_no_filtering():
    """Regression guard: mqa_ranges=None must not filter anything (MOS/PNP behavior)."""
    df = _make_group_df()
    checker = RangeChecker(
        metrics=[_make_ib_spec()],
        default_threshold=Threshold(max_out_of_range_percent=100.0),
        mqa_ranges=None,
    )

    report_df, _ = checker.analyze(df)
    meas_row = report_df[report_df["target"] == "meas"].iloc[0]

    assert int(meas_row["n_points"]) == len(df), meas_row.to_dict()
    assert int(meas_row["n_excluded"]) == 0, meas_row.to_dict()


def test_characteristic_stem_exact_match_not_prefix():
    """'fg_vcb0' must never match 'fg_vcb05' (or vice versa) -- exact stem match only."""
    assert RangeChecker._normalize_characteristic("fg_vcb0_RF.mdm") == "fg_vcb0"
    assert RangeChecker._normalize_characteristic("fg_vcb05_RF.mdm") == "fg_vcb05"
    assert RangeChecker._normalize_characteristic(
        "fg_vcb0_RF.mdm"
    ) != RangeChecker._normalize_characteristic("fg_vcb05_RF.mdm")

    checker = RangeChecker(metrics=[], mqa_ranges={"fg_vcb0": {"ib": {"vbe": [0.7, 0.8]}}})
    # A group whose characteristic is "fg_vcb05" must NOT pick up the "fg_vcb0" window.
    assert checker._resolve_characteristic_window("fg_vcb05", "ib") is None
    assert checker._resolve_characteristic_window("fg_vcb0", "ib") == {"vbe": [0.7, 0.8]}


def _run_all() -> None:
    tests = [
        test_window_mask_matches_expected_points,
        test_analyze_reports_correct_n_points_and_n_excluded,
        test_no_window_configured_means_no_filtering,
        test_characteristic_stem_exact_match_not_prefix,
    ]
    for t in tests:
        t()
        print(f"PASS: {t.__name__}")
    print(f"\nAll {len(tests)} MQA window unit checks passed.")


if __name__ == "__main__":
    _run_all()
