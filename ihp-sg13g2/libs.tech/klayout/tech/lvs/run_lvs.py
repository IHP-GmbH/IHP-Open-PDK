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

"""Run IHP 130nm BiCMOS Open Source PDK - SG13G2 LVS.

Usage:
    run_lvs.py (--help| -h)
    run_lvs.py (--layout=<layout_path>) (--netlist=<netlist_path>) [--thr=<thr>]
    [--run_dir=<run_dir_path>] [--topcell=<topcell_name>] [--run_mode=<run_mode>]
    [--lvs_sub=<sub_name>] [--no_net_names] [--spice_comments] [--net_only]
    [--top_lvl_pins] [--no_simplify] [--combine] [--purge] [--purge_nets]
    [--schematic_simplify] [--verbose]

Options:
    --help -h                           Print this help message.
    --layout=<layout_path>              The input GDS file path.
    --netlist=<netlist_path>            The input netlist file path.
    --thr=<thr>                         The number of threads used in run.
    --run_dir=<run_dir_path>            Run directory to save all the results [default: pwd]
    --topcell=<topcell_name>            Topcell name to use.
    --run_mode=<run_mode>               Select Allowed klayout mode. (flat, deep). [default: flat]
    --lvs_sub=<sub_name>                Substrate name used in your design.
    --no_net_names                      Discard net names in extracted netlist.
    --spice_comments                    Enable netlist comments in extracted netlist.
    --net_only                          Enable netlist object creation for extracted netlist.
    --top_lvl_pins                      Enable top level pins only for extracted netlist.
    --no_simplify                       Disable layout simplification for extracted netlist.
    --combine                           Enable netlist combination for extracted netlist.
    --purge                             Enable netlist purge all for extracted netlist.
    --purge_nets                        Enable netlist purge nets for extracted netlist.
    --schematic_simplify                Enable schematic simplification for input netlist.
    --verbose                           Detailed rule execution log for debugging.
"""

from docopt import docopt
import os
import logging
import klayout.db
from datetime import datetime
from subprocess import check_call


def check_klayout_version():
    """
    Check klayout version and makes sure it would work with the LVS.
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
            klayout_v_list[1] == 28 and klayout_v_list[2] <= 13
        ):
            logging.error("Prerequisites at a minimum: KLayout 0.28.14")
            logging.error(
                "Using this klayout version has not been assessed. Limits are unknown"
            )
            # exit(1)

    logging.info(f"Your Klayout version is: {klayout_v_}")


def check_layout_type(layout_path):
    """
    Checks if the layout provided is GDS2 or OASIS. Otherwise, kill the process.

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
            f"GDS file path {layout_path} provided doesn't exist or not a file."
        )
        exit(1)

    if ".gds" not in layout_path and ".oas" not in layout_path:
        logging.error(
            f"Layout {layout_path} is not in GDS2 or OASIS format, please recheck."
        )
        exit(1)

    return os.path.abspath(layout_path)


def get_top_cell_names(gds_path):
    """
    Get the top cell names from the GDS file.

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


def get_run_top_cell_name(arguments, layout_path):
    """
    Get the top cell name to use for running. If it's provided by the user, we use the user input.
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
                "Layout has multiple topcells. Use --topcell to determine which topcell you want."
            )
            exit(1)
        else:
            topcell = layout_topcells[0]

    return topcell


def generate_klayout_switches(arguments, layout_path, netlist_path):
    """
    Parse all the args from input to prepare switches for LVS run.

    Parameters
    ----------
    arguments : dict
        Dictionary that holds the arguments used by user in the run command.
        This is generated by docopt library.
    layout_path : string
        Path to the layout file that we will run LVS on.
    netlist_path : string
        Path to the netlist file that we will run LVS on.

    Returns
    -------
    dict
        Dictionary that represent all run switches passed to klayout.
    """
    switches = dict()

    # No. of threads
    thrCount = 2 if arguments["--thr"] is None else int(arguments["--thr"])
    switches["thr"] = str(int(thrCount))

    if arguments["--run_mode"] in ["flat", "deep"]:
        switches["run_mode"] = arguments["--run_mode"]
    else:
        logging.error("Allowed klayout modes are (flat , deep) only")
        exit()

    if arguments["--lvs_sub"]:
        switches["lvs_sub"] = arguments["--lvs_sub"]
    else:
        switches["lvs_sub"] = "sub!"

    if arguments["--no_net_names"]:
        switches["spice_net_names"] = "false"
    else:
        switches["spice_net_names"] = "true"

    if arguments["--spice_comments"]:
        switches["spice_comments"] = "true"
    else:
        switches["spice_comments"] = "false"

    if arguments["--net_only"]:
        switches["net_only"] = "true"
    else:
        switches["net_only"] = "false"

    if arguments["--top_lvl_pins"]:
        switches["top_lvl_pins"] = "true"
    else:
        switches["top_lvl_pins"] = "false"

    if arguments["--no_simplify"]:
        switches["netlist_simplify"] = "false"
    else:
        switches["netlist_simplify"] = "true"

    if arguments["--combine"]:
        switches["combine"] = "true"
    else:
        switches["combine"] = "false"

    if arguments["--purge"]:
        switches["purge"] = "true"
    else:
        switches["purge"] = "false"

    if arguments["--purge_nets"]:
        switches["purge_nets"] = "true"
    else:
        switches["purge_nets"] = "false"

    if arguments["--schematic_simplify"]:
        switches["schematic_simplify"] = "true"
    else:
        switches["schematic_simplify"] = "false"

    if arguments["--verbose"]:
        switches["verbose"] = "true"
    else:
        switches["verbose"] = "false"

    switches["topcell"] = get_run_top_cell_name(arguments, layout_path)
    switches["input"] = os.path.abspath(layout_path)
    switches["schematic"] = os.path.abspath(netlist_path)

    return switches


