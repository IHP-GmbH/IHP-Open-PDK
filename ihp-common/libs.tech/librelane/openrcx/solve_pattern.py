#!/usr/bin/env python3
#==========================================================================
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
#==========================================================================
"""Solve one OpenRCX `gen_solver_patterns` pattern with FasterCap.

Reads the `wires` file of a pattern directory, builds the conductors
(ground planes and wires) as FasterCap panels in a uniform dielectric and
solves the pattern at two wire lengths. The difference of the two
capacitance matrices divided by the length difference removes the 3D end
effects of the finite wires; the result is scaled back to the pattern's
nominal wire length and written as `wires.log` in FasterCap's output
format, so OpenROAD's `fasterCapParse.py` can read it unchanged.

A uniform dielectric is used because the IHP SG13 stack is 4.1 +- 0.1
from Metal1 up to the passivation (the field oxide / ILD0 nitride below
Metal1 give an effective 4.11). Not modelled: the nitride passivation
above the top metal.

With --process, a `width_delta` entry in a CONDUCTOR block of the process
file (ignored by gen_solver_patterns) widens or narrows the wires of that
metal symmetrically; the tables stay keyed by drawn width and spacing.

Usage: solve_pattern.py <pattern_dir> [options]  (run from the $WORK dir,
the pattern path is written into the log and parsed for the pattern name)
"""

import argparse
import os
import subprocess
import sys
import time


def read_pattern(path):
    planes, wires, length = [], [], None
    for line in open(path):
        w = line.split()
        if not w:
            continue
        if w[0] == "GROUND_PLANE":
            # GROUND_PLANE <idx> <name> HEIGHT <bot> <top> THICKNESS <t>
            planes.append((w[2], float(w[4]), float(w[5])))
        elif w[0] == "WIRE":
            # WIRE <idx> <name> LL x y LR x y UR x y UL x y LENGTH l VOLTAGE v
            x0, y0 = float(w[4]), float(w[5])
            x1, y1 = float(w[10]), float(w[11])
            wires.append((w[2], x0, x1, y0, y1))
            length = float(w[16])
        elif w[0] == "WINDOW_BBOX":
            bbox = (float(w[2]), float(w[5]))
    return planes, wires, length, bbox


def read_width_deltas(path):
    """width_delta per metal index (1-based CONDUCTOR order)."""
    deltas = []
    for line in open(path):
        w = line.split()
        if w[:1] == ["CONDUCTOR"]:
            deltas.append(0.0)
        elif w[:1] == ["width_delta"] and deltas:
            deltas[-1] = float(w[1])
    return deltas


