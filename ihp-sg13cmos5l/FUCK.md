# FUCK.md
## Files Under Code-agent's Kingdom

> **DISCLAIMER**: This file tracks code and documentation generated or modified by AI code agents (e.g Claude Code, Open Code, Gemini CLI, Codex). This is a **work in progress** branch.

**Human Orchestrator**: Mauricio Montanares

---

## What is this?

This branch (`cmos5l-drc-with-agents`) contains work on the DRC (Design Rule Check) system for the IHP-SG13CMOS5L slim PDK. Most of this code was generated through agentic coding sessions using Claude Code.

## Status

| Status | Description |
|--------|-------------|
| **WIP** | Work in Progress - Not production ready |
| **REVIEW NEEDED** | All agent-generated code should be reviewed by humans |
| **TESTING REQUIRED** | DRC rules need validation against real designs |

---

## Files Generated/Modified by Code Agents

### Session A: DRC Infrastructure Setup 

#### Created Files

| File | Type | Description |
|------|------|-------------|
| `libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc` | Modified | Main DRC entry point (TopMetal removed) |
| `libs.tech/klayout/tech/drc/run_drc.py` | Symlink | Python CLI runner |
| `libs.tech/klayout/tech/drc/rule_decks/layers_def.drc` | Symlink | Layer definitions |
| `libs.tech/klayout/tech/drc/rule_decks/antenna.drc` | Symlink | Antenna rules |
| `libs.tech/klayout/tech/drc/rule_decks/density.drc` | Symlink | Density rules |
| `libs.tech/klayout/tech/drc/rule_decks/forbidden/` | Symlink | Forbidden patterns |
| `libs.tech/klayout/tech/drc/rule_decks/pin/` | Symlink | Pin rules |

#### FEOL Rule Symlinks (12 files)
| File | Status |
|------|--------|
| `rule_decks/feol/5_1_nwell.drc` | Symlink |
| `rule_decks/feol/5_2_pwellblock.drc` | Symlink |
| `rule_decks/feol/5_3_nbulay.drc` | Symlink |
| `rule_decks/feol/5_5_activ.drc` | Symlink |
| `rule_decks/feol/5_6_activfiller.drc` | Symlink |
| `rule_decks/feol/5_7_thickgateox.drc` | Symlink |
| `rule_decks/feol/5_8_gatpoly.drc` | Symlink |
| `rule_decks/feol/5_9_gatpolyfiller.drc` | Symlink |
| `rule_decks/feol/5_10_psd.drc` | Symlink |
| `rule_decks/feol/5_14_cont.drc` | Symlink |
| `rule_decks/feol/5_15_contbar.drc` | Symlink |
| `rule_decks/feol/7_2_latchup.drc` | Symlink |

#### BEOL Rule Symlinks (7 files)
| File | Status |
|------|--------|
| `rule_decks/beol/5_16_metal1.drc` | Symlink |
| `rule_decks/beol/5_17_metaln.drc` | Symlink |
| `rule_decks/beol/5_18_metalnfiller.drc` | Symlink |
| `rule_decks/beol/5_19_via1.drc` | Symlink |
| `rule_decks/beol/5_20_vian.drc` | Symlink |
| `rule_decks/beol/5_27_passiv.drc` | Symlink |
| `rule_decks/beol/9_1_lbe.drc` | Symlink |

### Documentation (2024-12-10)

| File | Description |
|------|-------------|
| `drc_documentation/README.md` | Documentation index |
| `drc_documentation/01_ARCHITECTURE_OVERVIEW.md` | DRC system architecture |
| `drc_documentation/02_RULE_FILE_SYNTAX.md` | Rule writing syntax guide |
| `drc_documentation/03_LAYER_DEFINITIONS.md` | Layer system documentation |
| `drc_documentation/04_CREATING_NEW_RULES.md` | Guide for adding new rules |
| `drc_documentation/05_QUICK_REFERENCE.md` | Quick reference card |

### Session B: Rule File Modifications (2024-12-11)

#### Modified Files

| File | Type | Description |
|------|------|-------------|
| `libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc` | Modified | Added cu_pillarpad, sbumppad derivations (M5) |
| `rule_decks/beol/6_10_sealring.drc` | Created | Sealring rules (TopMetal removed) |
| `rule_decks/beol/6_9_pad.drc` | Created | Pad rules (M5 as top layer) |
| `rule_decks/beol/7_3_metalslits.drc` | Created | Metal slits (M1-M5 only) |
| `rule_decks/sg13cmos5l_tech_default.json` | Created | DRC parameters (76 removed) |

