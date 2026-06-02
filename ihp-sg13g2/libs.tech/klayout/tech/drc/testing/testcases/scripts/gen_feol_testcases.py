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

"""Generate testcase GDS files for 6 FEOL DRC tables.

Each GDS contains minimal geometry that triggers the DRC rules as violations,
enabling golden-based regression testing.

Tables: extblock, salblock, nmosi, rhigh, rsil, rppd

Usage:
    python gen_feol_testcases.py [--output-dir PATH]
"""

import argparse
from pathlib import Path

import klayout.db as db

# Database unit: 1 nm
DBU = 0.001

# Layer definitions (layer_number, datatype)
L_ACTIV = (1, 0)
L_GATPOLY = (5, 0)
L_CONT = (6, 0)
L_NSD = (7, 0)
L_NSD_BLOCK = (7, 21)
L_PSD = (14, 0)
L_RES = (24, 0)
L_SALBLOCK = (28, 0)
L_NWELL = (31, 0)
L_NBULAY = (32, 0)
L_THICKGATEOX = (44, 0)
L_PWELL_BLOCK = (46, 21)
L_EXTBLOCK = (111, 0)
L_POLYRES = (128, 0)


def um(val):
    """Convert micrometers to database units (nm)."""
    return int(round(val * 1000))


def box(layout, cell, layer, x1, y1, x2, y2):
    """Insert a rectangle in dbu coordinates."""
    li = layout.layer(*layer)
    cell.shapes(li).insert(db.Box(x1, y1, x2, y2))


def gen_extblock(output_dir: Path):
    """EXTB.a-c: EXTBlock width, space, space-to-pSD rules."""
    layout = db.Layout()
    layout.dbu = DBU
    top = layout.create_cell("extblock")

    # EXTB.a: Min. EXTBlock width = 0.31 um. Draw 0.20 um wide rect.
    x = 0
    box(layout, top, L_EXTBLOCK, x, 0, x + um(0.20), um(2.0))

    # EXTB.b: Min. EXTBlock space = 0.31 um. Draw two rects 0.20 um apart.
    x = um(5)
    box(layout, top, L_EXTBLOCK, x, 0, x + um(1.0), um(2.0))
    box(layout, top, L_EXTBLOCK, x + um(1.0) + um(0.20), 0,
        x + um(2.0) + um(0.20), um(2.0))

    # EXTB.c: Min. EXTBlock space to pSD = 0.31 um. Draw 0.20 um apart.
    x = um(12)
    box(layout, top, L_EXTBLOCK, x, 0, x + um(1.0), um(2.0))
    box(layout, top, L_PSD, x + um(1.0) + um(0.20), 0,
        x + um(2.0) + um(0.20), um(2.0))

    path = output_dir / "extblock.gds"
    layout.write(str(path))
    print(f"Generated {path}")


def gen_salblock(output_dir: Path):
    """Sal.a-e: SalBlock width, space, enclosure, space-to-Activ/GatPoly/Cont."""
    layout = db.Layout()
    layout.dbu = DBU
    top = layout.create_cell("salblock")

    # Sal.a: Min. SalBlock width = 0.42 um. Draw 0.30 um wide.
    x = 0
    box(layout, top, L_SALBLOCK, x, 0, x + um(0.30), um(2.0))

    # Sal.b: Min. SalBlock space = 0.42 um. Draw two rects 0.30 um apart.
    x = um(5)
    box(layout, top, L_SALBLOCK, x, 0, x + um(1.0), um(2.0))
    box(layout, top, L_SALBLOCK, x + um(1.0) + um(0.30), 0,
        x + um(2.0) + um(0.30), um(2.0))

    # Sal.c: Min. SalBlock extension over Activ/GatPoly = 0.20 um.
    # ext_enclosed checks: GatPoly INSIDE SalBlock with insufficient margin.
    # GatPoly inside SalBlock but only 0.10 um from SalBlock right edge (< 0.20 um).
    x = um(12)
    box(layout, top, L_SALBLOCK, x, 0, x + um(2.0), um(2.0))
    box(layout, top, L_GATPOLY, x + um(0.5), um(0.3),
        x + um(2.0) - um(0.10), um(1.7))

    # Sal.d: Min. SalBlock space to unrelated Activ/GatPoly = 0.20 um.
    # Unrelated GatPoly 0.10 um from SalBlock edge.
    x = um(19)
    box(layout, top, L_SALBLOCK, x, 0, x + um(1.0), um(2.0))
    box(layout, top, L_GATPOLY, x + um(1.0) + um(0.10), 0,
        x + um(2.0) + um(0.10), um(2.0))

    # Sal.e: Min. SalBlock space to Cont = 0.20 um. Draw Cont 0.10 um away.
    x = um(26)
    box(layout, top, L_SALBLOCK, x, 0, x + um(1.0), um(2.0))
    box(layout, top, L_CONT, x + um(1.0) + um(0.10), um(0.5),
        x + um(1.0) + um(0.10) + um(0.16), um(0.5) + um(0.16))

    path = output_dir / "salblock.gds"
    layout.write(str(path))
    print(f"Generated {path}")


