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
Unit checks for bias fidelity of the DC simulation path:

  - IC-CAP SYNC'd inputs (``vc ... SYNC 1 <offset> vb``) are parsed from the MDM header,
    the compact sweep row keeps the MASTER as the sweep variable and carries the relation
    for the slave, and the rendered netlist ties the slave source to the master node
    (``Vc c b <offset>``) instead of holding it at 0 V (which simulated every forward
    Gummel at VCB=const with VBE = 0).
  - The template's sweep-type branches match case-insensitively (the runner passes
    lower-case ``vcb``/``vbe``/``vce``).
  - Current clipping is sign-preserving (negative currents are not collapsed onto the
    positive floor).
  - ``design_param_overrides`` replaces design-parameter columns case-insensitively.

No pytest dependency is required. Run standalone from $DEV (PYTHONPATH=$PWD):
    python models_verifier/tests/test_sync_sweep.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, StrictUndefined

_DEV_ROOT = Path(__file__).resolve().parents[2]
if str(_DEV_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEV_ROOT))

from models_verifier.mdm_processing.parser import MdmParser  # noqa: E402
from models_verifier.mdm_processing.utils import parse_header_sync  # noqa: E402
from models_verifier.models_verifier import MdmVerifier  # noqa: E402

_HEADER = """BEGIN_HEADER
 ICCAP_INPUTS
  ve         V  E GROUND SMU_E 0.1 CON        0
  vc         V  C GROUND SMU_C 0.1 SYNC       1 -0.5 vb
  vs         V  S GROUND SMU_S 0.015 CON        0
  vb         V  B GROUND SMU_B 0.015 LIN        1    0.6        0.8        3    0.1
 ICCAP_OUTPUTS
  ib         I  B GROUND SMU_B M
  ic         I  C GROUND SMU_C M
 ICCAP_VALUES
  TNOM "27"
  TEMP "27"
  DEV_GEOM_L "0.9"
  DEV_GEOM_W "0.07"
  NUM_OF_TRANS_RF "1"
  REMARKS "Nx=8; synthetic"
END_HEADER
"""

_MDM = _HEADER + """
BEGIN_DB
 ICCAP_VAR ve         0
 ICCAP_VAR vs         0

 #vb              vc              ib              ic
  0.6             0.1             1e-9            1e-7
  0.7             0.2             1e-8            1e-6
  0.8             0.3             1e-7            1e-5
END_DB
"""


