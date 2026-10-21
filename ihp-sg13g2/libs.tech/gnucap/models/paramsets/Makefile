include ../../gnucap.mk

MODELGEN_VERILOG = gnucap-mg-vams
OPENVAF = openvaf-r
IHP_VERILOG_DIR = ../../../verilog-a

MGFLAGS = -I $(shell gnucap-conf --includedir) -I . -I ..

TARGET_DIR = ../../plugins/models
OSDI_DIR = ../../plugins/osdi

TARGETS = \
	resistor \
	capacitor \
	sg13g2_moscap \
	sg13g2_svaricaphv \
	sg13g2_moslv \
	sg13g2_moslv_rf \
	sg13g2_moshv \
	sg13g2_moshv_rf \
	sg13g2_hbt

PLUGINS = $(TARGETS:%=$(TARGET_DIR)/%_paramset.so)

SOURCES = $(TARGETS:%=%.va)

# Compact models required by each family.
MODELS_resistor = r3_cmc
MODELS_capacitor = cap_cmomi cap_cmomf
MODELS_sg13g2_moscap = psp103
MODELS_sg13g2_svaricaphv = mosvar
MODELS_sg13g2_moslv = psp103
MODELS_sg13g2_moslv_rf = psp103
MODELS_sg13g2_moshv = psp103
MODELS_sg13g2_moshv_rf = psp103
MODELS_sg13g2_hbt = vbic_1p3

# Default target
all: $(PLUGINS)

# Create target directories if they don't exist
$(TARGET_DIR):
	mkdir -p $(TARGET_DIR)

$(OSDI_DIR):
	mkdir -p $(OSDI_DIR)

# Auto-generate convenience targets for each item in TARGETS
$(TARGETS): %: $(TARGET_DIR)/%_paramset.so
# Auto-generate convenience targets to dump each item in TARGETS
$(TARGETS:%=dump-%): dump-%: %_paramset.dump.va
# Auto-generate convenience targets to build OSDI for each item in TARGETS
$(TARGETS:%=osdi-%): osdi-%: $(OSDI_DIR)/%_paramset.osdi

# Apply family-specific include paths to both code generation and VA dumps.
define PARAMSET_FLAGS
$(TARGET_DIR)/$(1)_paramset.cc $(1)_paramset.dump.va: \
	MGFLAGS += $(addprefix -I $(IHP_VERILOG_DIR)/,$(MODELS_$(1)))
endef
$(foreach target,$(TARGETS),$(eval $(call PARAMSET_FLAGS,$(target))))

# Declare the entry source first so $< remains the build entry source when the
# included-source prerequisites below are added to these targets.
$(TARGETS:%=$(TARGET_DIR)/%_paramset.cc): $(TARGET_DIR)/%_paramset.cc: %.va | $(TARGET_DIR)
	$(MODELGEN_VERILOG) $(MGFLAGS) -o $@ --cc $<

$(TARGETS:%=%_paramset.dump.va): %_paramset.dump.va: %.va
	$(MODELGEN_VERILOG) $(MGFLAGS) -o $@ --dump $<

# Sources reached through `include, listed by hand because gnucap-mg-vams has no
# dependency-output mode. Without them make compares only the paramset file
# itself, so editing r3_cmc.va, psp103.va, either cap_cmom*.va or discipline.h
# leaves a stale .so in place and `make check` then validates the previous
# build instead of the current one. The external model trees are taken wholesale: any of their
# .include files feeds the compile, and they are third-party sources that change
# rarely enough that over-triggering costs nothing.

