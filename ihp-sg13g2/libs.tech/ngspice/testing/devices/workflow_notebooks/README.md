# Device Verification

This folder provides the **pytest test suite** and a **Jupyter notebook workflow** for device-level verification of the SG13G2 Device Model.
It complements the `models_verifier` package and integrates with the top-level `Makefile`.

# Table of contents

- [Device Verification](#device-verification)
- [Table of contents](#table-of-contents)
  - [Folder Structure](#folder-structure)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [Run with pytest](#run-with-pytest)
    - [Run with Jupyter Notebook](#run-with-jupyter-notebook)
  - [Interpreting Pytest Failures](#interpreting-pytest-failures)
    - [Meaning of Each Part](#meaning-of-each-part)


## Folder Structure

```text
📁 validation
 ┣ 📜 test_devices.py        Pytest regression tests for all supported devices.
 ┣ 📜 devices_testing.ipynb  Interactive notebook for manual verification flow.
 ┗ 📜 README.md              Documentation (this file).
```

## Prerequisites

Before running the verification tests, ensure that you have completed the setup described in the [devices README](../README.md):

- Python virtual environment created and activated
- Dependencies installed via `requirements.txt`
- OSDI models compiled (see [verilog-a/README.md](../../../verilog-a/README.md))


## Usage

### Run with pytest

To execute all device tests directly with pytest:

```bash
cd .. # ihp-sg13g2/libs.tech/ngspice/testing/devices
export PYTHONPATH=$PWD
pytest -v validation/test_devices.py
```

Run a specific device test (e.g., `nmos_lv`):

```bash
pytest -v validation/test_devices.py::test_devices[nmos_lv]
```

These tests are automatically called when running `make test-* RUNNER=pytest` from the parent `devices` folder.

---

### Run with Jupyter Notebook

The notebook `devices_testing.ipynb` demonstrates the verification flow interactively:

- Load MDM data
- Run simulations
- Inspect merged DataFrames
- Analyze tolerance checks and reports
- Plot the test results for each device across different design configurations


## Interpreting Pytest Failures

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

- `[metric/target]` — Metric and target (`meas` = measured, `tt` = typical).
- `file=...` — Source MDM file.
- `block_index=...` — Block index inside that file.
- `n=` — Total points in that group.
- `out_of_bounds=` — Number outside allowed envelope.
- `(%)` — Percent of failing points.
- `STATUS:` — Summary across groups.
- Bullet list — Per-metric breakdown of failures.
