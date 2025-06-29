# SG13G2 LVS Testing

Explains how to test SG13G2 LVS rule decks.

## Folder Structure

```text
📁 testing
 ┣ 📜README.md                 This file documents the contents of the testing directory.
 ┣ 📜Makefile                  Used for testing the SG13G2 LVS rule deck.
 ┣ 📜run_regression.py         Main regression script for testing SG13G2 devices.
 ┣ 📜run_regression_cells.py   Main regression script for testing SG13G2 cells.
 ┣ 📁testcases                 Contains all test cases used for LVS testing.
 ```

## Prerequisites

At a minimum:

You need the following set of tools installed to be able to run the regression:
- Python 3.9+
- KLayout 0.29.0+

We have tested this using the following setup:
- Python 3.9.18
- KLayout 0.29.0

## Installation

To install the required Python packages, execute the following command:

```bash
pip install -r ../../../../../../requirements.txt
```

## Devices Status

The following table explains the list of available SG13G2 devices we have supported in our LVS runset.

| Device          | Tested           |
|-----------------|------------------|
| **MOSFET**      |                  |
| sg13_lv_nmos    |:white_check_mark:|
| sg13_hv_nmos    |:white_check_mark:|
| sg13_lv_pmos    |:white_check_mark:|
| sg13_hv_pmos    |:white_check_mark:|
| **RF-MOSFET**   |                  |
| rfnmos          |:white_check_mark:|
| rfnmosHV        |:white_check_mark:|
| rfpmos          |:white_check_mark:|
| rfpmosHV        |:white_check_mark:|
| **BJTs**        |                  |
| npn13G2         |:white_check_mark:|
| npn13G2L        |:white_check_mark:|
| npn13G2V        |:white_check_mark:|
| pnpMPA          |:white_check_mark:|
| **Diodes**      |                  |
| dantenna        |:white_check_mark:|
| dpantenna       |:white_check_mark:|
| schottky_nbl1   |:white_check_mark:|
| **Resistors**   |                  |
| rsil            |:white_check_mark:|
| rppd            |:white_check_mark:|
| rhigh           |:white_check_mark:|
| lvsres          |:white_check_mark:|
| **Capacitors**  |                  |
| SVaricap        |:white_check_mark:|
| cap_cmim        |:white_check_mark:|
| rfcmim          |:white_check_mark:|
| **ESD**         |                  |
| diodevdd_4kv    |:white_check_mark:|
| diodevdd_2kv    |:white_check_mark:|
| diodevss_4kv    |:white_check_mark:|
| diodevss_2kv    |:white_check_mark:|
| idiodevdd_4kv   |:white_check_mark:|
| idiodevdd_2kv   |:white_check_mark:|
| idiodevss_4kv   |:white_check_mark:|
| idiodevss_2kv   |:white_check_mark:|
| nmoscl_2        |:white_check_mark:|
| nmoscl_4        |:white_check_mark:|
| **Inductors**   |                  |
| inductor        |:white_check_mark:|
| inductor3       |:white_check_mark:|
| **Taps**        |                  |
| ptap1           |:white_check_mark:|
| ntap1           |:white_check_mark:|

## Devices Regression Usage

```bash
  run_regression.py (--help| -h)
  run_regression.py [--device=<device>] [--run_dir=<run_dir_path>] [--mp=<num>]
```

Example:

```bash
  python3 run_regression.py --device=MOS --run_dir=test_mos
```

**Options**

- `--help -h`                  Print this help message.
    
- `--device=<device>`          Select device category you want to run regression on.

- `--run_dir=<run_dir_path>`   Run directory to save all the results [default: pwd]

- `--mp=<num>`                 The number of threads used in run.


Another approach for testing SG13G2 devices, you could make a full test for SG13G2 LVS rule deck, by executing the following command in current testing directory:

```bash
  make test-LVS-main
```

## Cells Regression Usage

```bash
  run_regression_cells.py (--help| -h)
  run_regression_cells.py [--cell=<cell>] [--run_dir=<run_dir_path>] [--mp=<num>]
```

Example:

```bash
python3 run_regression_cells.py --cell=sg13g2_inv_1 --run_dir=test_inv
```

**Options**

- `--help -h`                  Print this help message.
    
- `--cell=<cell>`              Specify the cell to run; all cells run if not specified.

- `--run_dir=<run_dir_path>`   Run directory to save all the results [default: pwd]

- `--mp=<num>`                 The number of threads used in run.


Another approach for testing SG13G2 cells, you could make a full test for SG13G2 cells, by executing the following command in current testing directory:

```bash
  make test-LVS-cells
```


## LVS Outputs

You could find the regression run results at your run directory if you previously specified it through `--run_name=<run_name>`. Default path of run directory is `unit_tests_<date>_<time>` in the current testing directory.

**Folder Structure of regression run results**

```text
📁 unit_tests_<date>_<time>
 ┣ 📜 unit_tests_<date>_<time>.log
 ┣ 📜 all_test_cases_results.csv
 ┗ 📜 rule_deck_rules.csv
 ┗ 📁 <device_name>
    ┣ 📜 <device_name>_lvs.log
    ┣ 📜 <device_name>.gds
    ┣ 📜 <device_name>.cdl
    ┣ 📜 <device_name>_extracted.cir                     
    ┣ 📜 <device_name>.lvsdb
 ```

The outcome includes a database file for each device (`<device_name>.lvsdb`) containing LVS extractions and comparison results. You can view it by opening your gds file with: `klayout <device_name>.gds -mn <device_name>.lvsdb`. Alternatively, you can visualize it on your GDS file using the netlist browser option in the tools menu of the KLayout GUI as illustrated in [LVS-Output](../README.md#lvs-outputs).
