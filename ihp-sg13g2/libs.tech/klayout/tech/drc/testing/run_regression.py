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

from subprocess import check_call
import concurrent.futures
import traceback
import yaml
import argparse
import os
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import time
import pandas as pd
import logging
from pathlib import Path
from tqdm import tqdm
import re
import gdstk
import klayout.db
import errno
import numpy as np
from collections import defaultdict
from itertools import product


SUPPORTED_TC_EXT = "gds"
SUPPORTED_SW_EXT = "yaml"
GOLDEN_LAY_NUM = 222
VIOL_LAY_NUM = 333
PATH_WIDTH = 0.01
RULE_SEP = "--"
ANALYSIS_RULES = [
    "viol_not_golden",
    "golden_not_viol",
]
RULES_VAR = {
    "met_no": ("2", "3", "4", "5"),
    "via_no": ("2", "3", "4"),
    "metalfiller_no": ("1", "2", "3", "4", "5"),
    "slt_met": ("M1", "M2", "M3", "M4", "M5", "TM1", "TM2"),
    "pin_rule": ("a", "b", "e", "f_M2", "f_M3", "f_M4", "f_M5", "g", "h"),
    "forb_lay": (
        "baspoly",
        "biwind",
        "colwind",
        "deepco",
        "empoly",
        "flash",
        "ldmos",
        "nodrc",
        "pemwind",
        "pbiwind",
        "pempoly",
    ),
    "sealb_lay": (
        "metal1",
        "metal2",
        "metal3",
        "metal4",
        "metal5",
        "topmetal1",
        "topmetal2",
        "activ",
        "psd",
    ),
}


def get_unit_test_coverage(gds_file):
    """
    This function is used for getting all test cases available inside a single test table.
    Parameters
    ----------
    gds_file : str
        Path string to the location of unit test cases path.
    Returns
    -------
    list
        A list of unique rules found.
    """
    # Get rules from gds
    rules = []

    # layer num of rule text
    lay_num = 11
    # layer data type of rule text
    lay_dt = 222

    # Getting all rules names from testcase
    library = gdstk.read_gds(gds_file)
    top_cells = library.top_level()  # Get top cells
    for cell in top_cells:
        flatten_cell = cell.flatten()
        # Get all text labels for each cell
        labels = flatten_cell.get_labels(
            apply_repetitions=True, depth=None, layer=lay_num, texttype=lay_dt
        )
        # Get label value
        for label in labels:
            rule = label.text
            if rule not in rules:
                rules.append(rule)

    return rules


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


def get_switches(yaml_file, rule_name):
    """Parse yaml file and extract switches data
    Parameters
    ----------
    yaml_file : str
            yaml config file path given py the user.
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

    return [f"{param}={value}" for param, value in yaml_dic[rule_name].items()]


def parse_results_db(results_database):
    """
    This function will parse Klayout database for analysis.

    Parameters
    ----------
    results_database : string or Path object
        Path string to the results file

    Returns
    -------
    set
        A set that contains all rules in the database with or without violations
    """

    mytree = ET.parse(results_database)
    myroot = mytree.getroot()

    # Initial values for counter
    rule_counts = defaultdict(int)

    # Get the list of all rules that ran regardless it generated output or not
    for z in myroot[5]:
        rule_name = f"{z[0].text}"
        rule_counts[rule_name] = 0

    # Count rules with violations.
    for z in myroot[7]:
        rule_name = f"{z[1].text}".replace("'", "")
        rule_counts[rule_name] += 1

    return rule_counts


def parse_results_db_splitted(results_database):
    """
    This function will parse Klayout database for analysis.

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


