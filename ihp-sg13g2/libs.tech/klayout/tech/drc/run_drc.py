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

import argparse
import os
from pathlib import Path
import xml.etree.ElementTree as ET
import logging
import klayout.db
from datetime import datetime, timezone
import time
from subprocess import check_call
import shutil
import multiprocessing as mp
import concurrent.futures
import traceback
from typing import Dict, List, Optional, Set, Union


def get_rules_with_violations(results_database: Union[str, Path]) -> Set[str]:
    """
    Parse a KLayout RDB (Results Database) file and return a set of rule names
    that have reported violations.

    Parameters
    ----------
    results_database : str or Path
        Path to the KLayout-generated RDB file.

    Returns
    -------
    set
        A set of rule names (strings) that have violations.
    """

    results_database = Path(results_database)
    if not results_database.is_file():
        logging.error(f"Results database not found: {results_database}")
        raise FileNotFoundError(f"No such file: {results_database}")

    try:
        tree = ET.parse(results_database)
        root = tree.getroot()
    except ET.ParseError as e:
        logging.error(f"Failed to parse results database: {results_database}")
        raise e

    violating_rules = set()
    for rule in root[7]:  # root[7] : List rules with violations
        violating_rules.add(f"{rule[1].text}".replace("'", ""))

    return violating_rules


def merge_klayout_drc_reports(input_files: List[str], output_file: str):
    """
    Merges multiple KLayout DRC report XML files into a single XML file.

    Parameters:
        input_files (List[str]): List of paths to input DRC XML files.
        output_file (str): Path to write the merged output XML.

    Behavior:
        - Retains metadata (description, top-cell, etc.) from the first file.
        - Merges <categories>, <cells>, and <items> from all input files.
        - Skips any input file that is missing required structure.
    """
    # Load the first file as the base document
    base_tree = ET.parse(input_files[0])
    base_root = base_tree.getroot()

    # Locate primary mergeable elements in the base document
    base_categories = base_root.find("categories")
    base_cells = base_root.find("cells")
    base_items = base_root.find("items")

    if base_categories is None or base_cells is None or base_items is None:
        raise ValueError(
            f"Base file '{input_files[0]}' is missing required elements, failed in merging result database."
        )

    # Iterate through the remaining files and merge elements
    for file_path in input_files[1:]:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            # Append each <category> from this file
            categories = root.find("categories")
            if categories is not None:
                for category in categories.findall("category"):
                    base_categories.append(category)

            # Collect existing cell names from base_cells
            existing_names = set()
            for cell in base_cells.findall("cell"):
                name_elem = cell.find("name")
                if name_elem is not None and name_elem.text:
                    existing_names.add(name_elem.text.strip())

            # Append new <cell> only if not already present
            cells = root.find("cells")
            if cells is not None:
                for cell in cells.findall("cell"):
                    name_elem = cell.find("name")
                    if name_elem is not None and name_elem.text:
                        name = name_elem.text.strip()
                        if name not in existing_names:
                            base_cells.append(cell)
                            existing_names.add(name)

            # # Append each <items> from this file
            items = root.find("items")
            if items is not None:
                for item in items.findall("item"):
                    base_items.append(item)

        except ET.ParseError as e:
            logging.error(f"Error parsing '{file_path}': {e}. Skipping.")
            continue
    # Write the merged XML content to output
    base_tree.write(output_file, encoding="utf-8", xml_declaration=True)


