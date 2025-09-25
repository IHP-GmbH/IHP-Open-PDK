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
MDM Parser Utilities

This module provides utilities to parse measurement data files.
It extracts metadata, design parameters, and tabular data blocks, and
converts them into structured Python objects and pandas DataFrames.

Main features:
- Value conversion with unit scaling
- Metadata and data block parsing
- DUT parameter derivation from filenames
- Logging setup for reproducible runs
"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Generator, Union

import pandas as pd

from models_verifier.constants import (
    DESIGN_PARAMETERS,
    DUTS,
    UNIT_MULTIPLIERS,
    UNIT_REGEX,
)

# ---------------------------
# Value Conversion Utilities
# ---------------------------

def convert_value(value: str) -> Union[float, str]:
    """
    Convert a string value into a float (with unit scaling) or return it as-is.

    Examples:
        >>> convert_value("1.2k")
        1200.0
        >>> convert_value("3.3")
        3.3
        >>> convert_value("remark")
        'remark'

    Args:
        value: A raw string containing a number, optional unit, or arbitrary text.

    Returns:
        Converted float if numeric with optional unit, otherwise the cleaned string.
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
            logging.debug(f"Failed to parse numeric value: {cleaned_value}")
            return cleaned_value

    return cleaned_value


# ---------------------------
# Section Handling
# ---------------------------

def find_section_bounds(
    lines: List[str], start_token: str, end_token: str
) -> Tuple[int, int]:
    """
    Find the start and end indices of a section delimited by tokens.

    Args:
        lines: List of text lines.
        start_token: Marker indicating the start of the section.
        end_token: Marker indicating the end of the section.

    Returns:
        Tuple (start_index, end_index). Returns (-1, -1) if not found.
        The start index is the line *after* the start_token.
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
) -> Tuple[List[str], int]:
    """
    Extract lines from within a section.

    Args:
        lines: Full text split into lines.
        start_token: Section start marker.
        end_token: Section end marker.

    Returns:
        A tuple (section_lines, end_index).
        If start not found → ([], -1).
        If end not found → (remaining_lines, -1).
    """
    start_idx, end_idx = find_section_bounds(lines, start_token, end_token)

    if start_idx == -1:
        logging.warning(f"Section '{start_token}' not found")
        return [], -1
    if end_idx == -1:
        logging.warning(f"End token '{end_token}' not found for section '{start_token}'")
        return lines[start_idx:], -1
    return lines[start_idx:end_idx], end_idx


def extract_data_blocks(lines: List[str]) -> Generator[List[str], None, None]:
    """
    Yield consecutive data blocks marked with BEGIN_DB ... END_DB.

    Args:
        lines: Full file lines.

    Yields:
        Lists of lines belonging to one block.
    """
    current_block: List[str] = []
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
        elif in_block:
            current_block.append(line)


# ---------------------------
# Header & Parameters Parsing
# ---------------------------

def parse_header_inputs(header_lines: List[str]) -> Set[str]:
    """
    Extract input variable names from the ICCAP_INPUTS section.

    Args:
        header_lines: Lines from the file header.

    Returns:
        A set of unique input variable names.
    """
    input_lines, _ = extract_section(header_lines, "ICCAP_INPUTS", "ICCAP_OUTPUTS")
    return {
        line.strip().split()[0]
        for line in input_lines
        if line.strip() and not line.strip().startswith("!")
    }


def parse_design_parameters(
    header_lines: List[str], device_type: str
) -> Dict[str, Union[float, str]]:
    """
    Parse ICCAP_VALUES section to extract design parameters.

    Special handling is applied for HBT devices.

    Args:
        header_lines: Header lines containing ICCAP_VALUES.
        device_type: Device type (e.g., "hbt").

    Returns:
        Dictionary mapping parameter names to values.
    """
    design_params: Dict[str, Union[float, str]] = {}
    in_values_section = False

    for line in header_lines:
        stripped = line.strip()

        if stripped.startswith("ICCAP_VALUES"):
            in_values_section = True
            continue

        if in_values_section and stripped.startswith(("ICCAP_INPUTS", "ICCAP_OUTPUTS")):
            logging.error("Unexpected section order in header")
            break

        if in_values_section and stripped:
            parts = stripped.split(None, 1)
            if len(parts) != 2:
                continue

            key, value = parts
            param_name = key.split(".")[-1]

            # HBT-specific mappings
            if device_type == "hbt":
                if param_name == "NUM_OF_TRANS_RF":
                    design_params["M"] = convert_value(value)
                elif param_name == "DEV_GEOM_L":
                    design_params["L"] = convert_value(value)
                elif param_name == "DEV_GEOM_W":
                    design_params["W"] = convert_value(value)
                elif param_name == "REMARKS":
                    if nx_match := re.search(r"Nx=(\d+)", value):
                        design_params["Nx"] = int(nx_match.group(1))

            if param_name in DESIGN_PARAMETERS:
                design_params[param_name] = convert_value(value)

    return design_params


# ---------------------------
# Data Block Parsing
# ---------------------------