### Session C: Testing Infrastructure (2024-12-11)

#### Testing Scripts (Local Copies)

| File | Type | Description |
|------|------|-------------|
| `testing/run_regression.py` | Local Copy | Regression test runner |
| `testing/gen_golden.py` | Local Copy | Golden reference generator |
| `testing/README.md` | Symlink | Testing documentation |

#### Test Cases Included (32 symlinks)

| Category | Test Files |
|----------|------------|
| **FEOL (12)** | activ, activfiller, gatpoly, gatpolyfiller, cont, contbar, nwell, pwellblock, nbulay, psd, thickgateox, latchup |
| **BEOL M1-M5 (10)** | metal1, metal2, metal3, metal4, metal5, metalnfiller, via1, via2, via3, via4 |
| **BEOL Mixed (7)** | lbe, metalslits, pad, passiv, pin, sealring, antenna |
| **Density (2)** | density_pass, density_fail |
| **Other (1)** | forbidden |

#### Test Cases Excluded (11 files - TopMetal/HBT/MIM)

| Reason | Files |
|--------|-------|
| TopMetal exclusive | topmetal1, topmetal1filler, topmetal2, topmetal2filler, topvia1, topvia2 |
| HBT/MIM/Schottky | mim, npnsubstratetie, schottkydiode |
| TopMetal dependent | copperpillar, solderbump |

### Session C.2: Golden Reference Generation (2024-12-11)

#### Created/Modified Files

| File | Type | Description |
|------|------|-------------|
| `run_drc.py` | Local Copy | Modified for slim PDK paths |
| `testing/gen_golden.py` | Local Copy | Uses local run_drc.py |
| `testing/run_regression.py` | Local Copy | Uses local run_drc.py |

#### Fixed Symlinks

| Directory | Issue | Fix |
|-----------|-------|-----|
| `rule_decks/*.drc` | 5 levels deep | Fixed to 6 levels |
| `rule_decks/feol/*.drc` | 6 levels deep | Fixed to 7 levels |
| `rule_decks/beol/*.drc` | 6 levels deep | Fixed to 7 levels |
| `testcases/unit/density/` | 9 levels deep | Fixed to 10 levels |

#### Golden References Generated (29 files)

| Category | Files |
|----------|-------|
| **FEOL** | activ, activfiller, gatpoly, gatpolyfiller, cont, contbar, nwell, pwellblock, nbulay, psd, thickgateox, latchup |
| **BEOL M1-M5** | metal1, metal2-5, via1, via2-4, metalnfiller, passiv, lbe |
| **Density** | density_pass, density_fail |
| **Other** | antenna, forbidden, pin |

#### Missing Golden Files (no violations)

| Test | Reason |
|------|--------|
| metalslits.gds | TopMetal slit patterns only |
| pad.gds | TopMetal pad patterns only |
| sealring.gds | TopMetal sealring patterns only |

---

## Session Roadmap

| Session | Description | Status |
|---------|-------------|--------|
| **A** | DRC Infrastructure Setup | COMPLETE |
| **B** | Rule File Modifications | COMPLETE |
| **C** | Testing Infrastructure | COMPLETE |
| **C.2** | Golden Reference Generation | COMPLETE |
| **C.3** | TopMetal Cleanup (optional) | FUTURE |
| **D** | DRC Rule Editor (optional) | FUTURE |

---

## Important Notes

1. **Symlinks**: Many rule files are symlinks to the full PDK (`ihp-sg13g2`). This keeps them in sync with upstream changes.

2. **Modified Files**: Files marked as "Modified" or "Local Copy" have been changed to remove TopMetal/HBT references or use slim PDK paths.

3. **Testing**: DRC regression has been run. Core CMOS rules (FEOL + BEOL M1-M5) PASS. TopMetal rules in density.drc/antenna.drc still need cleanup.

4. **Review**: All code should be reviewed by humans familiar with DRC development and the IHP PDK.

---

## How to Contribute

1. Review agent-generated code carefully
2. Test DRC rules on real layouts
3. Report issues in the appropriate tracking files
4. Mark completed reviews in this file

---

## Contact

For questions about this branch, refer to:
- `AGENTS_SESSION_LOG.md` - Detailed session logs
- `AGENTS_TODO.md` - Remaining tasks
