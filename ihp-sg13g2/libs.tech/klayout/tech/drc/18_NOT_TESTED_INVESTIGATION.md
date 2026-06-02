# Investigation: 18 Rule Not Tested (2026-04-21)

Baseline: 599 Passed, 0 Unknown, 18 Rule Not Tested
Branch: feature/drc-modular-parity
After: QA GDS integration + RULES_VAR fix + orchestrator nil fix

## Summary

| Category | Count | Rules | Root Cause | Fix |
|----------|------:|-------|-----------|-----|
| Parser phantom | 5 | Slt.g.M1, Slt.g.M2, Slt.g.M3, Slt.g.M4, Slt.g.TM2 | RULES_VAR expands `#{met_abbrev}` to all 7 metals but Slt.g only exists for M5/TM1 per spec sec 7.3 | RULES_EXCLUDE |
| Parser phantom | 3 | Slt.h2.M1, Slt.h2.TM1, Slt.h2.TM2 | Slt.h2 only for M2-M5 per spec; M1=Slt.h1, TM1=Slt.h3, TM2=Slt.h4 | RULES_EXCLUDE |
| Parser phantom | 2 | Seal.c1.TopVia1, Seal.c1.TopVia2 | Seal.c1 iterates Via1-4 only per spec sec 6.10; TopVia1=Seal.c2, TopVia2=Seal.c3 | RULES_EXCLUDE |
| Wrong table map | 4 | nSDB.a, nSDB.b, nSDB.c, nSDB.e | QA cell nSDBlock split to `nsdblock.gds` -> table "nsdblock", but rules in table "psd" | Rename to psd_nSDBlock.gds |
| **DRC bug** | 3 | npn13G2.a, npn13G2L.a, npn13G2V.a | `ext_with_length` bug: `+1` adds 1um instead of 1dbu | Fix ext_utils.drc |
| No fail geometry | 1 | Rhi.b | pSD/nSD mismatch check in Rhigh; QA has correct geometry -> zero violations | Need fail structures |

## BUG: ext_with_length `+1` adds 1 micrometer instead of 1 dbu

### Discovery

While investigating why npn13G2.a/L.a/V.a show "Rule Not Tested" despite the QA GDS
having proper fail structures (EmWind with undersized dimensions inside TRANS), we
discovered that the `ext_with_length` utility function has a unit error that renders
multiple DRC rules non-functional.

### Root Cause

File: `rule_decks/ext_utils.drc` lines 882-895
File: `rule_decks/sg13g2_maximal.drc` lines 1013-1026 (identical copy)

```ruby
def ext_with_length(constraint)
    # ...
    constraint.each do |expression|
        if expression[0] == ">"
            edge_layer = edge_layer.with_length((expression[1] + 1), nil)  # BUG: +1 = +1um
        # ...
        elsif expression[0] == "<="
            edge_layer = edge_layer.with_length(nil, (expression[1] + 1))  # BUG: +1 = +1um
        end
    end
end
```

KLayout's `with_length(min, nil)` selects edges with length >= min. To convert strict
`>` into `>=`, the code adds 1 to the threshold, intending to add 1 database unit (1nm).
But `expression[1]` is a float in micrometers (e.g., `0.07.um` = 0.07), so `+ 1` adds
**1 micrometer** instead of 1nm.

Compare with the correct pattern used elsewhere in the same file (line 306):
```ruby
lower_bound = value + 1.dbu**2   # correct: adds 1 dbu-squared for area
```

### Proof

Debug DRC run on `npnsubstratetie.gds`:
```
emit_npn13g2 count: 4001
all edges: 16004
buggy  >0.07 (uses +1um):  0 edges   -- threshold = 1.07um, no edge that long
correct >0.07 (uses +1dbu): 8002 edges
correct combined (>0.07 AND <0.9): 2 edges  -- the 2 edges of the 0.070x0.890 fail EmWind
```

