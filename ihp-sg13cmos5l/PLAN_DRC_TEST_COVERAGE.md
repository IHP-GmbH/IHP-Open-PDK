# Plan: DRC Test Coverage for CMOS5L

## Rules Without Test Coverage (39 total)

### Priority 1: Core BEOL Rules (8 rules)

**TopVia1 (4 rules)** - Layer 125/0
| Rule | Description | Value |
|------|-------------|-------|
| TV1.a | Min/max TopVia1 width | 0.42 um |
| TV1.b | Min TopVia1 space | 0.42 um |
| TV1.c | Min Metal4 enclosure of TopVia1 | 0.10 um |
| TV1.d | Min TopMetal1 enclosure of TopVia1 | 0.42 um |

**TopMetal1 (2 rules)** - Layer 126/0
| Rule | Description | Value |
|------|-------------|-------|
| TM1.a | Min TopMetal1 width | 1.64 um |
| TM1.b | Min TopMetal1 space/notch | 1.64 um |

**TopMetal1 Filler (2 rules)** - Layer 126/22
| Rule | Description | Value |
|------|-------------|-------|
| TM1Fil.a1 | Max TopMetal1:filler width | 10.0 um |
| TM1Fil.c | Min TopMetal1:filler space to TopMetal1 | 3.0 um |

---

### Priority 2: Density Rules (3 rules)

| Rule | Description |
|------|-------------|
| TM1.c | Min global TopMetal1 density 25% |
| TM1.d | Max global TopMetal1 density 70% |
| Slt.i_TM1 | TopMetal1 slit rules |

---

### Priority 3: Antenna Rules (4 rules)

| Rule | Description |
|------|-------------|
| Ant.b_TopMetal1 | TopMetal1 antenna ratio |
| Ant.e_TopMetal1 | TopMetal1 cumulative antenna ratio |
| Ant.d_TopVia1 | TopVia1 antenna ratio |
| Ant.f_TopVia1 | TopVia1 cumulative antenna ratio |

---

### Priority 4: Metal Slits (5 rules)

| Rule | Description |
|------|-------------|
| Slt.e1_M1 | Metal1 slit enclosure |
| Slt.e1_M2 | Metal2 slit enclosure |
| Slt.e1_M3 | Metal3 slit enclosure |
| Slt.e1_M4 | Metal4 slit enclosure |
| Slt.e1_TM1 | TopMetal1 slit enclosure |

---

### Priority 5: Pad Rules (7 rules)

| Rule | Description |
|------|-------------|
| Pad.fR_M1 | Pad to Metal1 |
| Pad.fR_M2 | Pad to Metal2 |
| Pad.fR_M3 | Pad to Metal3 |
| Pad.fR_M4 | Pad to Metal4 |
| Pad.fR_TM1 | Pad to TopMetal1 |
| Pad.i | Pad rule i |
| Pad.m | Pad rule m |

---

### Priority 6: Pin Rules (2 rules)

| Rule | Description |
|------|-------------|
| Pin.f_TM1 | TopMetal1 pin rules |
| Pin.h | Pin rule h |

---

### Priority 7: Sealring Rules (11 rules)

| Rule | Description |
|------|-------------|
| Seal.b_activ | Sealring activ |
| Seal.b_metal1 | Sealring metal1 |
| Seal.b_metal2 | Sealring metal2 |
| Seal.b_metal3 | Sealring metal3 |
| Seal.b_metal4 | Sealring metal4 |
| Seal.b_psd | Sealring pSD |
| Seal.b_topmetal1 | Sealring TopMetal1 |
| Seal.k | Sealring rule k |
| Seal.l | Sealring rule l |
| Seal.m | Sealring rule m |
| Seal.n | Sealring rule n |

---

## Implementation Plan

### Phase 1: TopVia1 and TopMetal1 Tests

**Files to create:**
```
testcases/unit/topvia1.gds
testcases/unit/topmetal1.gds
testcases/unit/topmetal1filler.gds
testcases/unit_golden/topvia1_golden.gds
testcases/unit_golden/topmetal1_golden.gds
testcases/unit_golden/topmetal1filler_golden.gds
```

**Layer reference:**
- Metal4: 50/0
- TopVia1: 125/0
- TopMetal1: 126/0
- TopMetal1:filler: 126/22

**Test structure for each rule:**
1. Create geometry that passes (correct dimensions)
2. Create geometry that fails (violates rule)
3. Golden file contains expected violations

