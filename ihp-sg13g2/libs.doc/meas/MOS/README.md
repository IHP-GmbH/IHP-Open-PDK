This folder contains MOS device measurement data in IC-CAP Data Manager ([MDM](https://people.ece.ubc.ca/robertor/Links_files/Files/ICCAP-2008-doc/icug/icug136.html)) format.
<img src="https://github.com/IHP-GmbH/IHP-Open-PDK/assets/116548619/d9c76cfe-9e2f-4075-9c69-2af43305ad87" width="70%">  
MOS devices supported: nmos (low and high voltage), pmos (low and high voltage)  
Directory contents:
* doc -> report files with comparison against Spectre simulations
* SG13_`<device>` -> measurement data
* test_structures -> different test segments layouts (GDSII) with the documentation

### CMOS Device under Test (DUT) Naming Convention
Example: `W10u0_L0u5_S387_5`
* `W10u0` -> width 10um
* `L0u5`  -> length 0.5um
* `S387`  -> test segment S387
* `5`     -> DUT №5

