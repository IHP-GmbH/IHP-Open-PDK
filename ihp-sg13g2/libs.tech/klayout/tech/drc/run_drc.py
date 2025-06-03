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
Run IHP SG13G2 OpenSource DRC.

Usage:
    run_drc.py (--help| -h)
    run_drc.py (--path=<file_path>) [--table=<table_name>]... [--mp=<num_cores>] [--run_dir=<run_dir_path>]
    [--topcell=<topcell_name>] [--thr=<thr>] [--run_mode=<run_mode>] [--drc_json=<json_path>] [--no_feol]
    [--no_beol] [--MaxRuleSet] [--no_connectivity] [--density] [--density_only] [--antenna] [--antenna_only]
    [--no_offgrid] [--macro_gen]

Options:
    --help -h                           Displays this help message.
    --path=<file_path>                  Specifies the file path of the input GDS file.
    --topcell=<topcell_name>            Specifies the name of the top cell to be used.
    --table=<table_name>                Specifies the name of the table on which to execute the rule deck.
    --mp=<num_cores>                    Run the rule deck in parts in parallel to speed up the run. [default: 1]
    --run_dir=<run_dir_path>            un directory to save all the generated results [default: pwd]
    --thr=<thr>                         Specifies the number of threads to use during the run.
    --run_mode=<run_mode>               Selects the allowed KLayout mode, (flat , deep, tiling). [default: deep]
    --drc_json=<json_path>              Path to the JSON file that contains the DRC rules values to be used.
    --no_feol                           Disables FEOL rules from running.
    --no_beol                           Disables BEOL rules from running.
    --MaxRuleSet                        Runs DRC using the complete rule deck.
    --no_connectivity                   Disables connectivity rules.
    --density                           Enables Density rules.
    --density_only                      Runs Density rules only.
    --antenna                           Enables Antenna checks.
    --antenna_only                      Runs Antenna checks only.
    --no_offgrid                        Disables OFFGRID checking rules.
    --macro_gen                         Generating the full rule deck without run.
