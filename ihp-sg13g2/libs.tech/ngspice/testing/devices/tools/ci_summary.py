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
Markdown summary of every verification run under a results folder (CI job summary or a local
check). A waiver means "reviewed", not "good": waived curves are counted as failures; the
column "new" (failures without an exactly matching exception, or not simulated) is what makes
a run exit 1. Counts are of the measured target (the verification result), except "new", which
counts both targets because either makes the run exit 1; the typical target (tt inside the ss..ff
band, a check of the model corners) has its own column. A run that started (toolchain.txt) but
wrote no reports is listed as "did not finish". Below the table:
every new failure and every exception whose curve is missing from the run, and the toolchain
record (ngspice version, OSDI hashes) of each run.

    python3 tools/ci_summary.py models_results/<toolchain> [--title "..."]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

MAX_LISTED = 50


def read_csv(path: Path) -> pd.DataFrame:
    """A report CSV (empty frame when it is missing or has no rows)."""
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    return pd.read_csv(path, dtype={"input_data": str})


def summarize(results_root: Path) -> list[str]:
    """One table row per run (case and tier) found under `results_root`, a totals row, then the
    new failures, the exceptions of missing curves and the toolchain records."""
    lines = ["| run | toolchain | curves | passed | failed | of which waived | new | tt failed | not judged "
             "| stale exceptions | simulation errors |",
             "|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    totals = [0] * 9
    new_rows, missing, records = [], [], []
    for full_path in sorted(results_root.rglob("final_reports/full_results.csv")):
        reports, run_dir = full_path.parent, full_path.parent.parent
        name = run_dir.relative_to(results_root).as_posix()
        full = read_csv(full_path)
        meas = full[full["target"] == "meas"]["status"].astype(str)
        tt = full[full["target"] == "tt"]["status"].astype(str)
        judged = meas.eq("Passed") | meas.str.startswith("Failed")
        stale = read_csv(reports / "stale_exceptions.csv")
        numbers = [int(judged.sum()), int(meas.eq("Passed").sum()), int(meas.str.startswith("Failed").sum()),
                   int(meas.str.startswith("Failed (waived").sum()),
                   int(full["status"].isin(["Failed (new)", "Failed (not simulated)"]).sum()),
                   int(tt.str.startswith("Failed").sum()), int((~judged).sum()),
                   len(stale), len(read_csv(reports / "simulation_errors.csv"))]
        record = {}
        if (run_dir / "toolchain.txt").exists():
            for ln in (run_dir / "toolchain.txt").read_text().splitlines():
                key, _, value = ln.partition(":")
                record.setdefault(key.strip(), []).append(value.strip())
            records.append((name, record))
        lines.append(f"| {name} | {record.get('toolchain', [''])[0]} | " + " | ".join(map(str, numbers)) + " |")
        totals = [t + n for t, n in zip(totals, numbers)]
        new = read_csv(reports / "new_failures.csv")
        new_rows += [f"- {name}: `{r.input_data}` block {r.block_index}, {r.metric} ({r.target}): {r.status}, "
                     f"{r.n_out_of_bounds} of {r.n_points} points out of band" for r in new.itertuples()]
        if "reason" in stale:
            missing += [f"- {name}: `{r.input_data}` block {r.block_index}, {r.metric} ({r.target})"
                        for r in stale.itertuples() if str(r.reason).startswith("curve not in this run")]
    for record_path in sorted(results_root.rglob("toolchain.txt")):
        run_dir = record_path.parent
        tiers = [run_dir] + [run_dir / t for t in ("cv", "sparam") if (run_dir / t).is_dir()]
        if not any((d / "final_reports" / "full_results.csv").exists() for d in tiers):
            lines.append(f"| {run_dir.relative_to(results_root).as_posix()} | did not finish (no reports) |"
                         + " |" * 9)
    lines.append("| **total** | | " + " | ".join(f"**{n}**" for n in totals) + " |")
    for title, items in (("New failures (make the job fail)", new_rows),
                         ("Exceptions whose curve is missing from the run (make the job fail)", missing)):
        if items:
            lines += ["", f"**{title}:** {len(items)}", ""] + items[:MAX_LISTED]
            if len(items) > MAX_LISTED:
                lines.append(f"- ... {len(items) - MAX_LISTED} more in the uploaded final_reports")
    if records:
        lines += ["", "**Toolchain records** (`toolchain.txt`, one line per distinct record):", ""]
        seen = {}
        for name, record in records:
            osdi = "; ".join(Path(o.split(" sha256=")[0]).name + " sha256=" + o.split(" sha256=")[-1]
                             for o in record.get("osdi", [])) or "no OSDI model"
            seen.setdefault(f"{record.get('ngspice_version', ['?'])[0].split(':')[0].strip()}; {osdi}", []).append(name)
        lines += [f"- {text} ({len(runs)} run(s))" for text, runs in seen.items()]
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("results_root", type=Path)
    parser.add_argument("--title", default="Verification summary")
    args = parser.parse_args()
    print(f"### {args.title}\n")
    print("Waived curves are counted as failures (a waiver means reviewed, not good). "
          "Curves of the measured target; \"tt failed\": typical target (model corner check).\n")
    print("\n".join(summarize(args.results_root)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
