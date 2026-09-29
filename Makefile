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

# The only Makefile in this repository, and the only place make is started
# from. The PDK directories carry no build rules of their own: tools such as
# Ciel archive them for distribution, and a build system is not part of a PDK.
#
# The regression targets every PDK shares live in ihp-common/pdk.mk. Anything
# specific to one PDK lives in Makefile.<pdk> beside this file, included below
# for the selected PDK only.
#
#     make test-DRC-main                      # the default PDK
#     make test-DRC-main PDK=ihp-sg13cmos5l   # another one
#     make help PDK=ihp-sg13cmos5l            # what that PDK offers

# The top directory where environment will be created. Evaluated before any
# include, so $(MAKEFILE_LIST) still ends in this file.
TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
VENV_RUN_COMMAND = $(TOP_DIR)/actions_venv/bin/activate

# The PDK that `make test-...` targets when none is named.
PDK ?= ihp-sg13g2

PDK_DIR  := $(TOP_DIR)/$(PDK)
PDK_NAME := $(PDK)

# Catch a mistyped or missing PDK here, by name. Without this the shared rules
# below would report every test as "not carried by this PDK" and succeed, which
# is the same output a real but incomplete PDK produces.
ifeq ($(wildcard $(PDK_DIR)/libs.tech),)
$(error PDK '$(PDK)' not found: no $(PDK_DIR)/libs.tech. Set PDK to one of: $(patsubst $(TOP_DIR)/%/libs.tech,%,$(wildcard $(TOP_DIR)/ihp-*/libs.tech)))
endif

# A pip `requirements.txt` file.
# https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
REQUIREMENTS_FILE := requirements.txt

.DEFAULT_GOAL := help

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

# Every PDK at once, for local use. `make lint` is the selected PDK only and
# comes from ihp-common/pdk.mk, which is what CI runs one leg per PDK.
lint-all: env
	@echo "Running python linting for Klayout-DRC/LVS scripts in every PDK"
	@. $(VENV_RUN_COMMAND); flake8 $(TOP_DIR)/ihp-*/libs.tech/klayout/tech/drc
	@. $(VENV_RUN_COMMAND); flake8 $(TOP_DIR)/ihp-*/libs.tech/klayout/tech/lvs

#==========================
# --------- HELP ----------
#==========================

# Double-colon, matching pdk.mk and the per-PDK files, so all three append to
# one listing. This one is defined first and therefore prints first.
help::
	@echo ""
	@echo " ==== Repository-wide targets ===="
	@echo ""
	@echo "... env                        (Create the shared Python virtual environment  )"
	@echo "... lint-all                   (Run python linting across every PDK           )"
	@echo ""
	@echo "Everything below acts on \$$(PDK), currently '$(PDK)'."
	@echo "Select another with e.g. PDK=ihp-sg13cmos5l."

#=================================
# --------- REGRESSIONS ----------
#=================================

# The regression targets shared by every PDK. A PDK reports and succeeds on a
# target it does not carry, so the same target can be called for each PDK
# without this file knowing which ones are real.
include $(TOP_DIR)/ihp-common/pdk.mk

# The targets only $(PDK) carries. Optional: a PDK may add nothing of its own.
# A typo in PDK cannot land here silently, it is caught by the check above.
-include $(TOP_DIR)/Makefile.$(PDK:ihp-%=%)

.PHONY: env lint-all help
