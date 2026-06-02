#!/usr/bin/env python3
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

"""Generate offgrid.gds testcase for the 74 OffGrid DRC rules.

Each rule checks that polygons on a specific layer are aligned to the
5 nm manufacturing grid.  For every layer we place one small rectangle
with a vertex intentionally off-grid by 3 nm so the rule fires.

Usage:
    python gen_offgrid.py [--output PATH]
"""

import argparse
from pathlib import Path

import klayout.db as db

# (rule_name, layer_number, datatype)
OFFGRID_LAYERS = [
    # FEOL
    ("OffGrid.NWell", 31, 0),
    ("OffGrid.PWell", 46, 0),
    ("OffGrid.PWell_block", 46, 21),
    ("OffGrid.nBuLay", 32, 0),
    ("OffGrid.nBuLay_block", 32, 21),
    ("OffGrid.Activ", 1, 0),
    ("OffGrid.ThickGateOx", 44, 0),
    ("OffGrid.Activ_filler", 1, 22),
    ("OffGrid.GatPoly_filler", 5, 22),
    ("OffGrid.GatPoly", 5, 0),
    ("OffGrid.pSD", 14, 0),
    ("OffGrid.nSD", 7, 0),
    ("OffGrid.nSD_block", 7, 21),
    ("OffGrid.EXTBlock", 111, 0),
    ("OffGrid.SalBlock", 28, 0),
    ("OffGrid.Cont", 6, 0),
    ("OffGrid.Activ_nofill", 1, 23),
    ("OffGrid.GatPoly_nofill", 5, 23),
    # BEOL
    ("OffGrid.Metal1", 8, 0),
    ("OffGrid.Via1", 19, 0),
    ("OffGrid.Metal2", 10, 0),
    ("OffGrid.Via2", 29, 0),
    ("OffGrid.Metal3", 30, 0),
    ("OffGrid.Via3", 49, 0),
    ("OffGrid.Metal4", 50, 0),
    ("OffGrid.Via4", 66, 0),
    ("OffGrid.Metal5", 67, 0),
    ("OffGrid.MIM", 36, 0),
    ("OffGrid.Vmim", 129, 0),
    ("OffGrid.TopVia1", 125, 0),
    ("OffGrid.TopMetal1", 126, 0),
    ("OffGrid.TopVia2", 133, 0),
    ("OffGrid.TopMetal2", 134, 0),
    ("OffGrid.Passiv", 9, 0),
    # Filler
    ("OffGrid.Metal1_filler", 8, 22),
    ("OffGrid.Metal2_filler", 10, 22),
    ("OffGrid.Metal3_filler", 30, 22),
    ("OffGrid.Metal4_filler", 50, 22),
    ("OffGrid.Metal5_filler", 67, 22),
    ("OffGrid.TopMetal1_filler", 126, 22),
    ("OffGrid.TopMetal2_filler", 134, 22),
    # NoFill
    ("OffGrid.Metal1_nofill", 8, 23),
    ("OffGrid.Metal2_nofill", 10, 23),
    ("OffGrid.Metal3_nofill", 30, 23),
    ("OffGrid.Metal4_nofill", 50, 23),
    ("OffGrid.Metal5_nofill", 67, 23),
    ("OffGrid.TopMetal1_nofill", 126, 23),
    ("OffGrid.TopMetal2_nofill", 134, 23),
    ("OffGrid.NoMetFiller", 160, 0),
    # Slit
    ("OffGrid.Metal1_slit", 8, 24),
    ("OffGrid.Metal2_slit", 10, 24),
    ("OffGrid.Metal3_slit", 30, 24),
    ("OffGrid.Metal4_slit", 50, 24),
    ("OffGrid.Metal5_slit", 67, 24),
    ("OffGrid.TopMetal1_slit", 126, 24),
    ("OffGrid.TopMetal2_slit", 134, 24),
    # Miscellaneous
    ("OffGrid.EdgeSeal", 39, 0),
    ("OffGrid.EmWind", 33, 0),
    ("OffGrid.dfpad", 41, 0),
    ("OffGrid.Polimide", 98, 0),
    ("OffGrid.TRANS", 26, 0),
    ("OffGrid.IND", 27, 0),
    ("OffGrid.RES", 24, 0),
    ("OffGrid.RFMEM", 147, 0),
    ("OffGrid.Recog_diode", 99, 31),
    ("OffGrid.Recog_esd", 99, 30),
    ("OffGrid.DigiBnd", 16, 0),
    ("OffGrid.DigiSub", 60, 0),
    ("OffGrid.SRAM", 25, 0),
    ("OffGrid.dfpad_pillar", 41, 35),
    ("OffGrid.dfpad_sbump", 41, 36),
    ("OffGrid.DeepVia", 152, 0),
    ("OffGrid.LBE", 157, 0),
    ("OffGrid.PolyRes", 128, 0),
]


def generate_offgrid_gds(output_path: Path) -> None:
    """Create a GDS with one off-grid rectangle per layer."""
    layout = db.Layout()
    layout.dbu = 0.001  # 1 nm database unit

    top = layout.create_cell("offgrid")

    spacing = 10_000  # 10 um between shapes (in dbu)

    for idx, (rule_name, layer_no, datatype) in enumerate(OFFGRID_LAYERS):
        layer_idx = layout.layer(layer_no, datatype)
        x_offset = idx * spacing

        # Rectangle with one vertex off-grid by 3 nm.
        # Grid is 5 nm = 5 dbu.  3 nm = 3 dbu is not aligned to 5 nm.
        # Box: (x, 0) to (x + 1003, 1000) -- right edge at x+1003 is off-grid
        top.shapes(layer_idx).insert(
            db.Box(x_offset, 0, x_offset + 1003, 1000)
        )

    layout.write(str(output_path))
    print(f"Generated {output_path} with {len(OFFGRID_LAYERS)} off-grid test shapes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate offgrid.gds testcase")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "unit" / "offgrid.gds",
        help="Output GDS path",
    )
    args = parser.parse_args()
    generate_offgrid_gds(args.output)
