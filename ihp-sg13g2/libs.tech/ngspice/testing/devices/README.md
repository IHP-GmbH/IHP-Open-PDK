# Device Testing

## Table of Contents

- [Device Testing](#device-testing)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Purpose and Verification Methodology](#purpose-and-verification-methodology)
    - [Verification Approach](#verification-approach)
    - [Corner-Based Validation](#corner-based-validation)
      - [Validation methodology](#validation-methodology)
    - [MQA Bias-Window Range Limits](#mqa-bias-window-range-limits)
  - [Folder Structure](#folder-structure)
  - [Prerequisites](#prerequisites)
    - [Toolchains (ngspice + OpenVAF-Reloaded)](#toolchains-ngspice--openvaf-reloaded)
    - [Building OSDI Models](#building-osdi-models)
    - [Setup Python Virtual Environment](#setup-python-virtual-environment)
  - [Usage](#usage)
    - [Running Tests with Makefile](#running-tests-with-makefile)
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
    - [Generating figures](#generating-figures)
  - [Exceptions (waivers)](#exceptions-waivers)
    - [How a curve is judged](#how-a-curve-is-judged)
    - [Writing exceptions](#writing-exceptions)
  - [HBT Test Structures](#hbt-test-structures)
  - [HBT S-Parameter Characteristics (CjE, CjC, fT)](#hbt-s-parameter-characteristics-cje-cjc-ft)
    - [Extraction equations](#extraction-equations)
    - [Simulated side](#simulated-side)
    - [Running the S-param tests](#running-the-s-param-tests)
  - [C-V Tier (Capacitances)](#c-v-tier-capacitances)
  - [MOS Junction Diodes and pnpMPA Geometry](#mos-junction-diodes-and-pnpmpa-geometry)
  - [MOS Error EDA (ML Clustering + Report)](#mos-error-eda-ml-clustering--report)
  - [Continuous Integration](#continuous-integration)

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

### MQA Bias-Window Range Limits

In addition to the corner envelope check above, a metric can be restricted to a **fixed
bias window** before pass/fail is evaluated — this is how the SiGe HBT MQA (Model
Quality Assurance) valid ranges are enforced (e.g. only compare the forward-Gummel base
current inside `VBE ∈ [0.7, 0.8] V`). Points whose derived bias falls **outside** the
window are excluded from the comparison entirely (counted separately as `n_excluded`,
not as pass or fail).

This is configured per metric, per device config YAML, via two independent mechanisms
(`models_verifier/error_analyzer/config.py::MetricSpec`):

- **`valid_range`** — a flat, per-metric bias-window gate, keyed by the *derived* bias
  variable name (bias columns in the merged DataFrame are **node voltages**, not
  VBE/VCE/VCB directly — e.g. HBT derives `VBE = vb - ve`, `VCE = vc - ve`,
  `VCB = vc - vb`; MOS derives `VGS = vg - vs`, `VDS = vd - vs`, `VBS = vb - vs`):
  ```yaml
  metrics:
    - name: "ib"
      meas: "ib_meas"
      tt: "ib_sim_hbt_typ"
      valid_range: {vbe: [0.7, 0.8]}
  ```
- **`mqa_ranges`** — the same windows expressed per-characteristic (keyed by the
  normalized MDM `input_data` stem, e.g. `fg_vcb0`, `fg_vce`, `fo_vb`) so one block can
  cover every metric of that characteristic (`_all`) or name metrics individually. This
  is how the three HBT configs (`configs/hbt/*/*.yaml`) declare the PDF MQA windows:
  ```yaml
  mqa_ranges:
    fg_vcb0:                 # forward Gummel @ VCB=0
      ib: {vbe: [0.7, 0.8]}
      ic: {vbe: [0.6, 0.96]}
    fg_vce:                  # forward Gummel @ VCE
      ib: {vce: [0.5, 1.5], vbe: [0.7, 0.8]}
      ic: {vce: [0.5, 1.5], vbe: [0.6, 0.96]}
    fo_vb:                   # output, IC vs VCE @ VBE=const
      _all: {vce: [0.2, 1.5], vbe: [0.7, 0.9]}
  ```
- **`min_limit` / `max_limit`** — a fixed numeric bound used instead of the FF/SS
  envelope columns (needed for metrics, such as the S-param characteristics below, that
  don't have a natural corner envelope column to compare against).

Both are **optional and additive** — a config with none of these keys behaves exactly
as before (no gating). Running `make test-npn13g2` logs the applied VBE/VCE windows and
the resulting (reduced) compared-point count; `make test-nmos_lv` (no `valid_range`
declared) is unaffected.

---

## Folder Structure

```text
📁 devices  
 ┣ 📜 Makefile             Main entry point for running device tests  
 ┣ 📁 configs              YAML configuration files and templates for SG13G2 devices  
 ┣ 📁 models_verifier      Python package for simulation and verification  
 ┃  ┣ 📁 error_analyzer    Range-checking / bias-window gating (config.py, range_checker.py)  
 ┃  ┣ 📁 waivers           Exact-value curve exceptions (schema 2) + generator  
 ┃  ┣ 📁 eda               MOS error EDA / ML clustering / report generation (Milestone M3)  
 ┃  ┣ 📁 sp_runner         HBT S-parameter (CjE/CjC/fT) sim + verifier, open-short de-embedding  
 ┃  ┣ 📁 cv_runner         C-V tier: capacitance-meter simulation + verifier (MOS, pnpMPA)  
 ┃  ┗ 📁 mdm_processing     MDM parsing, aggregation, and S-param deembedding  
 ┣ 📁 waivers              Committed per-device exception files (schema 2, per toolchain)  
 ┣ 📁 tools                toolchain.py (toolchains, OSDI), check_hbt_deembedding.py (S_deemb check)  
 ┣ 📜 toolchain.lock       Pinned ngspice + OpenVAF-Reloaded versions, URLs, checksums, build options  
 ┣ 📁 validation           Validation plotting helpers and analysis scripts  
 ┣ 📁 workflow_notebooks   Step-by-step notebooks for running and visualizing the verification flow  
 ┗ 📜 README.md            Documentation for SG13G2 models testing (this file)  
```

Four directories are **generated at run time and gitignored** (never committed): `models_results/<toolchain>/<case>/` (Makefile `test-*`/`test-*-sparam` targets), `figures/<toolchain>/<case>/` (`plot-*` targets), `eda_report/<device>/` (`eda-*` targets) and `osdi_build/ovr-<commit>/` (`make osdi`) — see [Output Results](#output-results), [HBT S-Parameter Characteristics](#hbt-s-parameter-characteristics-cje-cjc-ft), and [MOS Error EDA](#mos-error-eda-ml-clustering--report) below.

---

## Prerequisites

Before running the SG13G2 model tests, ensure that the following tools and dependencies are installed and available in your environment:  

- **Python 3.14** (the CI version; 3.12 or later is needed) – required for running scripts and test automation  
- **python3-venv** – used for creating isolated Python virtual environments  
- **ngspice 46 / 47** with OSDI support, and **OpenVAF-Reloaded** – installed as pinned *toolchains* (below)  

### Toolchains (ngspice + OpenVAF-Reloaded)

Results depend on the simulator and on the compiler of the Verilog-A models, so every run names
its **toolchain**: `ng<ngspice version>-ovr-<OpenVAF-Reloaded commit>`, e.g. `ng47-ovr-b4517ad`.
The versions, download URLs, checksums and build options are pinned in
[`toolchain.lock`](toolchain.lock); [`tools/toolchain.py`](tools/toolchain.py) installs them
under `$TOOLCHAIN_ROOT` (default `~/.local/toolchains`):

```bash
python3 tools/toolchain.py list                      # pinned toolchains and what is installed
python3 tools/toolchain.py build ngspice 47          # download (sha256 checked), configure, make, install
python3 tools/toolchain.py build openvaf b4517ad     # download the pinned commit, cargo build (LLVM 21)
python3 tools/toolchain.py register ngspice 46 ~/.local/bin/ngspice   # or use an existing local build
make osdi TOOLCHAIN=ng47-ovr-b4517ad                 # PSP103 compiled with that OpenVAF -> osdi_build/ovr-b4517ad/
```

The MOS tests load `psp103.osdi` / `psp103_nqs.osdi` from `$OSDI_DIR` (see [`.spiceinit`](.spiceinit));
the Makefile exports it, together with `NGSPICE_BIN`, `TOOLCHAIN` and `RESULTS_ROOT`, and the
MOS test targets compile the models first when needed. The bipolar models (VBIC) are built into
ngspice, so those devices depend only on the ngspice version. The general PDK build of all OSDI
models is described in the [Verilog-A README](../../../verilog-a/README.md).

---

### Setup Python Virtual Environment

It is strongly recommended to work inside a local Python virtual environment:  

```bash  
# Step 1: Create a new Python virtual environment
python3 -m venv test_env

# Step 2: Activate the virtual environment
source test_env/bin/activate

# Step 3: Install the pinned dependencies (the exceptions are recorded with these versions;
# requirements.txt lists the direct dependencies only)
pip install -r requirements.lock

# Note:
# On some Linux distributions (e.g., Debian/Ubuntu with Python 3.11+),
# you may need to allow installation outside the virtual environment.
# In that case, use the following instead:
pip install --break-system-packages -r requirements.lock
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
`TOOLCHAIN=<id>` selects the toolchain (default `ng47-ovr-b4517ad`); results go to
`models_results/<toolchain>/<case>/`. Group targets run every case and exit 1 at the end if any
case had a new failure.

#### Device Configurations

Each Makefile target corresponds to one of the YAML configuration files under the [configs directory](configs/).  
For example:
- `make test-nmos_lv` → uses `configs/mos/nmos_lv/sg13_lv_nmos.yaml`
- `make test-npn13g2` → uses `configs/hbt/npn13g2/npn13g2.yaml`

The Makefile automatically passes the corresponding configuration file to the verifier.

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

These DC targets are described in detail above. Three further groups of Makefile
targets are documented in their own sections below:
- **Exception targets** (`waive-<case>`, `waive-all`, `waive-hbt-sparam`) — see
  [Exceptions (waivers)](#exceptions-waivers).
- **HBT S-parameter targets** (`test-hbt-sparam`, `test-<hbt-device>-sparam`) — see
  [HBT S-Parameter Characteristics](#hbt-s-parameter-characteristics-cje-cjc-ft).
- **MOS EDA targets** (`eda-mos`, `eda-<mos-device>`) — see
  [MOS Error EDA](#mos-error-eda-ml-clustering--report).

Run `make help` at any time for the full, current list of targets.

---

#### Examples

Run all devices with the verifier:  

```bash  
make test-all  
```

Run only MOS devices:  

```bash  
make test-mos  
```

Run a single device (example: LV NMOS) with the verifier:  

```bash  
make test-nmos_lv  
```

Run every case on another toolchain, and the framework unit tests:  

```bash  
make test-all TOOLCHAIN=ng46-ovr-fdf2522  
make unit-tests  
```

Run the PNP MPA device:  

```bash  
make test-pnp_mpa  
```

For a full list of available targets and options, run:  

```bash  
make help  
```

---

## Output Results

When a test run finishes, all results are written to the output directory of the device configuration file under the toolchain's results root: `models_results/<toolchain>/<case>/` (the Makefile sets `RESULTS_ROOT=models_results/<toolchain>`, which replaces the leading `models_results` of the config's `output_dir`).  

Each device gets its own dedicated subdirectory containing simulation inputs, intermediate data, and final verification reports.  

### Output Folder Structure

```
📁 models_results
 ┣ 📁 <toolchain>/<case>/
 ┃ ┣ 📜 toolchain.txt          Toolchain ID, exception key, ngspice version, OSDI files (sha256) of the run.
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
| `<metric>_band_lo`, `<metric>_band_hi`, `<metric>_judged` | The acceptance band of each metric at each point (ss..ff widened by `corner_tolerance_percent`) and whether the point was judged (inside the bias window, all values present), exactly as the range check used them; written after the check. |

Each file name (e.g., `dc_idvg.csv`) corresponds to the **test master type** — the same flag defined in the MDM file (e.g., `DC_IDVG`, `DC_IDVD`).

This dataset is used for all later comparisons, tolerance analysis, summary generation and the figures.
Current columns are already floored at `clip_curr` (sign kept), as the check saw them.

---

#### `4. final_reports/`

This folder holds all **aggregated outputs and summaries** from the validation:

| File | Description |
|------|--------------|
| `full_results.csv` | One row per curve × metric × target with its `status`: `Passed`, `Failed (new)`, `Failed (not simulated)` (measured points without simulated values: a framework error, never waived), `Failed (waived, auto, pending review)` or `Failed (waived, approved)` — see [Exceptions](#exceptions-waivers) — and `points_sha256`, the fingerprint of a failing row's points. `n_missing` counts measured points the simulation did not give (e.g. a corner that did not converge at the end of a sweep). A row with such points never passes: they are listed in `failed_results.csv` with an empty band and deviation, so an exception records which points were missing; a row with no simulated point at all is `Failed (not simulated)`. |
| `results_summary.csv` | Per metric × target: points, out-of-band points, and curve counts `n_passed`, `n_failed` (waived ones included), `n_waived` (of which waived), `n_failed_new`, `n_not_judged`. |
| `failed_results.csv` | Every out-of-band point, and every measured point the simulation did not give (empty band and deviation): bias (including the swept `vbe`/`vbc`/`vce` of junction C-V files), the judged value, the band, and the simulated tt/ss/ff and measured values. The exceptions fingerprint these points. |
| `new_failures.csv` | Rows with status `Failed (new)` or `Failed (not simulated)`: failures without an exactly matching exception. They make the run exit 1. Empty when there are none. |
| `stale_exceptions.csv` | Exceptions of this toolchain that no failing row used, with a `reason`: the curve passes or is not judged now (to be reviewed and removed), or the curve is not in the run at all (lost coverage: the run exits 1). |
| `simulation_errors.csv` | Blocks whose simulation failed completely. Any row makes the run exit 1; the exception generator refuses such a run. |
| `final_summary.md` | A human-readable Markdown summary; waived curves are counted as failures. |

These reports are the final outcome of the model validation process, summarizing how closely the simulation models align with measured fab data across all process corners.


##### Example Output logs — nmos_lv

```bash
2025-10-06 00:43:36 [INFO] Summary report saved to: models_results/<toolchain>/nmos_lv/final_reports/results_summary.csv  
2025-10-06 00:43:36 [INFO] Detailed failure report saved to: models_results/<toolchain>/nmos_lv/final_reports/failed_results.csv  
2025-10-06 00:43:36 [INFO] Summary written to: models_results/<toolchain>/nmos_lv/final_reports/final_summary.md  

Target       Curves   Passed   Failed   Waived      New  NotJudged     Points    FailPts
Measured       7704     6920      784      784        0          0     249960      13612
Typical        7704     7663       41       41        0          0     249960        248
TOTALS: 15408 curves | passed 14583 | failed 825 (waived 825, new 0) | stale exceptions 0
```

### Generating figures

`validation/plot_verification_results.py` draws one PNG per measured block and output variable from a run's
`combined_results/` (DC, `cv/` and `sparam/` alike): the measurement (open grey circles), the typical simulation
(black line), the acceptance band of every metric on that output where it was judged (light blue: ss..ff widened
by `corner_tolerance_percent`), grey spans over points outside the bias windows (not judged), and the out-of-band
measured points of the verdict (filled orange; the five furthest ones are labelled), and measured points the
simulation did not give (orange crosses). The band and the judged points
are the `<metric>_band_lo`, `<metric>_band_hi`, `<metric>_judged` columns the verifier writes into
`combined_results`, so a figure shows exactly what was checked. Each figure goes to the folder of its status
(`passed`, `failed_new`, `failed_waived`, `failed_not_simulated`, `no_points`) from `final_reports/full_results.csv`.
The file name keeps the structure, measurement group and temperature of the MDM file
(`<structure>_<group>_<temp>_b<block>_<output>_<sweep>.png`), so the files of one structure at several
temperatures do not overwrite each other:

```bash
make test-npn13g2    # writes models_results/<toolchain>/npn13g2/ (and sparam/ after test-npn13g2-sparam)
make plot-npn13g2    # -> figures/<toolchain>/npn13g2/<group>/<status>/<file>_b<block>_<output>_<sweep>.png
make plot-hbt        # all HBT cases; S-parameter / C-V figures go to .../<case>/sparam/ and .../<case>/cv/
make plot-all        # every case; FIG_DIR=<dir> redirects the output
```

`figures/` is gitignored.

---

## Exceptions (waivers)

Some curves do not meet the acceptance check and have been reviewed. An **exception** keeps
the run's exit code at 0 for such a curve as long as the simulation reproduces it **exactly**;
any change makes it a new failure again. A waiver means *reviewed*, **not** *good*: every report
still counts a waived curve as a failure.

### How a curve is judged

- A curve is one measured data block, identified by `(input_data, block_index)` (`block_id`
  is a new uuid every run and is never a key). It is judged per metric (`id`, `ib`, `ic`, ...)
  and per target (`meas` = the measurement, `tt` = the typical simulation) against the
  ss..ff band widened by `corner_tolerance_percent`, inside the MQA bias windows. It fails when
  more than `threshold_percent_oob` of its points are out of band.
- Each device has a committed exception file `waivers/<device_name>.yaml` (S-parameters:
  `waivers/sparam/`). An entry names the curve, metric and target, its `status`
  (`auto-waived`, or `approved` / `rejected` set by the reviewer), a reason, the date it was
  first waived, and **per toolchain** the number of judged points, the number of failing
  points, a fingerprint (`points_sha256`) of every failing point's bias and simulated
  tt/ss/ff values rounded to `exact_sig_digits` (6) significant digits (any change of a failing point larger than
  1e-5 relative shows; points inside the band are not fingerprinted, only counted; the
  last-digit differences between machines, up to 5e-11 seen, change it only for a value next to a rounding
  step), and the worst point
  for the reader. Bipolar devices key their records by ngspice version (`ng47`); devices with a
  Verilog-A model by the full toolchain ID (`ng47-ovr-b4517ad`).
- A failing row is `Failed (waived, ...)` **only** when the run reproduces that toolchain's
  record exactly (same counts, same fingerprint). Anything else — one more or one fewer failing
  point, a changed value, a toolchain without a record, a rejected entry — is `Failed (new)`,
  is listed in `final_reports/new_failures.csv` and makes the run exit 1.
- `final_reports/stale_exceptions.csv` lists exceptions that no failing row used; one whose curve is missing from the
  run (a file that disappeared, was excluded or could not be built) makes the run exit 1.
- A run removes the reports of the previous run when it starts and checks that the ngspice
  binary and the PSP103 objects belong to its toolchain ID; the generator only reads a run
  that finished without simulation errors.

### Writing exceptions

`waivers/generate.py` reads a **finished** run (no new simulation) and writes its
`Failed (new)` rows into the exception file. It keeps every existing entry and the records of
other toolchains, never touches a rejected entry, and puts an approved entry whose values
changed back to `auto-waived`; it never sets `approved`.

```bash
make test-npn13g2                 # 1. run (exit 1 lists the new failures)
make waive-npn13g2                # 2. write them into waivers/npn13g2.yaml (same TOOLCHAIN)
make test-npn13g2                 # 3. exit 0: every failure is reproduced exactly
make waive-all WAIVE_REASON="..." # all cases; waive-<hbt>-sparam / waive-hbt-sparam for S-parameters
```

Run the generator once per toolchain (`TOOLCHAIN=...`) so each toolchain has its records. Review
the new entries (`final_reports/failed_results.csv` has every failing point; `make plot-<case>`
draws them) before committing the files; the reviewer sets `approved` or `rejected`.

---

## HBT Test Structures

Each HBT device has one MQA test structure in its device config (`npn13g2_T03`,
`npn13g2l_T01`, `npn13g2v_T01`). The other 11 measured structures are their own cases
(`make test-<case>`, `test-<case>-sparam`, `test-hbt-variants[-sparam]`), configured in
`configs/hbt/variants/<case>.yaml` with `base_config` (everything not set there comes from the
device config) and their own exception folders `waivers/variants/<case>/`:

| case | difference from the device config |
|---|---|
| `npn13g2_T00`, `_T01`, `_T02` | fT from `spar_vcb025`, `spar_vcb05` (the only constant-VCB files there) |
| `npn13g2l_T00` | `Nx: 2` (header says 3; with 3 the measured IC is 0.67x the model, with 2 it is 1.00x like the other structures; pending IHP confirmation) |
| `npn13g2l_T02`, `_T03`, `_T04` | `design_param_overrides: {}` (the header Nx is right; the device config forces Nx = 4 for T01). Emitter length 5.0 um, outside the stated validity of the model card (El = 1 - 2.5 um): their failures include extrapolation |
| `npn13g2v_T00`, `_T02`, `_T03`, `_T04` | no `spar_vcb05`: fT judged on `spar_vce_deemb` (VCB 0.67-0.75 V inside the MQA window, closest to 0.5 V), `spar_vcb0`, `spar_vcb10_deemb`, `spar_vcbm05` |

## HBT S-Parameter Characteristics (CjE, CjC, fT)

Milestone M4 adds three RF characteristics for the HBT devices (`npn13g2`, `npn13g2l`,
`npn13g2v`), extracted from the **deembedded** S-parameters of the `spar_*` MDM files
(`dummy_open`/`dummy_short` open/short deembedding, via **scikit-rf**):

| Metric | Measured data set | MQA valid window (npn13g2 / npn13g2l) | MQA valid window (npn13g2v) |
|--------|--------------------|----------------------------------------|-------------------------------|
| `cje` (CjE, emitter-base junction cap) | `spar_vb` (cold, VCB=0) | VBE ∈ [−1.5, 0.5] V | VBE ∈ [−1.5, 0.5] V |
| `cjc` (CjC, base-collector junction cap) | `spar_vc` (cold) | VBC ∈ [−1.5, 0.5] V, averaged 0.5–5 GHz | same |
| `ft` (transit frequency) | `spar_vcb025` / `spar_vcb05` (hot) | @VCB=0.25 V, VBE ∈ [0.7, 0.96] V | @VCB=0.5 V, VBE ∈ [0.75, 0.83] V |

### Extraction equations

From the deembedded, S→Y converted 2-port (`sp_runner/extract.py`):
- `CjE = Im(Y11 + Y12) / (2·π·f)` — averaged over the full frequency range.
- `CjC = -0.5 · Im(Y21 + Y12) / (2·π·f)` — averaged over 0.5–5 GHz.
- `fT = |H21| · f` — extrapolated to f = 30 GHz assuming an ideal 10 dB/decade H21
  rolloff.

Extracted measured CjE/CjC are in the low tens-of-fF range and monotonic in bias; fT
peaks near the expected PDF value (~350 GHz for npn13g2/npn13g2l, ~110 GHz for
npn13g2v) within the windows above.

### Simulated side

The simulated CjE/CjC/fT come from an ngspice **AC** small-signal 2-port **Y**
extraction of the HBT subckt (`configs/hbt/hbt_sp.spice.j2`) at the same bias grid as
the measured `spar_*` sweep, then reduces with the **same** extraction equations as the
measured side, so meas-vs-sim comparison is apples-to-apples.

### Running the S-param tests

```bash
make test-npn13g2-sparam        # one HBT device
make test-npn13g2l-sparam
make test-npn13g2v-sparam
make test-hbt-sparam            # all three

# Write the new S-param failures of the last run into waivers/sparam/<device>.yaml
# (separate from the DC files in waivers/):
make waive-hbt-sparam
```

**fT at every measured VCB.** `sparam_files` may list several files per metric; each file is its
own curve, judged in the device's MQA fT window (`sparam_mqa_ranges`, keyed by file):
npn13g2 `spar_vcb025` (MQA), `spar_vcb0`, `spar_vcb05`, `spar_vcb10`, `spar_vcbm05`; npn13g2l
`spar_vcb025` (MQA), `spar_vcb05`; npn13g2v `spar_vcb05` (MQA), `spar_vcb0`, `spar_vcb10_deemb`,
`spar_vcb15_deemb`, `spar_vcbm05`. fmax is not extracted.

**Measured data are checked before they are judged:**
- A judged file whose IC-CAP `S_deemb` is identical to another file's of the folder stops the run
  (copied data). Known copies are declared: npn13g2v_T01 `spar_vcb10` / `spar_vcb15` (copies of
  `spar_vcb05`; the `*_deemb` files hold the real data) and npn13g2_T03 `spar_vcb10` (copy of
  `spar_vcb05`), whose raw S is de-embedded again with the folder's OPEN/SHORT dummies
  (`sparam_self_deembed`, `models_verifier/sp_runner/deembed.py`).
- A file without `S_deemb` is judged only when listed in `sparam_allow_raw`.
- `npn13g2v_T01/spar_vcb20` is not used: its biases (ICCAP_VAR) are VCB = 0.25 V.
- `make check-deembedding` recomputes IC-CAP's `S_deemb` of every file from its raw S and the
  folder's dummies (agreement ~5e-6 for every genuine file of the npn13g2 and npn13g2l folders;
  the npn13g2v folders have no dummies and are only checked for copies) and lists copies
  (`$(RESULTS_ROOT)/hbt_deembedding_check.md`; exit 1 for an unhandled copy or mismatch).
- A file declared in `sparam_copied_deemb` is never judged with its `S_deemb` (listing it in
  `sparam_files` stops the run).

Results land under `models_results/<toolchain>/<device>/sparam/` (separate from the DC
`combined_results/` / `final_reports/` trees, same file layout otherwise), and are
range-checked meas-vs-sim using the same bias windows (`sparam_mqa_ranges`) and exception
mechanism as the DC metrics. See `sparam_files`, `sparam_metrics`, and
`sparam_mqa_ranges` in `configs/hbt/*/*.yaml` for the exact wiring.

---

## C-V Tier (Capacitances)

`make test-<case>-cv` (`test-cv` for all) checks the capacitance measurements of the four MOS
devices (junction `c_bd_*` / `c_bs_*`, gate `c_g_ds`, `c_g_dsb`, `c_d_g`, oxide `c_oxide`) and of
pnpMPA (CBE / CBC of the 12000-cell DUT16 array). `models_verifier/cv_runner/` reproduces the
capacitance meter: the HIGH terminal(s) carry the measured bias plus an AC voltage, the LOW
terminals sit at 0 V through sources whose AC currents are summed, and one AC analysis per bias
point (1 MHz; the meter frequency is not recorded) gives `C = sum Im(I_low) / (2 pi f)`. The
results are judged with the normal check (ss..ff band + `corner_tolerance_percent`,
`threshold_percent_oob`) into `models_results/<toolchain>/<case>/cv/`, exceptions in `waivers/cv/`.

| group | HIGH | LOW | note |
|---|---|---|---|
| `c_bd_area/perim` | b | d | the header COMMENT says "S/D-Low", but counting S as well doubles C |
| `c_bs_area/perim` | b | s | |
| `c_g_ds` | g | d, s | b AC ground |
| `c_g_dsb` | g | d, s, b | |
| `c_d_g` | d, s, b | g | PIN_H "15+5": S/D and B driven together |
| `c_oxide` (LV) | b | g | sweep = V(B) - V(G); S/D floating for AC, tied to B for DC |
| pnpMPA `cbe` | b | e | c AC ground |
| pnpMPA `cbc` | b | c | the file's `vbc` is -V(B): sweep sign inverted |

Header corrections (`cv_file_overrides`, logged per file): lv_pmos `Cgds1`/`Cgdsb1` L = 130 nm and
`Cgds3`/`Cgdsb3` L = 10 um (the headers say 250 nm; with these the structures match their
`Cbdsg1/3` twins), hv_nmos `Cgdsb2` NF = 40, pnpMPA DUT16 m = 12000. The HV `c_oxide` files
contain only zeros and are not judged; the pnpMPA "single" files (array / 12000) and the
"Vorlage" templates are excluded.

## MOS Junction Diodes and pnpMPA Geometry

**Junction diodes (`di_bd_*`, `di_bs_*`).** These structures are a single junction; their output
`ib` is the current at the junction-terminal SMU (header `ib I GROUND D SMU1` / `... S SMU3`), not
at the bulk. `configs/mos/diode_template.spice.j2` (selected per group with `setup_templates`)
puts D, G and S of the PDK transistor on the swept junction node, so the stand-in channel carries
no current and its gate oxide sees no voltage, reports the current into that node as `ib`, and
keeps `as` above 0 (1e-30) so the subcircuit uses the header's drain area instead of recomputing
the geometry from W.

**pnpMPA DUTs.** `constants.DUTS` holds, per DUT, the emitter area/perimeter (`a`, `p`) and the
n-well area/perimeter (`ac`, `pc`), all passed to the subcircuit. DUT1-12 follow the setup
document; DUT5, 9, 13, 14, 15 and every n-well come from the layout
`test_structures/T323_pnpMPA_DC_all.gds` (which reproduces the documented DUTs exactly). DUT3 is
excluded: its measured IC is 5 % of the area/perimeter scaling of the other DUTs. An unknown DUT
stops the run instead of getting a default geometry.

## MOS Error EDA (ML Clustering + Report)

Milestone M3 adds an offline error-analysis pipeline for the four MOS devices
(`nmos_lv`, `pmos_lv`, `nmos_hv`, `pmos_hv`) that goes beyond pass/fail: it clusters
*where* and *why* the model disagrees with measurement, and proposes valid ranges —
mirroring the HBT MQA "valid window" methodology, but derived from data instead of a
PDF.

```bash
make eda-nmos_lv        # single device
make eda-mos            # all 4 MOS devices
```

Pipeline (`models_verifier/eda/`), reading `models_results/<toolchain>/<device>/combined_results/*.csv`
and `final_reports/full_results.csv` (already produced by `make test-<device>`):
1. **`error_features.py`** — per-point absolute/relative/log-domain error features vs
   TT (id/is/ib/ig), tagged with region (subthreshold/linear/saturation), bias, W/L, and
   FF/SS envelope containment.
2. **`cluster.py`** — standardizes features and clusters error patterns with
   **scikit-learn** (KMeans + DBSCAN, picked via silhouette score); flags outlier
   *measurements* via IQR / z-score / IsolationForest.
3. **`llm_labeler.py`** — names each cluster with a physical failure theme (e.g.
   subthreshold leakage, high-Vds avalanche, low-current measurement noise), proposes a
   valid range per metric/region, and explains flagged outliers. Results are **cached to
   `eda_report/<device>/labels.json`**; the default/CI path uses a deterministic
   rule-based labeler (no network), so the pipeline is fully reproducible offline. An
   LLM-backed labeler can be enabled explicitly (`EDA_USE_LLM=1` + API key) without
   changing the offline default.
4. **`report.py`** — renders `eda_report/<device>/report.md` (named cluster table,
   proposed valid-range table per metric/region, outlier-measurement list keyed by
   `input_data` + bias coordinates) plus matplotlib/seaborn figures (error
   distributions, error-vs-bias, cluster scatter).

`eda_report/` is **gitignored** — it is regenerated by `make eda-mos` / `make eda-<device>`,
never committed.

---

## Bias Fidelity and Current-Sign Conventions

These framework rules keep the simulated bias and the compared quantities faithful to the
measurement:

- **IC-CAP `SYNC` inputs.** An MDM input declared as `vc ... SYNC 1 <offset> vb` is driven
  point-by-point as `vc = vb + offset` (forward Gummel at constant VCB: `fg_vcb0`,
  `fg_vcbm05`, `fg_vcb05`, ...). The parser keeps the master (`vb`) as the sweep variable
  and records the relation for the slave (`sync 1 <offset> vb` in the compact sweep table);
  the DC runner then renders the slave's source **tied to the master node**
  (`Vc c b <offset>`) instead of a constant. Only ratio 1 between two node voltages is
  supported; anything else is reported as a simulation error. (Before this, the slave was
  held at 0 V and every constant-VCB Gummel sweep was simulated with VBE = 0.)
- **Sweeps that cross 0 V run as two segments from 0 V outward** (e.g. `-1..1.04 V` becomes
  `0..-1` and `0..1.04`, HBT and pnpMPA templates, with `reset` between the two so the second
  segment starts from a fresh circuit); the runner concatenates the two output files. Starting a
  DC sweep at an extreme bias (VBE = VCB = -1 V with the substrate at 0 V) can fail to converge.
- **A corner that aborts part-way keeps the points that did converge.** The runner logs a
  `WARNING` naming the file, block, corner and the simulated range instead of dropping the
  whole characteristic for every corner. The measured/simulated merge keeps every measured
  point (left join): a point without a simulated value fails its curve (`n_missing`); a curve
  without any simulated point is `Failed (not simulated)`.
- **Sign-preserving current clipping.** `clip_curr` floors `|I|` while keeping the sign
  (`-3e-13 -> -clip_curr`). Currents that are negative by convention (PMOS drain current,
  NMOS source current, pnp base/collector currents, HBT reverse-mode base current) are
  therefore compared for real instead of collapsing onto the floor on both sides. Points
  where the measured value and both corner bounds all sit at the floor are scored as
  agreement ("unmeasurably small" on both sides), so the random sign of pA noise does not
  produce failures (`n_floor` in `full_results.csv` counts them).
- **`design_param_overrides`** (per-device YAML, optional) forces design-parameter columns
  (`Nx`, `W`, `L`, `M`) to declared values on both the DC and the S-param path, e.g. when an
  MDM `REMARKS` field disagrees with the documented MQA variant
  (`configs/hbt/npn13g2l/npn13g2l.yaml`: `Nx: 4`). Overrides are logged as warnings.

## Continuous Integration

`.github/workflows/device-testing.yml` runs on a push to `device_models_testing`, on pull requests that
touch the device tests, the ngspice models or the Verilog-A sources, and on demand (`workflow_dispatch`, available
once the workflow file is on the repository's default branch).
It is thin by design: every step calls a script in `tools/` or a make target, which run the same way locally.

| job | what it does |
|---|---|
| `plan` | `tools/ci_matrix.py` turns `toolchain.lock` into the job matrices (2 ngspice versions, 2 OpenVAF-Reloaded commits, one test job per make target and toolchain) |
| `ngspice` | builds each pinned ngspice version once (`tools/toolchain.py build ngspice <ver>`), cached |
| `openvaf` | builds each pinned OpenVAF-Reloaded commit and compiles PSP103 with it (`tools/toolchain.py osdi <id>`); both cached, nothing is built when the PSP103 objects are cached |
| `unit-tests` | `make unit-tests` and `make check-deembedding` (no simulation) |
| `tests` | one job per (toolchain, target): `make <target> TOOLCHAIN=<id>`, the job summary from `tools/ci_summary.py`, the `final_reports/` as an artifact |

The MOS targets (PSP103 through OSDI) and `test-cv` run on all four toolchains; the HBT and pnpMPA
targets (models built into ngspice) run once per ngspice version. The caches are keyed on
`toolchain.lock`, `tools/ci_setup.sh` and the runner image (and the PSP103 sources for the objects), so a
pin change rebuilds them; raise `cache_version` in `toolchain.lock` after a change of the build steps. A test
job fails on a new failure (no exactly matching exception in `waivers/`), a simulation error, or when an exception names a curve that is not in the run (lost coverage). The job summary
gives the counts per run (waived curves counted as failures), lists every new failure and the toolchain record
(ngspice version, PSP103 object hash); every failure, waived or not, is in the uploaded `final_reports/`.

These summaries provide a concise view of how the model performs across all targets and conditions.
