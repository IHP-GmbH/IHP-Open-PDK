# ==========================================================================
# Copyright 2024 IHP PDK Authors
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

"""Run IHP 130nm BiCMOS Open Source PDK - SG13G2 LVS Regression.

Usage:
    run_regression.py (--help| -h)
    run_regression.py [--device=<device>] [--run_dir=<run_dir_path>] [--mp=<num>]

Options:
    --help -h                 Print this help message.
    --device=<device>         Select device category you want to run regression on.
    --run_dir=<run_dir_path>  Run directory to save all the results [default: pwd]
    --mp=<num>                The number of threads used in run.
"""

from subprocess import check_call
import concurrent.futures
import traceback
import yaml
from docopt import docopt
import os
from datetime import datetime
import time
import pandas as pd
import logging
import glob
from pathlib import Path
import errno
import shutil

# CONSTANTS
SUPPORTED_TC_EXT = "gds"
SUPPORTED_SPICE_EXT = "cdl"
SUPPORTED_SW_EXT = "yaml"


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
    elif len(klayout_v_list) >= 2 or len(klayout_v_list) <= 3:
        if klayout_v_list[1] < 28 or (
            klayout_v_list[1] == 28 and klayout_v_list[2] <= 3
        ):
            logging.error("Prerequisites at a minimum: KLayout 0.28.4")
            logging.error(
                "Using this klayout version is not supported in this development."
            )
            exit(1)

    logging.info(f"Your Klayout version is: {klayout_v_}")


def parse_existing_devices(rule_deck_path, output_path, target_device_group=None):
    """
    This function collects the rule names from the existing drc rule decks.

    Parameters
    ----------
    rule_deck_path : string or Path object
        Path string to the LVS directory where all the LVS files are located.
    output_path : string or Path
        Path of the run location to store the output analysis file.
    target_device_group : string Optional
        Name of the device group to be in testing

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with the rule and rule deck used.
    """

    if target_device_group is None:
        lvs_files = glob.glob(
            os.path.join(rule_deck_path, "rule_decks", "*_extraction.lvs")
        )
    else:
        table_device_file = os.path.join(
            rule_deck_path,
            "rule_decks",
            f"{str(target_device_group).lower()}_extraction.lvs",
        )
        if not os.path.isfile(table_device_file):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), table_device_file
            )

        lvs_files = [table_device_file]

    rules_data = list()

    for runset in lvs_files:
        with open(runset, "r") as f:
            for line in f:
                if "extract_devices" in line:
                    line_list = line.split("'")
                    rule_info = dict()
                    rule_info["device_group"] = (
                        os.path.basename(runset).replace("_extraction.lvs", "").upper()
                    )
                    rule_info["device_name"] = line_list[1]
                    rule_info["in_rule_deck"] = 1
                    rules_data.append(rule_info)

    df = pd.DataFrame(rules_data)
    df.drop_duplicates(inplace=True)
    df.to_csv(os.path.join(output_path, "rule_deck_rules.csv"), index=False)
    return df


def build_tests_dataframe(unit_test_cases_dir, target_device_group):
    """
    Getting all test cases available in a formatted dataframe before running.

    Parameters
    ----------
    unit_test_cases_dir : str
        Path string to the location of unit test cases path.
    target_device_group : str or None
        Name of device group that we want to run regression for. If None, run all found.

    Returns
    -------
    pd.DataFrame
        A DataFrame that has all the targeted test cases that we need to run.
    """
    all_unit_test_cases_layout = sorted(
        Path(unit_test_cases_dir).rglob("*.{}".format(SUPPORTED_TC_EXT))
    )
    logging.info(
        "Total number of gds files test cases found: {}".format(
            len(all_unit_test_cases_layout)
        )
    )

    all_unit_test_cases_netlist = sorted(
        Path(unit_test_cases_dir).rglob("*.{}".format(SUPPORTED_SPICE_EXT))
    )
    logging.info(
        "Total number of spice files test cases found: {}".format(
            len(all_unit_test_cases_netlist)
        )
    )

    if len(all_unit_test_cases_netlist) != len(all_unit_test_cases_layout):
        logging.error("Each testcase should have Layout and Netlist file")
        exit(1)

    # Get test cases df from test cases
    tc_df = pd.DataFrame(
        {
            "test_layout_path": all_unit_test_cases_layout,
            "test_netlist_path": all_unit_test_cases_netlist,
        }
    )
    tc_df["device_name"] = tc_df["test_layout_path"].apply(
        lambda x: x.name.replace(".gds", "")
    )
    tc_df["device_group"] = tc_df["test_layout_path"].apply(
        lambda x: x.parent.parent.name.replace("_devices", "").upper()
    )

    if target_device_group is not None:
        tc_df = tc_df[tc_df["device_group"] == target_device_group]
    if len(tc_df) < 1:
        logging.error("No test cases remaining after filtering.")
        exit(1)

    tc_df["run_id"] = range(len(tc_df))
    return tc_df


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


