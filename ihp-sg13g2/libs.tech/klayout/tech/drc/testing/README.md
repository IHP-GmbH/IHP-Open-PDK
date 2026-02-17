IHP-SG13G2 DRC Testing
======================

Explains how to test SG13G2 DRC rule decks.

# Table of contents

- [IHP-SG13G2 DRC Testing](#ihp-sg13g2-drc-testing)
- [Table of contents](#table-of-contents)
  - [Folder Structure](#folder-structure)
  - [**Prerequisites**](#prerequisites)
  - [Installation](#installation)
  - [**Usage Guide**](#usage-guide)
    - [🧪 Golden Results (For Developers Only)](#-golden-results-for-developers-only)
    - [🔁 Regression Testing](#-regression-testing)
  - [DRC Regression Outputs](#drc-regression-outputs)
    - [📁 Folder Structure of regression run results](#-folder-structure-of-regression-run-results)
    - [🧾 Output Regression Log](#-output-regression-log)
      - [📋 Sample Regression Output](#-sample-regression-output)
      - [📊 Explanation of Result Columns](#-explanation-of-result-columns)
      - [✅ Summary Insights](#-summary-insights)
  - [Cells Regression Testing](#cells-regression-testing)
    - [DRC Cells Regression Outputs](#drc-cells-regression-outputs)
      - [📁 Folder Structure of regression run results](#-folder-structure-of-regression-run-results-1)
      - [🧾 Output Cells Regression Log](#-output-cells-regression-log)

## Folder Structure

```text
📁 testing
 ┣ 📜README.md                       This file to document the regression.
 ┣ 📜run_regression.py               Main regression script used for DRC testing.
 ┣ 📁testcases                       All testcases used in regression.
 ```

## **Prerequisites**

You need the following set of tools installed to be able to run SG13G2 DRC regression:

- Python 3.9+
- KLayout 0.30.3+

We have tested this using the following setup:
- Python 3.9.18
- KLayout 0.30.3

## Installation

To install the required Python packages, execute the following command:

```bash
pip install -r ../../../../../requirements.txt
```

## **Usage Guide**

### 🧪 Golden Results (For Developers Only)

> **Note:** This section is intended for *developers*. If you are an end user, you can safely ignore it.

Golden unit tests are generated for all implemented and verified DRC rules and are stored in the [Golden Unit](./testcases/unit_golden/) directory. These serve as the reference ("golden") results to validate the correctness of the DRC implementation.

To regenerate golden results based on the current rule implementation, use the following script:

```bash
    gen_golden.py (--help | -h)
    gen_golden.py [--table_name=<table_name>] [--run_dir=<dir>] [--mp=<num>] [--keep]

Options:
  -h, --help            show this help message and exit
  --table_name TABLE_NAME
                        Target rule table name to generate golden results for.
  --run_dir RUN_DIR     Directory to store output. If not specified, a timestamped folder will be created.
  --mp MP               The number of cores used in the run. [default: 1]
  --keep                Keep output logs and intermediate files after processing.
```

**Example:**

```bash
python3 gen_golden.py --table_name=activ --run_dir=testcases/unit_golden
```

---

### 🔁 Regression Testing

Use the regression script to validate current rule outputs against the golden references.

```bash
    run_regression.py (--help | -h)
    run_regression.py [--run_dir=<run_dir>] [--table_name=<table_name>] [--mp=<num>]

Options:
  -h, --help            show this help message and exit
  --run_dir RUN_DIR     Run directory to save all the results. If not provided, a timestamped directory will be created.
  --table_name TABLE_NAME
                        Target specific rule table to run.
  --mp MP               The number of parts to split the rule deck for parallel execution. [default: 1]
```

**Example:**

```bash
python3 run_regression.py --table_name=activ --run_dir=activ_regression
```

## DRC Regression Outputs

You could find the regression run results at your run directory if you previously specified it through `--run_name=<run_name>`. Default path of run directory is `unit_tests_<date>_<time>` in current directory.

### 📁 Folder Structure of regression run results

```text
📁 unit_tests_<date>_<time>
 ┣ 📜 unit_tests_<date>_<time>.log
 ┣ 📜 all_test_cases_results.csv
 ┗ 📜 rule_deck_rules.csv
 ┗ 📁 <table_name>
    ┣ 📜 drc_run_<date>_<time>.log  
    ┣ 📜 <table_name>_drc.log
    ┣ 📜 <table_name>_main_markers_merged_analysis.log
    ┣ 📜 <table_name>.drc                     
    ┣ 📜 <table_name>_main_analysis.drc  
    ┣ 📜 <table_name>_main.lyrdb        
    ┣ 📜 <table_name>_main_markers_merged_final.lyrdb
    ┣ 📜 <table_name>_main_markers.gds  
    ┣ 📜 <table_name>_main_markers_merged.gds
 ```

The result is a database file (`<table_name>_main_markers_merged_final.lyrdb`) contains all violations. 
You could view it on your file using: `klayout <table_name>_main_markers_merged.gds -m <table_name>_main_markers_merged_final.lyrdb`, or you could view it on your gds file via marker browser option in tools menu using klayout GUI.


### 🧾 Output Regression Log

After completing a DRC regression run, a summary log is generated that provides detailed insights into the comparison between the golden reference and the actual DRC results from the tested rule deck.

#### 📋 Sample Regression Output

```bash
15-Jun-2025 10:31:37 | INFO    | # Final analysis table:
  table_name rule_name  viol_not_golden  golden_not_viol  in_tests  in_rule_deck run_status rule_status
0      activ     Act.a                0                0         1             1  completed      Passed
1      activ     Act.b                0                0         1             1  completed      Passed

15-Jun-2025 10:31:37 | INFO    | # Failing test cases:
Empty DataFrame
Columns: [table_name, rule_name, viol_not_golden, golden_not_viol, in_tests, in_rule_deck, run_status, rule_status]
Index: []

15-Jun-2025 10:31:37 | INFO    | # All testcases passed.
15-Jun-2025 10:31:37 | INFO    | Test completed successfully.
15-Jun-2025 10:31:37 | INFO    | Total DRC Regression Run time: 8.26 seconds
```

---

#### 📊 Explanation of Result Columns

| Column Name         | Description                                                                                                                                          |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| table_name          | The name of the rule group or category. (e.g., activ, gatepoly, metal1, etc.)                                  |
| rule_name           | The specific name of the DRC rule being tested, as defined in the design rule manual.                               |
| viol_not_golden     | Count of violations found in the actual test result but not present in the golden reference. These are false positives.                             |
| golden_not_viol     | Count of violations found in the golden reference but missing from the actual result. These are false negatives.                                     |
| in_tests            | Indicates whether the rule exists in the unit test files (1 = present, 0 = missing).                                                                |
| in_rule_deck        | Indicates whether the rule is implemented in the current rule deck (1 = present, 0 = missing).                                                      |
| run_status          | Status of the individual test run (completed, not run, or other diagnostic states).                                                                  |
| rule_status         | Final regression result for this rule (Passed if matched expected results, otherwise Failed).                                                       |

---

#### ✅ Summary Insights

A successful DRC regression run typically shows:

- **No mismatches** between the test and golden results:
  - `viol_not_golden` = 0 for all rules (no unexpected violations).
  - `golden_not_viol` = 0 for all rules (no missing expected violations).
- **All rules pass**:  
  - Every `rule_status` should be `Passed`.
- **No failing test cases**:  
  - The `Failing test cases` section should be empty.


If mismatches are detected:

- **False positives** occur when a rule violates in the test but not in the golden reference (`viol_not_golden > 0`).
- **False negatives** occur when a rule is violated in the golden but missing in the test result (`golden_not_viol > 0`).


The regression also validates:

- **Test coverage**: Ensures each rule exists in the unit tests (`in_tests = 1`).
- **Rule deck integrity**: Confirms the rule is present in the rule deck (`in_rule_deck = 1`).

---

## Cells Regression Testing

Use the regression script to validate the SG13G2 cells (pr, io, std, sram)

```bash
Usage:
    run_regression_cells.py (--help | -h)
    run_regression_cells.py [--cell=<cell>] [--run_dir=<run_dir_path>] [--mp=<num>]

Options:
    --help -h                 Show this help message.
    --cell=<cell>             Run regression for a specific cell only.
    --run_dir=<run_dir_path>  Output directory to store results [default: pwd].
    --mp=<num>                Number of threads for parallel DRC runs.
```

**Example:**

To run all cells:

```bash
python3 run_regression_cells.py --run_dir=regression_cells_results
```

### DRC Cells Regression Outputs

You could find the regression run results at your run directory if you previously specified it through `--run_name=<run_name>`. Default path of run directory is `drc_cells_<date>_<time>` in current directory.

#### 📁 Folder Structure of regression run results

```text
📁 drc_cells_<date>_<time>
 ┣ 📜 drc_cells_<date>_<time>.log
 ┗ 📁 <cell_name>
    ┣ 📜 <cell_name>.gds
    ┣ 📜 <cell_name>_drc.log
 ┗ 📁 drc_run<cell_name>
    ┣ 📜 <cell_name>_*.lyrdb
    ┣ 📜 <cell_name>_*.log  
    ┣ ..
 ```

The result is a database file (`<cell_name>_*.lyrdb`) contains all violations. 
You could view it on your file as explained above.

#### 🧾 Output Cells Regression Log

After completing a DRC cells regression run, a summary log is generated that provides detailed insights into the DRC results from the tested rule deck.

```bash
16-Feb-2026 21:08:19 | INFO    | 📄 Saved results to: /home/runner/work/IHP-Open-PDK/IHP-Open-PDK/drc_cells_2026_02_16_21_00_15/all_test_cases_results.csv
16-Feb-2026 21:08:19 | INFO    | 🎉 All runnable DRC testcases passed successfully (some may be excluded or waived).
16-Feb-2026 21:08:19 | INFO    | Total execution time: 482.96s
```
