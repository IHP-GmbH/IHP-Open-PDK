#!/usr/bin/env python3
# ==========================================================================
# Copyright 2025 IHP PDK Authors
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
# ==========================================================================

"""
Run IHP 130nm BiCMOS Open Source PDK - SG13G2 DRC Regression For Cells.

This script runs DRC on the reference GDS layouts from ihp-sg13g2/libs.ref

Usage:
    run_regression_cells.py (--help | -h)
    run_regression_cells.py [--lib=<lib>] [--cell=<cell>] [--run_dir=<run_dir_path>] [--mp=<num>]

Options:
    --help -h                 Show this help message.
    --lib=<lib>               Run regression for a specific library only.
                                Supported: sg13g2_io, sg13g2_pr, sg13g2_stdcell, sg13g2_sram
    --cell=<cell>             Run regression for a specific cell only (top cell name).
    --run_dir=<run_dir_path>  Output directory to store results [default: pwd].
    --mp=<num>                Number of threads for parallel DRC runs.
"""

import os
import shutil
import time
import logging
import traceback
import concurrent.futures
import re
import ast
from datetime import datetime, timezone
from subprocess import run
from docopt import docopt
import pandas as pd
from pathlib import Path
import gdstk

# ==============================
# Constants / Config
# ==============================
SUPPORTED_TC_EXT = "gds"

# libs.ref expected structure (relative to ihp-sg13g2)
LIBREF_SUBPATH = "libs.ref"

# Merged GDS files that contain many top cells
MERGED_GDS = [
    ("sg13g2_io", "sg13g2_io/gds/sg13g2_io.gds"),
    ("sg13g2_pr", "sg13g2_pr/gds/sg13g2_pr.gds"),
    ("sg13g2_stdcell", "sg13g2_stdcell/gds/sg13g2_stdcell.gds"),
]

# SRAM GDS directory (one file per macro)
SRAM_GDS_DIR = "sg13g2_sram/gds"

SUPPORTED_LIBS = {"sg13g2_io", "sg13g2_pr", "sg13g2_stdcell", "sg13g2_sram"}

# ==============================
# Cells policies
# ==============================
# 1) Fully ignored cells (not executed at all) -> status = "Excluded"
IGNORE_TESTS = {
    "sg13g2_pr/colors_and_stipples": "Not an actual physical cell; visualization/example content only.",
}

# 2) Waived-violations cells (executed) -> pass only if violated rules ⊆ allowed set
#    If the cell violates anything outside the allowed list -> Failed.
WAIVER_PROFILES = {
    "OFFGRID_M1_PIN": {
        "reason": "Known real offgrid violations on metal1.pin for this standalone IO cell.",
        "allowed_rules": {"metal1_pin_Offgrid"},
    },
    "PR_PCELL_BASE": {
        "reason": "Parametric (PCell) template; not used as-is. Violations disappear in real layouts.",
        "allowed_rules": {"M1.d", "Gat.e", "LU.b"},
    },
    "PR_DANTENNA": {
        "reason": "Parametric (PCell) template; not used as-is. Violations disappear in real layouts.",
        "allowed_rules": {"LU.b"},
    },
    "STDCELL_FILL": {
        "reason": "Expected standalone violations; filler not used alone. Violations disappear in real layouts.",
        "allowed_rules": {"pSD.k"},
    },
}