def run_test_case(
    lvs_dir,
    layout_path,
    netlist_path,
    run_dir,
    device_name,
):
    """
    This function run a single test case using the correct DRC file.

    Parameters
    ----------
    lvs_dir : string or Path
        Path to the location where all runsets exist.
    layout_path : stirng or Path object
        Path string to the layout of the test pattern we want to test.
    netlist_path : stirng or Path object
        Path string to the netlist of the test pattern we want to test.
    run_dir : stirng or Path object
        Path to the location where is the regression run is done.
    device_name : string
        Device name that we are running on.

    Returns
    -------
    dict
        A dict with all rule counts
    """

    # Get switches used for each run
    sw_file = os.path.join(
        Path(layout_path.parent).absolute(), f"{device_name}.{SUPPORTED_SW_EXT}"
    )

    # Switches setup
    if os.path.exists(sw_file):
        switches = " ".join(get_switches(sw_file, device_name))
    else:
        # Get switches
        switches = " --lvs_sub=sub!"  # default switch

    # Creating run folder structure and copy testcases in it
    pattern_clean = ".".join(os.path.basename(layout_path).split(".")[:-1])
    output_loc = os.path.join(run_dir, device_name)
    pattern_log = os.path.join(output_loc, f"{pattern_clean}_lvs.log")
    os.makedirs(output_loc, exist_ok=True)
    layout_path_run = os.path.join(run_dir, device_name, f"{device_name}.gds")
    netlist_path_run = os.path.join(run_dir, device_name, f"{device_name}.cdl")
    shutil.copyfile(layout_path, layout_path_run)
    shutil.copyfile(netlist_path, netlist_path_run)

    # command to run LVS
    call_str = (
        f"python3 {lvs_dir}/run_lvs.py --layout={layout_path_run} "
        f"--netlist={netlist_path_run} --run_dir={output_loc} {switches} > {pattern_log} 2>&1"
    )

    # Starting klayout run
    try:
        check_call(call_str, shell=True)
    except Exception as e:
        pattern_results = glob.glob(os.path.join(output_loc, f"{pattern_clean}*.lvsdb"))
        if len(pattern_results) < 1:
            logging.error("%s generated an exception: %s" % (pattern_clean, e))
            traceback.print_exc()
            raise Exception("Failed DRC run.")

    # dumping log into output to make CI have the log
    if os.path.isfile(pattern_log):
        with open(pattern_log, "r") as f:
            result = f.read()
            for line in f:
                line = line.strip()
                logging.info(f"{line}")

        # checking device status
        device_status = "Failed"
        if "Congratulations! Netlists match" in result:
            logging.info(f"{device_name} testcase passed")
            device_status = "Passed"
        else:
            logging.error(f"{device_name} testcase failed.")
            logging.error(f"Please recheck {layout_path} file.")
    else:
        logging.error("Klayout LVS run failed, there is no log file is generated")
        exit(1)

    return device_status


def run_all_test_cases(tc_df, lvs_dir, run_dir, num_workers):
    """
    This function run all test cases from the input dataframe.

    Parameters
    ----------
    tc_df : pd.DataFrame
        DataFrame that holds all the test cases information for running.
    lvs_dir : string or Path
        Path string to the location of the lvs runsets.
    run_dir : string or Path
        Path string to the location of the testing code and output.
    num_workers : int
        Number of workers to use for running the regression.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with all test cases information post running.
    """

    tc_df["device_status"] = "no status"

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_run_id = dict()
        for _, row in tc_df.iterrows():
            future_to_run_id[
                executor.submit(
                    run_test_case,
                    lvs_dir,
                    row["test_layout_path"],
                    row["test_netlist_path"],
                    run_dir,
                    row["device_name"],
                )
            ] = row["run_id"]

        for future in concurrent.futures.as_completed(future_to_run_id):
            run_id = future_to_run_id[future]
            try:
                tc_df.loc[tc_df["run_id"] == run_id, "device_status"] = future.result()
            except Exception as exc:
                logging.error("%d generated an exception: %s" % (run_id, exc))
                traceback.print_exc()
                tc_df.loc[tc_df["run_id"] == run_id, "device_status"] = "exception"

    return tc_df


def aggregate_results(results_df: pd.DataFrame, devices_df: pd.DataFrame):
    """
    aggregate_results Aggregate the results for all runs.

    Parameters
    ----------
    results_df : pd.DataFrame
        Dataframe that holds the information about the unit test rules.
    devices_df : pd.DataFrame
        Dataframe that holds the information about all the devices implemented in the rule deck.

    Returns
    -------
    pd.DataFrame
        A DataFrame that has all data analysis aggregated into one.
    """
    if len(devices_df) < 1 and len(results_df) < 1:
        logging.error("There are no rules for analysis or run.")
        exit(1)
    elif len(devices_df) < 1 and len(results_df) > 0:
        df = results_df
    elif len(devices_df) > 0 and len(results_df) < 1:
        df = devices_df
    else:
        df = results_df.merge(
            devices_df, how="outer", on=["device_group", "device_name"]
        )

    df.loc[(df["device_status"] != "Passed"), "device_status"] = "Failed"

    return df


