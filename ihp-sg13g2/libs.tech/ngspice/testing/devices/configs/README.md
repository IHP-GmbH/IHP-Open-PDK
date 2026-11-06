# Configuration Files for Device Testing

This directory contains all **YAML configuration files** that define the behavior of each device test in the SG13G2 model verification framework.

Each configuration file provides the necessary parameters for:
- Defining which **device** to test (e.g., `sg13_lv_nmos`).
- Linking to the corresponding **measured data** from the fab (MDM format).
- Specifying the **model card** paths.
- Setting up **simulation parameters** (bias sweeps, corners, etc).
- Declaring **validation targets** and **tolerance thresholds**.

---

## Directory Structure

```
📁 configs  
 ┣ 📁 mos/  
 ┃ ┣ 📁 nmos_lv, pmos_lv, nmos_hv, pmos_hv   one config per device (DC + C-V tier)  
 ┃ ┣ 📜 dc_template.spice.j2      transistor DC sweep  
 ┃ ┣ 📜 diode_template.spice.j2   junction-diode structures (di_bd_*, di_bs_*)  
 ┃ ┗ 📜 cv_template.spice.j2      capacitance meter (C-V tier)  
 ┣ 📁 hbt/  
 ┃ ┣ 📁 npn13g2, npn13g2l, npn13g2v   one config per device (its MQA test structure; DC + S-parameters)  
 ┃ ┣ 📁 variants              the other test structures (not MQA, run on request; base_config + a few keys)  
 ┃ ┣ 📜 hbt_dc.spice.j2  
 ┃ ┗ 📜 hbt_sp.spice.j2  
 ┗ 📁 pnp_mpa/  
   ┣ 📜 pnpmpa.yaml            DC (14 DUTs) + C-V tier (DUT16 array)  
   ┣ 📜 pnpMPA_dc.spice.j2  
   ┗ 📜 pnpMPA_cv.spice.j2  
```

Each folder corresponds to a **device category**, and each YAML file inside represents a **specific device configuration**.

---

## Validation Configuration Overview

This section describes the key parameters controlling the validation and tolerance behavior during model verification.  

---

### 1. Thresholds and Out-of-Bound Control

| Variable | Description | Example |
|-----------|--------------|----------|
| **threshold_percent_oob** | Maximum allowed percentage (%) of points that can fall **outside** the target envelope before a sweep is considered failed. | `0.5` |

**Example:**  
If `threshold_percent_oob = 0.5`, then a sweep will pass only if at least **99.5% of its data points** lie within the expected envelope.

---

### 2. Corner Envelope Tolerance

| Variable | Description | Example |
|-----------|--------------|----------|
| **corner_tolerance_percent** | Defines the **relative tolerance margin (%)** applied to the FF and SS simulation bounds to account for process variation and measurement uncertainty. | `0.27` |

**Example:**  
If `corner_tolerance_percent = 0.27`,  
then the FF and SS bounds will be expanded by ±0.27% around their nominal values.

---

### 3. Current Clipping

| Variable | Description | Example |
|-----------|--------------|----------|
| **clip_curr** | Current floor (A): measured and simulated currents below it are floored to ±clip_curr (sign kept); a point where the measurement and both band edges sit at the floor counts as agreement (`n_floor`). | `1e-11` |

**Example:**  
Currents below 1e-11 A are compared as ±1e-11 A (sign kept); a point at the floor on both sides is an agreement.

---

### 4. Parallel Execution

| Variable | Description | Example |
|-----------|--------------|----------|
| **max_workers** | Number of parallel threads or workers used for validation tasks. | `8` |

This helps speed up processing across multiple sweeps or corners.

---

### 5. Keys added for the test structures, diodes, S-parameters and C-V tier

| Key | Description |
|---|---|
| **base_config** | Path of another config read first; this config's top-level keys replace the base's as a whole (`design_param_overrides: {}` drops the base's overrides). Used by `hbt/variants/`. |
| **setup_templates** | `{measurement group: template}`: a netlist template for one group instead of `dc_template_path` (MOS: the junction diodes). |
| **exclude_patterns** | Substrings of file names left out before parsing (pnpMPA: DUT3, the CBC/CBE templates and "single" files); every dropped file is logged. |
| **mqa_ranges_only** | `true`: only the characteristics / metrics with an `mqa_ranges` window are judged (inside it); the others are "No points" (not judged). The HBTs: checked only in the MQA ranges. |
| **sparam_files** | `{metric: file stem or list of stems}`; each file is its own curve, judged in its `sparam_mqa_ranges` window. |
| **sparam_self_deembed** | `{stem: {open: <dummy stem>, short: <dummy stem>}}`: open-short de-embed the raw S of this file with the folder's dummies (its IC-CAP S_deemb is a copy). |
| **sparam_copied_deemb** | Stems whose S_deemb is a known copy of another file's: never judged with it, left out of the copy check of the others. A judged file whose S_deemb equals another file's stops the run. |
| **sparam_allow_raw** | Stems without S_deemb whose raw S may be judged (otherwise such a file stops the run). |
| **cv_template_path**, **cv_subckt_pins**, **cv_freq_hz** | C-V netlist, the subcircuit's pin order, the meter frequency (1 MHz assumed). |
| **cv_setups** | `{group: {high: [...], low: [...], float: [...], float_to: pin, sign: -1}}`: meter terminals per measurement group (see `models_verifier/cv_runner/cv_sweep_runner.py`). |
| **cv_metrics** | Metric columns of the C-V tier, like `metrics`. |
| **cv_file_overrides** | `{file-name substring: {design parameter: value}}`: corrections of wrong header values for the C-V tier (logged per file). |
| **cv_waivers_dir**, **sparam_waivers_dir**, **waivers_dir** | Exception folders of the C-V, S-parameter and DC tiers. |

---

## Notes

- All file paths are **relative to the device testing root directory (`devices/`)**.  
- If a specific parameter is not defined, a **default** will be applied automatically by the verification framework.  
- For detailed information on the verification logic and output reports, refer to the [main Device Testing README](../README.md).  
