---
title: "sg13g2_stdcell_hv — Generation of a Thick-Oxide (3.3 V) Standard Cell Library"
subtitle: "IHP SG13G2 open PDK · derivation, all views, verification and physical sign-off"
author:
  - "Koen Van Caekenberghe, Ph.D."
  - "ChipDesign B.V."
  - "[info@chipdesign.be](mailto:info@chipdesign.be)"
date: "2026-08-18 (rev. 5: all 84 cells drawn, strict-rule N-wells, LibreLane SCL, drive limits, special-cell characterization)"
logo: "ChipDesign_logo.png"
---

# Scope and result

The IHP SG13G2 open PDK ships no 3.3 V standard cells: its thick-oxide
devices appear only in the `sg13g2_io` pad ring. `sg13g2_stdcell_hv` fills
that gap — **all 84 cells** of `sg13g2_stdcell` rebuilt on `sg13_hv_nmos` /
`sg13_hv_pmos`, same topology, pin names and pin order, named `sg13g2_hv_*`
so both libraries coexist in one netlist.

| Deliverable | Coverage | Status |
|---|---|---|
| SPICE netlist (`spice/`) | 84 cells, 920 devices | verified against 3 independent views |
| CDL netlist (`cdl/`) | 84 cells + 2 tie cells | LVS reference, all 84 cells match |
| Verilog (`verilog/`) | 84 modules | shared `ihp_*` UDPs, deliberately not duplicated |
| xschem symbols / schematics | 84 + gallery sheet | netlist-equivalence proven |
| GDS layout (`gds/`) | **84 cells** (66 retargeted + 18 per-cell generated) | **DRC clean, LVS clean** |
| LEF abstracts (`lef/`) | **84 macros** + `CoreSiteHV` site | generated from the GDS, pin sets verified against CDL |
| Liberty NLDM (`lib/`) | **all 84 cells**, 668 timing tables, **3 corners** | combinational, sequential, tri-state and clock-gate; areas all measured; typ, fast and slow |
| LibreLane SCL (`librelane/`) | site, cell maps, tracks, excludes | flops map natively through `dfflibmap` |

Physical sign-off, one fixed invocation of the PDK's own klayout decks — on
the abutted two-row array and on the stricter **shared-rail array** (rows at
the true 7.14 µm pitch, mixed and mirrored vertical neighbours — what a
placed block actually produces) — and, since rev. 5, under Magic's *strict
analog* N-well rules as well:

| Check | This library | IHP thin-oxide control (same harness) |
|---|---|---|
| DRC, cell rules | **0** | 0 |
| DRC, cell rules, shared-rail mixed array | **0** | — |
| DRC, Magic (strict analog N-well rules) | **0 `NW.*`** | — |
| DRC, chip-level metal density | 7 | 6 |
| LVS | **84 / 84 match** | fill cells fail identically without the documented relaxation |

The density items are harness properties, not cell defects: metal density is
a check on a *filled* die, and the one differing count (`M1.j`, min 35 %
Metal1) reads 35.0 % over the padded array's bounding box against 37.1 %
over the actual cell area (control: 45.2 %).

The library has also carried a real block: two variants of the `spi_slave`
IP placed and routed through LibreLane/OpenROAD at 100 MHz pass the full
IHP signoff deck — zero geometry violations (section 6).

---

# The device transform

| | thin oxide | thick oxide |
|---|---|---|
| device model | `sg13_lv_nmos` / `sg13_lv_pmos` | `sg13_hv_nmos` / `sg13_hv_pmos` |
| gate length | 130 nm | **450 nm** (`Gat.a3` minimum) |
| NMOS width | — | unchanged |
| PMOS width | — | **× 2.40**, snapped per finger to the 5 nm grid |
| `as`/`ad`/`ps`/`pd` | — | recomputed from device geometry |
| supply | 1.2 V | 3.3 V |

Deliberate long-channel devices (decap 1.0 µm, `sighold` 700 nm,
`dlygate4sd3_1` 500 nm) keep their lengths; 914 devices moved to 450 nm.
The antenna cell is unchanged apart from its name (junction diodes).

**Why × 2.40.** The thin-oxide library is sized for a centred switching
threshold ($V_m/V_{DD} = 0.5046$ at $W_p/W_n = 1.5135$), not drive match.
At 3.3 V / 450 nm the PMOS is far weaker (219 vs 533 µA/µm) and the same
$V_m$ needs $W_p/W_n = 3.63$, i.e. $K_p = 3.63/1.5135 = 2.40$ on every
PMOS with every NMOS untouched — preserving each cell's internal stack
ratios. Across the library's 0.3–17.9 µm width range the required ratio
stays within ±5 % of 2.40 (`work/vm_sweep.py`, `work/ratio_check.py`).

**Parasitics** follow the vendor deck's geometry formulas; before any
generation they were validated by recomputing all 924 thin-oxide devices
(worst relative error $3.75\times10^{-4}$, the vendor's four printed
digits). The generator refuses to run if this validation fails.

