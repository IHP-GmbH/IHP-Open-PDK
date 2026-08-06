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

# Run the cap_cmomi checks on their own (3 FAIL + 2 ERROR + 8 PASS, all expected)
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
| cap_cmomi_checks | cap_cmomi detection limits, see above | 3 FAIL + 2 ERROR + 8 PASS |

Every one of the 13 cases in `cap_cmomi_checks` declares the verdict it expects,
and the suite fails if a case stops behaving the way it is recorded to behave.
ERROR means the extractor rejected the layout and the run aborted before any
comparison ran. The eight passing cases are as load bearing as the five
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
