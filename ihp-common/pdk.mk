#==========================================================================
# Copyright 2026 IHP PDK Authors
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

# Regression targets shared by every PDK in this repository. The repository
# Makefile includes this once, for the PDK named by $(PDK), and then includes
# that PDK's own Makefile.<pdk> for anything specific to it.
#
# Every target here reports and succeeds when this PDK does not carry the test,
# so one CI matrix can call the same target on every PDK without the workflow
# tracking which PDK implements what. A mistyped target still fails, because an
# unknown target has no rule at all.
#
# Requires from the including Makefile: TOP_DIR, PDK_DIR, PDK_NAME and the
# `env` target.

# One venv for the whole repository: there is a single requirements.txt and a
# single klayout pin in versions.txt, and CI asserts the installed package
# matches the installed binary. A venv per PDK would make that assertion
# ambiguous and pip-install the same set twice per matrix leg.
VENV := $(TOP_DIR)/actions_venv/bin/activate

# Paths are relative to the PDK directory. Make runs in the repository root,
# so every use below is either prefixed with $(PDK_DIR) or reached after the
# `cd $(PDK_DIR)` that skip-unless performs.
DRC_TESTS  := libs.tech/klayout/tech/drc/testing
LVS_TESTS  := libs.tech/klayout/tech/lvs/testing
SRAM_TESTS := libs.qa/sram

LVS_MAKE = $(MAKE) --no-print-directory -C $(PDK_DIR)/$(LVS_TESTS)

# Run $(2) inside $(PDK_DIR) with the venv active, or report and succeed when
# $(1) is absent.
#
# The skip is deliberately loud. A green check that ran nothing looks exactly
# like a green check that passed, so ::notice:: puts it in the pull request's
# Checks view and the summary line puts it in the job summary.
#
# $(1) = file that must exist for this test to mean anything, relative to the PDK
# $(2) = command to run when it does, from inside the PDK directory
define skip-unless
@if [ ! -e "$(PDK_DIR)/$(1)" ]; then \
  echo "::notice::Skipping $@: $(PDK_NAME) has no $(1)"; \
  echo "- Skipped \`$@\`: $(PDK_NAME) has no \`$(1)\`" >> "$${GITHUB_STEP_SUMMARY:-/dev/null}"; \
else \
  set -e; . $(VENV); cd $(PDK_DIR); $(2); \
fi
endef

# ========================
# ----- LINTING TEST -----
# ========================

# Both flake8 runs report before the target fails, and the exit status is
# collected explicitly rather than left to the last command. .ONESHELL is a
# global switch in GNU Make, so every recipe here runs in one shell and a
# target's status is only that of its final line -- writing the two runs as
# two plain recipe lines silently discards a DRC failure whenever the LVS run
# that follows it passes.
lint_python: env
	@echo "Running python linting for Klayout-DRC/LVS scripts in $(PDK_NAME)"
	@. $(VENV); \
	 rc=0; \
	 flake8 $(PDK_DIR)/$(dir $(DRC_TESTS)) || rc=1; \
	 flake8 $(PDK_DIR)/$(dir $(LVS_TESTS)) || rc=1; \
	 exit $$rc

lint: lint_python

#=================================
# ----- test-DRC_regression ------
#=================================

.ONESHELL:
test-DRC-main: env
	$(call skip-unless,$(DRC_TESTS)/run_regression.py,\
	  echo "Running Klayout-DRC regression for all unit tests"; \
	  python3 $(DRC_TESTS)/run_regression.py)

#=================================
# -------- test-DRC-cells --------
#=================================

.ONESHELL:
test-DRC-cells: env
	$(call skip-unless,$(DRC_TESTS)/run_regression_cells.py,\
	  echo "Running Klayout-DRC regression for all $(PDK_NAME) cells"; \
	  python3 $(DRC_TESTS)/run_regression_cells.py)

#=================================
# ----- test-LVS_regression ------
#=================================

.ONESHELL:
test-LVS-main: env
	$(call skip-unless,$(LVS_TESTS)/Makefile,\
	  echo "Running Klayout-LVS regression for all devices"; \
	  $(LVS_MAKE) test-LVS-main)

#=================================
# -------- test-LVS-cells --------
#=================================

test-LVS-cells: env
	$(call skip-unless,$(LVS_TESTS)/Makefile,\
	  echo "Running Klayout-LVS for $(PDK_NAME) cells"; \
	  $(LVS_MAKE) test-LVS-cells)

#=================================
# -------- test-LVS-switch -------
#=================================

test-LVS-switch: env
	$(call skip-unless,$(LVS_TESTS)/Makefile,\
	  echo "Running Klayout-LVS switch test"; \
	  $(LVS_MAKE) test-LVS-switch)

#=================================
# -------- test-LVS-<name> -------
#=================================

# Catch-all for the device groups and the extra check suites the LVS testing
# Makefile defines (test-LVS-MOS, test-LVS-SVS, test-LVS-cmomi-checks, ...).
# It cannot skip on a missing target the way the rules above do, so an unknown
# name fails down there rather than here.
.ONESHELL:
test-LVS-%: env
	$(call skip-unless,$(LVS_TESTS)/Makefile,\
	  echo "Running Klayout-LVS regression for $* "; \
	  $(LVS_MAKE) test-LVS-$*)

#=================================
# --------- test-SRAM ------------
#=================================

test-SRAM: env
	$(call skip-unless,$(SRAM_TESTS)/validate_sram.py,\
	  echo "Validating $(PDK_NAME) SRAM views and Verilog models"; \
	  python3 $(SRAM_TESTS)/validate_sram.py)

#==========================
# --------- HELP ----------
#==========================

# Double-colon so the repository Makefile and the per-PDK file can append their
# own targets to this listing.
help::
	@echo ""
	@echo " ==== Targets for $(PDK_NAME) ===="
	@echo ""
	@echo "Targets this PDK does not implement report and succeed."
	@echo ""
	@echo "... lint                       (Run python linting for DRC/LVS scripts        )"
	@echo "... test-DRC-main              (Run DRC regression for all unit tests         )"
	@echo "... test-DRC-cells             (Run DRC regression for all cells              )"
	@echo "... test-LVS-main              (Run LVS for all devices                       )"
	@echo "... test-LVS-<device>          (Run LVS for specific device group             )"
	@echo "... test-LVS-cells             (Run LVS for all standard cells                )"
	@echo "... test-LVS-switch            (Run simple LVS switching test                 )"
	@echo "... test-SRAM                  (Validate SRAM views and Verilog models        )"

.PHONY: lint lint_python test-DRC-main test-DRC-cells test-LVS-main \
        test-LVS-cells test-LVS-switch test-SRAM help