The QA GDS contains intentional fail structures that the DRC cannot detect:
- npn13G2.a zone: EmWind 0.070x0.890um inside TRANS with "npn13G2" text label
- npn13G2L.a zone: EmWind 0.070x0.990um inside TRANS with "npn13G2L" text label
- npn13G2V.a zone: EmWiHv 0.120x0.990um inside TRANS with "npn13G2V" text label

### Fix

```ruby
# Line 884 (ext_utils.drc) and line 1015 (sg13g2_maximal.drc):
edge_layer = edge_layer.with_length((expression[1] + 1.dbu), nil)

# Line 894 (ext_utils.drc) and line 1025 (sg13g2_maximal.drc):
edge_layer = edge_layer.with_length(nil, (expression[1] + 1.dbu))
```

`1.dbu` in KLayout DRC context evaluates to 0.001um (1nm), which is the correct
minimum increment for the 5nm manufacturing grid.

### Full Impact Assessment

**Rules using `>` operator (dead or under-reporting):**

| Rule | Deck | Expression | Correct threshold | Buggy threshold | Impact |
|------|------|-----------|:-:|:-:|--------|
| npn13G2.a | both | `[[">", 0.07], ["<", 0.9]]` | >= 0.071um | >= 1.07um | **DEAD** -- never fires |
| npn13G2L.a | both | `[[">", 0.07], ["<", 1.0]]` | >= 0.071um | >= 1.07um | **DEAD** -- never fires |
| npn13G2V.a | both | `[[">", 0.12], ["<", 1.0]]` | >= 0.121um | >= 1.12um | **DEAD** -- never fires |
| npn13G2L.b | maximal | `[[">", 2.5]]` | >= 2.501um | >= 3.5um | Under-reports; modular uses `.edges.with_length` (no bug) |
| npn13G2V.b | maximal | `[[">", 5.0]]` | >= 5.001um | >= 6.0um | Under-reports; modular uses `.edges.with_length` (no bug) |
| Slt.b.M1 | both | `[['>', 20.0]]` | >= 20.001um | >= 21.0um | Under-reports max slit width |
| Slt.b.M2 | both | `[['>', 20.0]]` | >= 20.001um | >= 21.0um | Under-reports |
| Slt.b.M3 | both | `[['>', 20.0]]` | >= 20.001um | >= 21.0um | Under-reports |
| Slt.b.M4 | both | `[['>', 20.0]]` | >= 20.001um | >= 21.0um | Under-reports |
| Slt.b.M5 | both | `[['>', 20.0]]` | >= 20.001um | >= 21.0um | Under-reports |
| Slt.b.TM1 | both | `[['>', 20.0]]` | >= 20.001um | >= 21.0um | Under-reports |
| Slt.b.TM2 | both | `[['>', 20.0]]` | >= 20.001um | >= 21.0um | Under-reports |

**No current rules use `<=` operator**, but the bug exists and would affect future rules.

