# Agentic Sessions TODO List

This file tracks remaining tasks for the DRC implementation in the slim PDK.

---

## Current Priority: Session C.4 (M5 Density Issues) or Session D (Optional)

---

## Manual Validation Instructions

### Prerequisites

```bash
# Navigate to IHP-Open-PDK root directory (where you cloned the repo)
cd <path-to>/IHP-Open-PDK

# Activate virtual environment
source .venv/bin/activate

# Navigate to slim PDK testing directory
cd ihp-sg13cmos5l/libs.tech/klayout/tech/drc/testing
```

### Running DRC on a Single Test

```bash
# Run DRC on a specific test file
python ../run_drc.py --path testcases/unit/metal1.gds --table metal1

# View results in KLayout
klayout testcases/unit/metal1.gds -m metal1_main.lyrdb
```

### Generating Golden References

```bash
# Generate golden for all tests (parallel with 8 cores)
python gen_golden.py --mp 8

# Generate golden for specific table
python gen_golden.py --table_name activ --run_dir testcases/unit_golden

# Generate golden for density tests
python gen_golden.py --table_name density_pass --run_dir testcases/unit_golden
python gen_golden.py --table_name density_fail --run_dir testcases/unit_golden
```

### Running Regression Tests

```bash
# Run full regression (parallel with 8 cores)
python run_regression.py --mp 8

# Run regression for specific table
python run_regression.py --table_name metal1

# Run regression with custom output directory
python run_regression.py --mp 8 --run_dir my_regression_results
```

### Interpreting Results

| Column | Meaning |
|--------|---------|
| `viol_not_golden` | False positives (violations found but not in golden) |
| `golden_not_viol` | False negatives (expected violations missing) |
| `in_rule_deck` | 1 if rule exists in DRC deck, 0 otherwise |
| `rule_status` | Passed, Rule Failed, Rule Not In Deck (Skipped) |

### Last Successful Regression (Session C.3)

```
Date: 2025-12-11
Duration: ~95 seconds (8 cores)
Result: FEOL/BEOL M1-M5 PASSED, TopMetal rules SKIPPED
```

---

### Session C.2: Golden Reference Generation (COMPLETE)

- [x] Fix broken symlinks (rule_decks/, feol/, beol/, density tests)
- [x] Create local run_drc.py with slim PDK paths
- [x] Create local gen_golden.py and run_regression.py
- [x] Set up Python virtual environment
- [x] Generate 29 golden references (28.56 seconds)
- [x] Run DRC regression
- [x] Validate core CMOS rules pass

### Session C: Testing Infrastructure (COMPLETE)

- [x] Create `testing/testcases/` directory structure
- [x] Symlink testing scripts (run_regression.py, gen_golden.py, README.md)
- [x] Analyze test GDS files for layer compatibility
- [x] Symlink 32 compatible test cases (30 unit + 2 density)
- [x] Skip 11 TopMetal/HBT/MIM exclusive tests
- [x] Generate golden references for slim PDK
- [x] Run DRC regression
- [x] Validate core CMOS rules (FEOL + BEOL M1-M5)

### Session B: Rule File Modifications (COMPLETE)

- [x] **Modified `ihp-sg13cmos5l.drc`** (main entry)
  - Added `cu_pillarpad` derivation using `metal5_drw`
  - Added `sbumppad` derivation using `metal5_drw`

- [x] **Created `6_10_sealring.drc`** (modified copy)
  - Removed `topmetal1_drw`, `topmetal2_drw` from metal layer arrays
  - Removed `topmetal1`, `topmetal2` from name arrays
  - Updated rule comments for Metal5 as top layer

- [x] **Created `6_9_pad.drc`** (modified copy)
  - Removed TM1/TM2 from metals array
  - Changed `Pad.i` rule from TopMetal2 to Metal5

- [x] **Created `7_3_metalslits.drc`** (modified copy)
  - Removed `topmetal1_slit`, `topmetal2_slit` from slit layer array
  - Removed `TM1`, `TM2` from abbreviation array

- [x] **Created `sg13cmos5l_tech_default.json`**
  - Based on full PDK, removed 76 parameters (TopMetal, HBT, MIM, BackMetal)
  - ~300 CMOS parameters retained

---

## Session C.3: TopMetal Cleanup (COMPLETE)

- [x] Create modified density.drc (remove TM1/TM2 rules)
- [x] Create modified antenna.drc (remove TopMetal/TopVia references)
- [x] Remove metalslits.gds test symlink (MIM not in slim PDK)
- [x] Fix run_regression.py RULES_VAR (remove TopMetal/TopVia)
- [x] Modify run_regression.py to skip rules not in deck
- [x] Re-generate golden references after cleanup
- [x] Re-run regression - TopMetal rules now skipped

### Regression Results (Session C.3)

| Category | Status | Notes |
|----------|--------|-------|
| FEOL rules | ✓ PASSED | activ, cont, nwell, gatpoly, etc. |
| BEOL M1-M5 | ✓ PASSED | metal1-5, via1-4, metalnfiller, passiv, lbe |
| density M1-M4 | ✓ PASSED | M1-M4 density rules |
| density M5 | ⚠️ ISSUES | M5Fil.h, M5Fil.k, Slt.i_M1-M5 (pre-existing) |
| TopMetal rules | SKIPPED | TM1/TM2/TV1/TV2 rules - not in slim PDK |
| metalslits/pad/sealring | NOT TESTED | No test coverage (0 violations) |
| forbidden/pin | SKIPPED | Rules not in deck |

