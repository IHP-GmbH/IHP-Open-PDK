This is the sg13g2_io library. The following files are included in this library:

* `doc`:
  * `README.md`: this file
  * `InputPerformance.html`: simulation results for input bandwidth and duty ratio.
  * `DriveStrengthSim.html`: simulation of drive strength of the output drivers.
* `gds/sg13g2_io.gds`: GDS view of the IO cells
* `spice/sg13g2_io.spice`: spice netlists of the IO cells
* `lef/sg13g2_io.lef`: LEF view of the IO cells
* `lib/sg13g2_io_dummy.lib`: dummy liberty view of the IO cells.  
  This file only contains enough information to get the OpenROAD flow going; no timing
  or power data is available in this file.

These files are generated from python scripts of the Chips4Makers based IHP SG13G2
PDK. The code can be found in the
[c4m-pdk-ihpsg13g2](https://gitlab.com/Chips4Makers/c4m-pdk-ihpsg13g2.git) repo.
This library is built from version `0.0.4` of that source code.
The `README.md` file of this project explains how to use the code in there. The whole
build of the files plus preparation of the files described above for upstreaming can be
generated with the command `pdm doit patch4upstream`.

It also contains externally contributed files:

* cdl/sg13g2_io.cdl: CDL netlist
* verilog/sg13g2_io.v: Verilog netlist
* lib/sg13g2_io_*.lib: Liberty files with timing

18.06.2026  I/O Update 2 resolved issues:
==========================================================================================
	  - VIH/VIL input threshold parameters are fixed (cdl and layout) to be in spec.
	  - Receiver (input): Delay balance is fixed (cdl and layout).
	  - Issue #401. Analog Pad current capability is improved.
	  - Issue #385. M2 connections in ground pads are improved.
	  - Issue #419. Antenna diode structures were added to core inputs (layout fix).
	  - Issue #835. Layout of edges of cells is aligned to provide abutment without DRC errors.
	  - Issue #676. Liberty models are updated. New look-up tables with increased loads are used. Fillers and corner are added in Liberty and verilog model.
	  - Issue #909. Contacts are added in Filler200 cell.
	  - Celllist is updated: subblocks are not library cells.
	  - "sg13g2_Galery" top layout is removed from GDS 2 layout view.
	  - CDL netlist is regenerated.
	  - SPICE netlist is regenerated and renamed to "sg13g2_io.spice" to align the naming with sg13g2_stdcell library.
	  - Pin direction in LEF is fixed.
	   
