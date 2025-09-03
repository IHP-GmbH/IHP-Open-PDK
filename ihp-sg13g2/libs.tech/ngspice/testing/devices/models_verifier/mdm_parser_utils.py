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

import logging
from pathlib import Path
import re
from typing import Dict, List, Optional, Set, Tuple, Generator
import pandas as pd
from models_verifier.mdm_parser_const import (
    DESIGN_PARAMETERS,
    DUTS,
    UNIT_MULTIPLIERS,
    UNIT_REGEX,
)


def convert_value(value: str) -> float | str:
    """
    Convert string value to float with unit conversion, or return as string.

    Args:
        value: String value potentially with units

    Returns:
        Converted numeric value or original string
    """
    cleaned_value = value.strip().strip("\"'")

    if not cleaned_value:
        return cleaned_value

    match = UNIT_REGEX.match(cleaned_value)
    if match:
        try:
            number = float(match.group("num"))
            unit = match.group("unit").lower()
            multiplier = UNIT_MULTIPLIERS.get(unit, 1.0)
            return float(f"{(number * multiplier):.12g}")
        except ValueError:
            return cleaned_value

    return cleaned_value


def find_section_bounds(
    lines: List[str], start_token: str, end_token: str
) -> Tuple[int, int]:
    """
    Find start and end indices for a section.

    Returns:
        Tuple of (start_index, end_index) or (-1, -1) if not found
    """
    start_idx = end_idx = -1

    for i, line in enumerate(lines):
        if line.strip() == start_token:
            start_idx = i + 1
        elif line.strip() == end_token and start_idx != -1:
            end_idx = i
            break

    return start_idx, end_idx


def extract_section(
    lines: List[str], start_token: str, end_token: str
) -> tuple[List[str], int]:
    """Extract lines between start_token and end_token (exclusive)."""
    start_idx, end_idx = find_section_bounds(lines, start_token, end_token)

    if start_idx == -1:
        logging.warning(f"Section '{start_token}' not found")
        return [], -1

    if end_idx == -1:
        logging.warning(
            f"End token '{end_token}' not found for section '{start_token}'"
        )
        return lines[start_idx:], end_idx

    return lines[start_idx:end_idx], end_idx


def extract_data_blocks(lines: List[str]) -> Generator[List[str], None, None]:
    """
    Generator that yields data blocks between BEGIN_DB and END_DB markers.

    Yields:
        List of lines for each data block
    """
    current_block = []
    in_block = False

    for line in lines:
        stripped = line.strip()

        if stripped == "BEGIN_DB":
            in_block = True
            current_block = []
        elif stripped == "END_DB" and in_block:
            if current_block:
                yield current_block
            in_block = False
            current_block = []
        elif in_block:
            current_block.append(line)


def parse_header_inputs(header_lines: List[str]) -> Set[str]:
    """
    Extract ICCAP_INPUTS variable names from header.
    Returns a set of unique input names.
    """
    input_lines, _ = extract_section(header_lines, "ICCAP_INPUTS", "ICCAP_OUTPUTS")

    inputs: Set[str] = set()
    for line in input_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("!"):
            inputs.add(stripped.split()[0])

    return inputs


def parse_design_parameters(
    header_lines: List[str], device_type: str
) -> Dict[str, float | str]:
    """
    Parse ICCAP_VALUES section for design parameters.

    Returns:
        Dictionary of parameter names and values
    """
    design_params = {}
    in_values_section = False

    for line in header_lines:
        stripped = line.strip()

        if stripped.startswith("ICCAP_VALUES"):
            in_values_section = True
            continue

        if in_values_section and stripped.startswith(("ICCAP_INPUTS", "ICCAP_OUTPUTS")):
            logging.error("section order is wrong")
            break

        if in_values_section and stripped:
            parts = stripped.split(None, 1)  # stop after first split only 2
            if len(parts) == 2:
                key, value = parts
                param_name = key.split(".")[-1]
                if device_type == "hbt":
                    if param_name == "NUM_OF_TRANS_RF":
                        design_params["M"] = convert_value(value)
                    elif param_name == "DEV_GEOM_L":
                        design_params["L"] = convert_value(value)
                    elif param_name == "DEV_GEOM_W":
                        design_params["W"] = convert_value(value)
                    elif param_name == "REMARKS":
                        nx_match = re.search(r"Nx=(\d+)", value)
                        if nx_match:
                            design_params["Nx"] = int(nx_match.group(1))
                if param_name in DESIGN_PARAMETERS:
                    design_params[param_name] = convert_value(value)

    return design_params


