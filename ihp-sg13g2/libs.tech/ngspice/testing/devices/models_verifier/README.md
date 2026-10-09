# Models Verifier

models_verifier is the **verification engine** for SG13G2 device testing.
It runs **measurement-vs-simulation comparisons** using ngspice, aggregates results, and checks them against tolerance thresholds.

# Table of contents

* [Models Verifier](#models-verifier)
* [Table of contents](#table-of-contents)

  * [Folder Structure](#folder-structure)
  * [Modules Overview](#modules-overview)


## Folder Structure

```text
📁 models_verifier
 ┣ 📜 models_verifier.py     CLI entrypoint (main script).
 ┣ 📜 constants.py           Shared constants for device configs and tests.
 ┣ 📁 dc_runner              Orchestrates ngspice DC simulations.
 ┃ ┣ 📜 dc_sweep_runner.py   Runs DC sweeps for each device.
 ┃ ┗ 📜 helper.py            Helper functions for building runs.
 ┣ 📁 error_analyzer         Handles tolerance and range checks.
 ┃ ┣ 📜 config.py            Defines thresholds and metric specs.
 ┃ ┗ 📜 range_checker.py     Core pass/fail logic for metrics.
 ┣ 📁 mdm_processing         Parses and aggregates measurement data (MDM format).
 ┃ ┣ 📜 parser.py            Reads MDM files into DataFrames.
 ┃ ┣ 📜 aggregator.py        Combines MDM blocks into compact/merged views.
 ┃ ┗ 📜 utils.py             Utility helpers for parsing and cleaning data.
 ┗ 📜 README.md              Documentation (this file).
```


## Modules Overview

* **`models_verifier.py`**
  CLI entrypoint. Loads YAML config, runs the full flow (parse → simulate → analyze → report).

* **`dc_runner/`**
  Interfaces with **ngspice**: builds `.cir` netlists from Jinja2 templates, runs sweeps, collects outputs.

* **`mdm_processing/`**
  Handles measurement data (MDM format). Provides parsers, aggregators, and utilities to align simulation with measurement.

* **`error_analyzer/`**
  Applies tolerance thresholds (percentage or count of out-of-range points). Generates pass/fail reports.

* **`constants.py`**
  Stores shared device mappings and case definitions used by verifier flows.
