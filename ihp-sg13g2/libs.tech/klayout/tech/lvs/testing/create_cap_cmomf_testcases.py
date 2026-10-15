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
# Generator for every cap_cmomf LVS testcase layout in this tree.
#
# The sibling of create_cap_cmomi_testcases.py, and deliberately its mirror
# image: same helpers, same file layout, same conventions, so the two devices
# can be read side by side. The differences all come from the geometry.
# cap_cmomf has no 'feed' parameter, its two pins always sit on the same metal
# (the mmax one) and they are not opposite each other, so the checks that the
# cap_cmomi suite builds around 'same'/'none' feeds have no counterpart here,
# and the wiring needs a routed channel rather than a straight strap.
#
# Each layout listed below is built from the SG13_dev PCell by this script rather
# than drawn by hand, so the layouts can be regenerated when the PCell changes.
# The generated files are checked in, so the regression does not need a working
# PCell library at test time (same convention as create_ind_testcases.py).
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
#       cap_cmomf.gds          the device testcase
#       cap_cmomf_config.gds   configuration matrix, every instance must extract
#       cap_cmomf_hier.gds     hierarchical instantiation, no double extraction
#
#   testcases/manual_tests/cap_cmomf_checks/
#       cmomf_chain.gds        3 caps in series, asymmetric, the golden layout
#       cmomf_mirrored.gds     the same chain with the last cap mirrored
#       cmomf_shorted.gds      a cap whose two plates are tied together
#       cmomf_merged.gds       two caps under one merged Recog.momf marker
#       cmomf_all_dropped.gds  a cell whose every device is dropped
#       cmomf_hier_wired.gds   the hierarchy of cap_cmomf_hier, but wired to the top
#       cmomf_coexist.gds      one cap_cmomf beside one cap_cmomi
#
# The malformed layouts carry a well formed cap alongside the broken one, so that
# each one exercises a comparison rather than an empty cell. cmomf_all_dropped.gds
# deliberately keeps the malformed-only shape instead: an extractor that only logs
# a skipped marker loses the circuit from the layout netlist, and the comparison
# then matches any schematic at all, and that case is what holds the fix in place.
#
# Usage (must run under KLayout so the PCell library is available):
#
#   KLAYOUT_HOME=<empty dir> KLAYOUT_PATH=<repo>/libs.tech/klayout \
#     klayout -zz -r create_cap_cmomf_testcases.py
#
# KLAYOUT_HOME matters: a user KLayout home that has ihp-sg13g2 installed
# registers its own 'sg13g2' technology with a base path pointing at that
# installation, and the PCell would then be taken from there instead of from
# this tree.
#
import os

import pya

TECH_NAME = "sg13g2"
LIB_NAME = "SG13_dev"
PCELL_NAME = "cmomf"   # g2 names the PCell class short; the model is cap_cmomf

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_DIR = os.path.join(HERE, "testcases", "unit", "cap_devices", "layout")
CHECKS_DIR = os.path.join(HERE, "testcases", "manual_tests", "cap_cmomf_checks")

# Layer numbers as used by the LVS deck, see
# libs.tech/klayout/tech/lvs/rule_decks/layers_definitions.lvs.
# datatype 0 = drawing, datatype 2 = pin.
METAL_LAYER = {1: 8, 2: 10, 3: 30, 4: 50, 5: 67}
RECOG_MOMF = (99, 40)
RECOG_MOM = (99, 39)  # cap_cmomi's marker, used by the coexistence layout

# Top metal of the devices the checks suite builds (mmax of their band).
TOP_METAL = 5

# Clear space left between two device markers so their Recog.momf never merge.
MARKER_GAP = 4.0

# Width of the wires this script draws. 0.20 is the minimum for Metal2 and above
# (Mn.a in the DRM), and every routed layout here is on Metal5.
WIRE = 0.20


def _pcell(layout, name=PCELL_NAME, **params):
    """Instantiate a PCell, failing loudly if the library is absent."""
    cell = layout.create_cell(name, LIB_NAME, params)
    if cell is None:
        raise SystemExit(
            "%s PCell not found in %s. Check KLAYOUT_PATH and that the "
            "technology '%s' resolves to this tree." % (name, LIB_NAME, TECH_NAME)
        )
    return cell


