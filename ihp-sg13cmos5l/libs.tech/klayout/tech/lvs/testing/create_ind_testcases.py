# =========================================================================
# Copyright 2026 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# SPDX-License-Identifier: Apache-2.0
# =========================================================================

"""Generate the SG13CMOS5L inductor LVS testcases.

SG13G2 draws a coil with the winding on TopMetal2 and the underpass
crossings on TopMetal1. SG13CMOS5L has no TopMetal2, so the same coil
sits one level lower: winding on TopMetal1, crossings on Metal4, joined
by TopVia1. That is a pure layer shift, so this script derives the
CMOS5L testcases from the SG13G2 golden layouts instead of redrawing
them. Deriving them also means the expected w/s/d/nr_r values are
exactly the SG13G2 golden ones, which are already known good.

The shift lands inductor3 on the right layers too: its LA/LB ports move
from TopMetal1 to Metal4 and its LC port from TopMetal2 to TopMetal1.

The generated GDS files are checked in, so the regression does not need
a SG13G2 tree at test time. Re-run this script only when the SG13G2
golden layouts change.

Usage:
    python3 create_ind_testcases.py [--g2-dir PATH] [--out-dir PATH]
"""

import argparse
import os
import shutil
import sys

import klayout.db as kdb

# SG13G2 -> SG13CMOS5L layer shift. None means "drop".
#
# The winding moves TopMetal2 -> TopMetal1, the crossings move
# TopMetal1 -> Metal4, and the via between them moves TopVia2 ->
# TopVia1, matching the Metal4/TopVia1/TopMetal1 connection declared in
# sg13cmos5l.lyt. Metal5 has no counterpart at all.
LAYER_MAP = {
    (134, 0): (126, 0),    # TopMetal2.drawing  -> TopMetal1.drawing
    (134, 2): (126, 2),    # TopMetal2.pin      -> TopMetal1.pin
    (134, 23): (126, 23),  # TopMetal2.nofill   -> TopMetal1.nofill
    (133, 0): (125, 0),    # TopVia2            -> TopVia1
    (126, 0): (50, 0),     # TopMetal1.drawing  -> Metal4.drawing
    (126, 2): (50, 2),     # TopMetal1.pin      -> Metal4.pin
    (126, 23): None,       # TopMetal1.nofill: Metal4.nofill is already there
    (67, 23): None,        # Metal5.nofill: no Metal5 in CMOS5L
}

# Layers that must not survive the shift, per section 3.2 of
# SG13CMOS5L_os_layout_rules.pdf. cmos5l_forbidden_check.lvs aborts the
# LVS run if any of them carries a polygon.
FORBIDDEN = [
    (3, 0), (11, 0), (13, 0), (26, 0), (32, 0), (35, 0), (53, 0),
    (55, 0), (58, 0), (139, 0), (36, 0), (129, 0), (66, 0), (67, 0),
    (67, 22), (133, 0), (134, 0), (134, 22), (57, 0), (62, 0), (71, 0),
]

TESTCASES = ["inductor", "inductor3"]

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_G2_DIR = os.path.join(
    HERE, "..", "..", "..", "..", "..", "..",
    "ihp-sg13g2", "libs.tech", "klayout", "tech", "lvs", "testing",
    "testcases", "unit", "ind_devices",
)
DEFAULT_OUT_DIR = os.path.join(HERE, "testcases", "unit", "ind_devices")


def remap(src_path, dst_path):
    """Write a CMOS5L copy of the SG13G2 inductor layout."""
    src = kdb.Layout()
    src.read(src_path)

    dst = kdb.Layout()
    dst.dbu = src.dbu

    cell_of = {}
    for cell in src.each_cell():
        cell_of[cell.cell_index()] = dst.create_cell(cell.name)

    for cell in src.each_cell():
        dst_cell = cell_of[cell.cell_index()]
        for inst in cell.each_inst():
            trans = inst.cell_inst.dup()
            trans.cell_index = cell_of[inst.cell_index].cell_index()
            dst_cell.insert(trans)
        for layer_index in src.layer_indexes():
            info = src.get_info(layer_index)
            key = (info.layer, info.datatype)
            if key in LAYER_MAP:
                target = LAYER_MAP[key]
                if target is None:
                    continue
            else:
                target = key
            dst_layer = dst.layer(target[0], target[1])
            dst_cell.shapes(dst_layer).insert(cell.shapes(layer_index))

    dst.write(dst_path)
    return dst


