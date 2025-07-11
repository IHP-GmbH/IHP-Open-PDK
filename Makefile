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
env: $(TOP_DIR)/actions_venv
	@. $(VENV_RUN_COMMAND); pip install -r $(REQUIREMENTS_FILE)

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
# -------- test-LVS-switch -------
#=================================

test-LVS-switch: env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-LVS switch test"
	@. $(VENV_RUN_COMMAND); cd $(KLAYOUT_LVS_TESTS) && make test-LVS-switch