def _new_layout():
    layout = pya.Layout()
    layout.technology_name = TECH_NAME
    return layout


def _pin_boxes(layout, cell, metal):
    """Pin boxes of `cell` on Metal<metal>, left to right.

    For an unmirrored cap_cmomf that is [PLUS, MINUS]: PLUS hugs the left edge
    at mid height and MINUS sits at the middle of the top edge, which is the
    same order CapMomExtractor produces when it sorts the two ports by x.
    """
    li = layout.layer(METAL_LAYER[metal], 2)
    return sorted((s.dbbox() for s in cell.shapes(li).each()), key=lambda b: b.center().x)


def _row(layout, top, cells, mirrored=None, y=0.0, gap=MARKER_GAP):
    """Place `cells` left to right with `gap` between bounding boxes.

    `mirrored` is an optional per-cell flag; a mirrored instance is reflected
    about the y axis, which is what a designer does when placing a symmetric
    device and what moves the PLUS pin from the left edge to the right one.

    Returns the placement transform used for each cell, so callers can map a
    cell-local box to its position in `top`.
    """
    trans = []
    x = 0.0
    for i, cell in enumerate(cells):
        base = pya.DTrans(pya.DTrans.M90) if (mirrored and mirrored[i]) else pya.DTrans()
        bbox = cell.dbbox().transformed(base)
        t = pya.DTrans(pya.DVector(x - bbox.left, y)) * base
        top.insert(pya.DCellInstArray(cell, t))
        trans.append(t)
        x += bbox.width() + gap
    return trans


def _wire(layout, cell, metal, src, dst, channel_y, drop_x):
    """Route from `src` upwards into an overhead channel and into `dst` sideways.

    cap_cmomf does not offer two pins facing each other, so its devices cannot be
    chained with the single strap cap_cmomi uses. `src` is a pin that is reachable
    from above (the one on the top edge) and `dst` one that is reachable from the
    side (the one on a left or right connecting bar). The route leaves `src`
    upwards, runs across the channel above the row, drops down at `drop_x`, which
    must be in the clear gap beside `dst`'s device, and enters `dst` horizontally
    at its own y.

    Approaching `dst` from the side rather than from above is the whole point: the
    top edge of a cap_cmomf belongs to the other plate on every band whose top
    metal runs its fingers along x, so a wire coming straight down would short the
    device it is supposed to feed.
    """
    li = layout.layer(METAL_LAYER[metal], 0)
    top_y = channel_y + WIRE
    # up from src, across the channel, down beside dst, then into dst
    cell.shapes(li).insert(pya.DBox(src.left, src.bottom, src.right, top_y))
    cell.shapes(li).insert(pya.DBox(min(src.left, drop_x), channel_y,
                                    max(src.right, drop_x + WIRE), top_y))
    cell.shapes(li).insert(pya.DBox(drop_x, dst.bottom, drop_x + WIRE, top_y))
    cell.shapes(li).insert(pya.DBox(min(drop_x, dst.left), dst.bottom,
                                    max(drop_x + WIRE, dst.right), dst.top))


def _write(layout, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    layout.write(path)
    print("  wrote %s" % path)


# ----------------------------------------------------------------------------
# unit testcases (must pass)
# ----------------------------------------------------------------------------

# Every entry gets its own net pair in the CDL, so the only thing the testcase
# asserts is that each configuration is recognised and extracted exactly once.
#
# The bands are chosen for the port layer they land on, not for variety: the
# pins always sit on the mmax metal, so mmax is the only thing that decides
# which of the deck's m1p..m5p port paths is exercised at all. Every one of the
# five is covered here. mmax=1 also puts the pins on the 0.16 wide Metal1 bar,
# the one case where the PCell has to clip the pin box to the metal it labels.
CONFIG_MATRIX = [
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 5},   # ports on Metal5, full stack
    {"w": 5e-6, "l": 5e-6, "mmin": 2, "mmax": 5},   # ports on Metal5, band off Metal1
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 4},   # ports on Metal4
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 3},   # ports on Metal3
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 2},   # ports on Metal2
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 1},   # ports on Metal1, single layer
    {"w": 5e-6, "l": 5e-6, "mmin": 1, "mmax": 5, "subblock": 1},  # PWell.block variant
    {"w": 10e-6, "l": 20e-6, "mmin": 1, "mmax": 5},  # non-square, exercises l->X / w->Y
]


