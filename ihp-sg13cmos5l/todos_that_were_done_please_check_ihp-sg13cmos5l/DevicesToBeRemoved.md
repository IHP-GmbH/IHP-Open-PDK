# Devices to be removed

These devices are NOT included in the SG13CMOS5L PDK because they require:
- HBT/bipolar device layers (EmWind, EmWiHV, nBuLay special config)
- TopMetal layers (TopMetal1/2, TopVia1/2)
- MIM capacitor layers (MIM, Vmim)
- Inductor layers (IND)

## Removed Devices

- [x] **npn13G2** - HBT NPN transistor
  - Requires: EmWind (33), nBuLay (32) special config
  - Tech.json params removed: npn13G2_*

- [x] **npn13G2L** - HBT NPN transistor (low power)
  - Requires: EmWind (33), nBuLay (32) special config
  - Tech.json params removed: npn13G2L_*

- [x] **npn13G2V** - HBT NPN transistor (high voltage)
  - Requires: EmWind (33), EmWiHV (34), nBuLay (32) special config
  - Tech.json params removed: npn13G2V_*

- [x] **Schottky** - Schottky diode
  - Requires: nBuLay, ContBar special configuration
  - Tech.json params removed: Schottky_NW_*, dschottky_*, schottky_nbl1_*, schottky_nw1_*

- [x] **inductor2** - 2-terminal inductor
  - Requires: TopMetal1 (126), TopMetal2 (134), IND (27)
  - Not available in M1-M4-TM1 stack (no TopMetal2)

- [x] **inductor3** - 3-terminal inductor
  - Requires: TopMetal1 (126), TopMetal2 (134), IND (27)
  - Not available in M1-M4-TM1 stack (no TopMetal2)

- [x] **CMiM** - MIM capacitor
  - Requires: MIM (36), Vmim (129), TopMetal1 (126)
  - Tech.json params removed: cmim_*

- [x] **rfCMiM** - RF MIM capacitor with guard ring
  - Requires: MIM (36), Vmim (129), TopMetal1 (126)
  - Tech.json params removed: rfcmim_*

- [x] **isolbox** - Deep isolation structure
  - Requires: nBuLay (32), NWell (31) deep isolation config
  - Tech.json params removed: isolbox_*

## Tech.json Cleanup Summary

The following parameter groups were removed from `sg13cmos5l_tech.json`:

| Category | Parameters Removed |
|----------|-------------------|
| HBT transistors | npn13G2_*, npn13G2L_*, npn13G2V_*, npnMPA_* |
| Schottky diodes | Schottky_NW_*, dschottky_*, schottky_nbl1_*, schottky_nw1_* |
| MIM capacitors | cmim_*, rfcmim_*, Mim_* |
| Isolation | isolbox_* |
| TopMetal filler | TM1Fil_*, TM2Fil_*, BM1Fil_* |