def run_regression(lvs_dir, output_path, target_device_group, cpu_count):
    """
    Runs the full regression on all test cases.

    Parameters
    ----------
    lvs_dir : string
        Path string to the LVS directory where all the LVS files are located.
    output_path : str
        Path string to the location of the output results of the run.
    target_device_group : str or None
        Name of device group that we want to run regression for. If None, run all found.
    cpu_count : int
        Number of cpu cores to be used in running testcases.
    Returns
    -------
    bool
        If all regression passed, it returns true. If any of the rules failed it returns false.
    """

    # Parse Existing Rules
    devices_df = parse_existing_devices(lvs_dir, output_path, target_device_group)
    logging.info(
        "Total number of devices found in rule decks: {}".format(len(devices_df))
    )
    logging.info("Parsed devices: \n" + str(devices_df))

    # Get all test cases available in the repo.
    test_cases_path = os.path.join(lvs_dir, "testing/testcases")
    unit_test_cases_path = os.path.join(test_cases_path, "unit")
    tc_df = build_tests_dataframe(unit_test_cases_path, target_device_group)
    logging.info("Total table gds files found: {}".format(len(tc_df)))
    logging.info("Found testcases: \n" + str(tc_df))

    # Run all test cases.
    results_df = run_all_test_cases(tc_df, lvs_dir, output_path, cpu_count)
    logging.info("Testcases found results: \n" + str(results_df))

    # Aggregate all dataframe into one
    df = aggregate_results(results_df, devices_df)
    df.drop_duplicates(inplace=True)
    df.drop("run_id", inplace=True, axis=1)
    logging.info("Final analysis table: \n" + str(df))

    # Generate error if there are any missing info or fails.
    df.to_csv(os.path.join(output_path, "all_test_cases_results.csv"), index=False)

    # Check if there any rules that generated false positive or false negative
    failing_results = df[~df["device_status"].isin(["Passed"])]
    logging.info("Failing test cases: \n" + str(failing_results))

    if len(failing_results) > 0:
        logging.error("Some test cases failed .....")
        return False
    else:
        logging.info("All testcases passed.")
        return True


def main(lvs_dir, output_path, target_device_group):
    """
    Main function to run LVS regression for SG13G2.

    Parameters
    ----------
    lvs_dir : str
        Path string to the LVS directory where all the LVS files are located.
    output_path : str
        Path string to the location of the output results of the run.
    target_device_group : str or None
        Name of device group that we want to run regression for. If None, run all found.
    Returns
    -------
    bool
        If all regression passed, it returns true. If any of the rules failed it returns false.
    """

    # No. of threads
    cpu_count = os.cpu_count() if args["--mp"] is None else int(args["--mp"])

    # info logs for args
    logging.info("Run folder is: {}".format(output_path))
    logging.info("Target device is: {}".format(target_device_group))

    # Start of execution time
    t0 = time.time()

    # Check Klayout version
    check_klayout_version()

    # Calling regression function
    run_status = run_regression(lvs_dir, output_path, target_device_group, cpu_count)

    #  End of execution time
    logging.info("Total execution time {}s".format(time.time() - t0))

    if run_status:
        logging.info("Test completed successfully.")
    else:
        logging.error("Test failed.")
        exit(1)


if __name__ == "__main__":

    # docopt setup
    args = docopt(__doc__, version="LVS Regression: 0.2")

    # default run name
    run_name = datetime.utcnow().strftime("unit_tests_%Y_%m_%d_%H_%M_%S")

    # args setup
    run_dir = args["--run_dir"]
    if run_dir == "pwd" or run_dir == "" or run_dir is None:
        output_path = os.path.join(os.path.abspath(os.getcwd()), run_name)
    else:
        output_path = os.path.abspath(run_dir)

    # Creating output dir
    os.makedirs(output_path, exist_ok=True)

    # Paths of regression dirs
    testing_dir = os.path.dirname(os.path.abspath(__file__))
    lvs_dir = os.path.dirname(testing_dir)

    # logs format
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(os.path.join(output_path, "{}.log".format(run_name))),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    # Pandas setup
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("max_colwidth", None)
    pd.set_option("display.width", 1000)

    # selected device
    allowed_devices = ["MOS", "RFMOS", "BJT", "DIODE", "RES", "CAP", "ESD", "TAP", "IND"]
    target_device_group = args["--device"]

    if target_device_group and (target_device_group not in allowed_devices):
        logging.error(
            "Allowed devices are (MOS, RFMOS, BJT, DIODE, RES, CAP, ESD, TAP, IND) only"
        )
        exit(1)

    # Calling main function
    run_status = main(lvs_dir, output_path, target_device_group)
