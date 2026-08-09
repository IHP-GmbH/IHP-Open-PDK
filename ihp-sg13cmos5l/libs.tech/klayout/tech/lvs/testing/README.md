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
| IND | Custom inductors (inductor2, inductor3) | Supported |

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
- `m` is not compared either, despite being declared `is_primary=true`: the
  SPICE reader takes it as the standard device multiplier rather than mapping it
  onto the class parameter of the same name, so a netlist declaring `m=2`
  against a single placement still matches. That matters because `m` is the only
  token beyond `w`/`l` that the xschem symbol's `lvs_format` emits.
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
- **In deep mode, cap_cmomi geometry below the top cell produces no circuit at
  all**, and the empty netlist then matches any schematic. Extraction is not what
  fails: the `.lvsdb` still carries the device abstract with its terminal
  geometry, identical to the flat run's, and no marker is ever rejected. What is
  missing is the circuit, so the devices are never instantiated. Every cap_cmomi
  layout here that is a single flat cell deep-extracts correctly; wrap one in a
  parent cell and the same shapes drop to zero circuits and zero nets. It is not
  `simplify`, not a missing `--topcell`, and not deep mode in general, since the
  `sg13_lv_nmos` switch testcase wrapped the same way still extracts its devices.
  Case 12 of the checks suite records it. Deep is not the default for
  `run_lvs.py` or for the regression, so nothing in CI runs cap_cmomi that way,
  but a user who does gets a clean run that checked nothing. Cause not diagnosed,
  see [#91](https://github.com/IHP-GmbH/ihp-sg13cmos5l/issues/91).

`make test-LVS-cmomi-checks` holds all of the above as executable cases, so any
change in this behaviour surfaces as a verdict change rather than silently
altering what LVS accepts.

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

# Run manual tests (ESD ptap, implicit connections, SRAM support, cap_cmomi)
make test-LVS-manual

# Run the cap_cmomi checks on their own (2 FAIL + 2 ERROR + 8 PASS, all expected)
make test-LVS-cmomi-checks

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
| cap_cmomi_checks | cap_cmomi detection limits, see above | 2 FAIL + 2 ERROR + 8 PASS |

Every one of the 12 cases in `cap_cmomi_checks` declares the verdict it expects,
and the suite fails if a case stops behaving the way it is recorded to behave.
ERROR means the extractor rejected the layout and the run aborted before any
comparison ran. The eight passing cases are as load bearing as the four
detections: they record what `cap_cmomi` matching does *not* check, which would
otherwise only be visible by reading the rule decks.

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

# Ignore top-level port mismatches (floating-bulk SRAM)
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

The cap_cmomi layouts are the exception: they are generated from the SG13_dev
PCell by `create_cap_cmomi_testcases.py` rather than drawn by hand, and the
results are checked in so the regression does not need a working PCell library
at test time. Regenerate them after a PCell change with

```bash
KLAYOUT_HOME=$(mktemp -d) KLAYOUT_PATH=<repo>/libs.tech/klayout \
  klayout -zz -r create_cap_cmomi_testcases.py
```

`KLAYOUT_HOME` matters: a user KLayout home with ihp-sg13cmos5l installed
registers its own `sg13cmos5l` technology whose base path points at that
installation, and the PCell is then taken from there instead of from this tree.
