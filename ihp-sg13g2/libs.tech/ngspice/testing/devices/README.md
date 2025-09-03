# Device Testing

This directory provides setup files, Makefile targets, and scripts to run **device-level verification** for the IHP SG13 PDK.
Tests can be executed with either **pytest** or the custom **`models_verifier`** runner.

# Table of contents

- [Device Testing](#device-testing)
- [Table of contents](#table-of-contents)

  - [Folder Structure](#folder-structure)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)

    - [Running with Makefile](#running-with-makefile)
    - [Examples](#examples)

## Folder Structure

```text
📁 devices
 ┣ 📜 Makefile               Main entrypoint for running device tests.
 ┣ 📁 devices_configs        YAML configs and templates for MOS, HBT, PNP devices.
 ┣ 📁 models_verifier        Python package for simulation & verification.
 ┣ 📁 models_run             Generated outputs (netlists, CSVs, reports).
 ┣ 📁 verification           Pytest tests and notebooks.
 ┗ 📜 README.md              Documentation (this file).
```

## Prerequisites

You need the following tools to run the SG13G2 device tests:

- **Python 3.9+**
- **python3-venv** (for creating a virtual environment)
- **ngspice** (for running simulations)
- **openvaf** (for compiling Verilog-A models)

To build the required OSDI models, please follow the instructions in:
[`README`](../../../verilog-a/README.md)

### Setup Python Virtual Environment

It is recommended to use a local virtual environment:

```bash
# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

## Usage

> Always run from this directory:
> `ihp-sg13g2/libs.tech/ngspice/testing/devices`

### Running with Makefile

The Makefile defines groups and individual device targets.
The **default runner** is `models_verifier`. To switch, use `RUNNER=pytest`.

**Available targets:**

- **Groups**:

  - `make test-all` → all devices
  - `make test-mos` → NMOS/PMOS (LV/HV)
  - `make test-hbt` → HBT (NPN13G2 variants)
  - `make test-pnp` → PNP MPA

- **Devices**:

  - `nmos_lv`, `pmos_lv`, `nmos_hv`, `pmos_hv`,
  - `npn13g2`, `npn13g2l`, `npn13g2v`,
  - `pnp_mpa`

### Examples

Run all devices with default runner (`models_verifier`):

```bash
make test-all
```

Run only MOS devices with pytest:

```bash
make test-mos RUNNER=pytest
```

Run a single device (e.g., LV NMOS) with verifier:

```bash
make nmos_lv
```

Run PNP MPA with pytest:

```bash
make pnp_mpa RUNNER=pytest
```


For more details on available targets and options, run:

```bash
make help
```

---
