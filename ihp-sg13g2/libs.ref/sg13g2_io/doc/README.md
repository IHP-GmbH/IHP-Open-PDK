This is the sg13g2_io library. The following files are included in this library:

* `doc`:
  * `README.md`: this file
  * `InputPerformance.svg`: simulation results for input bandwidth and duty ratio.
  * DriveStrengthSim.txt: simulation of drive strength of the output drivers.
* `gds/sg13g2_io.gds`: GDS view of the IO cells
* `spice/sg13g2_io.spi`: spice netlists of the IO cells
* `lef/sg13g2_io.lef`: LEF view of the IO cells
* `liberty/sg13g2_io_dummy.lib`: dummy liberty view of the IO cells.  
  This file only contains enough information to get the openroad flow going; no timing
  or power data is available in this file.

These files are generated from python scripts of the Chips4Makers based IHP SG13G2
PDK. The code can be found in the
[c4m-pdk-ihpsg13g2](https://giotlab.com/Chips4Makers/c4m-pdk-ihpsg13g2.git) repo.
This library is built from version `0.0.1` of that source code.
The `README.md` file of this project explains how to use the code in there. The whole
build of the files plus preparation of the files descrived above for upstreaming can be
generated with the command `pdm doit patch4upstream`.