def check_drc_results(
    results_db_files: List[Union[str, Path]],
    run_dir: Path,
    layout_path: str,
    switches: dict,
):
    """
    Check the results database(s) generated from the KLayout DRC run and report if the run passed or failed.

    Parameters
    ----------
    results_db_files : list of str or Path
        Paths to individual .lyrdb result databases generated by KLayout.
    run_dir : Path
        Directory where the run output is generated.
    layout_path : str
        Full path to the layout file (GDS/OAS).
    switches : SimpleNamespace or None
        Optional argument containing user switches, including topcell name.
    """

    if len(results_db_files) < 1:
        logging.error("❌ KLayout did not generate any result database (.lyrdb). Please check the logs.")
        exit(1)

    results_db_files = [Path(f) for f in results_db_files]

    if len(results_db_files) > 1:
        layout_name = Path(layout_path).stem
        topcell = switches["topcell"]
        merged_report = run_dir / f"{layout_name}_{topcell}_full.lyrdb"
        merge_klayout_drc_reports(results_db_files, merged_report)

        # Delete partial reports after merging
        for f in results_db_files:
            if f != merged_report and f.exists():
                os.remove(f)

        report_path = merged_report
    else:
        report_path = results_db_files[0]

    # Parse violations
    violating_rules = get_rules_with_violations(report_path)

    if violating_rules:
        logging.error("==================================================================================")
        logging.error("❌ --- KLayout DRC Check Failed: Violations were detected in the layout. --- ❌")
        logging.error("==================================================================================")
        logging.error(f"Violated rules are : {str(violating_rules)}\n")
    else:
        logging.info("=====================================================================================")
        logging.info("✅ --- KLayout DRC Check Passed: No DRC violations detected in the layout. --- ✅")
        logging.info("=====================================================================================")


def generate_drc_run_template(
    drc_dir: str,
    run_dir: Path,
    run_tables_list: Optional[List[str]] = None
) -> Path:
    """
    Generate the rule deck template to run DRC from individual table files.

    Parameters
    ----------
    drc_dir : str
        Directory containing rule_decks.
    run_dir : Path
        Directory where the assembled rule deck will be saved.
    run_tables_list : List[str], optional
        List of table base names to include (without ".drc" extension).
        If None or empty, all tables except the excluded ones will be included.

    Returns
    -------
    Path
        Path to the generated DRC rule deck file.
    """
    drc_dir = Path(drc_dir)
    rule_deck_dir = drc_dir / "rule_decks"
    run_tables_list = run_tables_list or []

    deck_name = "main"
    exclude_decks = {"antenna", "density", "sg13g2_maximal", "main", "layers_def", "tail"}

    # Gather all available .drc files in rule_decks/
    all_drc_files = list(rule_deck_dir.glob("*.drc"))
    all_drc_names = [f.name for f in all_drc_files]

    # Determine which tables to include
    if not run_tables_list:
        # Default: include all except excluded
        selected_tables = [
            f.name for f in all_drc_files
            if f.stem not in exclude_decks
        ]

        # Sort by numeric prefix
        selected_tables.sort(
            key=lambda name: tuple(
                int(part) if part.isdigit() else float("inf")
                for part in name.replace(".drc", "").split("_")
            )
        )
    else:
        # Specific tables requested — match against *_<table>.drc
        selected_tables = []
        for table in run_tables_list:
            match = next(
                (name for name in all_drc_names if name.endswith(f"_{table}.drc")),
                None
            )
            if match:
                selected_tables.append(match)
            else:
                logging.warning(f"Requested table '{table}' not found in rule_decks.")

        if len(run_tables_list) == 1:
            deck_name = run_tables_list[0]

    logging.info(f"Generating DRC rule deck using tables: {selected_tables}")
    logging.info(f"DRC output will be written to: {run_dir.resolve()}")

    # Ensure run directory exists
    run_dir.mkdir(parents=True, exist_ok=True)

    # Copy layers_def.drc to run_dir (needed by main.drc)
    layers_def_src = rule_deck_dir / "layers_def.drc"
    layers_def_dst = run_dir / "layers_def.drc"
    if not layers_def_src.is_file():
        raise FileNotFoundError(f"layers_def.drc not found at {layers_def_src}")
    shutil.copyfile(layers_def_src, layers_def_dst)

    # Assemble the full rule deck
    final_deck_path = run_dir / f"{deck_name}.drc"
    all_tables = ["main.drc"] + selected_tables + ["tail.drc"]

    with open(final_deck_path, "w") as output_fd:
        for rule_file in all_tables:
            full_path = rule_deck_dir / rule_file
            if full_path.exists():
                with open(full_path, "r") as input_fd:
                    shutil.copyfileobj(input_fd, output_fd)
            else:
                logging.warning(f"Rule file {rule_file} not found and will be skipped.")

    return final_deck_path


