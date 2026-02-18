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

"""Run IHP 130nm BiCMOS Open Source PDK - SG13G2 LVS."""

import argparse
import os
import logging
import klayout.db
from datetime import datetime, timezone
from subprocess import run
import time
import sys


class ConsoleColorFormatter(logging.Formatter):
    """Color formatter for console logs (file logs remain plain)."""

    RESET = "\033[0m"
    COLORS = {
        logging.DEBUG: "\033[36m",     # cyan
        logging.INFO: "\033[32m",      # green
        logging.WARNING: "\033[33m",   # yellow
        logging.ERROR: "\033[31m",     # red
        logging.CRITICAL: "\033[41m",  # red background
    }

    def __init__(self, fmt, datefmt=None, use_color=False):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.use_color = use_color

    def format(self, record):
        original_levelname = record.levelname
        if self.use_color:
            color = self.COLORS.get(record.levelno, "")
            if color:
                record.levelname = f"{color}{record.levelname}{self.RESET}"
        output = super().format(record)
        record.levelname = original_levelname
        return output


class ImportantEventCollector(logging.Handler):
    """Collect warning/error messages for end-of-run summary."""

    def __init__(self):
        super().__init__(level=logging.WARNING)
        self.warnings = []
        self.errors = []

    def emit(self, record):
        message = record.getMessage()
        if record.levelno >= logging.ERROR:
            self.errors.append(message)
        elif record.levelno >= logging.WARNING:
            self.warnings.append(message)


class KLayoutRunError(RuntimeError):
    """Raised when KLayout LVS execution fails."""

    def __init__(self, message, artifacts, returncode, stdout_text="", stderr_text=""):
        super().__init__(message)
        self.artifacts = artifacts
        self.returncode = returncode
        self.stdout_text = stdout_text or ""
        self.stderr_text = stderr_text or ""


def setup_logging(lvs_run_dir, run_name):
    """Configure console/file logging and return collector + main log path."""
    log_format = "%(asctime)s | %(levelname)-7s | %(message)s"
    log_datefmt = "%d-%b-%Y %H:%M:%S"
    main_log_path = os.path.join(lvs_run_dir, f"{run_name}.log")

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()

    file_handler = logging.FileHandler(main_log_path)
    file_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=log_datefmt))

    use_color = sys.stderr.isatty() and os.environ.get("NO_COLOR") is None and os.environ.get("TERM") != "dumb"
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        ConsoleColorFormatter(fmt=log_format, datefmt=log_datefmt, use_color=use_color)
    )

    collector = ImportantEventCollector()

    root.addHandler(file_handler)
    root.addHandler(console_handler)
    root.addHandler(collector)

    return collector, main_log_path


def evaluate_run_outcome(layout_log_path, effective_net_only):
    """Extract final run outcome message from KLayout LVS log."""
    if effective_net_only:
        return "NET_ONLY mode: extracted netlist generated from layout only."

    if not layout_log_path or not os.path.isfile(layout_log_path):
        return "Comparison mode: outcome unknown (layout log not found)."

    try:
        with open(layout_log_path, "r") as f:
            content = f.read()
    except OSError:
        return "Comparison mode: outcome unknown (failed to read layout log)."

    if "Congratulations! Netlists match." in content:
        return "Comparison mode: PASS (netlists match)."
    if "ERROR : Netlists don't match" in content:
        return "Comparison mode: FAIL (netlists do not match)."
    return "Comparison mode: completed (no explicit PASS/FAIL signature found)."


def collect_layout_log_signals(layout_log_path, limit=5):
    """Collect warning/error messages from the KLayout layout log."""
    if not layout_log_path or not os.path.isfile(layout_log_path):
        return [], []

    warning_lines = []
    error_lines = []

    try:
        with open(layout_log_path, "r") as f:
            for raw_line in f:
                line = raw_line.strip()
                if "WARNING :" in line or line.startswith("WARNING:"):
                    warning_lines.append(line)
                elif "ERROR :" in line or line.startswith("ERROR:"):
                    error_lines.append(line)
    except OSError:
        return [], []

    warning_lines = list(dict.fromkeys(warning_lines))[:limit]
    error_lines = list(dict.fromkeys(error_lines))[:limit]
    return warning_lines, error_lines