**Cost**, measured on `inv_1` (`work/fo4.py`): input capacitance 2.67 →
5.87 fF (2.20×), FO4 delay 53.6 → 142.4 ps (2.66×). The thick-oxide NMOS
delivers *more* current per micron at 3.3 V than the thin-oxide at 1.2 V
(533 vs 391 µA/µm) — the loss is capacitance, not drive.

---

# The views

All netlist views are re-emitted from one internal model by
`work/gen_hv_lib.py`, so a device cannot silently diverge between views.

* **`spice/`** — 84 subckts, 920 PSP103 devices (OSDI/ngspice); widths
  synchronised to the drawn layout.
* **`cdl/`** — the same subcircuits as `M`-cards with `*.PININFO`, the LVS
  reference; compared field-by-field against SPICE by `verify_sch.py`.
* **`verilog/`** — 84 modules; deliberately no copy of `sg13g2_udp.v` (the
  `ihp_*` UDPs are shared — a second copy would collide).
* **`sym/`, `sch/`** — 84 symbols (thin-oxide drawn geometry, thick-oxide
  netlist prefix, `$::SG13G2_HV_SCH` resolution) and 84 schematics plus a
  generated gallery sheet; three-view consistency proven on all 920
  devices.
* **`gds/`** — **all 84 cells**: 66 by 1-D retarget (section 4), 18 by
  per-cell generators (section 4.1). Uniform 7.140 µm row height (17
  tracks), every width a 0.48 µm site multiple, all contact/via cuts
  exactly 0.16 × 0.16 µm, every rail tap on the site-centred 0.48 µm grid
  (`work/fix_rail_contacts.py`, section 6).
* **`lef/`** — 84 macros + `CoreSiteHV`, generated from the GDS: pins from
  the pin datatypes labelled by contained text, OBS = drawn metal minus pin
  geometry, antenna values recomputed from the netlist (the thin-oxide
  numbers are wrong for 3.5× longer gates). Parsed back with klayout and
  pin sets verified against the CDL.
* **`lib/`** — Liberty NLDM at 3.3 V / 25 °C typical (section 7).
* **`librelane/`** — a complete LibreLane standard-cell-library
  configuration (section 8), installed as
  `libs.tech/librelane/sg13g2_stdcell_hv/`.
* **`klayout/`** — a cell-library registration macro: with the repository's
  `klayout/` directory on `KLAYOUT_PATH`, all 84 cells appear in
  KLayout's Instance dialog as library `sg13g2_stdcell_hv`.

---

# Layout generation

Hand-drawn 2-D layout cannot be regenerated by placement, but it can be
**1-D retargeted**: monotone piecewise-linear coordinate maps applied to
every vertex preserve topology, so connectivity survives by construction
(`work/layout_retarget.py`). The engineering is in the breakpoints and the
exceptions:

* **x-map**: gates widen 0.13 → 0.45 µm about their centres; contacted
  poly pitch 0.48 → 0.80 µm. One accepted consequence: `dlygate4sd2_1`
  staggers two gates at overlapping x, so its PMOS lands at a legal
  0.625 µm, carried consistently into every netlist view.
* **y-map**: PMOS band × 2.40 plus three channel inserts for the
  thick-oxide clearances (`NW.d1.dig` 0.215 µm, `pSD.j1` 0.100 µm,
  `pSD.i1` rail insert 0.430 µm), derived library-wide so every cell keeps
  one row height.
* **PMOS diffusion** is re-emitted per connected slab piece with channel
  slabs frozen — the only scheme that keeps exact 5 nm-grid device widths
  without merging, collapsing or renaming devices (each alternative was
  tried and caught by LVS or `Act.*` rules).
* **Cut layers are translated, never scaled**; contacts are re-tiled inside
  the new Activ at 0.36 µm pitch (`Cnt.b1` array spacing), grouped by
  polygon.
* **ThickGateOx** is drawn on the cell boundary grown 0.27 µm in x and
  0.42 µm in y — the y-margin proven by the N-row edge experiment (the
  TGO.a count stays 2 for any N and moves with the outer edge).
* **Five Metal1 re-routes** (`M1E_EDITS` in the generator) resolve the
  `M1.e` wide-metal gaps the retarget manufactures; each edit is verified
  in code (polygon count, `M1.a/b/c1`, 5 nm grid).
* **Netlist ↔ layout sync**: the drawn width is authoritative;
  `work/sync_netlist_widths.py` brings SPICE and CDL to the drawn geometry
  per *finger* and recomputes parasitics.
* **Site and tracks**: `TRACK_PAD` stretches the mid-cell dead zone to make
  exactly 17 horizontal 0.42 µm tracks; `pad_to_site` pads each width to
  the 0.48 µm site (13.75 µm total across the library). Mean cell area is
  **2.87×** the thin-oxide library (median 2.83, range 1.89–4.21).

