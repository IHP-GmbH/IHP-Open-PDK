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
# cap_cmomi drawn-geometry test.
#
# Two checks that cap_cmomi_sweep.py cannot make.
#
# 1. GEOMETRY.  The number of fully coupled rows and columns the PCell actually
#    draws must equal the number the compact model bills for.  Both sides are
#    measured, neither is re-derived:
#      - the drawn counts come out of the generated GDS (bars and teeth on the
#        bottom metal, at the 0.89 / 0.84 unit-cell pitch),
#      - the billed counts come out of the OSDI binary under ngspice.  With
#        feed='none' the modelled capacitance is pure active area, so dividing
#        C(w) by the one-pitch step C(w+0.89) - C(w) returns the row count the
#        model used, and the same trick in x returns the column count.
#    Because the area formula is never written a second time here, this check
#    cannot be satisfied by two copies of the same mistake agreeing with each
#    other, which is exactly what a label-against-model comparison does.
#
# 2. FREEZE.  A digest of the drawn geometry, pinned to the current output,
#    taken once per drawing path (each feed variant, each metal window).
#    The drawn cell is already in fabricated designs, so a model correction must
#    leave the layout untouched.  Any edit that reaches the drawing path breaks
#    this check loudly instead of silently changing future GDS.
#
# Usage:
#   KLAYOUT_PATH=<libs.tech/klayout> python3 cap_cmomi_geometry_test.py [--run_dir DIR]
#
# Options:
#   --update-freeze   re-pin the freeze digests (only with a deliberate,
#                     reviewed layout change; never to make a red test green)
#
import hashlib
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KLAYOUT_DIR = os.path.dirname(HERE)                       # libs.tech/klayout
PDK_ROOT = os.path.dirname(os.path.dirname(KLAYOUT_DIR))  # <pdk>
OSDI = os.path.join(PDK_ROOT, "libs.tech", "ngspice", "osdi", "cap_cmomi.osdi")
TECH_NAME = "sg13cmos5l"

UC_X, UC_Y = 0.84, 0.89       # unit cell pitch in um
BOT_LAYER = (8, 0)            # Metal1.drawing, the mmin=1 comb
FMEAS = 1e6                   # low enough that L and R are negligible vs 1/(wC)

# Widths and lengths to check the counting law on.  8.9 and 21.0 are exact
# pitch multiples, where the epsilon-before-floor snapping has to land on the
# geometric count rather than one below it.
GEOM_W = [2.0, 3.0, 5.0, 7.0, 8.9, 15.0]
GEOM_L = [2.0, 3.0, 5.0, 5.5, 10.0, 21.0]

# Layout freeze: digests of the flattened PCell output.  One entry per drawing
# path, not just per size: the feed variants and the metal window each build
# different geometry, and a digest taken only on the default would not see a
# change confined to one of them.  Regenerate only with --update-freeze, and
# only when the layout was meant to move.
FREEZE_CASES = [
    {"w": 2.0, "l": 2.0, "mmin": 1, "mmax": 4, "feed": "double"},
    {"w": 5.0, "l": 5.0, "mmin": 1, "mmax": 4, "feed": "double"},
    {"w": 7.0, "l": 5.5, "mmin": 1, "mmax": 4, "feed": "double"},
    {"w": 5.0, "l": 5.0, "mmin": 1, "mmax": 4, "feed": "same"},
    {"w": 5.0, "l": 5.0, "mmin": 1, "mmax": 4, "feed": "none"},
    {"w": 5.0, "l": 5.0, "mmin": 2, "mmax": 4, "feed": "double"},
    {"w": 5.0, "l": 5.0, "mmin": 3, "mmax": 4, "feed": "same"},
]


def fkey(c):
    return f"w{c['w']}_l{c['l']}_m{c['mmin']}{c['mmax']}_{c['feed']}"


FREEZE = {
    "w2.0_l2.0_m14_double": "944b83dd6b44143a",
    "w5.0_l5.0_m14_double": "2580ac3086c98b97",
    "w7.0_l5.5_m14_double": "9b89e22667a019f9",
    "w5.0_l5.0_m14_same": "a481a5460c965ea3",
    "w5.0_l5.0_m14_none": "c5965f6812c5a713",
    "w5.0_l5.0_m24_double": "e445e40120aabd8d",
    "w5.0_l5.0_m34_same": "aa68dede0ef23d5f",
}


# ----------------------------------------------------------------- KLayout side