**Rules NOT affected** (use `<`, `>=`, `==`, `!=` -- these are correctly implemented):
All other `ext_with_length` callers, and all rules that use `.edges.with_length()` directly
(like the modular deck's npn13G2L.b and npn13G2V.b).

### Additional Finding: EmWiHv layer discrepancy

The maximal deck uses `EmWind` (33/0) for ALL three NPN variants:
```ruby
# sg13g2_maximal.drc
emit_npn13G2V = EmWind.inside(transG2V)   # line 1798 -- uses EmWind
```

The modular deck correctly uses `EmWiHv` (156/0) for npn13G2V:
```ruby
# 6_1_npnsubstratetie.drc
emit_npn13g2v = emwihv_drw.inside(trans_g2v)  # line 63 -- uses EmWiHv
```

The QA GDS confirms the modular is correct: npn13G2V fail structures use EmWiHv (156/0),
not EmWind (33/0). The maximal deck has a latent layer mismatch for npn13G2V that is
masked by the `ext_with_length` bug (the rule never fires either way).

---

## Detailed Analysis

### Parser Phantoms (10 rules) -- CONFIRMED against spec PDF

The `parse_existing_rules()` function in `run_regression.py` uses `RULES_VAR` to expand
Ruby interpolations like `#{met_abbrev}` in `.output()` calls. It cannot understand Ruby
conditionals, so it generates rule names for ALL variable values, including combinations
that the code never reaches.

**Metalslits (sec 7.3 of SG13G2_os_layout_rules.pdf):**
- Slt.g: "Min. Metal5:slit and TopMetal1:slit space to MIM = 0.60" -- ONLY M5, TM1
- Slt.h family is split by layer:
  - Slt.h1: M1 only (space to Cont and Via1, 0.30um)
  - Slt.h2: M2-M5 (space to Via(n-1) and Via(n), 0.30um)
  - Slt.h3: TM1 only (space to TopVia1, 1.00um)
  - Slt.h4: TM2 only (space to TopVia2, 1.00um)
- DRC implementation matches spec: `7_3_metalslits.drc` lines 130-193

**Sealring (sec 6.10 of SG13G2_os_layout_rules.pdf):**
- Seal.c1: "EdgeSeal-Via(n=1-4) ring width = 0.19" -- Via1-Via4 ONLY
- Seal.c2: "EdgeSeal-TopVia1 ring width = 0.42" -- separate rule
- Seal.c3: "EdgeSeal-TopVia2 ring width = 0.90" -- separate rule
- DRC implementation matches: `6_10_sealring.drc` lines 137-174
- Seal.c2 and Seal.c3 ARE already implemented and tested (they pass)

**Proposed fix:** Add `RULES_EXCLUDE` set to `run_regression.py` containing these 10 phantom names,
and filter them out in `parse_existing_rules()` after expansion.

### Wrong Table Mapping: nSDB (4 rules)

Rules nSDB.a-c,e are defined in `rule_decks/feol/5_10_psd.drc` (table = "psd").
QA has cell "nSDBlock" which was split to `qa_split/nsdblock.gds`.
The regression framework derives table name from golden filename: first underscore token.
`nsdblock_golden.gds` -> table "nsdblock" (wrong; should be "psd").

**Fix:** Copy `qa_split/nsdblock.gds` to `unit/psd_nSDBlock.gds` -> golden `psd_nSDBlock_golden.gds` -> table "psd".

### No Fail Geometry: Rhi.b (1 rule)

**Rhi.b** (`6_4_rhigh.drc` line 53-57):
- Checks: `psd_nsd_mismatch.and(rhigh_recog)` -- pSD and nSD must be identical within Rhigh
- QA rhigh.gds has proper pSD/nSD alignment -> zero violations
- QA file identical to unit file (90 shapes, 10 layers)
- Fix: create a Rhigh structure with mismatched pSD/nSD (shift nSD:drawing by ~0.1um)
- Required layers: GatPoly (5/0), pSD (14/0), nSD:drawing (7/0), SalBlock (28/0),
  EXTBlock (111/0), Cont (6/0)
- Spec reference: section 6.4, Figure 6.5

## Files Reference

- Spec PDF: `/home/montanares/git/IHP-Open-PDK/ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf`
- ext_utils bug: `rule_decks/ext_utils.drc` lines 884, 894
- maximal bug: `rule_decks/sg13g2_maximal.drc` lines 1015, 1025
- Parser: `testing/run_regression.py` lines 49-84 (RULES_VAR), 607-683 (parse_existing_rules)
- metalslits DRC: `rule_decks/beol/7_3_metalslits.drc` lines 98, 130-193
- sealring DRC: `rule_decks/beol/6_10_sealring.drc` lines 137-174
- rhigh DRC: `rule_decks/feol/6_4_rhigh.drc` lines 53-57
- npn DRC: `rule_decks/feol/6_1_npnsubstratetie.drc` lines 136-185
- psd DRC: `rule_decks/feol/5_10_psd.drc` lines 218-244
- QA split: `testing/testcases/qa_split/` (52 files)
- QA split script: `testing/testcases/scripts/split_qa_gds.py`
