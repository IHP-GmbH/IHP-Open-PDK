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
Open-short de-embedding of 2-port S-parameters with the OPEN and SHORT dummy structures:

    Y_dut = [ (Y_raw - Y_open)^-1 - (Y_short - Y_open)^-1 ]^-1

Used (1) by the S-parameter verifier for a file whose IC-CAP de-embedded S (`S_deemb`) is a
copy of another file's (config `sparam_self_deembed`), and (2) by
tools/check_hbt_deembedding.py, which recomputes IC-CAP's `S_deemb` of every file from its raw
`S` to check it. All arrays are (nf, 2, 2) complex.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from models_verifier.mdm_processing.sparam_parser import parse_sparam_mdm
from models_verifier.sp_runner.extract import s_to_y


def open_short(y_raw: np.ndarray, y_open: np.ndarray, y_short: np.ndarray) -> np.ndarray:
    """Open-short de-embedding in the Y domain; returns Y of the device."""
    z_dut = np.linalg.inv(y_raw - y_open) - np.linalg.inv(y_short - y_open)
    return np.linalg.inv(z_dut)


def dummy_y(path: Path, freq: np.ndarray) -> np.ndarray:
    """Y of a dummy structure (its first block, raw S) at the frequencies `freq` of the device file."""
    block = parse_sparam_mdm(path, s_column="S").bias_points[0]
    if block.freq.shape != freq.shape or not np.allclose(block.freq, freq):
        raise ValueError(f"{Path(path).name}: frequencies differ from the device file")
    return s_to_y(block.freq, block.s)
