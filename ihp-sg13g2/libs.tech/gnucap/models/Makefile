include ../gnucap.mk

MODELGEN_VERILOG = gnucap-mg-vams
OPENVAF = openvaf-r
IHP_VERILOG_DIR = ../../verilog-a
MGFLAGS = -I $(shell gnucap-conf --includedir) -I . -I $(IHP_VERILOG_DIR)/r3_cmc -I $(IHP_VERILOG_DIR)/psp103 -I $(IHP_VERILOG_DIR)/cap_cmomi -I $(IHP_VERILOG_DIR)/cap_cmomf

TARGET_DIR = ../plugins/models
OSDI_DIR = ../plugins/osdi

TARGETS = \
	idc \
	resistor_paramset \
	capacitor_paramset \
	sg13g2_moslv_paramset \
	sg13g2_moslv_rf_paramset \
	sg13g2_moshv_paramset \
	sg13g2_moshv_rf_paramset \

PLUGINS = $(TARGETS:%=$(TARGET_DIR)/%.so)

# Default target
all: $(PLUGINS)

# Create target directories if they don't exist
$(TARGET_DIR):
	mkdir -p $(TARGET_DIR)

$(OSDI_DIR):
	mkdir -p $(OSDI_DIR)

# Auto-generate convenience targets for each item in TARGETS
$(TARGETS): %: $(TARGET_DIR)/%.so
# Auto-generate convenience targets to dump each item in TARGETS
$(TARGETS:%=dump-%): dump-%: %.dump.va
# Auto-generate convenience targets to build OSDI for each item in TARGETS
$(TARGETS:%=osdi-%): osdi-%: $(OSDI_DIR)/%.osdi

# Sources reached through `include, listed by hand because gnucap-mg-vams has no
# dependency-output mode. Without them make compares only the paramset file
# itself, so editing r3_cmc.va, psp103.va, either cap_cmom*.va or discipline.h
# leaves a stale .so in place and `make check` then validates the previous
# build instead of the current one. The external model trees are taken wholesale: any of their
# .include files feeds the compile, and they are third-party sources that change
# rarely enough that over-triggering costs nothing.
va_sources  = $(wildcard $(1)/*.va $(1)/*.vams $(1)/*.include $(1)/*.h)
R3CMC_SRC  := $(call va_sources,$(IHP_VERILOG_DIR)/r3_cmc)
PSP103_SRC := $(call va_sources,$(IHP_VERILOG_DIR)/psp103)
CMOMI_SRC  := $(call va_sources,$(IHP_VERILOG_DIR)/cap_cmomi)
CMOMF_SRC  := $(call va_sources,$(IHP_VERILOG_DIR)/cap_cmomf)

$(TARGET_DIR)/resistor_paramset.cc:        resistor.va discipline.h $(R3CMC_SRC)
$(TARGET_DIR)/capacitor_paramset.cc:       capacitor.va $(CMOMI_SRC) $(CMOMF_SRC)
$(TARGET_DIR)/sg13g2_moslv_paramset.cc:    discipline.h $(PSP103_SRC)
$(TARGET_DIR)/sg13g2_moslv_rf_paramset.cc: discipline.h $(PSP103_SRC)
$(TARGET_DIR)/sg13g2_moshv_paramset.cc:    discipline.h $(PSP103_SRC)
$(TARGET_DIR)/sg13g2_moshv_rf_paramset.cc: discipline.h $(PSP103_SRC)

resistor_paramset.dump.va:        resistor.va discipline.h $(R3CMC_SRC)
capacitor_paramset.dump.va:       capacitor.va $(CMOMI_SRC) $(CMOMF_SRC)
sg13g2_moslv_paramset.dump.va:    discipline.h $(PSP103_SRC)
sg13g2_moslv_rf_paramset.dump.va: discipline.h $(PSP103_SRC)
sg13g2_moshv_paramset.dump.va:    discipline.h $(PSP103_SRC)
sg13g2_moshv_rf_paramset.dump.va: discipline.h $(PSP103_SRC)

# Naming the generated C++ as explicit targets above would make it permanent:
# GNU make only treats a file as intermediate, and deletes it after the build,
# when it is never mentioned as a target or prerequisite. These are hundreds of
# MB, so keep them intermediate; the dependencies above still decide when the
# chain has to be rebuilt.
.INTERMEDIATE: $(TARGETS:%=$(TARGET_DIR)/%.cc)

# Generate C++ from Verilog-A
$(TARGET_DIR)/%.cc: %.va | $(TARGET_DIR)
	${MODELGEN_VERILOG} ${MGFLAGS} -o $@ --cc $<

# Generate C++ from Verilog-AMS
$(TARGET_DIR)/%.cc: %.vams | $(TARGET_DIR)
	${MODELGEN_VERILOG} ${MGFLAGS} -o $@ --cc $<

# Compile generated C++ to object
$(TARGET_DIR)/%.o: $(TARGET_DIR)/%.cc
	${CXX} $(GNUCAP_CPPFLAGS) $(CPPFLAGS) -shared -fPIC ${GNUCAP_CXXFLAGS} ${CXXFLAGS} $< -o $@ -c

# Link object to shared library
$(TARGET_DIR)/%.so: $(TARGET_DIR)/%.o
	${CXX} -shared ${GNUCAP_LDFLAGS} ${LDFLAGS} $< -o $@

# Dump paramset as VA module
%.dump.va: %.va
	${MODELGEN_VERILOG} ${MGFLAGS} -o $@ --dump $<

# Generate OSDI from dumped paramset Verilog-A module
# (into OSDI_DIR, which is where clean looks for it)
$(OSDI_DIR)/%.osdi: %.dump.va | $(OSDI_DIR)
	${OPENVAF} $< -o $@

# Clean plugins
clean:
	rm -f $(PLUGINS)
	rm -f $(TARGETS:%=$(TARGET_DIR)/%.cc)
	rm -f $(TARGETS:%=$(TARGET_DIR)/%.o)
	rm -f $(TARGETS:%=$(OSDI_DIR)/%.osdi)
	rm -f $(TARGETS:%=%.dump.va)

# Help
help:
	@echo "Build Verilog-AMS Model Plugins"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build all Verilog-AMS model plugins (default)"
	@echo "  clean        - Remove all build artifacts"
	@echo "  <model>      - Build specific model plugin"
	@echo "  dump-<model> - Dump model as Verilog-A module"
	@echo "  osdi-<model> - Build OSDI plugin from dumped paramset"
	@echo ""
	@echo "Models:"
	@for target in $(TARGETS); do echo "  $$target"; done

.PHONY: clean all $(TARGETS) $(TARGETS:%=dump-%) $(TARGETS:%=osdi-%) help
