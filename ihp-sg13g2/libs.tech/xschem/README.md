
# XSCHEM configuration 

The library and configuration file `xschemrc` can be found in the directory `libs.tech/xschem`. It configures 
the xschem editor to in order to include PDK root directory, library directories and simulation models. Since the configuration script uses 
`PDK_ROOT` environmental variable, it should be exported before running xschem.

Do it only once:
```bash
export PDK_ROOT=<your_path>/IHP-Open-PDK
./install.py
```
Now you can run xschem and enjoy the examples:

```
xschem
```



# XSCHEM primitives and test benches for IHP Open PDK

## XSCHEM symbols
The symbol library can be found in `libs.tech/xschem/sg13g2_pr` and it contains the following devices.

|Device             |Description                                                                                                                                |
|:------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
|npn13g2            |HBT NPN bipolar transistor device with a Nx-number of devices parameter                                                                    |
|npn13g2l           |HBT NPN bipolar transistor device with a Nx-number of devices and El-emitter length parameters                                             |
|npn13g2v           |HBT NPN bipolar transistor device with a Nx-number of devices parameter, device for high power and lower frequency applications            |
|sg13_lv_nmos       |N-channel, low voltage parametrizable mosfet device. W-channel width, L-channel length, ng-number of gates, m-number of devices            |
|sg13_hv_nmos       |N-channel, high voltage parametrizable mosfet device. W-channel width, L-channel length, ng-number of gates, m-number of devices           |
|sg13_lv_pmos       |P-channel, low voltage parametrizable mosfet device. W-channel width, L-channel length, ng-number of gates, m-number of devices            |
|sg13_hv_pmos       |P-channel, high voltage parametrizable mosfet device. W-channel width, L-channel length, ng-number of gates, m-number of devices           |
|rsil               |Silicide resistor of a sheet resistance of 7 $\Omega / \square$                                                                            |    
|rppd               |Polysilicon resistor of a sheet resistance of 7 $\Omega / \square$                                                                         |
|rhigh              |Polysilicon resistor of a high sheet resistance of 1360 $\Omega / \square$                                                                 |
|ntap1              |N-well difussion conntact resistance  of 262 $\Omega$                                                                                      |
|ptap1              |P-well (substrate) difussion conntact resistance  of 262 $\Omega$                                                                          |
|cap_cmim           |Metal-Insulator-Metal capacitor                                                                                                            |
|cap_cpara          |Parasitic capacitor symbol attached to a model (used only for parasitics extraction)                                                       |
|cap_rfcmim         |Metal-Insulator-Metal capacitor model for RF                                                                                               |
|dantenna           |Antenna diode symbol. This diode is used to protect against low voltage. The anode of the diode should be connected to the ptap1 resistor. |
|dpantenna          |Antenna diode symbol. This diode is used to protect against high voltage. The cathode of the diode should be connected to the ntap1 resistor.|
|pnpMPA             |pnp HBT used for band-gap reference circuit                                                                                                |

    
## XSCHEM testcases

The top level schematic is `IHP_testcases.sch` can be found at `libs.tech/xschem/sg13g2_tests` directory. 
By default each test case exports the netlist to the `simulations` directory where `.spiceinit`file is used to configure NGSpice in HSPICE compatibility mode. Also a `psp103_nqs.osdi` file is 
by default placed in this directory in order to simulate the MOSFET devices using PSP103 model. This file can be regenerated and updated (if necessary) using method described [here](../ngspice/openvaf/README.md).
It is important to notice that the NGSpice version should be 40+ and it has to be compiled using `--enable-osdi` flag as follows:
```
git clone https://git.code.sf.net/p/ngspice/ngspice ngspice-ngspice
cd ngspice-ngspice
./configure --enable-osdi
make
sudo make install
```

The `raw` files generated using simulations are placed in `simulations/` folder. If a test case exports CSV file it will be placed in `csv/` directory. The `scripts/` folder contains 
Python scripts, which are used for CSV data post processing. All plots generated by the scripts are exported to the `fig/` directory. More information about test cases can be found
[here](simulations/README.md).

