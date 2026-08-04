# Makefile for Gnucap and Ngspice tests
# (c) Felix Salfelder 2024
#     Lukas Deutz 2026
# GPLv3+

# Default: run all tests
all: check

# Run both gnucap and ngspice tests.
#
# Not a plain prerequisite list: each half now exits nonzero when a test
# mismatches, and stopping at the first failure would hide whether the other
# simulator failed too. That distinction is the useful one here, since a failure
# on both sides points at the model or the reference data while a failure on one
# side points at that simulator's plumbing. So both halves always run and the
# status is reported afterwards.
check:
	@rc=0; \
	$(MAKE) -C gnucap check || rc=1; \
	$(MAKE) -C ngspice check || rc=1; \
	exit $$rc

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
	@echo "To run one test directory:"
	@echo "  make -C gnucap check-<testdir>"
	@echo "  make -C ngspice check-<testdir>"
	@echo ""
	@echo "For the test directories this PDK has, and the test counts:"
	@echo "  make -C gnucap help"
	@echo "  make -C ngspice help"

.PHONY: all check check-gnucap check-ngspice clean help
