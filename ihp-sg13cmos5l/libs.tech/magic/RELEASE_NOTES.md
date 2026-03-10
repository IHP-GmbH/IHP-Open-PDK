# IHP SG13CMOS5L Technology files for magic

> version 0.5.0
    March 10, 2026
    Open Circuit Design, LLC

Included in this pre-release:

1. Technology file for magic (`ihp-sg13cmos5l.tech`)
	* Layer definitions and styles
	* Connectivity definitions
	* Interactive wiring definitions
	* LEF/DEF read/write
2. Additional technology files (read by `ihp-sg13cmos5l.tech`) 
	* DRC rules (`ihp-sg13cmos5l-drc.tech`)
	* Device extraction (`ihp-sg13cmos5l-extract.tech`)
	* Parasitic extraction (`ihp-sg13cmos5l-extract.tech`)
	* GDS read/write (`ihp-sg13cmos5l-cifin.tech`/`ihp-sg13cmos5l-cifout.tech`)
	* Antenna rules (`ihp-sg13cmos5l-drc.tech`)
3. Startup script for magic (`ihp-sg13cmos5l.magicrc`)
4. Device generator for magic (`ihp-sg13cmos5l.tcl`) (top level).  
5. Additional device generator files and data (see file list below). 
6. Technology file for magic with GDS-mapped layers (`ihp-sg13cmos5l-GDS.tech`)
7. LVS setup for netgen (`../netgen/ihp-sg13cmos5l_setup.tcl`)
8. Density rule check (`check_density.py`) script
9. Fill generation (`generate_fill.py`) script 
10. Seal ring generator (`generate_seal.py`) script
11. Script to configure magic for reading the SRAM macros (`read_sram_gds.tcl`)

All magic technology files and associated scripts in this release:

1. Startup script for magic:
	* ihp-sg13cmos5l.magicrc	Use with "magic -rcfile <filename>"

2. Technology files:
	* ihp-sg13cmos5l.tech		Primary technology file (top level)
	* ihp-sg13cmos5l-cifout.tech	GDS output rule deck technology file
	* ihp-sg13cmos5l-cifin.tech		GDS input rule deck technology file
	* ihp-sg13cmos5l-drc.tech		DRC rule deck technology file
	* ihp-sg13cmos5l-extract.tech	Extraction rule deck technology file
	* ihp-sg13cmos5l-GDS.tech		Standalone GDS-layer-exact technology file

3. Device generators:
	* ihp-sg13cmos5l.tcl	Device generator top level
	* ihp-sg13cmos5l-fet.tcl	MOSFET device generators
	* ihp-sg13cmos5l-bjt.tcl	Bipolar device generators (PNP only)
	* ihp-sg13cmos5l-res.tcl	Resistor device generators
	* ihp-sg13cmos5l-var.tcl	Varactor device generator
	* ihp-sg13cmos5l-dio.tcl	Diode device generators
	* ihp-sg13cmos5l-ind.tcl	Inductor device generator
	* ihp-sg13cmos5l-pad.tcl	Pad (device) generator
	* ihp-sg13cmos5l-via.tcl	Via stack generator
	* ihp-sg13cmos5l-fix.tcl	Fixed-layout device geneators
	* ihp-sg13cmos5l-misc.tcl	Substrate/well contact generators
	* ihp-sg13cmos5l-util.tcl	Utility functions

4. Fixed device generator data:
	* nmoscl_2.tcl		Draws the nmoscl_2 subcircuit (without deep nwell)
	* nmoscl_4.tcl		Draws the nmoscl_4 subcircuit (without deep nwell)
	* diodevdd_2kv.tcl	Draws the diodevdd_2kv subcircuit
	* diodevdd_4kv.tcl	Draws the diodevdd_4kv subcircuit
	* diodevss_2kv.tcl	Draws the diodevss_2kv subcircuit
	* diodevss_4kv.tcl	Draws the diodevss_4kv subcircuit

5. Support scripts:
	* generate_fill.py	Python script to generate fill patterns
	* generate_seal.py	Python script to create a seal ring
	* check_density.py	Python script to run density checks
	* read_sram_gds.tcl	Tcl script to configure magic for reading SRAM macros

6. Support script data:
	* sealring_corner.tcl	Seal ring corner subcircuit generator
	* sealring_side.tcl	Seal ring side subcircuit generator
