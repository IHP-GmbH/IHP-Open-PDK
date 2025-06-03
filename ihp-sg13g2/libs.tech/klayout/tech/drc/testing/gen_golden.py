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
Run IHP-SG13G2 Golden DRC Results Generation

Usage:
    gen_golden.py (--help| -h)
    gen_golden.py [--table_name=<table_name>] [--run_dir=<dir>] [--mp=<num>] [--keep]

Options:
    --table_name=<table>   Target rule table name to generate golden results for.
    --run_dir=<dir>        Directory to store output.
    --mp=<num>             The number of cores used in run.
    --keep                 Keep output logs and intermediate files after processing.
"""

from subprocess import check_call
import concurrent.futures
import traceback
import yaml
from docopt import docopt
import os
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import time
import pandas as pd
import logging
import glob
from pathlib import Path
from tqdm import tqdm
import re
import gdstk
import klayout.db
import numpy as np
from fnmatch import fnmatch
import shutil


SUPPORTED_TC_EXT = "gds"
SUPPORTED_SW_EXT = "yaml"
GOLDEN_LAY_NUM = 222
PATH_WIDTH = 0.01


def check_klayout_version():
    """
    check_klayout_version checks KLayout version and ensures
    it meets the minimum required version for the DRC.
    """
    klayout_v_output = os.popen("klayout -b -v").read().strip()

    if not klayout_v_output:
        logging.error(
            "KLayout is not found. Please make sure KLayout is installed and accessible in PATH."
        )
        exit(1)

    version_str = klayout_v_output.split()[-1]  # Expecting format: 'KLayout 0.29.11'
    version_parts = version_str.split(".")

    try:
        klayout_v_list = [int(part) for part in version_parts]
    except ValueError:
        logging.error(f"Could not parse KLayout version from string: '{version_str}'")
        exit(1)

    # Pad to 3 parts if necessary
    while len(klayout_v_list) < 3:
        klayout_v_list.append(0)

    # Minimum required version: 0.29.11
    min_required = [0, 29, 11]
    if klayout_v_list < min_required:
        logging.error("Minimum required KLayout version is 0.29.11")
        logging.error(f"Your KLayout version is: {version_str}")
        exit(1)

    logging.info(f"KLayout version: {version_str}")


def clean_run_dir(run_dir):
    """
    Cleans the run_dir by:
    - Moving all *_golden_merged.gds files from subdirectories to the top level of run_dir.
    - Renaming them to remove duplicated name segments (e.g., activ_activ_golden_merged.gds → activ_golden_merged.gds).
    - Removing all other files and directories.
    """
    # Move and rename golden GDS files to top-level
    pattern_merged = "_golden_merged.gds"
    pattern_golden = "_golden.gds"
    for root, _, files in os.walk(run_dir):
        for file in files:
            if fnmatch(file, f"*{pattern_merged}"):
                src_path = os.path.join(root, file)

                # Simplify the filename if it has repeated parts
                name_parts = file.replace(pattern_merged, "").split("_")
                simplified_name = "_".join(dict.fromkeys(name_parts))
                new_name = f"{simplified_name}{pattern_golden}"

                dest_path = os.path.join(run_dir, new_name)

                try:
                    if os.path.abspath(src_path) != os.path.abspath(dest_path):
                        shutil.move(src_path, dest_path)
                    elif src_path != dest_path:
                        os.rename(src_path, dest_path)
                except Exception as e:
                    logging.warning(
                        f"Failed to move/rename {src_path} → {dest_path}: {e}"
                    )

    # Remove all files except simplified golden GDS files in top-level
    for root, dirs, files in os.walk(run_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if root != run_dir or not fnmatch(file, f"*{pattern_golden}"):
                try:
                    os.remove(file_path)
                except Exception as e:
                    logging.warning(f"Failed to remove file {file_path}: {e}")

    # Remove all subdirectories (bottom-up)
    for root, dirs, _ in os.walk(run_dir, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                shutil.rmtree(dir_path)
            except Exception as e:
                logging.warning(f"Failed to remove directory {dir_path}: {e}")


def merge_cells(input_dir, prefix, remove_org_gds=True):
    """
    Merges all GDS files in `input_dir` starting with `prefix` into a single GDS file.
    Each file contributes its top-level cell as a new top cell in the merged output.

    Parameters:
    - input_dir (str): Directory containing the GDS files.
    - prefix (str): File prefix (e.g., 'density_pass').
    - remove_org_gds (bool): If True, delete original GDS files after merging.
    """
    gds_files = [
        f for f in os.listdir(input_dir)
        if f.endswith(".gds") and f.startswith(f"{prefix}_")
    ]

    if not gds_files:
        return

    merged_lib = gdstk.Library()

    for filename in gds_files:
        filepath = os.path.join(input_dir, filename)
        gds_lib = gdstk.read_gds(filepath)

        # Derive the top cell name from the filename suffix
        suffix = filename[len(prefix) + 1:-4]  # Strip prefix + '_' and '.gds'
        top_cell = gds_lib.top_level()[0].copy(name=suffix)
        merged_lib.add(top_cell)

    # Write merged GDS output
    output_file = os.path.join(input_dir, f"{prefix}_golden.gds")
    merged_lib.write_gds(output_file)

    if remove_org_gds:
        for filename in gds_files:
            os.remove(os.path.join(input_dir, filename))


def generate_merged_testcase(original_testcase, marker_testcase, cell_name):
    """
    This function will merge original gds file with generated
    markers gds file.

    Parameters
    ----------
    original_testcase : str or Path object
        Path string to the original testcase
    marker_testcase : str or Path
        Path of the output marker gds file generated from db file.
    cell_name : string
        Cell name that we are running on.
    Returns
    -------
    merged_gds_path : str or Path
        Path of the final merged gds file generated.
    """

    new_lib = gdstk.Library()

    lib_org = gdstk.read_gds(original_testcase)
    lib_marker = gdstk.read_gds(marker_testcase)

    # Get all top-level cells
    top_cells = lib_org.top_level()
    # Try to find the top cell with the given name
    top_cell_org = next((cell for cell in top_cells if cell.name == cell_name), None)
    if top_cell_org is None:
        logging.warning(f"Top cell '{cell_name}' not found. Falling back to the first one.")
        top_cell_org = top_cells[0]
    # Flatten with repetitions
    top_cell_org = top_cell_org.flatten(apply_repetitions=True)
    logging.debug(f"Top cell from original testcase: {top_cell_org.name}")
    top_cell_marker = lib_marker.top_level()[0].flatten(apply_repetitions=True)
    marker_polygons = top_cell_marker.get_polygons(
        apply_repetitions=True, include_paths=True, depth=None
    )

    # Merging all polygons of markers with original testcase
    for marker_polygon in marker_polygons:
        top_cell_org.add(marker_polygon)

    # Adding flattened merged cell
    new_lib.add(top_cell_org.flatten(apply_repetitions=True))

    # Writing final merged gds file
    merged_gds_path = f'{marker_testcase.replace(".gds", "")}_merged.gds'
    new_lib.write_gds(merged_gds_path)

    return merged_gds_path


def draw_polygons(polygon_data, cell, lay_num, lay_dt, path_width):
    """
    This function is used for drawing gds file with all violated polygons.

    Parameters
    ----------
    polygon_data : str
        Contains data points for each violated polygon
    cell: gdstk.Cell
        Top cell will contains all generated polygons
    lay_num: int
        Number of layer used to draw violated polygons
    lay_dt : int
        Data type of layer used to draw violated polygons
    path_width : float
        Width  will used to draw edges

    Returns
    -------
    None
    """

    # Cleaning data points
    polygon_data = re.sub(r"\s+", "", polygon_data)
    polygon_data = re.sub(r"[()]", "", polygon_data)

    tag_split = polygon_data.split(":")
    tag = tag_split[0]
    poly_txt = tag_split[1]
    polygons = re.split(r"[/|]", poly_txt)

    # Select shape type to be drawn
    if tag == "polygon":
        for poly in polygons:
            points = [
                (float(p.split(",")[0]), float(p.split(",")[1]))
                for p in poly.split(";")
            ]
            cell.add(gdstk.Polygon(points, lay_num, lay_dt))

    elif tag == "edge-pair":
        for poly in polygons:
            points = [
                [float(p.split(",")[0]), float(p.split(",")[1])]
                for p in poly.split(";")
            ]
            dist = np.sqrt(
                ((points[0][0]) - (points[1][0])) ** 2
                + ((points[0][1]) - (points[1][1])) ** 2
            )
            # Adding condition for extremely small edge length
            # to generate a path to be drawn
            if dist < path_width:
                points[1][0] = points[0][0] + 2 * path_width
            cell.add(gdstk.FlexPath(points, path_width, layer=lay_num, datatype=lay_dt))

    elif tag == "edge":
        for poly in polygons:
            points = [
                [float(p.split(",")[0]), float(p.split(",")[1])]
                for p in poly.split(";")
            ]
            dist = np.sqrt(
                ((points[0][0]) - (points[1][0])) ** 2
                + ((points[0][1]) - (points[1][1])) ** 2
            )
            # Adding condition for extremely small edge length
            # to generate a path to be drawn
            if dist < path_width:
                points[1][0] = points[0][0] + 2 * path_width
            cell.add(gdstk.FlexPath(points, path_width, layer=lay_num, datatype=lay_dt))

    elif "float" in tag or "text" in tag:
        # Known antenna values for antenna ratios
        pass

    else:
        logging.error(f"# Unknown type: {tag} ignored")


def convert_db_to_gds(results_database: str):
    """
    This function will parse Klayout database for analysis.
    It converts the lyrdb klayout database file to GDSII file

    Parameters
    ----------
    results_database : str or Path object
        Path string to the results file

    Returns
    -------
    output_gds_path : str or Path
        Path of the output marker gds file generated from db file.
    output_runset_path : str or Path
        Path of the output drc runset used for analysis.
    """

    # Generating violated rules and its points
    cell_name = ""
    lib = None
    cell = None
    in_item = False
    rule_data_type_map = list()

    for ev, elem in tqdm(ET.iterparse(results_database, events=("start", "end"))):

        if elem.tag != "item" and not in_item:
            elem.clear()
            continue

        if elem.tag != "item" and in_item:
            continue

        if elem.tag == "item" and ev == "start":
            in_item = True
            continue

        rules = elem.findall("category")
        values = elem.findall("values")

        if len(values) > 0:
            polygons = values[0].findall("value")
        else:
            polygons = []

        if cell_name == "":
            all_cells = elem.findall("cell")

            if len(all_cells) > 0:
                cell_name = all_cells[0].text

                if cell_name is None:
                    elem.clear()
                    continue

                lib = gdstk.Library(f"{cell_name}_golden")
                cell = lib.new_cell(f"{cell_name}_golden")

        if len(rules) > 0:
            rule_name = re.sub(r"[^\w\-]", "_", rules[0].text.strip())
            if rule_name is None:
                elem.clear()
                continue
        else:
            elem.clear()
            continue

        if rule_name not in rule_data_type_map:
            rule_data_type_map.append(rule_name)

        # Drawing polygons here.
        rule_lay_dt = rule_data_type_map.index(rule_name) + 1

        if cell is not None:
            for p in polygons:
                draw_polygons(p.text, cell, GOLDEN_LAY_NUM, rule_lay_dt, PATH_WIDTH)

        # Clearing memory
        in_item = False
        elem.clear()

    # Writing final marker gds file
    if lib is not None:
        output_gds_path = f'{results_database.replace(".lyrdb", "")}_golden.gds'
        lib.write_gds(output_gds_path)
    else:
        logging.error(f"Failed to get any results in the {results_database} database.")
        return False

    return output_gds_path


def get_switches(yaml_file, testcase_basename):
    """Parse yaml file and extract switches data
    Parameters
    ----------
    yaml_file : str
            yaml config file path given py the user.
    testcase_basename : str
        Testcase name that we are running on.
    Returns
    -------
    yaml_dic : dictionary
            dictionary containing switches data.
    """

    # load yaml config data
    with open(yaml_file, "r") as stream:
        try:
            yaml_dic = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return [f"{param}={value}" for param, value in yaml_dic[testcase_basename].items()]


def run_test_case(
    drc_dir,
    layout_path,
    run_dir,
    testcase_basename,
    table_name,
    cell_name,
):
    """
    This function run a single test case using the correct DRC file.

    Parameters
    ----------
    drc_dir : str or Path
        Path to the location where all runsets exist.
    layout_path : stirng or Path object
        Path string to the layout of the test pattern we want to test.
    run_dir : stirng or Path object
        Path to the location where is the regression run is done.
    testcase_basename : str
        Testcase name that we are running on.
    table_name : str
        Table name that we are running on.
    cell_name : string
        Cell name that we are running on.

    Returns
    -------
    dict
        A dict with all rule counts
    """
    # Get switches used for each run
    sw_file = os.path.join(
        Path(layout_path.parent).absolute(), f"{testcase_basename}.{SUPPORTED_SW_EXT}"
    )

    if os.path.exists(sw_file):
        switches = " ".join(get_switches(sw_file, testcase_basename))
    else:
        switches = ""  # default switch

    # Adding switches for specific runsets
    if "antenna" in str(layout_path):
        switches += " --antenna_only"
    elif "density" in str(layout_path):
        switches += " --density_only"

    # Creating run folder structure
    pattern_name = f"{testcase_basename}_{cell_name}"
    output_loc = os.path.join(run_dir, table_name, cell_name)
    pattern_log = os.path.join(output_loc, f"{pattern_name}_drc.log")

    # command to run drc
    call_str = (
        f"python3 {drc_dir}/run_drc.py "
        f"--path={layout_path} "
        f"{switches} "
        f"--table={table_name} "
        f"--topcell={cell_name} "
        f"--run_dir={output_loc} "
        f"--run_mode=flat "
        f"> {pattern_log} 2>&1"
    )

    # Starting klayout run
    os.makedirs(output_loc, exist_ok=True)
    try:
        check_call(call_str, shell=True)
    except Exception as e:
        pattern_results = glob.glob(os.path.join(output_loc, f"{pattern_name}*.lyrdb"))
        if len(pattern_results) < 1:
            logging.error("%s generated an exception: %s" % (pattern_name, e))
            traceback.print_exc()
            raise Exception("Failed DRC run.")

    # dumping log into output to make CI have the log
    if os.path.isfile(pattern_log):
        logging.info("# Dumping drc run output log:")
        with open(pattern_log, "r") as f:
            for line in f:
                line = line.strip()
                logging.info(f"{line}")

    # Checking if run is completed or failed
    pattern_results = glob.glob(os.path.join(output_loc, f"{pattern_name}*.lyrdb"))

    if len(pattern_results) > 0:
        # db to gds conversion
        marker_output = convert_db_to_gds(pattern_results[0])

        # Generating merged testcase for violated rules
        generate_merged_testcase(layout_path, marker_output, cell_name)

    else:
        logging.error(
            f"No db results are generated for {layout_path}, please check logs."
        )
        return False


def run_all_test_cases(tc_df, drc_dir, run_dir, num_workers):
    """
    This function run all test cases from the input dataframe.

    Parameters
    ----------
    tc_df : pd.DataFrame
        DataFrame that holds all the test cases information for running.
    drc_dir : str or Path
        Path string to the location of the drc runsets.
    run_dir : str or Path
        Path string to the location of the testing code and output.
    num_workers : int
        Number of workers to use for running the regression.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with all test cases information post running.
    """

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_run_id = dict()
        for i, row in tc_df.iterrows():
            future_to_run_id[
                executor.submit(
                    run_test_case,
                    drc_dir,
                    row["test_path"],
                    run_dir,
                    row["testcase_basename"],
                    row["table_name"],
                    row["top_cell"],
                )
            ] = row["run_id"]


def build_tests_dataframe(unit_test_cases_dir, target_table):
    """
    This function is used for getting all test cases available
    in a formatted dataframe before running.

    Parameters
    ----------
    unit_test_cases_dir : str
        Path string to the location of unit test cases path.
    target_table : str or None
        Name of table that we want to run regression for. If None, run all found.

    Returns
    -------
    pd.DataFrame
        A DataFrame that has all the targeted test cases that we need to run.
    """
    all_unit_test_cases = sorted(
        Path(unit_test_cases_dir).rglob("*.{}".format(SUPPORTED_TC_EXT))
    )

    logging.info(
        "# Total number of test cases found: {}".format(len(all_unit_test_cases))
    )

    # Get test cases df from test cases
    tc_df = pd.DataFrame({"test_path": all_unit_test_cases})
    tc_df["testcase_basename"] = tc_df["test_path"].apply(
        lambda x: x.name.replace(".gds", "")
    )
    tc_df["table_name"] = tc_df["testcase_basename"].apply(lambda x: x.split("_")[0])

    # Updating some table names
    tc_df["table_name"] = tc_df["table_name"].replace(
        {r"^via[2-4]$": "vian", r"^metal[2-5]$": "metaln"}, regex=True
    )

    if target_table is not None:
        tc_df = tc_df[tc_df["table_name"] == target_table]

    if len(tc_df) < 1:
        logging.error("No test cases exist for generation, please check.")
        exit(1)

    # Expand rows to one per top cell
    expanded_rows = []
    for _, row in tc_df.iterrows():
        top_cells = get_top_cell_names(row["test_path"])
        for cell in top_cells:
            new_row = row.copy()
            new_row["top_cell"] = cell
            expanded_rows.append(new_row)

    # Create expanded DataFrame
    expanded_df = pd.DataFrame(expanded_rows)
    expanded_df.reset_index(drop=True, inplace=True)
    expanded_df["run_id"] = range(len(expanded_df))

    return expanded_df


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


def gen_golden(drc_dir, output_path, target_table, cpu_count):
    """
    Running Golden Results Generation Procedure.

    This function generate the drc golden results for selected tests.

    Parameters
    ----------
    drc_dir : str
        Path string to the DRC directory where all the DRC files are located.
    output_path : str
        Path string to the location of the output results of the run.
    target_table : str or None
        Name of table that we want to run regression for. If None, run all found.
    cpu_count : int
        Number of cores to use in running testcases.
    Returns
    -------
    bool
        If all regression passed, it returns true. If any of the rules failed it returns false.
    """

    # Get all test cases available in the repo.
    unit_tests_path = os.path.join(drc_dir, "testing", "testcases", "unit")
    tc_df = build_tests_dataframe(unit_tests_path, target_table)
    logging.info("# Total table gds files found: {}".format(len(tc_df)))
    logging.info("# Found testcases: \n" + str(tc_df))

    # Run all test cases.
    run_all_test_cases(tc_df, drc_dir, output_path, cpu_count)


def main(drc_dir: str, output_path: str, target_table: str):
    """
    Main Procedure.

    This function is the main execution procedure

    Parameters
    ----------
    drc_dir : str
        Path string to the DRC directory where all the DRC files are located.
    output_path : str
        Path string to the location of the output results of the run.
    target_table : str or None
        Name of table that we want to run regression for. If None, run all found.
    Returns
    -------
    bool
        If all regression passed, it returns true. If any of the rules failed it returns false.
    """

    # No. of threads
    cpu_count = os.cpu_count() if arguments["--mp"] is None else int(arguments["--mp"])

    # Pandas printing setup
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("max_colwidth", None)
    pd.set_option("display.width", 1000)

    # info logs for args
    logging.info(f"# === Run folder is: {output_path}")
    logging.info(f"# === Target Table is: {target_table}")

    # Start of execution time
    time_start = time.time()

    # Check Klayout version
    check_klayout_version()

    # Calling regression function
    gen_golden(drc_dir, output_path, target_table, cpu_count)

    # keep output dir
    keep = arguments["--keep"]

    if not keep:
        logging.info(
            f"Cleaning {output_path} and preserving only *_golden_merged.gds files.."
        )
        clean_run_dir(output_path)
        merge_cells(output_path, "density_pass")
        merge_cells(output_path, "density_fail")

    #  End of execution time
    logging.info(f"Total execution time {time.time() - time_start}s")


# ================================================================
# -------------------------- MAIN --------------------------------
# ================================================================


if __name__ == "__main__":

    # arguments
    arguments = docopt(__doc__, version="Gen Golden DRC Results: 1.0")

    # run dir format
    now_str = datetime.now(timezone.utc).strftime("gen_golden_%Y_%m_%d_%H_%M_%S")

    # Paths of regression dirs
    testing_dir = os.path.dirname(os.path.abspath(__file__))
    drc_dir = os.path.dirname(testing_dir)

    if (
        arguments["--run_dir"] == "pwd"
        or arguments["--run_dir"] == ""
        or arguments["--run_dir"] is None
    ):
        output_path = os.path.join(testing_dir, "testcases", "unit_golden")
    else:
        output_path = os.path.abspath(arguments["--run_dir"])

    # target table
    target_table = arguments["--table_name"]

    # Creating output dir
    os.makedirs(output_path, exist_ok=True)

    # logs format
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(os.path.join(output_path, f"{now_str}.log")),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | [%(threadName)s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    # Calling main function
    main(drc_dir, output_path, target_table)
