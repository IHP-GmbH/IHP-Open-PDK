include ../gnucap.mk

MODELGEN_VERILOG = gnucap-mg-vams
OPENVAF = openvaf-r

MGFLAGS = -I $(shell gnucap-conf --includedir) -I .

TARGET_DIR = ../plugins/models
OSDI_DIR = ../plugins/osdi

MODULE_TARGETS = \
	capacitors_mod \
	diodes_mod \
	sg13g2_dschottky_nbl1_mod \
	sg13g2_esd \
	sg13g2_hbt_mod \
	sg13g2_moscap_mod \
	sg13g2_moshv_mod \
	sg13g2_moslv_mod \
	sg13g2_svaricaphv_mod

TARGETS = $(MODULE_TARGETS)

PLUGINS = $(TARGETS:%=$(TARGET_DIR)/%.so)

# Default target
all: $(PLUGINS) paramsets util

# Build paramset plugins in their own directory.
paramsets:
	@$(MAKE) -C paramsets

util:
	@$(MAKE) -C util

# Create target directories if they don't exist
$(TARGET_DIR):
	mkdir -p $(TARGET_DIR)

$(OSDI_DIR):
	mkdir -p $(OSDI_DIR)

# Auto-generate convenience targets for each item in TARGETS
$(TARGETS): %: $(TARGET_DIR)/%.so

# Generate C++ from Verilog-A
$(TARGET_DIR)/%.cc: %.va | $(TARGET_DIR)
	${MODELGEN_VERILOG} ${MGFLAGS} -o $@ --cc $<

# Generate C++ from Verilog-AMS
$(TARGET_DIR)/%.cc: %.vams | $(TARGET_DIR)
	${MODELGEN_VERILOG} ${MGFLAGS} -o $@ --cc $<

# Compile generated C++ to object
$(TARGET_DIR)/%.o: $(TARGET_DIR)/%.cc
	${CXX} $(GNUCAP_CPPFLAGS) $(CPPFLAGS) -c -fPIC ${GNUCAP_CXXFLAGS} ${CXXFLAGS} $< -o $@

# Link object to shared library
$(TARGET_DIR)/%.so: $(TARGET_DIR)/%.o
	${CXX} -shared ${GNUCAP_LDFLAGS} ${LDFLAGS} $< -o $@

# Dump model as VA module
%.dump.va: %.va
	${MODELGEN_VERILOG} ${MGFLAGS} -o $@ --dump $<

# Generate OSDI from dumped Verilog-A module
$(OSDI_DIR)/%.osdi: %.dump.va | $(OSDI_DIR)
	${OPENVAF} $< -o $@

# Clean plugins
clean:
	rm -f $(PLUGINS)
	rm -f $(TARGETS:%=$(TARGET_DIR)/%.cc)
	rm -f $(TARGETS:%=$(TARGET_DIR)/%.o)
	@$(MAKE) -C paramsets clean
	@$(MAKE) -C util clean

# Help
help:
	@echo "Build Verilog-AMS Model Plugins"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build model, paramset, and utility plugins (default)"
	@echo "  paramsets    - Build paramset plugins"
	@echo "  util         - Build utility plugins"
	@echo "  clean        - Remove all model and paramset build artifacts"
	@echo "  <model>      - Build specific model plugin"
	@echo ""
	@echo "Models:"
	@for target in $(TARGETS); do echo "  $$target"; done
	@echo ""
	@echo "Build specific paramsets with make -C paramsets <target>."

.PHONY: clean all paramsets util $(TARGETS) help
