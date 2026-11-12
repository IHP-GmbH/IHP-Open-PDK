#!/usr/bin/env python3
# =========================================================================================
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
# =========================================================================================

"""
Check the de-embedded S-parameters (S_deemb) of the HBT measurement files (no simulation).

For every HBT test-structure folder and every spar_* file:
  1. copies: is its S_deemb identical to another file's of the same folder?
  2. where the folder has OPEN and SHORT dummies: open-short de-embed the file's raw S with
     them (models_verifier/sp_runner/deembed.py) and compare with IC-CAP's S_deemb, as the
     largest |Y_recomputed - Y_file| relative to the largest |Y_file| over all bias points.
     A genuine file agrees to ~1e-6; a copied S_deemb does not.
Writes a Markdown table and exits 1 when a file is neither in agreement nor a known case:
the known copies are the ones the configs handle (sparam_copied_deemb / sparam_self_deembed).

    python3 tools/check_hbt_deembedding.py --meas ../../../../libs.doc/meas/HBT --out <file.md>
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models_verifier.mdm_processing.sparam_parser import SparamParseError, parse_sparam_mdm  # noqa: E402
from models_verifier.models_verifier import read_config  # noqa: E402
from models_verifier.sp_runner.deembed import dummy_y, open_short  # noqa: E402
from models_verifier.sp_runner.extract import s_to_y  # noqa: E402

# Agreement limit of the recomputed de-embedding (relative to the largest |Y| of the file).
TOLERANCE = 1e-4


def known_copies(configs_dir: Path) -> dict:
    """{folder name: stems the configs treat as copies (sparam_copied_deemb + sparam_self_deembed)}."""
    known: dict = {}
    for path in sorted(configs_dir.glob("hbt/**/*.yaml")):
        cfg = read_config(path)
        folder = Path(cfg["mdm_dir"]).name
        stems = set(cfg.get("sparam_copied_deemb") or []) | set(cfg.get("sparam_self_deembed") or {})
        known.setdefault(folder, set()).update(stems)
    return known


def s_deemb(path: Path):
    """The file's parsed S_deemb data, or None when it has no S_deemb."""
    try:
        return parse_sparam_mdm(path, s_column="S_deemb")
    except SparamParseError:
        return None


def check_folder(folder: Path, known: set) -> list:
    """One row per spar_* file: (file, copy of, recomputed deviation, verdict)."""
    files = sorted(folder.glob("spar_*.mdm"))
    deemb = {f: s_deemb(f) for f in files}
    copies = {f: [] for f in files}
    for a, b in itertools.combinations(files, 2):
        da, db = deemb[a], deemb[b]
        if da is None or db is None or len(da.bias_points) != len(db.bias_points):
            continue
        if all(np.array_equal(x.s, y.s) for x, y in zip(da.bias_points, db.bias_points)):
            copies[a].append(b.stem)
            copies[b].append(a.stem)

    opens, shorts = sorted(folder.glob("dummy_open*.mdm")), sorted(folder.glob("dummy_short*.mdm"))
    rows = []
    for f in files:
        dev = None
        if deemb[f] is not None and opens and shorts:
            raw = parse_sparam_mdm(f, s_column="S").bias_points
            y_open, y_short = dummy_y(opens[0], raw[0].freq), dummy_y(shorts[0], raw[0].freq)
            diff, scale = 0.0, 0.0
            for r, d in zip(raw, deemb[f].bias_points):
                y_file = s_to_y(d.freq, d.s)
                y_new = open_short(s_to_y(r.freq, r.s), y_open, y_short)
                diff = max(diff, float(np.max(np.abs(y_new - y_file))))
                scale = max(scale, float(np.max(np.abs(y_file))))
            dev = diff / scale
        # A file identical to a known copy is the copy's source: fine. Any other identity is not.
        unexplained = [c for c in copies[f] if c not in known]
        if deemb[f] is None:
            verdict = "no S_deemb (raw S only)"
        elif f.stem in known:
            verdict = "declared copy (sparam_copied_deemb / sparam_self_deembed)"
        elif unexplained:
            verdict = "COPY (not handled in a config)"
        elif dev is None:
            verdict = "not checked (no OPEN/SHORT dummies in the folder)"
        elif dev > TOLERANCE:
            verdict = "MISMATCH"
        else:
            verdict = "ok"
        rows.append((f.stem, ", ".join(copies[f]), dev, verdict))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--meas", type=Path, default=Path("../../../../libs.doc/meas/HBT"))
    parser.add_argument("--configs", type=Path, default=Path("configs"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    known = known_copies(args.configs)
    lines = ["# HBT S-parameter de-embedding check", "",
             f"Recomputed open-short de-embedding vs IC-CAP S_deemb (relative max |dY|; ok below {TOLERANCE:g}).", "",
             "| folder | file | S_deemb identical to | recomputed deviation | verdict |", "|---|---|---|--:|---|"]
    bad = 0
    for folder in sorted(p for p in args.meas.glob("npn13g2*_T0*") if p.is_dir()):
        for stem, copy_of, dev, verdict in check_folder(folder, known.get(folder.name, set())):
            dev_text = "-" if dev is None else f"{dev:.1e}"
            lines.append(f"| {folder.name} | {stem} | {copy_of or '-'} | {dev_text} | {verdict} |")
            bad += verdict.startswith(("COPY", "MISMATCH"))
    checked = sum(1 for ln in lines if ln.startswith("| npn13g2"))
    lines += ["", f"Files checked: {checked}. Files needing attention: {bad}."]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    if not checked:
        print(f"no HBT S-parameter folder found under {args.meas}", file=sys.stderr)
        return 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
