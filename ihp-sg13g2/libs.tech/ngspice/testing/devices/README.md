# Device Testing

## Table of Contents

- [Device Testing](#device-testing)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Purpose and Verification Methodology](#purpose-and-verification-methodology)
    - [Verification Approach](#verification-approach)
    - [Corner-Based Validation](#corner-based-validation)
      - [Validation methodology](#validation-methodology)
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
      - [`1. run_data/`](#1-run_data)
      - [`2. clean_measured_data/`](#2-clean_measured_data)
      - [`3. combined_results/`](#3-combined_results)
      - [`4. final_reports/`](#4-final_reports)
        - [Example Output logs — nmos\_lv](#example-output-logs--nmos_lv)

---

## Introduction

This directory contains the complete infrastructure for performing **device-level verification** of the IHP SG13G2 PDK.  

It provides a structured environment with Makefile targets, configuration files, and automation scripts that enable consistent and reproducible testing of model cards. 

The goal is to ensure that all supported device types (MOS, HBT, and PNP) are correctly validated against their reference specifications using standardized simulation flows.  

---
## Purpose and Verification Methodology

The purpose of this testing framework is to **validate and qualify the accuracy of the IHP SG13G2 device models** by directly comparing **measured silicon data** from the fabrication process with **simulated results** generated using ngspice.

This comparison ensures that:
- The **SPICE model cards** used for circuit design accurately represent the real physical devices.
- Any **deviation between measurement and simulation** is within acceptable process variation limits.
- The **model behavior across process corners** (Fast, Slow, and Typical) stays consistent with the expected fabrication spread.

### Verification Approach

For each device type (MOS, HBT, and PNP):
1. **Measured data** from the foundry is parsed, cleaned, and normalized into a standardized format.  
2. **Simulation data** is generated using ngspice, based on automatically created netlists derived from templates.  
3. The measured and simulated results are **merged and compared point-by-point**, evaluating electrical quantities such as current or voltage over multiple bias conditions.  
4. **Statistical summaries** are produced to quantify deviations and to detect potential model inaccuracies or corner mismatches.

### Corner-Based Validation

This stage validates the SG13G2 model cards by comparing **measured silicon data** from the fab and the **Typical (TT)** simulation results against the performance envelope defined by the **Fast (FF)** and **Slow (SS)** corners. In short: **both the measured data and the Typical simulation must lie inside the FF/SS envelope**, and measured data is then compared to the Typical simulation to quantify model accuracy.

#### Validation methodology

1. **Simulate all three corners**  
   For each device and each test bias condition, generate simulation results for FF, TT, and SS.

2. **Build the FF/SS envelope**  
   For every x-axis sweep point (e.g., Vgs, Vce) compute the envelope boundaries from the FF and SS curves (FF = upper bound, SS = lower bound). The envelope is the allowed region of physical variation.

3. **Apply statistical corner tolerance (σ adjustment)**  
   The FF/SS bounds are expanded by a **relative tolerance margin** to account for process variation and measurement uncertainty. This is usually based on a **3σ coverage**.

4. **Envelope containment checks (FF/SS)**  
   - **Measured-in-envelope:** Verify every measured data point falls within the FF/SS envelope (including tolerance).  
   - **Typical-in-envelope:** Verify the TT simulation curve also lies within the same envelope.  
   Both checks must pass for the model and measured data to be considered consistent with the declared corner spread.

5. **Interpretation rules (examples)**  
   - **TT inside envelope & measured inside envelope & small measured/TT error:** model validated (expected).  
   - **TT inside envelope but measured outside envelope:** likely process or measurement outlier — investigate wafer/measurement data.  
   - **Measured inside envelope but TT outside envelope:** model cornering issue — model tuning required to bring TT inside FF/SS envelope.  
   - **Both TT and measured outside envelope:** serious mismatch — re-evaluate model and process assumptions.

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

All device tests are controlled through **YAML configuration files** located in the [configs directory](configs/).  
Each configuration file defines:
- Which device to test
- Model and measured data sources
- Simulation setup (sweeps, biasing, corners)
- Validation targets and pass/fail thresholds

📘 **For detailed configuration format, template usage, and examples**, see this documentation:  
[Configuration Files README](configs/README.md)

---

### Running Tests with Makefile

The provided **Makefile** is the main entry point for running device tests.  
It supports both **group-level** (e.g., all MOS or all HBT) and **device-level** (single-device) execution.

#### Test Runners

- **Default runner**: `models_verifier` (recommended)  
- **Alternative runner**: `pytest` (append `RUNNER=pytest` to the command)

#### Device Configurations

Each Makefile target corresponds to one of the YAML configuration files under the [configs directory](configs/).  
For example:
- `make test-nmos_lv` → uses `configs/mos/sg13_lv_nmos.yaml`
- `make test-npn13g2` → uses `configs/hbt/sg13g2_npn13g2.yaml`

The Makefile automatically detects and passes the corresponding configuration file to the selected test runner.

---

#### Available Targets

##### Group Targets
- `make test-all` → Run **all device tests**
- `make test-mos` → Run all MOS devices (LV + HV)
- `make test-hbt` → Run all HBT devices
- `make test-pnp` → Run all PNP devices

##### Device Targets
Each device can be run individually:
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
 ┃ ┣ 📁 run_data              Intermediate data generated during simulation runs — 
 ┃ ┃                          includes circuit files, logs, and raw CSV outputs from ngspice.
 ┃ ┣ 📁 netlists              Generated ngspice netlists (for debugging or inspection).
 ┃ ┣ 📁 clean_measured_data   Extracted and cleaned measured data from the input MDM files.
 ┃ ┣ 📁 combined_results      Fully merged results combining simulated and measured datasets.
 ┃ ┗ 📁 final_reports         Aggregated Markdown and CSV reports summarizing 
 ┃                            overall verification metrics and pass/fail statistics.
```

This structure helps you easily trace every stage of data processing — from raw measurements to final summarized reports.

---

#### `1. run_data/`
Contains **all intermediate data generated during the run**, including:
- **Circuit netlists** used for ngspice simulation.
- **Simulation logs** capturing ngspice outputs and potential warnings.
- **Raw CSV results** generated directly from each simulation sweep before merging.

This directory acts as a complete record of the simulation process — useful for debugging or re-running individual sweeps.

---

#### `2. clean_measured_data/`
This directory stores **processed measurement data** extracted from the input MDM (Measured Data Model) files.  
The goal is to provide a clear and uniform format compatible with the verification scripts.

Each file corresponds to one test type (e.g., `dc_idvg.csv`, `dc_idvd.csv`, etc.) and contains columns as shown in the following example for the **nmos_lv** device:

| Column | Description |
|--------|--------------|
| block_id | Unique block identifier within the dataset. |
| block_index | Sub-index or measurement instance. |
| input_data | Raw data section name from the MDM file. |
| input_vars / output_vars | Variables used for biasing and measured outputs. |
| TEMP | Measurement temperature (°C). |
| W, L | Device width and length. |
| AD, AS, PD, PS | Diffusion area and perimeter parameters. |
| NF, M | Number of fingers and device multiplicity. |
| vg | Gate voltage. |
| sweep_var | The swept bias variable (e.g., Vd, Vg, or Vb). |

Other devices (e.g., **pmos_lv**, **npn13g2**, etc.) follow a **similar structure** — only the bias variable names and measured outputs differ slightly depending on the device type and test configuration.

---

#### `3. combined_results/`

This directory contains **merged datasets** that align the measured and simulated results for direct comparison.  
Each file represents one test type (e.g., `dc_idvg.csv`) and includes both measured and simulated data across all corners.

| Column | Description |
|--------|--------------|
| block_id, block_index | Same identifiers as in measured data. |
| input_data, input_vars, output_vars | Source information. |
| temp, w, l, ad, as, pd, ps, nf, m | Device geometry and setup. |
| vg, vd, vb, vs, sweep_var | Applied bias conditions. |
| ib_meas, id_meas, ig_meas, is_meas | Measured bias and current values. |
| ib_sim_mos_tt, id_sim_mos_tt, ig_sim_mos_tt, is_sim_mos_tt | Simulated data at **Typical** corner. |
| ib_sim_mos_ss, id_sim_mos_ss, ig_sim_mos_ss, is_sim_mos_ss | Simulated data at **Slow** corner. |
| ib_sim_mos_ff, id_sim_mos_ff, ig_sim_mos_ff, is_sim_mos_ff | Simulated data at **Fast** corner. |

Each file name (e.g., `dc_idvg.csv`) corresponds to the **test master type** — the same flag defined in the MDM file (e.g., `DC_IDVG`, `DC_IDVD`).

This dataset is used for all later comparisons, tolerance analysis, and summary generation.

---

#### `4. final_reports/`

This folder holds all **aggregated outputs and summaries** from the validation:

| File | Description |
|------|--------------|
| `full_results.csv` | The complete dataset combining measured and all simulated results. |
| `results_summary.csv` | Aggregated statistics showing pass/fail counts and out-of-bounds (OOB) rates. |
| `failed_results.csv` | Only entries that failed tolerance criteria. |
| `final_summary.md` | A human-readable Markdown summary with statistics and metrics for all tests. |

These reports are the final outcome of the model validation process, summarizing how closely the simulation models align with measured fab data across all process corners.


##### Example Output logs — nmos_lv

```bash
2025-10-06 00:43:36 [INFO] Summary report saved to: models_results/nmos_lv/final_reports/results_summary.csv  
2025-10-06 00:43:36 [INFO] Detailed failure report saved to: models_results/nmos_lv/final_reports/failed_results.csv  
2025-10-06 00:43:36 [INFO] Summary written to: models_results/nmos_lv/final_reports/final_summary.md  

========== RANGE-CHECK SUMMARY ==========  
Target       Sweeps     Pass     Fail     TotPts    FailPts   Fail%Cases   Fail%Pts  
-----------------------------------------------------------------------------------  
Measured       7704     6920      784     249960      13612        10.18       5.45  
Typical        7704     7663       41     249960        248         0.53       0.10  
=========================================  
```

These summaries provide a concise view of how the model performs across all targets and conditions.
