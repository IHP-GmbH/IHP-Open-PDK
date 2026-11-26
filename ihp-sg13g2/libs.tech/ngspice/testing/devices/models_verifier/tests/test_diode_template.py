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
Unit tests for the MOS junction-diode netlist (configs/mos/diode_template.spice.j2), rendered
with the context the DC runner passes (no simulation):
  - D, G and S of the stand-in transistor sit on the swept junction node;
  - AS = 0 in the header (drain diodes) becomes 1e-30, so the subcircuit keeps AD/PD;
  - a given AS (source diodes) is passed through;
  - "ib" is the current into the swept junction terminal, as the junction SMU measured.
"""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

TEMPLATE = Path(__file__).resolve().parents[2] / "configs" / "mos" / "diode_template.spice.j2"


def _render(sweep_var: str, sweep_node: str, ad: str, as_: str) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE.parent)), undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True)
    return env.get_template(TEMPLATE.name).render(
        VD="0", VS="0", VG="0", VB="0", W="1e-06", L="1e-06", AD=ad, AS=as_, PD="0.00085", PS="0",
        NF="1", M="1", sweep_node=sweep_node, sweep_var=sweep_var, device_subckt="sg13_lv_nmos",
        TEMP="27", sweep_start="0", sweep_stop="-1", sweep_step="-0.01", out_path="out.csv",
        model_corner_lib="cornerMOSlv.lib", corner="mos_tt",
    )


def test_drain_diode_ties_pins_and_guards_as():
    text = _render("vd", "d", ad="3.75e-08", as_="0")
    assert "XU1 d d d b sg13_lv_nmos" in text
    assert ".param AS=1e-30" in text and ".param AD=3.75e-08" in text
    assert "let ib = -i(vd)" in text and "wrdata out.csv v(d) ib" in text


def test_source_diode_keeps_header_as():
    text = _render("vs", "s", ad="0", as_="3.75e-08")
    assert "XU1 s s s b sg13_lv_nmos" in text
    assert ".param AS=3.75e-08" in text
    assert "let ib = -i(vs)" in text
