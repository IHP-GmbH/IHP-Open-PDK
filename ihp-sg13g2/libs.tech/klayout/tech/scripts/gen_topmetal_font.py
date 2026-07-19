"""Module to automatically generate a KLayout custom font file containing DRC-clean
uppercase A-Z glyphs (plus a space) for the highest TopMetal layer of whichever IHP
PDK is checked out next to this one -- SG13G2's TopMetal2, or SG13CMOS5L's
TopMetal1 (that stack has no TopMetal2). Can be used in Klayout's batch mode. For
example, to regenerate the font shipped with this PDK:

klayout -zz -r gen_topmetal_font.py \
        -rd output=../../fonts/topmetal_font.gds.gz

Which PDK is active is auto-detected by which tech rule-deck JSON is present on
disk (see TECH_CONFIGS/detect_tech() below) -- there is no PDK/PDK_ROOT env var or
KLayout technology argument involved. Exactly one of the two is expected to exist
at a time; this script only ever ships inside the sg13g2 tree, but it walks up to
the common parent directory and looks for both, so it works unmodified if run from
a checkout that has an ihp-sg13cmos5l sibling instead.

The output path's extension controls compression: KLayout's GDS writer/reader (and
TextGenerator.load_from_file) transparently gzip-compress/decompress based on a
".gz" suffix, so writing straight to "topmetal_font.gds.gz" needs no separate
compression step. The generated file is checked into
libs.tech/klayout/fonts/topmetal_font.gds.gz so it is available to everyone using
this PDK without a per-user install: that directory is the first entry of the
KLAYOUT_PATH this PDK's own docs recommend (libs.tech/klayout/tech/drc/README.md),
and it is what KLAYOUT_HOME should point at if used in place of the default
~/.klayout. KLayout looks for a "fonts" folder in both locations, so no manual copy
step is needed. The font is registered under its filename stem regardless of the
".gds.gz" double extension, so it still shows up by name ("topmetal_font") in the
Basic:TEXT PCell's font list. Always use magnification 1 with this font -- scaling
it down can reopen the TopMetal width/space violations it was built to avoid.
"""
# pylint: disable=import-error
import json
import pathlib
import sys
import klayout.db as db

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
# .../<repo_root>/ihp-sg13g2/libs.tech/klayout/tech/scripts -> <repo_root>
REPO_ROOT = SCRIPT_DIR.parents[4]

# Each entry describes one IHP PDK/stack option: where its tech rule-deck JSON
# lives (relative to the repo root, so this also works for a sibling PDK this
# script doesn't ship inside), and which of its DRC rule keys give the min.
# width/space of that stack's *highest* TopMetal layer.
TECH_CONFIGS = [
    {
        'rel_path': ('ihp-sg13g2', 'libs.tech', 'klayout', 'tech', 'drc',
                     'rule_decks', 'sg13g2_tech_default.json'),
        'width_key': 'TM2_a',
        'space_key': 'TM2_b',
        'layer_name': 'TopMetal2',
    },
    {
        'rel_path': ('ihp-sg13cmos5l', 'libs.tech', 'klayout', 'tech', 'drc',
                     'rule_decks', 'sg13cmos5l_tech_default.json'),
        'width_key': 'TM1_a',
        'space_key': 'TM1_b',
        'layer_name': 'TopMetal1',
    },
]

# Safety margin added on top of the live TM.a/TM.b values so the font keeps
# clearing DRC with room to spare if the rule deck ever tightens slightly.
MARGIN_UM = 0.3

DBU = 0.001
GLYPH_LAYER = (1, 0)
ADVANCE_LAYER = (2, 0)
FONT_NAME = 'topmetal_font'

# Glyph design grid: 5 columns (x = 0..4) x 7 rows (y = 0..6), baseline at y = 0.
GLYPH_COLS = 4
GLYPH_ROWS = 6
ADVANCE_COLS = GLYPH_COLS + 1  # one extra grid step reserved as inter-character spacing


