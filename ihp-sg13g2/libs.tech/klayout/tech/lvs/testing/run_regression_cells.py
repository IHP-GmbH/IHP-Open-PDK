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

"""Run IHP 130nm BiCMOS Open Source PDK - SG13G2 LVS Regression For Cells.

Usage:
    run_regression_cells.py (--help| -h)
    run_regression_cells.py [--cell=<cell>] [--run_dir=<run_dir_path>] [--mp=<num>]

Options:
    --help -h                 Print this help message.
    --cell=<cell>             Specify the cell to run; all cells run if not specified.
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
import shutil

# CONSTANTS
SUPPORTED_TC_EXT = "gds"
SUPPORTED_SPICE_EXT = "cdl"
SUPPORTED_SW_EXT = "yaml"


def build_tests_dataframe(cells_dir, target_cell, cells):
    """
    Getting all test cases available in a formatted dataframe before running.

    Parameters
    ----------
    cells_dir :  sting
        Path string to the cells directory where all the testcases are located.
    target_cell : str or None
        Name of cell that we want to run regression for. If None, run all found.
    cells : list
        List that holds all available cells will be tested.

    Returns
    -------
    pd.DataFrame
        A DataFrame that has all the targeted test cases that we need to run.
    """

    # Construct df that holds all info
    tc_df = pd.DataFrame({"cell_name": cells})

    all_cells_layout = sorted(Path(cells_dir).rglob("*.{}".format(SUPPORTED_TC_EXT)))
    all_cells_netlist = sorted(
        Path(cells_dir).rglob("*.{}".format(SUPPORTED_SPICE_EXT))
    )

    # Mapping cell names to paths for both layout and netlist files
    cell_paths = {
        cell_name: {
            "layout_path": next(
                (path for path in all_cells_layout if cell_name in str(path)), None
            ),
            "netlist_path": next(
                (path for path in all_cells_netlist if cell_name in str(path)), None
            ),
        }
        for cell_name in tc_df["cell_name"]
    }

    # Adding paths to new columns in the DataFrame
    tc_df[["layout_path", "netlist_path"]] = tc_df["cell_name"].apply(
        lambda x: pd.Series(cell_paths[x])
    )

    # Print warning for cells without layout or netlist path
    missing_cells = tc_df[
        (tc_df["layout_path"].isnull()) | (tc_df["netlist_path"].isnull())
    ]["cell_name"]
    if not missing_cells.empty:
        logging.warning(
            "The following cells are missing layout (GDS) or netlist (CDL) files, or both: {}".format(
                missing_cells.tolist()
            )
        )
        logging.warning("These missing cells will be ignored in testing.")

    # Drop missing cells
    tc_df.drop(tc_df[tc_df["cell_name"].isin(missing_cells)].index, inplace=True)

    # Check selected cell is available
    if target_cell is not None:
        tc_df = tc_df[tc_df["cell_name"] == target_cell]
    if len(tc_df) < 1:
        logging.error("No test cases remaining for selected cells after filtering.")
        exit(1)

    # info about available cells
    logging.info("Total cells found: {}".format(len(tc_df)))
    logging.info("Found cells: \n" + str(tc_df["cell_name"]))

    tc_df["run_id"] = range(len(tc_df))

    # Duplicate the original cells for iso/digisub
    iso_df = tc_df.copy()
    sub_df = tc_df.copy()

    # Add the suffix to each cell in the column
    iso_df["cell_name"] = iso_df["cell_name"] + "_iso"
    sub_df["cell_name"] = sub_df["cell_name"] + "_digisub"

    # Concatenate the original DataFrame with the modified DataFrame
    final_df = pd.concat([tc_df, iso_df, sub_df])
    final_df.reset_index(drop=True, inplace=True)

    final_df["run_id"] = range(len(final_df))

    return final_df


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
    lvs_dir, layout_path, netlist_path, run_dir, cell_name,
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
    cell_name : string
        Cell name that we are running on.

    Returns
    -------
    dict
        A dict with all rule counts
    """

    # Get switches used for each run
    sw_file = os.path.join(
        Path(layout_path.parent).absolute(), f"{cell_name}.{SUPPORTED_SW_EXT}"
    )

    # Switches setup
    if os.path.exists(sw_file):
        switches = " ".join(get_switches(sw_file, cell_name))
    else:
        # Get switches
        switches = ""  # default switch

    # Creating run folder structure and copy testcases in it
    pattern_clean = ".".join(os.path.basename(layout_path).split(".")[:-1])
    output_loc = os.path.join(run_dir, cell_name)
    pattern_log = os.path.join(output_loc, f"{pattern_clean}_lvs.log")
    os.makedirs(output_loc, exist_ok=True)
    layout_path_run = os.path.join(run_dir, cell_name, f"{cell_name}.gds")
    netlist_path_run = os.path.join(run_dir, cell_name, f"{cell_name}.cdl")
    shutil.copyfile(layout_path, layout_path_run)
    shutil.copyfile(netlist_path, netlist_path_run)

    # command to run LVS
    call_str = (
        f"python3 {lvs_dir}/run_lvs.py --layout={layout_path_run} --topcell={cell_name} "
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
            raise Exception("Failed LVS run.")

    # dumping log into output to make CI have the log
    if os.path.isfile(pattern_log):
        with open(pattern_log, "r") as f:
            result = f.read()
            for line in f:
                line = line.strip()
                logging.info(f"{line}")

        # checking device status
        cell_status = "Failed"
        if "Congratulations! Netlists match" in result:
            logging.info(f"{cell_name} testcase passed")
            cell_status = "Passed"
        else:
            logging.error(f"{cell_name} testcase failed.")
            logging.error(f"Please recheck {layout_path} and {netlist_path} files.")
    else:
        logging.error("Klayout LVS run failed, there is no log file is generated")
        exit(1)

    return cell_status


def run_all_test_cases(tc_df: pd.DataFrame, lvs_dir, run_dir, num_workers):
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

    tc_df["cell_status"] = "no status"

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_run_id = dict()
        for _, row in tc_df.iterrows():
            future_to_run_id[
                executor.submit(
                    run_test_case,
                    lvs_dir,
                    row["layout_path"],
                    row["netlist_path"],
                    run_dir,
                    row["cell_name"],
                )
            ] = row["run_id"]

        for future in concurrent.futures.as_completed(future_to_run_id):
            run_id = future_to_run_id[future]
            try:
                tc_df.loc[tc_df["run_id"] == run_id, "cell_status"] = future.result()
            except Exception as exc:
                logging.error("%d generated an exception: %s" % (run_id, exc))
                traceback.print_exc()
                tc_df.loc[tc_df["run_id"] == run_id, "cell_status"] = "exception"

    return tc_df


def run_regression(lvs_dir, cells_dir, output_path, target_cell, cpu_count, cells):
    """
    Runs the full regression for std cells.

    Parameters
    ----------
    lvs_dir : string
        Path string to the LVS directory where all the LVS files are located.
    cells_dir :  sting
        Path string to the cells directory where all the testcases are located.
    output_path : str
        Path string to the location of the output results of the run.
    target_cell : str or None
        Name of cell that we want to run regression for. If None, run all found.
    cpu_count : int
        Number of cpu cores to be used in running testcases.
    cells : list
        List that holds all available cells will be tested.
    Returns
    -------
    bool
        If all regression passed, it returns true. If any of the cells failed it returns false.
    """

    # Get all test cases available in the repo.
    tc_df = build_tests_dataframe(cells_dir, target_cell, cells)

    # Run all test cases.
    results_df = run_all_test_cases(tc_df, lvs_dir, output_path, cpu_count)
    results_df.drop_duplicates(inplace=True)
    results_df.drop("run_id", inplace=True, axis=1)
    logging.info("Final results table: \n" + str(results_df))

    # Generate error if there are any missing info or fails.
    results_df.to_csv(
        os.path.join(output_path, "all_test_cases_results.csv"), index=False
    )

    # Check if there any cell that generated failure
    failing_results = results_df[~results_df["cell_status"].isin(["Passed"])]
    logging.info("Failing test cases: \n" + str(failing_results))

    if len(failing_results) > 0:
        logging.error("Some test cases failed .....")
        return False
    else:
        logging.info("All testcases passed.")
        return True


def main(lvs_dir, cells_dir, output_path, target_cell, cells):
    """
    Main function to run LVS regression for SG13G2 std cells.

    Parameters
    ----------
    lvs_dir : str
        Path string to the LVS directory where all the LVS files are located.
    cells_dir :  sting
        Path string to the cells directory where all the testcases are located.
    output_path : str
        Path string to the location of the output results of the run.
    target_cell : str or None
        Name of cell that we want to run regression for. If None, run all found.
    cells : list
        List that holds all available cells will be tested
    Returns
    -------
    bool
        If all regression passed, it returns true. If any of the cells failed it returns false.
    """

    # No. of threads
    cpu_count = os.cpu_count() if args["--mp"] is None else int(args["--mp"])

    # info logs for args
    logging.info("Run folder is: {}".format(output_path))
    logging.info("Target cell is: {}".format(target_cell))

    # Start of execution time
    t0 = time.time()

    # Calling regression function
    run_status = run_regression(
        lvs_dir, cells_dir, output_path, target_cell, cpu_count, cells
    )

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
    run_name = datetime.utcnow().strftime("cells_tests_%Y_%m_%d_%H_%M_%S")

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

    # Available cells
    cells_dir = os.path.join(testing_dir, "testcases", "sg13g2_cells")
    if not os.path.isdir(cells_dir):
        logging.error("Cells tests directory doesn't exist, please recheck")
        logging.error(f"{cells_dir} path doesn't exist")
        exit(1)

    cells = [cell.name for cell in os.scandir(cells_dir) if cell.is_dir()]

    # Make sure that we have std cells
    if len(cells) < 1:
        logging.error(f"There are no cells exist in {cells_dir}, please recheck")
        exit(1)

    # selected cell
    target_cell = args["--cell"]
    if target_cell and (target_cell not in cells):
        logging.error("Selected cell doesn't exist, please recheck.")
        logging.info(f"Allowed cells are {cells}")
        exit(1)

    # Calling main function
    main(lvs_dir, cells_dir, output_path, target_cell, cells)