## The 18 cells the library-wide map could not produce

`layout_retarget.py` skips 18 cells, and for a long time they were the
library's headline limitation. They are not a single hard case: the skips
have **one shared root cause**. A p+ source finger butts into the VDD rail
tap, so the library-wide y-map cannot scale that band without moving the
rail off the cell boundary and breaking abutment. Several flip-flops add a
second obstruction, an NMOS Activ band that reaches the library channel
cut.

Once that was understood the fix is mechanical, and is applied per cell
rather than library-wide:

1. **Cut the butting finger before the map** — the neck joining the p+
   source to the rail tap is removed, asserted exactly, so the band is free
   to scale.
2. **Split the y-insert per cell** — instead of the library's single
   0.975 µm insert, each cell distributes the same total across a rail
   insert, a channel-cut insert and a pSD insert, chosen so that every
   template band (rails, taps, pSD, N-well, ThickGateOx) lands exactly on
   its shipped position and the high NMOS band tops out 0.62 µm below the
   strict N-well bottom.
3. **Restore the finger after the map** at y = 6.99 µm, the butted-junction
   convention the drawn `slgcp_1` already uses and which the LVS deck
   connects through `psd_ntap_abutt`.
4. **Rebuild the N-well** with the strict-rule construction of section 6,
   and re-tile rail contacts onto the site-centred grid.

`work/flop_pilot/gen_seq.py` drives the eight flip-flops from a per-cell
insert table; `work/cell_dev/{latches,ebufn,misc}/gen_*.py` cover the four
latches, the two tri-state drives, `lgcp_1` and `sighold`. Two cells are
not retargets at all: `lgcp_1` is derived from the drawn `slgcp_1` by
deleting the scan leg (which also required splitting a shared series
node — the scan cell joins the PMOS and NMOS chains in Metal1 where the
plain gate does not), and `sighold` is built from scratch on the tie-cell
frame. **No device width, length or connectivity deviates from the CDL in
any of the 18 cells**, so the existing characterization stays valid; only
`area` changes, and it changes from an estimate to a measurement.

Every generated cell had to pass `work/cell_verify.py` before it was
merged into the library: LVS against the CDL, both KLayout decks in an
abutted mirrored context, Magic, the structural conventions (row height,
site-multiple width, N-well rules) and the pin/track report. The gate was
itself validated by running it against an already-shipped cell.

---

# Functional verification

| Suite | Coverage | Result |
|---|---|---|
| `verify_logic.py` | 60 combinational cells, 452 vectors, both libraries in one deck | **PASS** |
| `verify_seq.py` | 16 stateful cells, 400 clocked samples | **PASS** |
| `verify_sch.py` | 84 schematics + CDL vs SPICE, 920 devices field-by-field | **PASS** |

The thin-oxide library is the golden reference — the transform changed
devices, never logic. The 12 high-impedance states of the tri-state cells
are exercised; illegal set/reset combinations are excluded rather than
counted as passes; both suites were re-run on the final, shipped netlists.

---

# Physical sign-off

**Methodology.** Cells are checked in abutted context, never standalone.
Two harnesses: `work/make_drc_top.py` (every cell in its own column,
mirrored second row at the padded bbox pitch) for cell-internal rules, and
`work/make_shared_rail_rows.py` — rows at the true 7.14 µm pitch,
orientations N/S/FS, rotated cell order per row, cells advanced by LEF
width — for everything only a placed block exhibits. Measurement rules,
each bought with a wrong conclusion: one fixed runner invocation (counts
from different flag sets are not comparable), diagnosis from flat
`klayout.db` rule replication (deep-mode marker coordinates mis-attribute
cells), and the IHP thin-oxide library run through the identical harness as
control. Pass/fail is parsed from the report database, never the exit code.

**DRC.** 781 raw violations after the first retarget were driven to zero
cell-rule items (density-only residue, same class as the control). One
defect class survived the original harness because it could not express it:
the retarget left each cell's **rail-tap contacts** at cell-specific x, and
in a placed block — where *different* cells share every rail — partially
overlapping taps merged into 0.19–0.32 µm bars: ~19 000 `Cnt`/`CntB`
markers on the first `spi_slave` signoff. `work/fix_rail_contacts.py`
re-tiles every rail tap onto the site-centred 0.48 µm grid, which both the
FS row flip and placement's x-mirror preserve, with in-code guards for
implant polarity, enclosures, gate clearance, contact spacing and tap
continuity (1 134 → 1 810 rail contacts).

