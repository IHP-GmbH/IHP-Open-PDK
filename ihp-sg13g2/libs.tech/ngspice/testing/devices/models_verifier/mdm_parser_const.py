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

import re

DESIGN_PARAMETERS = frozenset(
    {"W", "L", "NF", "M", "AD", "AS", "PD", "PS", "TEMP", "TNOM", "MASTER_SETUP_TYPE"}
)

UNIT_REGEX = re.compile(
    r"^(?P<num>[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)(?P<unit>[unpmkfµ]?)$"
)

UNIT_MULTIPLIERS = {
    "f": 1e-15,
    "p": 1e-12,
    "n": 1e-9,
    "µ": 1e-6,
    "u": 1e-6,
    "m": 1e-3,
    "k": 1e3,
}

DUTS = {
    "DUT1": {"a": 20e-6, "p": 24e-6},
    "DUT2": {"a": 10e-6, "p": 22e-6},
    "DUT4": {"a": 5e-6, "p": 12e-6},
    "DUT6": {"a": 4e-6, "p": 8e-6},
    "DUT7": {"a": 2e-6, "p": 6e-6},
    "DUT8": {"a": 2e-6, "p": 6e-6},
    "DUT10": {"a": 1e-6, "p": 4e-6},
    "DUT11": {"a": 1.36e-6, "p": 5.36e-6},
    "DUT12": {"a": 0.68e-6, "p": 3.36e-6},
}