def build_switches_string(sws: dict):
    """
    Build switches string from dictionary.

    Parameters
    ----------
    sws : dict
        Dictionary that holds the Antenna switches.
    """
    return " ".join(f"-rd {k}={v}" for k, v in sws.items())


def check_lvs_results(results_db_files: list):
    """
    Checks the results db generated from run and report at the end if the LVS run failed or passed.

    Parameters
    ----------
    results_db_files : list
        A list of strings that represent paths to results databases of all the LVS runs.
    """

    if len(results_db_files) < 1:
        logging.error("Klayout did not generate any db results. Please check run logs")
        exit(1)


def run_check(lvs_file: str, path: str, run_dir: str, sws: dict):
    """
    Run LVS check.

    Parameters
    ----------
    lvs_file : str
        String that has the file full path to run.
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

    logging.info(
        f'Running SG13G2 LVS checks on design {path} on cell {sws["topcell"]}'
    )

    layout_base_name = os.path.basename(path).split(".")[0]
    new_sws = sws.copy()
    report_path = os.path.join(run_dir, f"{layout_base_name}.lvsdb")
    ext_net_path = os.path.join(run_dir, f"{layout_base_name}_extracted.cir")
    new_sws["report"] = report_path
    new_sws["target_netlist"] = ext_net_path

    sws_str = build_switches_string(new_sws)

    run_str = f"klayout -b -r {lvs_file} {sws_str}"
    check_call(run_str, shell=True)

    return report_path


def main(lvs_run_dir: str, arguments: dict):
    """
    Main function to run the LVS.

    Parameters
    ----------
    lvs_run_dir : str
        String with absolute path of the full run dir.
    arguments : dict
        Dictionary that holds the arguments used by user in the run command.
        This is generated by docopt library.
    """

    # Check Klayout version
    check_klayout_version()

    # Check layout file existence
    layout_path = arguments["--layout"]
    if not os.path.exists(arguments["--layout"]):
        logging.error(
            f"The input GDS file path {layout_path} doesn't exist, please recheck."
        )
        exit(1)

    # Check layout type
    layout_path = check_layout_type(layout_path)

    # Check netlist file existence
    netlist_path = arguments["--netlist"]
    if not os.path.exists(arguments["--netlist"]):
        logging.error(
            f"The input netlist file path {netlist_path} doesn't exist, please recheck."
        )
        exit(1)

    lvs_rule_deck = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "sg13g2.lvs"
    )

    # Get run switches
    switches = generate_klayout_switches(arguments, layout_path, netlist_path)

    # Run LVS check
    res_db_files = run_check(lvs_rule_deck, layout_path, lvs_run_dir, switches)

    # Check run
    check_lvs_results(res_db_files)


# ================================================================
# -------------------------- MAIN --------------------------------
# ================================================================


if __name__ == "__main__":
    # arguments
    arguments = docopt(__doc__, version="RUN LVS: 1.0")

    now_str = datetime.utcnow().strftime("lvs_run_%Y_%m_%d_%H_%M_%S")

    if (
        arguments["--run_dir"] == "pwd"
        or arguments["--run_dir"] == ""
        or arguments["--run_dir"] is None
    ):
        lvs_run_dir = os.path.join(os.path.abspath(os.getcwd()), now_str)
    else:
        lvs_run_dir = os.path.abspath(arguments["--run_dir"])

    os.makedirs(lvs_run_dir, exist_ok=True)

    # logs format
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(os.path.join(lvs_run_dir, "{}.log".format(now_str))),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    # Calling main function
    main(lvs_run_dir, arguments)
