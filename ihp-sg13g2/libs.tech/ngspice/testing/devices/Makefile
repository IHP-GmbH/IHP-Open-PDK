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
# Usage (from this folder, Python environment active):
#   make help
#   make test-nmos_lv                          one case on the default toolchain
#   make test-all TOOLCHAIN=ng46-ovr-fdf2522   every case on another toolchain
#   make unit-tests
# =========================================================

SHELL := /bin/bash
PYTHON ?= python3

# ------------------------
# Toolchain (tools/toolchain.py, pinned in toolchain.lock)
# ------------------------
# TOOLCHAIN = ng<ngspice version>-ovr-<OpenVAF-Reloaded commit>. It selects the ngspice binary
# and the PSP103 model compiled with that OpenVAF build; every run writes its results to
# $(RESULTS_ROOT)/<case>/ and records the toolchain in toolchain.txt there.
# `$(PYTHON) tools/toolchain.py list` shows which toolchains are installed.
TOOLCHAIN    ?= ng47-ovr-b4517ad
RESULTS_ROOT ?= models_results/$(TOOLCHAIN)
TOOLCHAIN_PY  = $(PYTHON) tools/toolchain.py
NGSPICE_BIN  := $(shell $(TOOLCHAIN_PY) path ngspice $(TOOLCHAIN))
OSDI_DIR     := $(shell $(TOOLCHAIN_PY) path osdi-dir $(TOOLCHAIN))
export TOOLCHAIN RESULTS_ROOT NGSPICE_BIN OSDI_DIR
export PYTHONPATH := $(CURDIR)

VERIFIER_BIN    = $(PYTHON) -m models_verifier.models_verifier
SP_VERIFIER_BIN = $(PYTHON) -m models_verifier.sp_runner.verifier
CV_VERIFIER_BIN = $(PYTHON) -m models_verifier.cv_runner.verifier
WAIVER_GEN      = $(PYTHON) -m models_verifier.waivers.generate
EDA_BIN         = $(PYTHON) -m models_verifier.eda.run
PLOT_BIN        = $(PYTHON) validation/plot_verification_results.py

# ------------------------
# Cases: one config per case. A config's output_dir is models_results/<case>.
# ------------------------
CONFIG_nmos_lv  = configs/mos/nmos_lv/sg13_lv_nmos.yaml
CONFIG_pmos_lv  = configs/mos/pmos_lv/sg13_lv_pmos.yaml
CONFIG_nmos_hv  = configs/mos/nmos_hv/sg13_hv_nmos.yaml
CONFIG_pmos_hv  = configs/mos/pmos_hv/sg13_hv_pmos.yaml
CONFIG_pnp_mpa  = configs/pnp_mpa/pnpmpa.yaml
CONFIG_npn13g2  = configs/hbt/npn13g2/npn13g2.yaml
CONFIG_npn13g2l = configs/hbt/npn13g2l/npn13g2l.yaml
CONFIG_npn13g2v = configs/hbt/npn13g2v/npn13g2v.yaml

# HBT test structures other than each device's main (MQA) one: configs/hbt/variants/<case>.yaml.
HBT_VARIANTS = npn13g2_T00 npn13g2_T01 npn13g2_T02 \
               npn13g2l_T00 npn13g2l_T02 npn13g2l_T03 npn13g2l_T04 \
               npn13g2v_T00 npn13g2v_T02 npn13g2v_T03 npn13g2v_T04
$(foreach v,$(HBT_VARIANTS),$(eval CONFIG_$(v) = configs/hbt/variants/$(v).yaml))

MOS_DEVICES  = nmos_lv pmos_lv nmos_hv pmos_hv
HBT_DEVICES  = npn13g2 npn13g2l npn13g2v
PNP_DEVICES  = pnp_mpa
ALL_DEVICES  = $(MOS_DEVICES) $(HBT_DEVICES) $(PNP_DEVICES)
HBT_CASES    = $(HBT_DEVICES) $(HBT_VARIANTS)
CV_CASES     = $(MOS_DEVICES) $(PNP_DEVICES)        # cases with a C-V tier (cv_setups in the config)

# The config of a case, or a clear error for an unknown case.
config_of = $(or $(CONFIG_$(1)),$(error unknown case '$(1)'; see `make help`))

# Runs every target of a list even when one fails, then exits 1 if any failed. Recipes that use
# it start with "+" so that `make -n` also shows the recursive calls.
run_all = rc=0; for t in $(1); do $(MAKE) --no-print-directory $$t || rc=1; done; exit $$rc

all: test-all