def box_panels(name, x0, x1, y0, y1, z0, z1):
    # six faces of a box, vertex order as in OpenROAD's
    # UniversalFormat2FasterCap converter: FasterCap's automatic mesh
    # refinement is sensitive to it, other orderings need ~50x more panels
    faces = [
        [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
        [(x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (x1, y0, z0)],
        [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)],
        [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)],
        [(x0, y0, z1), (x0, y1, z1), (x1, y1, z1), (x1, y0, z1)],
        [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
    ]
    return "".join(
        f"Q wire_{name} " + " ".join(f"{c:.6g}" for v in f for c in v) + "\n"
        for f in faces
    )


def write_geometry(pdir, tag, planes, wires, bbox, length, ext, eps,
                   deltas):
    lst = []
    for name, ybot, ytop in planes:
        f = f"plane_{name}_{tag}.txt"
        with open(os.path.join(pdir, f), "w") as fh:
            fh.write(box_panels(name, bbox[0] - ext, bbox[1] + ext,
                                ybot, ytop, -ext, length + ext))
        lst.append(f"C {f} {eps}e-06 0 0 0")
    for name, x0, x1, y0, y1 in wires:
        met = int(name[1:name.index("_")])  # M<met>_w<i>
        dw = deltas[met - 1] if met <= len(deltas) else 0.0
        f = f"wire_{name}_{tag}.txt"
        with open(os.path.join(pdir, f), "w") as fh:
            fh.write(box_panels(name, x0 - dw / 2, x1 + dw / 2, y0, y1,
                                0.0, length))
        lst.append(f"C {f} {eps}e-06 0 0 0")
    lstfile = os.path.join(pdir, f"wires_{tag}.lst")
    with open(lstfile, "w") as fh:
        fh.write("\n".join(lst) + "\n")
    return lstfile


def run_fastercap(exe, lstfile, accuracy, timeout):
    pdir = os.path.dirname(lstfile)
    log = lstfile[:-4] + ".log"
    with open(log, "w") as fh:
        try:
            subprocess.run([exe, "-b", os.path.basename(lstfile), "-g",
                            f"-a{accuracy}"], cwd=pdir, stdout=fh,
                           stderr=subprocess.STDOUT, timeout=timeout)
        except subprocess.TimeoutExpired:
            fh.write(f"\nKilled after {timeout} s\n")
    return parse_log(log)


def parse_log(log):
    """Return (names, matrix, frobenius, seconds) of the last complete
    iteration, or None if the run produced no complete matrix."""
    names, matrix, last, frob, secs = [], [], None, None, 0
    rows_left = 0
    for line in open(log):
        w = line.split()
        if line.startswith("Dimension"):
            rows_left = int(w[1])
            names, matrix = [], []
        elif rows_left:
            names.append(w[0])
            matrix.append([float(v) for v in w[1:]])
            rows_left -= 1
        elif line.startswith("Weighted Frobenius"):
            last, frob = (names, matrix), float(w[-1])
        elif line.startswith("Total time"):
            secs = float(w[2].rstrip("s"))
    if last is None:
        return None
    return last[0], last[1], frob, secs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pattern", help="pattern directory (relative to cwd)")
    ap.add_argument("--fastercap", default="FasterCap")
    ap.add_argument("--process", help="process file, for width_delta")
    ap.add_argument("--eps", type=float, default=4.1,
                    help="relative permittivity of the uniform dielectric")
    ap.add_argument("--ext", type=float, default=20.0,
                    help="ground plane extension beyond the window (um)")
    ap.add_argument("--len1", type=float, default=10.0,
                    help="shorter wire length (um)")
    ap.add_argument("--len2", type=float, default=20.0,
                    help="longer wire length (um)")
    ap.add_argument("--accuracy", type=float, default=0.01)
    ap.add_argument("--timeout", type=float, default=600.0,
                    help="seconds per FasterCap run")
    a = ap.parse_args()

    pdir = a.pattern.rstrip("/")
    planes, wires, nominal, bbox = read_pattern(os.path.join(pdir, "wires"))
    deltas = read_width_deltas(a.process) if a.process else []
    t0 = time.time()
    results = []
    for tag, length in (("L1", a.len1), ("L2", a.len2)):
        lst = write_geometry(pdir, tag, planes, wires, bbox, length,
                             a.ext, a.eps, deltas)
        r = run_fastercap(a.fastercap, lst, a.accuracy, a.timeout)
        if r is None:
            sys.exit(f"{pdir}: no complete FasterCap iteration for {tag}")
        results.append(r)
    (names, m1, f1, s1), (_, m2, f2, s2) = results

    # per-length capacitance without end effects, scaled to the nominal
    # length the parser normalizes with
    scale = nominal / (a.len2 - a.len1)
    m = [[(b - c) * scale for b, c in zip(r2, r1)] for r1, r2 in zip(m1, m2)]

    with open(os.path.join(pdir, "wires.log"), "w") as fh:
        fh.write("FasterCap via solve_pattern.py: uniform dielectric "
                 f"eps={a.eps}, lengths {a.len1}/{a.len2} um, "
                 f"scaled to {nominal} um\n")
        fh.write(f"Input file: {pdir}/wires.lst\n")
        fh.write("Iteration number #1\n")
        fh.write("Capacitance matrix is:\n")
        fh.write(f"Dimension {len(m)} x {len(m)}\n")
        for n, row in zip(names, m):
            fh.write(n + "  " + " ".join(f"{v:.6g}" for v in row) + "\n")
        fh.write("Weighted Frobenius norm of the difference between "
                 f"capacitance (auto option): {max(f1, f2):.6g}\n")
        fh.write("Total allocated memory: 0 kilobytes\n")
        fh.write(f"Total time: {time.time() - t0:.6f}s\n")
    print(f"{pdir}: {s1 + s2:.0f} s solver, frobenius {f1:.3g} {f2:.3g}")


if __name__ == "__main__":
    main()