"""


from docopt import docopt
import os
import xml.etree.ElementTree as ET
import logging
import klayout.db
import glob
from datetime import datetime, timezone
from subprocess import check_call
import shutil
import concurrent.futures
import traceback
from typing import Dict, List


def get_rules_with_violations(results_database):
    """
    This function will find all the rules that has violated in a database.

    Parameters
    ----------
    results_database : string or Path object
        Path string to the results file

    Returns
    -------
    set
        A set that contains all rules in the database with violations
    """

    mytree = ET.parse(results_database)
    myroot = mytree.getroot()

    all_violating_rules = set()

    for z in myroot[7]:  # myroot[7] : List rules with viloations
        all_violating_rules.add(f"{z[1].text}".replace("'", ""))

    return all_violating_rules


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

            # Append each <item> from this file
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
    results_db_files: list, run_dir: str, layout_path: str, switches: dict = None
):
    """
    check_drc_results Checks the results db generated from run and report at the end if the DRC run failed or passed.
    This function will exit with 1 if there are violations.

    Parameters
    ----------
    results_db_files : list
        A list of strings that represent paths to results databases of all the DRC runs.
    run_dir : str
        Absolute path string to the run location where all the run output will be generated.
    layout_path : string
        Path to the target layout.
    switches (dict): Switches to be passed to klayout.
    """

    if len(results_db_files) < 1:
        logging.error("Klayout did not generate any rdb results. Please check run logs")
        exit(1)

    if len(results_db_files) > 1:
        layout_name = os.path.basename(layout_path).split(".")[0]
        topcell = switches["topcell"]
        report_path = os.path.join(run_dir, f"{layout_name}_{topcell}_full.lyrdb")
        merge_klayout_drc_reports(results_db_files, report_path)
        list(map(os.remove, [f for f in results_db_files if f != report_path]))
    else:
        report_path = results_db_files[0]

    # Get violating rules
    violating_rules = get_rules_with_violations(report_path)

    if len(violating_rules) > 0:
        logging.error(
            "=================================================================================="
        )
        logging.error(
            "❌ --- KLayout DRC Check Failed. DRC violations detected in the GDS layout. --- ❌"
        )
        logging.error(
            "=================================================================================="
        )
        logging.error(f"Violated rules are : {str(violating_rules)}\n")
    else:
        logging.info(
            "====================================================================================="
        )
        logging.info(
            "✅ --- KLayout DRC Check Passed: No DRC violations detected in the GDS layout. --- ✅"
        )
        logging.info(
            "====================================================================================="
        )


def generate_drc_run_template(drc_dir: str, run_dir: str, run_tables_list: list = []):
    """
    generate_drc_run_template will generate the template file to run drc in the run_dir path.

    Parameters
    ----------
    drc_dir : str
        Path string to the location where the DRC files would be found to get the list of the rule tables.
    run_dir : str
        Absolute path string to the run location where all the run output will be generated.
    deck_name : str, optional
        Name of the rule deck to use for generating the template, by default ""
    run_tables_list : list, optional
        list of target parts of the rule deck, if empty assume all of the rule tables found, by default []

    Returns
    -------
    str
        Absolute path to the generated DRC file.
    """
    drc_files = glob.glob(os.path.join(drc_dir, "rule_decks", "*.drc"))
    if len(run_tables_list) < 1:
        all_tables = [
            os.path.basename(f)
            for f in drc_files
            if "antenna" not in f
            and "density" not in f
            and "maximal" not in f
            and "main" not in f
            and "layers_def" not in f
            and "tail" not in f
        ]
        # Sort by the numeric prefix
        all_tables.sort(
            key=lambda name: (
                (
                    int(name.split("_")[0])
                    if name.split("_")[0].isdigit()
                    else float("inf")
                ),
                (
                    int(name.split("_")[1])
                    if len(name.split("_")) > 1 and name.split("_")[1].isdigit()
                    else float("inf")
                ),
            )
        )
        deck_name = "main"
    elif len(run_tables_list) == 1:
        deck_name = str(run_tables_list[0]).split("_")[-1]
        drc_decks = [os.path.basename(f) for f in drc_files]
        all_tables = [d for d in drc_decks if d.split("_")[-1] == f"{deck_name}.drc"]
    else:
        deck_name = "main"
        drc_decks = [os.path.basename(f) for f in drc_files]
        all_tables = [
            d for d in drc_decks if any(f"{t}.drc" in d for t in run_tables_list)
        ]
        print(all_tables)

    logging.info(
        f"# Generating template with for the following rule tables: {all_tables}"
    )
    logging.info(f"# Your run dir located at: {run_dir}")

    all_tables.insert(0, "main.drc")
    all_tables.append("tail.drc")

    # Adding layers_def to run  dir to used in main rule deck
    lyrs_def_path = os.path.join(drc_dir, "rule_decks", "layers_def.drc")
    lyrs_def_loc = os.path.join(run_dir, "layers_def.drc")
    shutil.copyfile(lyrs_def_path, lyrs_def_loc)

    gen_rule_deck_path = os.path.join(run_dir, "{}.drc".format(deck_name))
    with open(gen_rule_deck_path, "wb") as wfd:
        for f in all_tables:
            with open(os.path.join(drc_dir, "rule_decks", f), "rb") as fd:
                shutil.copyfileobj(fd, wfd)

    return gen_rule_deck_path


def get_top_cell_names(gds_path):
    """
    get_top_cell_names get the top cell names from the GDS file.

    Parameters
    ----------
    gds_path : string
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

    exc_list = ("antenna", "density", "maximal", "main", "layers_def", "tail")
    if arguments["--run_mode"] == "flat":
        return [
            os.path.basename(f).replace(".drc", "")
            for f in glob.glob(os.path.join(drc_dir, "rule_decks", "*.drc"))
            if all(t not in f for t in exc_list)
        ]
    else:
        return [
            os.path.basename(f).replace(".drc", "")
            for f in glob.glob(os.path.join(drc_dir, "rule_decks", "*.drc"))
            if all(t not in f for t in exc_list)
        ]


def get_run_top_cell_name(arguments, layout_path):
    """
    get_run_top_cell_name Get the top cell name to use for running. If it's provided by the user, we use the user input.
    If not, we get it from the GDS file.

    Parameters
    ----------
    arguments : dict
        Dictionary that holds the user inputs for the script generated by docopt.
    layout_path : string
        Path to the target layout.

    Returns
    -------
    string
        Name of the topcell to use in run.

    """

    if arguments["--topcell"]:
        topcell = arguments["--topcell"]
    else:
        layout_topcells = get_top_cell_names(layout_path)
        if len(layout_topcells) > 1:
            logging.error(
                "# Layout has multiple topcells. Please use --topcell to determine which topcell you want to run on."
            )
            exit(1)
        else:
            topcell = layout_topcells[0]

    return topcell


