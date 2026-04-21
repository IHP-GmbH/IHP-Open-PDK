---
title: "IHP SG13G2 DRC Test Coverage Gap Analysis"
subtitle: "Pre-existing issues exposed by PR \\#885 (Modular DRC Deck)"
author: "Mauricio Montanares"
date: "2026-04-10"
geometry: margin=2.5cm
fontsize: 11pt
toc: true
numbersections: true
header-includes:
  - \usepackage{longtable}
  - \usepackage{booktabs}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{IHP SG13G2 DRC Test Coverage}
  - \fancyhead[R]{Internal Report}
  - \usepackage{xcolor}
  - \usepackage{hyperref}
  - \hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}
  - \usepackage{enumitem}
  - \setlist[description]{style=nextline}
---

# Executive Summary

[PR #885](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/885) ports the monolithic DRC deck (`sg13g2_maximal.drc`, 3071 lines, 272 rules) into a modular architecture of 49 files orchestrated by `ihp-sg13g2.drc`. This is the first time the modular orchestrator is activated in CI, exposing **170 pre-existing test framework gaps** that were previously hidden because the orchestrator had all include directives commented out.

Key findings:

- **0 DRC logic regressions**: cross-deck comparison shows 0 COUNT_MISMATCH across 40 unit testcases.
- **25 "Unknown" results**: caused by a parser bug in `run_regression.py`, not a DRC issue. Fix: 3 lines.
- **145 "Rule Not Tested"**: rules without dedicated testcase GDS files. 7 tables have no testcase at all; 6 have partial coverage.
- **Separate QA assets exist** (`libs.qa/drc/`) but are not integrated into the regression framework ([Issue #925](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/925)).

# Background

## The modular DRC deck (PR 885)

| Item | Value |
|------|-------|
| PR URL | `https://github.com/IHP-GmbH/IHP-Open-PDK/pull/885` |
| Branch | `feature/drc-modular-parity` on fork `Mauricio-xx/IHP-Open-PDK` |
| Base | `dev` |
| Commits | 11 (signed-off, GPG-signed) |
| Rules ported | 272/272 (100%) |
| Cross-deck parity | 0 COUNT_MISMATCH on 40 unit GDS + 47 MB real chip layout |
| Runtime parity | maximal 41m08s vs modular 41m43s (mp=1) |

## Why CI never caught these issues before

On the `dev` branch, the modular orchestrator `ihp-sg13g2.drc` has **all 38 `%include` directives commented out**:

```ruby
# File: ihp-sg13g2/libs.tech/klayout/tech/drc/ihp-sg13g2.drc (dev branch)
# %include rule_decks/layers_def.drc
# %include rule_decks/feol/5_1_nwell.drc
# %include rule_decks/feol/5_5_activ.drc
# ... (38 lines, all commented)
```

This means CI ran the orchestrator but **executed zero rules**. Combined with the GitHub Actions `paths:` filter (`ihp-sg13g2/libs.tech/klayout/tech/drc/**`), the `drc_regression` workflow only triggers when a PR modifies DRC files. Recent PRs to `dev` (magic fixes, librelane, LVS updates) did not touch this path, so the workflow did not execute at all.

[PR #885](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/885) activates the orchestrator (`#!include` instead of `# %include`) and touches `drc/**`, triggering the workflow for the first time with actual rule execution.

## CI exit code behavior

`run_regression.py` determines pass/fail at line 1125:

```python
# File: testing/run_regression.py, line 1125
failing_results = df[~df["rule_status"].isin(["Passed"])]
```

Any rule status other than `Passed` causes exit 1. This includes `Rule Not Tested` and `Unknown`, not only `Rule Failed`. The `Makefile` target `test-DRC-main` wraps this, and GNU make converts the exit 1 into exit 2, which is what CI reports.

# Analysis of the 25 "Unknown" Rules

## Root cause: parser bug in RULES_VAR

All 25 `Unknown` results are in the `sealring` table. The function `parse_existing_rules()` in `run_regression.py` extracts rule names from `.output()` calls using regex, then expands Ruby `#{}` interpolations via a dictionary called `RULES_VAR` (lines 49--81).

Three variables are **missing** from `RULES_VAR`:

| Variable | Used by | Expands to | Rules affected |
|----------|---------|-----------|----------------|
| `seal_a_name` | `Seal.a_#{seal_a_name}` | Activ, pSD, Metal1--5, TopMetal1--2 | 9 |
| `cv_name` | `Seal.d.#{cv_name}` | Cont, Via1--4, TopVia1--2 | 7 |
| `sf_name` | `Seal.f.#{sf_name}` | Activ, pSD, Metal1--5, TopMetal1--2 | 9 |

Without expansion, the parser sets `in_rule_deck=0` for these rules. Even though the DRC runs correctly (`viol_not_golden=0`, `golden_not_viol=0`), the status logic cannot assign `Passed` because `in_rule_deck` is false. The fallback status is `Unknown`.

## Affected file and lines

| File | Lines | What to change |
|------|------:|----------------|
| `testing/run_regression.py` | 49--81 | Add 3 entries to `RULES_VAR` dict |
| `testing/gen_golden.py` | (verify) | Add same entries if `RULES_VAR` exists |

## Fix

```python
# Add to RULES_VAR in testing/run_regression.py (lines 49-81):
"seal_a_name": ("Activ", "pSD", "Metal1", "Metal2", "Metal3",
                "Metal4", "Metal5", "TopMetal1", "TopMetal2"),
"cv_name": ("Cont", "Via1", "Via2", "Via3", "Via4",
            "TopVia1", "TopVia2"),
"sf_name": ("Activ", "pSD", "Metal1", "Metal2", "Metal3",
            "Metal4", "Metal5", "TopMetal1", "TopMetal2"),
```

## DRC rule implementation (for reference)

The sealring rules are in `rule_decks/beol/6_10_sealring.drc`:

- **Seal.a** (lines 96--106): Min EdgeSeal-layer width = 3.50 um. Iterates over conductor layers.
- **Seal.d** (lines 179--196): Min EdgeSeal-Activ enclosure of contact/via ring = 1.30 um.
- **Seal.f** (lines 206--223): Min Passiv ring outside sealring space to EdgeSeal-layer.

All three use Ruby loops with interpolated output names. The DRC logic is correct; only the test parser fails to match the names.

# Analysis of the 145 "Rule Not Tested"

## Full inventory

### Rules without any testcase GDS (7 tables, 103 rules)

\small

**offgrid (74 rules)** -- `rule_decks/offgrid/offgrid.drc`

All check 5nm grid alignment via `.ongrid()`. No `testing/testcases/unit/offgrid.gds` exists.

| Rule | Layer | Rule | Layer |
|------|-------|------|-------|
| OffGrid.Activ | 1:0 | OffGrid.Activ_filler | 1:22 |
| OffGrid.Activ_nofill | 1:23 | OffGrid.Cont | 6:0 |
| OffGrid.DeepVia | -- | OffGrid.DigiBnd | -- |
| OffGrid.DigiSub | -- | OffGrid.EXTBlock | -- |
| OffGrid.EdgeSeal | -- | OffGrid.EmWind | -- |
| OffGrid.GatPoly | 5:0 | OffGrid.GatPoly_filler | 5:22 |
| OffGrid.GatPoly_nofill | 5:23 | OffGrid.IND | -- |
| OffGrid.LBE | -- | OffGrid.MIM | -- |
| OffGrid.Metal1 | 8:0 | OffGrid.Metal1_filler | 8:22 |
| OffGrid.Metal1_nofill | 8:23 | OffGrid.Metal1_slit | 8:24 |
| OffGrid.Metal2--5 | 10--49:0 | (+ filler/nofill/slit variants) | |
| OffGrid.NWell | 31:0 | OffGrid.PWell | 46:0 |
| OffGrid.PWell_block | -- | OffGrid.Passiv | -- |
| OffGrid.TopMetal1--2 | 126--134:0 | (+ filler/nofill/slit variants) | |
| OffGrid.TopVia1--2 | -- | OffGrid.Via1--4 | -- |
| OffGrid.pSD | 14:0 | OffGrid.nSD | 7:0 |
| OffGrid.nBuLay | 32:0 | OffGrid.nBuLay_block | -- |
| OffGrid.nSD_block | -- | OffGrid.SalBlock | -- |
| OffGrid.ThickGateOx | -- | OffGrid.TRANS | -- |
| OffGrid.Vmim | -- | OffGrid.SRAM | -- |
| OffGrid.RFMEM | -- | OffGrid.Recog_diode | -- |
| OffGrid.Recog_esd | -- | OffGrid.PolyRes | -- |
| OffGrid.Polimide | -- | OffGrid.NoMetFiller | -- |
| OffGrid.dfpad | -- | OffGrid.dfpad_pillar | -- |
| OffGrid.dfpad_sbump | -- | | |

\normalsize

**rhigh (6 rules)** -- `rule_decks/feol/6_4_rhigh.drc`

`Rhi.a` (width), `Rhi.b` (space), `Rhi.c` (enclosure), `Rhi.d` (overlap), `Rhi.e` (area), `Rhi.f` (density). No `rhigh.gds` exists.

**rsil (6 rules)** -- `rule_decks/feol/6_2_rsil.drc`

`Rsil.a`--`Rsil.f`. No `rsil.gds` exists.

**nmosi (5 rules)** -- `rule_decks/feol/5_11_nmosi.drc`

`nmosi.b`, `nmosi.c`, `nmosi.d`, `nmosi.f`, `nmosi.g`. No `nmosi.gds` exists.

**rppd (5 rules)** -- `rule_decks/feol/6_3_rppd.drc`

`Rppd.a`--`Rppd.e`. No `rppd.gds` exists.

**salblock (5 rules)** -- `rule_decks/feol/5_12_salblock.drc`

`Sal.a`--`Sal.e`. No `salblock.gds` exists.

**extblock (3 rules)** -- location TBD

`EXTB.a`, `EXTB.b`, `EXTB.c`. No `extblock.gds` exists.

### Rules with existing GDS but incomplete coverage (6 tables, 42 rules)

| Table | Not Tested | Existing GDS | Missing rules |
|-------|--------:|--------------|---------------|
| psd | 21 | `psd.gds` (21 KB) | pSD.a--n (17), nSDB.a/b/c/e (4) |
| metalslits | 8 | `metalslits.gds` (47 KB) | Slt.g.{M1--M4,TM2}, Slt.h2.{M1,TM1,TM2} |
| nbulay | 4 | `nbulay_nBuLay.gds` (16 KB) | NBLB.a/b/c/d |
| npnsubstratetie | 3 | `npnsubstratetie.gds` (35 MB) | npn13G2.a, npn13G2L.a, npn13G2V.a |
| nwell | 3 | `nwell.gds` (22 KB) | NW.c1.dig, NW.d1.dig, NW.e1.dig |
| sealring | 2 | `sealring.gds` (414 KB) | Seal.c1.TopVia1, Seal.c1.TopVia2 |

For `psd`: the GDS and golden exist but the golden was generated before the modular port added these rules. Regenerating the golden may resolve most or all 21 entries.

# Relationship with [Issue #925](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/925)

[Issue #925](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/925) (`DRC test coverage: integrate libs.qa cells into regression framework`) identifies a broader structural problem: the repository has **two separate sets of DRC test assets** that are not integrated.

## The two test asset sets

\small

| Aspect | `libs.tech/.../ testing/` | `libs.qa/drc/` |
|:-------|:--------------------------|:---------------|
| Purpose | Automated CI regression | Manual QA |
| Format | 1 GDS per table + golden | Pass/fail pairs per rule |
| Coverage | 48 GDS, 447 rules pass | 31 cells, devices+layers |
| CI | Yes (`run_regression.py`) | None |
| Scripts | `gen_golden`, `run_regression` | None |
| Devices | No rhigh, rppd, rsil GDS | Has rhigh, rppd, rsil |

\normalsize

## The duplication problem

While creating testcase GDS files for rhigh, rppd, rsil, and other device tables, we built geometry from scratch. `libs.qa/drc/devices/` already had cells for several of these tables with proper device recognition stacks. The QA cells use a **pass/fail pair approach** that is arguably better for regression testing:

- Each rule has a "pass" cell (valid geometry, no violations expected) and a "fail" cell (intentionally violating geometry)
- The framework can validate both false positives (violations in pass cell) and false negatives (no violations in fail cell)

The current `run_regression.py` framework only uses golden-based comparison and expects one GDS per table with a specific naming convention. The QA cells cannot be directly consumed without adaptation.

## Proposed resolution (from [Issue #925](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/925))

Three options under discussion:

1. **Adapt the framework** to consume QA cells (add a mapping layer between QA cell names and the regression table structure)
2. **Restructure QA cells** to follow the `testing/testcases/unit/` naming convention
3. **Run both as separate CI suites** (parallel workflows)

This decision affects how we proceed with the 145 Rule Not Tested items. If the QA cells are integrated, many of the missing testcases are already solved.

# Impact on CI

## Current CI status for PR 885

| Check | Status | Root cause |
|-------|--------|------------|
| Python Code Linting | PASS | -- |
| DCO | PASS | All 11 commits have `Signed-off-by` |
| drc_regression | FAIL | 170 pre-existing non-Passed items (exit 2 from make) |
| drc_regression_cells | FAIL | Genuine pre-existing violations in SVaricap, pmos, pmosHV PCell templates |

## Projected fix effort

| Phase | Items resolved | Effort | Dependency |
|-------|--------:|--------|------------|
| RULES_VAR parser fix | 25 | Trivial (3 lines) | None |
| psd golden regeneration | up to 21 | Low (scripted) | None |
| offgrid.gds creation | 74 | Low (scriptable) | None |
| 6 new device GDS files | ~30 | Medium (manual KLayout) | Spec PDF |
| 5 existing GDS enhancements | ~16 | Medium (manual KLayout) | Spec PDF |
| QA cell integration ([Issue #925](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/925)) | overlapping | High (framework changes) | Design decision |

## Recommended path forward

1. **Immediate**: fix `RULES_VAR` and regenerate psd golden (46 items, trivial effort).
2. **Short-term**: create `offgrid.gds` programmatically (74 items, scriptable).
3. **Medium-term**: decide on [Issue #925](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/925) before creating remaining device GDS files. If QA cells are integrated, several tables are already covered.
4. **Do not relax `run_regression.py` exit semantics**. Fix the testcases rather than hiding the problem.

# Appendix: Key File Paths

All paths relative to repository root (`IHP-Open-PDK/`).

## DRC deck files

\small

- **`ihp-sg13g2/libs.tech/klayout/tech/drc/ihp-sg13g2.drc`**\
  Modular orchestrator (38 include directives)
- **`ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/sg13g2_maximal.drc`**\
  Monolithic reference deck (272 rules, 3071 lines)
- **`ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/sg13g2_tech_default.json`**\
  Default DRC parameter values
- **`ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/offgrid/offgrid.drc`**\
  74 offgrid rules (single file)
- **`ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/beol/6_10_sealring.drc`**\
  Sealring rules (Seal.a/d/f — the 25 Unknown rules)

## Testing framework

- **`ihp-sg13g2/libs.tech/klayout/tech/drc/testing/run_regression.py`**\
  Golden regression script. `RULES_VAR` dict at lines 49--81.
- **`ihp-sg13g2/libs.tech/klayout/tech/drc/testing/gen_golden.py`**\
  Golden GDS generator
- **`ihp-sg13g2/libs.tech/klayout/tech/drc/testing/run_crossdeck_comparison.py`**\
  Cross-deck parity check (modular vs maximal)
- **`ihp-sg13g2/libs.tech/klayout/tech/drc/testing/testcases/unit/`**\
  41 testcase GDS files
- **`ihp-sg13g2/libs.tech/klayout/tech/drc/testing/testcases/unit_golden/`**\
  41 golden GDS files

## QA assets (Issue [#925](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/925))

- **`ihp-sg13g2/libs.qa/drc/`**\
  QA DRC cells (not integrated into CI)
- **`ihp-sg13g2/libs.qa/drc/devices/`**\
  Device-level pass/fail cells (rhigh, rppd, rsil, mim, sealring)

## Spec documentation

- **`ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf`**\
  Layout design rules specification
- **`ihp-sg13g2/libs.doc/doc/SG13G2_os_process_spec.pdf`**\
  Process specification

\normalsize

# References

- [PR #885 -- Modular DRC deck](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/885)
- [PR #885 -- CI status comment](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/885#issuecomment-4212487032)
- [Issue #925 -- DRC test coverage: integrate libs.qa cells](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/925)
- [PR #900 -- Fix DRC JSON precedence](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/900)
- [PR #819 -- DRC updates (added untested rules)](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/819)