def gen_nmosi(output_dir: Path):
    """nmosi.b/c/d/f/g: NMOS-Iso rules.

    The key derived layer is iso_pwell_act = Activ AND nBuLay NOT (NWell OR PWell_block).
    We create an Activ+nBuLay region outside NWell to form the isolated p-well active.
    """
    layout = db.Layout()
    layout.dbu = DBU
    top = layout.create_cell("nmosi")

    # Common structure: large nBuLay island with Activ inside (no NWell, no PWell_block)
    # This creates iso_pwell_act at the Activ region

    # ---- nmosi.b: Min. nBuLay enclosure of Iso-PWell-Activ = 1.24 um ----
    # Draw nBuLay with only 1.00 um enclosure of Activ (< 1.24 um)
    x = 0
    enc = um(1.00)  # insufficient enclosure
    act_w, act_h = um(2.0), um(2.0)
    box(layout, top, L_NBULAY, x, 0,
        x + act_w + 2 * enc, act_h + 2 * enc)
    box(layout, top, L_ACTIV, x + enc, enc,
        x + enc + act_w, enc + act_h)

    # ---- nmosi.c: Min. NWell space to Iso-PWell-Activ = 0.39 um ----
    # Uses ext_separation(nwell_drw.with_holes, ..., max_angle: 180).
    # .with_holes selects NWell polygons that HAVE internal holes.
    # Create NWell donut: outer rect with inner hole containing the
    # nBuLay+Activ island.  Hole edge 0.20 um from Activ (< 0.39 um).
    x = um(10)
    enc_ok = um(2.0)
    act_w = um(1.5)
    act_h = um(1.5)
    act_x0 = x + enc_ok
    act_y0 = enc_ok
    box(layout, top, L_NBULAY, x, 0,
        x + act_w + 2 * enc_ok, act_h + 2 * enc_ok)
    box(layout, top, L_ACTIV, act_x0, act_y0,
        act_x0 + act_w, act_y0 + act_h)
    # NWell donut: outer covering the whole area, hole around the island
    # Hole edges 0.20 um from Activ edges
    nw_li = layout.layer(*L_NWELL)
    hole_margin = um(0.20)  # < 0.39 um minimum
    outer = db.DBox(
        (x - um(3.0)) * DBU, -um(3.0) * DBU,
        (x + act_w + 2 * enc_ok + um(3.0)) * DBU,
        (act_h + 2 * enc_ok + um(3.0)) * DBU
    )
    hole = db.DBox(
        (act_x0 - hole_margin) * DBU, (act_y0 - hole_margin) * DBU,
        (act_x0 + act_w + hole_margin) * DBU,
        (act_y0 + act_h + hole_margin) * DBU
    )
    nw_poly = db.DPolygon(outer)
    nw_poly.insert_hole(db.DBox(hole.left, hole.bottom, hole.right, hole.top))
    top.shapes(nw_li).insert(nw_poly)

    # ---- nmosi.d: Min. NWell-nBuLay width = 0.62 um ----
    # Draw NWell AND nBuLay overlap with width 0.40 um (< 0.62 um)
    x = um(22)
    # NWell ring around iso region: place nBuLay+NWell overlap narrowly
    box(layout, top, L_NBULAY, x, 0, x + um(0.40), um(3.0))
    box(layout, top, L_NWELL, x, 0, x + um(0.40), um(3.0))

    # ---- nmosi.f: Min. nSD:block width = 0.62 um ----
    # Draw narrow nSD_block inside iso_pwell_act
    x = um(28)
    enc_ok2 = um(2.0)
    box(layout, top, L_NBULAY, x, 0,
        x + um(2.0) + 2 * enc_ok2, um(2.0) + 2 * enc_ok2)
    box(layout, top, L_ACTIV, x + enc_ok2, enc_ok2,
        x + enc_ok2 + um(2.0), enc_ok2 + um(2.0))
    # Narrow nSD_block inside the Activ area
    box(layout, top, L_NSD_BLOCK, x + enc_ok2 + um(0.5), enc_ok2 + um(0.5),
        x + enc_ok2 + um(0.5) + um(0.40), enc_ok2 + um(1.5))

    # ---- nmosi.g: Min. SalBlock overlap of nSD:block over Activ = 0.15 um ----
    # ext_enclosed checks nSD_block INSIDE SalBlock with insufficient margin.
    # SalBlock encloses nSD_block but with only 0.08 um margin on right (< 0.15 um).
    x = um(38)
    enc_ok3 = um(2.0)
    box(layout, top, L_NBULAY, x, 0,
        x + um(3.0) + 2 * enc_ok3, um(3.0) + 2 * enc_ok3)
    box(layout, top, L_ACTIV, x + enc_ok3, enc_ok3,
        x + enc_ok3 + um(3.0), enc_ok3 + um(3.0))
    # nSD_block in center of Activ
    nsdb_x = x + enc_ok3 + um(0.5)
    nsdb_w = um(1.0)
    nsdb_y0 = enc_ok3 + um(0.5)
    nsdb_y1 = enc_ok3 + um(2.5)
    box(layout, top, L_NSD_BLOCK, nsdb_x, nsdb_y0,
        nsdb_x + nsdb_w, nsdb_y1)
    # SalBlock enclosing nSD_block with sufficient margin on 3 sides but
    # only 0.08 um on the right side
    box(layout, top, L_SALBLOCK, nsdb_x - um(0.5), nsdb_y0 - um(0.5),
        nsdb_x + nsdb_w + um(0.08), nsdb_y1 + um(0.5))

    path = output_dir / "nmosi.gds"
    layout.write(str(path))
    print(f"Generated {path}")