WAIVED_GROUPS = {
    "OFFGRID_M1_PIN": {
        "sg13g2_io": [
            "sg13g2_IOPadInOut30mA",
            "sg13g2_IOPadOut30mA",
            "sg13g2_IOPadTriOut30mA",
        ],
        "sg13g2_sram": [
            "RM_IHPSG13_1P_1024x8_c2_bm_bist",
            "RM_IHPSG13_1P_1024x16_c2_bm_bist",
            "RM_IHPSG13_1P_256x16_c2_bm_bist",
            "RM_IHPSG13_1P_1024x32_c2_bm_bist",
            "RM_IHPSG13_1P_256x32_c2_bm_bist",
            "RM_IHPSG13_1P_256x48_c2_bm_bist",
            "RM_IHPSG13_1P_256x8_c3_bm_bist",
            "RM_IHPSG13_1P_256x64_c2_bm_bist",
            "RM_IHPSG13_1P_1024x64_c2_bm_bist",
            "RM_IHPSG13_1P_512x16_c2_bm_bist",
            "RM_IHPSG13_1P_4096x8_c3_bm_bist",
            "RM_IHPSG13_1P_512x32_c2_bm_bist",
            "RM_IHPSG13_1P_512x8_c3_bm_bist",
            "RM_IHPSG13_1P_64x64_c2_bm_bist",
            "RM_IHPSG13_1P_4096x16_c3_bm_bist",
            "RM_IHPSG13_1P_512x64_c2_bm_bist",
            "RM_IHPSG13_1P_2048x64_c2_bm_bist",
        ],
    },
    "PR_PCELL_BASE": {
        "sg13g2_pr": ["nmos", "nmosHV", "pmos", "pmosHV"],
    },
    "PR_DANTENNA": {
        "sg13g2_pr": ["dantenna"],
    },
    "STDCELL_FILL": {
        "sg13g2_stdcell": ["sg13g2_fill_1"],
    },
}


def build_waived_tests() -> dict[str, dict]:
    """Expand grouped waiver definitions into the legacy flat lookup map."""
    waived: dict[str, dict] = {}

    for profile_name, libs_cells in WAIVED_GROUPS.items():
        profile = WAIVER_PROFILES[profile_name]
        for lib, cells in libs_cells.items():
            for cell in cells:
                key = f"{lib}/{cell}"
                if key in waived:
                    raise ValueError(f"Duplicate waived test entry: {key}")
                waived[key] = {
                    "reason": profile["reason"],
                    "allowed_rules": set(profile["allowed_rules"]),
                }

    return waived


WAIVED_TESTS = build_waived_tests()


def ignore_reason(lib: str, cell_name: str) -> str | None:
    return IGNORE_TESTS.get(f"{lib}/{cell_name}")


def waived_info(lib: str, cell_name: str) -> dict | None:
    return WAIVED_TESTS.get(f"{lib}/{cell_name}")


# ==============================
# gdstk-based cell discovery
# ==============================

def gdstk_list_topcells(gds_path: str) -> list[str]:
    """Return a sorted list of top cell names in a GDS using gdstk."""
    gds_path = os.path.abspath(gds_path)
    if not os.path.isfile(gds_path):
        raise FileNotFoundError(f"GDS not found: {gds_path}")

    lib = gdstk.read_gds(gds_path)

    all_names = set()
    for cell in lib.cells:
        if getattr(cell, "name", None):
            all_names.add(cell.name)

    referenced = set()
    for cell in lib.cells:
        refs = getattr(cell, "references", None)
        if not refs:
            continue
        for ref in refs:
            target = getattr(ref, "cell", None)
            if target is None:
                continue
            if isinstance(target, str):
                referenced.add(target)
            else:
                name = getattr(target, "name", None)
                if name:
                    referenced.add(name)

    return sorted(all_names - referenced)


def gdstk_list_first_level_cells(gds_path: str, topcell_name: str) -> list[str]:
    """
    Return a sorted list of unique cell names referenced directly by `topcell_name`
    (1st hierarchy level only).

    This is used for sg13g2_io.gds when IO cells are subcells of a single wrapper topcell.
    """
    gds_path = os.path.abspath(gds_path)
    if not os.path.isfile(gds_path):
        raise FileNotFoundError(f"GDS not found: {gds_path}")

    lib = gdstk.read_gds(gds_path)

    top = None
    for c in lib.cells:
        if getattr(c, "name", None) == topcell_name:
            top = c
            break
    if top is None:
        raise RuntimeError(f"Top cell '{topcell_name}' not found in {gds_path}")

    children = set()
    refs = getattr(top, "references", None) or []
    for ref in refs:
        target = getattr(ref, "cell", None)
        if target is None:
            continue
        if isinstance(target, str):
            children.add(target)
        else:
            name = getattr(target, "name", None)
            if name:
                children.add(name)

    return sorted(children)


