#!/usr/bin/env python3
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
Create DRC test GDS files for TopVia1, TopMetal1, and TopMetal1Filler rules.

SG13CMOS5L CMOS5L - Metal stack: M1-V1-M2-V2-M3-V3-M4-TV1-TM1
- TopVia1 connects Metal4 (not Metal5 as in full PDK) to TopMetal1
"""

import klayout.db as pya
from pathlib import Path

# Layer definitions for SG13CMOS5L
M4 = pya.LayerInfo(50, 0)       # Metal4
TV1 = pya.LayerInfo(125, 0)     # TopVia1
TM1 = pya.LayerInfo(126, 0)     # TopMetal1
TM1F = pya.LayerInfo(126, 22)   # TopMetal1:filler
TEXT = pya.LayerInfo(63, 0)     # Text labels

# Rule values from sg13cmos5l_tech_default.json
TV1_WIDTH = 0.42      # TV1.a: Min/max width (um)
TV1_SPACE = 0.42      # TV1.b: Min space (um)
TV1_M4_ENC = 0.10     # TV1.c: Min M4 enclosure (um)
TV1_TM1_ENC = 0.42    # TV1.d: Min TM1 enclosure (um)

TM1_WIDTH = 1.64      # TM1.a: Min width (um)
TM1_SPACE = 1.64      # TM1.b: Min space (um)

TM1FIL_MAX_W = 10.0   # TM1Fil.a1: Max filler width (um)
TM1FIL_SPACE = 3.0    # TM1Fil.c: Min filler space to TM1 (um)


def um_to_dbu(um_value, dbu=0.001):
    """Convert micrometers to database units."""
    return int(um_value / dbu)


def create_topvia1_test():
    """Create TopVia1 test GDS file with TV1.a, TV1.b, TV1.c, TV1.d violations."""
    layout = pya.Layout()
    layout.dbu = 0.001  # 1nm database unit

    top_cell = layout.create_cell("topvia1")

    m4_idx = layout.layer(M4)
    tv1_idx = layout.layer(TV1)
    tm1_idx = layout.layer(TM1)
    text_idx = layout.layer(TEXT)

    # Helper function to create box
    def box_um(x1, y1, x2, y2):
        return pya.Box(um_to_dbu(x1), um_to_dbu(y1), um_to_dbu(x2), um_to_dbu(y2))

    # ===== PASS region (left side) - good geometry =====
    # Good via: 0.42um wide
    good_via_w = TV1_WIDTH
    good_m4_enc = TV1_M4_ENC + 0.1   # Extra margin
    good_tm1_enc = TV1_TM1_ENC + 0.1  # Extra margin

    # Good via at (-15, 0)
    x_pass = -15
    # M4 rectangle
    top_cell.shapes(m4_idx).insert(box_um(
        x_pass - good_via_w/2 - good_m4_enc, -good_via_w/2 - good_m4_enc,
        x_pass + good_via_w/2 + good_m4_enc, good_via_w/2 + good_m4_enc))
    # TopVia1
    top_cell.shapes(tv1_idx).insert(box_um(
        x_pass - good_via_w/2, -good_via_w/2,
        x_pass + good_via_w/2, good_via_w/2))
    # TM1 rectangle
    top_cell.shapes(tm1_idx).insert(box_um(
        x_pass - good_via_w/2 - good_tm1_enc, -good_via_w/2 - good_tm1_enc,
        x_pass + good_via_w/2 + good_tm1_enc, good_via_w/2 + good_tm1_enc))

    # PASS label
    top_cell.shapes(text_idx).insert(pya.Text("PASS", pya.Trans(um_to_dbu(x_pass), um_to_dbu(3))))

    # ===== FAIL region (right side) - violating geometry =====
    x_fail = 5
    y_offset = 0

    # --- TV1.a test: Min/max width violation ---
    # Via too small (0.38um instead of 0.42um)
    small_via = TV1_WIDTH - 0.04
    y_a = y_offset
    top_cell.shapes(tv1_idx).insert(box_um(
        x_fail - small_via/2, y_a - small_via/2,
        x_fail + small_via/2, y_a + small_via/2))
    # Surrounding M4 and TM1 (adequate enclosure)
    top_cell.shapes(m4_idx).insert(box_um(
        x_fail - small_via/2 - 0.2, y_a - small_via/2 - 0.2,
        x_fail + small_via/2 + 0.2, y_a + small_via/2 + 0.2))
    top_cell.shapes(tm1_idx).insert(box_um(
        x_fail - small_via/2 - 0.6, y_a - small_via/2 - 0.6,
        x_fail + small_via/2 + 0.6, y_a + small_via/2 + 0.6))

    # Via too large (0.46um instead of 0.42um max)
    large_via = TV1_WIDTH + 0.04
    x_large = x_fail + 3
    top_cell.shapes(tv1_idx).insert(box_um(
        x_large - large_via/2, y_a - large_via/2,
        x_large + large_via/2, y_a + large_via/2))
    top_cell.shapes(m4_idx).insert(box_um(
        x_large - large_via/2 - 0.2, y_a - large_via/2 - 0.2,
        x_large + large_via/2 + 0.2, y_a + large_via/2 + 0.2))
    top_cell.shapes(tm1_idx).insert(box_um(
        x_large - large_via/2 - 0.6, y_a - large_via/2 - 0.6,
        x_large + large_via/2 + 0.6, y_a + large_via/2 + 0.6))

    # --- TV1.b test: Min space violation ---
    # Two vias spaced 0.38um apart (needs 0.42um)
    y_b = y_offset - 4
    via1_x = x_fail
    via2_x = x_fail + TV1_WIDTH + 0.38  # 0.38um gap (violation)

    for vx in [via1_x, via2_x]:
        top_cell.shapes(tv1_idx).insert(box_um(
            vx - TV1_WIDTH/2, y_b - TV1_WIDTH/2,
            vx + TV1_WIDTH/2, y_b + TV1_WIDTH/2))
    # Common M4 covering both vias
    top_cell.shapes(m4_idx).insert(box_um(
        via1_x - TV1_WIDTH/2 - 0.2, y_b - TV1_WIDTH/2 - 0.2,
        via2_x + TV1_WIDTH/2 + 0.2, y_b + TV1_WIDTH/2 + 0.2))
    # Common TM1 covering both vias
    top_cell.shapes(tm1_idx).insert(box_um(
        via1_x - TV1_WIDTH/2 - 0.6, y_b - TV1_WIDTH/2 - 0.6,
        via2_x + TV1_WIDTH/2 + 0.6, y_b + TV1_WIDTH/2 + 0.6))

    # --- TV1.c test: M4 enclosure violation ---
    # Via with M4 enclosure < 0.10um on one side
    y_c = y_offset - 8
    top_cell.shapes(tv1_idx).insert(box_um(
        x_fail - TV1_WIDTH/2, y_c - TV1_WIDTH/2,
        x_fail + TV1_WIDTH/2, y_c + TV1_WIDTH/2))
    # M4 with insufficient enclosure on right side (0.06um instead of 0.10um)
    top_cell.shapes(m4_idx).insert(box_um(
        x_fail - TV1_WIDTH/2 - 0.2, y_c - TV1_WIDTH/2 - 0.2,
        x_fail + TV1_WIDTH/2 + 0.06, y_c + TV1_WIDTH/2 + 0.2))  # Only 0.06um on right
    # Adequate TM1
    top_cell.shapes(tm1_idx).insert(box_um(
        x_fail - TV1_WIDTH/2 - 0.6, y_c - TV1_WIDTH/2 - 0.6,
        x_fail + TV1_WIDTH/2 + 0.6, y_c + TV1_WIDTH/2 + 0.6))

    # --- TV1.d test: TM1 enclosure violation ---
    # Via with TM1 enclosure < 0.42um on one side
    y_d = y_offset - 12
    top_cell.shapes(tv1_idx).insert(box_um(
        x_fail - TV1_WIDTH/2, y_d - TV1_WIDTH/2,
        x_fail + TV1_WIDTH/2, y_d + TV1_WIDTH/2))
    # Adequate M4
    top_cell.shapes(m4_idx).insert(box_um(
        x_fail - TV1_WIDTH/2 - 0.2, y_d - TV1_WIDTH/2 - 0.2,
        x_fail + TV1_WIDTH/2 + 0.2, y_d + TV1_WIDTH/2 + 0.2))
    # TM1 with insufficient enclosure on right side (0.3um instead of 0.42um)
    top_cell.shapes(tm1_idx).insert(box_um(
        x_fail - TV1_WIDTH/2 - 0.6, y_d - TV1_WIDTH/2 - 0.6,
        x_fail + TV1_WIDTH/2 + 0.30, y_d + TV1_WIDTH/2 + 0.6))  # Only 0.30um on right

    # Labels
    top_cell.shapes(text_idx).insert(pya.Text("FAIL", pya.Trans(um_to_dbu(x_fail + 2), um_to_dbu(3))))
    top_cell.shapes(text_idx).insert(pya.Text("TV1.a/b/c/d", pya.Trans(um_to_dbu(x_fail), um_to_dbu(6))))
    top_cell.shapes(text_idx).insert(pya.Text("5.21 TopVia1", pya.Trans(um_to_dbu(-5), um_to_dbu(10))))

    return layout


def create_topmetal1_test():
    """Create TopMetal1 test GDS file with TM1.a, TM1.b violations."""
    layout = pya.Layout()
    layout.dbu = 0.001

    top_cell = layout.create_cell("topmetal1")

    tm1_idx = layout.layer(TM1)
    text_idx = layout.layer(TEXT)

    def box_um(x1, y1, x2, y2):
        return pya.Box(um_to_dbu(x1), um_to_dbu(y1), um_to_dbu(x2), um_to_dbu(y2))

    # ===== PASS region =====
    x_pass = -15
    # Good metal: 1.64um wide
    top_cell.shapes(tm1_idx).insert(box_um(
        x_pass - TM1_WIDTH/2, -5,
        x_pass + TM1_WIDTH/2, 5))
    top_cell.shapes(text_idx).insert(pya.Text("PASS", pya.Trans(um_to_dbu(x_pass), um_to_dbu(7))))

    # ===== FAIL region =====
    x_fail = 5

    # --- TM1.a test: Min width violation ---
    # Metal trace 1.5um wide (needs 1.64um)
    narrow_w = TM1_WIDTH - 0.14  # 1.5um
    y_a = 5
    top_cell.shapes(tm1_idx).insert(box_um(
        x_fail - narrow_w/2, y_a - 3,
        x_fail + narrow_w/2, y_a + 3))

    # --- TM1.b test: Min space violation ---
    # Two traces spaced 1.5um apart (needs 1.64um)
    y_b = -5
    trace1_x = x_fail
    trace2_x = x_fail + TM1_WIDTH + 1.5  # 1.5um gap

    top_cell.shapes(tm1_idx).insert(box_um(
        trace1_x - TM1_WIDTH/2, y_b - 3,
        trace1_x + TM1_WIDTH/2, y_b + 3))
    top_cell.shapes(tm1_idx).insert(box_um(
        trace2_x - TM1_WIDTH/2, y_b - 3,
        trace2_x + TM1_WIDTH/2, y_b + 3))

    # Labels
    top_cell.shapes(text_idx).insert(pya.Text("FAIL", pya.Trans(um_to_dbu(x_fail + 2), um_to_dbu(10))))
    top_cell.shapes(text_idx).insert(pya.Text("TM1.a/b", pya.Trans(um_to_dbu(x_fail), um_to_dbu(12))))
    top_cell.shapes(text_idx).insert(pya.Text("5.22 TopMetal1", pya.Trans(um_to_dbu(-5), um_to_dbu(15))))

    return layout


def create_topmetal1filler_test():
    """Create TopMetal1Filler test GDS file with TM1Fil.a1, TM1Fil.c violations."""
    layout = pya.Layout()
    layout.dbu = 0.001

    top_cell = layout.create_cell("topmetal1filler")

    tm1_idx = layout.layer(TM1)
    tm1f_idx = layout.layer(TM1F)
    text_idx = layout.layer(TEXT)

    def box_um(x1, y1, x2, y2):
        return pya.Box(um_to_dbu(x1), um_to_dbu(y1), um_to_dbu(x2), um_to_dbu(y2))

    # ===== PASS region =====
    x_pass = -20
    # Good filler: 5um wide (under 10um max)
    top_cell.shapes(tm1f_idx).insert(box_um(
        x_pass - 2.5, -2.5,
        x_pass + 2.5, 2.5))
    # TM1 metal at adequate distance (3.5um away)
    top_cell.shapes(tm1_idx).insert(box_um(
        x_pass + 2.5 + 3.5, -3,
        x_pass + 2.5 + 3.5 + 2, 3))
    top_cell.shapes(text_idx).insert(pya.Text("PASS", pya.Trans(um_to_dbu(x_pass), um_to_dbu(5))))

    # ===== FAIL region =====
    x_fail = 10

    # --- TM1Fil.a1 test: Max filler width violation ---
    # Filler 10.5um wide (max is 10um)
    y_a = 10
    filler_w = TM1FIL_MAX_W + 0.5  # 10.5um
    top_cell.shapes(tm1f_idx).insert(box_um(
        x_fail - filler_w/2, y_a - 2.5,
        x_fail + filler_w/2, y_a + 2.5))

    # --- TM1Fil.c test: Min space to TM1 violation ---
    # Filler 2.5um from TM1 metal (needs 3um)
    y_c = -5
    filler_edge = x_fail - 5
    metal_edge = filler_edge + 5 + 2.5  # 2.5um gap

    top_cell.shapes(tm1f_idx).insert(box_um(
        filler_edge, y_c - 2.5,
        filler_edge + 5, y_c + 2.5))
    top_cell.shapes(tm1_idx).insert(box_um(
        metal_edge, y_c - 3,
        metal_edge + 3, y_c + 3))

    # Labels
    top_cell.shapes(text_idx).insert(pya.Text("FAIL", pya.Trans(um_to_dbu(x_fail), um_to_dbu(15))))
    top_cell.shapes(text_idx).insert(pya.Text("TM1Fil.a1/c", pya.Trans(um_to_dbu(x_fail), um_to_dbu(17))))
    top_cell.shapes(text_idx).insert(pya.Text("5.23 TopMetal1Filler", pya.Trans(um_to_dbu(-5), um_to_dbu(20))))

    return layout


def main():
    """Create all test GDS files."""
    output_dir = Path(__file__).parent / "testcases" / "unit"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create TopVia1 test
    print("Creating TopVia1 test file...")
    layout = create_topvia1_test()
    output_file = output_dir / "topvia1.gds"
    layout.write(str(output_file))
    print(f"  Written: {output_file}")

    # Create TopMetal1 test
    print("Creating TopMetal1 test file...")
    layout = create_topmetal1_test()
    output_file = output_dir / "topmetal1.gds"
    layout.write(str(output_file))
    print(f"  Written: {output_file}")

    # Create TopMetal1Filler test
    print("Creating TopMetal1Filler test file...")
    layout = create_topmetal1filler_test()
    output_file = output_dir / "topmetal1filler.gds"
    layout.write(str(output_file))
    print(f"  Written: {output_file}")

    print("\nDone! Run gen_golden.py to generate golden files.")


if __name__ == "__main__":
    main()
