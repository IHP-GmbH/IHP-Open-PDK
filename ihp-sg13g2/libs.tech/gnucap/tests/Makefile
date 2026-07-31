# Makefile for Gnucap and Ngspice tests
# (c) Felix Salfelder 2024
#     Lukas Deutz 2026
# GPLv3+

# Default: run all tests
all: check

# Run both gnucap and ngspice tests
check: check-gnucap check-ngspice

# Run gnucap tests
check-gnucap:
	@echo "Running Gnucap tests..."
	@$(MAKE) -C gnucap check

# Run ngspice tests
check-ngspice:
	@echo "Running Ngspice tests..."
	@$(MAKE) -C ngspice check

# Clean all test outputs
clean:
	@$(MAKE) -C gnucap clean
	@$(MAKE) -C ngspice clean

# Help
help:
	@echo "Test Suite Orchestrator"
	@echo ""
	@echo "Targets:"
	@echo "  check (default) - Run all tests (gnucap + ngspice)"
	@echo "  check-gnucap    - Run gnucap tests only"
	@echo "  check-ngspice   - Run ngspice tests only"
	@echo "  clean           - Remove all test outputs"
	@echo ""
	@echo "To run individual test directories (resistor, capacitor, moslv, moshv):"
	@echo "  make -C gnucap <testdir>"
	@echo "  make -C ngspice <testdir>"

.PHONY: all check gnucap ngspice clean help