def generate_klayout_switches(arguments, layout_path):
    """
    parse_switches Function that parse all the args from input to prepare switches for DRC run.

    Parameters
    ----------
    arguments : dict
        Dictionary that holds the arguments used by user in the run command. This is generated by docopt library.
    layout_path : string
        Path to the layout file that we will run DRC on.

    Returns
    -------
    dict
        Dictionary that represent all run switches passed to klayout.
    """
    switches = dict()

    # No. of threads
    thrCount = 2 if arguments["--thr"] is None else int(arguments["--thr"])
    switches["thr"] = str(int(thrCount))

    if arguments["--run_mode"] not in ["flat", "deep"]:
        logging.error("Allowed klayout modes are (flat , deep) only")
        exit(1)

    # JSON file with DRC rules values
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tech_rule_path = os.path.abspath(
        os.path.join(script_dir, "../../python/sg13g2_pycell_lib/sg13g2_tech.json")
    )
    default_rule_path = os.path.abspath(
        os.path.join(script_dir, "rule_decks/sg13g2_tech_default.json")
    )

    # Always assign default path
    switches["drc_json_default"] = default_rule_path

    # Determine candidate paths in priority order
    if arguments["--drc_json"]:
        user_path = arguments["--drc_json"]
        logging.info(f"User provided JSON for DRC rules values: {user_path}")
        candidate_paths = [user_path, tech_rule_path, default_rule_path]
    else:
        logging.warning(
            "No --drc_json option provided; falling back to predefined json file paths."
        )
        candidate_paths = [tech_rule_path, default_rule_path]

    # Find the first existing file
    for path in candidate_paths:
        if os.path.isfile(path):
            logging.info(f"Using DRC JSON file: {path}")
            switches["drc_json"] = path
            break
    else:
        logging.error("No valid DRC JSON file found in provided or fallback locations.")
        raise FileNotFoundError(
            "DRC rules JSON not found in any of the expected paths."
        )

    # Enable maximum runset
    if arguments["--MaxRuleSet"]:
        switches["MaxRuleSet"] = "true"
    else:
        switches["MaxRuleSet"] = "false"

    if arguments["--no_feol"]:
        switches["no_feol"] = "true"
    else:
        switches["no_feol"] = "false"

    if arguments["--no_beol"]:
        switches["no_beol"] = "true"
    else:
        switches["no_beol"] = "false"

    if arguments["--no_offgrid"]:
        switches["no_offgrid"] = "true"
    else:
        switches["no_offgrid"] = "false"

    if arguments["--no_connectivity"]:
        switches["no_connectivity"] = "true"
    else:
        switches["no_connectivity"] = "false"

    if arguments["--density"]:
        switches["density"] = "true"
    else:
        switches["density"] = "false"

    switches["topcell"] = get_run_top_cell_name(arguments, layout_path)
    switches["input"] = layout_path

    return switches


def check_klayout_version():
    """
    check_klayout_version checks klayout version and makes sure it would work with the DRC.
    """
    # ======= Checking Klayout version =======
    klayout_v_ = os.popen("klayout -b -v").read()
    klayout_v_ = klayout_v_.split("\n")[0]
    klayout_v_list = []

    if klayout_v_ == "":
        logging.error("Klayout is not found. Please make sure klayout is installed.")
        exit(1)
    else:
        klayout_v_list = [int(v) for v in klayout_v_.split(" ")[-1].split(".")]

    if len(klayout_v_list) < 1 or len(klayout_v_list) > 3:
        logging.error("Was not able to get klayout version properly.")
        exit(1)
    elif len(klayout_v_list) >= 2 and len(klayout_v_list) <= 3:
        if klayout_v_list[1] < 29 or (
            klayout_v_list[1] == 29 and klayout_v_list[2] < 11
        ):
            logging.error("Prerequisites at a minimum: KLayout 0.29.11")
            logging.error(
                "Using this klayout version is not supported in this development."
            )
            exit(1)

    logging.info(f"Your Klayout version is: {klayout_v_}")