def _summary_status_from_outcome(outcome_text):
    """Map free-form outcome text to a compact status label."""
    outcome = (outcome_text or "").upper()
    if "PASS" in outcome:
        return "PASS"
    if "FAIL" in outcome:
        return "FAIL"
    if "NET_ONLY" in outcome:
        return "NET_ONLY"
    return "UNKNOWN"


def _truncate_text(value, max_len):
    """Truncate long summary values so the table stays readable."""
    text = str(value) if value is not None else "n/a"
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _emit_summary_table(rows, key_width=16, value_width=None):
    """Emit an ASCII summary table."""
    if value_width is None:
        max_value_len = max(len(str(value)) for _, value in rows) if rows else 0
        value_width = max(60, max_value_len)

    border = f"+-{'-' * key_width}-+-{'-' * value_width}-+"
    logging.info(border)
    for key, value in rows:
        logging.info(
            "| %s | %s |",
            _truncate_text(key, key_width).ljust(key_width),
            _truncate_text(value, value_width).ljust(value_width),
        )
    logging.info(border)


def emit_important_summary(run_dir, run_meta, collector, total_time):
    """Print a compact recap of the most important run information."""
    logging.info("==============================================================================")
    logging.info("Important Summary")

    layout_path = run_meta.get("layout_path") if run_meta else None
    topcell = run_meta.get("topcell") if run_meta else None
    effective_net_only = run_meta.get("effective_net_only") if run_meta else False
    run_mode = "NET_ONLY" if effective_net_only else "COMPARE"
    outcome = run_meta.get("outcome", "n/a") if run_meta else "n/a"
    status = _summary_status_from_outcome(outcome)

    klayout_warns, klayout_errs = collect_layout_log_signals(
        run_meta.get("layout_log_path") if run_meta else None
    )
    script_warns = list(dict.fromkeys(collector.warnings))
    script_errs = list(dict.fromkeys(collector.errors))

    all_warns = list(dict.fromkeys(script_warns + klayout_warns))
    all_errs = list(dict.fromkeys(script_errs + klayout_errs))

    rows = [
        ("Status", status),
        ("Mode", run_mode),
        ("Outcome", outcome),
        ("Layout", os.path.basename(layout_path) if layout_path else "n/a"),
        ("Top Cell", topcell or "n/a"),
        ("Results Dir", run_dir),
        ("Warnings", str(len(all_warns))),
        ("Errors", str(len(all_errs))),
        ("Run Time (s)", str(total_time)),
    ]
    _emit_summary_table(rows)

    if all_errs:
        logging.error("Key errors:")
        for msg in all_errs[:5]:
            logging.error("  - %s", msg)
    if all_warns:
        logging.warning("Key warnings:")
        for msg in all_warns[:5]:
            logging.warning("  - %s", msg)

    logging.info("==============================================================================")


def discover_run_artifacts(run_dir, main_log_path):
    """Best-effort discovery of generated run artifacts in a run directory."""
    layout_logs = []
    result_dbs = []
    extracted_netlists = []

    try:
        for name in os.listdir(run_dir):
            full_path = os.path.join(run_dir, name)
            if full_path == main_log_path:
                continue
            if name.endswith(".log"):
                layout_logs.append(full_path)
            elif name.endswith(".lvsdb"):
                result_dbs.append(full_path)
            elif name.endswith("_extracted.cir"):
                extracted_netlists.append(full_path)
    except OSError:
        return {
            "layout_log_path": None,
            "report_path": None,
            "extracted_netlist_path": None,
        }

    return {
        "layout_log_path": sorted(layout_logs)[0] if layout_logs else None,
        "report_path": sorted(result_dbs)[0] if result_dbs else None,
        "extracted_netlist_path": (
            sorted(extracted_netlists)[0] if extracted_netlists else None
        ),
    }


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
        if klayout_v_list[1] < 30 or (klayout_v_list[1] == 30 and klayout_v_list[2] < 2):
            logging.error("Prerequisites at a minimum: KLayout 0.30.2")
            logging.error(
                "Using this klayout version has not been assessed. Limits are unknown"
            )
            exit(1)

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

    return layout_path


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