def get_top_cell_names(gds_path: str):
    """
    get_top_cell_names get the top cell names from the GDS file.

    Parameters
    ----------
    gds_path : str
        Path to the target GDS file.

    Returns
    -------
    List of string
        Names of the top cell in the layout.
    """
    layout = klayout.db.Layout()
    layout.read(gds_path)
    top_cells = [t.name for t in layout.top_cells()]

    return top_cells


def get_list_of_tables(drc_dir: str):
    """
    get_list_of_tables get the list of available tables in the drc

    Parameters
    ----------
    drc_dir : str
        Path to the DRC folder to get the list of tables from.
    """
    exclude_decks = {"antenna", "density", "sg13g2_maximal", "main", "layers_def", "tail"}
    tables = []
    for f in (Path(drc_dir) / "rule_decks").glob("*.drc"):
        parts = f.stem.split("_")
        if len(parts) >= 3:
            name = "_".join(parts[2:])
        else:
            name = f.stem  # fallback: keep the full name

        if name not in exclude_decks:
            tables.append(name)

    return tables


def get_run_top_cell_name(args, layout_path: str):
    """
    Get the top cell name to use for DRC. If the user provides it, use that;
    otherwise, extract it from the layout.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments.
    layout_path : str
        Path to the target layout (GDS/OAS file).

    Returns
    -------
    str
        Name of the topcell to use.
    """
    if args.topcell:
        topcell = args.topcell
    else:
        layout_topcells = get_top_cell_names(layout_path)
        if len(layout_topcells) > 1:
            logging.error(
                "Layout has multiple topcells. Please specify one using --topcell."
            )
            exit(1)
        elif not layout_topcells:
            logging.error("No topcell found in layout. Invalid or empty GDS/OAS file?")
            exit(1)
        else:
            topcell = layout_topcells[0]

    return topcell


def generate_klayout_switches(arguments, layout_path: str) -> dict:
    """
    Parses the input arguments and prepares a dictionary of switches for the KLayout DRC run.

    Parameters
    ----------
    arguments : SimpleNamespace
        Namespace holding all user-provided command-line options.
    layout_path : str
        Path to the layout file that will be checked.

    Returns
    -------
    dict
        Dictionary representing all switches to be passed to KLayout.
    """
    switches = {}

    # Number of threads
    switches["thr"] = arguments.density_thr

    # Locate JSON rule file paths
    script_dir = Path(__file__).resolve().parent
    tech_rule_path = (script_dir / "../../python/sg13g2_pycell_lib/sg13g2_tech_mod.json").resolve()
    default_rule_path = (script_dir / "rule_decks/sg13g2_tech_default.json").resolve()
    switches["drc_json_default"] = default_rule_path

    # Select best-available JSON rules file
    if arguments.drc_json:
        user_path = Path(arguments.drc_json).resolve()
        logging.info(f"User-provided DRC rules JSON: {user_path}")
        candidate_paths = [user_path, tech_rule_path, default_rule_path]
    else:
        candidate_paths = [tech_rule_path, default_rule_path]

    for path in candidate_paths:
        if path.is_file():
            logging.info(f"Using DRC JSON file: {path}")
            switches["drc_json"] = path
            break
    else:
        logging.error("No valid DRC JSON file found in any expected location.")
        raise FileNotFoundError("DRC JSON not found in user or fallback paths.")

    # Optional switches
    switches["run_mode"] = arguments.run_mode if arguments.run_mode else "deep"
    switches["MaxRuleSet"] = "true" if arguments.MaxRuleSet else "false"
    switches["no_feol"] = "true" if arguments.no_feol else "false"
    switches["no_beol"] = "true" if arguments.no_beol else "false"
    switches["no_offgrid"] = "true" if arguments.no_offgrid else "false"
    switches["no_connectivity"] = "true" if arguments.no_connectivity else "false"
    switches["density"] = "false" if arguments.no_density else "true"

    # Set topcell and input layout
    switches["topcell"] = get_run_top_cell_name(arguments, layout_path)
    switches["input"] = layout_path

    return switches