def build_original():
    """The cap_cmomf device testcase for the unit regression.

    Three caps covering both orientations of the top metal plus a stack that
    stops below Metal5. The finger direction alternates per layer, so the metal
    that carries the pins and the shape of the bar they land on both depend on
    how many layers the stack has.

    Flattened. A cap_cmomf alone in a sub-cell extracts nothing in deep mode
    (see build_hier), and a testcase should not depend on the regression running
    it flat.
    """
    layout = _new_layout()
    top = layout.create_cell("cap_cmomf")

    cells = [
        _pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5),
        _pcell(layout, w=5e-6, l=5e-6, mmin=2, mmax=5),
        _pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=3),
    ]
    _row(layout, top, cells)

    top.flatten(-1, True)
    _write(layout, os.path.join(UNIT_DIR, "cap_cmomf.gds"))


def build_config():
    """Configuration matrix: one device per PCell configuration, own net pair."""
    layout = _new_layout()
    top = layout.create_cell("cap_cmomf_config")
    cells = [_pcell(layout, **p) for p in CONFIG_MATRIX]
    _row(layout, top, cells)
    top.flatten(-1, True)
    _write(layout, os.path.join(UNIT_DIR, "cap_cmomf_config.gds"))


def build_hier():
    """Hierarchical placement: a sub-cell instanced twice plus one direct cap.

    Deliberately not flattened, so the same marker geometry appears under
    several cell instances. The regression runs it in the default flat mode.

    None of these caps connects to anything outside its own cell, and in deep
    mode the layout netlist then comes out empty. cap_cmomi behaves the same
    way, which is the first evidence that the hole is not specific to either
    device; see IHP-GmbH/ihp-sg13cmos5l#91, where it was first recorded. This
    PDK does not refuse an empty layout netlist, so a deep run of this layout
    reports a match having compared nothing, and the checks suite records that.
    """
    layout = _new_layout()
    top = layout.create_cell("cap_cmomf_hier")

    pcell = _pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5)
    unit = layout.create_cell("cmomf_unit")
    unit.insert(pya.DCellInstArray(pcell, pya.DTrans()))

    pitch = pcell.dbbox().width() + MARKER_GAP
    top.insert(pya.DCellInstArray(unit, pya.DTrans(pya.DVector(0.0, 0.0))))
    top.insert(pya.DCellInstArray(unit, pya.DTrans(pya.DVector(pitch, 0.0))))
    top.insert(pya.DCellInstArray(pcell, pya.DTrans(pya.DVector(2 * pitch, 0.0))))

    _write(layout, os.path.join(UNIT_DIR, "cap_cmomf_hier.gds"))


