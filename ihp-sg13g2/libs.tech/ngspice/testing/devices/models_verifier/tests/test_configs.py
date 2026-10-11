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
Unit tests for configuration and geometry helpers:
  - `base_config`: a variant config replaces whole top-level keys of its device config;
  - every HBT variant config reads, points at an existing folder and has its own exception folders;
  - pnpMPA DUT geometry: emitter and n-well per DUT, an unknown DUT raises (no silent default),
    also through the aggregator (a file that cannot be parsed stops the run);
  - a missing `setup_templates` file is a configuration error.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import shutil

from models_verifier.constants import DUTS
from models_verifier.mdm_processing.aggregator import MdmDirectoryAggregator
from models_verifier.mdm_processing.parser import MdmParseError
from models_verifier.mdm_processing.utils import get_dut_params
from models_verifier.models_verifier import ConfigError, MdmVerifier, read_config

ROOT = Path(__file__).resolve().parents[2]


def test_base_config_replaces_whole_keys(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "base.yaml").write_text("device_name: npn13g2l\ndesign_param_overrides: {Nx: 4}\nmetrics: [ib]\n")
    (tmp_path / "variant.yaml").write_text("base_config: base.yaml\ndesign_param_overrides: {}\nmdm_dir: x\n")
    config = read_config(tmp_path / "variant.yaml")
    assert config == {"device_name": "npn13g2l", "design_param_overrides": {}, "metrics": ["ib"], "mdm_dir": "x"}


def test_hbt_variant_configs(monkeypatch):
    monkeypatch.chdir(ROOT)
    variants = sorted((ROOT / "configs/hbt/variants").glob("*.yaml"))
    assert len(variants) == 11
    for path in variants:
        config = read_config(path)
        assert (ROOT / config["mdm_dir"]).is_dir(), path
        assert config["output_dir"] == f"models_results/{path.stem}"
        assert config["waivers_dir"] == f"waivers/variants/{path.stem}"
        assert config["sparam_waivers_dir"] == f"waivers/variants/{path.stem}/sparam"
    assert read_config(ROOT / "configs/hbt/variants/npn13g2l_T00.yaml")["design_param_overrides"] == {"Nx": 2}
    assert read_config(ROOT / "configs/hbt/variants/npn13g2l_T02.yaml")["design_param_overrides"] == {}


def test_pnpmpa_geometry():
    assert get_dut_params(Path("fg_vce_d0406_DUT15.mdm")) == {"A": 0.204e-12, "P": 1.96e-6, "AC": 5.98e-12, "PC": 9.8e-6}
    assert get_dut_params(Path("fg_vce_d0406_DUT7.mdm"))["AC"] == 13.328e-12      # the subckt default
    assert "DUT3" not in DUTS
    with pytest.raises(ValueError, match="No pnpMPA geometry"):
        get_dut_params(Path("fg_vce_d0406_DUT3.mdm"))


def test_unknown_dut_stops_the_aggregation(tmp_path):
    pnp = ROOT / "../../../../libs.doc/meas/pnpMPA"
    shutil.copy(pnp / "fg_vce_d0406_DUT7.mdm", tmp_path / "fg_vce_d0406_DUT7.mdm")
    shutil.copy(pnp / "fg_vce_d0406_DUT7.mdm", tmp_path / "fg_vce_d0406_DUT99.mdm")
    with pytest.raises(MdmParseError, match="DUT99"):
        MdmDirectoryAggregator(input_dir=tmp_path, device_type="pnpmpa").aggregate()
    excluded = MdmDirectoryAggregator(input_dir=tmp_path, device_type="pnpmpa", exclude_patterns=["_DUT99.mdm"])
    assert [p.name for p in excluded.find_mdm_files()] == ["fg_vce_d0406_DUT7.mdm"]


def test_missing_setup_template_is_a_config_error(tmp_path):
    config = tmp_path / "c.yaml"
    config.write_text("mdm_dir: x\ndc_template_path: t\ncorner_lib_path: l\ndevice_type: mos\ndevice_name: d\n"
                      "metrics: [id]\noutput_dir: o\nsetup_templates: {di_bd_area: missing.j2}\n")
    with pytest.raises(ConfigError, match="di_bd_area"):
        object.__new__(MdmVerifier)._load_config(config)