def check_klayout_version():
    """
    Checks if the installed KLayout version meets the minimum required version (>= 0.29.11).

    Raises
    ------
    SystemExit
        If KLayout is not installed or version is below the required minimum.
    """
    try:
        klayout_version_output = os.popen("klayout -b -v").read().strip()
    except Exception as e:
        logging.error(f"Error while checking KLayout version: {e}")
        exit(1)

    if not klayout_version_output:
        logging.error("KLayout is not found. Please make sure it is installed and in your PATH.")
        exit(1)

    version_str = klayout_version_output.split()[-1]
    version_parts = version_str.split(".")

    try:
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0
        patch = int(version_parts[2]) if len(version_parts) > 2 else 0
    except ValueError:
        logging.error(f"Failed to parse KLayout version string: '{klayout_version_output}'")
        exit(1)

    if (major, minor, patch) < (0, 29, 11):
        logging.error("Minimum required KLayout version is 0.29.11.")
        logging.error(f"Your version: {version_str}")
        exit(1)

    logging.info(f"KLayout version detected: {version_str}")


def check_layout_path(layout_path: str) -> str:
    """
    Validates that the layout file exists and is in supported format (GDS or OAS).

    Parameters
    ----------
    layout_path : str
        Path to the layout file provided by the user.

    Returns
    -------
    str
        Absolute path to the valid layout file.

    Raises
    ------
    SystemExit
        If the file does not exist or is not a supported layout format.
    """

    path = Path(layout_path)

    if not path.is_file():
        logging.error(f"Layout file path '{layout_path}' does not exist or is not a file.")
        exit(1)

    if not layout_path.endswith((".gds", ".oas")):
        logging.error(
            f"Layout '{layout_path}' is not in GDSII (.gds) or OASIS (.oas) format. Please use a supported format."
        )
        exit(1)

    return str(path.resolve())


def build_switches_string(sws: dict) -> str:
    """
    Build a command-line switch string from a dictionary of KLayout -rd options.

    Parameters
    ----------
    sws : dict
        Dictionary containing runtime variables to be passed as -rd to KLayout.

    Returns
    -------
    str
        A space-separated string of -rd key=value pairs.
    """
    return " ".join(f"-rd {k}={v}" for k, v in sws.items())


def run_check(
    drc_file: str,
    drc_table: str,
    layout_path: str,
    run_dir: Path,
    sws: dict,
) -> str:
    """
    Run a DRC check based on the provided DRC rule file.

    Parameters
    ----------
    drc_file : str
        Full path to the DRC rule deck file to run.
    drc_table : str
        Name of the DRC table (used in naming reports).
    layout_path : str
        Full path to the layout (GDS/OAS) file.
    run_dir : Path
        Output directory where reports and logs will be stored.
    sws : dict
        Dictionary containing runtime switches (e.g., topcell, threads, etc.).

    Returns
    -------
    str
        Path to the DRC results database generated by the run.
    """
    layout_name = Path(layout_path).stem
    topcell = sws["topcell"]

    logging.info(f"Running IHP-SG13G2 {drc_table} checks on design {layout_path}, topcell: {topcell}")

    report_path = run_dir / f"{layout_name}_{topcell}_{drc_table}.lyrdb"
    log_path = run_dir / f"{layout_name}_{topcell}_{drc_table}.log"
    new_sws = sws.copy()
    new_sws.update({
        "report": report_path,
        "log": log_path,
        "run_mode": sws["run_mode"]
    })

    sws_str = build_switches_string(new_sws)
    sws_str += f" -rd table_name={drc_table}"

    run_cmd = f"klayout -b -r {drc_file} {sws_str}"
    check_call(run_cmd, shell=True)

    return str(report_path)


