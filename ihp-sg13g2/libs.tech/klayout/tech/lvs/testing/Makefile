#==========================================================================
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
#==========================================================================

#=========================================================================
# ---------------------------------- LVS ---------------------------------
#=========================================================================

SHELL        := /bin/bash

.DEFAULT_GOAL := all

all: test-LVS

test-LVS: test-LVS-switch  test-LVS-main

#=================================
# ----- test-LVS_regression ------
#=================================

.ONESHELL:
test-LVS-main: test-LVS-MOS test-LVS-RFMOS test-LVS-BJT test-LVS-DIODE test-LVS-RES test-LVS-CAP test-LVS-ESD test-LVS-IND test-LVS-TAP

.ONESHELL:
test-LVS-%:
	@echo "========== LVS-$* testing =========="
	@ python3 run_regression.py --device=$*

#=================================
# -------- test-LVS-switch -------
#=================================

.ONESHELL:
test-LVS-switch:
	@echo "========== LVS-Switch Testing =========="
	@python3 ../run_lvs.py --layout=testcases/extraction_checking/sg13_lv_nmos.gds --netlist=testcases/extraction_checking/sg13_lv_nmos.cdl --run_mode=deep --run_dir=test_nmos_deep
	@python3 ../run_lvs.py --layout=testcases/extraction_checking/sg13_lv_nmos.gds --netlist=testcases/extraction_checking/sg13_lv_nmos.cdl --run_mode=flat --run_dir=test_nmos_flat

.ONESHELL:
list-devices:
	@echo "test-LVS-MOS"
	@echo "test-LVS-RFMOS"
	@echo "test-LVS-BJT"
	@echo "test-LVS-DIODE"
	@echo "test-LVS-RES"
	@echo "test-LVS-CAP"
	@echo "test-LVS-ESD"
	@echo "test-LVS-IND"
	@echo "test-LVS-TAP"

#==========================
# --------- HELP ----------
#==========================

# Help Target
help:
	@echo "\n ==== The following are some of the valid targets for this Makefile ====\n"
	@echo "... all                        (the default if no target is provided             )"
	@echo "... test-LVS                   (To run LVS for all devices with switching test   )"
	@echo "... test-LVS-main              (To run LVS for all devices                       )"
	@echo "... test-LVS-switch            (To run simple LVS switching test                 )"
	@echo "... test-LVS-<device>          (To run LVS for specific device group             )"
	@echo "... list-devices               (To list all available device groups              )"
