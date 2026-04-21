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

"""Enhance existing testcase GDS files with additional violation geometry.

Adds geometry for rules that are currently 'Rule Not Tested' because the
existing testcases lack the necessary layer structures.

Tables: nbulay (NBLB.a-d), psd (nSDB.a/b/c/e),
        nwell (NW.c1/d1/e1.dig), npnsubstratetie (npn13G2*.a)

Usage:
    python enhance_existing_testcases.py [--testcase-dir PATH]
"""

import argparse
from pathlib import Path

import klayout.db as db

DBU = 0.001

# Layer definitions
L_ACTIV = (1, 0)
L_GATPOLY = (5, 0)
L_CONT = (6, 0)
L_NSD = (7, 0)
L_NSD_BLOCK = (7, 21)
L_PSD = (14, 0)
L_DIGIBND = (16, 0)
L_TRANS = (26, 0)
L_SALBLOCK = (28, 0)
L_NWELL = (31, 0)
L_NBULAY = (32, 0)
L_NBULAY_BLOCK = (32, 21)
L_EMWIND = (33, 0)
L_THICKGATEOX = (44, 0)
L_TEXT = (63, 0)


def um(val):
    """Convert micrometers to database units (nm)."""
    return int(round(val * 1000))


def box(layout, cell, layer, x1, y1, x2, y2):
    """Insert a rectangle in dbu coordinates."""
    li = layout.layer(*layer)
    cell.shapes(li).insert(db.Box(x1, y1, x2, y2))


def add_text(layout, cell, layer, x, y, text):
    """Insert a text label at position (x, y) in dbu."""
    li = layout.layer(*layer)
    t = db.Text(text, db.Trans(db.Point(x, y)))
    cell.shapes(li).insert(t)


def enhance_nbulay(testcase_dir: Path):
    """Add nBuLay:block (32/21) geometry for NBLB.a-d rules.

    Place new structures far from existing geometry to avoid interference.
    """
    path = testcase_dir / "nbulay.gds"
    layout = db.Layout()
    layout.read(str(path))

    top = layout.top_cell()
    # Place new structures at y = -50 um to avoid existing geometry
    y_base = -um(50)

    # NBLB.a: Min. nBuLay:block width = 1.50 um. Draw 1.00 um wide.
    x = um(0)
    box(layout, top, L_NBULAY_BLOCK, x, y_base, x + um(1.00), y_base + um(5.0))
    # Also need nbulay_drw enclosing the block for context
    box(layout, top, L_NBULAY, x - um(2.0), y_base - um(2.0),
        x + um(1.00) + um(2.0), y_base + um(5.0) + um(2.0))

    # NBLB.b: Min. nBuLay:block space = 1.00 um. Draw two blocks 0.60 um apart.
    x = um(15)
    box(layout, top, L_NBULAY_BLOCK, x, y_base, x + um(2.0), y_base + um(5.0))
    box(layout, top, L_NBULAY_BLOCK, x + um(2.0) + um(0.60), y_base,
        x + um(4.0) + um(0.60), y_base + um(5.0))
    box(layout, top, L_NBULAY, x - um(2.0), y_base - um(2.0),
        x + um(4.0) + um(0.60) + um(2.0), y_base + um(5.0) + um(2.0))

    # NBLB.c: Min. nBuLay enclosure of nBuLay:block = 1.00 um.
    # nbulay_block inside nbulay_drw with only 0.50 um enclosure.
    x = um(35)
    blk_w, blk_h = um(3.0), um(3.0)
    enc = um(0.50)  # < 1.00 um required
    box(layout, top, L_NBULAY_BLOCK, x, y_base, x + blk_w, y_base + blk_h)
    box(layout, top, L_NBULAY, x - enc, y_base - enc,
        x + blk_w + enc, y_base + blk_h + enc)

    # NBLB.d: Min. nBuLay:block space to unrelated nBuLay = 1.50 um.
    # Standalone nbulay_block (no enclosing nbulay_drw), with a separate
    # nbulay_drw island 1.00 um away.
    x = um(50)
    y_d = y_base - um(15)
    box(layout, top, L_NBULAY_BLOCK, x, y_d, x + um(2.0), y_d + um(5.0))
    # nbulay_drw island 1.00 um to the right (< 1.50 um)
    box(layout, top, L_NBULAY, x + um(2.0) + um(1.0), y_d,
        x + um(2.0) + um(1.0) + um(3.0), y_d + um(5.0))

    layout.write(str(path))
    print(f"Enhanced {path} with NBLB test geometry")