def run_parallel_run(
    args,
    rule_deck_full_path: Path,
    layout_path: str,
    switches: dict,
    run_dir: Path,
):
    """
    Run DRC checks in parallel using multiple threads.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments.
    rule_deck_full_path : Path
        Path to the directory containing rule decks.
    layout_path : str
        Path to the layout file to be checked.
    switches : dict
        Dictionary of switches passed to KLayout.
    run_dir : Path
        Directory where DRC run output will be stored.
    """
    if args.macro_gen:
        generate_drc_run_template(rule_deck_full_path, run_dir)
        return 0

    rule_deck_files = {}

    # Optional checks
    if args.antenna:
        rule_deck_files["antenna"] = rule_deck_full_path / "rule_decks" / "antenna.drc"

    if not args.no_density:
        rule_deck_files["density"] = rule_deck_full_path / "rule_decks" / "density.drc"

    if args.MaxRuleSet:
        rule_deck_files["sg13g2_maximal"] = rule_deck_full_path / "rule_decks" / "sg13g2_maximal.drc"

    # Main table-based checks
    table_list = args.table if args.table else get_list_of_tables(rule_deck_full_path)
    for table in table_list:
        drc_file = generate_drc_run_template(rule_deck_full_path, run_dir, [table])
        rule_deck_files[table] = drc_file

    result_db_files = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers_count) as executor:
        future_to_name = {
            executor.submit(run_check, rule_file, name, layout_path, run_dir, switches): name
            for name, rule_file in rule_deck_files.items()
        }

        for future in concurrent.futures.as_completed(future_to_name):
            name = future_to_name[future]
            try:
                result_db_files.append(future.result())
            except Exception as e:
                logging.error(f"{name} generated an exception: {e}")
                traceback.print_exc()

    check_drc_results(result_db_files, run_dir, layout_path, switches)
    return 0


def run_single_processor(
    args,
    rule_deck_full_path: Path,
    layout_path: str,
    switches: Dict,
    run_dir: Path,
) -> int:
    """
    Runs the DRC checks as a single-threaded process.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments from the user.
    rule_deck_full_path : Path
        Path to the rule deck directory.
    layout_path : str
        Absolute path to the input layout (GDS/OAS).
    switches : dict
        Dictionary of KLayout switches.
    run_dir : Path
        Path to the output directory for this DRC run.
    """
    result_dbs: List[str] = []

    # Macro generation mode: generate rule deck and exit
    if args.macro_gen:
        generate_drc_run_template(rule_deck_full_path, run_dir)
        return 0

    def run_check_by_flag(flag_enabled: bool, name: str):
        """
        Helper to run an optional DRC check.
        """
        if flag_enabled:
            drc_path = rule_deck_full_path / "rule_decks" / f"{name}.drc"
            result_dbs.append(run_check(drc_path, name, layout_path, run_dir, switches))
            logging.info(f"Completed running {name.capitalize()} checks.")

    # Handle *_only flags (exclusive checks)
    if args.antenna_only:
        run_check_by_flag(True, "antenna")
        check_drc_results(result_dbs, run_dir, layout_path, switches)
        return 0

    if args.density_only:
        run_check_by_flag(True, "density")
        check_drc_results(result_dbs, run_dir, layout_path, switches)
        return 0

    # Run primary table check
    table_name = args.table[0] if args.table else "main"
    drc_file = generate_drc_run_template(rule_deck_full_path, run_dir, args.table)
    result_dbs.append(run_check(drc_file, table_name, layout_path, run_dir, switches))

    # Run additional checks if requested
    run_check_by_flag(args.antenna, "antenna")
    run_check_by_flag(not args.no_density, "density")
    run_check_by_flag(args.MaxRuleSet, "sg13g2_maximal")

    # Final result verification
    check_drc_results(result_dbs, run_dir, layout_path, switches)
    return 0


def main(run_dir: Path, args):
    """
    Main function to run the DRC regression.

    Parameters
    ----------
    run_dir : Path
        Absolute path of the run directory where outputs will be stored.
    args : argparse.Namespace
        Parsed command-line arguments containing user-provided options.
    """

    # Set multiprocessing to use 'spawn' — safer when called from GUI-based tools like KLayout
    mp.set_start_method("spawn", force=True)

    # Check that input GDS file exists
    if not Path(args.path).exists():
        logging.error(f"The input GDS file path '{args.path}' does not exist. Please recheck.")
        exit(1)

    # Get rule deck directory
    rule_deck_full_path = Path(__file__).resolve().parent

    # Verify KLayout version
    check_klayout_version()

    # Check layout file path and extension
    layout_path = check_layout_path(args.path)

    # Generate KLayout run switches from arguments
    switches = generate_klayout_switches(args, layout_path)

    # Choose between single-core and multi-core run
    if workers_count == 1 or args.antenna_only or args.density_only:
        run_single_processor(
            args, rule_deck_full_path, layout_path, switches, run_dir
        )
    else:
        run_parallel_run(
            args, rule_deck_full_path, layout_path, switches, run_dir
        )


