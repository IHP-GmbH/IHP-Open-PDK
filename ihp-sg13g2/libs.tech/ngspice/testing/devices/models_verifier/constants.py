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
    {"W", "L", "NF", "M", "AD", "AS", "PD", "PS", "TEMP", "MASTER_SETUP_TYPE"}
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

# pnpMPA DUT geometries (single transistors of test chip T323): emitter area a (m^2) and
# perimeter p (m), n-well (base) area ac (m^2) and perimeter pc (m; not used by the model card).
# The substrate is the collector. The pnpMPA subckt
# scales its model card with dev_a = a*1e12 (um^2) and dev_p = p*1e6 (um), so 1 um^2 is 1e-12.
# Emitter W x L of DUT1-12 from libs.doc/meas/pnpMPA/doc/setup/dc_new.htm; the other DUTs and
# every n-well from the layout test_structures/T323_pnpMPA_DC_all.gds (emitter = Activ & pSD &
# NWell, n-well = layer 31; the layout reproduces the documented DUTs exactly). DUT7's n-well
# equals the subckt default (ac=13.328p, pc=14.64u).
# DUT3 (2 x 5 um) is not listed: its measured IC is 5 % of the area/perimeter scaling of the
# other DUTs (defective or mis-measured device); its files are excluded in the config.
# DUT16 is the capacitance array: 12000 cells of 0.64 x 10 um (values per cell; m = 12000).
DUTS = {
    "DUT1": {"a": 20e-12, "p": 24e-6, "ac": 64.368e-12, "pc": 34.64e-6},
    "DUT2": {"a": 10e-12, "p": 22e-6, "ac": 40.528e-12, "pc": 30.64e-6},
    "DUT4": {"a": 5e-12, "p": 12e-6, "ac": 23.528e-12, "pc": 20.64e-6},
    "DUT5": {"a": 3e-12, "p": 20.6e-6, "ac": 27.416e-12, "pc": 28.44e-6},
    "DUT6": {"a": 4e-12, "p": 8e-6, "ac": 21.168e-12, "pc": 18.64e-6},
    "DUT7": {"a": 2e-12, "p": 6e-6, "ac": 13.328e-12, "pc": 14.64e-6},
    "DUT8": {"a": 2e-12, "p": 6e-6, "ac": 15.768e-12, "pc": 16.64e-6},
    "DUT9": {"a": 1.5e-12, "p": 10.6e-6, "ac": 15.916e-12, "pc": 18.44e-6},
    "DUT10": {"a": 1e-12, "p": 4e-6, "ac": 9.928e-12, "pc": 12.64e-6},
    "DUT11": {"a": 1.36e-12, "p": 5.36e-6, "ac": 14.040e-12, "pc": 16.00e-6},
    "DUT12": {"a": 0.68e-12, "p": 3.36e-6, "ac": 8.840e-12, "pc": 12.00e-6},
    "DUT13": {"a": 0.6e-12, "p": 4.6e-6, "ac": 9.016e-12, "pc": 12.44e-6},
    "DUT14": {"a": 0.3e-12, "p": 2.6e-6, "ac": 6.716e-12, "pc": 10.44e-6},
    "DUT15": {"a": 0.204e-12, "p": 1.96e-6, "ac": 5.980e-12, "pc": 9.80e-6},
    "DUT16": {"a": 6.4e-12, "p": 21.28e-6, "ac": 31.946e-12, "pc": 29.2e-6},
}

CASES = [
    ("nmos_lv", "configs/mos/nmos_lv/sg13_lv_nmos.yaml"),
    ("pmos_lv", "configs/mos/pmos_lv/sg13_lv_pmos.yaml"),
    ("nmos_hv", "configs/mos/nmos_hv/sg13_hv_nmos.yaml"),
    ("pmos_hv", "configs/mos/pmos_hv/sg13_hv_pmos.yaml"),
    ("pnp_mpa", "configs/pnp_mpa/pnpmpa.yaml"),
    ("npn13g2", "configs/hbt/npn13g2/npn13g2.yaml"),
    ("npn13g2l", "configs/hbt/npn13g2l/npn13g2l.yaml"),
    ("npn13g2v", "configs/hbt/npn13g2v/npn13g2v.yaml"),
]
