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
#   make <target>
#
# Example:
#   make test-all
#   make test-nmos_lv
# =========================================================

# ------------------------
# Global settings
# ------------------------
VERIFIER_BIN = python3 -m models_verifier.models_verifier
SP_VERIFIER_BIN = python3 -m models_verifier.sp_runner.verifier
WAIVER_GEN   = python3 -m models_verifier.waivers.generate
SP_WAIVER_GEN = python3 -m models_verifier.sp_runner.generate
EDA_BIN      = python3 -m models_verifier.eda.run

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
# Unified test runner (models_verifier only)
# ------------------------
define run_test
	@echo ">>> Running $(1) with verifier ..."
	@$(VERIFIER_BIN) --config $(2)
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
	@for dev in $(MOS_DEVICES); do $(MAKE) test-$$dev; done

test-hbt:
	@for dev in $(HBT_DEVICES); do $(MAKE) test-$$dev; done

test-pnp:
	@for dev in $(PNP_DEVICES); do $(MAKE) test-$$dev; done

test-all: test-mos test-hbt test-pnp

# ------------------------
# HBT S-parameter tests (Milestone M4): CjE, CjC, fT (measured vs simulated)
# ------------------------
# Extracts CjE/CjC/fT from the deembedded S-parameters (S_deemb) of the spar_* MDM files
# (S->Y via scikit-rf), runs an ngspice AC 2-port Y extraction of the HBT subckt at the
# same bias grid, and range-checks meas-vs-sim within the MQA windows (reusing the M1
# range-checker + M2 waivers). Results go to <output_dir>/sparam/ so DC results are
# untouched.
test-npn13g2-sparam:   ; $(SP_VERIFIER_BIN) --config $(NPN13G2_CONFIG)
test-npn13g2l-sparam:  ; $(SP_VERIFIER_BIN) --config $(NPN13G2L_CONFIG)
test-npn13g2v-sparam:  ; $(SP_VERIFIER_BIN) --config $(NPN13G2V_CONFIG)

test-hbt-sparam:
	@for dev in $(HBT_DEVICES); do $(MAKE) test-$$dev-sparam; done

# ------------------------
# Waiver / baseline generation (Milestone M2)
# ------------------------
# Snapshots each device's CURRENT (non-waived) Failed range-check rows into
# waivers/<device_name>.yaml. Run after reviewing `make test-all` output; re-run any
# time a NEW/WORSE diff in new_failures.csv is confirmed as an accepted baseline.
waive-all:
	@for dev in $(ALL_DEVICES); do \
		echo ">>> Generating waivers for $$dev ..."; \
		$(WAIVER_GEN) --device $$dev; \
	done

# Snapshots current Failed S-param (cje/cjc/ft) rows into waivers/sparam/<device>.yaml
# for the 3 HBT devices (separate from the DC waivers so `waive-all` can't clobber them).
waive-hbt-sparam:
	@for dev in $(HBT_DEVICES); do \
		echo ">>> Generating S-param waivers for $$dev ..."; \
		$(SP_WAIVER_GEN) --device $$dev; \
	done

# ------------------------
# MOS error EDA / ML clustering / report (Milestone M3)
# ------------------------
# Computes per-point sim-vs-measurement error features, clusters error patterns
# (scikit-learn KMeans/DBSCAN), flags outlier measurements (IsolationForest/IQR/
# z-score), labels clusters + proposes valid ranges (offline deterministic rule-based
# labeler by default; see models_verifier/eda/llm_labeler.py), and renders
# eda_report/<device>/report.md + figures. Fully offline/reproducible: labels are
# cached to eda_report/<device>/labels.json and reused on re-run.
eda-nmos_lv:  ; $(EDA_BIN) --device nmos_lv
eda-pmos_lv:  ; $(EDA_BIN) --device pmos_lv
eda-nmos_hv:  ; $(EDA_BIN) --device nmos_hv
eda-pmos_hv:  ; $(EDA_BIN) --device pmos_hv

eda-mos:
	@for dev in $(MOS_DEVICES); do $(MAKE) eda-$$dev; done

# ------------------------
# Help message
# ------------------------
help:
	@echo "========================================================="
	@echo " Device Testing Makefile (IHP SG13G2 PDK)"
	@echo "========================================================="
	@echo " Usage:"
	@echo "   make <target>"
	@echo
	@echo " Targets:"
	@echo "   test-all          - Run all device tests"
	@echo "   test-mos          - Run MOS device tests ($(MOS_DEVICES))"
	@echo "   test-hbt          - Run HBT device tests ($(HBT_DEVICES))"
	@echo "   test-hbt-sparam   - Run HBT S-param CjE/CjC/fT meas-vs-sim tests ($(HBT_DEVICES))"
	@echo "   test-<device>-sparam - Run S-param tests for one HBT device (e.g. make test-npn13g2-sparam)"
	@echo "   test-pnp          - Run PNP device tests ($(PNP_DEVICES))"
	@echo "   test-<device>     - Run a specific device (e.g. make test-nmos_lv)"
	@echo "   waive-all         - Snapshot current Failed rows into waivers/*.yaml (all 8 devices)"
	@echo "   waive-hbt-sparam  - Snapshot current Failed S-param rows into waivers/sparam/*.yaml (3 HBT devices)"
	@echo "   eda-mos           - MOS error EDA + ML clustering + report ($(MOS_DEVICES))"
	@echo "   eda-<device>      - EDA for a single MOS device (e.g. make eda-nmos_lv)"
	@echo
	@echo " Examples:"
	@echo "   make test-all"
	@echo "   make test-npn13g2"
	@echo "   make test-pmos_lv"
	@echo "   make waive-all"
	@echo "   make eda-mos"
