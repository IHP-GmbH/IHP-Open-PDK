# MDM DC verification – quick guide

This script runs the MDM aggregation → DC simulation → envelope checks using the YAML configs for each device.
## Environment setup

Before running, make sure you have:

* **Python 3.8+** installed
* **ngspice** available on your system (required for simulations)
* **openvaf** installed and in your PATH (needed to compile Verilog-A models)

### Build OSDI files (once per repo checkout)

```bash
cd <repo path>/ihp-sg13g2/libs.tech/verilog-a
chmod +x openvaf-compile-va.sh
./openvaf-compile-va.sh

# Verify OSDI files were built
ls -la <repo path>/ihp-sg13g2/libs.tech/ngspice/osdi
```
### Create a Python virtual environment and install dependencies

```bash
# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate   


# Install required Python packages
pip install pandas pyyaml jinja2 pytest
```

## Run commands

> Run from the **devices** folder so the relative paths in the configs resolve correctly.

```bash
cd ihp-sg13g2/libs.tech/ngspice/testing/devices
```
```bash 
export IHP_OPEN_REPO=<repo path>
```
### NMOS (sg13_lv_nmos)
```bash
python3 -m models_verifier.models_verifier -c mos/nmos_lv/sg13_lv_nmos.yaml
```

### PMOS (sg13_lv_pmos)

```bash
python3 -m models_verifier.models_verifier -c mos/pmos_lv/sg13_lv_pmos.yaml
```

## Outputs

When a run finishes you will see:

1. Per-setup merged CSVs (for debugging/inspection)

- Directory: `<output_dir>/sim_merged/`
- One CSV per discovered sweep/setup (filename derived from `master_setup_type`)

2. Reports (per the `output_dir` in the YAML)

- **Full summary:** `<output_dir>/full_report.csv`
  One row per `(block_id, metric, target)` with counts and pass/fail.
- **Roll-up summary:** `<output_dir>/summary.csv`
  Aggregated by `(metric, target)` with overall out-of-bounds percentages.
- **Detailed failures:** `<output_dir>/detailed_failures.csv` _(only if there are any)_
  Row per failing point with value, bounds, and basic context.

The script also prints a short summary block to the terminal, including total cases, per-target pass/fail counts, and the number of failing points.

## Exit status

- `0` → all selected targets in the run passed their thresholds
- `1` → one or more groups failed (reports still written)

(Other non-zero exit codes indicate early termination before reporting.)

## Interpreting pytest assertion failures

When you run the tests , a device test fails if any checked group exceeds the configured out-of-range threshold. In that case, pytest raises an **AssertionError** and prints lines like:

```
check failed:
[id/meas] (FAIL file=/path/to/meas.mdm, block_index=42) n=120 out_of_bounds=7 (5.83%)
[ib/tt]   (FAIL file=/path/to/meas.mdm, block_index=7)  n=95  out_of_bounds=6 (6.32%)
...

STATUS: 2/24 groups FAILED (8.33%); pass rate = 91.67%
  - id/meas: 1 fails
  - ib/tt:  1 fails
```

### What each part means

- `[metric/target]` — which metric and target failed (`meas` = measured, `tt` = typical corner).
- `file=...` — the source mdm that produced the failing group (if available).
- `block_index=...` — the block index within that file (if available).
- `n=` — total points evaluated in that group.
- `out_of_bounds=` — number of points outside the allowed envelope.
- `(%)` — percent of points outside the envelope for that group.
- `STATUS:` — summary across all groups: how many failed vs. total, plus pass rate.
- Per-metric lines (`- <metric>/<target>: <count> fails`) — quick breakdown by metric/target.

## Run locally

### Run a single device case (same as CI)

```bash
cd ihp-sg13g2/libs.tech/ngspice/testing/devices
python3 -m pytest --tb=short -p no:capture \
  'tests/test_devices.py::test_devices[nmos_lv]'
```

Replace `nmos_lv` with any of: `pmos_lv`, `nmos_hv`, `pmos_hv`, `pnp_mpa`, `npn13g2`, `npn13g2l`, `npn13g2h`.


### Run all  tests

```bash
cd ihp-sg13g2/libs.tech/ngspice/testing/devices
python3 -m pytest --tb=short -p no:capture tests/test_devices.py
```

---
  