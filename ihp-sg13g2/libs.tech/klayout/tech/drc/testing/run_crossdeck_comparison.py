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
Cross-deck DRC comparison: modular vs maximal.

For each unit test GDS file, runs both the maximal deck and the modular deck,
then compares violation counts per rule for all overlapping rules (rules that
exist in both decks).

Usage:
    python3 run_crossdeck_comparison.py [--table=<name>] [--mp=<num>] [--run_dir=<dir>]
"""

import argparse
import csv
import logging
import os
import re
import sys
import time
import traceback
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from subprocess import CalledProcessError, check_call

import concurrent.futures
import klayout.db


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TESTING_DIR = Path(__file__).resolve().parent
DRC_DIR = TESTING_DIR.parent
UNIT_TEST_DIR = TESTING_DIR / "testcases" / "unit"
MAXIMAL_DRC = DRC_DIR / "rule_decks" / "sg13g2_maximal.drc"

# GDS files to skip (they use standalone decks, not modular tables)
SKIP_GDS = {"antenna"}

# Comparison status codes
MATCH = "MATCH"
BOTH_CLEAN = "BOTH_CLEAN"
COUNT_MISMATCH = "COUNT_MISMATCH"
MODULAR_MISSING = "MODULAR_MISSING"
MAXIMAL_MISSING = "MAXIMAL_MISSING"


# ---------------------------------------------------------------------------
# XML Parsing (reused logic from run_regression.py / run_drc.py)
# ---------------------------------------------------------------------------

def parse_results_db(results_database):
    """Parse a KLayout .lyrdb file and return {rule_name: violation_count}.

    Rules that ran but had zero violations are included with count 0.
    """
    results_database = Path(results_database)
    if not results_database.is_file():
        logging.error(f"Results database not found: {results_database}")
        return {}

    tree = ET.parse(results_database)
    root = tree.getroot()

    rule_counts = defaultdict(int)

    # Categories (root[5]) list all rules that ran
    categories = root.find("categories")
    if categories is not None:
        for cat in categories:
            name_elem = cat.find("name")
            if name_elem is not None and name_elem.text:
                rule_counts[name_elem.text.strip()] = 0

    # Items (root[7]) list actual violations
    items = root.find("items")
    if items is not None:
        for item in items:
            cat_elem = item.find("category")
            if cat_elem is not None and cat_elem.text:
                rule_name = cat_elem.text.strip().replace("'", "")
                rule_counts[rule_name] += 1

    return dict(rule_counts)


# ---------------------------------------------------------------------------
# GDS -> Table mapping
# ---------------------------------------------------------------------------

def gds_to_table(gds_name):
    """Map a GDS filename (without extension) to a modular table name."""
    name = gds_name.lower()
    # metal2-5 -> metaln
    if re.match(r"^metal[2-5]$", name):
        return "metaln"
    # via2-4 -> vian
    if re.match(r"^via[2-4]$", name):
        return "vian"
    return name


def get_top_cell_names(gds_path):
    """Get top cell names from a GDS file."""
    layout = klayout.db.Layout()
    layout.read(str(gds_path))
    return [t.name for t in layout.top_cells()]


# ---------------------------------------------------------------------------
# DRC Runners
# ---------------------------------------------------------------------------

def run_maximal(gds_path, topcell, run_dir):
    """Run the maximal deck on a GDS file. Returns path to .lyrdb."""
    gds_name = Path(gds_path).stem
    report = run_dir / f"{gds_name}_{topcell}_maximal.lyrdb"
    log_file = run_dir / f"{gds_name}_{topcell}_maximal.log"

    cmd = (
        f"klayout -b -r '{MAXIMAL_DRC}' "
        f"-rd input='{gds_path}' "
        f"-rd topcell='{topcell}' "
        f"-rd report='{report}' "
        f"-rd run_mode='deep' "
        f"> '{log_file}' 2>&1"
    )

    try:
        check_call(cmd, shell=True)
    except CalledProcessError:
        # Non-zero exit is expected when violations are found
        pass

    if not report.exists():
        logging.error(f"Maximal run produced no report for {gds_name}/{topcell}")
        if log_file.exists():
            logging.error(f"Log: {log_file}")
        return None

    return report


def run_modular(gds_path, topcell, table_name, run_dir):
    """Run the modular deck via run_drc.py. Returns path to .lyrdb."""
    gds_name = Path(gds_path).stem
    output_dir = run_dir / f"{gds_name}_{topcell}_modular"
    log_file = run_dir / f"{gds_name}_{topcell}_modular.log"

    # Force the modular deck to use the same default JSON the maximal deck
    # relies on (values hardcoded in sg13g2_maximal.drc). Without this, the
    # orchestrator picks sg13g2_tech_mod.json (with post-#900 precedence),
    # whose values diverge from maximal and break count parity.
    default_json = DRC_DIR / "rule_decks" / "sg13g2_tech_default.json"
    cmd = (
        f"python3 '{DRC_DIR / 'run_drc.py'}' "
        f"--path='{gds_path}' "
        f"--table={table_name} "
        f"--topcell={topcell} "
        f"--drc_json='{default_json}' "
        f"--disable_extra_rules "
        f"--no_density "
        f"--run_dir='{output_dir}' "
        f"--run_mode=deep "
        f"> '{log_file}' 2>&1"
    )

    try:
        check_call(cmd, shell=True)
    except CalledProcessError:
        # Non-zero exit is expected when violations are found
        pass

    # Find the generated .lyrdb
    lyrdb_files = list(output_dir.rglob("*.lyrdb"))
    if not lyrdb_files:
        logging.error(f"No .lyrdb generated for modular run: {gds_name}/{table_name}")
        return None

    return lyrdb_files[0]


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------

def compare_rules(maximal_counts, modular_counts):
    """Compare two rule count dicts. Returns list of (rule, max_count, mod_count, status)."""
    all_rules = set(maximal_counts.keys()) | set(modular_counts.keys())
    results = []

    for rule in sorted(all_rules):
        max_c = maximal_counts.get(rule, -1)
        mod_c = modular_counts.get(rule, -1)

        # Only compare overlapping rules (present in both decks)
        in_maximal = max_c >= 0
        in_modular = mod_c >= 0

        if not in_maximal and not in_modular:
            continue

        if in_maximal and not in_modular:
            # Rule only in maximal deck -- expected for rules not yet ported
            if max_c > 0:
                status = MAXIMAL_MISSING
            else:
                status = BOTH_CLEAN
            results.append((rule, max_c, -1, "MAXIMAL_ONLY"))
            continue

        if in_modular and not in_maximal:
            # Rule only in modular deck (precheck-only or modular extras)
            results.append((rule, -1, mod_c, "MODULAR_ONLY"))
            continue

        # Rule in both decks
        if max_c == 0 and mod_c == 0:
            status = BOTH_CLEAN
        elif max_c == mod_c:
            status = MATCH
        elif max_c > 0 and mod_c == 0:
            status = MODULAR_MISSING
        elif max_c == 0 and mod_c > 0:
            status = MAXIMAL_MISSING
        else:
            status = COUNT_MISMATCH

        results.append((rule, max_c, mod_c, status))

    return results


# ---------------------------------------------------------------------------
# Single test case runner
# ---------------------------------------------------------------------------

def run_single_comparison(gds_path, run_dir):
    """Run both decks on a single GDS and return comparison results.

    Returns: (gds_name, table_name, results_list, error_msg)
    """
    gds_path = Path(gds_path)
    gds_name = gds_path.stem
    table_name = gds_to_table(gds_name)

    if gds_name in SKIP_GDS:
        return (gds_name, table_name, [], f"Skipped (standalone deck)")

    # Get top cell
    try:
        top_cells = get_top_cell_names(str(gds_path))
    except Exception as e:
        return (gds_name, table_name, [], f"Failed to read GDS: {e}")

    if not top_cells:
        return (gds_name, table_name, [], "No top cells found")

    topcell = top_cells[0]

    # Create per-GDS output dir
    gds_run_dir = run_dir / gds_name
    gds_run_dir.mkdir(parents=True, exist_ok=True)

    # Run both decks
    logging.info(f"[{gds_name}] Running maximal deck (topcell={topcell})...")
    maximal_report = run_maximal(gds_path, topcell, gds_run_dir)
    if maximal_report is None:
        return (gds_name, table_name, [], "Maximal run failed")

    logging.info(f"[{gds_name}] Running modular deck (table={table_name}, topcell={topcell})...")
    modular_report = run_modular(gds_path, topcell, table_name, gds_run_dir)
    if modular_report is None:
        return (gds_name, table_name, [], "Modular run failed")

    # Parse results
    maximal_counts = parse_results_db(maximal_report)
    modular_counts = parse_results_db(modular_report)

    logging.info(
        f"[{gds_name}] Maximal: {len(maximal_counts)} rules, "
        f"Modular: {len(modular_counts)} rules"
    )

    # Compare
    results = compare_rules(maximal_counts, modular_counts)

    return (gds_name, table_name, results, None)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Cross-deck DRC comparison: modular vs maximal"
    )
    parser.add_argument(
        "--table", type=str, default=None,
        help="Run comparison only for GDS files mapping to this table."
    )
    parser.add_argument(
        "--mp", type=int, default=1,
        help="Number of parallel workers. [default: 1]"
    )
    parser.add_argument(
        "--run_dir", type=str, default=None,
        help="Output directory. [default: timestamped]"
    )
    args = parser.parse_args()

    # Setup run directory
    now_str = datetime.now(timezone.utc).strftime("crossdeck_%Y_%m_%d_%H_%M_%S")
    if args.run_dir:
        run_dir = Path(args.run_dir).resolve()
    else:
        run_dir = Path.cwd() / now_str
    run_dir.mkdir(parents=True, exist_ok=True)

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(run_dir / f"{now_str}.log"),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    logging.info(f"Cross-deck comparison output: {run_dir}")
    logging.info(f"DRC directory: {DRC_DIR}")
    logging.info(f"Maximal deck: {MAXIMAL_DRC}")
    logging.info(f"Unit test GDS dir: {UNIT_TEST_DIR}")

    # Discover GDS files
    gds_files = sorted(UNIT_TEST_DIR.glob("*.gds"))
    logging.info(f"Found {len(gds_files)} GDS files")

    # Filter by table if requested
    if args.table:
        gds_files = [
            g for g in gds_files
            if gds_to_table(g.stem) == args.table
        ]
        logging.info(f"Filtered to {len(gds_files)} GDS files for table '{args.table}'")

    if not gds_files:
        logging.error("No GDS files to process.")
        return 1

    # Run comparisons
    time_start = time.time()
    all_results = []

    if args.mp > 1:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.mp) as executor:
            futures = {
                executor.submit(run_single_comparison, gds, run_dir): gds
                for gds in gds_files
            }
            for future in concurrent.futures.as_completed(futures):
                gds = futures[future]
                try:
                    all_results.append(future.result())
                except Exception as e:
                    logging.error(f"{gds.stem} raised exception: {e}")
                    traceback.print_exc()
                    all_results.append((gds.stem, gds_to_table(gds.stem), [], str(e)))
    else:
        for gds in gds_files:
            try:
                result = run_single_comparison(gds, run_dir)
                all_results.append(result)
            except Exception as e:
                logging.error(f"{gds.stem} raised exception: {e}")
                traceback.print_exc()
                all_results.append((gds.stem, gds_to_table(gds.stem), [], str(e)))

    # Aggregate and report
    csv_path = run_dir / "crossdeck_summary.csv"
    total_match = 0
    total_clean = 0
    total_mismatch = 0
    total_mod_missing = 0
    total_max_missing = 0
    total_maximal_only = 0
    total_modular_only = 0
    table_pass = {}
    table_errors = {}

    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "gds_file", "table_name", "rule_id",
            "maximal_count", "modular_count", "status"
        ])

        for gds_name, table_name, results, error in sorted(all_results):
            if error:
                logging.warning(f"[{gds_name}] {error}")
                table_errors[gds_name] = error
                continue

            gds_pass = True
            for rule, max_c, mod_c, status in results:
                writer.writerow([gds_name, table_name, rule, max_c, mod_c, status])

                if status == MATCH:
                    total_match += 1
                elif status == BOTH_CLEAN:
                    total_clean += 1
                elif status == COUNT_MISMATCH:
                    total_mismatch += 1
                    gds_pass = False
                elif status == MODULAR_MISSING:
                    total_mod_missing += 1
                    gds_pass = False
                elif status == MAXIMAL_MISSING:
                    total_max_missing += 1
                elif status == "MAXIMAL_ONLY":
                    total_maximal_only += 1
                elif status == "MODULAR_ONLY":
                    total_modular_only += 1

            table_pass[gds_name] = gds_pass

    # Print summary
    elapsed = time.time() - time_start
    logging.info("")
    logging.info("=" * 70)
    logging.info("CROSS-DECK COMPARISON SUMMARY")
    logging.info("=" * 70)
    logging.info(f"Total GDS files processed: {len(all_results)}")
    logging.info(f"Total rules compared (overlapping): {total_match + total_clean + total_mismatch + total_mod_missing + total_max_missing}")
    logging.info(f"  MATCH:            {total_match}")
    logging.info(f"  BOTH_CLEAN:       {total_clean}")
    logging.info(f"  COUNT_MISMATCH:   {total_mismatch}")
    logging.info(f"  MODULAR_MISSING:  {total_mod_missing}")
    logging.info(f"  MAXIMAL_MISSING:  {total_max_missing}")
    logging.info(f"  MAXIMAL_ONLY:     {total_maximal_only} (not in modular)")
    logging.info(f"  MODULAR_ONLY:     {total_modular_only} (not in maximal)")
    logging.info("")

    # Per-GDS status
    logging.info("Per-GDS results:")
    for gds_name in sorted(table_pass.keys()):
        passed = table_pass[gds_name]
        status_str = "PASS" if passed else "FAIL"
        logging.info(f"  {gds_name:30s} {status_str}")
    for gds_name in sorted(table_errors.keys()):
        logging.info(f"  {gds_name:30s} ERROR: {table_errors[gds_name]}")

    logging.info("")

    # Overall verdict
    all_passed = all(table_pass.values()) if table_pass else False
    failures = total_mismatch + total_mod_missing
    # Skipped GDS files (e.g., antenna) are not failures
    real_errors = {k: v for k, v in table_errors.items() if "Skipped" not in v}

    if all_passed and failures == 0 and not real_errors:
        logging.info("OVERALL: PASS")
    else:
        logging.info(f"OVERALL: FAIL ({failures} rule discrepancies, {len(real_errors)} errors)")

    logging.info(f"Results CSV: {csv_path}")
    logging.info(f"Total time: {elapsed:.1f} seconds")

    return 0 if (all_passed and failures == 0 and not real_errors) else 1


if __name__ == "__main__":
    sys.exit(main())
