# Globalfoundries 180nm MCU LVS Testing

Explains how to test GF180nm LVS rule decks.

## Folder Structure

```text
📁 testing
 ┣ 📜README.md                       This file to document the regression.
 ┣ 📜Makefile                        To make a full test for GF180nm LVS rule deck.
 ┣ 📜run_regression.py               Main regression script used for LVS testing.
 ┣ 📁testcases                       All testcases used in LVS regression.
 ```

## **Prerequisites**
You need the following set of tools installed to be able to run the regression:
- Python 3.6+
- KLayout 0.28.4+

We have tested this using the following setup:
- Python 3.9.12
- KLayout 0.28.5

## **Usage**

```bash
    run_regression.py (--help| -h)
    run_regression.py [--device_name=<device_name>] [--mp=<num>] [--run_name=<run_name>]
```

Example:

```bash
    python3 run_regression.py --device_name=MOS --run_name=mos_regression
```

### Options

- `--help -h`                           Print this help message.

- `--mp=<num>`                          The number of threads used in run.

- `--run_name=<run_name>`               Select your run name.
    
- `--device_name=<device_name>`         Target specific device.


To make a full test for GF180nm LVS rule deck, you could use the following command in testing directory:

```bash
make all
```

## **LVS Outputs**

You could find the regression run results at your run directory if you previously specified it through `--run_name=<run_name>`. Default path of run directory is `unit_tests_<date>_<time>` in current directory.

### Folder Structure of regression run results

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

The result is a database file for each device (`<device_name>.lvsdb`) contains LVS extractions and comparison results.
You could view it on your file using: `klayout <device_name>.gds -mn <device_name>.lvsdb`, or you could view it on your gds file via marker browser option in tools menu using klayout GUI.

You could also find the extracted netlist generated from your design at (`<device_name>.cir`) in your run directory.
