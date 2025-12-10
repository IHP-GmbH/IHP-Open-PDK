# Additional Devices Added to Slim PDK


- [x] **rsil** - Silicided resistor (CMOS-compatible, M1-only)
  - File: `ihp/rsil_code.py` (symlink to full PDK)

- [x] **rppd** - P+ poly resistor (CMOS-compatible, M1-only)
  - File: `ihp/rppd_code.py` (symlink to full PDK)

- [x] **rhigh** - High-R poly resistor (CMOS-compatible, M1-only)
  - File: `ihp/rhigh_code.py` (symlink to full PDK)

- [x] **ntap1** - N-tap (NWell contact)
  - Layers: M1, Activ, Cont, NWell, nBuLay
  - File: `ihp/ntap1_code.py` (symlink)

- [x] **ptap1** - P-tap (substrate contact)
  - Layers: M1, Activ, pSD, Cont, Substrate
  - File: `ihp/ptap1_code.py` (symlink)

- [x] **nmosHV** - High voltage NMOS
  - Layers: M1, Activ, GatPoly, Cont, ThickGateOx
  - File: `ihp/nmosHV_code.py` (symlink)

- [x] **pmosHV** - High voltage PMOS
  - Layers: M1, Activ, GatPoly, pSD, NWell, ThickGateOx
  - File: `ihp/pmosHV_code.py` (symlink)

- [x] **dantenna** - N-type antenna diode
  - Layers: M1, Activ, Cont, pSD, Recog
  - File: `ihp/dantenna_code.py` (symlink)

- [x] **dpantenna** - P-type antenna diode
  - Layers: M1, Activ, pSD, Cont, NWell, Recog
  - File: `ihp/dpantenna_code.py` (symlink)

- [x] **esd** - ESD protection structures
  - Layers: M1-M3, Via1-2, Activ, GatPoly, Cont
  - File: `ihp/esd_code.py` (symlink)

- [x] **rfnmos** - RF NMOS
  - Layers: M1-M2, Via1, Activ, GatPoly, Cont
  - File: `ihp/rfnmos_code.py` (symlink)

- [x] **rfnmosHV** - RF NMOS HV
  - Layers: M1-M2, Via1, Activ, GatPoly, ThickGateOx
  - File: `ihp/rfnmosHV_code.py` (symlink)

- [x] **rfpmos** - RF PMOS
  - Layers: M1-M2, Via1, Activ, GatPoly, pSD, NWell
  - File: `ihp/rfpmos_code.py` (symlink)

- [x] **rfpmosHV** - RF PMOS HV
  - Layers: M1-M2, Via1, pSD, NWell, ThickGateOx
  - File: `ihp/rfpmosHV_code.py` (symlink)

- [x] **NoFillerStack** - No filler utility (M1-M5 only)
  - Modified: Removed TM1/TM2 options
  - File: `ihp/NoFillerStack_code.py` (modified copy)

## NOT Compatible (Not Added)

| PCell | Reason |
|-------|--------|
| inductor2_code.py | Uses TopMetal1/2 layers |
| inductor3_code.py | Uses TopMetal1/2 layers |
| inductors_code.py | Base class - uses TopMetal |
| pnpMPA_code.py | PNP bipolar transistor |
| isolbox_code.py | Deep isolation for BiCMOS |

