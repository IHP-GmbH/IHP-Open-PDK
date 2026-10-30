# ihp-sg13g2/libs.tech/gnucap/Makefile

include gnucap.mk

BUNDLE = plugins/sg13g2.so

# Build everything
all: models-plugins gnucap-plugins

# Build model plugins and link the model and paramset bundle.
models-plugins:
	@$(MAKE) -C models
	# Modelgen embeds the same runtime helpers in each object; use
    # allow-multiple-definition to keep only once
	$(CXX) -shared -Wl,--allow-multiple-definition $(GNUCAP_LDFLAGS) $(LDFLAGS) plugins/models/*.o -o $(BUNDLE)

# Build gnucap plugins
gnucap-plugins:
	@$(MAKE) -C cpp

# Run all tests, after building what they load.
#
# The prerequisites used to read `models plugins`. Neither has a rule with a
# recipe, and they resolved only because .PHONY declared them, which makes them
# silent no-ops: check ran the suite without building anything, even though the
# README describes it as building the required plugins first.
check: all
	@$(MAKE) -C tests

# Clean everything
clean-plugin-dir = rm -f $(1)/*.cc $(1)/*.o $(1)/*.so

clean:
	@$(MAKE) -C models clean
	@$(MAKE) -C cpp clean
	@$(MAKE) -C tests clean
	# Remove leftover outdated artifacts (better safe than sorry)
	$(call clean-plugin-dir,plugins/models)
	$(call clean-plugin-dir,plugins/gnucap)
	$(call clean-plugin-dir,plugins/util)
	rm -f $(BUNDLE) plugins/*.so plugins/osdi/*.osdi

# Help
help:
	@echo "Build Gnucap Verilog-AMS Model and Simulator Plugins"
	@echo ""
	@echo "Targets:"
	@echo "  all             - Build all plugins"
	@echo "  models-plugins  - Build model plugins and bundle"
	@echo "  gnucap-plugins  - Build Gnucap simulator plugins only"
	@echo "  check           - Build the plugins, then run the test suite"
	@echo "  clean           - Remove all build artifacts"

.PHONY: all models-plugins gnucap-plugins check clean help