def check_layout_path(layout_path):
    """
    check_layout_type checks if the layout provided is GDS or OAS.
    Otherwise, kill the process. We only support GDS or OAS now.

    Parameters
    ----------
    layout_path : string
        string that represent the path of the layout.

    Returns
    -------
    string
        string that represent full absolute layout path.
    """

    if not os.path.isfile(layout_path):
        logging.error(
            f"# GDS file path {layout_path} provided doesn't exist or not a file."
        )
        exit(1)

    if ".gds" not in layout_path and ".oas" not in layout_path:
        logging.error(
            f"# Layout {layout_path} is not in GDSII or OASIS format. Please use gds format."
        )
        exit(1)

    return os.path.abspath(layout_path)


def build_switches_string(sws: dict):
    """
    build_switches_string Build swtiches string from dictionary.

    Parameters
    ----------
    sws : dict
        Dictionary that holds the Antenna swithces.
    """
    return " ".join(f"-rd {k}={v}" for k, v in sws.items())


def run_check(drc_file: str, drc_table: str, path: str, run_dir: str, sws: dict):
    """
    run_antenna_check run DRC check based on DRC file provided.

    Parameters
    ----------
    drc_file : str
        String that has the file full path to run.
    drc_table : str
        str that holds the name of drc table to be run.
    path : str
        String that holds the full path of the layout.
    run_dir : str
        String that holds the full path of the run location.
    sws : dict
        Dictionary that holds all switches that needs to be passed to the antenna checks.

    Returns
    -------
    string
        string that represent the path to the results output database for this run.

    """

    # Using print because of the multiprocessing
    logging.info(
        "Running IHP-SG13G2 {} checks on design {} on cell {}:".format(
            path, drc_table, sws["topcell"]
        )
    )
    layout_name = os.path.basename(path).split(".")[0]
    topcell = sws["topcell"]
    report_path = os.path.join(run_dir, f"{layout_name}_{topcell}_{drc_table}.lyrdb")
    new_sws = sws.copy()
    new_sws["report"] = report_path
    new_sws["run_mode"] = arguments["--run_mode"]
    sws_str = build_switches_string(new_sws)
    sws_str += f" -rd table_name={drc_table}"

    run_str = f"klayout -b -r {drc_file} {sws_str}"
    check_call(run_str, shell=True)

    return report_path