def detect_tech():
    found = [cfg for cfg in TECH_CONFIGS if (REPO_ROOT / pathlib.Path(*cfg['rel_path'])).is_file()]
    if not found:
        candidates = ", ".join(str(pathlib.Path(*cfg['rel_path'])) for cfg in TECH_CONFIGS)
        raise FileNotFoundError(
            f"Could not find a tech rule-deck JSON for any known PDK under {REPO_ROOT} "
            f"(looked for: {candidates}). This script auto-detects SG13G2 vs. "
            "SG13CMOS5L by which rule-deck file is present."
        )
    if len(found) > 1:
        names = ", ".join(str(pathlib.Path(*cfg['rel_path'])) for cfg in found)
        raise RuntimeError(
            f"Found rule-deck JSON files for more than one PDK ({names}); expected "
            "exactly one of SG13G2 / SG13CMOS5L to be checked out at a time."
        )
    cfg = found[0]
    return cfg, REPO_ROOT / pathlib.Path(*cfg['rel_path'])


def load_tm_rules():
    cfg, path = detect_tech()
    with open(path, encoding='utf-8') as tech_file:
        rules = json.load(tech_file)['drc_rules']
    try:
        return cfg, rules[cfg['width_key']], rules[cfg['space_key']]
    except KeyError as exc:
        raise KeyError(
            f"{path} no longer defines {exc}; update this script's rule keys for "
            f"{cfg['layer_name']}"
        ) from exc


TECH_CFG, TM_A_UM, TM_B_UM = load_tm_rules()
STROKE_UM = TM_A_UM + MARGIN_UM
GAP_UM = TM_B_UM + MARGIN_UM
PITCH_UM = STROKE_UM + GAP_UM


def to_dbu(value_um):
    return int(round(value_um / DBU))


STROKE = to_dbu(STROKE_UM)
HALF_STROKE = STROKE // 2
PITCH = to_dbu(PITCH_UM)


def grid_point(x, y):
    return int(round(x * PITCH)), int(round(y * PITCH))


def seg_box(p0, p1):
    """A stroke_width-wide box covering segment p0->p1, extended by half a stroke
    width along its own axis at both ends so that segments meeting at a shared grid
    point genuinely overlap (a full stroke_width x stroke_width square at the
    joint) instead of merely touching at a corner."""
    x0, y0 = p0
    x1, y1 = p1
    if y0 == y1:
        xa, xb = sorted((x0, x1))
        return db.Box(xa - HALF_STROKE, y0 - HALF_STROKE, xb + HALF_STROKE, y0 + HALF_STROKE)
    if x0 == x1:
        ya, yb = sorted((y0, y1))
        return db.Box(x0 - HALF_STROKE, ya - HALF_STROKE, x0 + HALF_STROKE, yb + HALF_STROKE)
    raise ValueError(f"non-Manhattan segment {p0} -> {p1}")


def polyline_region(points):
    grid_pts = [grid_point(x, y) for x, y in points]
    region = db.Region()
    for a, b in zip(grid_pts, grid_pts[1:]):
        region.insert(seg_box(a, b))
    return region


def staircase(x0, y0, x1, y1, nsteps):
    """Manhattan approximation of a straight line from (x0,y0) to (x1,y1),
    alternating horizontal/vertical unit steps instead of a diagonal edge -- real
    diagonals are what created sub-minimum notches with KLayout's default font."""
    points = [(x0, y0)]
    cy = y0
    for i in range(1, nsteps + 1):
        nx = x0 + (x1 - x0) * i / nsteps
        points.append((nx, cy))
        ny = y0 + (y1 - y0) * i / nsteps
        points.append((nx, ny))
        cy = ny
    return points


def glyph_region(polylines):
    region = db.Region()
    for pl in polylines:
        region += polyline_region(pl)
    return region.merged()


_O_OUTLINE = [
    (1, 0), (3, 0), (3, 1), (4, 1), (4, 5), (3, 5), (3, 6), (1, 6),
    (1, 5), (0, 5), (0, 1), (1, 1), (1, 0),
]

