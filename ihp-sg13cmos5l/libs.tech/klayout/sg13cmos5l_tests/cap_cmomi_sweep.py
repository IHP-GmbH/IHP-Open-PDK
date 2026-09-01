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
# cap_cmomi PCell DRC + LVS sweep.
#
# Generates a matrix of cap_cmomi configurations from the SG13_dev PyCell library
# and checks each one:
#   - the PCell instantiates and writes a GDS,
#   - geometric DRC reports no rule the device itself is responsible for,
#   - for the complete 2-terminal feeds ('double', 'same') the LVS extractor
#     recognises a cap_cmomi device with two distinct terminal nets.
# 'none' is a layout-only bare array, so only generation + DRC are asserted.
#
# Dual mode (single file):
#   - run under KLayout (pya available) with CAP_MOM_CFG/CAP_MOM_OUT set: emits
#     one config's GDS. This is how the orchestrator generates each layout.
#   - run as plain python3: orchestrates the whole sweep and exits non-zero on
#     any failure (CI friendly).
#
# Usage:
#   KLAYOUT_PATH=<libs.tech/klayout> python3 cap_cmomi_sweep.py [--run_dir DIR]
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

# Rules that fire on any bare device cell because the surroundings are absent:
# an isolated capacitor has no Activ, no GatPoly and no TopMetal1 anywhere, so
# the global density rules have nothing to measure. Anything outside this set
# is a real violation of the device itself.
DRC_EXPECTED_VIOLATIONS = {
    "AFil.g", "GFil.g", "TM1.c", "M1.j", "M2.j", "M3.j", "M4.j",
}

# name -> pcell params. 'two_terminal' marks feeds that must extract as a cap.
CONFIGS = [
    ("dbl_5x5_n4",  {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 4, "feed": "double"}, True),
    ("dbl_5x5_n3",  {"w": 5e-6,  "l": 5e-6,  "mmin": 2, "mmax": 4, "feed": "double"}, True),
    ("dbl_min",     {"w": 2e-6,  "l": 2e-6,  "mmin": 1, "mmax": 4, "feed": "double"}, True),
    ("dbl_big",     {"w": 15e-6, "l": 15e-6, "mmin": 1, "mmax": 4, "feed": "double"}, True),
    ("dbl_sub",     {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 4, "feed": "double", "subblock": 1}, True),
    ("same_5x5_n4", {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 4, "feed": "same"},   True),
    ("same_5x5_n3", {"w": 5e-6,  "l": 5e-6,  "mmin": 2, "mmax": 4, "feed": "same"},   True),
    ("same_n2",     {"w": 5e-6,  "l": 5e-6,  "mmin": 3, "mmax": 4, "feed": "same"},   True),
    ("same_min",    {"w": 2e-6,  "l": 2e-6,  "mmin": 1, "mmax": 4, "feed": "same"},   True),
    ("none_5x5",    {"w": 5e-6,  "l": 5e-6,  "mmin": 1, "mmax": 4, "feed": "none"},   False),
]