# ==============================
# DRC log parsing helpers
# ==============================

_VIOLATED_RULES_RE = re.compile(r"Violated rules are\s*:\s*(\{.*\})")


def extract_violated_rules(log_content: str) -> set[str]:
    """
    Parse the DRC log and return the set of violated rule names.

    Expected line format in log:
        Violated rules are : {'Act.b', 'Act.d', ...}
    """
    m = _VIOLATED_RULES_RE.search(log_content)
    if not m:
        return set()

    raw = m.group(1).strip()
    try:
        parsed = ast.literal_eval(raw)
    except Exception:
        return set()

    if isinstance(parsed, (set, list, tuple)):
        return {str(x) for x in parsed}
    return set()


# ==============================
# Test discovery (libs.ref)
# ==============================

def discover_libref_tests(libref_root: str) -> pd.DataFrame:
    """
    Discover all (lib, cell_name, layout_path) testcases from libs.ref.

    - IO (sg13g2_io.gds):
        * If multiple topcells exist -> run each topcell.
        * If only ONE topcell exists (wrapper) -> run each 1st-level child cell of that wrapper.
    - PR, STDCELL:
        * Run each topcell in the merged GDS.
    - SRAM:
        * For each *.gds file, run each topcell inside it.

    Fully-ignored tests are kept in report but not executed.
    Waived-violations tests are executed and pass only if violations are limited to allowed rules.

    Returns:
        DataFrame columns:
            lib, cell_name, layout_path,
            ignore_reason, waiver_reason, allowed_rules,
            run_id
    """
    libref_root = os.path.abspath(libref_root)
    logging.info("Step: Discovering tests from libs.ref ...")
    logging.info(f"libs.ref root: {libref_root}")

    if not os.path.isdir(libref_root):
        logging.error(f"libs.ref directory does not exist: {libref_root}")
        raise FileNotFoundError(libref_root)

    tests: list[dict] = []

    def add_test(lib: str, cell_name: str, layout_path: str) -> None:
        ig = ignore_reason(lib, cell_name) or ""
        w = waived_info(lib, cell_name) or {}
        waiver_reason = str(w.get("reason", "")) if w else ""
        allowed = sorted(list(w.get("allowed_rules", set()))) if w else []
        tests.append(
            {
                "lib": lib,
                "cell_name": cell_name,
                "layout_path": layout_path,
                "ignore_reason": ig,
                "waiver_reason": waiver_reason,
                "allowed_rules": ",".join(allowed),  # CSV-friendly
            }
        )

    # ---- Merged libraries (io/pr/stdcell)
    for lib_name, relpath in MERGED_GDS:
        gds = os.path.join(libref_root, relpath)
        if not os.path.isfile(gds):
            logging.error(f"[DISCOVERY] Missing merged GDS for {lib_name}: {gds}")
            continue

        try:
            topcells = gdstk_list_topcells(gds)
        except Exception as e:
            logging.error(f"[DISCOVERY] Failed to read topcells for {lib_name} ({gds}): {e}")
            continue

        if not topcells:
            logging.error(f"[DISCOVERY] No topcells found in {lib_name} GDS: {gds}")
            continue

        # Special handling for IO: if only one topcell exists, run on 1st-level children
        if lib_name == "sg13g2_io" and len(topcells) == 1:
            io_wrapper = topcells[0]
            try:
                first_level = gdstk_list_first_level_cells(gds, io_wrapper)
            except Exception as e:
                logging.error(
                    f"[DISCOVERY] {lib_name}: failed to get 1st-level cells from wrapper '{io_wrapper}' ({gds}): {e}"
                )
                continue

            if not first_level:
                logging.error(
                    f"[DISCOVERY] {lib_name}: wrapper top cell '{io_wrapper}' has no direct child references in {gds}."
                )
                continue

            logging.info(
                f"[DISCOVERY] {lib_name}: found 1 wrapper topcell '{io_wrapper}' in {os.path.basename(gds)}; "
                f"running {len(first_level)} first-level cells instead."
            )
            for c in first_level:
                add_test(lib_name, c, gds)
        else:
            logging.info(f"[DISCOVERY] {lib_name}: found {len(topcells)} topcells in {os.path.basename(gds)}")
            for c in topcells:
                add_test(lib_name, c, gds)

    # ---- SRAM (one or more top cells per file)
    sram_dir = os.path.join(libref_root, SRAM_GDS_DIR)
    if not os.path.isdir(sram_dir):
        logging.error(f"[DISCOVERY] Missing SRAM GDS directory: {sram_dir}")
    else:
        sram_files = sorted(Path(sram_dir).glob(f"*.{SUPPORTED_TC_EXT}"))
        if not sram_files:
            logging.error(f"[DISCOVERY] No SRAM GDS files found in: {sram_dir}")
        else:
            logging.info(f"[DISCOVERY] SRAM: found {len(sram_files)} GDS files.")
            for gds_path in sram_files:
                gds = str(gds_path)
                try:
                    topcells = gdstk_list_topcells(gds)
                except Exception as e:
                    logging.error(f"[DISCOVERY] Failed to read SRAM topcells ({gds}): {e}")
                    continue

                if not topcells:
                    logging.error(f"[DISCOVERY] No topcells found in SRAM GDS: {gds}")
                    continue

                for c in topcells:
                    add_test("sg13g2_sram", c, gds)

    df = pd.DataFrame(tests)
    if df.empty:
        logging.error("No tests discovered from libs.ref (missing GDS files or no cells discovered).")
        raise RuntimeError("Discovery produced zero tests.")

    df = df.drop_duplicates(subset=["layout_path", "cell_name"]).reset_index(drop=True)
    df["run_id"] = range(len(df))

    logging.info("Step: Discovery summary")
    logging.info(f"Discovered total tests: {len(df)}")

    by_lib = df.groupby("lib")["cell_name"].nunique().to_dict()
    for l, n in sorted(by_lib.items()):
        logging.info(f"  - {l}: {n} cells")

    ignored_count = (df["ignore_reason"].astype(str).str.len() > 0).sum()
    waived_count = (df["allowed_rules"].astype(str).str.len() > 0).sum()
    logging.info(f"Ignored (not run): {ignored_count}")
    logging.info(f"Waived-policy cells (run with allowed rules): {waived_count}")

    return df