def parse_args():
    USAGE = """
    run_drc.py (--help | -h)
    run_drc.py --path=<file_path>
            [--table=<table_name>]... [--mp=<num_cores>] [--run_dir=<run_dir_path>]
            [--topcell=<topcell_name>] [--run_mode=<mode>] [--drc_json=<json_path>]
            [--no_feol] [--no_beol] [--MaxRuleSet] [--no_connectivity] [--no_density]
            [--density_thr=<density_threads>] [--density_only] [--antenna]
            [--antenna_only] [--no_offgrid] [--macro_gen]
    """

    parser = argparse.ArgumentParser(
        description="Run IHP SG13G2 OpenSource DRC checks",
        usage=USAGE,
    )

    parser.add_argument(
        "--path", type=str, required=True,
        help="Path to the input GDS file to be processed."
    )

    parser.add_argument(
        "--table", action='append', default=[],
        help="DRC table name(s) to execute (e.g., activ, metal1). "
             "This option can be used multiple times."
    )

    parser.add_argument(
        "--mp", type=int, default=1,
        help="Number of parts to split the rule deck for parallel execution. [default: 1]"
    )

    parser.add_argument(
        "--run_dir", type=str, default=None,
        help="Dir to store all run results. If not specified, a timestamped dir under the current path will be used."
    )

    parser.add_argument(
        "--topcell", type=str,
        help="Top-level cell name to use from the input GDS."
    )

    parser.add_argument(
        "--density_thr",
        type=int,
        default=os.cpu_count(),
        help="Number of threads to use during the density run (default: number of CPU cores)."
    )

    parser.add_argument(
        "--run_mode", type=str, choices=["flat", "deep", "tiling"], default="deep",
        help="KLayout execution mode: flat, deep, or tiling. [default: deep]"
    )

    parser.add_argument(
        "--drc_json", type=str,
        help="Path to a JSON file that defines rule values to use."
    )

    parser.add_argument("--no_feol", action="store_true", help="Disable all FEOL-related DRC checks.")
    parser.add_argument("--no_beol", action="store_true", help="Disable all BEOL-related DRC checks.")
    parser.add_argument("--MaxRuleSet", action="store_true", help="Force execution of the full rule deck.")
    parser.add_argument("--no_connectivity", action="store_true", help="Skip connectivity-related rules.")
    parser.add_argument("--no_density", action="store_true", help="Disable density rule checks.")
    parser.add_argument("--density_only", action="store_true", help="Run only density rules.")
    parser.add_argument("--antenna", action="store_true", help="Enable antenna rule checks.")
    parser.add_argument("--antenna_only", action="store_true", help="Run only antenna rules.")
    parser.add_argument("--no_offgrid", action="store_true", help="Disable offgrid rule checks.")
    parser.add_argument("--macro_gen", action="store_true", help="Only generate the DRC rule deck without running.")

    return parser.parse_args()

# ================================================================
# -------------------------- MAIN --------------------------------
# ================================================================


if __name__ == "__main__":
    # Parse arguments using argparse
    args = parse_args()

    # Generate a timestamped run directory name
    now_str = datetime.now(timezone.utc).strftime("drc_run_%Y_%m_%d_%H_%M_%S")

    # Determine run directory
    if args.run_dir in ["pwd", "", None]:
        run_dir = Path.cwd().resolve() / now_str
    else:
        run_dir = Path(args.run_dir).resolve()

    os.makedirs(run_dir, exist_ok=True)

    # Configure logging to both file and console
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(run_dir / f"{now_str}.log"),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    # Determine number of workers
    workers_count = int(args.mp) if args.mp else os.cpu_count()

    # Record start time
    time_start = time.time()

    # Execute main flow
    main(run_dir, args)

    # Log total execution time
    elapsed_time = time.time() - time_start
    logging.info(
        f"Total DRC Run time: {elapsed_time:.2f} seconds (including execution, analysis, and reporting)"
    )
