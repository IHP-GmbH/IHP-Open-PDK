########################################################################
#
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
#
########################################################################
#
# Generator for the cap_cmomi LVS testcase layouts added alongside the original
# cap_cmomi testcase (which predates this script and is not regenerated here).
#
# Each layout listed below is built from the SG13_dev PCell by
# this script rather than drawn by hand, so the layouts can be regenerated when
# the PCell changes. The generated files are checked in, so the regression does
# not need a working PCell library at test time.
#
# Regeneration is content-stable but not byte-stable: GDS carries modification
# and access timestamps in its BGNLIB and BGNSTR records, so re-running this
# script rewrites those timestamp bytes and git reports every layout as modified
# even when the geometry is unchanged. Only commit regenerated files when the
# geometry actually changed; a quick way to tell is an XOR of the old and new
# layouts on every layer.
#
# Produces two families:
#
#   testcases/unit/cap_devices/layout/
#       cap_cmomi_config.gds   configuration matrix, every instance must extract
#       cap_cmomi_hier.gds     hierarchical instantiation, no double extraction
#
#   testcases/manual_tests/cap_cmomi_checks/
#       cmomi_chain.gds        3 caps in series, asymmetric, the golden layout
#       cmomi_short_same.gds   'same' feed with the two stacked plates shorted
#       cmomi_merged.gds       two caps under one merged Recog.mom marker
#       cmomi_all_dropped.gds  a cell whose every device is dropped
#       cmomi_feed_none.gds    'none' feed, an array with no feed structure
#
# The malformed layouts carry a well formed cap alongside the broken one, so that
# each one exercises a comparison rather than an empty cell. cmomi_all_dropped.gds
# deliberately keeps the malformed-only shape instead: before the extractor
# reported a skipped marker through error(), such a cell lost its circuit from the
# layout netlist and then matched any schematic at all, and that case is what
# holds the fix in place.
#
# Usage (must run under KLayout so the PCell library is available):
#
#   KLAYOUT_HOME=<empty dir> KLAYOUT_PATH=<repo>/libs.tech/klayout \
#     klayout -zz -r create_cap_cmomi_testcases.py
#
# KLAYOUT_HOME matters: a user KLayout home that has another IHP PDK installed
# can register its own technology of the same name with a base path pointing at that
# installation, and the PCell would then be taken from there instead of from
# this tree.
#
import os

import pya

TECH_NAME = "sg13g2"
LIB_NAME = "SG13_dev"
PCELL_NAME = "cmomi"

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.join(HERE, "testcases", "unit", "cap_devices", "layout")
CHECKS_DIR = os.path.join(HERE, "testcases", "manual_tests", "cap_cmomi_checks")

# Layer numbers as used by the LVS deck, see
# libs.tech/klayout/tech/lvs/rule_decks/layers_definitions.lvs.
# datatype 0 = drawing, datatype 2 = pin.
METAL_LAYER = {1: 8, 2: 10, 3: 30, 4: 50, 5: 67}
VIA_LAYER = {1: 19, 2: 29, 3: 49, 4: 66}  # VIAn connects Metal n to Metal n+1
RECOG_MOM = (99, 39)

# Top metal of the devices the checks suite builds (mmax of their band).
TOP_METAL = 5

# Clear space left between two device markers so their Recog.mom never merge.
MARKER_GAP = 4.0


def _pcell(layout, **params):
    """Instantiate the cap_cmomi PCell, failing loudly if the library is absent."""
    cell = layout.create_cell(PCELL_NAME, LIB_NAME, params)
    if cell is None:
        raise SystemExit(
            "cap_cmomi PCell not found in %s. Check KLAYOUT_PATH and that the "
            "technology '%s' resolves to this tree." % (LIB_NAME, TECH_NAME)
        )
    return cell


def _new_layout():
    layout = pya.Layout()
    layout.technology_name = TECH_NAME
    return layout


def _pin_boxes(layout, cell, metal):
    """Pin boxes of `cell` on Metal<metal>, left to right."""
    li = layout.layer(METAL_LAYER[metal], 2)
    return sorted((s.dbbox() for s in cell.shapes(li).each()), key=lambda b: b.center().x)


