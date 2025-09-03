# Device Testing Directory

## Introduction

This directory contains setup files, templates, scripts, and reports for device-level verification of the IHP SG13 PDK.  
It is organized by device type (MOS, HBT, PNP) and includes a custom test runner (`models_verifier`) and Makefile.

## Folder Structure

```
📁devices
 ┣ 📜Makefile                      Make targets to run device tests (pytest or models_verifier).
 ┣ 📁mos                           Directory for MOSFET device testing (NMOS/PMOS, LV/HV).
 ┃ ┣ 📜cap_template.spice.j2       Template for MOS capacitance simulation.
 ┃ ┣ 📜dc_template.spice.j2        Template for MOS DC sweep simulation.
 ┃ ┣ 📁nmos_lv                     Low-voltage NMOS device configs and results.
 ┃ ┃ ┣ 📜sg13_lv_nmos.yaml         Config file for LV NMOS tests.
 ┃ ┣ 📁nmos_hv                     High-voltage NMOS device configs.
 ┃ ┃ ┗ 📜sg13_hv_nmos.yaml         Config file for HV NMOS tests.
 ┃ ┣ 📁pmos_lv                     Low-voltage PMOS device configs.
 ┃ ┃ ┗ 📜sg13_lv_pmos.yaml         Config file for LV PMOS tests.
 ┃ ┗ 📁pmos_hv                     High-voltage PMOS device configs.
 ┃   ┗ 📜sg13_hv_pmos.yaml         Config file for HV PMOS tests.
 ┣ 📁hbt                           Directory for HBT (NPN) device testing.
 ┃ ┣ 📜hbt_dc.spice.j2             Template for HBT DC sweep simulation.
 ┃ ┣ 📁npn13g2                     NPN13G2 variant device configs and results.
 ┃ ┃ ┣ 📜npn13g2.yaml              Config file for NPN13G2.
 ┃ ┣ 📁npn13g2l                    NPN13G2L variant configs and results (same structure).
 ┃ ┗ 📁npn13g2v                    NPN13G2V variant configs and results (same structure).
 ┣ 📁pnp_mpa                       Directory for PNP MPA device testing.
 ┃ ┣ 📜pnpmpa.yaml                 Config file for PNP MPA device.
 ┃ ┣ 📜pnpMPA_dc.spice.j2          Template for PNP DC sweep.
 ┣ 📁models_verifier               Python package for running simulations and verification.
 ┃ ┣ 📜models_verifier.py          CLI entry point for running verification with a config.
 ┃ ┣ 📜mdm_aggregator.py           Combines measurement data into dataframes.
 ┃ ┣ 📜mdm_parser.py               Parser for raw MDM measurement files.
 ┃ ┣ 📜mdm_parser_utils.py         Helper utilities for parsing MDM files.
 ┃ ┣ 📜mdm_parser_const.py         Constants for parsing and verification.
 ┃ ┣ 📁dc_runner                   Module for DC sweep simulation.
 ┃ ┃ ┣ 📜dc_sweep_runner.py        Orchestrates ngspice DC runs.
 ┃ ┃ ┗ 📜helper.py                 Helper functions for simulation configs.
 ┃ ┣ 📁error_analyzer              Module for analyzing simulation vs measurement results.
 ┃ ┃ ┣ 📜config.py                 Metric and threshold specification.
 ┃ ┃ ┗ 📜range_checker.py          Range/tolerance checking of results.
 ┃ ┗ 📜README.md                   Package-level documentation.
 ┣ 📁tests                         Pytest test suite for device verification.
 ┃ ┗ 📜test_devices.py             Runs pytest-based device verification.
 ┗ 📁run_test_flow                 Example notebooks / workflows.
   ┗ 📜IHP_devices_testing.ipynb   Notebook demonstrating device testing flow.
```
