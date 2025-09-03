# Models Run Outputs

This folder is the **output directory for device verification runs**.
Each device will create its own subfolder here when tests are executed using the Makefile or `models_verifier`.

# Table of contents

* [Models Run Outputs](#models-run-outputs)
* [Table of contents](#table-of-contents)

  * [Folder Structure Template](#folder-structure-template)
  * [Content Description](#content-description)


## Folder Structure Template

When populated, this folder will look like the following:

```text
📁 models_run
 ┣ 📁 <device_name>/
 ┃ ┣ 📁 netlists/              Generated ngspice netlists (if enabled in YAML).
 ┃ ┣ 📁 per_setup_mdm_csvs/    Merged CSVs per measurement/setup.
 ┃ ┣ 📁 per_setup_sim_vs_meas/ CSV comparisons of simulation vs measurement.
 ┃ ┗ 📁 verification_reports/  Aggregated pass/fail reports.
 ┗ 📜 README.md                Documentation (this file).
```

## Content Description

* **`netlists/`**
  Contains generated `.cir` netlists from templates.
  Only created if `generate_netlists: true` is set in the device YAML config.

* **`per_setup_mdm_csvs/`**
  Contains merged CSVs for each test setup, combining measurement and simulation data.

* **`per_setup_sim_vs_meas/`**
  Contains CSV comparisons between simulated and measured data (if applicable for the device).

* **`verification_reports/`**
  Final verification summaries:

  * `summary.csv` → Roll-up summary by metric/target
  * `full_report.csv` → Detailed results per block/metric
  * `detailed_failures.csv` → List of failing points (only if failures exist)

---

**Note**

* This folder is **initially empty**.
* Subfolders are created automatically the first time you run `make <device>`.