def build_hier_wired():
    """The same hierarchy as build_hier, with one net crossing a cell boundary.

    Two instances of a sub-cell holding one cap, joined by a Metal5 route drawn
    in the top cell, so the sub-circuits get a pin and are not dropped. This is
    the deep-mode counterpart of build_hier, whose layout extracts nothing in
    deep and is then reported as a match having compared nothing. This one is
    what makes that case mean something: it compares for real, so a total
    collapse of deep extraction shows up here instead of hiding behind the
    other case's vacuous pass.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomf_hier_wired")

    unit = layout.create_cell("cmomf_unit")
    unit.insert(pya.DCellInstArray(
        _pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5), pya.DTrans()))
    unit.flatten(-1, True)

    bbox = unit.dbbox()
    pitch = bbox.width() + MARKER_GAP
    left = pya.DTrans(pya.DVector(-bbox.left, 0.0))
    right = pya.DTrans(pya.DVector(-bbox.left + pitch, 0.0))
    top.insert(pya.DCellInstArray(unit, left))
    top.insert(pya.DCellInstArray(unit, right))

    pins = _pin_boxes(layout, unit, TOP_METAL)
    plus, minus = pins[0], pins[-1]
    _wire(layout, top, TOP_METAL, minus.transformed(left), plus.transformed(right),
          channel_y=bbox.top + 1.0, drop_x=bbox.right + 1.0)

    _write(layout, os.path.join(CHECKS_DIR, "cmomf_hier_wired.gds"))


# ----------------------------------------------------------------------------
# characterization / negative layouts
# ----------------------------------------------------------------------------


def _chain(layout, top, mirrored=None):
    """Three identical caps wired in series in `top`: A-N1-N2-B.

    It matters that it is a chain and not three floating caps: the shared nodes
    give each net a distinct terminal degree, so a netlist that swaps one
    device's terminals can no longer be matched by relabelling nets.

    Each link leaves the left device's top pin and enters the right device's
    side pin, dropping down in the clear gap beside it. A mirrored instance has
    its side pin on the right, so the drop moves past that device instead of
    stopping before it, which is the only thing mirroring changes here.

    Only the last device may be mirrored, and the routing is why. Dropping past
    a device means the channel that carries the link runs over it, and every
    device except the last one also sends a riser up from its own top pin to
    that same channel. The two would touch, which ties the device's two plates
    together, and KLayout then drops it from the netlist and the case tests
    nothing. The last device has no riser, so there is nothing to cross.
    """
    if mirrored and any(mirrored[:-1]):
        raise SystemExit("_chain: only the last device may be mirrored")

    cells = [_pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5) for _ in range(3)]
    trans = _row(layout, top, cells, mirrored=mirrored)

    placed = []
    for cell, t in zip(cells, trans):
        pins = _pin_boxes(layout, cell, TOP_METAL)
        boxes = [b.transformed(t) for b in pins]
        # The side pin is the one whose x range touches the device's own edge;
        # the other is the top pin. Mirroring exchanges which is which.
        bbox = cell.dbbox().transformed(t)
        side = min(boxes, key=lambda b: min(b.left - bbox.left, bbox.right - b.right))
        top_pin = boxes[0] if boxes[1] is side else boxes[1]
        placed.append((side, top_pin, bbox))

    channel_y = max(b.top for _, _, b in placed) + 1.0
    for (_, src, _), (dst, _, dst_bbox) in zip(placed, placed[1:]):
        # Drop before the device when its side pin is on the left, past it when
        # mirroring has moved that pin to the right.
        on_left = (dst.left - dst_bbox.left) < (dst_bbox.right - dst.right)
        drop_x = dst_bbox.left - 1.0 if on_left else dst_bbox.right + 1.0
        _wire(layout, top, TOP_METAL, src, dst, channel_y, drop_x)

    top.flatten(-1, True)


def build_chain():
    """Three identical caps wired in series: A-N1-N2-B. The golden layout."""
    layout = _new_layout()
    top = layout.create_cell("cmomf_chain")
    _chain(layout, top)
    _write(layout, os.path.join(CHECKS_DIR, "cmomf_chain.gds"))


def build_mirrored():
    """The same chain with the last cap mirrored about the y axis.

    Electrically identical to build_chain and it compares against the same
    netlist, because a cap_cmomf is symmetric: mirroring one placement does not
    change the circuit. What it does change is the order in which
    CapMomExtractor hands the two ports over, since it sorts them by x and
    never reads their pin names, so the pin that was mim_top becomes mim_btm.

    That only stays invisible while the two terminals are declared equivalent
    on the device class. This case is what says whether they are.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomf_mirrored")
    _chain(layout, top, mirrored=[False, False, True])
    _write(layout, os.path.join(CHECKS_DIR, "cmomf_mirrored.gds"))


