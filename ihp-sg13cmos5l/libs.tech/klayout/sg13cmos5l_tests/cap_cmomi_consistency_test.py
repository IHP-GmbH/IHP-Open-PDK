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
# cap_cmomi cross-artifact consistency test.
#
# The capacitance of this device is written down in several places that nothing
# keeps in step: the Verilog-A source, the OSDI binary built from it (tracked,
# with no build rule that reruns on a source change), the PCell's C= label, the
# xschem symbol's tcleval expression, and the gnucap and ngspice reference
# outputs.  Edit the coefficients and any one of them can be left behind
# silently.
#
# Every artifact is asked for the capacitance of the same device and compared
# against the OSDI under ngspice, which is the object a designer's simulation
# actually runs.  The reference side is never a re-implementation of the
# formula: the symbol expression is evaluated by tclsh exactly as xschem would,
# and the stored reference outputs are read back through the same high-pass
# relation their testbench uses.
#
# This test is deliberately blind to whether the formula is right.  It only
# says whether every copy of it agrees.  cap_cmomi_geometry_test.py is the one
# that checks the formula against the drawn cell.
#
# Usage:
#   python3 cap_cmomi_consistency_test.py [--run_dir DIR]
#
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KLAYOUT_DIR = os.path.dirname(HERE)                       # libs.tech/klayout
PDK_ROOT = os.path.dirname(os.path.dirname(KLAYOUT_DIR))  # <pdk>
LIBS_TECH = os.path.join(PDK_ROOT, "libs.tech")
OSDI = os.path.join(LIBS_TECH, "ngspice", "osdi", "cap_cmomi.osdi")
SYMS = [os.path.join(LIBS_TECH, "xschem", d, "cap_cmomi.sym")
        for d in ("sg13cmos5l_pr", "sg13g2_pr")]
GNUCAP_REF = os.path.join(LIBS_TECH, "gnucap", "tests", "gnucap", "capacitor",
                          "ref", "tb_cap_cmomi_typ.gc.out")
NGSPICE_REF = os.path.join(LIBS_TECH, "gnucap", "tests", "ngspice", "capacitor",
                           "ref", "tb_cap_cmomi_typ.sp.out")
TECH_NAME = "sg13cmos5l"
FMEAS = 1e6
FEED_CODE = {"none": 0, "same": 1, "double": 2}

# The device both stored reference outputs were taken on.
CANON = {"w": 5.0, "l": 5.0, "mmin": 1, "mmax": 4, "feed": "double"}
R_LOAD = 1e5          # the high-pass load resistor in both testbenches

# Configurations the PCell label and the symbol expression are checked on.
CASES = [
    {"w": 5.0,  "l": 5.0,  "mmin": 1, "mmax": 4, "feed": "double"},
    {"w": 2.0,  "l": 2.0,  "mmin": 1, "mmax": 4, "feed": "double"},
    {"w": 15.0, "l": 15.0, "mmin": 1, "mmax": 4, "feed": "double"},
    {"w": 5.0,  "l": 5.0,  "mmin": 2, "mmax": 4, "feed": "double"},
    {"w": 5.0,  "l": 5.0,  "mmin": 3, "mmax": 4, "feed": "double"},
    {"w": 8.9,  "l": 21.0, "mmin": 1, "mmax": 4, "feed": "double"},
    {"w": 5.0,  "l": 5.0,  "mmin": 1, "mmax": 4, "feed": "none"},
    {"w": 5.0,  "l": 5.0,  "mmin": 1, "mmax": 4, "feed": "same"},
    # Below w = 1.78 um the row clamp is the only thing setting the row count,
    # and the model and the layout used to disagree there. The PCell will not
    # draw it (w is constrained to [2:100] um and an out-of-range value falls
    # back to the default), so this case checks the model against the symbol
    # only: "pcell": False.
    {"w": 1.0,  "l": 2.0,  "mmin": 1, "mmax": 4, "feed": "same",
     "pcell": False},
]

TOL_REL = 1e-4        # exact artifacts: the same arithmetic, or nearly
TOL_ABS = 6e-4        # the PCell label is printed to 3 decimals of a fF
TOL_MEAS = 5e-3       # reference outputs go through a -3 dB corner measurement


def key(c):
    return f"w{c['w']}_l{c['l']}_m{c['mmin']}{c['mmax']}_{c['feed']}"


# ----------------------------------------------------------------- KLayout side

