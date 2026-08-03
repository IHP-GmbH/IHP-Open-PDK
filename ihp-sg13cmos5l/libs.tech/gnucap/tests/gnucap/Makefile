# Makefile for Gnucap tests
# (c) Felix Salfelder 2024
#     Lukas Deutz 2026
# GPLv3+
GNUCAP = gnucap
DIFF = diff
# Exclude test files starting with
TEST_EXCLUDE_PREFIX = wip_
# Force rebuild on check
MAKEFLAGS += -B

TESTDIRS = \
	resistor \
	moslv \
	moshv

# Discover tests automatically: resistor/*.gc, moslv/*.gc, ...
ALL_TESTS := $(foreach d, $(TESTDIRS), $(wildcard $(d)/*.gc))
ALL_TESTS := $(foreach f,$(ALL_TESTS), $(if $(filter $(TEST_EXCLUDE_PREFIX)%,$(notdir $(f))),,$(f)))
# Each test generates an output
ALL_OUTS := $(foreach f, $(ALL_TESTS), $(dir $(f))check/$(notdir $(f)).out)

# Default: check all tests
check: $(ALL_OUTS)
# Rule: one test file *.gc generates one output file *.gc.out
define TEST_RULE
$(dir $(1))check/$(notdir $(1)).out: $(1)
	@mkdir -p $(dir $(1))check
	@# Run gnucap and filter output:
	@cd "$(dir $(1))" && \
	  $(GNUCAP) "$(notdir $(1))" 2>&1 | \
	  tail -n +12 | \
	  grep -v '^stashing as' | \
	  grep -v 'already installed' | \
	  grep -v '^@@' \
	  > "check/$(notdir $(1)).out" || true
	@if [ -f "$(dir $(1))ref/$(notdir $(1)).out" ]; then \
	  if $(DIFF) -u "$(dir $(1))ref/$(notdir $(1)).out" "$$@" > "$$(basename $$@).diff" 2>&1; then \
	    echo "PASS $$(notdir $$<)"; \
	    rm -f "$$(basename $$@).diff"; \
	  else \
	    echo "FAIL $$(notdir $$<)"; \
	  fi; \
	else \
	  echo "MISS $$(notdir $$<)"; \
	fi
endef

# Create one output file target for each test file using TEST_RULE
$(foreach f, $(ALL_TESTS), $(eval $(call TEST_RULE,$(f))))

# Rule: Make each test directory an aggregate target for its test
define DIR_RULE
check-$(1): $(foreach f, $(filter $(1)/%.gc, $(ALL_TESTS)), $(dir $(f))check/$(notdir $(f)).out)
endef
# Create one aggregate per directory in TESTDIRS using DIR_RULE
$(foreach d,$(TESTDIRS),$(eval $(call DIR_RULE,$(d))))

clean:
	@for dir in $(TESTDIRS); do \
	  rm -rf $$dir/check; \
	done

# Help
help:
	@echo "Gnucap Test Suite"
	@echo ""
	@echo "Targets:"
	@echo "  check            - Run all tests (default)"
	@echo "  clean            - Remove all test outputs"
	@echo "  check-<testdir>  - Run tests in specific directory"
	@echo ""
	@echo "Test directories:"
	@for dir in $(TESTDIRS); do echo "  $$dir"; done
	@echo ""
	@echo "Total tests: $(words $(ALL_TESTS))"

.PHONY: check clean $(TESTDIRS) help

