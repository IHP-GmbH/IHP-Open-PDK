#!/usr/bin/env python3
"""
Validate QA GDS pass/fail semantics by running DRC on split cells
and checking if violations fall in FAIL region (x > 0) vs PASS region (x < 0).

Usage:
    python validate_qa_passfail.py --table <table_name> --gds <path_to_gds>
    python validate_qa_passfail.py --all --gds_dir <path_to_qa_split>
"""

import argparse
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


DRC_DIR = Path(__file__).resolve().parents[3]  # .../drc/
RUN_DRC = DRC_DIR / "run_drc.py"
DEFAULT_JSON = DRC_DIR / "rule_decks" / "sg13g2_tech_default.json"


def run_drc_on_gds(gds_path: Path, table: str, topcell: str, output_dir: Path):
    """Run DRC on a single GDS file and return the .lyrdb path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = (
        f"python3 {RUN_DRC} "
        f"--path={gds_path} "
        f"--table={table} "
        f"--topcell={topcell} "
        f"--run_dir={output_dir} "
        f"--run_mode=flat "
        f"--mp=1 "
        f"--drc_json='{DEFAULT_JSON}' "
    )
    print(f"  Running DRC: table={table}, cell={topcell}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f"  DRC stderr: {result.stderr[-500:]}")

    # Find .lyrdb file
    lyrdb_files = list(output_dir.rglob("*.lyrdb"))
    if lyrdb_files:
        return lyrdb_files[0]
    return None


def parse_violations(lyrdb_path: Path):
    """Parse .lyrdb to extract rule names and violation coordinates."""
    violations = {}  # rule_name -> [(x_center, y_center), ...]

    tree = ET.parse(str(lyrdb_path))
    root = tree.getroot()

    for item in root.iter("item"):
        cats = item.findall("category")
        if not cats or not cats[0].text:
            continue
        rule_name = cats[0].text.strip().replace("'", "")

        values = item.find("values")
        if values is None:
            continue

        coords = []
        for val in values.findall("value"):
            text = val.text or ""
            # Extract coordinates from polygon/edge data
            # Format: "polygon: x1,y1;x2,y2;..." or "edge-pair: x1,y1;x2,y2/x3,y3;x4,y4"
            nums = re.findall(r"(-?\d+\.?\d*),(-?\d+\.?\d*)", text)
            if nums:
                xs = [float(x) for x, y in nums]
                x_center = sum(xs) / len(xs)
                coords.append(x_center)

        if rule_name not in violations:
            violations[rule_name] = []
        violations[rule_name].extend(coords)

    return violations


def validate_passfail(violations: dict, boundary_x: float = 0.0):
    """
    Check if violations fall in FAIL region (x > boundary) vs PASS region (x < boundary).

    Returns dict with:
      rule_name -> {
        'total': N,
        'in_fail': N,    # x > boundary (expected)
        'in_pass': N,    # x < boundary (unexpected - DRC bug or test issue)
        'status': 'OK' | 'PASS_VIOLATION' | 'NO_VIOLATIONS'
      }
    """
    results = {}
    for rule, x_coords in violations.items():
        in_fail = sum(1 for x in x_coords if x > boundary_x)
        in_pass = sum(1 for x in x_coords if x <= boundary_x)

        if len(x_coords) == 0:
            status = "NO_VIOLATIONS"
        elif in_pass > 0:
            status = "PASS_VIOLATION"
        else:
            status = "OK"

        results[rule] = {
            "total": len(x_coords),
            "in_fail": in_fail,
            "in_pass": in_pass,
            "status": status,
        }
    return results


def validate_table(gds_path: Path, table: str, topcell: str, work_dir: Path):
    """Run DRC and validate pass/fail for a single table."""
    print(f"\n{'='*60}")
    print(f"Validating: {table} (cell={topcell}, file={gds_path.name})")
    print(f"{'='*60}")

    output_dir = work_dir / table / topcell
    lyrdb = run_drc_on_gds(gds_path, table, topcell, output_dir)

    if not lyrdb:
        print(f"  ERROR: No .lyrdb generated for {table}/{topcell}")
        return None

    violations = parse_violations(lyrdb)
    if not violations:
        print(f"  WARNING: No violations found in {lyrdb.name}")
        return {}

    results = validate_passfail(violations)

    # Print results
    ok_count = 0
    pass_viol_count = 0
    no_viol_count = 0

    for rule, info in sorted(results.items()):
        marker = ""
        if info["status"] == "PASS_VIOLATION":
            marker = " *** UNEXPECTED VIOLATION IN PASS REGION ***"
            pass_viol_count += 1
        elif info["status"] == "NO_VIOLATIONS":
            marker = " (no coordinate data)"
            no_viol_count += 1
        else:
            ok_count += 1
        print(f"  {rule}: total={info['total']} fail_region={info['in_fail']} "
              f"pass_region={info['in_pass']} [{info['status']}]{marker}")

    print(f"\n  Summary: {ok_count} OK, {pass_viol_count} PASS_VIOLATION, "
          f"{no_viol_count} NO_VIOLATIONS, {len(results)} total rules")

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate QA GDS pass/fail semantics")
    parser.add_argument("--table", help="Single table to validate")
    parser.add_argument("--gds", help="Path to GDS file (for single table)")
    parser.add_argument("--topcell", help="Top cell name (auto-detected if omitted)")
    parser.add_argument("--all", action="store_true", help="Validate all gap tables")
    parser.add_argument("--gds_dir", default="testing/testcases/qa_split",
                        help="Directory with split QA GDS files")
    parser.add_argument("--work_dir", default="qa_validation",
                        help="Working directory for DRC outputs")
    args = parser.parse_args()

    work_dir = Path(args.work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    if args.table and args.gds:
        import klayout.db as db
        gds_path = Path(args.gds)
        if args.topcell:
            topcell = args.topcell
        else:
            layout = db.Layout()
            layout.read(str(gds_path))
            topcell = layout.top_cells()[0].name
        validate_table(gds_path, args.table, topcell, work_dir)

    elif args.all:
        import klayout.db as db
        gds_dir = Path(args.gds_dir)

        # Gap tables we want to validate
        gap_tables = {
            "rhigh": "rhigh",
            "nmosi": "nmosi",
            "rppd": "rppd",
            "rsil": "rsil",
            "salblock": "salblock",
            "extblock": "extblock",
            "offgrid": "offgrid",
            "nbulay": "nbulay",
            "npnsubstratetie": "npnsubstratetie",
            "nwell": "nwell",
            "psd": "psd",
            "metalslits": "metalslits",
            "contbar": "contbar",
        }

        all_results = {}
        for table, filename_prefix in gap_tables.items():
            gds_files = list(gds_dir.glob(f"{filename_prefix}*.gds"))
            if not gds_files:
                # Try exact match
                gds_files = list(gds_dir.glob(f"{filename_prefix}.gds"))
            if not gds_files:
                print(f"\nSKIP: No GDS found for {table} in {gds_dir}")
                continue

            for gds_path in gds_files:
                layout = db.Layout()
                layout.read(str(gds_path))
                for tc in layout.top_cells():
                    result = validate_table(gds_path, table, tc.name, work_dir)
                    if result is not None:
                        all_results[f"{table}/{tc.name}"] = result

        # Final summary
        print(f"\n{'='*60}")
        print("FINAL SUMMARY")
        print(f"{'='*60}")
        total_ok = 0
        total_pv = 0
        total_nv = 0
        for key, results in sorted(all_results.items()):
            ok = sum(1 for r in results.values() if r["status"] == "OK")
            pv = sum(1 for r in results.values() if r["status"] == "PASS_VIOLATION")
            nv = sum(1 for r in results.values() if r["status"] == "NO_VIOLATIONS")
            total_ok += ok
            total_pv += pv
            total_nv += nv
            marker = " <<<" if pv > 0 else ""
            print(f"  {key}: {ok} OK, {pv} PASS_VIOL, {nv} NO_DATA{marker}")

        print(f"\n  TOTAL: {total_ok} OK, {total_pv} PASS_VIOLATIONS, {total_nv} NO_DATA")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
