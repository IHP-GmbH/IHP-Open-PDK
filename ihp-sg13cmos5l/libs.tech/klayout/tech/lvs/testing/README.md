# SG13CMOS5L LVS Testing

This directory contains the LVS regression testing infrastructure for the SG13CMOS5L PDK.

## Supported Device Groups

| Device Group | Description | Status |
|-------------|-------------|--------|
| MOS | NMOS/PMOS transistors (LV, HV) | Supported |
| DIODE | Antenna diodes (dantenna, dpantenna) | Supported |
| RES | Resistors (poly, silicide, metal M1-M4, TM1) | Supported |
| ESD | ESD protection devices (diodevdd/vss only) | Supported |
| TAP | Substrate/well taps | Supported |
| CAP | MoM capacitor (cap_cmomi, Metal1-Metal4) | Supported (approximate model, pending silicon) |
| CAP_CMOMF | MoM fringe capacitor (cap_cmomf, Metal1-Metal4) | Supported (approximate model, pending silicon) |

`cap_cmomf` sits in its own group rather than in CAP because it is registered
from a cmos5l-local `cap_cmomf_extraction.lvs`: this runner derives the group
from the extraction deck's filename and matches it against the testcase
directory, and the shared `cap_extraction.lvs` where the device belongs is a
symlink into the sibling ihp-sg13g2. The two merge once cap_cmomf is
upstreamed. The device is recognised by its own marker, `Recog.momf` (99/40),
because `cap_cmomi` owns `Recog.mom` (99/39) by design in the shared deck.

Inductors are recognised, not generated: CMOS5L ships no inductor PCell, so
a coil is drawn by hand and marked up per section 6.6 of
`SG13CMOS5L_os_layout_rules.pdf`. The winding goes on TopMetal1 and the
underpass crossings on Metal4/Metal3, which is one level below the SG13G2
TopMetal2/TopMetal1 pair. `sg13cmos5l.lvs` says so via `ind_wind`/`ind_cross`;
the rule decks themselves stay shared with G2.

Besides the `IND`, `IND:pin` and `IND:text` markup the section describes, the
device also needs a text label matching `inductor2*` or `inductor3*` on the
general text layer (63/0) inside the `IND` box, or nothing is extracted.

## cap_cmomi comparison semantics

`cap_cmomi` is matched **topologically**, and it is worth knowing exactly what
that leaves unchecked before trusting a green run on a real block.

The rule decks that decide all of this (`custom_mom_extractor.lvs`,
`custom_mim_extractor.lvs`, `cap_cmomi_connections.lvs`) are symlinked into
`ihp-sg13g2`, so the behaviour recorded here is shared with that PDK and arrives
on this side when `.github/ihp-sg13g2.ref` is bumped. The metal band is the one
difference that matters: this PDK stops at Metal4.

`custom_mom_extractor.lvs` builds the device on `DeviceCustomMIM`, which adds
`w` and `l` with `is_primary=false`, so neither is compared. `A` and `P` are
primary but the extractor never sets them and the CDL never carries them, so
both sides hold 0. `m` is 1 on both sides. The values the extractor does record
for `w`/`l` are the `Recog.mom` bounding box **including the feed pads**, so a
nominal 5x5 um device extracts as `w=5.09u l=6u` and never equalled the
schematic value in the first place.

What follows from that:

- `mmin`, `mmax` and `feed` reach the SPICE reader and are then dropped. They
  are not device parameters. A cap_cmomi built on `mmin=3..mmax=4` has the same
  footprint, the same marker bounding box and its pins on the same Metal4 as
  one built on `mmin=1..mmax=4`, so **a device on the wrong metal band matches
  silently** while its capacitance differs by roughly 2x. Deriving the band from
  the geometry is not a fix: `metalN.and(marker)` cannot tell the device's own
  metal from routing that happens to cross over it, so it misreports as soon as
  anything is routed above the cap. Doing this properly needs the PCell to
  encode the band in the markup.
- `m` is not compared either, despite being declared `is_primary=true`, and the
  reason is a substring test. `CustomReader` intercepts every `C` element
  (`CUSTOM_READER` in `globals.lvs`), so the default SPICE delegate never runs,
  and `map_capacitor_params` sets `m` only `if model.downcase.include?('mim')`.
  `cap_cmomi` does not contain `mim`, so the value is read off the card and
  dropped, and both sides keep the class default of 1. A netlist declaring `m=2`
  against a single placement matches. That matters because `m` is the only token
  beyond `w`/`l` that the xschem symbol's `lvs_format` emits. Anyone fixing this
  should look at that `'mim'` gate, not at multiplier handling.