def build_shorted():
    """A cap whose two plates are tied together outside the device.

    cap_cmomf keeps its two combs apart through nothing but their own via
    stacks and the per-metal pin connect, so a wire from the PLUS bar to the
    MINUS edge collapses the device onto one net. The route runs outside the
    marker on the left and enters the top edge from above, so it touches each
    plate exactly once and adds nothing inside the device.

    A well formed cap sits next to it, so the cell still holds a comparable
    device once the shorted one is accounted for.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomf_shorted")

    cells = [_pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5) for _ in range(2)]
    trans = _row(layout, top, cells)

    plus, minus = [b.transformed(trans[0]) for b in _pin_boxes(layout, cells[0], TOP_METAL)]
    bbox = cells[0].dbbox().transformed(trans[0])
    top.flatten(-1, True)

    _wire(layout, top, TOP_METAL, minus, plus,
          channel_y=bbox.top + 1.0, drop_x=bbox.left - 1.0)

    _write(layout, os.path.join(CHECKS_DIR, "cmomf_shorted.gds"))


def _bridge_markers(layout, top):
    """Join the two leftmost Recog.momf markers of `top` with a bridging rect."""
    recog = layout.layer(*RECOG_MOMF)
    markers = sorted((s.dbbox() for s in top.shapes(recog).each()), key=lambda b: b.left)
    if len(markers) < 2:
        raise SystemExit("bridge: expected at least 2 markers, got %d" % len(markers))
    left, right = markers[0], markers[1]
    y_lo = max(left.bottom, right.bottom)
    y_hi = min(left.top, right.top)
    top.shapes(recog).insert(pya.DBox(left.right - 0.1, y_lo, right.left + 0.1, y_hi))


def build_merged():
    """Two caps whose Recog.momf markers are merged, next to a well formed cap.

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
    top = layout.create_cell("cmomf_merged")

    cells = [_pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5) for _ in range(3)]
    _row(layout, top, cells)
    top.flatten(-1, True)
    _bridge_markers(layout, top)

    _write(layout, os.path.join(CHECKS_DIR, "cmomf_merged.gds"))


def build_all_dropped():
    """A cell whose every cap_cmomf is dropped by the extractor.

    Same merged-marker construction as build_merged, but with nothing else in
    the cell. If the extractor only logged the skipped marker, both devices
    would be skipped, the circuit would be left with none, it would drop out of
    the layout netlist, and the comparison would then match any schematic at
    all. This layout exists to keep that closed for cap_cmomf too.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomf_all_dropped")

    cells = [_pcell(layout, w=5e-6, l=5e-6, mmin=1, mmax=5) for _ in range(2)]
    _row(layout, top, cells)
    top.flatten(-1, True)
    _bridge_markers(layout, top)

    _write(layout, os.path.join(CHECKS_DIR, "cmomf_all_dropped.gds"))


def build_coexist():
    """One cap_cmomf beside one cap_cmomi, both on Metal1..Metal5.

    The two devices are extracted by two instances of the same CapMomExtractor,
    told apart by nothing but their recognition marker: 99/39 for cap_cmomi and
    99/40 for cap_cmomf. Sharing one marker would make a single geometry extract
    as both devices and fail on the device count, which is why cap_cmomf carries
    its own. This case is what holds that apart, and it is the one check in this
    suite with no counterpart on the cap_cmomi side.

    Deliberately rectangular, so a w/l swap in either device would also show up.
    """
    layout = _new_layout()
    top = layout.create_cell("cmomf_coexist")

    cells = [
        _pcell(layout, w=4e-6, l=12e-6, mmin=1, mmax=5),
        _pcell(layout, name="cmomi", w=4e-6, l=12e-6, mmin=1, mmax=5, feed="double"),
    ]
    _row(layout, top, cells)
    top.flatten(-1, True)

    _write(layout, os.path.join(CHECKS_DIR, "cmomf_coexist.gds"))


def main():
    print("Generating cap_cmomf LVS testcase layouts")
    build_original()
    build_config()
    build_hier()
    build_hier_wired()
    build_chain()
    build_mirrored()
    build_shorted()
    build_merged()
    build_all_dropped()
    build_coexist()
    print("Done.")


# Guarded, so importing this module to reuse its helpers does not rewrite every
# checked-in layout as a side effect. `klayout -zz -r` sets __name__ to
# "__main__", so the documented invocation still runs.
if __name__ == "__main__":
    main()