def _measure():
    """Run inside KLayout: emit drawn counts and freeze digests as JSON."""
    import pya

    # Provenance guard.  Both PDKs register a library called SG13_dev and one of
    # them may be installed under ~/.klayout, so confirm the PCell code actually
    # loaded is the one in this tree before believing any measurement.
    import sg13cmos5l_pycell_lib.ihp.cap_cmomi_code as pcell_mod
    src = os.path.realpath(pcell_mod.__file__)
    if not src.startswith(os.path.realpath(PDK_ROOT) + os.sep):
        # KLayout exits 0 on an uncaught SystemExit, so report through the file.
        with open(os.environ["CAP_CMOMI_GEOM_OUT"], "w") as f:
            json.dump({"error": f"PCell resolved to {src}, outside {PDK_ROOT}"}, f)
        return

    def build(w, l, mmin=1, mmax=4, feed="double"):
        layout = pya.Layout()
        layout.technology_name = TECH_NAME
        cell = layout.create_cell("cap_cmomi", "SG13_dev",
                                  {"w": w * 1e-6, "l": l * 1e-6,
                                   "mmin": mmin, "mmax": mmax, "feed": feed})
        if cell is None:
            raise SystemExit("cap_cmomi PCell not found in SG13_dev library")
        top = layout.create_cell("T")
        top.insert(pya.DCellInstArray(cell, pya.DTrans()))
        top.flatten(-1, True)
        return layout, top

    def counts(layout, top):
        """Drawn coupled rows and columns of the bottom-metal comb.

        The comb is drawn as boxes: one horizontal bar per row boundary, running
        the full array length, and two vertical teeth per unit cell in x.  N+1
        bars bound N coupled rows; the teeth sit in pairs at half the x pitch,
        so the number of distinct tooth x-positions is twice the column count.
        Square boxes are the via landing pads of the feed columns and belong to
        neither, so both tests are strict.
        """
        li = layout.layer(*BOT_LAYER)
        bars, tooth_x = 0, set()
        for s in top.shapes(li).each():
            b = s.box
            if b.width() > b.height():
                bars += 1
            elif b.height() > b.width():
                tooth_x.add(round((b.left + b.right) / 2 * layout.dbu, 4))
        return bars - 1, len(tooth_x) // 2

    def digest(layout, top):
        """Order-independent hash of the drawn geometry, in database units.

        Polygons go in through their full string form, so holes count as well
        as hulls.  Text is deliberately excluded: the C label states a modelled
        value and legitimately moves whenever a coefficient does, so hashing it
        here would turn every honest model change into a red freeze and invite
        re-pinning, which is the one thing this check exists to prevent.  The
        label's value is pinned separately, in cap_cmomi_consistency_test.py.
        """
        per_layer = []
        for li in layout.layer_indexes():
            info = str(layout.get_info(li))
            items = sorted(
                sh.polygon.to_s() for sh in top.shapes(li).each()
                if not sh.is_text()
            )
            if items:
                per_layer.append(info + "|" + "|".join(items))
        blob = "\n".join(sorted(per_layer)).encode()
        return hashlib.sha256(blob).hexdigest()[:16]

    out = {"rows": {}, "cols": {}, "freeze": {}}
    for w in GEOM_W:
        layout, top = build(w, 5.0)
        out["rows"][f"{w}"] = counts(layout, top)[0]
    for l in GEOM_L:
        layout, top = build(5.0, l)
        out["cols"][f"{l}"] = counts(layout, top)[1]
    for c in FREEZE_CASES:
        layout, top = build(c["w"], c["l"], c["mmin"], c["mmax"], c["feed"])
        out["freeze"][fkey(c)] = digest(layout, top)

    with open(os.environ["CAP_CMOMI_GEOM_OUT"], "w") as f:
        json.dump(out, f)


# ------------------------------------------------------------- model-side probe

def _billed_counts(run_dir):
    """Row and column counts the compact model bills, read back from the OSDI.

    feed='none' has no feed term, so the modelled capacitance is proportional to
    the billed active area.  One pitch step in w is worth exactly one row, so
    C(w) / (C(w + 0.89) - C(w)) is the billed row count; likewise in l.
    """
    probes, index = [], {}
    for w in GEOM_W:
        index[("row", w)] = len(probes)
        probes += [(5.0, w), (5.0, w + UC_Y)]
    for l in GEOM_L:
        index[("col", l)] = len(probes)
        probes += [(l, 5.0), (l + UC_X, 5.0)]

    lines = ["* cap_cmomi billed-count probe", ".model cmom cap_cmomi"]
    for i, (l, w) in enumerate(probes):
        lines += [f"N{i} p{i} 0 0 cmom w={w}u l={l}u mmin=1 mmax=4 feed=0",
                  f"V{i} p{i} 0 dc 0 ac 1"]
    lines.append(".end")
    tb = os.path.join(run_dir, "tb_cap_cmomi_counts.sp")
    with open(tb, "w") as f:
        f.write("\n".join(lines) + "\n")

    cmds = [f"osdi {OSDI}", f"source {tb}", f"ac lin 1 {FMEAS} {FMEAS}"]
    for i in range(len(probes)):
        cmds += [f"let c{i} = -imag(v{i}#branch)/({2 * math.pi}*{FMEAS})*1e15",
                 f"print c{i}"]
    cmds.append("quit")
    p = subprocess.run(["ngspice", "-p"], input="\n".join(cmds) + "\n",
                       capture_output=True, text=True, timeout=300)
    vals = {}
    for ln in p.stdout.splitlines():
        m = re.match(r"\s*c(\d+)\s*=\s*([-\d.eE+]+)", ln)
        if m:
            vals[int(m.group(1))] = float(m.group(2))
    if len(vals) != len(probes):
        sys.stderr.write(p.stdout[-2000:] + p.stderr[-1000:])
        raise SystemExit(f"ngspice returned {len(vals)}/{len(probes)} points")

    def count(i):
        step = vals[i + 1] - vals[i]
        if step <= 0:
            raise SystemExit("non-monotonic model capacitance; probe is invalid")
        return vals[i] / step

    rows = {f"{w}": count(index[("row", w)]) for w in GEOM_W}
    cols = {f"{l}": count(index[("col", l)]) for l in GEOM_L}
    return rows, cols


