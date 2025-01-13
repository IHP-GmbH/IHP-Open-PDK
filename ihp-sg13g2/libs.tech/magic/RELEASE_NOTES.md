# IHP SG13G2 Technology files for magic

> version 0.1.2 (alpha pre-release)  
    December 17, 2024  
    Efabless Corporation

Included in this pre-release:

1. Technology file for magic (`ihp-sg13g2.tech`)
	* Layer definitions and styles
	* Connectivity definitions
	* Interactive wiring definitions
	* DRC rules
	* Device extraction
	* Parasitic extraction
	* GDS read/write
	* LEF/DEF read/write
	* Antenna rules
2. Technology file for magic with GDS-mapped layers (`ihp-sg13g2-GDS.tech`)
3. Startup script for magic (`ihp-sg13g2-GDS.magicrc`)
4. LVS setup for netgen (`../netgen/ihp-sg13g2_setup.tcl`)

Not included/completed in this pre-release:

1. Device generator for magic (`ihp-sg13g2.tcl`).  
   The file in the pre-release version is a placeholder only.
2. Density rule check (`check_density.py`)  
   Needs verification.
3. Fill generation (`generate_fill.py`)  
   Work in progress.
4. Seal ring generator (may be implemented in the device generation script)

All items not included in this pre-release are expected to be completed by April 2025.