# Every letter is built from Manhattan polylines only (no 45-degree edges anywhere);
# apparent diagonals (K, N, R, V, W, X, Y, Z) are Manhattan staircases via staircase().
GLYPHS = {
    'A': [
        [(0, 0), (0, 6)],
        [(4, 0), (4, 6)],
        [(0, 6), (4, 6)],
        [(0, 3), (4, 3)],
    ],
    'B': [
        [(0, 0), (0, 6)],
        [(0, 6), (3, 6), (3, 3), (0, 3)],
        [(0, 3), (3, 3), (3, 0), (0, 0)],
    ],
    'C': [[(3, 6), (0, 6), (0, 0), (3, 0)]],
    'D': [[(0, 0), (0, 6)], [(0, 6), (3, 6), (3, 0), (0, 0)]],
    'E': [[(0, 0), (0, 6)], [(0, 6), (3, 6)], [(0, 3), (2, 3)], [(0, 0), (3, 0)]],
    'F': [[(0, 0), (0, 6)], [(0, 6), (3, 6)], [(0, 3), (2, 3)]],
    'G': [[(3, 6), (0, 6), (0, 0), (3, 0), (3, 2), (2, 2)]],
    'H': [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    'I': [[(1, 6), (3, 6)], [(2, 6), (2, 0)], [(1, 0), (3, 0)]],
    'J': [[(2, 6), (4, 6)], [(3, 6), (3, 0)], [(3, 0), (1, 0), (1, 1)]],
    'K': [[(0, 0), (0, 6)], staircase(0, 3, 4, 6, 3), staircase(0, 3, 4, 0, 3)],
    'L': [[(0, 0), (0, 6)], [(0, 0), (3, 0)]],
    'M': [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 6), (1, 6), (1, 4), (3, 4), (3, 6), (4, 6)]],
    'N': [[(0, 0), (0, 6)], [(4, 0), (4, 6)], staircase(0, 6, 4, 0, 4)],
    'O': [_O_OUTLINE],
    'P': [[(0, 0), (0, 6)], [(0, 6), (3, 6), (3, 3), (0, 3)]],
    'Q': [_O_OUTLINE, staircase(2, 1, 4, -1, 2)],
    'R': [[(0, 0), (0, 6)], [(0, 6), (3, 6), (3, 3), (0, 3)], staircase(1, 3, 4, 0, 3)],
    'S': [[(4, 6), (0, 6), (0, 3), (4, 3), (4, 0), (0, 0)]],
    'T': [[(0, 6), (4, 6)], [(2, 6), (2, 0)]],
    'U': [[(0, 6), (0, 0), (4, 0), (4, 6)]],
    'V': [
        [(0, 6), (0, 2)] + staircase(0, 2, 2, 0, 2)[1:],
        [(4, 6), (4, 2)] + staircase(4, 2, 2, 0, 2)[1:],
    ],
    'W': [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 0), (1, 0), (1, 2), (3, 2), (3, 0), (4, 0)]],
    'X': [
        [(0, 6), (0, 5), (1, 5), (1, 3), (3, 3), (3, 1), (4, 1), (4, 0)],
        [(4, 6), (4, 5), (3, 5), (3, 3), (1, 3), (1, 1), (0, 1), (0, 0)],
    ],
    'Y': [[(0, 6), (0, 4), (4, 4), (4, 6)], [(2, 4), (2, 0)]],
    'Z': [
        [(0, 6), (4, 6)],
        [(4, 6), (4, 5), (3, 5), (3, 3), (1, 3), (1, 1), (0, 1), (0, 0)],
        [(0, 0), (4, 0)],
    ],
}


def cell_name_for(char):
    if char.isalpha():
        return char
    return f"{ord(char):03d}"


