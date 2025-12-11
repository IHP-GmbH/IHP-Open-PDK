# Agentic Sessions TODO List

This file tracks remaining tasks for the DRC implementation in the slim PDK.

---

## Current Priority: Session C

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

## Backlog: Session C

### Session C: Testing Infrastructure

- [ ] Create `testing/testcases/` directory structure
- [ ] Symlink compatible test GDS files (27 of 38)
- [ ] Skip TopMetal/MIM/HBT test cases (11 files)
- [ ] Run DRC regression on test cases
- [ ] Validate no false violations

### Test Cases to INCLUDE (27)

| Category | Test Cases |
|----------|------------|
| FEOL | activ, activfiller, gatpoly, gatpolyfiller, cont, contbar, nwell, pwellblock, nbulay, psd, thickgateox, latchup |
| BEOL | metal1-5, via1-4, metalnfiller, metalslits, passiv, sealring, pad, lbe |
| Special | antenna, density, forbidden, pin |

### Test Cases to SKIP (11)

| Category | Test Cases |
|----------|------------|
| TopMetal | topmetal1, topmetal2, topvia1, topvia2, topmetal1filler, topmetal2filler |
| Special | mim, npnsubstratetie, schottkydiode, copperpillar, solderbump |

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

## Notes

- Session B is the next priority - required to have functional DRC
- Session C is important for validation
- Session D is optional but would be useful for future rule management
- All agent work should be reviewed by humans before production use