def _emit_labels():
    """Run inside KLayout: emit each case's PCell C= label as JSON."""
    import pya

    import sg13cmos5l_pycell_lib.ihp.cap_cmomi_code as pcell_mod
    src = os.path.realpath(pcell_mod.__file__)
    out_path = os.environ["CAP_CMOMI_LABEL_OUT"]
    if not src.startswith(os.path.realpath(PDK_ROOT) + os.sep):
        with open(out_path, "w") as f:
            json.dump({"error": f"PCell resolved to {src}, outside {PDK_ROOT}"}, f)
        return

    labels = {}
    for c in CASES:
        if not c.get("pcell", True):
            continue
        layout = pya.Layout()
        layout.technology_name = TECH_NAME
        cell = layout.create_cell("cap_cmomi", "SG13_dev",
                                  {"w": c["w"] * 1e-6, "l": c["l"] * 1e-6,
                                   "mmin": c["mmin"], "mmax": c["mmax"],
                                   "feed": c["feed"]})
        if cell is None:
            with open(out_path, "w") as f:
                json.dump({"error": "cap_cmomi PCell not found"}, f)
            return
        top = layout.create_cell("T")
        top.insert(pya.DCellInstArray(cell, pya.DTrans()))
        top.flatten(-1, True)
        found = None
        for li in layout.layer_indexes():
            for s in top.shapes(li).each():
                if s.is_text():
                    m = re.search(r"C=([-\d.eE+]+)fF", s.text.string)
                    if m:
                        found = float(m.group(1))
        labels[key(c)] = found
    with open(out_path, "w") as f:
        json.dump({"labels": labels}, f)


# -------------------------------------------------------------------- artifacts

def osdi_values(run_dir):
    """Capacitance of every case from the tracked OSDI, under ngspice."""
    lines = ["* cap_cmomi consistency reference", ".model cmom cap_cmomi"]
    for i, c in enumerate(CASES):
        lines += [f"N{i} p{i} 0 0 cmom w={c['w']}u l={c['l']}u mmin={c['mmin']} "
                  f"mmax={c['mmax']} feed={FEED_CODE[c['feed']]}",
                  f"V{i} p{i} 0 dc 0 ac 1"]
    lines.append(".end")
    tb = os.path.join(run_dir, "tb_cap_cmomi_consistency.sp")
    with open(tb, "w") as f:
        f.write("\n".join(lines) + "\n")

    cmds = [f"osdi {OSDI}", f"source {tb}", f"ac lin 1 {FMEAS} {FMEAS}"]
    for i in range(len(CASES)):
        cmds += [f"let c{i} = -imag(v{i}#branch)/({2 * math.pi}*{FMEAS})*1e15",
                 f"print c{i}"]
    cmds.append("quit")
    p = subprocess.run(["ngspice", "-p"], input="\n".join(cmds) + "\n",
                       capture_output=True, text=True, timeout=300)
    vals = {}
    for ln in p.stdout.splitlines():
        m = re.match(r"\s*c(\d+)\s*=\s*([-\d.eE+]+)", ln)
        if m:
            vals[key(CASES[int(m.group(1))])] = float(m.group(2))
    if len(vals) != len(CASES):
        sys.stderr.write(p.stdout[-2000:] + p.stderr[-1000:])
        raise SystemExit(f"ngspice returned {len(vals)}/{len(CASES)} points")
    return vals


def sym_values(sym_path):
    """Capacitance the xschem symbol would display, evaluated by tclsh.

    The tcleval body is handed to the same expr engine xschem uses, so this
    compares the shipped expression rather than a Python transcription of it.
    """
    text = open(sym_path).read()
    m = re.search(r"tcleval\(C=\[ev\s*\\\{(.*?)\\\}\]\)", text, re.S)
    if not m:
        return None
    expr = m.group(1)
    out = {}
    for c in CASES:
        e = expr
        # longest name first: substituting @m before @mmax would eat its prefix.
        # feed is a token, and xschem pastes it in bare, so it goes in unwrapped
        # and the symbol expression is the thing that has to quote it.
        e = e.replace("@feed", c["feed"])
        for name, val in (("@mmax", c["mmax"]), ("@mmin", c["mmin"]),
                          ("@m", 1), ("@w", c["w"] * 1e-6),
                          ("@l", c["l"] * 1e-6)):
            e = e.replace(name, f"({val})")
        p = subprocess.run(["tclsh"], input=f"puts [expr {{{e}}}]\n",
                           capture_output=True, text=True, timeout=60)
        if p.returncode != 0 or not p.stdout.strip():
            raise SystemExit(f"{sym_path}: tclsh could not evaluate the symbol "
                             f"expression: {p.stderr.strip() or 'no output'}")
        out[key(c)] = float(p.stdout.strip()) * 1e15
    return out


