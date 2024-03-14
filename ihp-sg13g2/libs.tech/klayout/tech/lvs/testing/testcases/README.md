# Globalfoundries 180nm MCU LVS Tests


## Folder Structure

```text
📁 testcases
 ┣ 📜README.md                       This file to document the unit tests.
 ┣ 📁 unit                           Contains the unit test structures per device.
   ┣ 📁<device_group>_devices        Contains all LVS testcases for each group.
    ┣ 📁layout                       Layout gds file for each device.
    ┣ 📁netlist                      Spice netlist file for each device.
 ┣ 📁 extraction_checking            Contains a small test case to be used for testing the LVS switches.
 ┣ 📁 torture                        Contains a few large test cases to test the performance of the rule deck. 
 ```
 