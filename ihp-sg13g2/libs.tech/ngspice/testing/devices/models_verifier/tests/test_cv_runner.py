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
Unit tests for the C-V runner (models_verifier/cv_runner/cv_sweep_runner.py), no simulation:
  - terminal roles -> netlist nodes, and the errors for wrong roles;
  - the MOS netlist: several HIGH pins on one node, LOW pins on meter sources, floating pins
    DC-tied to the HIGH node, the AS guard, the per-file header override;
  - the pnpMPA netlist with the inverted sweep sign;
  - reading the "sweep c" table.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from models_verifier.cv_runner.cv_sweep_runner import CvSweepRunner, pin_nodes, read_cv_table, render_netlist

CONFIGS = Path(__file__).resolve().parents[2] / "configs"


def _task(template: str, setup: dict, pins: list, params: dict, sign: float = 1.0) -> dict:
    nodes = pin_nodes(setup, pins)
    return {"template_path": str(CONFIGS / template), "params": params, "nodes": [nodes[p] for p in pins],
            "low_pins": setup["low"], "float_pins": setup.get("float", []),
            "float_to": nodes[setup["float_to"]] if setup.get("float_to") else "0",
            "sweep_values": [0.5, -1.0], "sign": sign, "freq": 1e6, "device_subckt": "dut", "TEMP": "27.0",
            "corner_lib_path": "corner.lib"}


def test_pin_nodes_and_role_errors():
    assert pin_nodes({"high": ["d", "s", "b"], "low": ["g"]}, ["d", "g", "s", "b"]) == \
        {"d": "nh", "g": "nl_g", "s": "nh", "b": "nh"}
    assert pin_nodes({"high": ["b"], "low": ["d"]}, ["d", "g", "s", "b"]) == \
        {"d": "nl_d", "g": "0", "s": "0", "b": "nh"}
    with pytest.raises(ValueError, match="not a subckt pin"):
        pin_nodes({"high": ["x"], "low": ["d"]}, ["d", "g", "s", "b"])
    with pytest.raises(ValueError, match="both"):
        pin_nodes({"high": ["d"], "low": ["d"]}, ["d", "g", "s", "b"])
    with pytest.raises(ValueError, match="needs"):
        pin_nodes({"high": ["d"]}, ["d", "g", "s", "b"])


def test_mos_netlist_oxide_and_as_guard():
    setup = {"high": ["b"], "low": ["g"], "float": ["d", "s"], "float_to": "b"}
    params = {"W": 1.6e-4, "L": 2.5e-4, "AD": 0.0, "AS": 0.0, "PD": 0.0, "PS": 0.0, "NF": 1.0, "M": 3.0}
    text = render_netlist(_task("mos/cv_template.spice.j2", setup, ["d", "g", "s", "b"], params), "mos_tt", Path("o.txt"))
    assert "XU1 nf_d nl_g nf_s nh dut" in text
    assert "Rfl_d nf_d nh 1e12" in text and "Rfl_s nf_s nh 1e12" in text
    assert ".param AS=1e-30" in text
    assert "foreach vsw 0.5 -1" in text and "imag(i(Vl_g))" in text
    assert "destroy all" in text and "wrdata o.txt sweep c" in text


def test_pnp_netlist_with_inverted_sweep():
    setup = {"high": ["b"], "low": ["c"], "sign": -1}
    params = {"A": 6.4e-12, "P": 21.28e-6, "AC": 31.946e-12, "PC": 29.2e-6, "M": 12000.0}
    text = render_netlist(_task("pnp_mpa/pnpMPA_cv.spice.j2", setup, ["c", "b", "e"], params, sign=-1.0),
                          "hbt_typ", Path("o.txt"))
    assert "X1 nl_c nh 0 dut a=6.4e-12 p=2.128e-05 ac=3.1946e-11 pc=2.92e-05 m=12000" in text
    assert "foreach vsw -0.5 1" in text


def test_file_override_replaces_header_value(tmp_path):
    runner = CvSweepRunner(template_path=CONFIGS / "mos/cv_template.spice.j2", corner_lib_path=CONFIGS / "mos/cv_template.spice.j2",
                           device_subckt="dut", subckt_pins=["d", "g", "s", "b"], cv_setups={}, output_dir=tmp_path,
                           corners=["mos_tt"], file_overrides={"Cgds1_S351B_11": {"L": 130e-9}})
    params = runner._params({"W": 8e-3, "L": 250e-9, "NF": 800}, "SG13_pmos~Cgds1_S351B_11~c_g_ds~300K.mdm")
    assert params == {"W": 8e-3, "L": 130e-9, "NF": 800.0}


def test_read_cv_table(tmp_path):
    path = tmp_path / "t.txt"
    path.write_text(" 1.0e+06 -1.0e+00 1.5e-15\n 1.0e+06 0.0e+00 1.6e-15\n")
    table = read_cv_table(path)
    assert list(table["c"]) == [1.5e-15, 1.6e-15]
    assert read_cv_table(tmp_path / "missing.txt") is None
