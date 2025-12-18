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

# =========================================================
# Makefile for Device Testing (IHP SG13G2 PDK)
# =========================================================
# Usage:
#   make <target> [RUNNER=verifier|pytest]
#
# Example:
#   make test-all
#   make test-mos RUNNER=pytest
#
# Default runner is 'verifier'.
# =========================================================

# ------------------------
# Global settings
# ------------------------
RUNNER      ?= verifier
PYTEST_ARGS  = --tb=short -p no:capture
PYTEST_FILE  = validation/test_devices.py

VERIFIER_BIN = python3 -m models_verifier.models_verifier
PYTEST_BIN   = python3 -m pytest $(PYTEST_FILE) $(PYTEST_ARGS)

# ------------------------
# Device configuration files
# ------------------------
NMOS_LV_CONFIG  = configs/mos/nmos_lv/sg13_lv_nmos.yaml
PMOS_LV_CONFIG  = configs/mos/pmos_lv/sg13_lv_pmos.yaml
NMOS_HV_CONFIG  = configs/mos/nmos_hv/sg13_hv_nmos.yaml
PMOS_HV_CONFIG  = configs/mos/pmos_hv/sg13_hv_pmos.yaml
PNP_MPA_CONFIG  = configs/pnp_mpa/pnpmpa.yaml
NPN13G2_CONFIG  = configs/hbt/npn13g2/npn13g2.yaml
NPN13G2L_CONFIG = configs/hbt/npn13g2l/npn13g2l.yaml
NPN13G2V_CONFIG = configs/hbt/npn13g2v/npn13g2v.yaml

# ------------------------
# Device groups
# ------------------------
MOS_DEVICES = nmos_lv pmos_lv nmos_hv pmos_hv
HBT_DEVICES = npn13g2 npn13g2l npn13g2v
PNP_DEVICES = pnp_mpa
ALL_DEVICES = $(MOS_DEVICES) $(HBT_DEVICES) $(PNP_DEVICES)

# ------------------------
# Default target
# ------------------------
all: test-all

# ------------------------
# Unified test runner
# ------------------------
define run_test
	@echo ">>> Running $(1) with $(RUNNER) ..."
	@if [ "$(RUNNER)" = "pytest" ]; then \
		$(PYTEST_BIN) -k "$(1)"; \
	else \
		$(VERIFIER_BIN) --config $(2); \
	fi
endef

# ------------------------
# Individual device targets
# ------------------------
test-nmos_lv:   ; $(call run_test,nmos_lv,$(NMOS_LV_CONFIG))
test-pmos_lv:   ; $(call run_test,pmos_lv,$(PMOS_LV_CONFIG))
test-nmos_hv:   ; $(call run_test,nmos_hv,$(NMOS_HV_CONFIG))
test-pmos_hv:   ; $(call run_test,pmos_hv,$(PMOS_HV_CONFIG))
test-pnp_mpa:   ; $(call run_test,pnp_mpa,$(PNP_MPA_CONFIG))
test-npn13g2:   ; $(call run_test,npn13g2,$(NPN13G2_CONFIG))
test-npn13g2l:  ; $(call run_test,npn13g2l,$(NPN13G2L_CONFIG))
test-npn13g2v:  ; $(call run_test,npn13g2v,$(NPN13G2V_CONFIG))

# ------------------------
# Grouped targets
# ------------------------
test-mos:
	@for dev in $(MOS_DEVICES); do $(MAKE) test-$$dev RUNNER=$(RUNNER); done

test-hbt:
	@for dev in $(HBT_DEVICES); do $(MAKE) test-$$dev RUNNER=$(RUNNER); done

test-pnp:
	@for dev in $(PNP_DEVICES); do $(MAKE) test-$$dev RUNNER=$(RUNNER); done

test-all: test-mos test-hbt test-pnp

# ------------------------
# Help message
# ------------------------
help:
	@echo "========================================================="
	@echo " Device Testing Makefile (IHP SG13G2 PDK)"
	@echo "========================================================="
	@echo " Usage:"
	@echo "   make <target> [RUNNER=verifier|pytest]"
	@echo
	@echo " Targets:"
	@echo "   test-all          - Run all device tests"
	@echo "   test-mos          - Run MOS device tests ($(MOS_DEVICES))"
	@echo "   test-hbt          - Run HBT device tests ($(HBT_DEVICES))"
	@echo "   test-pnp          - Run PNP device tests ($(PNP_DEVICES))"
	@echo "   test-<device>     - Run a specific device (e.g. make test-nmos_lv)"
	@echo
	@echo " Options:"
	@echo "   RUNNER=verifier   Use models_verifier (default)"
	@echo "   RUNNER=pytest     Use pytest"
	@echo
	@echo " Examples:"
	@echo "   make test-all"
	@echo "   make test-mos RUNNER=pytest"
	@echo "   make test-npn13g2"
	@echo "   make test-pmos_lv RUNNER=pytest"