def gen_rhigh(output_dir: Path):
    """Rhi.a-f: High-R poly resistor rules.

    Rhigh recognition: GatPoly/PolyRes AND (pSD AND nSD-derived) AND SalBlock
    (no nSD_block, no Recog_esd).
    """
    layout = db.Layout()
    layout.dbu = DBU
    top = layout.create_cell("rhigh")

    # Build a rhigh resistor structure with specific violations.
    # Base structure: long GatPoly strip overlapped by pSD, nSD, SalBlock, EXTBlock
    # For each rule, we create a separate region with a violation.

    # ---- Rhi.a: Min. GatPoly width = 0.50 um ----
    # Narrow GatPoly strip forming rhigh (width = 0.35 um < 0.50 um)
    x = 0
    gp_w = um(0.35)
    gp_h = um(3.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w, gp_h)
    # pSD and nSD cover the entire GatPoly area
    box(layout, top, L_PSD, x - um(0.5), -um(0.5), x + gp_w + um(0.5), gp_h + um(0.5))
    box(layout, top, L_NSD, x - um(0.5), -um(0.5), x + gp_w + um(0.5), gp_h + um(0.5))
    # SalBlock covering the middle (no nSD_block or Recog_esd)
    box(layout, top, L_SALBLOCK, x - um(0.3), um(0.5), x + gp_w + um(0.3), gp_h - um(0.5))
    # EXTBlock enclosing the whole structure
    box(layout, top, L_EXTBLOCK, x - um(1.0), -um(1.0), x + gp_w + um(1.0), gp_h + um(1.0))

    # ---- Rhi.b: pSD and nSD identity check ----
    # rhigh_recog = EXTBlock AND pSD AND nSD covering GatPoly.
    # psd_nsd_mismatch = (nSD\pSD) union (pSD\nSD).
    # The mismatch can't intersect rhigh_recog (requires both pSD AND nSD).
    # This rule may be untriggerable — add it to RULES_EXCLUDE if confirmed.
    # For now, create a valid rhigh structure where pSD/nSD match exactly (0 violations).
    x = um(8)
    gp_w2 = um(1.0)
    gp_h2 = um(3.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w2, gp_h2)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5), x + gp_w2 + um(0.5), gp_h2 + um(0.5))
    box(layout, top, L_NSD, x - um(0.5), -um(0.5), x + gp_w2 + um(0.5), gp_h2 + um(0.5))
    box(layout, top, L_SALBLOCK, x - um(0.3), um(0.5), x + gp_w2 + um(0.3), gp_h2 - um(0.5))
    box(layout, top, L_EXTBLOCK, x - um(1.0), -um(1.0), x + gp_w2 + um(1.0), gp_h2 + um(1.0))

    # ---- Rhi.c: Min. pSD/nSD enclosure of GatPoly = 0.18 um ----
    # ext_enclosed: GatPoly must be INSIDE pSD AND nSD with < 0.18 um margin.
    # pSD/nSD enclose GatPoly but with only 0.10 um margin on the right side.
    x = um(16)
    gp_w3 = um(1.0)
    gp_h3 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w3, gp_h3)
    # pSD/nSD: sufficient enclosure everywhere except right side (only 0.10 um)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5),
        x + gp_w3 + um(0.10), gp_h3 + um(0.5))
    box(layout, top, L_NSD, x - um(0.5), -um(0.5),
        x + gp_w3 + um(0.10), gp_h3 + um(0.5))
    box(layout, top, L_SALBLOCK, x - um(0.3), um(0.5),
        x + gp_w3 + um(0.3), gp_h3 - um(0.5))
    box(layout, top, L_EXTBLOCK, x - um(1.5), -um(1.5),
        x + gp_w3 + um(1.5), gp_h3 + um(1.5))

    # ---- Rhi.d: Min. SalBlock space to Cont = 0.20 um ----
    # Cont placed within EXTBlock, 0.10 um from SalBlock
    x = um(24)
    gp_w4 = um(1.0)
    gp_h4 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w4, gp_h4)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5),
        x + gp_w4 + um(0.5), gp_h4 + um(0.5))
    box(layout, top, L_NSD, x - um(0.5), -um(0.5),
        x + gp_w4 + um(0.5), gp_h4 + um(0.5))
    sal_top = gp_h4 - um(1.0)
    box(layout, top, L_SALBLOCK, x - um(0.3), um(1.0),
        x + gp_w4 + um(0.3), sal_top)
    box(layout, top, L_EXTBLOCK, x - um(1.5), -um(1.5),
        x + gp_w4 + um(1.5), gp_h4 + um(1.5))
    # Cont just above SalBlock, only 0.10 um away
    box(layout, top, L_CONT, x + um(0.3), sal_top + um(0.10),
        x + um(0.3) + um(0.16), sal_top + um(0.10) + um(0.16))

    # ---- Rhi.e: Min. EXTBlock enclosure of GatPoly = 0.18 um ----
    # GatPoly extending beyond EXTBlock with only 0.10 um enclosure
    x = um(32)
    gp_w5 = um(1.0)
    gp_h5 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w5, gp_h5)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5),
        x + gp_w5 + um(0.5), gp_h5 + um(0.5))
    box(layout, top, L_NSD, x - um(0.5), -um(0.5),
        x + gp_w5 + um(0.5), gp_h5 + um(0.5))
    box(layout, top, L_SALBLOCK, x - um(0.3), um(0.5),
        x + gp_w5 + um(0.3), gp_h5 - um(0.5))
    # EXTBlock with only 0.10 um enclosure on the right side
    box(layout, top, L_EXTBLOCK, x - um(1.5), -um(1.5),
        x + gp_w5 + um(0.10), gp_h5 + um(1.5))

    # ---- Rhi.f: Min. SalBlock length = 0.50 um ----
    # Short SalBlock within rhigh (0.35 um < 0.50 um)
    x = um(40)
    gp_w6 = um(1.0)
    gp_h6 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w6, gp_h6)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5),
        x + gp_w6 + um(0.5), gp_h6 + um(0.5))
    box(layout, top, L_NSD, x - um(0.5), -um(0.5),
        x + gp_w6 + um(0.5), gp_h6 + um(0.5))
    # Short SalBlock: only 0.35 um wide (Sal.f checks width = length in context)
    box(layout, top, L_SALBLOCK, x + um(0.1), um(1.5),
        x + um(0.1) + um(0.35), um(2.5))
    box(layout, top, L_EXTBLOCK, x - um(1.5), -um(1.5),
        x + gp_w6 + um(1.5), gp_h6 + um(1.5))

    path = output_dir / "rhigh.gds"
    layout.write(str(path))
    print(f"Generated {path}")