# ------------------------
# Toolchain checks and the PSP103 model
# ------------------------
# Stop early when the selected toolchain is not installed.
check-toolchain:
	@test -x "$(NGSPICE_BIN)" || { echo "ngspice of $(TOOLCHAIN) is not installed ($(NGSPICE_BIN)); see: $(TOOLCHAIN_PY) list"; exit 1; }

# Compile PSP103 with the toolchain's OpenVAF build into $(OSDI_DIR) (only when missing or out of date).
osdi: check-toolchain
	@$(TOOLCHAIN_PY) osdi $(TOOLCHAIN)

# The MOS cases need the compiled model.
$(addprefix test-,$(MOS_DEVICES)) $(addsuffix -cv,$(addprefix test-,$(MOS_DEVICES))): osdi

# ------------------------
# Tests: DC (all devices) and HBT S-parameters (CjE, CjC, fT)
# ------------------------
# The S-parameter test extracts CjE/CjC/fT from the de-embedded S-parameters of the spar_*
# files, runs an ngspice AC 2-port extraction at the same biases and range-checks them
# within the MQA windows; results go to $(RESULTS_ROOT)/<case>/sparam/.
# C-V tier: capacitance-meter measurements (MOS junction / gate / oxide, pnpMPA CBC / CBE),
# one AC analysis per bias point; results go to $(RESULTS_ROOT)/<case>/cv/.
test-%-cv: check-toolchain
	@echo ">>> [$*] C-V verification on $(TOOLCHAIN) -> $(RESULTS_ROOT)/$*/cv"
	@$(CV_VERIFIER_BIN) --config $(call config_of,$*)

test-%-sparam: check-toolchain
	@echo ">>> [$*] S-parameter verification on $(TOOLCHAIN) -> $(RESULTS_ROOT)/$*/sparam"
	@$(SP_VERIFIER_BIN) --config $(call config_of,$*)

test-%: check-toolchain
	@echo ">>> [$*] verification on $(TOOLCHAIN) -> $(RESULTS_ROOT)/$*"
	@$(VERIFIER_BIN) --config $(call config_of,$*)

test-mos:        ; +@$(call run_all,$(addprefix test-,$(MOS_DEVICES)))
test-hbt:        ; +@$(call run_all,$(addprefix test-,$(HBT_DEVICES)))
test-pnp:        ; +@$(call run_all,$(addprefix test-,$(PNP_DEVICES)))
test-hbt-sparam: ; +@$(call run_all,$(addsuffix -sparam,$(addprefix test-,$(HBT_DEVICES))))
test-hbt-variants:        ; +@$(call run_all,$(addprefix test-,$(HBT_VARIANTS)))
test-hbt-variants-sparam: ; +@$(call run_all,$(addsuffix -sparam,$(addprefix test-,$(HBT_VARIANTS))))
test-cv:                  ; +@$(call run_all,$(addsuffix -cv,$(addprefix test-,$(CV_CASES))))
test-all: ; +@$(call run_all,test-mos test-hbt test-pnp test-hbt-sparam test-hbt-variants test-hbt-variants-sparam test-cv)

# HBT measurement check (no simulation): IC-CAP's de-embedded S of every spar_* file recomputed
# from its raw S and the folder's OPEN/SHORT dummies, plus copied S_deemb between files.
check-deembedding:
	@$(PYTHON) tools/check_hbt_deembedding.py --out $(RESULTS_ROOT)/hbt_deembedding_check.md

unit-tests:
	@$(PYTHON) -m pytest -q -p no:cacheprovider models_verifier/tests

# ------------------------
# Exceptions ("waivers", schema 2, see models_verifier/waivers/waiver.py)
# ------------------------
# Writes the "Failed (new)" rows of the LAST finished run of a case (same TOOLCHAIN) into its
# exception file (waivers/<device_name>.yaml, S-parameters: waivers/sparam/). Existing entries
# and other toolchains are kept. Review the new entries before committing them.
# WAIVE_REASON is written into new entries.
WAIVE_REASON ?= auto-waived from a run, pending review

waive-%-sparam:
	@$(WAIVER_GEN) --config $(call config_of,$*) --tier sparam --reason "$(WAIVE_REASON)"

waive-%-cv:
	@$(WAIVER_GEN) --config $(call config_of,$*) --tier cv --reason "$(WAIVE_REASON)"

waive-%:
	@$(WAIVER_GEN) --config $(call config_of,$*) --tier dc --reason "$(WAIVE_REASON)"

waive-all:        ; +@$(call run_all,$(addprefix waive-,$(ALL_DEVICES) $(HBT_VARIANTS)))
waive-hbt-sparam: ; +@$(call run_all,$(addsuffix -sparam,$(addprefix waive-,$(HBT_CASES))))
waive-cv:         ; +@$(call run_all,$(addsuffix -cv,$(addprefix waive-,$(CV_CASES))))