def analyze_splitted_results(layout_path, pattern_results, cell_name, test_criteria):
    """
    This function run a single test case using the correct DRC file.

    Parameters
    ----------
    layout_path : str or Path object
        Path string to the layout of the test pattern we want to test.
    pattern_results : str or Path object
        Path to the location where is the result db file of DRC run is generated.
    cell_name : str
        Name of the top cell that we are running on.
    test_criteria : string
        Type of test that we are running on.

    Returns
    -------
    dict
        A dict with all rule counts
    """

    # Initial value for counters
    rule_results = defaultdict(int)

    if len(pattern_results) > 0:
        violated_rules = set()
        for p in pattern_results:
            rules_with_violations = parse_results_db_splitted(p)
            violated_rules.update(rules_with_violations)

        if test_criteria == "pass":
            if cell_name in violated_rules:
                # false positive
                return {
                    f"{cell_name}{RULE_SEP}{ANALYSIS_RULES[0]}": 1,
                    f"{cell_name}{RULE_SEP}{ANALYSIS_RULES[1]}": 0,
                }
            else:
                # true positive
                return {
                    f"{cell_name}{RULE_SEP}{ANALYSIS_RULES[0]}": 0,
                    f"{cell_name}{RULE_SEP}{ANALYSIS_RULES[1]}": 0,
                }
        else:
            if cell_name in violated_rules:
                # true negative
                return {
                    f"{cell_name}{RULE_SEP}{ANALYSIS_RULES[0]}": 0,
                    f"{cell_name}{RULE_SEP}{ANALYSIS_RULES[1]}": 0,
                }
            else:
                # false negative
                return {
                    f"{cell_name}{RULE_SEP}{ANALYSIS_RULES[0]}": 0,
                    f"{cell_name}{RULE_SEP}{ANALYSIS_RULES[1]}": 1,
                }
    else:
        return rule_results


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


def run_test_case(
    drc_dir: Path,
    layout_path: str,
    run_dir: Path,
    testcase_basename: str,
    table_name: str,
    cell_name: str,
    test_criteria: str,
):
    """
    This function run a single test case using the correct DRC file.

    Parameters
    ----------
    drc_dir : Path
        Path to the location where all runset exist.
    layout_path : string or Path object
        Path string to the layout of the test pattern we want to test.
    run_dir : Path
        Path to the location where is the regression run is done.
    testcase_basename : str
        Testcase name that we are running on.
    table_name : str
        Table name that we are running on.
    cell_name : str
        Cell name that we are running on.
    test_criteria : str
        Type of test that we are running on.

    Returns
    -------
    dict
        A dict with all rule counts
    """

    # Initial value for counters
    rule_counts = defaultdict(int)

    # Get switches used for each run
    sw_file = Path(layout_path.parent).absolute() / f"{testcase_basename}.{SUPPORTED_SW_EXT}"

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
    output_loc = run_dir / table_name / cell_name
    pattern_log = output_loc / f"{pattern_name}_drc.log"

    # command to run drc
    call_str = (
        f"python3 {drc_dir}/run_drc.py "
        f"--path={layout_path} "
        f"{switches} "
        f"--table={table_name} "
        f"--topcell={cell_name} "
        f"--run_dir={output_loc} "
        f"--run_mode=flat "
        f"--no_density "
        f"> {pattern_log} 2>&1"
    )

    # Starting klayout run
    output_loc.mkdir(parents=True, exist_ok=True)
    try:
        check_call(call_str, shell=True)
    except Exception as e:
        pattern_results = list(output_loc.glob(f"{pattern_name}*.lyrdb"))
        if len(pattern_results) < 1:
            logging.error("%s generated an exception: %s" % (pattern_name, e))
            traceback.print_exc()
            raise Exception("Failed DRC run.")

    # dumping log into output to make CI have the log
    if pattern_log.is_file():
        logging.info("# Dumping drc run output log:")
        with open(pattern_log, "r") as f:
            for line in f:
                line = line.strip()
                logging.info(f"{line}")

    # Checking if run is completed or failed
    pattern_results = list(output_loc.glob(f"{pattern_name}*.lyrdb"))

    # Analysis of splitted testcases into patterns
    if test_criteria in ["pass", "fail"]:
        return analyze_splitted_results(
            layout_path, pattern_results, cell_name, test_criteria
        )
    else:
        # Get list of rules covered in the test case
        rules_tested = get_unit_test_coverage(layout_path)

        if len(pattern_results) > 0:
            # db to gds conversion
            marker_output, runset_analysis = convert_results_db_to_gds(
                pattern_results[0], rules_tested
            )

            # Generating merged testcase for violated rules
            merged_output = generate_merged_testcase(layout_path, marker_output)

            # Generating final db file
            if os.path.exists(merged_output):
                final_report = (
                    f'{merged_output.split(f".{SUPPORTED_TC_EXT}")[0]}_final.lyrdb'
                )
                analysis_log = (
                    f'{merged_output.split(f".{SUPPORTED_TC_EXT}")[0]}_analysis.log'
                )
                call_str = (
                    f"klayout -b -r {runset_analysis} "
                    f"-rd input={merged_output} "
                    f"-rd report={final_report} "
                    f"> {analysis_log} 2>&1"
                )
                failed_analysis_step = False

                try:
                    check_call(call_str, shell=True)
                except Exception as e:
                    failed_analysis_step = True
                    logging.error("%s generated an exception: %s" % (pattern_name, e))
                    traceback.print_exc()

                # dumping log into output to make CI have the log
                if os.path.isfile(analysis_log):
                    logging.info("# Dumping analysis run output log:")
                    with open(analysis_log, "r") as f:
                        for line in f:
                            line = line.strip()
                            logging.info(f"{line}")

                if failed_analysis_step:
                    raise Exception("Failed DRC analysis run.")

                if os.path.exists(final_report):
                    rule_counts = parse_results_db(final_report)
                    return rule_counts
                else:
                    return rule_counts
            else:
                return rule_counts
        else:
            return rule_counts


