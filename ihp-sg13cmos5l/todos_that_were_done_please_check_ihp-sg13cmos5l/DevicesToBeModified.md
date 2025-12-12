# Devices to be modified

## Completed

- [x] **sealring** - Modified for M1-M4-TM1 stack
  - Updated to use M1-M4-TM1 metal stack (no Metal5)
  - Uses TopVia1 to connect M4 to TopMetal1
  - Removed TopMetal2, TopVia2 references
  - File: `ihp-sg13cmos5l/.../ihp/sealring_code.py` (modified copy)

- [x] **ViaStack (via_stack)** - Modified for M1-M4-TM1 stack
  - Updated layer choices to Metal1-Metal4-TopMetal1
  - Uses TopVia1 to connect M4 to TopMetal1
  - Removed TopMetal2, TopVia2 references
  - Added TopVia1 tech params (TV1_a, TV1_b, TV1_c, TV1_d)
  - File: `ihp-sg13cmos5l/.../ihp/via_stack_code.py` (modified copy)

- [x] **bondpad** - Modified for M1-M4-TM1 stack
  - Changed topMetal to TopMetal1 (no TopMetal2)
  - Uses TopVia1 to connect M4 to TopMetal1
  - Updated layer lists to M1-M4-TM1 stack
  - Added TopVia1 via size handling
  - File: `ihp-sg13cmos5l/.../ihp/bondpad_code.py` (modified copy)

- [x] **SVaricap** - No modification needed
  - Uses only M1 + base device layers (Activ, GatPoly, nSD, pSD, NWell, etc.)
  - All layers already in SG13CMOS5L PDK
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
