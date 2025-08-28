# Makefile for Device Testing (never fails on test errors)

RUNNER ?= verifier
PYTEST_ARGS := --tb=short -p no:capture

# Device configurations
NMOS_LV_CONFIG := mos/nmos_lv/sg13_lv_nmos.yaml
PMOS_LV_CONFIG := mos/pmos_lv/sg13_lv_pmos.yaml
NMOS_HV_CONFIG := mos/nmos_hv/sg13_hv_nmos.yaml
PMOS_HV_CONFIG := mos/pmos_hv/sg13_hv_pmos.yaml
PNP_MPA_CONFIG := pnp_mpa/pnpmpa.yaml
NPN13G2_CONFIG := hbt/npn13g2/npn13g2.yaml
NPN13G2L_CONFIG := hbt/npn13g2l/npn13g2l.yaml
NPN13G2V_CONFIG := hbt/npn13g2v/npn13g2v.yaml

# Groups
MOS_DEVICES := nmos_lv pmos_lv nmos_hv pmos_hv
HBT_DEVICES := npn13g2 npn13g2l npn13g2v
PNP_DEVICES := pnp_mpa
ALL_DEVICES := $(MOS_DEVICES) $(HBT_DEVICES) $(PNP_DEVICES)

.PHONY: help all test-all test-mos test-hbt test-pnp \
        nmos_lv pmos_lv nmos_hv pmos_hv pnp_mpa npn13g2 npn13g2l npn13g2v \
        pytest-all pytest-mos pytest-hbt pytest-pnp \
        verifier-all verifier-mos verifier-hbt verifier-pnp

help:
	@echo "Device Testing Makefile"
	@echo "===================================="
	@echo
	@echo "Usage: make [target] [RUNNER=pytest|verifier]"
	@echo
	@echo "Test Groups:"
	@echo "  test-all         Run all device tests"
	@echo "  test-mos         Run MOS tests (nmos_lv, pmos_lv, nmos_hv, pmos_hv)"
	@echo "  test-hbt         Run HBT tests (npn13g2, npn13g2l, npn13g2v)"
	@echo "  test-pnp         Run PNP tests (pnp_mpa)"
	@echo
	@echo "Individual Devices:"
	@echo "  nmos_lv, pmos_lv, nmos_hv, pmos_hv, pnp_mpa, npn13g2, npn13g2l, npn13g2v"
	@echo
	@echo "Runner-Specific:"
	@echo "  pytest-all / -mos / -hbt / -pnp"
	@echo "  verifier-all / -mos / -hbt / -pnp"
	@echo
	@echo "Options:"
	@echo "  RUNNER=verifier  (default) | pytest"

define run_test
	@echo "Running $(1) test with $(RUNNER)..."
	@if [ "$(RUNNER)" = "pytest" ]; then \
		python3 -m pytest tests/test_devices.py::test_devices[$(1)] $(PYTEST_ARGS) || true; \
	else \
		python3 -m models_verifier.models_verifier --config $(2) || true; \
	fi
endef

nmos_lv:
	$(call run_test,nmos_lv,$(NMOS_LV_CONFIG))
pmos_lv:
	$(call run_test,pmos_lv,$(PMOS_LV_CONFIG))
nmos_hv:
	$(call run_test,nmos_hv,$(NMOS_HV_CONFIG))
pmos_hv:
	$(call run_test,pmos_hv,$(PMOS_HV_CONFIG))
pnp_mpa:
	$(call run_test,pnp_mpa,$(PNP_MPA_CONFIG))
npn13g2:
	$(call run_test,npn13g2,$(NPN13G2_CONFIG))
npn13g2l:
	$(call run_test,npn13g2l,$(NPN13G2L_CONFIG))
npn13g2v:
	$(call run_test,npn13g2v,$(NPN13G2V_CONFIG))

test-mos:
	@if [ "$(RUNNER)" = "pytest" ]; then $(MAKE) pytest-mos; else $(MAKE) verifier-mos; fi
test-hbt:
	@if [ "$(RUNNER)" = "pytest" ]; then $(MAKE) pytest-hbt; else $(MAKE) verifier-hbt; fi
test-pnp:
	@if [ "$(RUNNER)" = "pytest" ]; then $(MAKE) pytest-pnp; else $(MAKE) verifier-pnp; fi
test-all:
	@if [ "$(RUNNER)" = "pytest" ]; then $(MAKE) pytest-all; else $(MAKE) verifier-all; fi

pytest-mos:
	@echo "Running MOS device tests with pytest..."
	@python3 -m pytest tests/test_devices.py -k "nmos_lv or pmos_lv or nmos_hv or pmos_hv" $(PYTEST_ARGS) || true
pytest-hbt:
	@echo "Running HBT device tests with pytest..."
	@python3 -m pytest tests/test_devices.py -k "npn13g2 or npn13g2l or npn13g2v" $(PYTEST_ARGS) || true
pytest-pnp:
	@echo "Running PNP device tests with pytest..."
	@python3 -m pytest tests/test_devices.py -k "pnp_mpa" $(PYTEST_ARGS) || true
pytest-all:
	@echo "Running all device tests with pytest..."
	@python3 -m pytest tests/test_devices.py $(PYTEST_ARGS) || true

verifier-mos:
	@echo "Running MOS device tests with models_verifier..."
	@for device in $(MOS_DEVICES); do \
		echo "=== Testing $$device ==="; \
		case $$device in \
			nmos_lv) config=$(NMOS_LV_CONFIG) ;; \
			pmos_lv) config=$(PMOS_LV_CONFIG) ;; \
			nmos_hv) config=$(NMOS_HV_CONFIG) ;; \
			pmos_hv) config=$(PMOS_HV_CONFIG) ;; \
		esac; \
		python3 -m models_verifier.models_verifier --config $$config || echo "FAILED: $$device"; \
	done; true

verifier-hbt:
	@echo "Running HBT device tests with models_verifier..."
	@for device in $(HBT_DEVICES); do \
		echo "=== Testing $$device ==="; \
		case $$device in \
			npn13g2)  config=$(NPN13G2_CONFIG)  ;; \
			npn13g2l) config=$(NPN13G2L_CONFIG) ;; \
			npn13g2v) config=$(NPN13G2V_CONFIG) ;; \
		esac; \
		python3 -m models_verifier.models_verifier --config $$config || echo "FAILED: $$device"; \
	done; true

verifier-pnp:
	@echo "Running PNP device tests with models_verifier..."
	@python3 -m models_verifier.models_verifier --config $(PNP_MPA_CONFIG) || echo "FAILED: pnp_mpa"; true

verifier-all:
	@echo "Running all device tests with models_verifier..."
	@$(MAKE) verifier-mos || true; \
	$(MAKE) verifier-hbt || true; \
	$(MAKE) verifier-pnp || true; \
	true

all: test-all
mos: test-mos
hbt: test-hbt
pnp: test-pnp