def build_tests_dataframe(libref_root: str, target_cell: str | None, target_lib: str | None) -> pd.DataFrame:
    """
    Build the regression test DataFrame from libs.ref, optionally filtering to a lib and/or a single cell.
    """
    tc_df = discover_libref_tests(libref_root)

    if target_lib:
        logging.info(f"Step: Filtering to target lib: {target_lib}")
        tc_df = tc_df[tc_df["lib"] == target_lib].copy()

    if target_cell:
        logging.info(f"Step: Filtering to target cell: {target_cell}")
        tc_df = tc_df[tc_df["cell_name"] == target_cell].copy()

    if tc_df.empty:
        logging.error("No valid test cases found after filtering.")
        raise RuntimeError("No tests after filtering.")

    logging.info(f"Total cells/tests to run (including ignore/waive policies): {len(tc_df)}")
    return tc_df


# ==============================
# DRC execution
# ==============================

def run_test_case(
    drc_dir: str,
    layout_path: str,
    run_dir: str,
    lib: str,
    cell_name: str,
    allowed_rules: set[str] | None = None,
) -> tuple[str, str]:
    """
    Run a single DRC test case and return (status, violated_rules_csv).

    - If DRC passes normally -> ("Passed", "")
    - If DRC fails:
        * If allowed_rules is provided and violated_rules ⊆ allowed_rules -> ("Passed (Waived)", "<violations>")
        * Else -> ("Failed", "<violations>")
    """
    cell_dir = os.path.join(run_dir, lib, cell_name)
    os.makedirs(cell_dir, exist_ok=True)

    gds_basename = os.path.basename(layout_path)
    layout_path_run = os.path.join(cell_dir, gds_basename)
    pattern_log = os.path.join(cell_dir, f"{cell_name}_drc.log")

    try:
        shutil.copyfile(layout_path, layout_path_run)
    except Exception as e:
        logging.error(f"[{lib}/{cell_name}] Failed to copy GDS: {e}")
        return "Failed", ""

    run_drc_py = os.path.join(drc_dir, "run_drc.py")
    if not os.path.isfile(run_drc_py):
        logging.error(f"run_drc.py not found in DRC dir: {run_drc_py}")
        return "Failed", ""

    drc_out_dir = os.path.join(run_dir, f"drc_run_{lib}_{cell_name}")

    cmd = [
        "python3",
        run_drc_py,
        f"--path={layout_path_run}",
        f"--topcell={cell_name}",
        "--run_mode=flat",
        f"--run_dir={drc_out_dir}",
        "--no_density",
        "--disable_extra_rules",
    ]

    logger_prefix = f"[{lib}/{cell_name}]"
    logging.info(f"{logger_prefix} Executing DRC ...")

    try:
        with open(pattern_log, "w", encoding="utf-8") as lf:
            lf.write("Command:\n")
            lf.write(" ".join(cmd) + "\n\n")
            lf.flush()
            res = run(cmd, stdout=lf, stderr=lf, text=True)
            rc = res.returncode
    except Exception as e:
        logging.error(f"{logger_prefix} DRC generated an exception: {e}")
        traceback.print_exc()
        return "Failed", ""

    if not os.path.isfile(pattern_log):
        logging.error(f"❌ {logger_prefix} No DRC log found: {pattern_log}")
        return "Failed", ""

    try:
        with open(pattern_log, "r", encoding="utf-8", errors="replace") as f:
            log_content = f.read()
    except Exception as e:
        logging.error(f"{logger_prefix} Could not read DRC log: {e}")
        return "Failed", ""

    # Normal pass
    if rc == 0 and "KLayout DRC Check Passed" in log_content:
        logging.info(f"✅ {logger_prefix} passed DRC.")
        return "Passed", ""

    # Failed -> parse violated rules (if available)
    violated = extract_violated_rules(log_content)
    violated_csv = ",".join(sorted(violated)) if violated else ""

    # Waiver logic
    if allowed_rules is not None:
        # If we couldn't parse rules, be conservative and fail
        if not violated:
            logging.error(f"❌ {logger_prefix} failed DRC, but violated rules could not be parsed from log.")
            return "Failed", violated_csv

        if violated.issubset(allowed_rules):
            logging.info(
                f"✅ {logger_prefix} passed with WAIVER. Violations limited to allowed rules: "
                f"{sorted(violated)}"
            )
            return "Passed (Waived)", violated_csv

        unexpected = sorted(violated - allowed_rules)
        logging.error(
            f"❌ {logger_prefix} failed DRC (WAIVER REJECTED). Unexpected violated rules: {unexpected}"
        )
        return "Failed", violated_csv

    # No waiver policy -> fail
    logging.error(f"❌ {logger_prefix} failed DRC.")
    return "Failed", violated_csv


