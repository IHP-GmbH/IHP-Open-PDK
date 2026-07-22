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
 ┃ ┣ 📜 sg13_lv_nmos.yaml  
 ┃ ┣ 📜 sg13_lv_pmos.yaml  
 ┃ ┣ 📜 sg13_hv_nmos.yaml  
 ┃ ┗ 📜 sg13_hv_pmos.yaml  
 ┣ 📁 hbt/  
 ┃ ┣ 📜 sg13g2_npn13g2.yaml  
 ┃ ┣ 📜 sg13g2_npn13g2l.yaml  
 ┃ ┗ 📜 sg13g2_npn13g2v.yaml  
 ┣ 📁 pnp/  
 ┃ ┗ 📜 sg13_pnp_mpa.yaml  
 ┗ 📜 TEMPLATE.yaml  
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
| **clip_curr** | Minimum current value (in Amperes) used to exclude extremely small or noisy data points during comparison. | `1e-11` |

**Example:**  
Currents below 1e-11 A are ignored during validation.

---

### 4. Parallel Execution

| Variable | Description | Example |
|-----------|--------------|----------|
| **max_workers** | Number of parallel threads or workers used for validation tasks. | `8` |

This helps speed up processing across multiple sweeps or corners.

---

## Notes

- All file paths are **relative to the device testing root directory (`devices/`)**.  
- If a specific parameter is not defined, a **default** will be applied automatically by the verification framework.  
- For detailed information on the verification logic and output reports, refer to the [main Device Testing README](../README.md).  
