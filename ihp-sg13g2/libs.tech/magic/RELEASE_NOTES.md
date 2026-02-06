# IHP SG13G2 Technology files for magic

> version 1.0.0
    November 3, 2025 
    Open Circuit Design, LLC

Included in this pre-release:

1. Technology file for magic (`ihp-sg13g2.tech`)
	* Layer definitions and styles
	* Connectivity definitions
	* Interactive wiring definitions
	* LEF/DEF read/write
2. Additional technology files (read by `ihp-sg13g2.tech`) 
	* DRC rules (`ihp-sg13g2-drc.tech`)
	* Device extraction (`ihp-sg13g2-extract.tech`)
	* Parasitic extraction (`ihp-sg13g2-extract.tech`)
	* GDS read/write (`ihp-sg13g2-cifin.tech`/`ihp-sg13g2-cifout.tech`)
	* Antenna rules (`ihp-sg13g2-drc.tech`)
3. Startup script for magic (`ihp-sg13g2.magicrc`)
4. Device generator for magic (`ihp-sg13g2.tcl`) (top level).  
5. Additional device generator files and data (see file list below). 
6. Technology file for magic with GDS-mapped layers (`ihp-sg13g2-GDS.tech`)
7. LVS setup for netgen (`../netgen/ihp-sg13g2_setup.tcl`)
8. Density rule check (`check_density.py`) script
9. Fill generation (`generate_fill.py`) script 
10. Seal ring generator (`generate_seal.py`) script

All magic technology files and associated scripts in this release:

1. Startup script for magic:
	* ihp-sg13g2.magicrc	Use with "magic -rcfile <filename>"

2. Technology files:
	* ihp-sg13g2.tech		Primary technology file (top level)
	* ihp-sg13g2-cifout.tech	GDS output rule deck technology file
	* ihp-sg13g2-cifin.tech		GDS input rule deck technology file
	* ihp-sg13g2-drc.tech		DRC rule deck technology file
	* ihp-sg13g2-extract.tech	Extraction rule deck technology file
	* ihp-sg13g2-GDS.tech		Standalone GDS-layer-exact technology file

3. Device generators:
	* ihp-sg13g2.tcl	Device generator top level
	* ihp-sg13g2-fet.tcl	MOSFET device generators
	* ihp-sg13g2-bjt.tcl	Bipolar device generators
	* ihp-sg13g2-cap.tcl	MiM capacitor device generators
	* ihp-sg13g2-res.tcl	Resistor device generators
	* ihp-sg13g2-var.tcl	Varactor device generator
	* ihp-sg13g2-dio.tcl	Diode device generators
	* ihp-sg13g2-ind.tcl	Inductor device generator
	* ihp-sg13g2-pad.tcl	Pad (device) generator
	* ihp-sg13g2-via.tcl	Via stack generator
	* ihp-sg13g2-fix.tcl	Fixed-layout device geneators
	* ihp-sg13g2-misc.tcl	Substrate/well contact generators
	* ihp-sg13g2-util.tcl	Utility functions

4. Fixed device generator data:
	* nmoscl_2.tcl		Draws the nmoscl_2 subcircuit
	* nmoscl_4.tcl		Draws the nmoscl_4 subcircuit
	* diodevdd_2kv.tcl	Draws the diodevdd_2kv subcircuit
	* diodevdd_4kv.tcl	Draws the diodevdd_4kv subcircuit
	* diodevss_2kv.tcl	Draws the diodevss_2kv subcircuit
	* diodevss_4kv.tcl	Draws the diodevss_4kv subcircuit
	* schottky_nbl1.tcl	Draws the schottky_nbl1 subcircuit
	* scr1.tcl		Draws the scr1 subcircuit

5. Support scripts:
	* generate_fill.py	Python script to generate fill patterns
	* generate_seal.py	Python script to create a seal ring
	* check_density.py	Python script to run density checks

6. Support script data:
	* sealring_corner.tcl	Seal ring corner subcircuit generator
	* sealring_side.tcl	Seal ring side subcircuit generator