def run_all_test_cases(tc_df: pd.DataFrame, drc_dir: str, run_dir: str, num_workers: int) -> pd.DataFrame:
    """
    Execute DRC runs for all cells concurrently using a thread pool.

    - Ignored tests -> status "Excluded" (not executed)
    - Waived-policy tests -> executed; pass only if violated rules are a subset of allowed rules
    """
    logging.info("Step: Running all test cases ...")
    logging.info(f"Parallel workers: {num_workers}")

    tc_df = tc_df.copy()
    tc_df["cell_status"] = "Pending"
    tc_df["violated_rules"] = ""

    excluded_count = 0
    runnable_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_run_id = {}

        for _, row in tc_df.iterrows():
            lib = row["lib"]
            cell = row["cell_name"]

            ig = str(row.get("ignore_reason", "")).strip()
            if ig:
                logging.info(f"[{lib}/{cell}] EXCLUDED: {ig}")
                tc_df.loc[tc_df["run_id"] == row["run_id"], "cell_status"] = "Excluded"
                excluded_count += 1
                continue

            allowed_rules_str = str(row.get("allowed_rules", "")).strip()
            allowed_rules = set(filter(None, [x.strip() for x in allowed_rules_str.split(",")])) if allowed_rules_str else None

            if allowed_rules is not None:
                waiver_reason = str(row.get("waiver_reason", "")).strip()
                logging.info(
                    f"[{lib}/{cell}] WAIVER ENABLED: allowed_rules={sorted(allowed_rules)} | reason={waiver_reason}"
                )

            runnable_count += 1
            fut = executor.submit(
                run_test_case,
                drc_dir,
                row["layout_path"],
                run_dir,
                lib,
                cell,
                allowed_rules,
            )
            future_to_run_id[fut] = row["run_id"]

        logging.info(f"Runnable tests: {runnable_count} | Excluded tests: {excluded_count}")

        for future in concurrent.futures.as_completed(future_to_run_id):
            run_id = future_to_run_id[future]
            try:
                status, violated_csv = future.result()
                tc_df.loc[tc_df["run_id"] == run_id, "cell_status"] = status
                tc_df.loc[tc_df["run_id"] == run_id, "violated_rules"] = violated_csv
            except Exception as exc:
                logging.error(f"Run {run_id} raised an exception: {exc}")
                tc_df.loc[tc_df["run_id"] == run_id, "cell_status"] = "exception"

    return tc_df