### Phase 2: Density Tests for TM1

Add cells to existing density test files:
- `testcases/unit/density/fail/density_fail.gds` - add TM1.c, TM1.d, Slt.i_TM1 cells
- `testcases/unit/density/pass/density_pass.gds` - add passing TM1 cells

### Phase 3: Remaining Rules

Lower priority - can be addressed incrementally:
- Antenna (TM1/TV1 related)
- Metal slits
- Pad rules
- Pin rules
- Sealring rules

---

## Test Case Design Guidelines

### Width/Space Rules (TV1.a, TV1.b, TM1.a, TM1.b)
- Pass: geometry at exactly min value
- Fail: geometry slightly below min value (e.g., 0.01um less)

### Enclosure Rules (TV1.c, TV1.d)
- Pass: via with proper metal enclosure
- Fail: via with insufficient enclosure on one or more sides

### Filler Rules (TM1Fil.a1, TM1Fil.c)
- Pass: filler at max size, proper spacing
- Fail: oversized filler, filler too close to metal

---

## Verification

After each phase:
```bash
cd libs.tech/klayout/tech/drc/testing
python run_regression.py --table_name=<table> --mp=4
```

Final verification:
```bash
python run_regression.py --mp=4
```

Expected outcome: All rules show "Passed" or "Rule Not Tested" (for future phases).

---

## TODO: Review Implications of Forbidden Layer Removal

### Context
Commit `b6fb372` removed all references to forbidden layers from DRC rules:
- nBuLay (32/0), Metal5 (67/0), Via4 (66/0), TopMetal2 (134/0), TopVia2 (133/0)
- TRANS (26/0), MIM (36/0), Vmim (129/0)

### Tasks to Review

#### 1. PCell Implications
- [ ] Review `libs.tech/klayout/python/sg13cmos5l_pycell_lib/` for any PCells that:
  - Use forbidden layers (Metal5, Via4, nBuLay, etc.)
  - Generate structures that assume forbidden layers exist
  - Have layer stack assumptions that need updating to M1-M4-TM1
- [ ] Verify ViaStack PCell only generates up to TopVia1 (not Via4)
- [ ] Verify sealring PCell uses correct metal stack
- [ ] Update any PCell documentation referencing forbidden layers

#### 2. QA Cell Implications
- [ ] Review `libs.qa/drc/` test GDS files for:
  - Test cells containing forbidden layers (should fail forbidden check)
  - Test cells that need updating to use M1-M4-TM1 stack
- [ ] Review `libs.qa/drc/devices/` device test cells
- [ ] Review `libs.qa/drc/layers/` layer test cells
- [ ] Update golden files if test expectations changed

#### 3. DRC Regression Tests
- [x] Run full DRC regression: `cd libs.tech/klayout/tech/drc/testing && python run_regression.py`
- [x] Verify forbidden layer detection works for all 21 forbidden layers
- [x] Add CMOS5L_EXCLUDED_RULES to run_regression.py for rules needing golden file updates
- [ ] TODO: Regenerate golden files for activfiller, gatpolyfiller, antenna tables
  - These tables have golden files from G2 that include nBuLay/TRANS structures
  - CMOS5L DRC produces different violations since nBuLay/TRANS are forbidden
  - Excluded rules: AFil.d, AFil.j, GFil.e, Ant.d_Via3, Ant.e_Metal1, Ant.f_Via2, Ant.f_Via3

#### 4. LVS Integration (PR #3 branch)
- [x] Verify LVS rule decks work with symlinks to G2 (forbidden layers result in empty layers)
- [x] LVS regression passes with excluded_devices configured
- [x] Added forbidden layer detection to LVS (cmos5l_forbidden_check.lvs)
- [x] Created local sg13cmos5l.lvs (replaced symlink to G2)
- [x] Added ESD devices requiring nBuLay to exclusion list (PR #3 comment):
  - idiodevss_2kv, idiodevss_4kv, nmoscl_2, nmoscl_4
- [x] Full excluded_devices list now includes:
  - schottky_nbl1, res_metal5, res_topmetal2, cap_cmim, rfcmim
  - idiodevss_2kv, idiodevss_4kv, nmoscl_2, nmoscl_4

#### 5. Documentation
- [ ] Update CLAUDE.md if layer information changed
- [ ] Verify libs.doc matches actual allowed/forbidden layers
- [ ] Update any README files in affected directories
