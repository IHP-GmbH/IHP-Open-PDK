# ihp-sg13cmos5l/libs.tech/gnucap/Makefile

# Build everything
all: models-plugins gnucap-plugins

# Build Verilog-AMS model plugins
models-plugins:
	@$(MAKE) -C models

# Build gnucap plugins
gnucap-plugins:
	@$(MAKE) -C cpp

# Run all tests
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
	@echo "  check           - Build everything, then run the test suite"
	@echo "  clean           - Remove all build artifacts"

.PHONY: all models-plugins gnucap-plugins check clean help