- The capacitance itself comes from the ngspice/Verilog-A model, never from
  extraction, so LVS says nothing about whether the layout realises the C the
  schematic asked for.
- The two terminals **are** interchangeable for this device, unlike `cap_cmim`.
  `CapMomExtractor` picks the two ports by geometry and never reads their pin
  names, so the order it produces is arbitrary: for `double` it follows the
  instance orientation, and for `same` the metal index decides and puts the
  PCell's MINUS on pin 1. Enforcing that order only produced false mismatches,
  notably for a mirrored placement.
- The extractor requires exactly two pin ports under a marker and otherwise
  reports an **extraction error**, so the run aborts before the comparison and
  produces no verdict (a partial extracted netlist is still written). Two
  cap_cmomi whose `Recog.mom` markers touch form one cluster with four ports and
  take out **both** devices. This used to be a `logger.info`, and if the cell
  held nothing else the emptied circuit dropped out of the layout netlist and
  the comparison then matched any schematic at all.
- `feed='none'` still emits two pins, so an array with no feed structure, which
  is not a usable capacitor, extracts as an ordinary cap_cmomi.
- **In deep mode, a layout whose every cap_cmomi sits in a sub-cell with no net
  crossing that cell's boundary extracts nothing.** The netlist comes out empty
  and the comparison has nothing left to compare. Extraction itself is not what
  fails: the `.lvsdb` still carries the device abstract with its terminal
  geometry, identical to the flat run's, and no marker is ever rejected.

  This is recorded, not explained. What is measured, and only this: case 12 is
  that layout and it fails; case 13 is the same hierarchy with one Metal4 strap
  drawn in the top cell, so a single net crosses a boundary, and it extracts both
  caps and gets both verdicts right. A third cap in its own never-connected cell
  beside two strapped ones still extracts, so one isolated cap is not enough to
  trigger it. It is not `simplify` (`--no_simplify` changes nothing), not
  `--top_lvl_pins`, not a missing `--topcell`, and writing the schematic
  hierarchically with a subcircuit named after the sub-cell does not help either.

  It is not specific to `cap_cmomi`. `cap_cmomf` is a different geometry with a
  different marker, sharing only the extractor, and it empties the same way on
  the same construction; see the section below. That is two devices, not a
  proof, but it is enough to stop looking at the cap_cmomi decks for the cause.

  An empty layout netlist used to be reported as a match, since `compare` had no
  pair left to compare; the deck now refuses that (see below). The extraction
  hole itself is open, so deep mode still cannot verify such a layout. See
  [#91](https://github.com/IHP-GmbH/ihp-sg13cmos5l/issues/91).
- **An empty layout netlist is no longer a match.** `sg13cmos5l.lvs` counts the
  devices hanging off the schematic's top circuit before `align`, and the devices
  left on the layout side after it, and reports a mismatch when the layout side
  is empty and the schematic side is not. Without it, any extraction that
  silently produced nothing ended in a green run, whatever the cause. The
  schematic count is scoped to the compared top on purpose: counting the whole
  file instead failed a device-free block, a filler or a routing-only cell,
  verified against a library netlist whose other subcircuits do hold devices.
  This is local to this PDK: the cap_cmomi rule decks are symlinks into
  `ihp-sg13g2`, but the comparison flow is not, and G2 at the pinned commit still
  reports a match on the same layout.

`make test-LVS-cmomi-checks` holds all of the above as executable cases, so any
change in this behaviour surfaces as a verdict change rather than silently
altering what LVS accepts.

## cap_cmomf comparison semantics

`cap_cmomf` is extracted by the same `CapMomExtractor` into the same
`DeviceCustomMIM` class as `cap_cmomi`, told apart by nothing but its
recognition marker, `Recog.momf` (99/40) against `Recog.mom` (99/39). Everything
the section above says about what the comparison does not check therefore holds
here too, and `make test-LVS-cmomf-checks` records it case for case: `w` and `l`
are not compared, `m` is not compared because of the `'mim'` substring gate in
`map_capacitor_params`, a device declared on the wrong metal band matches
silently, and a hierarchy with no net crossing a cell boundary extracts nothing
in deep mode. The band case costs more here than there: `cap_cmomf` runs from
0.372 fF/um2 on Metal1 alone to 1.287 on the full Metal1-Metal4 stack, so a
wrong band is a factor of three, not two.

Three things differ, and they are what the cmomf suite adds:

- **The two terminals are equivalent, and this PDK is what says so.** The shared
  `DeviceCustomMIM` declares the equivalence only when the device name contains
  `cmomi`, so `cap_cmomf` falls outside it. Without the equivalence, mirroring an
  instance is reported as a mismatch: the extractor sorts its two ports by x and
  never reads the pin names, and the PCell puts PLUS on the left edge, so a
  mirror exchanges the terminals for a circuit that did not change.
  `rule_decks/cap_cmomf_registration.lvs` adds `cap_cmomf` to the equivalence the
  same way it extends `PREFIX_MAP` and `CustomReader`, and case 6 of the suite is
  the mirrored layout that fails without it. Fold this into the g2 gate when
  `cap_cmomf` is upstreamed.
- **The marker split is load bearing and is tested.** Case 11 puts one
  `cap_cmomf` beside one `cap_cmomi` and requires exactly one device of each
  class. Sharing 99/39 would make a single geometry extract as both devices,
  which is the collision described in
  [#68](https://github.com/IHP-GmbH/ihp-sg13cmos5l/issues/68).
- **A shorted device reports as a missing one.** Tying the two plates together
  puts both terminals on one net, and KLayout drops such a device from the
  netlist entirely, so the run fails on the device count and the log never says
  the word short. Case 3 records that, because the failure it produces points
  somewhere else than the defect.

The extraction error a marker cluster with the wrong port count raises comes from
the shared g2 extractor, and its message names `cap_cmomi` and `Recog.mom`
whatever device is being extracted. Cases 4 and 10 are `cap_cmomf` layouts that
end in exactly that message.

`cap_cmomf` layouts are generated by `create_cap_cmomf_testcases.py`, the sibling
of the cap_cmomi generator and used the same way.

## Excluded Device Groups (Not in CMOS5L)

- **RFMOS**: RF MOSFET devices
- **BJT**: HBT bipolar transistors (npn13G2, npn13G2L, npn13G2V)
- **CAP (S-Varicap only)**: `sg13_hv_svaricap` requires nwell_iso (forbidden); the
  MoM `cap_cmomi` in the CAP group IS supported (see the table above). The MOS
  varactors `sg13_moscap_n/p` are excluded for now (no CMOS5L testcase yet).
- **MIM**: MIM capacitors (cap_cmim, rfcmim) require the forbidden MIM layer
- **IND**: Inductors (inductor2, inductor3)
- **Schottky**: Schottky diodes (require nBuLay)

## Excluded Devices (nBuLay dependency)

These devices exist in G2 rule decks but are excluded from CMOS5L testing
because they require nBuLay (32/0), which is forbidden per Layout Rules Section 3.2:

- `idiodevdd_2kv`, `idiodevdd_4kv` - ESD idiode via nwell_iso
- `idiodevss_2kv`, `idiodevss_4kv` - ESD idiode via nbulay_drw
- `nmoscl_2`, `nmoscl_4` - ESD NMOS clamp via nbulay_drw
- `sg13_hv_svaricap` - S-Varicap via nwell_iso
- `schottky_nbl1` - Schottky diode via nwell_iso

## Metal Stack

CMOS5L uses M1-M4-TM1 metal stack:
- Metal1, Metal2, Metal3, Metal4
- TopMetal1 (top routing layer)
- Via1, Via2, Via3, TopVia1

Excluded layers: Metal5, Via4, TopMetal2, TopVia2

## Running Tests

```bash
# Run all device LVS tests (switch + device regression)
make test-LVS

# Run specific device group
make test-LVS-MOS
make test-LVS-RES
make test-LVS-TAP
make test-LVS-DIODE
make test-LVS-ESD

# Run switch test (quick deep/flat sanity check)
make test-LVS-switch

# Run SVS regression (1 PASS + 2 expected FAIL)
make test-LVS-SVS

# Run manual tests (ESD ptap, implicit connections, SRAM support, both MoM caps)
make test-LVS-manual

# Run either cap checks suite on its own (3 FAIL + 2 ERROR + 8 PASS, all expected)
make test-LVS-cmomi-checks
make test-LVS-cmomf-checks

# Run standard cell regression (generates testcases then runs LVS)
make test-LVS-cells

# List available device groups
make list-devices
```

## Manual Tests

Manual tests validate advanced LVS features using CMOS-compatible testcases
(symlinked from G2, with local run scripts invoking CMOS5L's run_lvs.py):

| Test Suite | Description | Expected Result |
|-----------|-------------|-----------------|
| svs_testss | SVS flow: schematic-vs-schematic comparison | 1 PASS + 2 FAIL |
| esd_ptap | ESD structure with ptap | PASS |
| implicit_connections | SP6TCClockGenerator with implicit vdd net | PASS |
| sram_support | SP01 SRAM cell (deep mode, OAS format) | PASS |
| cap_cmomi_checks | cap_cmomi detection limits, see above | 3 FAIL + 2 ERROR + 8 PASS |
| cap_cmomf_checks | cap_cmomf detection limits, see above | 3 FAIL + 2 ERROR + 8 PASS |

Every one of the 13 cases in each suite declares the verdict it expects, and the
suite fails if a case stops behaving the way it is recorded to behave. ERROR
means the extractor rejected the layout and the run aborted before any
comparison ran. The eight passing cases are as load bearing as the five
detections: they record what the matching does *not* check, which would
otherwise only be visible by reading the rule decks.

The two suites carry the same count by coincidence rather than by design. They
overlap on what the shared extractor decides and diverge where the geometries
do: cap_cmomi spends three cases on its `feed` variants, cap_cmomf spends them
on a mirrored placement, its marker split against cap_cmomi, and a shorted
device.

## Cross-Verification

The `run_cross_verification.py` script validates that CMOS5L LVS produces
identical results to G2 LVS for all CMOS-compatible devices:

```bash
python3 run_cross_verification.py
```

This confirms that the forbidden layer check and CMOS5L branding do not
introduce regressions relative to the G2 rule decks.

## run_lvs.py CLI

The `run_lvs.py` script supports additional flags beyond basic LVS:

```bash
# Standard extraction + comparison
python3 run_lvs.py --layout=design.gds --netlist=design.cdl

# SVS flow: schematic-vs-schematic using pre-extracted layout netlist
python3 run_lvs.py --layout_netlist=extracted.cir --netlist=schematic.cdl --topcell=TOP

# Net-only extraction (no comparison)
python3 run_lvs.py --layout=design.gds --net_only

# Implicit net connections (for SRAM or custom cells)
python3 run_lvs.py --layout=design.gds --netlist=design.cdl --implicit_nets="VDD,VSS"

# Ignore top-level port mismatches. Needed by every testcase in this tree, not
# just the floating-bulk SRAM: none of the layouts carries net labels on the
# deck's label layers, so every top-level net stays anonymous and the strict
# port check would fail them all. run_regression.py passes it for every device.
python3 run_lvs.py --layout=design.gds --netlist=design.cdl --ignore_top_ports_mismatch
```

## Test Cases

Test cases are symlinked from the G2 PDK where compatible:
- `testcases/unit/mos_devices/` - Full symlinks from G2
- `testcases/unit/tap_devices/` - Full symlinks from G2
- `testcases/unit/esd_devices/` - Full symlinks from G2
- `testcases/unit/res_devices/` - Selective symlinks (excludes M5, TM2 resistors)
- `testcases/unit/diode_devices/` - Selective symlinks (excludes Schottky)
- `testcases/extraction_checking/` - Symlink to G2 (NMOS switch test data)
- `testcases/manual_tests/` - Data symlinks from G2, local run scripts

The two MoM capacitors are the exception: their layouts are generated from the
SG13_dev PCell by `create_cap_cmomi_testcases.py` and
`create_cap_cmomf_testcases.py` rather than drawn by hand, and the results are
checked in so the regression does not need a working PCell library at test time.
Regenerate them after a PCell change with

```bash
KLAYOUT_HOME=$(mktemp -d) KLAYOUT_PATH=<repo>/libs.tech/klayout \
  klayout -zz -r create_cap_cmomi_testcases.py
KLAYOUT_HOME=$(mktemp -d) KLAYOUT_PATH=<repo>/libs.tech/klayout \
  klayout -zz -r create_cap_cmomf_testcases.py
```

`KLAYOUT_HOME` matters: a user KLayout home with ihp-sg13cmos5l installed
registers its own `sg13cmos5l` technology whose base path points at that
installation, and the PCell is then taken from there instead of from this tree.
