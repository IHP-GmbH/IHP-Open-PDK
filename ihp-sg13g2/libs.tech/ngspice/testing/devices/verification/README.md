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


## Folder Structure

```text
📁 verification
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
cd .. #ihp-sg13g2/libs.tech/ngspice/testing/devices
export PYTHONPATH=$PWD
pytest -v verification/test_devices.py
```

Run a specific device test (e.g., `nmos_lv`):

```bash
pytest -v verification/test_devices.py::test_devices[nmos_lv]
```

These tests are automatically called when running `make test-* RUNNER=pytest` from the parent `devices` folder.

---

### Run with Jupyter Notebook

The notebook `devices_testing.ipynb` demonstrates the verification flow interactively:

- Load MDM data
- Run simulations
- Inspect merged DataFrames
- Analyze tolerance checks and reports
- Plot the test results for each device across different design configurations.
