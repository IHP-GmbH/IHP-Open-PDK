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

## Excluded Device Groups (Not in CMOS5L)

- **RFMOS**: RF MOSFET devices
- **BJT**: HBT bipolar transistors (npn13G2, npn13G2L, npn13G2V)
- **CAP**: S-Varicap requires nBuLay (forbidden in CMOS5L)
- **MIM**: MIM capacitors (cap_cmim, rfcmim)
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
# Run all device LVS tests
make test-LVS-main

# Run specific device group
make test-LVS-MOS
make test-LVS-RES
make test-LVS-TAP
make test-LVS-DIODE
make test-LVS-ESD

# Run switch test (quick sanity check)
make test-LVS-switch

# Run standard cell regression (requires testcases to be generated first)
make test-LVS-cells

# List available device groups
make list-devices
```

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