def run_all_test_cases(tc_df: pd.DataFrame, drc_dir: Path, run_dir: Path, num_workers: int):
    """
    This function run all test cases from the input dataframe.

    Parameters
    ----------
    tc_df : pd.DataFrame
        DataFrame that holds all the test cases information for running.
    drc_dir : Path
        Path string to the location of the drc runsets.
    run_dir : Path
        Path string to the location of the testing code and output.
    num_workers : int
        Number of workers to use for running the regression.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with all test cases information post running.
    """

    results_df_list = []
    tc_df["run_status"] = "no status"

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
                    row["test_criteria"],
                )
            ] = row["run_id"]

        for future in concurrent.futures.as_completed(future_to_run_id):
            run_id = future_to_run_id[future]
            try:
                rule_results = future.result()
                if rule_results:
                    rule_results_df = pd.DataFrame(
                        {
                            "analysis_rule": rule_results.keys(),
                            "count": rule_results.values(),
                        }
                    )
                    rule_results_df["rule_name"] = (
                        rule_results_df["analysis_rule"].str.split(RULE_SEP).str[0]
                    )
                    rule_results_df["type"] = (
                        rule_results_df["analysis_rule"].str.split(RULE_SEP).str[1]
                    )
                    rule_results_df.drop(columns=["analysis_rule"], inplace=True)
                    rule_results_df["count"] = rule_results_df["count"].astype(int)
                    rule_results_df = rule_results_df.pivot(
                        index="rule_name", columns="type", values="count"
                    )
                    rule_results_df = rule_results_df.fillna(0)
                    rule_results_df = rule_results_df.reset_index(drop=False)
                    rule_results_df = rule_results_df.rename(
                        columns={"index": "rule_name"}
                    )
                    rule_results_df["table_name"] = tc_df.loc[
                        tc_df["run_id"] == run_id, "table_name"
                    ].iloc[0]

                    for c in ANALYSIS_RULES:
                        if c not in rule_results_df.columns:
                            rule_results_df[c] = 0

                    rule_results_df[ANALYSIS_RULES] = rule_results_df[
                        ANALYSIS_RULES
                    ].astype(int)
                    rule_results_df = rule_results_df[
                        ["table_name", "rule_name"] + ANALYSIS_RULES
                    ]
                    results_df_list.append(rule_results_df)
                    tc_df.loc[tc_df["run_id"] == run_id, "run_status"] = "completed"
                else:
                    tc_df.loc[tc_df["run_id"] == run_id, "run_status"] = "no output"

            except Exception as exc:
                logging.error("%d generated an exception: %s" % (run_id, exc))
                traceback.print_exc()
                tc_df.loc[tc_df["run_id"] == run_id, "run_status"] = "exception"

    if len(results_df_list) > 0:
        results_df = pd.concat(results_df_list)
        results_df["in_tests"] = 1
    else:
        results_df = pd.DataFrame()

    return results_df, tc_df