def gen_rsil(output_dir: Path):
    """Rsil.a-f: Silicided resistor rules.

    Rsil recognition: GatPoly/PolyRes AND RES AND EXTBlock, NOT interacting SalBlock.
    Also NOT interacting NWell or nBuLay.
    """
    layout = db.Layout()
    layout.dbu = DBU
    top = layout.create_cell("rsil")

    # ---- Rsil.a: Min. GatPoly width = 0.50 um ----
    # Narrow rsil structure (0.35 um < 0.50 um)
    x = 0
    gp_w = um(0.35)
    gp_h = um(3.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w, gp_h)
    box(layout, top, L_RES, x - um(0.3), -um(0.3), x + gp_w + um(0.3), gp_h + um(0.3))
    box(layout, top, L_EXTBLOCK, x - um(0.5), -um(0.5),
        x + gp_w + um(0.5), gp_h + um(0.5))

    # ---- Rsil.b: Min. RES space to Cont = 0.12 um ----
    # Cont placed 0.05 um from RES edge (< 0.12 um)
    x = um(6)
    gp_w2 = um(1.0)
    gp_h2 = um(3.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w2, gp_h2)
    res_right = x + gp_w2 + um(0.3)
    box(layout, top, L_RES, x - um(0.3), -um(0.3), res_right, gp_h2 + um(0.3))
    box(layout, top, L_EXTBLOCK, x - um(0.5), -um(0.5),
        x + gp_w2 + um(1.5), gp_h2 + um(0.5))
    # Cont 0.05 um from RES right edge
    box(layout, top, L_CONT, res_right + um(0.05), um(1.0),
        res_right + um(0.05) + um(0.16), um(1.0) + um(0.16))

    # ---- Rsil.c: Min. RES extension over GatPoly = 0.00 um ----
    # GatPoly extends beyond RES (RES doesn't fully cover GatPoly)
    x = um(14)
    gp_w3 = um(1.0)
    gp_h3 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w3, gp_h3)
    # RES shorter than GatPoly — GatPoly extends beyond RES at top
    box(layout, top, L_RES, x - um(0.3), -um(0.3),
        x + gp_w3 + um(0.3), gp_h3 - um(0.5))
    box(layout, top, L_EXTBLOCK, x - um(0.5), -um(0.5),
        x + gp_w3 + um(0.5), gp_h3 + um(0.5))

    # ---- Rsil.d: Min. pSD space to GatPoly = 0.18 um ----
    # pSD placed 0.10 um from GatPoly edge (< 0.18 um)
    x = um(22)
    gp_w4 = um(1.0)
    gp_h4 = um(3.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w4, gp_h4)
    box(layout, top, L_RES, x - um(0.3), -um(0.3),
        x + gp_w4 + um(0.3), gp_h4 + um(0.3))
    box(layout, top, L_EXTBLOCK, x - um(1.0), -um(1.0),
        x + gp_w4 + um(1.0), gp_h4 + um(1.0))
    # pSD placed nearby (0.10 um from GatPoly right edge)
    box(layout, top, L_PSD, x + gp_w4 + um(0.10), 0,
        x + gp_w4 + um(0.10) + um(1.0), gp_h4)

    # ---- Rsil.e: Min. EXTBlock enclosure of GatPoly = 0.18 um ----
    # EXTBlock with only 0.10 um enclosure
    x = um(30)
    gp_w5 = um(1.0)
    gp_h5 = um(3.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w5, gp_h5)
    box(layout, top, L_RES, x - um(0.3), -um(0.3),
        x + gp_w5 + um(0.3), gp_h5 + um(0.3))
    # EXTBlock with only 0.10 um on right
    box(layout, top, L_EXTBLOCK, x - um(0.5), -um(0.5),
        x + gp_w5 + um(0.10), gp_h5 + um(0.5))

    # ---- Rsil.f: Min. RES length = 0.50 um ----
    # Short RES (0.35 um < 0.50 um)
    x = um(38)
    gp_w6 = um(1.0)
    gp_h6 = um(3.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w6, gp_h6)
    box(layout, top, L_RES, x + um(0.1), um(1.0),
        x + um(0.1) + um(0.35), um(1.0) + um(1.0))
    box(layout, top, L_EXTBLOCK, x - um(0.5), -um(0.5),
        x + gp_w6 + um(0.5), gp_h6 + um(0.5))

    path = output_dir / "rsil.gds"
    layout.write(str(path))
    print(f"Generated {path}")


