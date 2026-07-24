include ../gnucap.mk

MODELGEN_VERILOG = gnucap-mg-vams
OPENVAF = openvaf-r
IHP_VERILOG_DIR = ../../verilog-a
MGFLAGS = -I $(shell gnucap-conf --includedir) -I . -I $(IHP_VERILOG_DIR)/r3_cmc -I $(IHP_VERILOG_DIR)/psp103 -I $(IHP_VERILOG_DIR)/cap_cmom

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

# Create target directory if it doesn't exist
$(TARGET_DIR):
	mkdir -p $(TARGET_DIR)

# Auto-generate convenience targets for each item in TARGETS
$(TARGETS): %: $(TARGET_DIR)/%.so
# Auto-generate convenience targets to dump each item in TARGETS
$(TARGETS:%=dump-%): dump-%: %.dump.va
# Auto-generate convenience targets to build OSDI for each item in TARGETS
$(TARGETS:%=osdi-%): osdi-%: $(TARGET_DIR)/%.osdi

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
$(TARGET_DIR)/%.osdi: %.dump.va
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