def parse_data_block(
    block_lines: List[str], input_variables: Set[str]
) -> Tuple[Dict[str, float | str], pd.DataFrame]:
    """
    Parse a single data block into metadata and DataFrame.

    Args:
        block_lines: Lines from the data block
        input_variables: Set of input variable names

    Returns:
        Tuple of (metadata_dict, dataframe)
    """
    metadata = {}
    data_rows = []
    column_names = []
    header_found = False

    for line in block_lines:
        stripped = line.strip()
        if not stripped:
            continue

        if not header_found and stripped.startswith("#"):
            column_names = stripped.lstrip("#").split()
            header_found = True
            continue

        if not header_found:
            if stripped.startswith("ICCAP_VAR"):
                parts = stripped.split(None, 2)
                if len(parts) == 3:
                    var_name = parts[1]
                    var_value = parts[2]
                    metadata[var_name] = convert_value(var_value)
            else:
                parts = stripped.split(None, 1)
                if len(parts) == 2:
                    param_name, param_value = parts
                    if param_name in input_variables or param_name in DESIGN_PARAMETERS:
                        metadata[param_name] = convert_value(param_value)
        else:
            values = stripped.split()
            if column_names and len(values) == len(column_names):
                converted_values = [convert_value(val) for val in values]
                data_rows.append(converted_values)

    if column_names and data_rows:
        dataframe = pd.DataFrame(data_rows, columns=column_names)
    else:
        dataframe = pd.DataFrame()

    return metadata, dataframe


def setup_global_logging(log_file: str = "./mdm_parser.logs") -> None:

    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)

    root.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setLevel(logging.INFO)
    file_fmt = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    fh.setFormatter(file_fmt)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    console_fmt = logging.Formatter("%(levelname)s %(message)s")
    ch.setFormatter(console_fmt)

    root.addHandler(fh)
    root.addHandler(ch)

    logging.captureWarnings(True)

    logging.info("Global logging setup complete.")


def infer_step(vals) -> float:
    """
    Infer step size from a numeric sequence when all steps are equal.
    Returns 0.0 if less than two points.
    """
    step = vals[1] - vals[0]
    return round(step, 12)


def normalize_master_setup_type(val: Optional[str]) -> Optional[str]:
    """Normalize master setup type values for consistent grouping."""
    if val is None:
        return None
    s = str(val).strip().strip("~").strip()
    return s.lower() if s else None


def safe_name(s: Optional[str]) -> str:
    """Create a filesystem-safe name from a string."""
    if not s:
        return "unknown"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


def _split_filename_parts(file_path: Path) -> list[str]:
    """Extract meaningful parts from filename stem split by underscores."""
    stem = file_path.stem
    return [p for p in stem.split("_") if p]


def derive_master_setup_type_from_filename(file_path: Path) -> str:
    parts = _split_filename_parts(file_path)

    if not parts:
        return "unknown"

    if parts[0].upper() in ("CBE", "CBC"):
        return parts[0].upper()

    return f"{parts[0]}_{parts[1]}"


def get_dut_params(file_path: Path):
    """
    Return (a, p) values for the given DUT.
    Falls back to default values if DUT not found.
    """
    parts = _split_filename_parts(file_path)
    dut_name = parts[-1].upper()
    params = DUTS.get(dut_name.upper(), {"a": 2e-12, "p": 6e-6})
    return params["a"], params["p"]


def derive_sweep_var(sweep_var: str, volt_name: str) -> str:
    if volt_name == sweep_var:
        return sweep_var

    combos = {
        frozenset(["vb", "vc"]): "vcb",
        frozenset(["vb", "ve"]): "vbe",
        frozenset(["vc", "ve"]): "vce",
    }
    key = frozenset([volt_name, sweep_var])
    if key in combos:
        return combos[key]

    return sweep_var
