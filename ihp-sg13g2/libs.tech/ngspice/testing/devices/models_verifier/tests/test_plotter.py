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
Tests of the figure script (validation/plot_verification_results.py) and of the band columns the
verifier writes for it: unique figure names, the swept bias of each table type, and the verdicts
read from the final reports (out-of-band and not-simulated points).
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance  # noqa: E402
from models_verifier.error_analyzer.range_checker import RangeChecker  # noqa: E402

_spec = importlib.util.spec_from_file_location("plot_verification_results",
                                               _ROOT / "validation" / "plot_verification_results.py")
plotter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(plotter)


def _block(input_data: str, block_index: int = 0) -> pd.DataFrame:
    return pd.DataFrame({"input_data": [input_data], "block_index": [block_index]})


def test_figure_names_keep_the_temperature():
    names = {plotter.figure_stem(_block(f"SG13_nmos~DUT_1~dc_idvg~{t}.mdm"), "id") for t in ("233K", "300K", "398K")}
    assert len(names) == 3
    assert plotter.figure_stem(_block("fo_vb_RF.mdm", 4), "id") == "fo_vb_RF_b4"


def test_sweep_of_each_table_type():
    dc = pd.DataFrame({"sweep_var": ["vb"], "vb": [0.7], "vc": [1.0]})
    cv = pd.DataFrame({"input_vars": ["vbc,ve"] * 3, "vbc": [0.5, 0.0, -0.5], "ve": [0.0] * 3})
    sp = pd.DataFrame({"vb": [0.6, 0.7, 0.8], "vc": [1.0, 1.0, 1.0], "ve": [0.0] * 3})
    assert plotter.ensure_sweep_columns(dc)["sweep_var"].iloc[0] == "vb"
    assert plotter.ensure_sweep_columns(cv)["sweep_var"].iloc[0] == "vbc"     # not the constant ve
    assert plotter.ensure_sweep_columns(sp)["sweep_var"].iloc[0] == "vb"


def test_verdicts_separate_out_of_band_and_not_simulated_points(tmp_path):
    reports = tmp_path / "final_reports"
    reports.mkdir()
    pd.DataFrame({"input_data": ["f.mdm"], "block_index": [0], "metric": ["ic"], "target": ["meas"],
                  "status": ["Failed (not simulated)"]}).to_csv(reports / "full_results.csv", index=False)
    pd.DataFrame({"input_data": ["f.mdm", "f.mdm"], "block_index": [0, 0], "metric": ["ic", "ic"],
                  "target": ["meas", "meas"], "vb": [0.7, 0.8], "lower_bound": [1e-6, np.nan]}
                 ).to_csv(reports / "failed_results.csv", index=False)
    status, oob, missing = plotter.Verdicts(tmp_path).lookup("f.mdm", 0, "ic", "vb")
    assert status == "Failed (not simulated)" and oob == {0.7} and missing == {0.8}
    assert plotter._STATUS_FOLDER[status] == "failed_not_simulated"


def test_band_columns_follow_the_check():
    """The band written for the figures is the band the checker used, and only judged points are marked."""
    vb = np.round(np.linspace(0.6, 0.9, 7), 3)
    tt = 1e-6 * np.exp((vb - 0.7) / 0.026)
    curve = pd.DataFrame({"block_id": "b", "input_data": "f.mdm", "block_index": 0, "output_vars": "ic",
                          "vb": vb, "ic_meas": tt * 1.01, "ic_sim_typ": tt, "ic_sim_bcs": tt * 0.9,
                          "ic_sim_Wcs": tt * 1.1})
    curve.loc[3, "ic_sim_bcs"] = np.nan            # one point not simulated: not judged, no band
    checker = RangeChecker(
        metrics=[MetricSpec(name="ic", meas="ic_meas", tt="ic_sim_typ", ss="ic_sim_bcs", ff="ic_sim_Wcs",
                            tolerance=Tolerance(abs=0.0, rel=5.0))],          # 5 %
        default_threshold=Threshold(max_out_of_range_percent=0.5),
    )
    checker.analyze(curve)
    band = checker.bands
    assert "ic_band_lo" in band.columns and "ic_judged" in band.columns
    assert list(band["ic_judged"]) == [True, True, True, False, True, True, True]
    assert np.allclose(band["ic_band_lo"][[0, 1, 2, 4, 5, 6]], (tt * 0.9 * 0.95)[[0, 1, 2, 4, 5, 6]])
