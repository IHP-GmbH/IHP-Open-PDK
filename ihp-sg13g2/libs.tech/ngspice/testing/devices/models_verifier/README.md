
# MDM DC Verification – Quick Guide

This script runs the flow:

**MDM aggregation → DC simulation → Envelope checks**  
using the YAML configs for each device.

## 1. Environment Setup

### Requirements
- **Python 3.8+**
- **ngspice** (required for simulations)
- **openvaf** in your `PATH` (needed to compile Verilog-A models)

### Build OSDI Files

```bash
cd <repo path>/ihp-sg13g2/libs.tech/verilog-a
chmod +x openvaf-compile-va.sh
./openvaf-compile-va.sh
````

### Create Virtual Environment & Install Dependencies

```bash
# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate   

# Install required packages
pip install pandas pyyaml jinja2 pytest
```

---

## 2. Running Tests

> Always run from the **devices** folder so relative paths in configs resolve correctly.

```bash
cd ihp-sg13g2/libs.tech/ngspice/testing/devices
```

### Run a Single Device

* **sg13_lv_nmos**

  ```bash
  python3 -m models_verifier.models_verifier -c mos/nmos_lv/sg13_lv_nmos.yaml
  ```

* **sg13_lv_pmos**

  ```bash
  python3 -m models_verifier.models_verifier -c mos/pmos_lv/sg13_lv_pmos.yaml
  ```

(Other devices: `nmos_hv`, `pmos_hv`, `pnp_mpa`, `npn13g2`, `npn13g2l`, `npn13g2v`)


## 3. Outputs

When a run finishes, you will see:

### 3.1 Per-setup merged CSVs (for debugging/inspection)

* Location: `<output_dir>/sim_merged/`
* One CSV per discovered sweep/setup
  (filename derived from `master_setup_type`)

### 3.2 Reports (per `output_dir` in YAML)

* **Full summary:** `<output_dir>/full_report.csv`
  One row per `(block_id, metric, target)` with counts and pass/fail.

* **Roll-up summary:** `<output_dir>/summary.csv`
  Aggregated by `(metric, target)` with overall out-of-bounds percentages.

* **Detailed failures:** `<output_dir>/detailed_failures.csv`
  Only written if failures exist.
  Row per failing point with value, bounds, and context.

Additionally, the script prints a **summary block to the terminal**, including:

* Total cases
* Per-target pass/fail counts
* Number of failing points


## 4. Exit Status Codes

* **0** → All selected targets passed thresholds
* **1** → One or more groups failed (reports still written)
* **Other non-zero** → Early termination before reporting

---

## 5. Interpreting Pytest Failures

When using pytest, a device test fails if any checked group exceeds the configured out-of-range threshold. Example output:

```
check failed:
[id/meas] (FAIL file=/path/to/meas.mdm, block_index=42) n=120 out_of_bounds=7 (5.83%)
[ib/tt]   (FAIL file=/path/to/meas.mdm, block_index=7)  n=95  out_of_bounds=6 (6.32%)

STATUS: 2/24 groups FAILED (8.33%); pass rate = 91.67%
  - id/meas: 1 fails
  - ib/tt:   1 fails
```

### Meaning of Each Part

* `[metric/target]` — Metric and target (`meas` = measured, `tt` = typical).
* `file=...` — Source MDM file.
* `block_index=...` — Block index inside that file.
* `n=` — Total points in that group.
* `out_of_bounds=` — Number outside allowed envelope.
* `(%)` — Percent of failing points.
* `STATUS:` — Summary across groups.
* Bullet list — Per-metric breakdown of failures.

---

## 6. Running Locally (CI-style)

### Run a Single Device with Pytest

```bash
cd ihp-sg13g2/libs.tech/ngspice/testing/devices
python3 -m pytest --tb=short -p no:capture \
  'tests/test_devices.py::test_devices[nmos_lv]'
```

Replace `nmos_lv` with any of:
`pmos_lv`, `nmos_hv`, `pmos_hv`, `pnp_mpa`, `npn13g2`, `npn13g2l`, `npn13g2v`

### Run All Devices

```bash
cd ihp-sg13g2/libs.tech/ngspice/testing/devices
python3 -m pytest --tb=short -p no:capture tests/test_devices.py
```