def expand_interpolations(rule_str, rules_vars):
    """
    Expand Ruby-like string interpolations #{var} in rule_str using rules_vars dict.
    Return list of expanded strings.
    """
    vars_found = re.findall(r"#\{(\w+)\}", rule_str)
    if not vars_found:
        return [rule_str]  # no interpolation

    subs_lists = []
    for var in vars_found:
        if var in rules_vars:
            subs_lists.append(rules_vars[var])
        else:
            subs_lists.append([f"#{{{var}}}"])  # keep as is if no substitution

    combinations = product(*subs_lists)

    expanded_strings = []
    for combo in combinations:
        temp_str = rule_str
        for var, val in zip(vars_found, combo):
            temp_str = re.sub(r"#\{" + var + r"\}", val, temp_str)
        expanded_strings.append(temp_str)

    return expanded_strings


def parse_existing_rules(
    rule_deck_path, output_path, target_table=None, rules_vars=None
):
    """
    This function collects the rule names from the existing drc rule decks,
    expanding any interpolated variables using rules_vars dictionary.

    Parameters
    ----------
    rule_deck_path : string or Path object
        Path to the DRC directory where all the DRC files are located.
    output_path : string or Path
        Path of the run location to store the output analysis file.
    target_table : string, Optional
        Name of the table to be in testing.
    rules_vars : dict, Optional
        Dictionary with variable names as keys and lists of substitution strings as values,
        used to expand interpolated variables in rule names.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with the rule and rule deck used.
    """
    rules_vars = RULES_VAR or {}

    if target_table is None:
        drc_files = list((rule_deck_path / "rule_decks").glob("*.drc"))
    else:
        matched_files = list((rule_deck_path / "rule_decks").glob(f"*{target_table}.drc"))

        if not matched_files:
            logging.error(f"No DRC rule deck matched the table name: '{target_table}'")
            raise FileNotFoundError(
                errno.ENOENT,
                f"No file found for target table '{target_table}'"
            )

        # Take first match if multiple
        table_rule_file = matched_files[0]
        drc_files = [table_rule_file]

    rules_data = list()
    output_pattern = re.compile(r"""\.output\(\s*(['"])(.*?)\1""")

    for runset in drc_files:
        with open(runset, "r") as f:
            for line in f:
                match = output_pattern.search(line)
                if match:
                    rule_str = match.group(2)
                    expanded_rules = expand_interpolations(rule_str, rules_vars)
                    for rule_name in expanded_rules:
                        rule_info = {
                            "table_name": os.path.basename(runset)
                            .replace(".drc", "")
                            .split("_")[-1],
                            "rule_name": rule_name,
                            "in_rule_deck": 1,
                        }
                        rules_data.append(rule_info)

    df = pd.DataFrame(rules_data)
    df.drop_duplicates(inplace=True)
    # Drop maximal runset rules
    df.drop(df[df["table_name"] == "maximal"].index, inplace=True)
    df.to_csv(output_path / "rule_deck_rules.csv", index=False)
    return df


def generate_merged_testcase(orignal_testcase, marker_testcase):
    """
    This function will merge orignal gds file with generated
    markers gds file.

    Parameters
    ----------
    orignal_testcase : string or Path object
        Path string to the orignal testcase

    marker_testcase : string or Path
        Path of the output marker gds file generated from db file.

    Returns
    -------
    merged_gds_path : string or Path
        Path of the final merged gds file generated.
    """

    new_lib = gdstk.Library()

    lib_org = gdstk.read_gds(orignal_testcase)
    lib_marker = gdstk.read_gds(marker_testcase)

    # Getting flattened top cells
    top_cell_org = lib_org.top_level()[0].flatten(apply_repetitions=True)
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


