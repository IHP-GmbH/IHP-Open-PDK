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

# The top directory where environment will be created.
TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
VENV_RUN_COMMAND = $(TOP_DIR)/actions_venv/bin/activate

# Path to regressions
KLAYOUT_DRC_TESTS := ihp-sg13g2/libs.tech/klayout/tech/drc/testing/
KLAYOUT_LVS_TESTS := ihp-sg13g2/libs.tech/klayout/tech/lvs/testing

# A pip `requirements.txt` file.
# https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
REQUIREMENTS_FILE := requirements.txt

# ======================= 
# ------ ENV SETUP ------ 
# =======================

$(TOP_DIR)/actions_venv:
	@python3 -m venv $(TOP_DIR)/actions_venv

# Install requirements
# tkinter is listed in requirements.txt but is not a PyPI package (it ships as the
# system package python3-tk), so pip aborts the whole install. Temporary waiver:
# if the install fails, warn and retry without tkinter so CI proceeds. A real
# dependency failure still aborts because the retry keeps every other package.
env: $(TOP_DIR)/actions_venv
	@. $(VENV_RUN_COMMAND); \
	pip install -r $(REQUIREMENTS_FILE) || { \
		echo "::warning::pip install failed on tkinter (not a PyPI package; install python3-tk via the system package manager). Continuing without it so CI can proceed."; \
		grep -vx 'tkinter' $(REQUIREMENTS_FILE) | pip install -r /dev/stdin; \
	}

# ========================
# ----- LINTING TEST -----
# ========================

# Lint python code
lint_python: env
	@echo "Running python linting for Klayout-DRC/LVS scripts"
	@. $(VENV_RUN_COMMAND); flake8 ihp-sg13g2/libs.tech/klayout/tech/drc
	@. $(VENV_RUN_COMMAND); flake8 ihp-sg13g2/libs.tech/klayout/tech/lvs

#=================================
# ----- test-DRC_regression ------
#=================================

.ONESHELL:
test-DRC-main: env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-DRC regression for all unit tests"
	@. $(VENV_RUN_COMMAND); python3 $(KLAYOUT_DRC_TESTS)/run_regression.py

#=================================
# -------- test-DRC-cells --------
#=================================

.ONESHELL:
test-DRC-cells: env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-DRC regression for all SG13G2 cells"
	@. $(VENV_RUN_COMMAND); python3 $(KLAYOUT_DRC_TESTS)/run_regression_cells.py

#=================================
# ----- test-LVS_regression ------
#=================================

.ONESHELL:
test-LVS-main: env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-LVS regression for all devices"
	@. $(VENV_RUN_COMMAND); cd $(KLAYOUT_LVS_TESTS) && make test-LVS-main

.ONESHELL:
test-LVS-% : env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-LVS regression for $* device"
	@. $(VENV_RUN_COMMAND); cd $(KLAYOUT_LVS_TESTS) && make test-LVS-$*

#=================================
# -------- test-LVS-cells --------
#=================================

test-LVS-cells: env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-LVS for SG13G2 cells"
	@. $(VENV_RUN_COMMAND); cd $(KLAYOUT_LVS_TESTS) && make test-LVS-cells

#=================================
# -------- test-SVS-cell ---------
#=================================

test-SVS-cell: env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-SVS for SG13G2 cell"
	@. $(VENV_RUN_COMMAND); cd $(KLAYOUT_LVS_TESTS) && make test-SVS-cell

#=================================
# -------- test-SRAM ------------
#=================================

test-SRAM:
	@python3 ihp-sg13g2/libs.qa/sram/validate_sram.py

#=================================
# -------- test-LVS-switch -------
#=================================

test-LVS-switch: env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-LVS switch test"
	@. $(VENV_RUN_COMMAND); cd $(KLAYOUT_LVS_TESTS) && make test-LVS-switch

#=================================
# ---- test-cap-cmomi-model ------
#=================================

# The guard that keeps the cap_cmomi capacitance honest. Six artifacts state it
# and nothing keeps them in step: the Verilog-A, the PCell C= label, the xschem
# tcleval expression, the qucs-s symbol equation, the copy of that equation
# pasted into the qucs-s example, and the two stored simulator references. The
# test asks each of them for the same devices and compares against the Verilog-A
# built here, which is what a simulation runs.
#
# No venv: it drives klayout, ngspice, openvaf and tclsh directly. Skips rather
# than fails when one of those is missing, like test-gnucap, so DRC/LVS work is
# not blocked by an absent simulator.
CAP_CMOMI_MODEL_TOOLS = klayout ngspice tclsh

.ONESHELL:
test-cap-cmomi-model:
	@for tool in $(CAP_CMOMI_MODEL_TOOLS); do \
	  if ! command -v $$tool >/dev/null 2>&1; then \
	    echo "Skipping: $$tool not installed"; \
	    exit 0; \
	  fi; \
	done; \
	if ! command -v openvaf-r >/dev/null 2>&1 && ! command -v openvaf >/dev/null 2>&1; then \
	  echo "Skipping: no Verilog-A compiler installed"; \
	  exit 0; \
	fi; \
	cd ihp-sg13g2/libs.tech/klayout/sg13g2_tests && \
	python3 cap_cmomi_consistency_test.py