def run_regression(
    drc_dir: str,
    libref_root: str,
    output_path: str,
    target_cell: str | None,
    target_lib: str | None,
    cpu_count: int,
) -> bool:
    """
    Full DRC regression flow.

    Final report includes all discovered cells with status:
        - Passed / Passed (Waived) / Failed / Excluded / exception
    """
    logging.info("Step: Building test list ...")
    tc_df = build_tests_dataframe(libref_root, target_cell, target_lib)

    logging.info("Step: Executing test list ...")
    results_df = run_all_test_cases(tc_df, drc_dir, output_path, cpu_count)
    results_df.drop_duplicates(inplace=True)
    results_df.drop("run_id", inplace=True, axis=1)

    results_df = results_df[
        [
            "lib",
            "cell_name",
            "layout_path",
            "cell_status",
            "violated_rules",
            "ignore_reason",
            "waiver_reason",
            "allowed_rules",
        ]
    ]
    results_df = results_df.sort_values(["lib", "cell_name"]).reset_index(drop=True)

    results_path = os.path.join(output_path, "all_test_cases_results.csv")
    results_df.to_csv(results_path, index=False)
    logging.info(f"📄 Saved results to: {results_path}")

    failing = results_df[results_df["cell_status"].isin(["Failed", "exception"])]
    if len(failing) > 0:
        logging.error("Some test cases failed DRC (Excluded are not counted as failures).")
        failing_list = failing["cell_name"].tolist()
        logging.error(f"Failing cells count: {len(failing_list)}")
        logging.error(f"Failing cells (first 50): {failing_list[:50]}")
        return False

    logging.info("🎉 All runnable DRC testcases passed successfully (some may be excluded or waived).")
    return True


