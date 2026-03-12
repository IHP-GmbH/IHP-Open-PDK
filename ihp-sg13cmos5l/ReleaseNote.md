# Release Notes

## v0.1.0

## Summary
- Added and aligned DRC rule decks and QA coverage with SG13G2 updates, including maximal rules and standalone deck support.
- Expanded Magic and Netgen support, updated tech files, and improved SRAM and latchup rule handling.
- Improved LibreLane integration, CI workflows, and RTL-to-GDS validation setup.
- Added LVS infrastructure and rule support alongside DRC updates.
- Added xschem support and updated ngspice/xyce integration for CMOS5L symbols and launchers.
- Updated IO/standard cell libraries, symbols, and layout layers for CMOS5L compatibility.
- Fixed various LVS/DRC issues, layer exclusions, and documentation cleanups.

## Notable Changes
- DRC: aligned rules with G2, added maximal rules, fixed density and windowed checks, and expanded test coverage.
- Magic/Netgen: updated tech files, added SRAM support, and improved rule handling and version requirements.
- LibreLane/CI: integrated LibreLane flow, adjusted CI commands, and improved custom PDK workflows.
- LVS: added infrastructure, forbidden layer detection, and device exclusions.
- xschem/ngspice/xyce: added xschem symbols, fixed launcher support, and improved simulator integration.
- Libraries: updated IO/standard cell assets, symbols, LEF/GDS, and layer mappings for CMOS5L.

## Supported Devices (Consolidated)
- MOSFETs: LV/HV NMOS/PMOS, plus RF variants (including HV RF).
- Bipolar: pnpMPA.
- Diodes: antenna diodes, diodevdd/diodevss variants.
- Resistors: silicided, p+ poly, high-R poly (and model variants).
- ESD: ESD devices nmoscl_2 nmoscl_4.
- Taps/utilities: ntap1, ptap1, sub, via stack, sealring, NoFillerStack.
