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

# Aggregate exit status.
#
# A test rule must not fail the build on the spot: the whole suite has to run so
# that one invocation reports the complete PASS/FAIL set. So each test that does
# not pass records itself here, and the aggregate targets fail afterwards. That
# is what makes `make check` return nonzero when something regressed, which the
# repository-root `make test-gnucap` target relies on.
FAILLOG = .check-failures

reset-failures:
	@rm -f $(FAILLOG)

REPORT = if [ -s $(FAILLOG) ]; then \
	  echo ""; \
	  echo "$$(wc -l < $(FAILLOG)) test(s) did not pass:"; \
	  sed 's/^/  /' $(FAILLOG); \
	  rm -f $(FAILLOG); \
	  exit 1; \
	else \
	  echo ""; \
	  echo "all $(words $(ALL_TESTS)) tests passed"; \
	fi

# Default: check all tests
check: $(ALL_OUTS)
	@$(REPORT)

# Rule: one test file *.gc generates one output file *.gc.out
define TEST_RULE
$(dir $(1))check/$(notdir $(1)).out: $(1) | reset-failures
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
	    echo "FAIL $$(notdir $$<)" >> $(FAILLOG); \
	  fi; \
	else \
	  echo "MISS $$(notdir $$<)"; \
	  echo "MISS $$(notdir $$<)" >> $(FAILLOG); \
	fi
endef

# Create one output file target for each test file using TEST_RULE
$(foreach f, $(ALL_TESTS), $(eval $(call TEST_RULE,$(f))))

# Rule: Make each test directory an aggregate target for its test
define DIR_RULE
check-$(1): $(foreach f, $(filter $(1)/%.gc, $(ALL_TESTS)), $(dir $(f))check/$(notdir $(f)).out)
	@$$(REPORT)
endef
# Create one aggregate per directory in TESTDIRS using DIR_RULE
$(foreach d,$(TESTDIRS),$(eval $(call DIR_RULE,$(d))))

clean:
	@rm -f $(FAILLOG)
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

# $(TESTDIRS) are directories, not targets; the aggregates are check-<testdir>.
.PHONY: check clean help reset-failures $(addprefix check-,$(TESTDIRS))