# TODO: generate dynamically from the MODELS_<target> mappings
va_sources  = $(wildcard $(1)/*.va $(1)/*.vams $(1)/*.include $(1)/*.h)
R3CMC_SRC  := $(call va_sources,$(IHP_VERILOG_DIR)/r3_cmc)
PSP103_SRC := $(call va_sources,$(IHP_VERILOG_DIR)/psp103)
CMOMI_SRC  := $(call va_sources,$(IHP_VERILOG_DIR)/cap_cmomi)
CMOMF_SRC  := $(call va_sources,$(IHP_VERILOG_DIR)/cap_cmomf)
VBIC_SRC   := $(call va_sources,$(IHP_VERILOG_DIR)/vbic_1p3)
MOSVAR_SRC := $(call va_sources,$(IHP_VERILOG_DIR)/mosvar)

RES_PARAMSETS = $(wildcard resistor_*.va)
CAPACITOR_PARAMSETS = $(wildcard capacitor_*.va)
HBT_PARAMSETS = $(wildcard sg13g2_hbt_*.va)
MOSCAP_PARAMSETS = $(wildcard sg13g2_moscap_*.va)
# RF umbrellas share the device-file prefix but are separate build entry sources.
MOSLV_PARAMSETS = $(filter-out $(SOURCES),$(wildcard sg13g2_moslv_*.va))
MOSHV_PARAMSETS = $(filter-out $(SOURCES),$(wildcard sg13g2_moshv_*.va))

$(TARGET_DIR)/resistor_paramset.cc:          ../spice/sp_resistor.va ../discipline.h $(R3CMC_SRC) $(RES_PARAMSETS)
$(TARGET_DIR)/capacitor_paramset.cc:         ../spice/sp_capacitor.va $(CMOMI_SRC) $(CMOMF_SRC) $(CAPACITOR_PARAMSETS)
$(TARGET_DIR)/sg13g2_svaricaphv_paramset.cc: ../spice/sp_capacitor.va $(MOSVAR_SRC)
$(TARGET_DIR)/sg13g2_moscap_paramset.cc:     ../discipline.h $(MOSCAP_PARAMSETS) $(PSP103_SRC)
$(TARGET_DIR)/sg13g2_moslv_paramset.cc:      ../discipline.h $(PSP103_SRC) $(MOSLV_PARAMSETS)
$(TARGET_DIR)/sg13g2_moslv_rf_paramset.cc:   ../discipline.h $(PSP103_SRC) $(MOSLV_PARAMSETS)
$(TARGET_DIR)/sg13g2_moshv_paramset.cc:      ../discipline.h $(PSP103_SRC) $(MOSHV_PARAMSETS)
$(TARGET_DIR)/sg13g2_moshv_rf_paramset.cc:   ../discipline.h $(PSP103_SRC) $(MOSHV_PARAMSETS)
$(TARGET_DIR)/sg13g2_hbt_paramset.cc:        $(HBT_PARAMSETS) $(VBIC_SRC)

resistor_paramset.dump.va:          ../spice/sp_resistor.va ../discipline.h $(R3CMC_SRC) $(RES_PARAMSETS)
capacitor_paramset.dump.va:         ../spice/sp_capacitor.va $(CMOMI_SRC) $(CMOMF_SRC) $(CAPACITOR_PARAMSETS)
sg13g2_moscap_paramset.dump.va:     ../discipline.h $(MOSCAP_PARAMSETS) $(PSP103_SRC)
sg13g2_svaricaphv_paramset.dump.va: ../spice/sp_capacitor.va $(MOSVAR_SRC)
sg13g2_moslv_paramset.dump.va:      ../discipline.h $(PSP103_SRC) $(MOSLV_PARAMSETS)
sg13g2_moslv_rf_paramset.dump.va:   ../discipline.h $(PSP103_SRC) $(MOSLV_PARAMSETS)
sg13g2_moshv_paramset.dump.va:      ../discipline.h $(PSP103_SRC) $(MOSHV_PARAMSETS)
sg13g2_moshv_rf_paramset.dump.va:   ../discipline.h $(PSP103_SRC) $(MOSHV_PARAMSETS)
sg13g2_hbt_paramset.dump.va:        $(HBT_PARAMSETS) $(VBIC_SRC)

# Naming the generated C++ as explicit targets above would make it permanent:
# GNU make only treats a file as intermediate, and deletes it after the build,
# when it is never mentioned as a target or prerequisite. These are hundreds of
# MB, so keep them intermediate; the dependencies above still decide when the
# chain has to be rebuilt.
.INTERMEDIATE: $(TARGETS:%=$(TARGET_DIR)/%_paramset.cc)

# Compile generated C++ to object
$(TARGET_DIR)/%.o: $(TARGET_DIR)/%.cc
	${CXX} $(GNUCAP_CPPFLAGS) $(CPPFLAGS) -c -fPIC ${GNUCAP_CXXFLAGS} ${CXXFLAGS} $< -o $@

# Link object to shared library
$(TARGET_DIR)/%.so: $(TARGET_DIR)/%.o
	${CXX} -shared ${GNUCAP_LDFLAGS} ${LDFLAGS} $< -o $@

# Generate OSDI from dumped paramset Verilog-A module
# (into OSDI_DIR, which is where clean looks for it)
$(OSDI_DIR)/%.osdi: %.dump.va | $(OSDI_DIR)
	${OPENVAF} $< -o $@

# Clean plugins
clean:
	rm -f $(PLUGINS)
	rm -f $(TARGETS:%=$(TARGET_DIR)/%_paramset.cc)
	rm -f $(TARGETS:%=$(TARGET_DIR)/%_paramset.o)
	rm -f $(TARGETS:%=$(OSDI_DIR)/%_paramset.osdi)
	rm -f $(TARGETS:%=%_paramset.dump.va)

# Help
help:
	@echo "Build Verilog-AMS Paramset Plugins"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build all Verilog-AMS paramset plugins (default)"
	@echo "  clean        - Remove all build artifacts"
	@echo "  <model>      - Build specific model plugin"
	@echo "  dump-<model> - Dump model as Verilog-A module"
	@echo "  osdi-<model> - Build OSDI plugin from dumped paramset"
	@echo ""
	@echo "Models:"
	@for target in $(TARGETS); do echo "  $$target"; done

.PHONY: clean all $(TARGETS) $(TARGETS:%=dump-%) $(TARGETS:%=osdi-%) help