def get_run_top_cell_name(args, layout_path):
    """
    Get the top cell name to use for running. If it's provided by the user, we use the user input.
    If not, we get it from the GDS file.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments.
    layout_path : string
        Path to the target layout.

    Returns
    -------
    string
        Name of the topcell to use in run.

    """

    if args.topcell:
        topcell = args.topcell
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


def normalize_optional_path(path_value):
    """
    Normalize optional file path arguments.

    Parameters
    ----------
    path_value : str or None
        Path value to normalize.

    Returns
    -------
    str or None
        Absolute normalized path, or None when empty/missing.
    """
    if path_value is None:
        return None

    path_value = path_value.strip()
    if path_value == "":
        return None

    return os.path.abspath(os.path.expanduser(path_value))


def generate_klayout_switches(args, layout_path, netlist_path, effective_net_only):
    """
    Parse all the args from input to prepare switches for LVS run.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments.
    layout_path : string
        Path to the layout file that we will run LVS on.
    netlist_path : string or None
        Path to the netlist file that we will run LVS on.
        If None, schematic loading is delegated to the runset fallback logic.
    effective_net_only : bool
        Effective net-only mode for this run.

    Returns
    -------
    dict
        Dictionary that represent all run switches passed to klayout.
    """
    switches = dict()

    if args.run_mode in ["flat", "deep"]:
        run_mode = args.run_mode
    else:
        logging.error("Allowed klayout modes are (flat , deep) only")
        exit(1)

    switches = {
        "run_mode": run_mode,
        "no_net_names": "true" if args.no_net_names else "false",
        "spice_comments": "true" if args.spice_comments else "false",
        "net_only": "true" if effective_net_only else "false",
        "top_lvl_pins": "true" if args.top_lvl_pins else "false",
        "no_simplify": "true" if args.no_simplify else "false",
        "no_series_res": "true" if args.no_series_res else "false",
        "no_parallel_res": "true" if args.no_parallel_res else "false",
        "combine_devices": "true" if args.combine_devices else "false",
        "purge": "true" if args.purge else "false",
        "purge_nets": "true" if args.purge_nets else "false",
        "verbose": "true" if args.verbose else "false",
        "topcell": get_run_top_cell_name(args, layout_path),
        "input": os.path.abspath(layout_path),
        "schematic": os.path.abspath(netlist_path) if netlist_path else None,
        "allow_unmatched_ports": "true" if args.allow_unmatched_ports else "false",
    }

    return switches


def build_switches_string(sws: dict):
    """
    Build switches string from dictionary.

    Parameters
    ----------
    sws : dict
        Dictionary that holds the Antenna switches.
    """
    return " ".join(f"-rd {k}={v}" for k, v in sws.items() if v is not None)