# ------------------------
# MOS error EDA / ML clustering / report (not a gate)
# ------------------------
# Computes per-point sim-vs-measurement error features, clusters error patterns
# (scikit-learn KMeans/DBSCAN), flags outlier measurements (IsolationForest/IQR/
# z-score), labels clusters + proposes valid ranges (offline deterministic rule-based
# labeler by default; see models_verifier/eda/llm_labeler.py), and renders
# eda_report/<device>/report.md + figures from $(RESULTS_ROOT)/<device>/combined_results.
eda-%: ; @$(EDA_BIN) --device $*
eda-mos: ; +@$(call run_all,$(addprefix eda-,$(MOS_DEVICES)))

# ------------------------
# Figures: measured vs simulated plots (validation/plot_verification_results.py)
# ------------------------
# One PNG per measured block and output variable, drawn from $(RESULTS_ROOT)/<case>/ (run
# `make test-<case>` first; the S-parameter and C-V results go to <case>/sparam and <case>/cv).
# Each figure shows the acceptance band and the judged points as the check used them, and sits in
# the folder of its status (passed, failed_new, failed_waived, ...). Figures go to
# $(FIG_DIR)/<case>/ (not in git); override with `make plot-all FIG_DIR=<dir>`.
FIG_DIR ?= figures/$(TOOLCHAIN)

plot-%:
	@echo ">>> Plotting $*: $(RESULTS_ROOT)/$* -> $(FIG_DIR)/$* ..."
	@$(if $(strip $(FIG_DIR)),rm -rf $(FIG_DIR)/$*)   # figures of an earlier run would stay in their old status folders
	@$(PLOT_BIN) --results $(RESULTS_ROOT)/$* --out $(FIG_DIR)/$*

plot-mos: ; +@$(call run_all,$(addprefix plot-,$(MOS_DEVICES)))
plot-hbt: ; +@$(call run_all,$(addprefix plot-,$(HBT_CASES)))
plot-pnp: ; +@$(call run_all,$(addprefix plot-,$(PNP_DEVICES)))
plot-all: ; +@$(call run_all,plot-mos plot-hbt plot-pnp)

# ------------------------
# Help message
# ------------------------
help:
	@echo "========================================================="
	@echo " Device Testing Makefile (IHP SG13G2 PDK)"
	@echo "========================================================="
	@echo " Toolchain: TOOLCHAIN=$(TOOLCHAIN) (ngspice $(NGSPICE_BIN), OSDI $(OSDI_DIR))"
	@echo "   pinned toolchains: $(TOOLCHAIN_PY) list ; results in $(RESULTS_ROOT)/<case>/"
	@echo
	@echo " Targets:"
	@echo "   test-<case>          - Verify one case: $(ALL_DEVICES)"
	@echo "                          HBT test structures: $(HBT_VARIANTS)"
	@echo "   test-<hbt case>-sparam - HBT S-parameter CjE/CjC/fT check (devices and test structures)"
	@echo "   test-mos | test-hbt | test-pnp | test-hbt-sparam | test-hbt-variants[-sparam] | test-all"
	@echo "                          - groups (all run; exit 1 if any failed)"
	@echo "   test-<case>-cv       - C-V (capacitance) check: $(CV_CASES); test-cv for all"
	@echo "   check-deembedding    - HBT S-parameter de-embedding check (no simulation)"
	@echo "   unit-tests           - Framework unit tests"
	@echo "   osdi                 - Compile PSP103 with the toolchain's OpenVAF (done by the MOS tests)"
	@echo "   waive-<case>         - Write the new failures of the last run into waivers/<device_name>.yaml"
	@echo "                          (HBT test structures: waivers/variants/<case>/)"
	@echo "   waive-<hbt>-sparam   - The same for an S-parameter run -> waivers/sparam/"
	@echo "   waive-<case>-cv      - The same for a C-V run -> waivers/cv/"
	@echo "   waive-all | waive-hbt-sparam | waive-cv - The same for every case"
	@echo "   eda-<mos case> | eda-mos - MOS error EDA report (not a gate)"
	@echo "   plot-<case> | plot-mos | plot-hbt | plot-pnp | plot-all - Figures into $(FIG_DIR)/<case>/"
	@echo
	@echo " Exit code: 1 for new failures, simulation errors, or exceptions whose curve is missing from"
	@echo " the run; waived failures are still reported as failures."

.PHONY: all check-toolchain osdi test-mos test-hbt test-pnp test-hbt-sparam test-hbt-variants \
        test-hbt-variants-sparam test-cv test-all check-deembedding unit-tests waive-cv \
        waive-all waive-hbt-sparam eda-mos plot-mos plot-hbt plot-pnp plot-all help
