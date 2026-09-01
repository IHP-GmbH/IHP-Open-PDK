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
# cap_cmomf PCell DRC + LVS sweep.
#
# Generates a matrix of cap_cmomf configurations from the SG13_dev PyCell
# library and checks each one:
#   - the PCell instantiates and writes a GDS,
#   - geometric DRC reports no rule the device itself is responsible for,
#   - the LVS extractor recognises a cap_cmomf device with two distinct
#     terminal nets,
#   - the extracted w and l match the drawn ones, which is what pins the axis
#     convention: the shared CapMomExtractor reads l from the marker bbox
#     WIDTH, so the PCell has to draw l along X. Get that backwards and the
#     netlist reports w and l swapped from the symbol. Nothing else catches it,
#     because both are non-primary parameters that LVS never compares and the C
#     label below is w*l, unchanged by a swap.
#   - the C label the PCell paints matches the analytic density formula, which
#     is the same expression the Verilog-A model and the xschem symbol carry.
#
# The sweep is also the DRC coverage for this device: the DRC regression only
# walks testcases/unit_golden and testcases/unit/density, so a device testcase
# dropped anywhere else would never be run.
#
# Dual mode (single file):
#   - run under KLayout (pya available) with CAP_CMOMF_CFG/CAP_CMOMF_OUT set:
#     emits one config's GDS. This is how the orchestrator generates each
#     layout.
#   - run as plain python3: orchestrates the whole sweep and exits non-zero on
#     any failure (CI friendly).
#
# Usage:
#   KLAYOUT_PATH=<libs.tech/klayout> python3 cap_cmomf_sweep.py [--run_dir DIR]
#
import os
import sys
import json
import re

HERE = os.path.dirname(os.path.abspath(__file__))
KLAYOUT_DIR = os.path.dirname(HERE)                       # libs.tech/klayout
LVS_RUNNER = os.path.join(KLAYOUT_DIR, "tech", "lvs", "run_lvs.py")
DRC_RUNNER = os.path.join(KLAYOUT_DIR, "tech", "drc", "run_drc.py")
TECH_NAME = "sg13cmos5l"

# Capacitance density [fF/um^2], kept in step with cap_cmomf_code.py,
# cap_cmomf.va, cap_cmomf.lib and cap_cmomf.sym. See the PCell docstring for
# where the numbers come from.
AREACAP_M1 = 0.372
AREACAP_MN = 0.305

# Placement grid, mirrored from sg13cmos5l_tech.json techParams. The PCell
# snaps w and l with GridFix before drawing anything, so the analytic check
# below has to snap them the same way or an off-grid config would look like a
# label mismatch instead of the pass it is.
GRID = 0.005
EPSILON = 0.001

# Rules that fire on any bare device cell because the surroundings are absent:
# an isolated capacitor has no Activ, no GatPoly and no TopMetal1 anywhere, so
# the global density rules have nothing to measure. Anything outside this set
# is a real violation of the device itself.
DRC_EXPECTED_VIOLATIONS = {
    "AFil.g", "GFil.g", "TM1.c", "M1.j", "M2.j", "M3.j", "M4.j",
}

# name -> pcell params. The metal stack drives the top-layer finger
# orientation, which is what decides where the PLUS/MINUS pins land, so the
# stack variants matter more here than they do for cap_cmomi.
CONFIGS = [
    ("n4_5x5",    {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 4}),
    ("n3_m1m3",   {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 3}),
    ("n3_m2m4",   {"w": 5e-6,  "l": 5e-6,  "mmin": 2, "mmax": 4}),
    ("n2_m1m2",   {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 2}),
    ("n2_m3m4",   {"w": 5e-6,  "l": 5e-6,  "mmin": 3, "mmax": 4}),
    ("n1_m1",     {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 1}),
    ("n4_min",    {"w": 2e-6,  "l": 2e-6,  "mmin": 1, "mmax": 4}),
    ("n4_big",    {"w": 15e-6, "l": 15e-6, "mmin": 1, "mmax": 4}),
    ("n4_rect",   {"w": 4e-6,  "l": 12e-6, "mmin": 1, "mmax": 4}),
    ("n4_sub",    {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 4, "subblock": 1}),
    # Dimensions that are not multiples of the 5 nm grid. The PCell has to snap
    # the outer extents, not just the shapes derived from them, or the metal
    # edges land off grid and the offgrid table fires on every metal layer.
    ("n4_offgrid", {"w": 3.333e-6, "l": 7.777e-6, "mmin": 1, "mmax": 4}),
]


