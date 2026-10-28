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
Unit tests for how the S-parameter verifier takes a measured 2-port (no simulation):
  - open-short de-embedding recovers a device placed between known pads;
  - on the npn13g2_T03 data, de-embedding the raw S with the folder's dummies reproduces
    IC-CAP's S_deemb of a genuine file (spar_vcb05);
  - the copy guard stops on spar_vcb05, whose S_deemb is identical to spar_vcb10's, unless the
    copy is declared;
  - a file without S_deemb is judged only when it is listed in sparam_allow_raw.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from models_verifier.mdm_processing.sparam_parser import parse_sparam_mdm
from models_verifier.models_verifier import VerificationError
from models_verifier.sp_runner.deembed import dummy_y, open_short
from models_verifier.sp_runner.extract import s_to_y
from models_verifier.sp_runner.verifier import SparamVerifier

HBT = Path(__file__).resolve().parents[6] / "libs.doc" / "meas" / "HBT"


def _verifier(folder: str, copied=(), allow_raw=()) -> SparamVerifier:
    """A SparamVerifier with just the attributes `_measured_y` needs (no config file, no run)."""
    v = object.__new__(SparamVerifier)
    v.config = {"mdm_dir": str(HBT / folder)}
    v.self_deembed = {}
    v.copied_deemb = set(copied)
    v.allow_raw = set(allow_raw)
    v._sdeemb_cache = {}
    return v


def test_open_short_recovers_the_device():
    rng = np.random.default_rng(1)
    nf = 4
    y_dut = rng.normal(size=(nf, 2, 2)) + 1j * rng.normal(size=(nf, 2, 2))
    y_open = 1j * np.abs(rng.normal(size=(nf, 2, 2))) * 1e-3          # pad capacitances
    z_series = (0.5 + 1j * rng.normal(size=(nf, 1, 1))) * np.eye(2)  # series lead impedance
    y_short = np.linalg.inv(z_series) + y_open
    y_raw = np.linalg.inv(np.linalg.inv(y_dut) + z_series) + y_open
    assert np.allclose(open_short(y_raw, y_open, y_short), y_dut)


def test_raw_s_with_dummies_reproduces_iccap_deembedding():
    folder = HBT / "npn13g2_T03"
    raw = parse_sparam_mdm(folder / "spar_vcb05.mdm", s_column="S").bias_points
    deemb = parse_sparam_mdm(folder / "spar_vcb05.mdm").bias_points
    y_open = dummy_y(folder / "dummy_open_D54.mdm", raw[0].freq)
    y_short = dummy_y(folder / "dummy_short_D64.mdm", raw[0].freq)
    for r, d in zip(raw[:5], deemb[:5]):
        y_new = open_short(s_to_y(r.freq, r.s), y_open, y_short)
        y_file = s_to_y(d.freq, d.s)
        assert np.max(np.abs(y_new - y_file)) < 1e-4 * np.max(np.abs(y_file))


def test_copy_guard_stops_on_copied_sdeemb_unless_declared():
    path = HBT / "npn13g2_T03" / "spar_vcb05.mdm"
    with pytest.raises(VerificationError, match="identical to spar_vcb10"):
        _verifier("npn13g2_T03")._check_not_a_copy(path)
    _verifier("npn13g2_T03", copied=["spar_vcb10"])._check_not_a_copy(path)   # no error


def test_raw_only_file_needs_opt_in():
    with pytest.raises(VerificationError, match="sparam_allow_raw"):
        _verifier("npn13g2_T00")._measured_y("spar_vce")
    _data, _ys, source = _verifier("npn13g2_T00", allow_raw=["spar_vce"])._measured_y("spar_vce")
    assert source == "S"