def check_lvs_results(results_db_files: list):
    """
    Checks the results db generated from run and report at the end if the LVS run failed or passed.

    Parameters
    ----------
    results_db_files : list
        A list of strings that represent paths to results databases of all the LVS runs.
    """

    if isinstance(results_db_files, str):
        results_db_files = [results_db_files]

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
    dict
        Output artifact paths generated for this run.

    """

    logging.info(
        f'Running SG13G2 LVS checks on design {path} on cell {sws["topcell"]}'
    )

    layout_base_name = os.path.basename(path).split(".")[0]
    new_sws = sws.copy()
    report_path = os.path.join(run_dir, f"{layout_base_name}.lvsdb")
    log_path = os.path.join(run_dir, f"{layout_base_name}.log")
    ext_net_path = os.path.join(run_dir, f"{layout_base_name}_extracted.cir")
    new_sws["report"] = report_path
    new_sws["log"] = log_path
    new_sws["target_netlist"] = ext_net_path

    sws_str = build_switches_string(new_sws)

    run_str = f"klayout -b -r {lvs_file} {sws_str}"
    proc = run(run_str, shell=True, text=True, capture_output=True)

    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)

    if proc.returncode != 0:
        raise KLayoutRunError(
            "KLayout LVS execution failed.",
            artifacts={
                "report_path": report_path,
                "layout_log_path": log_path,
                "extracted_netlist_path": ext_net_path,
            },
            returncode=proc.returncode,
            stdout_text=proc.stdout,
            stderr_text=proc.stderr,
        )

    return {
        "report_path": report_path,
        "layout_log_path": log_path,
        "extracted_netlist_path": ext_net_path,
    }


def main(lvs_run_dir: str, args: argparse.Namespace):
    """
    Main function to run the LVS.

    Parameters
    ----------
    lvs_run_dir : str
        String with absolute path of the full run dir.
    args : argparse.Namespace
        Parsed command-line arguments.
    """

    # Check Klayout version
    check_klayout_version()

    # Check layout file existence
    layout_path = args.layout
    layout_path = os.path.abspath(os.path.expanduser(layout_path))
    if not os.path.exists(layout_path):
        logging.error(
            f"The input GDS file path {layout_path} doesn't exist, please recheck."
        )
        exit(1)

    # Check layout type
    layout_path = check_layout_type(layout_path)

    # Resolve netlist/net-only with explicit user-facing logs.
    netlist_path = normalize_optional_path(args.netlist)
    effective_net_only = args.net_only

    if netlist_path is None and not args.net_only:
        logging.warning(
            "No netlist was provided and --net_only was not set. "
            "LVS comparison is disabled for this run; forcing --net_only behavior."
        )
        effective_net_only = True
    elif netlist_path is not None and args.net_only:
        logging.warning(
            "Both --netlist and --net_only were provided. "
            "The netlist input is ignored because net-only extraction was requested."
        )
        netlist_path = None

    # Check netlist file existence (only when it is used for comparison).
    if not effective_net_only and netlist_path:
        if not os.path.exists(netlist_path):
            logging.error(
                f"The input netlist file path {netlist_path} doesn't exist, please recheck."
            )
            exit(1)
        if not os.path.isfile(netlist_path):
            logging.error(
                f"The input netlist path {netlist_path} is not a file, please recheck."
            )
            exit(1)

    lvs_rule_deck = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "sg13g2.lvs"
    )

    # Get run switches
    switches = generate_klayout_switches(args, layout_path, netlist_path, effective_net_only)

    # Run LVS check
    run_artifacts = run_check(lvs_rule_deck, layout_path, lvs_run_dir, switches)

    # Check run
    check_lvs_results(run_artifacts["report_path"])

    return {
        "layout_path": layout_path,
        "topcell": switches["topcell"],
        "netlist_path_used": netlist_path,
        "effective_net_only": effective_net_only,
        "report_path": run_artifacts["report_path"],
        "layout_log_path": run_artifacts["layout_log_path"],
        "extracted_netlist_path": run_artifacts["extracted_netlist_path"],
    }


# ================================================================
# -------------------------- MAIN --------------------------------
# ================================================================


if __name__ == "__main__":
    USAGE = """
    run_lvs.py (--help | -h)
    run_lvs.py --layout=<layout_path>
               [--netlist=<netlist_path>] [--run_dir=<run_dir_path>]
               [--topcell=<topcell_name>] [--run_mode=<run_mode>]
               [--no_net_names] [--spice_comments] [--net_only] [--no_simplify]
               [--no_series_res] [--no_parallel_res] [--combine_devices] [--top_lvl_pins]
               [--purge] [--purge_nets] [--verbose] [--allow_unmatched_ports]
    """

    parser = argparse.ArgumentParser(
        description="Run IHP SG13G2 LVS checks.",
        usage=USAGE,
    )
    parser.add_argument(
        "--layout",
        type=str,
        required=True,
        help="Path to input GDS/OAS layout.",
    )
    parser.add_argument(
        "--netlist",
        type=str,
        default=None,
        help="Optional path to schematic netlist (.cdl/.spice/.cir).",
    )
    parser.add_argument(
        "--run_dir",
        type=str,
        default=None,
        help="Run directory for outputs. Default creates timestamped dir in cwd.",
    )
    parser.add_argument("--topcell", type=str, help="Top cell name to run.")
    parser.add_argument(
        "--run_mode",
        type=str,
        choices=["flat", "deep"],
        default="deep",
        help="KLayout run mode. [default: deep]",
    )
    parser.add_argument("--no_net_names", action="store_true", help="Omit net names in extracted netlist.")
    parser.add_argument("--spice_comments", action="store_true", help="Include comments in extracted netlist.")
    parser.add_argument("--net_only", action="store_true", help="Generate extracted netlist only (skip comparison).")
    parser.add_argument("--no_simplify", action="store_true", help="Disable simplify on layout/schematic netlists.")
    parser.add_argument("--no_series_res", action="store_true", help="Disable resistor series simplification.")
    parser.add_argument("--no_parallel_res", action="store_true", help="Disable resistor parallel simplification.")
    parser.add_argument("--combine_devices", action="store_true", help="Enable generic device combination.")
    parser.add_argument("--top_lvl_pins", action="store_true", help="Create top-level pins in netlists.")
    parser.add_argument("--purge", action="store_true", help="Purge unused nets/devices.")
    parser.add_argument("--purge_nets", action="store_true", help="Purge floating nets.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose rule-execution logging.")
    parser.add_argument(
        "--allow_unmatched_ports",
        action="store_true",
        help="Allow unmatched top-level ports during comparison.",
    )
    args = parser.parse_args()

    # Generate a timestamped run directory name
    now_str = datetime.now(timezone.utc).strftime("lvs_run_%Y_%m_%d_%H_%M_%S")

    if args.run_dir in ["pwd", "", None]:
        lvs_run_dir = os.path.join(os.path.abspath(os.getcwd()), now_str)
    else:
        lvs_run_dir = os.path.abspath(args.run_dir)

    os.makedirs(lvs_run_dir, exist_ok=True)

    # Setup logging
    collector, main_log_path = setup_logging(lvs_run_dir, now_str)

    # Start of execution time
    t0 = time.time()
    run_meta = None
    exit_code = 0

    try:
        # Calling main function
        run_meta = main(lvs_run_dir, args)
    except SystemExit as e:
        exit_code = e.code if isinstance(e.code, int) else 1
    except KLayoutRunError as e:
        logging.error("KLayout run failed with exit code %s.", e.returncode)
        for line in e.stderr_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("WARNING:") or "WARNING :" in stripped:
                logging.warning("KLayout stderr: %s", stripped)
            elif stripped.startswith("ERROR:") or "ERROR :" in stripped:
                logging.error("KLayout stderr: %s", stripped)

        run_meta = {
            "layout_path": os.path.abspath(os.path.expanduser(args.layout)),
            "topcell": args.topcell,
            "netlist_path_used": normalize_optional_path(args.netlist),
            "effective_net_only": args.net_only,
            "report_path": e.artifacts.get("report_path"),
            "layout_log_path": e.artifacts.get("layout_log_path"),
            "extracted_netlist_path": e.artifacts.get("extracted_netlist_path"),
        }
        exit_code = e.returncode
    except Exception:
        logging.exception("Unhandled exception during LVS run.")
        exit_code = 1
    finally:
        if run_meta is None:
            discovered = discover_run_artifacts(lvs_run_dir, main_log_path)
            run_meta = {
                "layout_path": os.path.abspath(os.path.expanduser(args.layout)),
                "topcell": args.topcell,
                "netlist_path_used": normalize_optional_path(args.netlist),
                "effective_net_only": args.net_only,
                "report_path": discovered.get("report_path"),
                "layout_log_path": discovered.get("layout_log_path"),
                "extracted_netlist_path": discovered.get("extracted_netlist_path"),
            }
        if run_meta:
            run_meta["outcome"] = evaluate_run_outcome(
                run_meta.get("layout_log_path"),
                run_meta.get("effective_net_only", False),
            )
        logging.getLogger().removeHandler(collector)
        emit_important_summary(
            lvs_run_dir,
            run_meta,
            collector,
            round(time.time() - t0, 3),
        )

    if exit_code != 0:
        raise SystemExit(exit_code)