def run_parallel_run(
    arguments: dict,
    rule_deck_full_path: str,
    layout_path: str,
    switches: dict,
    run_dir: str,
):
    """
    Run DRC checks in parallel using multiple threads.

    Parameters
    ----------
    arguments (dict): Arguments passed to the run_drc script.
    rule_deck_full_path (str): Path to the base dir containing rule decks.
    layout_path (str): Path to the layout file to be checked.
    switches (dict): Switches to be passed to klayout.
    run_dir (str): Path where the DRC run output will be stored.
    """
    if arguments.get("--macro_gen"):
        generate_drc_run_template(rule_deck_full_path, run_dir)
        return 0

    rule_deck_files = {}

    # Handle Antenna check
    if arguments.get("--antenna"):
        antenna_path = os.path.join(rule_deck_full_path, "rule_decks", "antenna.drc")
        rule_deck_files["antenna"] = antenna_path

    # Handle Density check
    if arguments.get("--density"):
        density_path = os.path.join(rule_deck_full_path, "rule_decks", "density.drc")
        rule_deck_files["density"] = density_path

    # Handle maximum check
    if arguments.get("--MaxRuleSet"):
        max_rules_path = os.path.join(
            rule_deck_full_path, "rule_decks", "sg13g2_maximal.drc"
        )
        rule_deck_files["sg13g2_maximal"] = max_rules_path

    # Determine tables to run
    if arguments.get("--table"):
        table_list = arguments["--table"]
    else:
        table_list = get_list_of_tables(rule_deck_full_path)

    # Generate DRC templates for each table
    for table in table_list:
        drc_file = generate_drc_run_template(rule_deck_full_path, run_dir, [table])
        rule_deck_files[table] = drc_file

    result_db_files = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers_count) as executor:
        future_to_name = {
            executor.submit(
                run_check, rule_file, name, layout_path, run_dir, switches
            ): name
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


def run_single_processor(
    arguments: Dict,
    rule_deck_full_path: str,
    layout_path: str,
    switches: Dict,
    run_dir: str,
) -> int:
    """
    Runs the DRC checks as a single process.

    Parameters
    ----------
    arguments : dict
        CLI arguments passed to the run_drc script.
    rule_deck_full_path : str
        Path to the rule deck directory.
    layout_path : str
        Path to the layout file (GDS/OAS).
    switches : dict
        Dictionary of switches passed to klayout.
    run_dir : str
        Output directory for the DRC run.
    """
    result_dbs: List[str] = []

    # Macro mode: generate rule deck only
    if arguments.get("--macro_gen"):
        generate_drc_run_template(rule_deck_full_path, run_dir)
        return 0

    def run_check_by_flag(flag: str, name: str):
        """
        Utility to run optional check based on the flag.
        """
        drc_path = os.path.join(rule_deck_full_path, "rule_decks", f"{name}.drc")
        result_dbs.append(run_check(drc_path, name, layout_path, run_dir, switches))
        logging.info(f"Completed running {name.capitalize()} checks.")

    # Handle *_only flags first: run that check and skip all others
    if arguments.get("--antenna_only"):
        run_check_by_flag("--antenna_only", "antenna")
        check_drc_results(result_dbs, run_dir, layout_path, switches)
        return 0

    if arguments.get("--density_only"):
        run_check_by_flag("--density_only", "density")
        check_drc_results(result_dbs, run_dir, layout_path, switches)
        return 0

    # Run main table check
    table_arg = arguments.get("--table")
    drc_file = generate_drc_run_template(rule_deck_full_path, run_dir, table_arg)
    table_name = table_arg[0] if table_arg else "main"

    result_dbs.append(run_check(drc_file, table_name, layout_path, run_dir, switches))

    # Run additional checks if requested
    if arguments.get("--antenna"):
        run_check_by_flag("--antenna", "antenna")

    if arguments.get("--density"):
        run_check_by_flag("--density", "density")

    if arguments.get("--MaxRuleSet"):
        run_check_by_flag("--MaxRuleSet", "sg13g2_maximal")

    # Final result verification
    check_drc_results(result_dbs, run_dir, layout_path, switches)
    return 0


def main(run_dir: str, arguments: dict):
    """
    main function to run the DRC.

    Parameters
    ----------
    run_dir : str
        String with absolute path of the full run dir.
    arguments : dict
        Dictionary that holds the arguments used by user in the run command. This is generated by docopt library.
    """

    # Check gds file existance
    if not os.path.exists(arguments["--path"]):
        file_path = arguments["--path"]
        logging.error(
            f"The input GDS file path {file_path} doesn't exist, please recheck."
        )
        exit(1)

    rule_deck_full_path = os.path.dirname(os.path.abspath(__file__))

    # Check Klayout version
    check_klayout_version()

    # Check if there was a layout provided.
    if not arguments["--path"]:
        logging.error("No provided gds file, please add one")
        exit(1)

    # Check layout type
    layout_path = arguments["--path"]
    layout_path = check_layout_path(layout_path)

    # Get run switches
    switches = generate_klayout_switches(arguments, layout_path)

    if workers_count == 1 or arguments["--antenna_only"] or arguments["--density_only"]:
        run_single_processor(
            arguments, rule_deck_full_path, layout_path, switches, run_dir
        )
    else:
        run_parallel_run(arguments, rule_deck_full_path, layout_path, switches, run_dir)


# ================================================================
# -------------------------- MAIN --------------------------------
# ================================================================

if __name__ == "__main__":

    # arguments
    arguments = docopt(__doc__, version="RUN DRC: 1.0")

    # run dir format
    now_str = datetime.now(timezone.utc).strftime("drc_run_%Y_%m_%d_%H_%M_%S")

    if (
        arguments["--run_dir"] == "pwd"
        or arguments["--run_dir"] == ""
        or arguments["--run_dir"] is None
    ):
        run_dir = os.path.join(os.path.abspath(os.getcwd()), now_str)
    else:
        run_dir = os.path.abspath(arguments["--run_dir"])

    os.makedirs(run_dir, exist_ok=True)

    # logs format
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(os.path.join(run_dir, "{}.log".format(now_str))),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    workers_count = int(arguments["--mp"]) if arguments["--mp"] else os.cpu_count()

    # Calling main function
    main(run_dir, arguments)