def _gridfix(x_um):
    """Snap to the placement grid exactly as the PCell's GridFix does."""
    return int(x_um / GRID + EPSILON) * GRID


def expected_c_ff(params):
    """Analytic capacitance in fF for a config, from the shared formula."""
    mmin = params.get("mmin", 1)
    mmax = params.get("mmax", 4)
    base = AREACAP_M1 if mmin == 1 else AREACAP_MN
    areacap = base + (mmax - mmin) * AREACAP_MN
    return areacap * _gridfix(params["l"] * 1e6) * _gridfix(params["w"] * 1e6)


def _generate_one():
    """KLayout-side: emit CAP_CMOMF_CFG to CAP_CMOMF_OUT as a flat GDS."""
    import pya
    cfg = json.loads(os.environ["CAP_CMOMF_CFG"])
    out = os.environ["CAP_CMOMF_OUT"]
    layout = pya.Layout()
    layout.technology_name = TECH_NAME
    cell = layout.create_cell("cap_cmomf", "SG13_dev", cfg["params"])
    if cell is None:
        raise SystemExit("cap_cmomf PCell not found in SG13_dev library")
    top = layout.create_cell(cfg["name"])
    top.insert(pya.DCellInstArray(cell, pya.DTrans()))
    top.flatten(-1, True)
    layout.write(out)


def _run(cmd):
    import subprocess
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def _drc_clean(drc_out):
    """Return (clean, unexpected_rules) from a run_drc.py transcript.

    The old check grepped 'Number of DRC errors for maximum rule set: 0'.
    That counter does not include the geometry offgrid table, so a layout with
    off-grid metal edges reported 0 there and 'Violated rules are' on the next
    line at the same time. Read the rule list instead: it is what run_drc.py
    exits non-zero on.
    """
    unexpected = set()
    for m in re.finditer(r"Violated rules are\s*:\s*(.+)", drc_out):
        for rule in re.findall(r"[A-Za-z][\w.]*", m.group(1)):
            if rule not in DRC_EXPECTED_VIOLATIONS:
                unexpected.add(rule)
    return (not unexpected), unexpected


# KLayout writes device parameters in engineering notation ('w=4u', and
# '3.33u' with the trailing zero dropped), so the values have to be scaled
# before they can be compared with the drawn dimensions.
SI_SUFFIX = {"": 1.0, "f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6,
             "m": 1e-3, "k": 1e3, "K": 1e3, "M": 1e6, "G": 1e9}


def _extracted_device(cir_path):
    """Parse the extracted cap_cmomf line.

    Returns (two_terminal, w_um, l_um). w_um/l_um are None when the device is
    absent or its parameters could not be read.
    """
    if not os.path.isfile(cir_path):
        return False, None, None
    for line in open(cir_path):
        if "cap_cmomf" in line and " w=" in line:
            toks = line.split()
            # <inst> <n1> <n2> cap_cmomf w=... l=... : nodes are toks[1], toks[2]
            if len(toks) < 4 or toks[1] == toks[2]:
                continue
            dims = {}
            for key in ("w", "l"):
                m = re.search(r"\b" + key + r"=([0-9.eE+-]+)([a-zA-Z]?)", line)
                if m:
                    dims[key] = (float(m.group(1))
                                 * SI_SUFFIX.get(m.group(2), 1.0) * 1e6)
            return True, dims.get("w"), dims.get("l")
    return False, None, None


def _label_c_ff(gds_path):
    """Read the 'cap_cmomf C=<x>fF' label the PCell paints on TEXT (63/0)."""
    import subprocess
    reader = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "cap_cmomf_sweep.py")
    env = dict(os.environ)
    env["CAP_CMOMF_LABEL_IN"] = gds_path
    p = subprocess.run(["klayout", "-zz", "-r", reader],
                       env=env, capture_output=True, text=True)
    m = re.search(r"cap_cmomf C=([0-9.]+)fF", p.stdout)
    return float(m.group(1)) if m else None


def _print_label():
    """KLayout-side: print every TEXT label of the given GDS."""
    import pya
    layout = pya.Layout()
    layout.read(os.environ["CAP_CMOMF_LABEL_IN"])
    li = layout.layer(63, 0)
    for cell in layout.each_cell():
        for shape in cell.shapes(li).each():
            if shape.is_text():
                print(shape.text.string)