def parse_data_block(
    block_lines: List[str], input_variables: Set[str]
) -> Tuple[Dict[str, Union[float, str]], pd.DataFrame]:
    """
    Parse a single data block into metadata and a DataFrame.

    Args:
        block_lines: Raw lines of a single block.
        input_variables: Set of valid input variable names.

    Returns:
        Tuple (metadata, dataframe).
        - metadata: dict of parameters and ICCAP_VAR values.
        - dataframe: DataFrame of numerical data.
    """
    metadata: Dict[str, Union[float, str]] = {}
    data_rows: List[List[Union[float, str]]] = []
    column_names: List[str] = []
    header_found = False

    for line in block_lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Detect column header
        if not header_found and stripped.startswith("#"):
            column_names = stripped.lstrip("#").split()
            header_found = True
            continue

        if not header_found:
            if stripped.startswith("ICCAP_VAR"):
                _, var_name, var_value = stripped.split(None, 2)
                metadata[var_name] = convert_value(var_value)
            else:
                parts = stripped.split(None, 1)
                if len(parts) == 2:
                    param_name, param_value = parts
                    if param_name in input_variables or param_name in DESIGN_PARAMETERS:
                        metadata[param_name] = convert_value(param_value)
        else:
            values = [convert_value(v) for v in stripped.split()]
            if column_names and len(values) == len(column_names):
                data_rows.append(values)

    dataframe = pd.DataFrame(data_rows, columns=column_names) if column_names else pd.DataFrame()
    return metadata, dataframe


# ---------------------------
# Logging
# ---------------------------

def setup_global_logging(log_file: str | Path) -> None:
    """
    Configure global logging with both file and console handlers.

    Args:
        log_file: Path to log file. Parent directories must exist.
    """
    log_path = Path(log_file)

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.INFO)

    # File handler
    fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        "%Y-%m-%d %H:%M:%S",
    ))

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("%(levelname)s %(message)s"))

    root.addHandler(fh)
    root.addHandler(ch)

    logging.captureWarnings(True)
    logging.info(f"Global logging setup complete. Log file: {log_path}")


# ---------------------------
# Helpers
# ---------------------------

def infer_step(vals: List[float]) -> float:
    """
    Infer the constant step size from a numeric sequence.

    Args:
        vals: List of floats.

    Returns:
        Step size (rounded to 12 decimals).
        Returns 0.0 if fewer than 2 values or steps are inconsistent.
    """
    if len(vals) < 2:
        return 0.0
    steps = {round(vals[i+1] - vals[i], 12) for i in range(len(vals)-1)}
    return steps.pop() if len(steps) == 1 else 0.0


def normalize_master_setup_type(val: Optional[str]) -> Optional[str]:
    """
    Normalize master setup type values for consistent grouping.

    Args:
        val: Raw setup type string.

    Returns:
        Normalized lowercase string or None.
    """
    if val is None:
        return None
    s = str(val).strip("~ ").lower()
    return s or None


def safe_name(s: Optional[str]) -> str:
    """
    Create a filesystem-safe name.

    Args:
        s: Raw string.

    Returns:
        Sanitized name with only alphanumeric, dot, dash, or underscore.
    """
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s or "unknown")


def _split_filename_parts(file_path: Path) -> List[str]:
    """Split filename stem by underscores into meaningful parts."""
    return [p for p in file_path.stem.split("_") if p]


def derive_master_setup_type_from_filename(file_path: Path) -> str:
    """
    Derive master setup type from filename parts.

    Args:
        file_path: Path to file.

    Returns:
        Derived setup type string.
    """
    parts = _split_filename_parts(file_path)
    if not parts:
        return "unknown"
    if parts[0].upper() in ("CBE", "CBC"):
        return parts[0].upper()
    return "_".join(parts[:2]) if len(parts) >= 2 else parts[0]


def get_dut_params(file_path: Path) -> Tuple[float, float]:
    """
    Get (a, p) parameters for a DUT from filename.

    Args:
        file_path: Path to DUT file.

    Returns:
        Tuple (a, p). Defaults to (2e-12, 6e-6) if DUT not recognized.
    """
    parts = _split_filename_parts(file_path)
    dut_name = parts[-1].upper() if parts else "UNKNOWN"
    params = DUTS.get(dut_name, {"a": 2e-12, "p": 6e-6})
    return params["a"], params["p"]


def derive_sweep_var(sweep_var: str, volt_name: str) -> str:
    """
    Derive combined sweep variable name from voltage names.

    Args:
        sweep_var: Primary sweep variable.
        volt_name: Secondary voltage name.

    Returns:
        Combined variable name (e.g., "vcb" for vb + vc).
    """
    if volt_name == sweep_var:
        return sweep_var

    combos = {
        frozenset(["vb", "vc"]): "vcb",
        frozenset(["vb", "ve"]): "vbe",
        frozenset(["vc", "ve"]): "vce",
    }
    return combos.get(frozenset([volt_name, sweep_var]), sweep_var)
