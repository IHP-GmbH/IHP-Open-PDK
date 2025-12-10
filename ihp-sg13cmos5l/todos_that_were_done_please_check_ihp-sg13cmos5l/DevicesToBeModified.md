# Devices to be modified

## Completed

- [x] **sealring** - Modified to limit to Metal5
  - Removed TopMetal1, TopMetal2 from layers list
  - Removed TopVia1, TopVia2 from vias list
  - Removed TV1_size, TV2_size parameters
  - File: `ihp-sg13cmos5l/.../ihp/sealring_code.py` (modified copy)

- [x] **ViaStack (via_stack)** - Modified to limit to M1-M5 vias
  - Removed TopMetal1, TopMetal2 from layer choices
  - Removed TopVia1, TopVia2 from via list
  - Removed vt1_columns/rows, vt2_columns/rows parameters
  - Removed TopVia tech params (TV1_*, TV2_*, TM1_*, TM2_*)
  - File: `ihp-sg13cmos5l/.../ihp/via_stack_code.py` (modified copy)

- [x] **bondpad** - Modified to limit to Metal5
  - Changed topMetal parameter from ['TM1', 'TM2'] to ['5']
  - Changed bottomMetal parameter from ['1'-'5', 'TM1'] to ['1'-'4']
  - Removed TV1/TV2 tech params
  - Simplified layer lists to M1-M5 only
  - Removed all TopVia via size handling
  - File: `ihp-sg13cmos5l/.../ihp/bondpad_code.py` (modified copy)

- [x] **SVaricap** - No modification needed
  - Uses only M1 + base device layers (Activ, GatPoly, nSD, pSD, NWell, etc.)
  - All layers already in slim PDK
  - File: `ihp-sg13cmos5l/.../ihp/SVaricap_code.py` (symlink to full PDK)

## Not Applicable

- [N/A] **GuardRing** - Not a standalone device
  - Guard ring is a layout technique used within other devices (rfCMiM, rfMOSFET)
  - No separate PCell exists in full PDK
  - No action required

## Additional Devices Added

- [x] **rsil** - Silicided resistor (CMOS-compatible, M1-only)
  - File: `ihp-sg13cmos5l/.../ihp/rsil_code.py` (symlink to full PDK)

- [x] **rppd** - P+ poly resistor (CMOS-compatible, M1-only)
  - File: `ihp-sg13cmos5l/.../ihp/rppd_code.py` (symlink to full PDK)

- [x] **rhigh** - High-R poly resistor (CMOS-compatible, M1-only)
  - File: `ihp-sg13cmos5l/.../ihp/rhigh_code.py` (symlink to full PDK)

## Summary

| Device | Status | Method |
|--------|--------|--------|
| sealring | Done | Modified copy |
| via_stack | Done | Modified copy |
| bondpad | Done | Modified copy |
| SVaricap | Done | Symlink |
| rsil | Done | Symlink |
| rppd | Done | Symlink |
| rhigh | Done | Symlink |
| GuardRing | N/A | Not a device |
