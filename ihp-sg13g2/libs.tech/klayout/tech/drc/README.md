Klayout-DRC
===========

Explains how to use the SG13G2 DRC rule decks.

# Table of contents
- [Klayout-DRC](#klayout-drc)
- [Table of contents](#table-of-contents)
  - [Folder Structure](#folder-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [CLI](#cli)
      - [DRC Outputs](#drc-outputs)
    - [GUI](#gui)


## Folder Structure

```text
📁 drc
 ┣ 📁images                         Directory for the SG13G2 DRC images.
 ┣ 📁testing                        Directory for the SG13G2 DRC testing environment.
 ┣ 📁rule_decks                     Contains all DRC rule decks used for SG13G2.
 ┣ 📜README.md                      Documentation for SG13G2 DRC.
 ┗ 📜run_drc.py                     Main Python script for SG13G2 DRC run.
 ```

## Prerequisites

You need the following set of tools installed to be able to run SG13G2 DRC:

- Python 3.9+
- KLayout 0.29.0+

We have tested this using the following setup:
- Python 3.9.18
- KLayout 0.30.1

## Installation

To install the required Python packages, execute the following command:

```bash
pip install -r ../../../../../requirements.txt
```

## Usage

You have the option to execute the SG13G2-DRC through either a Python script via the command-line interface [CLI](#cli) or by the Klayout graphical user interface [GUI](#gui), as detailed in the subsequent usage sections.

### CLI

The `run_drc.py` script takes your gds to run DRC rule decks with switches to select subsets of all checks.

```bash
    run_drc.py (--help| -h)
    run_drc.py (--path=<file_path>) [--table=<table_name>]... [--mp=<num_cores>] [--run_dir=<run_dir_path>]
    [--topcell=<topcell_name>] [--thr=<thr>] [--run_mode=<run_mode>] [--drc_json=<json_path>] [--no_feol]
    [--no_beol] [--MaxRuleSet] [--no_connectivity] [--density] [--density_only] [--antenna] [--antenna_only]
    [--no_offgrid] [--macro_gen]
```

**Example:**

```bash
    python3 run_drc.py --path=testing/testcases/unit/activ.gds --run_mode=deep --run_dir=test_activ
```

**Options:**

- `--help -h`                           Displays this help message.

- `--path=<file_path>`                  Specifies the file path of the input GDS file.

- `--topcell=<topcell_name>`            Specifies the name of the top cell to be used.

- `--table=<table_name>`                Specifies the name of the table on which to execute the rule deck.

- `--mp=<num_cores> `                   Run the rule deck in parts in parallel to speed up the run. [default: 1]

- `--run_dir=<run_dir_path>`            un directory to save all the generated results [default: pwd]

- `--thr=<thr>`                         Specifies the number of threads to use during the run.

- `--run_mode=<run_mode>`               Selects the allowed KLayout mode, (flat , deep, tiling). [default: deep]

- `--drc_json=<json_path>`              Path to the JSON file that contains the DRC rules values to be used.

- `--no_feol`                           Disables FEOL rules from running.

- `--no_beol`                           Disables BEOL rules from running.

- `--MaxRuleSet`                        Runs DRC using the complete rule deck.

- `--no_connectivity`                   Disables connectivity rules.

- `--density`                           Enables Density rules.

- `--density_only`                      Runs Density rules only.

- `--antenna`                           Enables Antenna checks.

- `--antenna_only`                      Runs Antenna checks only.

- `--no_offgrid`                        Disables OFFGRID checking rules.

- `--macro_gen`                         Generating the full rule deck without run.

> **Note**
> If the `--drc_json=<json_path>` option is not provided, the script will attempt to use the [SG13G2 tech JSON](../../python/sg13g2_pycell_lib/sg13g2_tech.json) file. If that file is missing, it will fall back to the [default tech DRC values](./rule_decks/default_drc_rules.json) file.

#### DRC Outputs

You could find the run results at your run directory if you previously specified it through `--run_dir=<run_dir_path>`. Default path of run directory is `drc_run_<date>_<time>` in current directory.

**Folder Structure of run results**

```text
📁 drc_run_<date>_<time>
 ┣ 📜 drc_run_<date>_<time>.log
 ┗ 📜 main.drc
 ┗ 📜 <your_design_name>.lyrdb
 ```

The outcome includes a database (`<your_design_name>.lyrdb`) containing DRC results. You can view it by opening your gds file with: `klayout <device_name>.gds -m <your_design_name>.lyrdb`. Alternatively, you can visualize it on your GDS file using the netlist browser option in the tools menu of the KLayout GUI as illustrated in the following figures.

<p align="center">
  <img src="images/drc_marker_1.png" width="50%" >
</p>
<p align="center">
  Fig. 1. Marker Browser for Klayout-DRC
</p>

After selecting Marker Browser option, you could load the database file and visualize the DRC results.

<p align="center">
  <img src="images/drc_marker_2.png" width="70%" >
</p>
<p align="center">
  Fig. 2. Loading DRC database file - 1
</p>

<p align="center">
  <img src="images/drc_marker_3.png" width="70%" >
</p>
<p align="center">
  Fig. 3. Loading DRC database file - 2
</p>

<p align="center">
  <img src="images/drc_marker_4.png" width="70%" >
</p>
<p align="center">
  Fig. 4. Visualize DRC results
</p>

### GUI

The SG13G2 also facilitates DRC execution via Klayout menus as depicted below:

First, you need to add the DRC menus to your `KLAYOUT_PATH`, you could do that by executing the following command:

```bash
KLAYOUT_PATH=$PDKPATH/libs.tech/klayout:$PDKPATH/libs.tech/klayout/tech/ klayout -e
```

> **_NOTE:_** In this context, `PDKPATH` refers to the path leading to the IHP-Open-PDK/ihp-sg13g2 directory within the current repository.

Then, you will get the DRC menus for SG13G2, you could set your desired options as shown below:

<p align="center">
  <img src="images/drc_menus_1.png" width="70%" >
</p>
<p align="center">
  Fig. 5. Setting up DRC Options-GUI - 1
</p>

<p align="center">
  <img src="images/drc_menus_2.png" width="50%" >
</p>
<p align="center">
  Fig. 6. Setting up DRC Options-GUI - 2
</p>

<p align="center">
  <img src="images/drc_menus_3.png" width="50%" >
</p>
<p align="center">
  Fig. 6. Setting up DRC Options-GUI - 2
</p>

For additional details on GUI options, please refer to the [CLI Options section](#cli).

Finally, after setting your option, you could execute the DRC using `Run Klayout DRC` from the dropdown menu.

<p align="center">
  <img src="images/drc_menus_4.png" width="70%" >
</p>
<p align="center">
  Fig. 7. Running DRC using Klayout menus
</p>

Upon executing the DRC, the result database will appear on your layout interface, allowing you to verify the outcome of the run.

<p align="center">
  <img src="images/drc_menus_5.png" width="80%" >
</p>
<p align="center">
  Fig. 7. Running DRC using Klayout menus
</p>

---
**NOTE**

The current SG13G2 DRC rules are categorized as follows:

- **Minimum Rule Set** – Refer to the [README](docs/MinList.md):  
  This set contains the essential DRC rules that are required for baseline verification. All rules in this category have been thoroughly verified, tested, and optimized for performance.

- **Maximum Rule Set** – Refer to the [README](docs/MaxList.md):  
  This set includes additional residual rules that are not part of the minimum set. These rules can be activated by using the `--MaxRuleSet` switch when executing the DRC. Please note that these rules have not been verified or tested.

- **Missing Rule Set** – Refer to the [README](docs/MissingList.md):  
  This set lists the DRC rules that have not yet been implemented.
---
