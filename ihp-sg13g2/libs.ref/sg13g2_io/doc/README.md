This is the sg13g2_io library. The following files are included in this library:

* `doc`:
  * `README.md`: this file
  * `InputPerformance.html`: simulation results for input bandwidth and duty ratio.
  * `DriveStrengthSim.html`: simulation of drive strength of the output drivers.
* `gds/sg13g2_io.gds`: GDS view of the IO cells
* `spice/sg13g2_io.spi`: spice netlists of the IO cells
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