def gnucap_ref():
    """The capacitance printed by the stored gnucap reference run."""
    for ln in open(GNUCAP_REF):
        m = re.match(r"\s*C1=\s*([-\d.eE+]+)", ln)
        if m:
            return float(m.group(1)) * 1e15
    return None


def ngspice_ref():
    """Capacitance implied by the stored ngspice AC curve.

    Both testbenches are the same high-pass R-C, so |H| = wRC / sqrt(1+(wRC)^2)
    and the -3 dB crossing gives C = 1/(2*pi*f_3dB*R).  Interpolate the stored
    magnitudes for the crossing rather than trusting a single row.
    """
    pts = []
    for ln in open(NGSPICE_REF):
        t = ln.split()
        if len(t) == 2:
            try:
                pts.append((float(t[0]), float(t[1])))
            except ValueError:
                continue
    for (f0, m0), (f1, m1) in zip(pts, pts[1:]):
        if m0 <= 0.707 <= m1:
            f = f0 + (0.707 - m0) * (f1 - f0) / (m1 - m0)
            return 1.0 / (2 * math.pi * f * R_LOAD) * 1e15
    return None


# ------------------------------------------------------------------ orchestrate

def main():
    args = sys.argv[1:]
    run_dir = args[args.index("--run_dir") + 1] if "--run_dir" in args else \
        os.path.join(os.getcwd(), "cap_cmomi_consistency_run")
    os.makedirs(run_dir, exist_ok=True)

    env = dict(os.environ)
    env["KLAYOUT_PATH"] = KLAYOUT_DIR
    lbl_out = os.path.join(run_dir, "labels.json")
    env["CAP_CMOMI_LABEL_OUT"] = lbl_out
    if os.path.exists(lbl_out):
        os.remove(lbl_out)
    p = subprocess.run(["klayout", "-zz", "-r", os.path.abspath(__file__)],
                       env=env, capture_output=True, text=True)
    if not os.path.isfile(lbl_out):
        sys.stderr.write(f"KLayout produced no labels (exit {p.returncode})\n")
        sys.stderr.write(p.stdout + p.stderr)
        return 1
    got = json.load(open(lbl_out))
    if "error" in got:
        sys.stderr.write(got["error"] + "\n")
        return 1
    labels = got["labels"]

    ref = osdi_values(run_dir)
    bad = 0

    print("\n=== every artifact against the tracked OSDI, C in fF ===")
    print(f"{'case':28s} {'osdi':>9} {'PCell':>9} " +
          " ".join(f"{os.path.basename(os.path.dirname(s)):>16s}" for s in SYMS))
    syms = [(s, sym_values(s)) for s in SYMS]
    for c in CASES:
        k = key(c)
        row = [f"{k:28s}", f"{ref[k]:9.4f}"]
        lab = labels.get(k)
        drawn = c.get("pcell", True)
        ok = (not drawn) or (lab is not None and
                             (abs(lab - ref[k]) <= TOL_ABS or
                              abs(lab - ref[k]) <= TOL_REL * ref[k]))
        bad += 0 if ok else 1
        row.append(f"{lab:9.4f}" if lab is not None else
                   f"{'not drawn':>9}" if not drawn else f"{'none':>9}")
        for path, vals in syms:
            v = vals.get(k) if vals else None
            sok = v is not None and abs(v - ref[k]) <= TOL_REL * max(ref[k], 1e-9)
            bad += 0 if sok else 1
            row.append(f"{v:16.4f}" if v is not None else f"{'none':>16}")
        marks = "" if ok else "  <- PCell label differs"
        print(" ".join(row) + marks)

    print("\n=== stored reference outputs, on " + key(CANON) + " ===")
    cref = ref[key(CANON)]
    for name, val in (("gnucap ref", gnucap_ref()), ("ngspice ref", ngspice_ref())):
        if val is None:
            print(f"{name:12s} unreadable")
            bad += 1
            continue
        dev = (val - cref) / cref
        ok = abs(dev) <= TOL_MEAS
        bad += 0 if ok else 1
        print(f"{name:12s} {val:9.4f}  vs osdi {cref:9.4f}  "
              f"{dev * 100:+6.2f}%  {'ok' if ok else 'STALE'}")

    print(f"\n{'FAIL' if bad else 'PASS'}: {bad} mismatch(es)")
    return 1 if bad else 0


if os.environ.get("CAP_CMOMI_LABEL_OUT"):
    _emit_labels()
else:
    sys.exit(main())