def enhance_psd(testcase_dir: Path):
    """Add nSD:block (7/21) geometry for nSDB.a/b/c/e rules."""
    path = testcase_dir / "psd.gds"
    layout = db.Layout()
    layout.read(str(path))

    top = layout.top_cell()
    # Place new structures at y = -50 um
    y_base = -um(50)

    # nSDB.a: Min. nSD:block width = 0.31 um. Draw 0.20 um wide.
    x = um(0)
    box(layout, top, L_NSD_BLOCK, x, y_base, x + um(0.20), y_base + um(3.0))

    # nSDB.b: Min. nSD:block space = 0.31 um. Draw two blocks 0.20 um apart.
    x = um(5)
    box(layout, top, L_NSD_BLOCK, x, y_base, x + um(1.0), y_base + um(3.0))
    box(layout, top, L_NSD_BLOCK, x + um(1.0) + um(0.20), y_base,
        x + um(2.0) + um(0.20), y_base + um(3.0))

    # nSDB.c: Min. nSD:block space to pSD = 0.31 um.
    # nSD:block and pSD 0.20 um apart (not interacting).
    x = um(12)
    box(layout, top, L_NSD_BLOCK, x, y_base, x + um(1.0), y_base + um(3.0))
    box(layout, top, L_PSD, x + um(1.0) + um(0.20), y_base,
        x + um(2.0) + um(0.20), y_base + um(3.0))

    # nSDB.e: nSD:block and Cont must NOT overlap.
    # Place Cont overlapping nSD:block to trigger violation.
    x = um(19)
    box(layout, top, L_NSD_BLOCK, x, y_base, x + um(2.0), y_base + um(2.0))
    # Cont inside the nSD_block
    box(layout, top, L_CONT, x + um(0.5), y_base + um(0.5),
        x + um(0.5) + um(0.16), y_base + um(0.5) + um(0.16))

    layout.write(str(path))
    print(f"Enhanced {path} with nSDB test geometry")


def enhance_nwell(testcase_dir: Path):
    """Add DigiBnd (16/0) geometry for NW.c1.dig, NW.d1.dig, NW.e1.dig rules.

    The .dig rules check NWell enclosure/spacing within DigiBnd regions
    for HV (ThickGateOx) transistors with relaxed thresholds.
    """
    path = testcase_dir / "nwell.gds"
    layout = db.Layout()
    layout.read(str(path))

    top = layout.top_cell()
    y_base = -um(80)

    # DigiBnd boundary region
    digibnd_x0, digibnd_y0 = um(0), y_base
    digibnd_w, digibnd_h = um(50), um(30)
    box(layout, top, L_DIGIBND, digibnd_x0, digibnd_y0,
        digibnd_x0 + digibnd_w, digibnd_y0 + digibnd_h)

    # NW.c1.dig: Min. NWell enclosure of P+Activ (HV, in DigiBnd) = 0.31 um
    # P+Activ = Activ AND pSD (no nSD), inside ThickGateOx
    # NWell enclosure of P+Activ < 0.31 um
    x = um(2)
    y = y_base + um(2)
    nw_w, nw_h = um(6.0), um(6.0)
    box(layout, top, L_NWELL, x, y, x + nw_w, y + nw_h)
    box(layout, top, L_THICKGATEOX, x + um(0.5), y + um(0.5),
        x + nw_w - um(0.5), y + nw_h - um(0.5))
    # P+Activ (Activ + pSD, no nSD) with tight NWell enclosure on right
    act_x = x + um(1.0)
    act_w = nw_w - um(1.0) - um(0.20)  # only 0.20 um from NWell right edge
    box(layout, top, L_ACTIV, act_x, y + um(1.0),
        act_x + act_w, y + nw_h - um(1.0))
    box(layout, top, L_PSD, act_x - um(0.5), y + um(0.5),
        act_x + act_w + um(0.5), y + nw_h - um(0.5))

    # NW.d1.dig: Min. NWell space to N+Activ (HV, in DigiBnd) = 0.31 um
    # N+Activ = Activ NOT pSD, inside ThickGateOx
    # NWell separation from N+Activ < 0.31 um
    x = um(15)
    y = y_base + um(2)
    box(layout, top, L_NWELL, x, y, x + um(4.0), y + um(6.0))
    box(layout, top, L_THICKGATEOX, x - um(1.0), y - um(1.0),
        x + um(8.0), y + um(8.0))
    # N+Activ (Activ without pSD) placed 0.20 um from NWell right edge
    nact_x = x + um(4.0) + um(0.20)
    box(layout, top, L_ACTIV, nact_x, y + um(1.0),
        nact_x + um(2.0), y + um(5.0))

    # NW.e1.dig: Min. NWell enclosure of N+Activ NWell tie (HV, in DigiBnd) = 0.24 um
    # NWell tie: N+Activ inside NWell and ThickGateOx
    x = um(30)
    y = y_base + um(2)
    nw_w2 = um(6.0)
    nw_h2 = um(6.0)
    box(layout, top, L_NWELL, x, y, x + nw_w2, y + nw_h2)
    box(layout, top, L_THICKGATEOX, x + um(0.3), y + um(0.3),
        x + nw_w2 - um(0.3), y + nw_h2 - um(0.3))
    # N+Activ inside NWell (NWell tie) with tight enclosure on right (0.15 um < 0.24 um)
    tie_x = x + um(1.0)
    tie_w = nw_w2 - um(1.0) - um(0.15)  # only 0.15 um from NWell right
    box(layout, top, L_ACTIV, tie_x, y + um(1.0),
        tie_x + tie_w, y + nw_h2 - um(1.0))

    # NW.c1 (analog): P+Activ HV OUTSIDE DigiBnd, NWell enclosure < 0.62 um
    # This is the base rule. pact_hv_ana = P+Activ inside ThickGateOx NOT
    # inside DigiBnd. Place these structures far from the DigiBnd region.
    x = um(0)
    y = y_base - um(20)  # well below DigiBnd region
    nw_w3, nw_h3 = um(6.0), um(6.0)
    box(layout, top, L_NWELL, x, y, x + nw_w3, y + nw_h3)
    box(layout, top, L_THICKGATEOX, x + um(0.3), y + um(0.3),
        x + nw_w3 - um(0.3), y + nw_h3 - um(0.3))
    # P+Activ with tight NWell enclosure (0.30 um < 0.62 um threshold)
    box(layout, top, L_ACTIV, x + um(1.0), y + um(1.0),
        x + nw_w3 - um(0.30), y + nw_h3 - um(1.0))
    box(layout, top, L_PSD, x + um(0.5), y + um(0.5),
        x + nw_w3 - um(0.1), y + nw_h3 - um(0.5))

    layout.write(str(path))
    print(f"Enhanced {path} with NW.*.dig and NW.c1 test geometry")