def convert_results_db_to_gds(results_database: str, rules_tested: list):
    """
    Parses a KLayout .lyrdb result file and generates:
    - A GDSII file with polygons drawn for violated rules.
    - A DRC runset for golden-vs-violation analysis.

    Parameters
    ----------
    results_database : str or Path
        Path to the KLayout results .lyrdb file.
    rules_tested : list of str
        List of rule names expected to be tested in this run.

    Returns
    -------
    output_gds_path : str
        Path to the generated marker GDS file.
    output_runset_path : str
        Path to the generated DRC analysis runset.
    """
    if not results_database.is_file():
        logging.error(f"Results database file does not exist: {results_database}")
        raise FileNotFoundError(results_database)

    base_path = results_database.with_suffix("")  # removes .lyrdb suffix
    output_gds_path = f"{base_path}_markers.gds"
    output_runset_path = f"{base_path}_analysis.drc"

    # Initial DRC analysis header
    runset_analysis_setup = """
source($input)
report("DRC analysis run report at", $report)
full_chip = extent.sized(0.0)
"""
    analysis_rules = [runset_analysis_setup]

    # Parsing XML DB
    rule_data_type_map = list()
    cell_name = ""
    lib = None
    cell = None
    in_item = False

    for event, elem in tqdm(
        ET.iterparse(results_database, events=("start", "end")), desc="Parsing results"
    ):
        if elem.tag != "item" and not in_item:
            elem.clear()
            continue

        if elem.tag == "item" and event == "start":
            in_item = True
            continue

        if elem.tag == "item" and event == "end":
            rules = elem.findall("category")
            values = elem.find("values")
            polygons = values.findall("value") if values is not None else []

            if not cell_name:
                cell_elems = elem.findall("cell")
                if cell_elems:
                    cell_name = cell_elems[0].text or ""
                    lib = gdstk.Library(f"{cell_name}_markers")
                    cell = lib.new_cell(f"{cell_name}_markers")

            rule_name = rules[0].text.replace("'", "") if rules else None
            if not rule_name:
                elem.clear()
                in_item = False
                continue

            if rule_name not in rule_data_type_map:
                rule_data_type_map.append(rule_name)

            # Draw polygons
            rule_lay_dt = rule_data_type_map.index(rule_name) + 1
            for p in polygons:
                draw_polygons(p.text, cell, VIOL_LAY_NUM, rule_lay_dt, PATH_WIDTH)

            elem.clear()
            in_item = False

    if not lib or not cell:
        logging.error(f"No valid violations found in {results_database}")
        raise RuntimeError("Marker generation failed")

    lib.write_gds(output_gds_path)

    # Generate marker inputs and analysis
    sorted_rules = sorted(rule_data_type_map)
    rule_layer_map = {rule: idx + 1 for idx, rule in enumerate(sorted_rules)}
    all_rules = set(sorted_rules) | set(rules_tested)

    for rule in all_rules:
        lay_dt = rule_layer_map.get(rule)
        if lay_dt:
            golden_marker = f"rule_{rule.replace('.', '_')}_golden"
            viol_marker = f"rule_{rule.replace('.', '_')}_viol"
            analysis_rules.append(
                f"{golden_marker} = input({GOLDEN_LAY_NUM}, {lay_dt})\n"
            )
            analysis_rules.append(f"{viol_marker} = input({VIOL_LAY_NUM}, {lay_dt})\n")

        # Output checks if not both golden and tested
        if not (rule in sorted_rules and rule in rules_tested):
            for tag, src, ref in [
                ("viol_not_golden", viol_marker, golden_marker),
                ("golden_not_viol", golden_marker, viol_marker),
            ]:
                analysis_rules.append(
                    f'{src}.not_interacting({ref}).output("{rule}{RULE_SEP}{tag}", "{rule}{RULE_SEP}{tag} polygons")\n'
                )

    with open(output_runset_path, "w") as f:
        f.writelines(analysis_rules)

    return output_gds_path, output_runset_path


def build_tests_dataframe(unit_test_case_dirs, target_table):
    """
    This function is used for getting all test cases available in a formated dataframe before running.

    Parameters
    ----------
    unit_test_case_dirs : List of str
        List of directories where unit test cases are located.
    target_table : str or None
        Name of table that we want to run regression for. If None, run all found.

    Returns
    -------
    pd.DataFrame
        A DataFrame that has all the targetted test cases that we need to run.
    """
    all_unit_test_cases = sorted(
        tc_file
        for dir_path in unit_test_case_dirs
        for tc_file in Path(dir_path).rglob(f"*.{SUPPORTED_TC_EXT}")
    )

    logging.info(
        "# Total number of test cases found: {}".format(len(all_unit_test_cases))
    )

    # Get test cases df from test cases
    tc_df = pd.DataFrame({"test_path": all_unit_test_cases})
    tc_df["testcase_basename"] = tc_df["test_path"].apply(
        lambda x: x.name.replace(".gds", "")
    )
    tc_df["table_name"] = tc_df["testcase_basename"].apply(
        lambda x: x.replace("_golden_merged", "").split("_")[0]
    )

    # Updating some table names
    tc_df["table_name"] = tc_df["table_name"].replace(
        {r"^via[2-4]$": "vian", r"^metal[2-5]$": "metaln"}, regex=True
    )

    tc_df["test_criteria"] = tc_df["test_path"].apply(lambda x: x.parent.name)

    if target_table is not None:
        tc_df = tc_df[tc_df["table_name"] == target_table]

    if len(tc_df) < 1:
        logging.error("No test cases remaining after filtering.")
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