def main(drc_dir: str, libref_root: str, output_path: str, target_cell: str | None, target_lib: str | None):
    """Entry point for the DRC regression workflow."""
    cpu_count = os.cpu_count() if args["--mp"] is None else int(args["--mp"])

    logging.info("============================================================")
    logging.info("IHP SG13G2 DRC regression (libs.ref)")
    logging.info("============================================================")
    logging.info(f"Run folder:  {output_path}")
    logging.info(f"libs.ref:    {libref_root}")
    logging.info(f"Target lib:  {target_lib if target_lib else 'All'}")
    logging.info(f"Target cell: {target_cell if target_cell else 'All'}")
    logging.info(f"Threads:     {cpu_count}")
    logging.info("============================================================")

    start = time.time()
    success = run_regression(drc_dir, libref_root, output_path, target_cell, target_lib, cpu_count)
    logging.info(f"Total execution time: {time.time() - start:.2f}s")

    if not success:
        raise SystemExit(1)


# ==============================
# Script Entry Point
# ==============================

if __name__ == "__main__":
    args = docopt(__doc__, version="DRC Regression: 0.4")

    run_name = datetime.now(timezone.utc).strftime("drc_cells_%Y_%m_%d_%H_%M_%S")
    run_dir = args["--run_dir"]
    output_path = os.path.abspath(run_dir if run_dir not in ["pwd", "", None] else os.getcwd())
    output_path = os.path.join(output_path, run_name)
    os.makedirs(output_path, exist_ok=True)

    testing_dir = os.path.dirname(os.path.abspath(__file__))
    drc_dir = os.path.dirname(testing_dir)
    libs_tech_dir = Path(drc_dir).parents[2]
    ihp_sg13g2_dir = libs_tech_dir.parent
    libref_root = str(ihp_sg13g2_dir / LIBREF_SUBPATH)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(os.path.join(output_path, f"{run_name}.log")),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    if not os.path.isdir(libref_root):
        logging.error(f"libs.ref directory not found: {libref_root}")
        logging.error("Expected structure: <ihp-sg13g2>/libs.ref/<lib>/gds/...")
        raise SystemExit(1)

    try:
        discovered_df = discover_libref_tests(libref_root)
    except Exception as e:
        logging.error(f"Failed to discover tests from libs.ref: {e}")
        raise SystemExit(1)

    target_lib = args["--lib"]
    if target_lib:
        if target_lib not in SUPPORTED_LIBS:
            logging.error(f"Unsupported lib '{target_lib}'. Supported: {sorted(SUPPORTED_LIBS)}")
            raise SystemExit(1)

        lib_cells = discovered_df[discovered_df["lib"] == target_lib]["cell_name"].unique().tolist()
        logging.info(f"Discovered cells in lib {target_lib}: {len(lib_cells)}")
        if len(lib_cells) == 0:
            logging.error(f"No cells discovered for lib: {target_lib}")
            raise SystemExit(1)

    all_cells = sorted(discovered_df["cell_name"].unique().tolist())
    logging.info(f"Discovered unique cell names (all libs): {len(all_cells)}")

    target_cell = args["--cell"]
    if target_cell:
        if target_cell not in all_cells:
            logging.error(f"Selected cell '{target_cell}' not found in discovered libs.ref cells.")
            logging.error(f"Discovered unique cells count: {len(all_cells)}")
            raise SystemExit(1)

        if target_lib:
            cells_in_lib = set(discovered_df[discovered_df["lib"] == target_lib]["cell_name"].tolist())
            if target_cell not in cells_in_lib:
                logging.error(f"Selected cell '{target_cell}' is not in selected lib '{target_lib}'.")
                raise SystemExit(1)

    main(drc_dir, libref_root, output_path, target_cell, target_lib)