def add_crossing_metal_bridge(layout):
    """Put a Metal3 shape under both terminals of one inductor.

    The IND:pin layer is connected to the crossing metals over the whole
    design, so crossing metal that happens to run under both pins of a
    coil will bond them unless that metal is clipped by IND first. The
    coil then extracts with its two terminals on one net, which reads as
    a short that is not in the layout: there is no via from Metal3 up to
    the TopMetal1 winding.

    SG13G2 never hits this, because both metals it uses for inductors
    already carry the IND exclusion. Metal3 and Metal4 do not, since on
    that stack they are ordinary routing.

    One shape is enough to cover it, so this adds it to the first coil
    that has exactly two pins. It creates no device, so the golden
    netlist is unaffected as long as the clip is in place.
    """
    top = layout.top_cell()
    ind = kdb.Region(top.begin_shapes_rec(layout.layer(27, 0)))
    pins = kdb.Region(top.begin_shapes_rec(layout.layer(27, 2)))

    for marker in ind.each():
        sel = kdb.Region(marker)
        found = list((pins & sel).each())
        if len(found) != 2:
            continue
        span = found[0].bbox() + found[1].bbox()
        bridge = kdb.Box(span.left, span.bottom, span.right,
                         span.bottom + 1000)
        top.shapes(layout.layer(30, 0)).insert(bridge)
        print("Metal3 bridge across both pins of one coil: {}".format(bridge))
        return True

    print("No coil with exactly two pins, no bridge added.")
    return False


def check(layout):
    """Fail loudly if the result cannot extract in CMOS5L.

    Two invariants matter. No forbidden layer may survive, or
    cmos5l_forbidden_check.lvs aborts the run. And every IND marker must
    hold at least one winding polygon, because nr_r is the count of
    winding arcs the crossings cut the coil into.
    """
    errors = []

    for layer, datatype in FORBIDDEN:
        layer_index = layout.find_layer(layer, datatype)
        if layer_index is None:
            continue
        count = sum(
            1
            for cell in layout.each_cell()
            for _ in cell.shapes(layer_index).each()
        )
        if count:
            errors.append(
                "forbidden layer {}/{} still has {} shapes".format(
                    layer, datatype, count
                )
            )

    top = layout.top_cell()
    ind = kdb.Region(top.begin_shapes_rec(layout.layer(27, 0)))
    wind = kdb.Region(top.begin_shapes_rec(layout.layer(126, 0)))
    cross = kdb.Region(top.begin_shapes_rec(layout.layer(50, 0)))
    if ind.is_empty():
        errors.append("no IND (27/0) markers found")

    turns = []
    for marker in ind.each():
        sel = kdb.Region(marker)
        n_wind = (wind & sel).merged().count()
        n_cross = (cross & sel).merged().count()
        turns.append((n_wind, n_cross))
        if n_wind < 1:
            errors.append("an IND marker holds no TopMetal1 winding")

    print("IND markers: {}".format(len(turns)))
    print("expected nr_r (winding arcs) -> marker count:")
    for value in sorted(set(n for n, _ in turns)):
        print("  nr_r={}: {}".format(
            value, sum(1 for n, _ in turns if n == value)
        ))
    print("markers with a Metal4 crossunder: {}".format(
        sum(1 for _, c in turns if c > 0)
    ))

    if errors:
        for message in errors:
            print("ERROR: {}".format(message), file=sys.stderr)
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--g2-dir", default=DEFAULT_G2_DIR)
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    g2_dir = os.path.normpath(args.g2_dir)
    out_dir = os.path.normpath(args.out_dir)
    if not os.path.isdir(g2_dir):
        print(
            "SG13G2 golden testcases not found: {}\n"
            "Pass --g2-dir, or place an ihp-sg13g2 checkout next to this "
            "one.".format(g2_dir),
            file=sys.stderr,
        )
        return 1

    os.makedirs(os.path.join(out_dir, "layout"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "netlist"), exist_ok=True)

    ok = True
    for name in TESTCASES:
        src = os.path.join(g2_dir, "layout", "{}.gds".format(name))
        dst = os.path.join(out_dir, "layout", "{}.gds".format(name))
        print("\n=== {} ===".format(name))
        print("{} -> {}".format(src, dst))
        layout = remap(src, dst)
        if name == "inductor":
            add_crossing_metal_bridge(layout)
            layout.write(dst)
        ok = check(layout) and ok

        # The layer shift does not move any edge, so the golden netlist
        # carries over unchanged.
        src_cdl = os.path.join(g2_dir, "netlist", "{}.cdl".format(name))
        dst_cdl = os.path.join(out_dir, "netlist", "{}.cdl".format(name))
        shutil.copyfile(src_cdl, dst_cdl)
        print("{} -> {}".format(src_cdl, dst_cdl))

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
