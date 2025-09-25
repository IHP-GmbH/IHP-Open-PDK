# Device Testing

This directory contains the complete infrastructure for performing **device-level verification** of the IHP SG13G2 PDK.  

It provides a structured environment with Makefile targets, configuration files, and automation scripts that enable consistent and reproducible testing of model cards. 

The goal is to ensure that all supported device types (MOS, HBT, and PNP) are correctly validated against their reference specifications using standardized simulation flows.  

Two testing frameworks are supported:  
- **models_verifier**: A custom verification engine designed for regression-style testing and detailed reporting (default).  
- **pytest**: A widely used Python testing framework for integration with broader verification environments.  

---

# Table of Contents

- [Device Testing](#device-testing)
- [Table of Contents](#table-of-contents)
  - [Folder Structure](#folder-structure)
  - [Prerequisites](#prerequisites)
    - [Building OSDI Models](#building-osdi-models)
    - [Setup Python Virtual Environment](#setup-python-virtual-environment)
  - [Usage](#usage)
    - [Running Tests with Makefile](#running-tests-with-makefile)
      - [Test Runners](#test-runners)
      - [Device Configurations](#device-configurations)
      - [Available Targets](#available-targets)
        - [Group Targets](#group-targets)
        - [Device Targets](#device-targets)
      - [Examples](#examples)
  - [Output Results](#output-results)
    - [Output Folder Structure](#output-folder-structure)
    - [Folder Contents Explained](#folder-contents-explained)

---

## Folder Structure

```text
📁 devices  
 ┣ 📜 Makefile             Main entry point for running device tests  
 ┣ 📁 configs              YAML configuration files and templates for SG13G2 devices  
 ┣ 📁 models_verifier      Python package for simulation and verification  
 ┣ 📁 validation           Pytest test cases and Jupyter notebooks  
 ┣ 📁 workflow_notebooks   Step-by-step notebooks for running and visualizing the verification flow  
 ┗ 📜 README.md            Documentation for SG13G2 models testing (this file)  
```

---

## Prerequisites

Before running the SG13G2 model tests, ensure that the following tools and dependencies are installed and available in your environment:  

- **Python 3.9 or later** – required for running scripts and test automation  
- **python3-venv** – used for creating isolated Python virtual environments  
- **ngspice** – the circuit simulator used to perform analog device simulations  
- **openvaf** – required for compiling Verilog-A models into OSDI-compatible libraries  

### Building OSDI Models

The simulation flow relies on precompiled **OSDI models**.  
To generate these models, follow the detailed build instructions provided in:  [Verilog-A README](../../../verilog-a/README.md)  

---

### Setup Python Virtual Environment

It is strongly recommended to work inside a local Python virtual environment:  

```bash  
# Step 1: Create a new Python virtual environment
python3 -m venv test_env

# Step 2: Activate the virtual environment
source test_env/bin/activate

# Step 3: Install all required dependencies
pip install -r requirements.txt

# Note:
# On some Linux distributions (e.g., Debian/Ubuntu with Python 3.11+),
# you may need to allow installation outside the virtual environment.
# In that case, use the following instead:
pip install --break-system-packages -r requirements.txt
```

---

## Usage

All commands should be executed from the [**current working directory**](./):  


### Running Tests with Makefile

The provided **Makefile** is the main entry point for running device tests.  
It supports both **group-level** (all devices of a given category) and **device-level** (a single device) execution.  


#### Test Runners

- **Default runner**: 'models_verifier' (recommended)  
- **Alternative runner**: 'pytest' (append 'RUNNER=pytest' to the command)  

This flexibility allows you to either:  
- Perform **full model validation** against measurement data using 'models_verifier'  
- Perform **lightweight regression checks** with 'pytest'  


#### Device Configurations

- All device tests are managed through dedicated YAML configuration files located in the [configs directory](configs/).

- These files specify data sources, model paths, simulation settings, and validation metrics.  

- For example, the LV NMOS configuration is defined in [sg13_lv_nmos](configs/mos/nmos_lv/sg13_lv_nmos.yaml).  

Every Makefile target maps directly to one of these configuration files.

---

#### Available Targets

##### Group Targets
- `make test-all` → Run **all device tests**  
- `make test-mos` → Run NMOS and PMOS (LV and HV variants)  
- `make test-hbt` → Run HBT devices (NPN13G2 family)  
- `make test-pnp` → Run PNP MPA devices  

##### Device Targets
Each individual device has its own target:  
- MOS: `test-nmos_lv`, `test-pmos_lv`, `test-nmos_hv`, `test-pmos_hv`  
- HBT: `test-npn13g2`, `test-npn13g2l`, `test-npn13g2v`  
- PNP: `test-pnp_mpa`  

---

#### Examples

Run all devices with the default runner (`models_verifier`):  

```bash  
make test-all  
```

Run only MOS devices using 'pytest':  

```bash  
make test-mos RUNNER=pytest  
```

Run a single device (example: LV NMOS) with the verifier:  

```bash  
make test-nmos_lv  
```

Run the PNP MPA device with pytest:  

```bash  
make test-pnp_mpa RUNNER=pytest  
```

For a full list of available targets and options, run:  

```bash  
make help  
```

---

## Output Results

When a test run finishes, all results are written to the output directory specified in the device configuration file (by default: `models_results/<device_name>`).  

Each device gets its own dedicated subdirectory containing simulation inputs, intermediate data, and final verification reports.  

### Output Folder Structure

```
📁 models_results
 ┣ 📁 <device_name>/  
 ┃ ┣ 📁 netlists/              Generated ngspice netlists (optional).  
 ┃ ┣ 📁 per_setup_mdm_csvs/    Merged CSVs for each measurement/setup.  
 ┃ ┣ 📁 per_setup_sim_vs_meas/ CSV comparisons of simulation vs. measurement.  
 ┃ ┗ 📁 verification_reports/  Final aggregated reports.  
```

### Folder Contents Explained

- **netlists**  
  Contains the generated .cir netlists created from Jinja2 templates.  
  This folder is only produced if **generate_netlists: true** is enabled in the device YAML configuration.  
  Useful for debugging the exact simulation inputs used.  

- **per_setup_mdm_csvs**  
  Holds merged CSV files for each test setup.  
  These files combine the raw measurement data (MDM) with the corresponding simulation results, providing a single source for analysis.  

- **per_setup_sim_vs_meas**  
  Contains CSV files that directly compare simulated vs. measured values on a per-setup basis.  
  Ideal for spotting mismatches, trends, or systematic offsets in the model behavior.  

- **verification_reports**  
  Aggregated reports summarizing the verification outcomes:  
  - **summary.csv** → High-level roll-up by device and metric (pass/fail).  
  - **full_report.csv** → Detailed results for every test block and metric.  
  - **detailed_failures.csv** → Lists of all failing points (only generated if failures exist).  