def _generate_one():
    """KLayout-side: emit CAP_MOM_CFG to CAP_MOM_OUT as a flat GDS."""
    import pya
    cfg = json.loads(os.environ["CAP_MOM_CFG"])
    out = os.environ["CAP_MOM_OUT"]
    layout = pya.Layout()
    layout.technology_name = TECH_NAME
    cell = layout.create_cell("cap_cmomi", "SG13_dev", cfg["params"])
    if cell is None:
        raise SystemExit("cap_cmomi PCell not found in SG13_dev library")
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

    The old check grepped 'Number of DRC errors for maximum rule set: 0'. That
    counter does not include the geometry offgrid table, so a layout with
    off-grid metal edges reported 0 there and 'Violated rules are' on the next
    line at the same time. Read the rule list instead: it is what run_drc.py
    exits non-zero on. Kept identical to cap_cmomf_sweep.py, where the weaker
    check hid two real defects.
    """
    unexpected = set()
    for m in re.finditer(r"Violated rules are\s*:\s*(.+)", drc_out):
        for rule in re.findall(r"[A-Za-z][\w.]*", m.group(1)):
            if rule not in DRC_EXPECTED_VIOLATIONS:
                unexpected.add(rule)
    return (not unexpected), unexpected


def _rm(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def _extracted_two_terminal(cir_path):
    """True if the extracted netlist has a cap_cmomi device with 2 distinct nets."""
    if not os.path.isfile(cir_path):
        return False
    for line in open(cir_path):
        if "cap_cmomi" in line and " w=" in line:
            toks = line.split()
            # <inst> <n1> <n2> cap_cmomi w=... : nodes are toks[1], toks[2]
            if len(toks) >= 4 and toks[1] != toks[2]:
                return True
    return False


def _orchestrate():
    import subprocess
    args = sys.argv[1:]
    run_dir = None
    if "--run_dir" in args:
        run_dir = args[args.index("--run_dir") + 1]
    if not run_dir:
        run_dir = os.path.join(os.getcwd(), "cap_cmomi_sweep_run")
    os.makedirs(run_dir, exist_ok=True)

    env = dict(os.environ)
    # Prepend, never setdefault: on a machine that already exports
    # KLAYOUT_PATH (a local PDK install does) the technology would resolve to
    # that tree instead of this one and every configuration comes back
    # GEN-FAIL for a device that is fine here.
    env["KLAYOUT_PATH"] = os.pathsep.join(
        [KLAYOUT_DIR] + [p for p in [os.environ.get("KLAYOUT_PATH")] if p])

    results = []
    for name, params, two_terminal in CONFIGS:
        gds = os.path.join(run_dir, name + ".gds")
        cfg = {"name": name, "params": params}

        # Both artifacts this loop judges are read back off disk, so a file left
        # by an earlier run into the same directory would be read as this run's
        # result. Delete them first, and believe the runners' exit codes rather
        # than the presence of a file.
        _rm(gds)
        genenv = dict(env)
        genenv["CAP_MOM_CFG"] = json.dumps(cfg)
        genenv["CAP_MOM_OUT"] = gds
        gen = subprocess.run(["klayout", "-zz", "-r", os.path.abspath(__file__)],
                             env=genenv, capture_output=True, text=True)
        if gen.returncode != 0 or not os.path.isfile(gds):
            results.append((name, "GEN-FAIL", "-", "-"))
            continue

        drc_dir = os.path.join(run_dir, name + "_drc")
        # The DRC exit code is deliberately not the verdict: a bare PCell with
        # no chip context always trips the density and fill rules, so the runner
        # exits non-zero on every config. _drc_clean reads the violated-rules
        # list from stdout and passes as long as none is outside the expected
        # set, so it cannot go stale on a leftover file either.
        _, drc_out = _run([sys.executable, DRC_RUNNER, "--path", gds,
                           "--topcell", name, "--run_dir", drc_dir])
        drc_ok, drc_unexpected = _drc_clean(drc_out)
        if not drc_ok:
            print(f"[{name}] unexpected DRC violations: "
                  f"{', '.join(sorted(drc_unexpected))}")

        lvs_dir = os.path.join(run_dir, name + "_lvs")
        cir = os.path.join(lvs_dir, name + "_extracted.cir")
        _rm(cir)
        rc, _ = _run([sys.executable, LVS_RUNNER, "--layout", gds,
                      "--topcell", name, "--net_only", "--run_dir", lvs_dir])
        if rc != 0:
            results.append((name, "LVS-FAIL", "clean" if drc_ok else "VIOL", "-"))
            continue
        dev = _extracted_two_terminal(cir)

        if two_terminal:
            status = "PASS" if (drc_ok and dev) else "FAIL"
        else:
            status = "PASS" if drc_ok else "FAIL"
        results.append((name, status, "clean" if drc_ok else "VIOL",
                        "2T" if dev else "array"))

    print("\n=== cap_cmomi PCell sweep ===")
    print(f"{'config':14s} {'status':8s} {'geoDRC':8s} {'extract':8s}")
    failed = 0
    for name, status, drc, dev in results:
        if status != "PASS":
            failed += 1
        print(f"{name:14s} {status:8s} {drc:8s} {dev:8s}")
    print(f"\n{len(results) - failed}/{len(results)} configurations passed.")
    return 0 if failed == 0 else 1


if os.environ.get("CAP_MOM_CFG"):
    _generate_one()
else:
    sys.exit(_orchestrate())