**N-wells: two rule sets, one layout.** The retarget placed the N-well for
the *digital* rule set — `NW.c1.dig`, 0.31 µm enclosure of HV p-active,
which the IHP rulebook grants inside a `DigiBnd` marker and which the
KLayout maximal deck verifies clean. Magic's SG13G2 tech has no DigiBnd
concept at all and applies the *analog* rules unconditionally, so it
flagged every cell: 1 128 `NW.c1` plus 9 `NW.e1` on a placed counter.
Measured against the strict rule the library was short by exactly **25 nm
in 65 of the 68 cells drawn at that point** (210 nm in `mux4_1`, 215 nm in
`slgcp_1`, both of which reach further down); the 16 cells drawn afterwards
were built to the strict rule from the start.

That margin is recoverable in the well layer alone, so rather than wait on
the tool, `work/fix_well_nwc1.py` rebuilds only the N-well: bottom edge
2.625 → 2.570 µm library-wide, a halo around each cell's PMOS active that
forces the two deeper jogs automatically, minus halos around NMOS active
and p-taps for `NW.d1`/`NW.f1`, and the lateral overhang widened
0.24 → 0.62 µm so the outermost cell of a row is enclosure-clean without
a neighbour's merged well (that last point also removed the block-edge
`NW.e1` flags). Every rule is asserted per cell in the generator with
corner-inclusive square sizing, the worst case of the euclidian deck
rules.

**Nothing about the devices changes.** The well is not a device terminal,
characterization runs on the schematic netlist, and the HV PSP model cards
carry no well-proximity parameters — so no re-characterization was needed,
and only the GDS differs. The result: Magic reports **0 `NW.*`** on the
abutted array and both KLayout decks stay clean, i.e. the layout now
satisfies the strict and the relaxed interpretation simultaneously. The
residual Magic flags (`Cnt.c` contact-overlap, wide-metal `M1.e`) are
tool-interpretation differences on geometry both KLayout decks accept.
The tool gap itself was reported upstream as IHP-Open-PDK issues #1106
(the modular KLayout deck implements neither `NW.c1` nor `NW.c1.dig`, so
its "0 errors" was silent on this rule) and #1107 (Magic lacks the DigiBnd
relaxation).

**LVS.** All 84 cells match, re-run in full after the re-tiling. The
four device-less `fill_*` cells need the runner's own
`--ignore_top_ports_mismatch` relaxation — IHP's own fill cells fail the
identical flow the same way. LVS caught five defect classes dimensional
checks could not (merged channels, collapsed notch devices, mis-paired
fingers, a dropped substrate tie, stale diode geometry), which is why the
per-cell sweep runs after every layout change.

**Block-level validation.** The `spi_slave` IP, in two variants, was
synthesised, placed and routed with this library through
LibreLane/OpenROAD at 100 MHz on ~354 × 400 µm dies. Both close timing
with zero setup/hold violations at the characterised corner, pass routing
DRC, antenna and Netgen LVS in the flow, pass gate-level simulation of the
routed netlist (all four SPI modes on the all-modes variant), and pass the
**full IHP signoff deck** with zero geometry violations — only the 8
chip-level density/filler markers a filled die resolves at tapeout. The
flow settings this takes (flip-flop mapping onto `sdfbbp_1`, excluded
cells, Metal1 routing, rails-only fillers) are documented in the
`spi-slave-ihp` repository.

---

# Liberty characterisation

`lib/sg13g2_stdcell_hv_typ_3p30V_25C.lib`,
`lib/sg13g2_stdcell_hv_fast_3p60V_m40C.lib` and
`lib/sg13g2_stdcell_hv_slow_3p00V_125C.lib` are produced with **CharLib**
against the shipped, layout-synchronised SPICE netlist on the PSP103/OSDI
models — 25 839 combinational simulations plus a 2 962-task sequential
run: 600 delay/slew tables over 66 cells (52 combinational, 9 flip-flops,
5 latches), none empty. The 6 tri-states add 60 more from the direct
measurement of section 7.2, for 660 tables over 72 cells in the shipped
file. Grids are the thin-oxide grids rescaled by the
measured 2.66× delay / 2.20× capacitance ratios; boolean functions are
translated from the thin-oxide Liberty and checked by truth-table
equivalence. Stock CharLib needed five committed tool workarounds (OSDI
shim, `ngspice-shared` backend, case-insensitive supply lookup, Liberty
syntax post-pass) and — for sequential cells, which stock CharLib cannot
characterise at all — custom clk→Q and setup/hold-bisection procedures
with a c2q-degradation pass criterion (`work/seq_delay_procedure.py`).