def build_font_layout():
    layout = db.Layout(True)
    layout.dbu = DBU
    glyph_layer = layout.layer(*GLYPH_LAYER)
    advance_layer = layout.layer(*ADVANCE_LAYER)

    advance_box = db.Box(0, 0, ADVANCE_COLS * PITCH, GLYPH_ROWS * PITCH)

    tm_a_dbu = to_dbu(TM_A_UM)
    tm_b_dbu = to_dbu(TM_B_UM)
    failures = []

    for char in sorted(GLYPHS):
        region = glyph_region(GLYPHS[char])
        width_violations = list(region.width_check(tm_a_dbu))
        space_violations = list(region.space_check(tm_b_dbu))
        if width_violations or space_violations:
            failures.append((char, len(width_violations), len(space_violations)))
            continue
        cell = layout.create_cell(cell_name_for(char))
        cell.shapes(glyph_layer).insert(region)
        cell.shapes(advance_layer).insert(advance_box)

    space_cell = layout.create_cell(cell_name_for(' '))
    space_cell.shapes(advance_layer).insert(advance_box)

    if failures:
        details = ", ".join(f"{c} (width={w}, space={s})" for c, w, s in failures)
        raise RuntimeError(
            f"Refusing to write font: glyphs fail {TECH_CFG['width_key']}/"
            f"{TECH_CFG['space_key']} self-check: {details}"
        )

    comment = layout.create_cell('COMMENT')
    comment_texts = [
        f"design_grid={PITCH}",
        f"line_width={STROKE}",
        f"{TECH_CFG['layer_name']} DRC-clean uppercase font (stroke {STROKE_UM:.2f}um, "
        f"gap {GAP_UM:.2f}um, {TECH_CFG['width_key']}/{TECH_CFG['space_key']} "
        f"margin {MARGIN_UM:.2f}um)",
    ]
    for text in comment_texts:
        comment.shapes(glyph_layer).insert(db.Text(text, db.Trans()))

    return layout, tm_a_dbu, tm_b_dbu


def verify_sample_string(font_path, tm_a_dbu, tm_b_dbu, sample=None):
    if sample is None:
        sample = f"{TECH_CFG['layer_name'].upper()} TEST"
    generator = db.TextGenerator()
    generator.load_from_file(str(font_path))
    region = generator.text(sample, DBU, 1.0)
    width_violations = list(region.width_check(tm_a_dbu))
    space_violations = list(region.space_check(tm_b_dbu))
    if width_violations or space_violations:
        raise RuntimeError(
            f"Refusing to write font: rendered sample {sample!r} fails "
            f"{TECH_CFG['width_key']}/{TECH_CFG['space_key']} self-check "
            f"(width={len(width_violations)}, space={len(space_violations)}); "
            "inter-character spacing needs to increase"
        )
    return region.bbox()


try:
    output
except NameError:
    print("Missing output argument. Please define '-rd output=<path-to-font-gds>'")
    sys.exit(1)

print(f"Detected {TECH_CFG['layer_name']} stack ({TECH_CFG['width_key']}={TM_A_UM}um "
      f"{TECH_CFG['space_key']}={TM_B_UM}um) -> stroke={STROKE_UM}um gap={GAP_UM}um "
      f"pitch={PITCH_UM}um")

font_layout, tm_a_dbu_v, tm_b_dbu_v = build_font_layout()
print(f"Built {len(GLYPHS) + 1} glyph cells, all pass "
      f"{TECH_CFG['width_key']}/{TECH_CFG['space_key']} self-check.")

output_path = pathlib.Path(output)  # pylint: disable=undefined-variable
output_path.parent.mkdir(parents=True, exist_ok=True)
font_layout.write(str(output_path))
print(f"Wrote font '{FONT_NAME}' to {output_path}")

sample_bbox = verify_sample_string(output_path, tm_a_dbu_v, tm_b_dbu_v)
print(f"Rendered sample string (loaded back from the written font file) passes "
      f"{TECH_CFG['width_key']}/{TECH_CFG['space_key']} self-check. "
      f"bbox: w={sample_bbox.width()*DBU:.3f}um h={sample_bbox.height()*DBU:.3f}um")
