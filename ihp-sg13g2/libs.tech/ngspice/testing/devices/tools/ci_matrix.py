#!/usr/bin/env python3
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
Job matrices of the CI workflow (.github/workflows/device-testing.yml), from toolchain.lock.
Prints GitHub step outputs:
    ngspice=[...]   ngspice versions to build
    openvaf=[...]   OpenVAF-Reloaded commits to build (with the PSP103 objects)
    tests={...}     one job per (toolchain, make target)

Targets with Verilog-A models (MOS) run on every toolchain; test-cv also holds the pnpMPA C-V
case, which therefore runs on every toolchain too (harmless). The other bipolar targets use models
built into ngspice, so they run once per ngspice version (with the first OpenVAF build of the lock).
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

OSDI_TARGETS = ["test-nmos_lv", "test-pmos_lv", "test-nmos_hv", "test-pmos_hv", "test-cv"]
BIPOLAR_TARGETS = ["test-pnp", "test-hbt", "test-hbt-sparam", "test-hbt-variants", "test-hbt-variants-sparam"]

lock = yaml.safe_load((Path(__file__).resolve().parents[1] / "toolchain.lock").read_text())
first_openvaf = next(iter(lock["openvaf"]))
tests = [{"toolchain": tc, "target": t} for tc in lock["toolchains"] for t in OSDI_TARGETS]
tests += [{"toolchain": tc, "target": t} for tc in lock["toolchains"] if tc.endswith(f"-ovr-{first_openvaf}")
          for t in BIPOLAR_TARGETS]
print(f"ngspice={json.dumps(sorted(lock['ngspice']))}")
print(f"openvaf={json.dumps(list(lock['openvaf']))}")
print(f"tests={json.dumps({'include': tests})}")
