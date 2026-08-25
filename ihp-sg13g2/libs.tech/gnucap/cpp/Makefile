include ../gnucap.mk

TARGET_DIR = ../plugins/gnucap

TARGETS = \
	func_rdist \
	measure_mean \
	measure_variance \
	measure_std \
	s_dc_seed \
	s_ac_seed \
	c_sweep \
	c_reseed


PLUGINS = $(TARGETS:%=$(TARGET_DIR)/%.so)

# Default target
all: $(PLUGINS)

# Create target directory if it doesn't exist
$(TARGET_DIR):
	mkdir -p $(TARGET_DIR)

# Auto-generate convenience targets for each item in TARGETS
$(TARGETS): %: $(TARGET_DIR)/%.so

# Compile C++ source to object
$(TARGET_DIR)/%.o: %.cc | $(TARGET_DIR)
	${CXX} $(GNUCAP_CPPFLAGS) $(CPPFLAGS) -shared -fPIC ${GNUCAP_CXXFLAGS} ${CXXFLAGS} $< -o $@ -c

# Link object to shared library
$(TARGET_DIR)/%.so: $(TARGET_DIR)/%.o
	${CXX} -shared ${GNUCAP_LDFLAGS} ${LDFLAGS} $< -o $@

# Clean plugins
clean:
	rm -f $(PLUGINS)
	rm -f $(TARGETS:%=$(TARGET_DIR)/%.o)

# Help
help:
	@echo "Build Gnucap Simulator Plugins"
	@echo ""
	@echo "Targets:"
	@echo "  all       - Build all simulator plugins (default)"
	@echo "  clean     - Remove all build artifacts"
	@echo "  <plugin>  - Build specific plugin"
	@echo ""
	@echo "Plugins:"
	@for target in $(TARGETS); do echo "  $$target"; done

.PHONY: clean all $(TARGETS) help