The shipped file is verified **as data** by `work/verify_lib.py`:
structure (660/660 tables populated), cross-view (all pins exist in the
CDL), physical (every `area` equals the drawn boundary to 1 nm²),
monotonicity along the load axis (2 141/2 142 series, one documented
pessimistic waiver: `xnor2_1` glitch latching), input capacitance against
an independent both-rails measurement (6.44 vs 5.87 fF, 9.7 % — this
check caught a 6.8–7.5× Miller defect in CharLib's default procedure),
and sequential arcs (14/14 cells: delay + setup + hold present, nothing
pinned at search bounds). A hand-written transient at a table corner
agrees to 0.3 %.

An independent characteriser, **lctime**, was run over eight cells on the
same grids and models: in the region STA exercises (real loads, slews
< 1 ns) the two agree to a median 2.9 % on delays and 0.0 % on
transitions; every disagreement region traces to a stimulus convention,
and a direct measurement sides with the shipped table (+0.15 % vs −19 %
at the probe point). lctime's input capacitance (+52 %) also corroborates
validating Cin against a direct measurement, not a characteriser.

`tiehi`/`tielo` are present in the Liberty without timing arcs (a constant
output has none) and with directly measured leakage —
`work/tie_leakage.py` applies the sequential cells' settled-tail average
to the tie netlists (0.011 / 0.013 nW), so no number is borrowed from
`inv_1`.

## Drive limits, and why their absence is not benign

CharLib emits no `max_capacitance` or `max_transition` at all, and the
first three revisions of this library shipped without them. That is worse
than a missing convenience. OpenSTA answers "no limit" for every pin, so a
flow's max-cap and max-slew checks pass **vacuously** — reporting zero
violations because there is nothing to violate — and OpenROAD's TritonCTS
dereferences an empty buffer-selection result and **segfaults** during
clock-tree synthesis, which is how the gap surfaced.

`work/finalize_lib.py` derives the limits from the characterization
itself rather than copying the thin-oxide numbers: a pin may not be asked
to drive more load than its tables cover, nor to accept a slower edge than
was characterized. Per output pin `max_capacitance` is the top of its load
axis (0.66–10.56 pF by drive class), per pin `max_transition` the top of
the slew axis it was characterized against (6.67 ns combinational,
3.36 ns sequential), with library defaults following the thin-oxide
convention of weakest-drive / slowest-edge. The crash is reproducible on
demand and was reported upstream with a minimal two-flop test case
(OpenROAD issue #11165): a liberty without limits should produce a
diagnosable error, not a signal 11.

## The cells CharLib cannot reach

Nine cells are drawn but were never characterized, and the reason is a
tool limitation in each case rather than a property of the cell:
`gen_charlib_config.py` skips the two statetable clock gates (CharLib has
no statetable input form) and the device-less/no-output cells, while the
six tri-states are *configured* but silently produce nothing — CharLib has
no high-impedance concept anywhere in its schema or code, so it emits an
empty result without an error. lctime is no substitute: it can carry a
`three_state` attribute but deliberately pins the enable and skips exactly
the enable arcs one needs.

They are therefore measured directly against the shipped netlists, the
same way the tie and sequential cells already are.

**`sighold`** (bus holder) is the simplest and is complete: it has no
timing arcs at all — the thin-oxide model is `driver_type : bus_hold`
plus capacitance and per-state leakage — so it needs leakage
(0.0118 nW / 0.0224 nW, ~10⁴ below the thin-oxide cell, the same
thick-oxide ratio the tie cells show) and a pin capacitance. The
capacitance is the interesting part: charge integration, the library's
method for ordinary gate pins, is **invalid here**. On a bus holder the
integral is dominated by the keeper fighting the driver, so it grows
monotonically with the driving edge rate — measured 30.5 fC at a 0.2 ns
edge to 86.4 fC at 5 ns, a 2.8× spread — and is a property of the driver,
not the cell. A 1 MHz small-signal measurement near the rails gives
0.00367 pF with a 7 % spread across bias; the keeper fight-back charge is
recorded separately rather than folded in. The same reasoning explains the
thin-oxide cell's 2.8× rise/fall capacitance asymmetry as an artifact of
its measurement, so the HV cell ships equal rise and fall values.

**The six tri-states** are characterized by
`work/char_tristate/char_tristate.py` and
are in the shipped Liberty. Each carries three arc classes rather than
one: the `combinational` data arc, plus `three_state_enable` and
`three_state_disable` measured into and out of a floating node defined by
a 1 GΩ mid-rail keeper — the construct the functional suite already uses
for its 12 Hi-Z checks. The harness is calibrated by re-measuring a
shipped cell's pin capacitance through the same code path (0.46 % against
the shipped value), and the combinational arcs land inside the library's
2.66× delay band.

The disable arc required a change of measured quantity, not just of
threshold. Waiting for a released output to cross a voltage threshold is
not physically measurable: once the driver lets go, only the keeper moves
the node, so the answer is $0.2\,RC \approx 0.5$ ms and scales with the
load. The thin-oxide library cannot have measured it that way either —
its disable tables are exactly load-independent, differing by a 1 fs
monotonicity epsilon. What is measured here is the drive current going
away: from `TE_B` at 50 % to $|I_Z|$ falling through half its on-state
value, which is load-independent by construction and needs no synthetic
epsilon. Section 10.2 of the companion characterization report gives the
derivation and the ratio tables.

**The two clock gates** are measured by `work/char_clockgate.py`: a
`CLK`→`GCLK` propagation arc, `setup_rising`/`hold_rising` on the enable
pins — the form the sequential bisection procedure already emits — and a
`min_pulse_width` constraint on the clock pin, bisected until the gated
output loses its pulse, alongside the statetable, internal state pin and
`state_function` metadata that make an integrated clock gate usable. With
these the Liberty covers **all 84 cells**.

The min-pulse-width measurement is worth one caution, because its first
result was wrong in a way that looked right. Under machine load the
trials time out; a timed-out trial returns no measurement, the bisection
predicate reads that as "failed at every width", and the search then
returns its own upper bound. The first fragment carried a 48 ns minimum
pulse width — 50× the cell's own CLK→GCLK delay — which would have told
STA that every realistic clock pulse is too narrow. The generator already
recorded a `bracketed` flag for exactly this case but emitted the value
anyway; it now refuses to, and names the offending points. All 16 points
are bracketed in the shipped data, 0.46–1.11 ns and monotone in input
slew.

`lgcp_1` and `slgcp_1` come out with identical min-pulse-widths, which is
expected rather than suspicious: their CLK→GCLK delays differ only in the
4th–6th digit and their clock-pin capacitances in the 7th — the scan leg
sits in the enable path, not the clock path — so the true difference is
far below the 0.01 ns bisection tolerance and both converge to the same
midpoint. That the two simulations are genuinely distinct is visible in
the delay and capacitance data.

Both cells nevertheless stay in the exclude lists, as the thin-oxide SCL
keeps its own: an integrated clock gate is instantiated deliberately, not
inferred.

## One deliberate omission: switching power

This library ships **no `internal_power` tables for any cell** — the
characterization was scoped to timing and leakage. The special-cell work
above kept that scope rather than adding power for nine cells alone: a
library where only the tri-states and clock gates carry switching power,
and every other cell reports zero, produces power analysis that is worse
than uniformly absent because it looks complete. It is recorded as a
library-level limitation instead.

---

# LibreLane integration

A library that a digital flow cannot load is not usable, and until rev. 5
this one could not be loaded: LibreLane rejects any `STD_CELL_LIBRARY`
without a `libs.tech/librelane/<name>/` directory, and the PDK-level
`config.tcl` hardcodes the thin-oxide liberty **filenames** in its `LIB`
dict while validating every path eagerly. The library now ships the
missing pieces.

**The SCL** (`librelane/`, installed as
`libs.tech/librelane/sg13g2_stdcell_hv/`): `config.tcl` with the
`CoreSiteHV` site (0.48 × 7.14) and the HV driving, tie, fill, decap,
diode and CTS cells; `tracks.info`; latch, mux and tri-state techmaps;
and both exclude lists, which mirror the thin-oxide ones. `PDN_RAIL_WIDTH`
stays 0.44 µm — the VSS rail is 0.44 µm symmetric about the row edge and
the VDD pin shape, though taller, fully covers a 0.44 µm strap.

**The PDK config** gets a conditional block for
`STD_CELL_LIBRARY == sg13g2_stdcell_hv` (every characterized corner is
registered; `*_typ_3p30V_25C` is the default, `VDD_PIN_VOLTAGE` 3.30), and the library ships a copy of the shared
`sg13g2_tech.lef` because that config globs it per-SCL and a Tcl `glob`
errors rather than returning empty. Both patches are idempotent.

**Flip-flops now map natively.** Before all 84 cells were drawn, the only
flop with both a liberty and a layout view was the scan cell
`sdfbbp_1` — which `dfflibmap` cannot target, because its `next_state`,
`(SCE & SCD) | (!SCE & D)`, is not a plain D function. The interim
solution was `sdfbbp_map.v`, a techmap covering every posedge Yosys
flip-flop type on the scan cell, with the scan mux recycled as the enable
mux for `$_DFFE_*` and sync resets folded into the D leg; all 23 clocked
mappings were proven equivalent to the Yosys cell semantics with
`equiv_induct`. With the `dfrbp`/`dfrbpq`/`sdfrbp`/`sdfrbpq` layouts drawn
it is no longer needed — `dfflibmap` maps directly, as in the thin-oxide
flow — and it remains only as a documented opt-in for DFT flows that want
every flop on the scan cell: drop `sg13g2_hv_sdfbbp_1` from
`synth_exclude.cells` and set, at design level,
`SYNTH_EXTRA_MAPPING_FILE: pdk_dir::libs.tech/librelane/sg13g2_stdcell_hv/sdfbbp_map.v`
(LibreLane does not let a PDK set that variable).
Removing it cut sequential area on the reference counter by **31 %**
(1 699.89 → 1 178.96 µm²), the tie-off overhead the workaround carried.

One lesson worth recording, because it cost two debugging rounds: a
techmap applied *after* the synthesis pass's own lowering must write its
glue as fine-grained gates (`$_NOT_`, `$_AND_`, `$_OR_`). Inline
expressions such as `~E` create coarse cells at a point where no later
pass will lower them, and they reach the netlist unmapped. The
thin-oxide latch map has the same latent issue; both HV maps avoid it.

**A view can be present and still be missing.** The spice view was absent
from the first three revisions of the upstream PR even though the
generator wrote it and the install script copied it every time: the PDK
repo's root `.gitignore` carries `*.spice`, and its `libs.ref/.gitignore`
re-includes only the `spice/` *directory*, not the file inside it, so
`git add` skipped it silently. The thin-oxide library's own spice view
predates that rule and is already tracked, so nothing complained — and
the failure reproduced only for someone cloning the branch, never for
anyone testing an installed tree, which is why every local gate passed.
`make_pdk_pr.py` now asks `git check-ignore --no-index` about every
installed file and fails the run if any would be invisible; the check
reproduces the defect against the unpatched `.gitignore` and passes 195
files against the fixed one.

**Tri-states are wired too**, now that they carry timing:
`SYNTH_TRISTATE_MAP` maps Yosys' `$_TBUF_` onto `sg13g2_hv_ebufn_2` and
`TRISTATE_CELLS` lists both footprints, mirroring the thin-oxide SCL.

**Block validation.** The reference 8-bit counter from the IIC-JKU
SG13G2 AMS chip template hardens end to end on the shipped library with
no design-level liberty or corner overrides: flops mapped natively, zero
unmapped cells, CTS clean, max-cap/max-slew checks non-vacuous and
passing, LVS clean through the auto-derived `CELL_SPICE_MODELS`, and
**both** KLayout and Magic DRC at zero.

A second design exercises the tri-states specifically — two registered
sources driving one shared internal bus, so synthesis must infer
`$_TBUF_` and STA must time the enable arcs. It hardens equally clean:
16 `sg13g2_hv_ebufn_2` instances, zero unmapped cells, Magic DRC 0,
KLayout DRC 0, LVS 0, routing DRC 0, antenna 0, and zero max-slew and
max-cap violations against real limits.

---

# Verification summary

| Check | Method | Scope | Result |
|---|---|---|---|
| Parasitic formulas | recompute vendor `as/ad/ps/pd` | all 924 thin-oxide devices | PASS, worst error 3.75×10⁻⁴ |
| Combinational logic | ngspice vs thin-oxide golden | 60 cells, 452 vectors, 12 high-Z states | **PASS** |
| Sequential logic | ngspice, clocked walk from reset | 16 stateful cells, 400 samples | **PASS** |
| Three-view consistency | symbols vs SPICE vs CDL | 84 cells, 920 devices | **PASS** |
| DRC, padded array | PDK deck, fixed invocation | **84 cells** | **0 cell rules**; 7 density items |
| DRC, shared-rail array | same deck, true-pitch mixed/mirrored rows | **84 cells** × 4 rows | **0 cell rules**; density only |
| DRC control | identical harness on IHP `sg13g2_stdcell` | 84 cells | 0 cell rules, 6 density |
| DRC, Magic strict analog rules | `drc(full)`, euclidean, abutted array | **84 cells** | **0 `NW.*`**; `Cnt.c`/`M1.e` tool-interpretation only |
| LVS | PDK deck, per cell, after the well rebuild | **84 cells** vs CDL | **84/84** |
| LEF | klayout parse-back + pin sets vs CDL | **84 macros** | PASS, on-grid |
| P&R block validation | LibreLane `spi_slave` ×2 + full signoff deck | ~354 × 400 µm, 100 MHz | all clean; signoff **0 geometry violations**, 8 density markers |
| Liberty structure/views/areas | `verify_lib.py` 1–3 | **84 cells**, 668 tables | PASS, **all areas measured**, exact to 1 nm² |
| Liberty monotonicity | `verify_lib.py` 4 | 2 142 delay series | 2 141 + 1 documented waiver |
| Liberty Cin | vs both-rails reference | `inv_1` | 6.44 vs 5.87 fF (9.7 %) |
| Liberty delay point-check | hand-written transient | table corner | 0.3 % |
| Independent characteriser | lctime, 8 cells, 3 132 points | STA region | median 2.9 % / 0.0 % |
| Sequential arcs | `verify_lib.py` 6 | 14 flip-flops/latches | **14/14 clean** |
| Site geometry | boundary scan | all **84 cells** | 7.140 µm, widths on 0.48 µm site |
| Tie-cell leakage | `tie_leakage.py` settled-tail average | `tiehi`/`tielo` | 0.011 / 0.013 nW, in the Liberty |
| Pin track alignment | `grid_align_pins.py --apply` + full re-signoff | 12 of 25 off-track pins widened; 11 of 282 remain | DRC 0 cell rules ×2, LVS clean |
| PDK dev-branch re-run | IHP-Open-PDK `dev` decks (KLayout 0.30.9) | both DRC arrays, 84-cell LVS | main tables **clean**, LVS **84/84** |
| New-cell signoff gate | `cell_verify.py` per candidate before merge | 18 generated cells | **18/18 PASS** (LVS + both decks + Magic + structure + pins) |
| Liberty drive limits | `verify_lib.py` 7 | 79 output pins | present on every pin; TritonCTS crash resolved |
| Liberty special classes | `verify_lib.py` 8 | tri-state / ICG / bus-hold constructs | complete-construct check |
| LibreLane block run | reference counter, no design-level overrides | RTL→GDS | flops native, DRC **0/0**, LVS clean |
| LibreLane tri-state run | shared-bus design inferring `$_TBUF_` | RTL→GDS | 16 `ebufn_2`, DRC **0/0**, LVS 0, slew/cap 0 |
| Git visibility of views | `git check-ignore --no-index` in `make_pdk_pr.py` | 195 installed files | all trackable |

The library is submitted upstream as
[IHP-Open-PDK PR #1103](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1103)
(draft): `libs.ref/sg13g2_stdcell_hv` following the dev-branch layout, a
two-line `xschemrc` registration, and an optional KLayout autorun macro,
with the cell-set choice, the macro, and xschem view-machinery
unification flagged as maintainer questions. `work/make_pdk_pr.py`
assembles and verifies the contribution against a checkout.

---

# Known limitations

* **No switching power.** The library ships `leakage_power` but no
  `internal_power` for any cell (section 7.3). Dynamic power analysis will
  see only leakage.
* **Clock gating is available but not automatic.** `lgcp_1` and
  `slgcp_1` carry the full ICG model, but an integrated clock gate is
  instantiated deliberately rather than inferred, so both remain in the
  exclude lists exactly as the thin-oxide SCL keeps its own. Enabling it
  needs two design-level variables, documented in the exclude list.
* **Three corners** (typ 3.3 V/25 °C, fast 3.6 V/−40 °C, slow 3.0 V/125 °C);
  sequential leakage is a
  single-settled-state number; the delay cells' ratios shift with the
  450 nm minimum; the decaps store less per unit area.
* **Timing is schematic-characterized.** Device sizes match the drawn
  layout exactly (LVS-proven per cell), but no parasitic extraction is
  folded back into the tables; a PEX-based re-characterization is the
  natural next step.
* **11 signal pins remain off the vertical Metal1 track grid** and cannot
  be widened within `M1.b` (12 others were). Route with `RT_MIN_LAYER`
  Metal1, or expect the router to jog.
* **Not silicon-proven.** Everything here is simulation against the PDK
  models. The library has now been independently re-tested by a third
  party — RTL-to-GDS on the upstream PR, reproducing the DRC, LVS, STA and
  mapping results — but it has not been fabricated.

---

# Reproducing the library

```sh
cd /foss/designs/sg13g2_stdcell_hv/work

python3 gen_hv_lib.py            # netlists, schematics, symbols, Verilog
python3 gen_gallery.py           # gallery sheet
python3 layout_retarget.py       # gds/ (66 cells; prints the 18 skips)
python3 gen_tie_cells.py         # + tiehi / tielo
python3 flop_pilot/gen_seq.py    # the 8 flip-flops (per-cell y-map recipe)
# latches, ebufn drives, lgcp_1, sighold: cell_dev/*/gen_*.py
python3 cell_verify.py <cell>.gds  # gate every generated cell before merge
python3 fix_rail_contacts.py     # rail taps onto the site-centred grid
python3 sync_netlist_widths.py   # SPICE + CDL follow the drawn geometry
python3 fix_well_nwc1.py         # N-wells to the strict analog HV rules
python3 gen_lef.py               # lef/ (CoreSiteHV + 84 macros)
python3 make_drc_top.py          # padded two-row DRC context
python3 make_shared_rail_rows.py # shared-rail mixed-row DRC context

python3 verify_logic.py; python3 verify_seq.py; python3 verify_sch.py
./run_lvs.sh                     # per-cell LVS, 84/84
# DRC: PDK run_drc.py on drc/drc_top.gds and drc/shared_rail.gds
#      plus magic drc(full) on drc_top.gds for the strict N-well rules

# Characterization is per PVT corner (corners.py); one command per corner:
./run_corner.sh typ              # or fast | slow
#   CharLib for what it can express, the project's own procedures for the
#   sequential cells, direct ngspice measurement for the cells no
#   characteriser models (tri-states, clock gates, bus holder, tie cells),
#   then drive limits, areas and the data gate -- in that order, because
#   the drive limits are derived from the table axes of whatever is
#   already merged.
python3 lctime_compare.py        # independent characteriser cross-check

python3 make_pdk_pr.py --pdk <IHP-Open-PDK checkout>   # assemble the PR
```

Every number in this report is reproducible from these scripts; the
`work/` directory and the `README.md` are the provenance of record.
