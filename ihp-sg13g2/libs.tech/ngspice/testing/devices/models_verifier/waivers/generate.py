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
Auto-waive generator: turn the "Failed (new)" rows of a FINISHED run into schema-2 exceptions
(see waivers/waiver.py). It reads the run's reports and does not simulate anything.

    python -m models_verifier.waivers.generate --config <device yaml> [--tier dc|sparam|cv]

Inputs, in <results> = the config's output_dir under $RESULTS_ROOT (plus "sparam" / "cv"):
    final_reports/full_results.csv     one row per curve x metric x target, with its status and
                                       the fingerprint of its failing points (points_sha256)
    final_reports/failed_results.csv   every failing point (for the worst point of each record)
    final_reports/simulation_errors.csv blocks that could not be simulated: must be empty
    toolchain.txt                      the toolchain that produced the run
Output: <waivers_dir>/<device_name>.yaml, where waivers_dir is the config's `waivers_dir`
(dc), `sparam_waivers_dir` or `cv_waivers_dir`.

Rules
    - Every "Failed (new)" row gets a record for the run's toolchain (rows already recorded
      exactly are skipped). A new entry is "auto-waived"; its first_waived date is today, or the
      date of the old schema-1 entry. "Failed (not simulated)" rows are errors, never recorded.
    - Existing entries and the records of other toolchains are kept; nothing is dropped. (A
      run lists exceptions whose row now passes in final_reports/stale_exceptions.csv.)
    - An entry the reviewer rejected is not touched: its row keeps failing.
    - An approved entry whose values changed, or that gets a record for a new toolchain, goes
      back to "auto-waived", because those values have not been reviewed. The generator never
      sets "approved".
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict

import pandas as pd

from models_verifier.models_verifier import read_config, resolve_output_dir
from models_verifier.run_record import UNREGISTERED, read_toolchain_txt
from models_verifier.waivers.waiver import (
    APPROVED,
    AUTO_WAIVED,
    FAILED_NEW,
    REJECTED,
    WAIVED_STATUSES,
    ExceptionStore,
    curve_key,
    index_failing_points,
    toolchain_record,
)

# tier -> (results subfolder, config key of the exception folder, its default)
TIERS = {
    "dc": ("", "waivers_dir", "waivers"),
    "sparam": ("sparam", "sparam_waivers_dir", "waivers/sparam"),
    "cv": ("cv", "cv_waivers_dir", "waivers/cv"),
}

DEFAULT_REASON = "auto-waived from a run, pending review"
DOCUMENTATION = "every failing point: final_reports/failed_results.csv of the run; figures: make plot-<case>"


def update_exceptions(store: ExceptionStore, full_res: pd.DataFrame, failures: pd.DataFrame,
                      toolchain: str, today: str, reason: str = DEFAULT_REASON) -> Dict[str, int]:
    """Add or refresh the record of `toolchain` for every "Failed (new)" row (rules in the module doc)."""
    points = index_failing_points(failures)
    counts: Counter = Counter()
    for row in full_res[full_res["status"] == FAILED_NEW].itertuples(index=False):
        key = curve_key(getattr(row, "input_data", None), getattr(row, "block_index", None),
                        row.metric, row.target)
        fingerprint = str(row.points_sha256)
        if store.status_of(key, toolchain, row.n_points, row.n_out_of_bounds, fingerprint) in WAIVED_STATUSES:
            counts["already recorded"] += 1      # e.g. the generator run twice on the same run
            continue
        entry = store.entries.get(key)
        if entry is None:
            input_data, block_index, metric, target = key
            entry = store.entries[key] = {
                "curve": {"input_data": input_data,
                          "block_index": int(block_index) if block_index.isdigit() else block_index,
                          "metric": metric, "target": target},
                "status": AUTO_WAIVED,
                "reason": reason,
                "first_waived": store.legacy_dates.get(key) or today,
                "documentation": DOCUMENTATION,
                "toolchains": {},
            }
            counts["added"] += 1
        elif entry.get("status") == REJECTED:
            counts["rejected, left failing"] += 1
            continue
        else:
            if entry.get("status") == APPROVED:
                change = "values changed on" if toolchain in (entry.get("toolchains") or {}) else "new toolchain"
                entry["status"] = AUTO_WAIVED
                # the reviewer's reason stays; the withdrawal is noted next to it
                entry["withdrawn"] = f"{change} {toolchain} ({today}): approval needs renewal"
                counts["approval withdrawn"] += 1
            counts["updated"] += 1
        records = entry.get("toolchains") or {}
        records[toolchain] = toolchain_record(row.n_points, row.n_out_of_bounds, fingerprint,
                                              points.get(key, []), store.sig_digits)
        entry["toolchains"] = dict(sorted(records.items()))
    return dict(counts)


def results_dir_of(config: dict, tier: str) -> Path:
    """Where the run of this config and tier wrote its reports."""
    subdir = TIERS[tier][0]
    base = resolve_output_dir(config["output_dir"])
    return base / subdir if subdir else base


def waive_run(config_path: Path, tier: str = "dc", reason: str = DEFAULT_REASON) -> Path:
    """Update the exception file of one device from its finished run; return the file path."""
    config = read_config(Path(config_path))
    results = results_dir_of(config, tier)
    reports = results / "final_reports"
    if not (reports / "full_results.csv").exists() or not (results / "toolchain.txt").exists():
        raise SystemExit(f"No finished run in {results}: run `make test-<case>` first.")
    if len(pd.read_csv(reports / "simulation_errors.csv")):
        raise SystemExit(f"{results} has simulation errors (final_reports/simulation_errors.csv): "
                         "fix them; failures of an incomplete run are never recorded.")

    run = read_toolchain_txt(results)
    device = config["device_name"]
    if run.get("device") != device:
        raise SystemExit(f"{results}/toolchain.txt is for device '{run.get('device')}', not '{device}'.")
    toolchain = run["exception_key"]
    if toolchain == UNREGISTERED:
        raise SystemExit(f"{results} was not run through a registered toolchain (make ... TOOLCHAIN=<id>).")

    _subdir, dir_key, default_dir = TIERS[tier]
    store = ExceptionStore.load(device, Path(config.get(dir_key) or default_dir))
    # File names stay text ("007" is not 7); floats are read back exactly (round trip).
    read = dict(dtype={"input_data": str, "points_sha256": str}, float_precision="round_trip")
    full_res = pd.read_csv(reports / "full_results.csv", **read)
    failed_path = reports / "failed_results.csv"
    failures = pd.read_csv(failed_path, **read) if failed_path.exists() else pd.DataFrame()

    counts = update_exceptions(store, full_res, failures, toolchain, date.today().isoformat(), reason)
    path = store.save()
    logging.info("%s (%s, toolchain %s): %s -> %d exception(s) in %s",
                 device, tier, toolchain, counts or "nothing to add", len(store), path)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="models_verifier.waivers.generate",
        description="Write the new failures of a finished run into the device's exception file.",
    )
    parser.add_argument("--config", "-c", type=Path, required=True, help="Device config YAML.")
    parser.add_argument("--tier", choices=sorted(TIERS), default="dc", help="Which run: dc (default), sparam or cv.")
    parser.add_argument("--reason", default=DEFAULT_REASON, help="Reason written into NEW entries.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    waive_run(args.config, args.tier, args.reason)
    return 0


if __name__ == "__main__":
    sys.exit(main())