def _orchestrate():
    import subprocess
    args = sys.argv[1:]
    run_dir = None
    if "--run_dir" in args:
        run_dir = args[args.index("--run_dir") + 1]
    if not run_dir:
        run_dir = os.path.join(os.getcwd(), "cap_cmomf_sweep_run")
    os.makedirs(run_dir, exist_ok=True)

    env = dict(os.environ)
    # Prepend, never setdefault: a machine that already exports KLAYOUT_PATH
    # (a local PDK install does) would otherwise silently resolve SG13_dev to
    # that tree instead of this worktree, and every configuration comes back
    # GEN-FAIL for a device that is perfectly fine here.
    env["KLAYOUT_PATH"] = os.pathsep.join(
        [KLAYOUT_DIR] + [p for p in [os.environ.get("KLAYOUT_PATH")] if p])

    results = []
    for name, params in CONFIGS:
        gds = os.path.join(run_dir, name + ".gds")
        cfg = {"name": name, "params": params}

        genenv = dict(env)
        genenv["CAP_CMOMF_CFG"] = json.dumps(cfg)
        genenv["CAP_CMOMF_OUT"] = gds
        gen = subprocess.run(["klayout", "-zz", "-r", os.path.abspath(__file__)],
                             env=genenv, capture_output=True, text=True)
        if not os.path.isfile(gds):
            # Say why. Swallowing this is what turns "the technology resolved
            # to the wrong tree" into a bare GEN-FAIL with no diagnostic.
            print(f"[{name}] generation failed:")
            print((gen.stdout + gen.stderr).strip() or "(no output)")
            results.append((name, "GEN-FAIL", "-", "-", "-", "-"))
            continue

        drc_dir = os.path.join(run_dir, name + "_drc")
        rc, drc_out = _run([sys.executable, DRC_RUNNER, "--path", gds,
                            "--topcell", name, "--run_dir", drc_dir])
        drc_ok, drc_unexpected = _drc_clean(drc_out)
        if not drc_ok:
            print(f"[{name}] unexpected DRC violations: "
                  f"{', '.join(sorted(drc_unexpected))}")

        lvs_dir = os.path.join(run_dir, name + "_lvs")
        _run([sys.executable, LVS_RUNNER, "--layout", gds, "--topcell", name,
              "--net_only", "--run_dir", lvs_dir])
        cir = os.path.join(lvs_dir, name + "_extracted.cir")
        dev, got_w, got_l = _extracted_device(cir)

        # Compare against the SNAPPED dimensions: the PCell draws on the 5 nm
        # grid, so an off-grid config extracts the snapped value, not the drawn
        # one. 1 nm of tolerance covers the printed precision.
        want_w, want_l = _gridfix(params["w"] * 1e6), _gridfix(params["l"] * 1e6)
        wl_ok = (got_w is not None and got_l is not None
                 and abs(got_w - want_w) < 1e-3 and abs(got_l - want_l) < 1e-3)
        if dev and not wl_ok:
            print(f"[{name}] extracted w/l is {got_w}/{got_l} um, "
                  f"expected {want_w}/{want_l} (w and l swapped?)")

        want = expected_c_ff(params)
        got = _label_c_ff(gds)
        # The label is printed to 3 decimals, so compare at that resolution.
        c_ok = got is not None and abs(got - want) < 1e-3

        status = "PASS" if (drc_ok and dev and wl_ok and c_ok) else "FAIL"
        results.append((name, status,
                        "clean" if drc_ok else "VIOL",
                        "2T" if dev else "NO-DEV",
                        "ok" if wl_ok else "BAD",
                        "{:.3f}".format(got) if got is not None else "none"))

    print("\n=== cap_cmomf PCell sweep ===")
    print(f"{'config':12s} {'status':8s} {'geoDRC':8s} {'extract':8s} "
          f"{'w/l':5s} {'C label/fF':>10s}")
    failed = 0
    for name, status, drc, dev, wl, cval in results:
        if status != "PASS":
            failed += 1
        print(f"{name:12s} {status:8s} {drc:8s} {dev:8s} {wl:5s} {cval:>10s}")
    print(f"\n{len(results) - failed}/{len(results)} configurations passed.")
    return 0 if failed == 0 else 1


if os.environ.get("CAP_CMOMF_LABEL_IN"):
    _print_label()
elif os.environ.get("CAP_CMOMF_CFG"):
    _generate_one()
else:
    sys.exit(_orchestrate())