def _render(template: str, **ctx) -> str:
    tpl_path = _DEV_ROOT / template
    env = Environment(
        loader=FileSystemLoader(str(tpl_path.parent)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    base = dict(
        model_corner_lib="cornerHBT.lib", corner="hbt_typ", TEMP="27", device_subckt="npn13g2",
        out_path="out.csv", sweep_src="Vb", sweep_node="b", sweep_start="0.6",
        sweep_stop="0.8", sweep_step="0.1", W="0.07", L="0.9", Nx="8", M="1",
        A="2e-12", P="6e-6", output_vars=["ib", "ic"],
    )
    base.update(ctx)
    return env.get_template(tpl_path.name).render(**base)


def test_parse_header_sync():
    sync = parse_header_sync(_HEADER.splitlines())
    assert sync == {"vc": (1.0, -0.5, "vb")}, sync


def test_compact_row_keeps_master_and_carries_sync_relation():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "fg_vcbm05_RF.mdm"
        path.write_text(_MDM)
        parser = MdmParser(path, device_type="hbt")
        full = parser.parse()
        row = parser.compact_rows[0]
    assert row["sweep_var"] == "vb", row
    assert row["vb"].split()[:2] == ["0.6", "0.8"], row
    assert row["vc"] == "sync 1 -0.5 vb", row
    assert row["Nx"] == 8 and row["L"] == 0.9
    # The measured (full) table still carries the slave's per-point values for the merge.
    assert list(full["vc"]) == [0.1, 0.2, 0.3]
    assert full["input_vars"].iloc[0] == "vb,vc,ve,vs"  # sorted -> deterministic


def test_hbt_template_ties_synced_source_to_master_node():
    for tpl in ("configs/hbt/hbt_dc.spice.j2", "configs/pnp_mpa/pnpMPA_dc.spice.j2"):
        net = _render(tpl, sweep_var="vb", VB=0.6, VC=0.0, VE=0.0,
                      sync={"vc": {"master_node": "b", "offset": "-0.5"}})
        lines = [ln.strip() for ln in net.splitlines()]
        # Slave referenced to a VCVS copy of the master node, never to the node itself
        # (that would push IC through Vb and make the simulated IB read IB+IC).
        assert "Evc_sync vc_sync 0 b 0 1" in lines and "Vc c vc_sync -0.5" in lines, net
        assert not any(ln.startswith("Vc c b") for ln in lines), net
        assert "Vb b 0 0.6" in lines and "Ve e 0 0.0" in lines, net
        assert "dc Vb 0.6 0.8 0.1" in lines, net
        # Without a sync entry the legacy constant source is emitted unchanged.
        net2 = _render(tpl, sweep_var="vb", VB=0.6, VC=1.0, VE=0.0, sync={})
        assert "Vc c 0 1.0" in [ln.strip() for ln in net2.splitlines()], net2


def test_template_branches_match_lower_case_sweep_var():
    net = _render("configs/hbt/hbt_dc.spice.j2", sweep_var="vcb", sweep_src="Vc",
                  sweep_node="c", VCB=0.0, VE=0.0)
    lines = [" ".join(ln.split()) for ln in net.splitlines()]
    assert "Vb b c 0" in lines and "Vc c 0 0" in lines, net


def test_clip_is_sign_preserving():
    s = pd.Series([-3e-13, -2e-3, 0.0, 4e-13, 5e-3, float("nan")])
    out = MdmVerifier._clip_current_sign_preserving(s, 1e-12)
    assert out.iloc[0] == -1e-12 and out.iloc[1] == -2e-3, out.tolist()
    assert out.iloc[2] == 1e-12 and out.iloc[3] == 1e-12 and out.iloc[4] == 5e-3, out.tolist()
    assert pd.isna(out.iloc[5])


def test_design_param_overrides_are_case_insensitive():
    df = pd.DataFrame({"block_id": ["a", "b"], "Nx": [5, 5], "L": [2.5, 2.5]})
    out = MdmVerifier._apply_design_overrides(df, {"nx": 4})
    assert list(out["Nx"]) == [4, 4] and "nx" not in out.columns, out
    assert list(df["Nx"]) == [5, 5]  # input untouched


def test_noise_floor_agreement_is_not_oob():
    from models_verifier.error_analyzer.config import MetricSpec, Threshold
    from models_verifier.error_analyzer.range_checker import RangeChecker
    # 4 points: two genuine agreements (in-band), one both-at-floor with OPPOSITE signs
    # (measured +1e-11 noise vs simulated -1e-11) and one real mismatch (meas at floor,
    # model at 5e-10).
    df = pd.DataFrame({
        "block_id": ["b"] * 4, "block_index": [0] * 4, "input_data": ["x.mdm"] * 4,
        "output_vars": ["ib"] * 4, "vb": [0.1, 0.2, 0.3, 0.4],
        "ib_meas": [1e-6, 2e-6, 1e-11, 1e-11],
        "ib_sim_mos_tt": [1e-6, 2e-6, -1e-11, 5e-10],
        "ib_sim_mos_ss": [0.9e-6, 1.9e-6, -1e-11, 4e-10],
        "ib_sim_mos_ff": [1.1e-6, 2.1e-6, -1e-11, 6e-10],
    })
    def run(floor):
        spec = MetricSpec(name="ib", meas="ib_meas", tt="ib_sim_mos_tt", ss="ib_sim_mos_ss",
                          ff="ib_sim_mos_ff", noise_floor=floor)
        rep, _ = RangeChecker(metrics=[spec], default_threshold=Threshold(max_out_of_range_percent=0.5)).analyze(df)
        return rep[rep.target == "meas"].iloc[0]
    with_floor = run(1e-11)
    assert int(with_floor.n_out_of_bounds) == 1 and int(with_floor.n_floor) == 1, with_floor.to_dict()
    without = run(None)
    assert int(without.n_out_of_bounds) == 2 and int(without.n_floor) == 0, without.to_dict()


def _run_all() -> None:
    tests = [
        test_parse_header_sync,
        test_compact_row_keeps_master_and_carries_sync_relation,
        test_hbt_template_ties_synced_source_to_master_node,
        test_template_branches_match_lower_case_sweep_var,
        test_clip_is_sign_preserving,
        test_design_param_overrides_are_case_insensitive,
        test_noise_floor_agreement_is_not_oob,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"{len(tests)}/{len(tests)} checks passed")


if __name__ == "__main__":
    _run_all()
