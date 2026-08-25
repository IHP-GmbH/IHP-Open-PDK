# ihp-sg13g2/libs.tech/gnucap/Makefile

# Build everything
all: models-plugins gnucap-plugins

# Build Verilog-AMS model plugins
models-plugins:
	@$(MAKE) -C models

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
clean:
	@$(MAKE) -C models clean
	@$(MAKE) -C cpp clean
	@$(MAKE) -C tests clean
	@# The sub-makes remove their own .so from plugins/models and plugins/gnucap;
	@# nothing is ever written to plugins/ itself, so only the empty dirs remain.
	@rmdir plugins/models plugins/gnucap plugins/osdi plugins 2>/dev/null || true

# Help
help:
	@echo "Build Gnucap Verilog-AMS Model and Simulator Plugins"
	@echo ""
	@echo "Targets:"
	@echo "  all             - Build all plugins"
	@echo "  models-plugins  - Build Verilog-AMS model plugins only"
	@echo "  gnucap-plugins  - Build Gnucap simulator plugins only"
	@echo "  check           - Build the plugins, then run the test suite"
	@echo "  clean           - Remove all build artifacts"

.PHONY: all models-plugins gnucap-plugins check clean help