def gen_rppd(output_dir: Path):
    """Rppd.a-e: P+ poly resistor rules.

    Rppd recognition: GatPoly/PolyRes AND pSD AND SalBlock (no nSD_block, no Recog_esd),
    NOT interacting Activ or nSD-derived.
    """
    layout = db.Layout()
    layout.dbu = DBU
    top = layout.create_cell("rppd")

    # Rppd structure: GatPoly strip + pSD + SalBlock, NO Activ or nSD nearby

    # ---- Rppd.a: Min. GatPoly width = 0.50 um ----
    x = 0
    gp_w = um(0.35)
    gp_h = um(3.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w, gp_h)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5), x + gp_w + um(0.5), gp_h + um(0.5))
    box(layout, top, L_SALBLOCK, x - um(0.3), um(0.5), x + gp_w + um(0.3), gp_h - um(0.5))
    box(layout, top, L_EXTBLOCK, x - um(1.0), -um(1.0), x + gp_w + um(1.0), gp_h + um(1.0))

    # ---- Rppd.b: Min. pSD enclosure of GatPoly = 0.18 um ----
    # ext_enclosed: GatPoly must be INSIDE pSD with < 0.18 um margin.
    # pSD encloses GatPoly with only 0.10 um on the right side.
    x = um(8)
    gp_w2 = um(1.0)
    gp_h2 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w2, gp_h2)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5),
        x + gp_w2 + um(0.10), gp_h2 + um(0.5))
    box(layout, top, L_SALBLOCK, x - um(0.3), um(0.5),
        x + gp_w2 + um(0.3), gp_h2 - um(0.5))
    box(layout, top, L_EXTBLOCK, x - um(1.5), -um(1.5),
        x + gp_w2 + um(1.5), gp_h2 + um(1.5))

    # ---- Rppd.c: Min. SalBlock space to Cont = 0.20 um ----
    x = um(16)
    gp_w3 = um(1.0)
    gp_h3 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w3, gp_h3)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5),
        x + gp_w3 + um(0.5), gp_h3 + um(0.5))
    sal_top = gp_h3 - um(1.0)
    box(layout, top, L_SALBLOCK, x - um(0.3), um(1.0),
        x + gp_w3 + um(0.3), sal_top)
    box(layout, top, L_EXTBLOCK, x - um(1.5), -um(1.5),
        x + gp_w3 + um(1.5), gp_h3 + um(1.5))
    # Cont 0.10 um from SalBlock
    box(layout, top, L_CONT, x + um(0.3), sal_top + um(0.10),
        x + um(0.3) + um(0.16), sal_top + um(0.10) + um(0.16))

    # ---- Rppd.d: Min. EXTBlock enclosure of GatPoly = 0.18 um ----
    x = um(24)
    gp_w4 = um(1.0)
    gp_h4 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w4, gp_h4)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5),
        x + gp_w4 + um(0.5), gp_h4 + um(0.5))
    box(layout, top, L_SALBLOCK, x - um(0.3), um(0.5),
        x + gp_w4 + um(0.3), gp_h4 - um(0.5))
    # EXTBlock tight on right
    box(layout, top, L_EXTBLOCK, x - um(1.5), -um(1.5),
        x + gp_w4 + um(0.10), gp_h4 + um(1.5))

    # ---- Rppd.e: Min. SalBlock length = 0.50 um ----
    x = um(32)
    gp_w5 = um(1.0)
    gp_h5 = um(4.0)
    box(layout, top, L_GATPOLY, x, 0, x + gp_w5, gp_h5)
    box(layout, top, L_PSD, x - um(0.5), -um(0.5),
        x + gp_w5 + um(0.5), gp_h5 + um(0.5))
    # Short SalBlock (0.35 um)
    box(layout, top, L_SALBLOCK, x + um(0.1), um(1.5),
        x + um(0.1) + um(0.35), um(2.5))
    box(layout, top, L_EXTBLOCK, x - um(1.5), -um(1.5),
        x + gp_w5 + um(1.5), gp_h5 + um(1.5))

    path = output_dir / "rppd.gds"
    layout.write(str(path))
    print(f"Generated {path}")


def main():
    parser = argparse.ArgumentParser(description="Generate FEOL DRC testcase GDS files")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "unit",
        help="Output directory for GDS files",
    )
    args = parser.parse_args()

    gen_extblock(args.output_dir)
    gen_salblock(args.output_dir)
    gen_nmosi(args.output_dir)
    gen_rhigh(args.output_dir)
    gen_rsil(args.output_dir)
    gen_rppd(args.output_dir)

    print(f"\nAll 6 FEOL testcase GDS files generated in {args.output_dir}")


if __name__ == "__main__":
    main()