def enhance_npnsubstratetie(testcase_dir: Path):
    """Add emitter geometry for npn13G2.a, npn13G2L.a, npn13G2V.a rules.

    These rules check emitter edge lengths via ext_with_length with exclusive bounds.
    The existing GDS has HBT structures but may lack emitters in the violation range.

    Device recognition requires:
    - npn13G2:  TRANS AND ptap.holes, interacting "npn13G2" text,
                covering EmWind AND Activ AND nSD_block
    - npn13G2L: TRANS AND ptap.holes, interacting "npn13G2L" text,
                covering EmWind AND Activ
    - npn13G2V: TRANS AND ptap.holes, interacting "npn13G2V" text,
                covering EmWiHV AND Activ
    """
    path = testcase_dir / "npnsubstratetie.gds"
    layout = db.Layout()
    layout.read(str(path))

    top = layout.top_cell()
    y_base = -um(100)

    # npn13G2.a: emitter with length in (0.07, 0.9) um range
    # Create a minimal npn13G2 device structure
    x = um(0)
    y = y_base
    trans_w, trans_h = um(10), um(10)

    # TRANS region
    box(layout, top, L_TRANS, x, y, x + trans_w, y + trans_h)
    # Text label for device recognition
    add_text(layout, top, L_TEXT, x + um(1), y + um(1), "npn13G2")
    # Activ inside (for ptap.holes)
    box(layout, top, L_ACTIV, x + um(2), y + um(2), x + um(8), y + um(8))
    # nSD_block covering the emitter area
    box(layout, top, L_NSD_BLOCK, x + um(3), y + um(3), x + um(7), y + um(7))
    # EmitterWindow with edge length 0.50 um (in violation range 0.07-0.9)
    box(layout, top, L_EMWIND, x + um(4), y + um(4),
        x + um(4) + um(0.50), y + um(4) + um(0.50))

    # npn13G2L.a: emitter with length in (0.07, 1.0) um range
    x = um(20)
    box(layout, top, L_TRANS, x, y, x + trans_w, y + trans_h)
    add_text(layout, top, L_TEXT, x + um(1), y + um(1), "npn13G2L")
    box(layout, top, L_ACTIV, x + um(2), y + um(2), x + um(8), y + um(8))
    box(layout, top, L_EMWIND, x + um(4), y + um(4),
        x + um(4) + um(0.50), y + um(4) + um(0.50))

    # npn13G2V.a: emitter with length in (0.12, 1.0) um range
    # npn13G2V uses emwihv_drw — need to check layer number
    x = um(40)
    box(layout, top, L_TRANS, x, y, x + trans_w, y + trans_h)
    add_text(layout, top, L_TEXT, x + um(1), y + um(1), "npn13G2V")
    box(layout, top, L_ACTIV, x + um(2), y + um(2), x + um(8), y + um(8))
    # emwihv_drw = layer 156/0 (from layers_def.drc)
    L_EMWIHV = (156, 0)
    box(layout, top, L_EMWIHV, x + um(4), y + um(4),
        x + um(4) + um(0.50), y + um(4) + um(0.50))

    layout.write(str(path))
    print(f"Enhanced {path} with npn13G2 emitter test geometry")


def main():
    parser = argparse.ArgumentParser(description="Enhance existing DRC testcase GDS files")
    parser.add_argument(
        "--testcase-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "unit",
        help="Directory containing testcase GDS files",
    )
    args = parser.parse_args()

    enhance_nbulay(args.testcase_dir)
    enhance_psd(args.testcase_dir)
    enhance_nwell(args.testcase_dir)
    enhance_npnsubstratetie(args.testcase_dir)

    print(f"\nAll existing testcases enhanced in {args.testcase_dir}")


if __name__ == "__main__":
    main()