# ------------------------------------------------------------------ orchestrate

def _orchestrate():
    args = sys.argv[1:]
    update = "--update-freeze" in args
    run_dir = args[args.index("--run_dir") + 1] if "--run_dir" in args else \
        os.path.join(os.getcwd(), "cap_cmomi_geometry_run")
    os.makedirs(run_dir, exist_ok=True)

    env = dict(os.environ)
    env["KLAYOUT_PATH"] = KLAYOUT_DIR
    out = os.path.join(run_dir, "measured.json")
    env["CAP_CMOMI_GEOM_OUT"] = out
    if os.path.exists(out):
        os.remove(out)
    p = subprocess.run(["klayout", "-zz", "-r", os.path.abspath(__file__)],
                       env=env, capture_output=True, text=True)
    if not os.path.isfile(out):
        sys.stderr.write(f"KLayout produced no measurement at {out} "
                         f"(exit {p.returncode})\n")
        sys.stderr.write(p.stdout + p.stderr)
        return 1
    drawn = json.load(open(out))
    if "error" in drawn:
        sys.stderr.write(drawn["error"] + "\n")
        return 1
    billed_rows, billed_cols = _billed_counts(run_dir)

    # The billed counts are a ratio of two printed capacitances, so they land
    # near an integer rather than on it.  Being wrong by a whole row is the
    # failure this test looks for; a few 1e-5 of numerical dust is not.
    tol = 1e-3

    bad = 0
    print("\n=== cap_cmomi drawn geometry vs billed model area ===")
    print(f"{'w [um]':>8} {'drawn rows':>11} {'billed rows':>12}   status")
    for w in GEOM_W:
        d, b = drawn["rows"][f"{w}"], billed_rows[f"{w}"]
        ok = abs(b - d) < tol
        bad += 0 if ok else 1
        print(f"{w:8.2f} {d:11d} {b:12.4f}   {'ok' if ok else 'MISMATCH'}")
    print(f"{'l [um]':>8} {'drawn cols':>11} {'billed cols':>12}   status")
    for l in GEOM_L:
        d, b = drawn["cols"][f"{l}"], billed_cols[f"{l}"]
        ok = abs(b - d) < tol
        bad += 0 if ok else 1
        print(f"{l:8.2f} {d:11d} {b:12.4f}   {'ok' if ok else 'MISMATCH'}")

    print("\n=== layout freeze ===")
    if update:
        _repin(drawn["freeze"])
        print("freeze digests re-pinned in", os.path.basename(__file__))
    else:
        for c in FREEZE_CASES:
            key = fkey(c)
            want, got = FREEZE.get(key), drawn["freeze"][key]
            if want is None:
                print(f"{key:28s} {got}  UNPINNED (run --update-freeze once)")
                bad += 1
            elif got != want:
                print(f"{key:28s} {got}  MOVED (pinned {want})")
                bad += 1
            else:
                print(f"{key:28s} {got}  unchanged")

    print(f"\n{'FAIL' if bad else 'PASS'}: {bad} check(s) failed")
    return 1 if bad else 0


def _repin(digests):
    """Rewrite the FREEZE table in this file with freshly measured digests."""
    path = os.path.abspath(__file__)
    src = open(path).read()
    body = "\n".join(f'    "{fkey(c)}": "{digests[fkey(c)]}",' for c in FREEZE_CASES)
    new = re.sub(r"FREEZE = \{.*?\n\}", "FREEZE = {\n" + body + "\n}", src,
                 flags=re.S)
    open(path, "w").write(new)


if os.environ.get("CAP_CMOMI_GEOM_OUT"):
    _measure()
else:
    sys.exit(_orchestrate())
