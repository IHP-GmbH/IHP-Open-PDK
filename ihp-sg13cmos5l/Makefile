#==========================================================================
# Copyright 2025 IHP PDK Authors
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
VENV_RUN_COMMAND = $(TOP_DIR)/.venv/bin/activate

# Path to regressions
KLAYOUT_DRC_TESTS := libs.tech/klayout/tech/drc/testing
KLAYOUT_LVS_TESTS := libs.tech/klayout/tech/lvs/testing

# A pip `requirements.txt` file (use parent repo's requirements)
REQUIREMENTS_FILE := ../requirements.txt

# =======================
# ------ ENV SETUP ------
# =======================

$(TOP_DIR)/.venv:
	@python3 -m venv $(TOP_DIR)/.venv

# Install requirements
env: $(TOP_DIR)/.venv
	@. $(VENV_RUN_COMMAND); pip install -r $(REQUIREMENTS_FILE)

# ========================
# ----- LINTING TEST -----
# ========================

# Lint python code
lint_python: env
	@echo "Running python linting for Klayout-DRC/LVS scripts"
	@. $(VENV_RUN_COMMAND); flake8 libs.tech/klayout/tech/drc
	@. $(VENV_RUN_COMMAND); flake8 libs.tech/klayout/tech/lvs || true

lint: lint_python

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
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-LVS for SG13CMOS5L cells"
	@. $(VENV_RUN_COMMAND); cd $(KLAYOUT_LVS_TESTS) && make test-LVS-cells

#=================================
# -------- test-LVS-switch -------
#=================================

test-LVS-switch: env
	@. $(VENV_RUN_COMMAND); echo "Running Klayout-LVS switch test"
	@. $(VENV_RUN_COMMAND); cd $(KLAYOUT_LVS_TESTS) && make test-LVS-switch

#=================================
# --------- test-gnucap ----------
#=================================

# Builds the Verilog-A model plugins, then runs the Gnucap and Ngspice test
# suites over them. Both suites diff against checked-in reference data and this
# target propagates their exit status, so it goes red on a model regression.
#
# Skips rather than fails when the toolchain or PDK_ROOT is absent, so that
# contributors working on DRC/LVS are not blocked by a missing simulator. The
# checks are deliberately specific: the plugin build alone takes tens of minutes,
# so anything that would make the run fail at the end is worth catching up front.
GNUCAP_TOOLS = gnucap gnucap-mg-vams ngspice

.ONESHELL:
test-gnucap:
	@for tool in $(GNUCAP_TOOLS); do \
	  if ! command -v $$tool >/dev/null 2>&1; then \
	    echo "Skipping: $$tool not installed (see libs.tech/gnucap/README.md)"; \
	    exit 0; \
	  fi; \
	done; \
	if [ -z "$$PDK_ROOT" ]; then \
	  echo "Skipping: PDK_ROOT is not set (see libs.tech/gnucap/README.md)"; \
	elif [ ! -d "$$PDK_ROOT/ihp-sg13cmos5l" ]; then \
	  echo "Skipping: no ihp-sg13cmos5l under PDK_ROOT=$$PDK_ROOT"; \
	  echo "  (the Ngspice suite reads its model cards from there)"; \
	elif [ ! -d "$$PDK_ROOT/ihp-sg13g2" ]; then \
	  echo "Skipping: no ihp-sg13g2 under PDK_ROOT=$$PDK_ROOT"; \
	  echo "  (this directory is symlinked into it, see libs.tech/gnucap/README.md)"; \
	elif [ ! -e "$$PDK_ROOT/ihp-sg13cmos5l/libs.tech/ngspice/osdi/psp103.osdi" ]; then \
	  echo "Skipping: the OSDI objects are not built"; \
	  echo "  cd \$$PDK_ROOT/ihp-sg13g2/libs.tech/verilog-a && ./openvaf-compile-va.sh"; \
	  echo "  (they are a gitignored build product of the sibling PDK, so the"; \
	  echo "   osdi/ symlinks here dangle until that runs, and the Ngspice half"; \
	  echo "   would fail on its first test)"; \
	else \
	  echo "Running Gnucap regression for SG13CMOS5L devices"; \
	  PDK=ihp-sg13cmos5l $(MAKE) -C libs.tech/gnucap check; \
	fi

#==========================
# --------- HELP ----------
#==========================

# Help Target
help:
	@echo "\n ==== The following are some of the valid targets for this Makefile ====\n"
	@echo "... env                        (Create Python virtual environment              )"
	@echo "... lint                       (Run python linting for DRC/LVS scripts        )"
	@echo "... test-DRC-main              (Run DRC regression for all unit tests         )"
	@echo "... test-LVS-main              (Run LVS for all devices                       )"
	@echo "... test-LVS-<device>          (Run LVS for specific device group             )"
	@echo "... test-LVS-cells             (Run LVS for all standard cells                )"
	@echo "... test-LVS-switch            (Run simple LVS switching test                 )"
	@echo "... test-gnucap                (Build model plugins, run the device regression)"

.PHONY: env lint lint_python test-DRC-main test-LVS-main test-LVS-cells test-LVS-switch test-gnucap help
