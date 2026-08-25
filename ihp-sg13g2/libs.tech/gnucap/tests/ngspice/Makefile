# Makefile for Ngspice tests
# (c) Felix Salfelder 2024
#     Lukas Deutz 2026
# GPLv3+
NGSPICE = ngspice
DIFF = diff
# Exclude test files starting with
TEST_EXCLUDE_PREFIX = wip_
# Force rebuild on check
MAKEFLAGS += -B

TESTDIRS = \
	resistor \
	capacitor \
	moslv \
	moshv

# Discover tests automatically: resistor/*.sp, moslv/*.sp, ...
ALL_TESTS := $(foreach d, $(TESTDIRS), $(wildcard $(d)/*.sp))
ALL_TESTS := $(foreach f,$(ALL_TESTS), $(if $(filter $(TEST_EXCLUDE_PREFIX)%,$(notdir $(f))),,$(f)))
# Each test generates an output
ALL_OUTS := $(foreach f, $(ALL_TESTS), $(dir $(f))check/$(notdir $(f)).out)

# Pinned, because the first rule below is reset-failures and make would
# otherwise take that as the goal: a bare `make` here would clear the
# bookkeeping, run no test and exit 0, which is the failure this file exists to
# stop.
.DEFAULT_GOAL := check

# Aggregate exit status.
#
# A test rule must not fail the build on the spot: the whole suite has to run so
# that one invocation reports the complete PASS/FAIL set. So each test that does
# not pass records itself here, and the aggregate targets fail afterwards. That is
# what makes `make check` return nonzero when something regressed, so it can be
# used as a gate rather than only read.
# Scoped to this make invocation: two concurrent runs in the same directory would
# otherwise share the files, and one finishing would clear the other's record,
# which can turn a real failure into a green report.
RUNID  := $(shell echo $$PPID)
FAILLOG = .check-failures.$(RUNID)
RUNLOG  = .check-ran.$(RUNID)

reset-failures:
	@rm -f $(FAILLOG) $(RUNLOG)

REPORT = ran=$$(cat $(RUNLOG) 2>/dev/null | wc -l); \
	bad=$$(cat $(FAILLOG) 2>/dev/null | wc -l); \
	echo ""; \
	if [ "$$bad" -gt 0 ]; then \
	  echo "$$bad of $$ran tests did not pass:"; \
	  sed 's/^/  /' $(FAILLOG); \
	  rm -f $(FAILLOG) $(RUNLOG); \
	  exit 1; \
	fi; \
	echo "all $$ran tests passed"; \
	rm -f $(RUNLOG)

# Default: check all tests
check: $(ALL_OUTS)
	@$(REPORT)

# Rule: one test file *.sp generates one output file *.sp.out
define TEST_RULE
$(dir $(1))check/$(notdir $(1)).out: $(1) | reset-failures
	@mkdir -p $(dir $(1))check
	@cd "$(dir $(1))" && \
	  $(NGSPICE) -b -o /dev/null "$(notdir $(1))" > /dev/null
	@echo "$$(notdir $$<)" >> $(RUNLOG)
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
check-$(1): $(foreach f, $(filter $(1)/%.sp, $(ALL_TESTS)), $(dir $(f))check/$(notdir $(f)).out)
	@$$(REPORT)
endef
# Create one aggregate per directory in TESTDIRS using DIR_RULE
$(foreach d, $(TESTDIRS), $(eval $(call DIR_RULE,$(d))))

clean:
	@rm -f .check-failures.* .check-ran.*
	@for dir in $(TESTDIRS); do \
	  rm -rf $$dir/check; \
	done

# Help
help:
	@echo "Ngspice Test Suite"
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