def aggregate_results(
    tc_df: pd.DataFrame, results_df: pd.DataFrame, rules_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Aggregates analysis data from testcases, rule results, and rule deck coverage.

    Parameters
    ----------
    tc_df : pd.DataFrame
        DataFrame with test case info (e.g., table_name, run_status).
    results_df : pd.DataFrame
        DataFrame with marker analysis results per rule.
    rules_df : pd.DataFrame
        DataFrame listing all rules in the rule deck.

    Returns
    -------
    pd.DataFrame
        Aggregated DataFrame with rule coverage and rule status.
    """
    # Ensure required columns are present
    if rules_df.empty and results_df.empty:
        logging.error("No rules available for analysis or results.")
        exit(1)

    # Merge rule deck and results (outer join to retain all cases)
    if not results_df.empty and not rules_df.empty:
        df = pd.merge(results_df, rules_df, how="outer", on=["table_name", "rule_name"])
    elif not results_df.empty:
        df = results_df.copy()
    else:
        df = rules_df.copy()
        for col in ANALYSIS_RULES:
            df[col] = 0

    # Ensure required columns are filled
    df[ANALYSIS_RULES] = df[ANALYSIS_RULES].fillna(0)
    df["in_rule_deck"] = df.get("in_rule_deck", 0).fillna(0)
    df["in_tests"] = df.get("in_tests", 0).fillna(0)

    # Attach testcase run status
    df = pd.merge(df, tc_df[["table_name", "run_status"]], how="left", on="table_name")

    # Initialize rule_status
    df["rule_status"] = "Unknown"

    # Mark rules as failed if any mismatches between golden and violation
    df.loc[(df["viol_not_golden"] > 0) | (df["golden_not_viol"] > 0), "rule_status"] = (
        "Rule Failed"
    )

    # If the testcase itself failed to run
    df.loc[~df["run_status"].isin(["completed"]), "rule_status"] = (
        "Test Case Run Failed"
    )

    # If the rule was not tested as it doesn't have any patterns
    df.loc[(df["in_tests"] < 1), "rule_status"] = "Rule Not Tested"

    # If a rule was in the deck and no mismatches were found → Passed
    df.loc[
        (df["viol_not_golden"] < 1)
        & (df["golden_not_viol"] < 1)
        & (df["in_rule_deck"] > 0)
        & (df["in_tests"] > 0)
        & (df["run_status"] == "completed"),
        "rule_status",
    ] = "Passed"

    return df


def run_regression(drc_dir: Path, output_path: Path, target_table: str, cpu_count: int):
    """
    Running Regression Procedure.

    This function runs the full regression on all test cases.

    Parameters
    ----------
    drc_dir : Path
        Path to the DRC directory where all the DRC files are located.
    output_path : Path
        Path to the location of the output results of the run.
    target_table : string or None
        Name of table that we want to run regression for. If None, run all found.
    cpu_count : int
        Number of cpu cores to use in running testcases.
    Returns
    -------
    bool
        If all regression passed, it returns true. If any of the rules failed it returns false.
    """

    # Parse Existing Rules
    rules_df = parse_existing_rules(drc_dir, output_path, target_table)
    logging.info(
        "# Total number of rules found in rule decks: {}".format(len(rules_df))
    )
    logging.info("# Parsed Rules: \n" + str(rules_df))

    # Get all test cases available in the repo.
    test_cases_path = drc_dir / "testing" / "testcases"
    unit_golden_tests_path = test_cases_path / "unit_golden"
    unit_density_path = test_cases_path / "unit" / "density"
    unit_tests_paths = [unit_golden_tests_path, unit_density_path]
    tc_df = build_tests_dataframe(unit_tests_paths, target_table)
    logging.info("# Total table gds files found: {}".format(len(tc_df)))
    logging.info("# Found testcases: \n" + str(tc_df))

    # Run all test cases.
    results_df, tc_df = run_all_test_cases(tc_df, drc_dir, output_path, cpu_count)
    logging.info("# Testcases found results: \n" + str(results_df))
    logging.info("# Updated testcases: \n" + str(tc_df))

    # Aggregate all dataframes into one
    df = aggregate_results(tc_df, results_df, rules_df)
    df.drop_duplicates(inplace=True)
    logging.info("# Final analysis table: \n" + str(df))

    # Generate error if there are any missing info or fails.
    df.to_csv(output_path / "all_test_cases_results.csv", index=False)

    # Check if there any rules that generated false positive or false negative
    failing_results = df[~df["rule_status"].isin(["Passed"])]
    logging.info("# Failing test cases: \n" + str(failing_results))

    if len(failing_results) > 0:
        logging.error("# Some test cases failed .....")
        return False
    else:
        logging.info("# All testcases passed.")
        return True


def main(drc_dir: Path, output_path: Path, target_table: str):
    """
    Main Procedure.

    This function is the main execution procedure

    Parameters
    ----------
    drc_dir : Path
        Path to the DRC directory where all the DRC files are located.
    output_path : Path
        Path to the location of the output results of the run.
    target_table : str or None
        Name of table that we want to run regression for. If None, run all found.
    Returns
    -------
    bool
        If all regression passed, it returns true. If any of the rules failed it returns false.
    """

    # Determine number of workers
    workers_count = int(args.mp) if args.mp else os.cpu_count()

    # Pandas printing setup
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("max_colwidth", None)
    pd.set_option("display.width", 1000)

    # info logs for args
    logging.info(f"# === Run folder is: {output_path}")
    logging.info(f"# === Target Table is: {target_table}")

    # Check Klayout version
    check_klayout_version()

    # Calling regression function
    run_status = run_regression(drc_dir, output_path, target_table, workers_count)

    if run_status:
        logging.info("Test completed successfully.")
    else:
        logging.error("Test failed.")
        exit(1)


def parse_args():
    USAGE = """
    run_regression.py (--help | -h)
    run_regression.py [--run_dir=<run_dir>] [--table_name=<table_name>] [--mp=<num>]
    """

    parser = argparse.ArgumentParser(
        description="Run IHP-SG13G2 DRC Unit Regression.",
        usage=USAGE,
    )

    parser.add_argument(
        "--run_dir",
        type=str,
        default=None,
        help="Run directory to save all the results. If not provided, a timestamped directory will be created."
    )

    parser.add_argument(
        "--table_name",
        type=str,
        default=None,
        help="Target specific rule table to run."
    )

    parser.add_argument(
        "--mp",
        type=int,
        default=1,
        help="The number of parts to split the rule deck for parallel execution. [default: 1]"
    )

    return parser.parse_args()

# ================================================================
# -------------------------- MAIN --------------------------------
# ================================================================


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Generate timestamped run directory name
    now_str = datetime.now(timezone.utc).strftime("unit_tests_%Y_%m_%d_%H_%M_%S")

    # Determine run directory
    if args.run_dir in [None, "", "pwd"]:
        run_dir = Path.cwd().resolve() / now_str
    else:
        run_dir = Path(args.run_dir).resolve()

    run_name = run_dir.name

    # Setup paths
    testing_dir = Path(__file__).resolve().parent
    drc_dir = testing_dir.parent
    rules_dir = drc_dir / "rule_decks"

    # Create output directory
    run_dir.mkdir(parents=True, exist_ok=True)

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(run_dir / f"{now_str}.log"),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    # Start timing
    time_start = time.time()

    # Run main logic
    main(drc_dir, run_dir, args.table_name)

    # End timing
    elapsed_time = time.time() - time_start
    logging.info(f"Total DRC Regression Run time: {elapsed_time:.2f} seconds")
