# Limitation: GatPoly:filler over PolyRes.drawing is not caught by the KLayout DRC

Proposed final location: `ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/optional/LIMITATION_gatpoly_filler_polyres.md`
(or an equivalent DRC-adjacent docs folder, at IHP's discretion)

Related: issue [#917](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/917), PR [#924](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/924), PR [#940](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/940).

## Summary

The KLayout DRC for `sg13g2` does not flag `GatPoly:filler` (5/22) overlapping `PolyRes.drawing` (128/0), even though the same overlap is a physical poly short according to our own 2.5D stackup. The gap is documented in [`SG13G2_os_layout_rules.pdf`](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/dev/ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf) as much as it is in the DRC decks and the filler generator; all three are mutually consistent, but out of step with the stackup model.

## Evidence

`FPGA8213.gds.gz` from the HeiChips'25 submission (see issue #917) exhibits 154 filler-over-PolyRes overlaps. Running `run_drc.py --precheck_drc` on current `dev` (HEAD `ef9a8bce`, post PR #924 merge) reports "KLayout DRC Check Passed: No DRC violations detected".

Chip-wide intersections measured with `klayout.db`:

| Intersection | Polygons |
|---|---|
| `GatPoly.filler` ∩ `PolyRes.drawing` (128/0) | 154 |
| `GatPoly.filler` ∩ `RES.drawing` (24/0) | 154 (same sites) |
| `GatPoly.filler` ∩ `HeatRes.drawing` (52/0) | 154 (same sites) |
| `GatPoly.filler` ∩ `GatPoly.drawing` (5/0) | 0 |
| `GatPoly.filler` ∩ `SalBlock` / `Activ` / `Cont` | 0 |

Because there is no `GatPoly.drawing` under the filler, PR #924's `drw.join(filler).space(0.18 um)` catches nothing; and because `PolyRes` is not in the `GFil.d` layer list, `GFil.d` stays silent too. PR #940 adds `.and()` overlap detection to the existing filler rules but does not extend them to `PolyRes`, so it does not cover this case either.

## Why `SG13G2_os_layout_rules.pdf` does not catch it

`SG13G2_os_layout_rules.pdf` Rev. 0.4:

- §5.9 `GFil.d`: "Min. GatPoly:filler space to Activ, GatPoly, Cont, pSD, nSD:block, SalBlock = 1.10 um". `PolyRes` is not in this list.
- §5.8 `Gat.b`: "Min. GatPoly space or notch = 0.18 um". Defined on `GatPoly.drawing`; does not pull in `PolyRes`.
- §2 Layer Table: `PolyRes 128/0` is described as "used to mark net resistors", i.e., a marker rather than a physical body layer.
- §6.2 `Rsil`: defines `Rsil = RES + GatPoly` with the poly resistor body drawn on `GatPoly.drawing`, not on `PolyRes`.

Following `SG13G2_os_layout_rules.pdf` strictly, filler over `PolyRes` is not a DRC violation.

## Why physics disagrees

`ihp-sg13g2/libs.tech/klayout/tech/d25/sg13g2_beol.lyd25` contains:

```
GatPoly  = input(5,0) | PolyRes
Rhigh    = SalBlock & pSD & nSD
Rppd     = SalBlock & pSD - nSD
Rsil     = PolyRes - Rhigh - Rppd
RGatPoly = GatPoly - Rhigh - Rppd - Rsil
```

Two things follow:

1. `GatPoly` in the 2.5D stackup is the union `GatPoly.drawing | PolyRes`. Filler placed on `PolyRes` sits on the same physical polysilicon sheet as normal gate poly.
2. `Rsil` is derived from `PolyRes` minus the other resistor flavours, i.e., the salicided n+ poly resistor body is expressed as `PolyRes` in the post-pycell layout, not as `GatPoly.drawing` + `RES`.

That is why the `FPGA8213.gds.gz` resistor cell has 154 filler shapes on `PolyRes` with zero underlying `GatPoly.drawing`; the pycell flow writes `PolyRes` and the DRC only looks at `GatPoly.drawing`.

## Why the existing DRC rule and the KLayout filler macro behave the same way

Both follow `SG13G2_os_layout_rules.pdf` literally, which means both reproduce the same gap.

DRC: `ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/feol/5_9_gatpolyfiller.drc`, line 27:

```
gfil_d_g = activ_drw.join(gatpoly_drw).join(cont_drw).join(psd_drw).join(nsd_block).join(salblock_drw)
```

Filler generator: `ihp-sg13g2/libs.tech/klayout/tech/macros/sg13g2_filler_ActGatP.lym`, line 213:

```
GFil_d = Activ_gp_cpy | Poly_gp_cpy | Cnt_gp_cpy | pSD_cpy | nSD_block_cpy | SalBlock_cpy
```

Neither includes `PolyRes`. A layout filled by our KLayout macro would therefore carry the same bug that Magic's filler had before PR #908, and the DRC would stay silent on it in both cases.

## Interim workaround (opt-in, not wired into precheck or maximal)

`filler_polyres_overlap_check.drc` runs standalone via KLayout's `-b -r` mode. It emits two categories:

- `GatPolyFil.PolyRes.overlap`: literal overlap (filler on PolyRes). This is the real short.
- `GatPolyFil.PolyRes.sep`: filler within 1.10 um of PolyRes, mirroring `GFil.d`'s intent extended to PolyRes.

Proposed install path once accepted upstream: `ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/optional/filler_polyres_overlap_check.drc`.

Invocation:

```
klayout -b -r filler_polyres_overlap_check.drc \
        -rd input=<layout.gds[.gz]> -rd report=<out.lyrdb>
```

Verified on `FPGA8213.gds.gz`: 154 overlap items and 118 proximity edge pairs reported, matching the independent `klayout.db` count.

The rule deck does not modify any file under `precheck_drc` or `maximal`; it is strictly additional and opt-in. It should not be made mandatory until IHP updates `SG13G2_os_layout_rules.pdf`.

## Plan

The direction is an internal IHP call, not a decision to be taken in the public issue. Two paths on the table:

1. Update `SG13G2_os_layout_rules.pdf` to list `PolyRes` under `GFil.d` (and possibly under `Gat.b` or a companion `PolyRes` section), then extend `5_9_gatpolyfiller.drc`, `5_8_gatpoly.drc`, and `sg13g2_filler_ActGatP.lym` symmetrically. Physically faithful and consistent with the 2.5D stackup.
2. Keep `SG13G2_os_layout_rules.pdf` as is but state explicitly that `PolyRes` is a recognition-only marker and that keeping filler off poly resistor bodies is the filler generator's responsibility (Magic, KLayout, and any third-party flow). The DRC gap then becomes a tooling requirement rather than a rule violation.

Until the direction is picked, this document and the opt-in rule deck are intentionally conservative; neither `precheck_drc` nor `maximal` changes classification. Once the call is made:

- Path 1: migrate `filler_polyres_overlap_check.drc` into `rule_decks/feol/5_9_gatpolyfiller.drc` (GFil.d extended with `PolyRes`) and `rule_decks/feol/5_8_gatpoly.drc` (Gat.b joined with `PolyRes`), classified in the appropriate `precheck_drc` / `maximal` tiers in `sg13g2_tech_default.json` and `sg13g2_tech_mod.json`. Update `sg13g2_filler_ActGatP.lym` so the KLayout filler generator respects the same keep-out.
- Path 2: retire the opt-in deck (or keep it as a hygiene-only tool), update `SG13G2_os_layout_rules.pdf` to make `PolyRes` recognition-only explicit, and require filler generators (Magic, KLayout, third-party) to carry the PolyRes keep-out by construction.