### Test Cases INCLUDED (32)

| Category | Test Cases |
|----------|------------|
| **FEOL (12)** | activ, activfiller, gatpoly, gatpolyfiller, cont, contbar, nwell, pwellblock, nbulay, psd, thickgateox, latchup |
| **BEOL M1-M5 (10)** | metal1-5, via1-4, metalnfiller |
| **BEOL Mixed (7)** | lbe, metalslits, pad, passiv, pin, sealring, antenna |
| **Density (2)** | density_pass, density_fail |
| **Other (1)** | forbidden |

### Test Cases SKIPPED (11)

| Category | Test Cases |
|----------|------------|
| TopMetal exclusive | topmetal1, topmetal2, topvia1, topvia2, topmetal1filler, topmetal2filler |
| HBT/MIM/Schottky | mim, npnsubstratetie, schottkydiode |
| TopMetal dependent | copperpillar, solderbump |

---

## Future: Session C.4 (M5 Density Rules Investigation)

### Known Issues (Pre-existing, not related to TopMetal cleanup)

The following density rules show failures in regression testing:

| Rule | Type | viol_not_golden | Description |
|------|------|-----------------|-------------|
| M5Fil.h | Filler | >0 | Metal5 filler rule |
| M5Fil.k | Filler | >0 | Metal5 filler rule |
| Slt.i_M1 | Slit | >0 | Metal1 slit density |
| Slt.i_M2 | Slit | >0 | Metal2 slit density |
| Slt.i_M3 | Slit | >0 | Metal3 slit density |
| Slt.i_M4 | Slit | >0 | Metal4 slit density |
| Slt.i_M5 | Slit | >0 | Metal5 slit density |

### Investigation Tasks

- [ ] Analyze M5Fil.h and M5Fil.k rule definitions in `density.drc`
- [ ] Compare slim PDK parameters vs full PDK parameters in `sg13cmos5l_tech_default.json`
- [ ] Check if test GDS files `density_pass.gds` and `density_fail.gds` need slim PDK versions
- [ ] Verify Slt.i rules are correctly parameterized for M1-M5 only
- [ ] Determine if issues are in rules, test cases, or golden references
- [ ] Fix identified issues and regenerate golden references

### Possible Root Causes

1. **Parameter mismatch**: `sg13cmos5l_tech_default.json` may have incorrect density values
2. **Test case incompatibility**: density tests may include TopMetal patterns that now fail differently
3. **Rule logic issue**: Slit rules may reference removed TopMetal layers indirectly

---

## Future: Session D (Optional)

### Session D: DRC Rule Editor

- [ ] Create `drc_tracking/` directory
- [ ] Write `parse_drc_to_json.py` script
- [ ] Generate `ihp-sg13g2_rules.json` from full PDK
- [ ] Create `ihp-sg13cmos5l_rules.json` (editable)
- [ ] Write `drc_editor_server.py` (REST API)
- [ ] Create `drc_editor.html` (web UI)
- [ ] Implement rule toggling
- [ ] Implement file regeneration

---

## Completed Tasks

### Session A (DONE)

- [x] Create DRC directory structure
- [x] Create utility symlinks (run_drc.py, layers_def.drc, etc.)
- [x] Create FEOL rule symlinks (12 files)
- [x] Create BEOL rule symlinks (7 files)
- [x] Symlink forbidden/ and pin/ directories
- [x] Create main entry point `ihp-sg13cmos5l.drc`
- [x] Remove TopMetal connectivity from main entry
- [x] Document excluded rule files
- [x] Create DRC architecture documentation (6 files)

### Branch Setup (DONE)

- [x] Create `cmos5l-drc-with-agents` branch
- [x] Move drc_documentation into slim PDK
- [x] Create FUCK.md tracking file
- [x] Create AGENTS_SESSION_LOG.md
- [x] Create AGENTS_TODO.md
- [x] Initial commit

---

### Session C (DONE)

- [x] Create testing directory structure
- [x] Symlink testing scripts (3 files)
- [x] Analyze test GDS files for TopMetal layers
- [x] Symlink 32 test cases (30 unit + 2 density)
- [x] Skip 11 TopMetal/HBT/MIM exclusive tests
- [x] Update tracking files (FUCK.md, AGENTS_SESSION_LOG.md)

---

## Notes

- Sessions A, B, C, C.2, C.3 completed - DRC infrastructure and testing functional
- Session C.4 (M5 density investigation) is next priority
- Session D (DRC Rule Editor) is optional but would be useful for future rule management
- All agent work should be reviewed by humans before production use

### Git Commits (Session History)

| Commit | Session | Description |
|--------|---------|-------------|
| 22d8ece | A | DRC infrastructure setup for slim PDK |
| 5dc5ebc | B | Rule file modifications for slim PDK (M5 top) |
| 5594fc2 | C | Testing infrastructure for slim PDK DRC |
| 974b92d | C.2 | Golden reference generation and regression testing |
| 914e7dd | C.3 | TopMetal rules cleanup |