def _row(layout, top, cells, y=0.0):
    """Place `cells` left to right with MARKER_GAP between bounding boxes.

    Returns the placement transform used for each cell, so callers can map a
    cell-local box to its position in `top`.
    """
    trans = []
    x = 0.0
    for cell in cells:
        bbox = cell.dbbox()
        t = pya.DTrans(pya.DVector(x - bbox.left, y))
        top.insert(pya.DCellInstArray(cell, t))
        trans.append(t)
        x += bbox.width() + MARKER_GAP
    return trans


def _strap(layout, cell, metal, box_a, box_b):
    """Draw a Metal<metal> rectangle joining two pin boxes that face each other.

    The strap keeps the pins' own y range, so it can only touch what the pins
    already touch, and it spans the clear gap between the two devices.
    """
    y_lo = max(box_a.bottom, box_b.bottom)
    y_hi = min(box_a.top, box_b.top)
    if y_hi <= y_lo:
        raise SystemExit("strap: pin boxes do not overlap in y")
    x_lo = min(box_a.left, box_b.left)
    x_hi = max(box_a.right, box_b.right)
    li = layout.layer(METAL_LAYER[metal], 0)
    cell.shapes(li).insert(pya.DBox(x_lo, y_lo, x_hi, y_hi))


def _write(layout, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    layout.write(path)
    print("  wrote %s" % path)


# ----------------------------------------------------------------------------
# unit testcases (must pass)
# ----------------------------------------------------------------------------

# Every entry gets its own net pair in the CDL, so the only thing the testcase
# asserts is that each configuration is recognised and extracted exactly once.
CONFIG_MATRIX = [
    # feed=double across the metal bands
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 5, "feed": "double"},
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 2, "feed": "double"},
    {"w": 5e-6, "l": 5e-6, "mmin": 4, "mmax": 5, "feed": "double"},
    # feed=same, including a band that does not start at Metal1
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 5, "feed": "same"},
    {"w": 5e-6, "l": 5e-6, "mmin": 2, "mmax": 5, "feed": "same"},
    # the PWell.block variant
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 5, "feed": "double", "subblock": 1},
    # non-square geometry, exercises the extractor's l->X / w->Y mapping
    {"w": 10e-6, "l": 20e-6, "mmin": 1, "mmax": 5, "feed": "double"},
]


def build_config():
    """Configuration matrix: one device per PCell configuration, own net pair."""
    layout = _new_layout()
    top = layout.create_cell("cap_cmomi_config")
    cells = [_pcell(layout, **p) for p in CONFIG_MATRIX]
    _row(layout, top, cells)
    top.flatten(-1, True)
    _write(layout, os.path.join(UNIT_DIR, "cap_cmomi_config.gds"))


def build_hier():
    """Hierarchical placement: a sub-cell instanced twice plus one direct cap.

    Deliberately not flattened, so the same marker geometry appears under
    several cell instances. The regression runs it in the default flat mode;
    deep mode is not exercised because the deep netlist collapses onto the
    PCell's own subcircuit and simplify drops the top cell, which is generic
    KLayout hierarchy behaviour and is already covered by test-LVS-switch.
    """
    layout = _new_layout()
    top = layout.create_cell("cap_cmomi_hier")

    pcell = _pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5, feed="double")
    unit = layout.create_cell("cmomi_unit")
    unit.insert(pya.DCellInstArray(pcell, pya.DTrans()))

    pitch = pcell.dbbox().width() + MARKER_GAP
    top.insert(pya.DCellInstArray(unit, pya.DTrans(pya.DVector(0.0, 0.0))))
    top.insert(pya.DCellInstArray(unit, pya.DTrans(pya.DVector(pitch, 0.0))))
    top.insert(pya.DCellInstArray(pcell, pya.DTrans(pya.DVector(2 * pitch, 0.0))))

    _write(layout, os.path.join(UNIT_DIR, "cap_cmomi_hier.gds"))


# ----------------------------------------------------------------------------
# characterization / negative layouts
# ----------------------------------------------------------------------------


