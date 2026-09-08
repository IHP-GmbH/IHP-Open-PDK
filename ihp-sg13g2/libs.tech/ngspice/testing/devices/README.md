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
  - [Waiver / Baseline Workflow](#waiver--baseline-workflow)
    - [How waiving works](#how-waiving-works)
    - [Generating and reviewing waivers](#generating-and-reviewing-waivers)
  - [HBT S-Parameter Characteristics (CjE, CjC, fT)](#hbt-s-parameter-characteristics-cje-cjc-ft)
    - [Extraction equations](#extraction-equations)
    - [Simulated side](#simulated-side)
    - [Running the S-param tests](#running-the-s-param-tests)
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
 ┃  ┣ 📁 waivers           Waiver store + generator (Milestone M2)  
 ┃  ┣ 📁 eda               MOS error EDA / ML clustering / report generation (Milestone M3)  
 ┃  ┣ 📁 sp_runner         HBT S-parameter (CjE/CjC/fT) sim + verifier (Milestone M4)  
 ┃  ┗ 📁 mdm_processing     MDM parsing, aggregation, and S-param deembedding  
 ┣ 📁 waivers              Committed per-device YAML waiver ("known failure baseline") files  
 ┣ 📁 validation           Validation plotting helpers and analysis scripts  
 ┣ 📁 workflow_notebooks   Step-by-step notebooks for running and visualizing the verification flow  
 ┗ 📜 README.md            Documentation for SG13G2 models testing (this file)  
```

Two directories are **generated at run time and gitignored** (never committed): `models_results/<device>/` (Makefile `test-*`/`test-*-sparam` targets) and `eda_report/<device>/` (`eda-*` targets) — see [Output Results](#output-results), [HBT S-Parameter Characteristics](#hbt-s-parameter-characteristics-cje-cjc-ft), and [MOS Error EDA](#mos-error-eda-ml-clustering--report) below.

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

#### Device Configurations

Each Makefile target corresponds to one of the YAML configuration files under the [configs directory](configs/).  
For example:
- `make test-nmos_lv` → uses `configs/mos/sg13_lv_nmos.yaml`
- `make test-npn13g2` → uses `configs/hbt/sg13g2_npn13g2.yaml`

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
- **Waiver targets** (`waive-all`, `waive-hbt-sparam`) — see
  [Waiver / Baseline Workflow](#waiver--baseline-workflow).
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
| `full_results.csv` | The complete dataset combining measured and all simulated results. Includes a `status` column (`Passed` / `Passed (Waived)` / `Failed`) — see [Waiver / Baseline Workflow](#waiver--baseline-workflow). |
| `results_summary.csv` | Aggregated statistics showing pass/fail counts and out-of-bounds (OOB) rates. |
| `failed_results.csv` | Only entries that failed tolerance criteria (non-waived `Failed` rows). |
| `new_failures.csv` | `Failed` rows whose waiver key has **no** waiver entry, or whose current `percentage_oob` is **worse** than its waiver's snapshot + margin — i.e. genuinely NEW or WORSE diffs. Empty when every current diff is waived. |
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

---

## Waiver / Baseline Workflow

Even a well-tuned compact model has *some* known, already-reviewed sim-vs-measurement
gaps (measurement noise, corner-region artifacts, etc.). The waiver system lets CI stay
**green** for those known gaps while still catching **new** or **worse** ones — modeled
on the DRC regression waiver design (`run_regression_cells.py::build_waived_tests`,
`actual ⊆ allowed → waived`).

### How waiving works

- Each device has a committed YAML file at `waivers/<device_name>.yaml` (device name
  from the config's `device_name`, e.g. `npn13g2`, `sg13_lv_nmos`, `pnpMPA` — not
  necessarily the Makefile target name), keyed on the **stable** tuple
  `(device, input_data, block_index, metric, target)`. `block_id` (a per-run `uuid4`)
  is deliberately **not** part of the key, since it isn't stable across runs.
- Each waiver entry records `reason`, `snapshot_percentage_oob`,
  `snapshot_deviation_max`, `margin`, and `date`.
- After `range_checker.analyze()`, every range-check row gets a `status` column:
  `Passed`, `Passed (Waived)`, or `Failed`. A `Failed` row is flipped to
  `Passed (Waived)` **only if** its key has a waiver entry **and** its current
  `percentage_oob` is no worse than `snapshot_percentage_oob + margin` — a regression
  beyond that stays `Failed` even though a waiver entry exists for that key.
- Exit code / summary counts only count **non-waived** `Failed` rows, so
  `make test-<device>` exits `0` once all current diffs are waived.
- Every run writes `models_results/<device>/final_reports/new_failures.csv` — the set of
  `Failed` rows that are NOT covered by an (adequate) waiver. Empty file → nothing new.

### Generating and reviewing waivers

```bash
# Snapshot ALL current Failed rows for one device into waivers/<device>.yaml:
python -m models_verifier.waivers.generate --device npn13g2

# Or, via the Makefile, for all 8 devices at once:
make waive-all
```

Typical review loop:
1. `make test-all` (or a single `make test-<device>`) — inspect
   `final_reports/failed_results.csv` / `new_failures.csv` for the device(s) you're
   about to baseline.
2. `make waive-all` (or run the generator for a single device) once the current failures
   have been reviewed and accepted as a known baseline.
3. Re-run `make test-all` — exit code `0`, summary shows `Passed (Waived)` counts,
   `new_failures.csv` is empty.
4. Commit the updated `waivers/*.yaml`.

If a config change (or a real model regression) makes a previously-waived row *worse*
than its snapshot, that row is **not** silently kept green — it reverts to `Failed` and
reappears in `new_failures.csv`, and the device's `make test-<device>` exits `1` again.
This is what the CI `tests` job relies on: waived devices are green; a genuinely new or
worse diff turns that device's job red.

---

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

# Snapshot current S-param Failed rows into waivers/sparam/<device>.yaml
# (kept separate from the DC `waivers/*.yaml` so `make waive-all` can't clobber them):
make waive-hbt-sparam
```

Results land under `models_results/<device>/sparam/` (separate from the DC
`combined_results/` / `final_reports/` trees, same file layout otherwise), and are
range-checked meas-vs-sim using the same M1 bias-window (`sparam_mqa_ranges`) and M2
waiver mechanisms as the DC metrics. See `sparam_files`, `sparam_metrics`, and
`sparam_mqa_ranges` in `configs/hbt/*/*.yaml` for the exact wiring.

---

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

Pipeline (`models_verifier/eda/`), reading `models_results/<device>/combined_results/*.csv`
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

## Continuous Integration

`.github/workflows/device-testing.yml` runs three jobs on every push/PR:

1. **`build`** — installs the OS/build toolchain, builds ngspice with OSDI support,
   installs OpenVAF, and compiles the Verilog-A models to `.osdi` (cached across runs).
2. **`tests`** *(matrix, `needs: build`)* — one job per `matrix.case`, each simply
   running `make test-${{ matrix.case }}` in `$DEV`. The matrix covers all 8 DC device
   targets plus the 3 HBT S-param targets:
   `nmos_lv, pmos_lv, nmos_hv, pmos_hv, pnp_mpa, npn13g2, npn13g2l, npn13g2v,
   npn13g2-sparam, npn13g2l-sparam, npn13g2v-sparam` — every entry maps 1:1 to a
   `test-<case>` Makefile target. Because the committed `waivers/*.yaml` /
   `waivers/sparam/*.yaml` baseline every currently-known gap (see
   [Waiver / Baseline Workflow](#waiver--baseline-workflow)), each case exits `0`
   (green) as long as nothing has regressed; a NEW or WORSE diff makes that one case's
   job exit `1` (red) without affecting the other, independent matrix jobs
   (`fail-fast: false`).
3. **`eda`** *(`needs: build`)* — generates the MOS `combined_results/` (`make
   test-mos`) and then runs `make eda-mos`, uploading `eda_report/` as a build artifact
   (`actions/upload-artifact`). This job is **analysis, not a pass/fail gate**: its EDA
   step runs with `continue-on-error: true` so a clustering/report failure does not turn
   the overall workflow red, while still surfacing a `::warning::` annotation and
   whatever partial `eda_report/` output exists as an artifact for inspection.

`pip install -r requirements.txt` (both jobs that need it) installs `scikit-learn` and
`scikit-rf` along with the existing deps, so the waiver, EDA, and S-param code paths all
have what they need in CI.

These summaries provide a concise view of how the model performs across all targets and conditions.
