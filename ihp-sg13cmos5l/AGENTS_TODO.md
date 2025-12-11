# Agentic Sessions TODO List

This file tracks remaining tasks for the DRC implementation in the slim PDK.

---

## Current Priority: Session C.3 (TopMetal Cleanup) or Session D (Optional)

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

## Remaining Tasks: Session C.3 (TopMetal Cleanup)

- [ ] Create modified density.drc (remove TM1/TM2 rules)
- [ ] Create modified antenna.drc (remove TopMetal references)
- [ ] Re-generate golden references after cleanup
- [ ] Re-run regression to validate all rules pass
- [ ] Document final test results

### Regression Results (Session C.2)

| Category | Status | Notes |
|----------|--------|-------|
| FEOL rules | ✓ PASSED | activ, cont, nwell, gatpoly, etc. |
| BEOL M1-M5 | ✓ PASSED | metal1-5, via1-4, metalnfiller |
| BEOL passiv/lbe | ✓ PASSED | All rules |
| density TM2.c | ✗ FAILED | TopMetal rule - needs removal |
| metalslits/pad/sealring | NOT TESTED | No M1-M5 violations in test files |
| forbidden/pin | UNKNOWN | Rules not in deck |

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

- Sessions A, B, C completed - DRC infrastructure and testing ready
- Session D is optional but would be useful for future rule management
- All agent work should be reviewed by humans before production use
- Testing TODO: Generate golden references and run regression