def build_chain():
    """Three identical double-feed caps wired in series: A-N1-N2-B.

    The chain is the golden layout for the checks suite. It matters that it is
    a chain and not three floating caps: the shared nodes give each net a
    distinct top/bottom terminal degree, so a netlist that swaps one device's
    terminals can no longer be matched by relabelling nets.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomi_chain")

    cells = [_pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5, feed="double") for _ in range(3)]
    trans = _row(layout, top, cells)

    # Pins are on the top metal (mmax) at the left and right feed pads.
    placed = []
    for cell, t in zip(cells, trans):
        left, right = _pin_boxes(layout, cell, TOP_METAL)
        placed.append((t * left, t * right))

    for (_, right), (left, _) in zip(placed, placed[1:]):
        _strap(layout, top, TOP_METAL, right, left)

    top.flatten(-1, True)
    _write(layout, os.path.join(CHECKS_DIR, "cmomi_chain.gds"))


def build_short_same():
    """A 'same' feed cap whose two stacked plates are shorted by a via.

    feed='same' stacks PLUS on mmax and MINUS on mmax-1 over the same footprint,
    and the two are kept apart only because cap_cmomi_connections.lvs ties each
    pin to its own metal. Dropping a Via4 cut into the overlap shorts them. If
    the per-metal connect were replaced by a merged port layer, this layout
    would look the same as the good one, so this is what proves the isolation
    is actually load bearing.

    A well formed cap sits next to it so the cell still holds a device once the
    shorted one is gone.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomi_short_same")

    broken = _pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5, feed="same")
    good = _pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5, feed="double")
    trans = _row(layout, top, [broken, good])

    # The mmax and mmax-1 pins share one footprint; a Via4 in it merges them.
    box = trans[0] * _pin_boxes(layout, broken, TOP_METAL)[0]
    top.flatten(-1, True)
    top.shapes(layout.layer(VIA_LAYER[TOP_METAL - 1], 0)).insert(box.enlarged(-0.005, -0.005))

    _write(layout, os.path.join(CHECKS_DIR, "cmomi_short_same.gds"))


def _bridge_markers(layout, top):
    """Join the two leftmost Recog.mom markers of `top` with a bridging rect."""
    recog = layout.layer(*RECOG_MOM)
    markers = sorted((s.dbbox() for s in top.shapes(recog).each()), key=lambda b: b.left)
    if len(markers) < 2:
        raise SystemExit("bridge: expected at least 2 markers, got %d" % len(markers))
    left, right = markers[0], markers[1]
    y_lo = max(left.bottom, right.bottom)
    y_hi = min(left.top, right.top)
    top.shapes(recog).insert(pya.DBox(left.right - 0.1, y_lo, right.left + 0.1, y_hi))


def build_merged():
    """Two caps whose Recog.mom markers are merged, next to a well formed cap.

    get_connectivity ties core to core, so two touching markers become a single
    device cluster carrying four pin ports. CapMomExtractor then takes the
    ports.size != 2 branch, which reports an extraction error naming the marker,
    so both of those devices are left out and no comparison runs.

    The markers are joined by a bridging rectangle rather than by abutting the
    two devices, so the case isolates the port-count path and does not also
    short the two combs together. The third, untouched cap is there so the
    partial extracted netlist still holds a device.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomi_merged")

    cells = [_pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5, feed="double") for _ in range(3)]
    _row(layout, top, cells)
    top.flatten(-1, True)
    _bridge_markers(layout, top)

    _write(layout, os.path.join(CHECKS_DIR, "cmomi_merged.gds"))


def build_all_dropped():
    """A cell whose every cap_cmomi is dropped by the extractor.

    Same merged-marker construction as build_merged, but with nothing else in
    the cell. Before the extractor reported the skipped marker through error(),
    both devices were skipped, the circuit was left with none, it was dropped
    from the layout netlist, and the comparison then matched any schematic at
    all. This layout exists to keep that closed.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomi_all_dropped")

    cells = [_pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5, feed="double") for _ in range(2)]
    _row(layout, top, cells)
    top.flatten(-1, True)
    _bridge_markers(layout, top)

    _write(layout, os.path.join(CHECKS_DIR, "cmomi_all_dropped.gds"))


def build_feed_none():
    """A feed='none' array: bars and teeth with no feed structure at all.

    The PCell still emits two MkPins, so the marker holds exactly two ports and
    the extractor builds a normal cap_cmomi from it, even though the alternating
    bars are never tied into two plates and the structure is not a usable
    capacitor.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomi_feed_none")
    cell = _pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5, feed="none")
    top.insert(pya.DCellInstArray(cell, pya.DTrans()))
    top.flatten(-1, True)
    _write(layout, os.path.join(CHECKS_DIR, "cmomi_feed_none.gds"))


def main():
    print("Generating cap_cmomi LVS testcase layouts")
    build_config()
    build_hier()
    build_chain()
    build_short_same()
    build_merged()
    build_all_dropped()
    build_feed_none()
    print("Done.")


main()
