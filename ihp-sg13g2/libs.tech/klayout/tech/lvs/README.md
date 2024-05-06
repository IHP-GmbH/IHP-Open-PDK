Klayout-LVS
===========

Explains how to use the SG13G2 LVS rule decks.

# Table of contents
- [Klayout-LVS](#klayout-lvs)
- [Table of contents](#table-of-contents)
  - [Folder Structure](#folder-structure)
  - [Prerequisites](#prerequisites)
  - [Devices Status](#devices-status)
  - [Usage](#usage)
    - [CLI](#cli)
      - [LVS Outputs](#lvs-outputs)
    - [GUI](#gui)


## Folder Structure

```text
📁 lvs
 ┣ 📁testing               Testing environment directory for SG13G2 LVS. 
 ┣ 📁rule_decks            Holds all LVS rule decks used for SG13G2.
 ┣ sg13g2.lvs              Main LVS runset that call all rule decks.
 ┣ 📜README.md             This file to document LVS for SG13G2.
 ┗ 📜run_lvs.py            Main python script used for SG13G2 LVS.
 ```

## Prerequisites

You need the following set of tools installed to be able to run SG13G2 LVS:

At a minimum:

- Python 3.9+
- KLayout 0.28.14+

## Installation

To install the required Python packages, execute the following command:

```bash
pip install -r ../../../../../requirements.txt
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


## Usage

You have the option to execute the SG13G2-LVS through either a Python script via the command-line interface [CLI](#cli) or by the Klayout graphical user interface [GUI](#gui), as detailed in the subsequent usage sections.

### CLI

The `run_lvs.py` script takes your gds and netlist files to run LVS rule decks with switches to select subsets of all checks.

```bash
    run_lvs.py (--help| -h)
    run_lvs.py (--layout=<layout_path>) (--netlist=<netlist_path>) [--thr=<thr>]
    [--run_dir=<run_dir_path>] [--topcell=<topcell_name>] [--run_mode=<run_mode>]
    [--lvs_sub=<sub_name>] [--no_net_names] [--spice_comments] [--schematic_simplify]
    [--net_only] [--top_lvl_pins] [--combine] [--purge] [--purge_nets] [--verbose]
```

**Options:**

- `--help -h `                        Print this help message.

- `--layout=<layout_path>`            The input GDS file path.

- `--netlist=<netlist_path>`          The input netlist file path.

- `--thr=<thr>`                       The number of threads used in run.

- `--run_dir=<run_dir_path>`          Run directory to save all the results [default: pwd]

- `--topcell=<topcell_name>`          Topcell name to use.

- `--run_mode=<run_mode>`             Select Allowed klayout mode. (flat, deep). [default: flat]

- `--lvs_sub=<sub_name>`              Substrate name used in your design.

- `--no_net_names`                    Discard net names in extracted netlist.

- `--spice_comments`                  Enable netlist comments in extracted netlist.

- `--net_only`                        Enable netlist object creation for extracted netlist.

- `--top_lvl_pins`                    Enable top level pins only for extracted netlist.

- `--no_simplify`                     Disable layout simplification for extracted netlist.

- `--combine`                         Enable netlist combination for extracted netlist.

- `--purge`                           Enable netlist purge all for extracted netlist.

- `--purge_nets`                      Enable netlist purge nets for extracted netlist.

- `--schematic_simplify`              Enable schematic simplification for input netlist.

- `--verbose`                         Detailed rule execution log for debugging.

**Example:**

```bash
    python3 run_lvs.py --layout=testing/testcases/unit/mos_devices/layout/sg13_lv_nmos.gds --netlist=testing/testcases/unit/mos_devices/netlist/sg13_lv_nmos.cdl --run_dir=test_nmos
```

#### LVS Outputs

You could find the run results at your run directory if you previously specified it through `--run_dir=<run_dir_path>`. Default path of run directory is `lvs_run_<date>_<time>` in current directory.

**Folder Structure of run results**

```text
📁 lvs_run_<date>_<time>
 ┣ 📜 lvs_run_<date>_<time>.log
 ┗ 📜 <your_design_name>.cir
 ┗ 📜 <your_design_name>.lvsdb
 ```

The outcome includes a database file for each device (`<device_name>.lvsdb`) containing LVS extractions and comparison results. You can view it by opening your gds file with: `klayout <device_name>.gds -mn <device_name>.lvsdb`. Alternatively, you can visualize it on your GDS file using the netlist browser option in the tools menu of the KLayout GUI as illustrated in the following figures.

<p align="center">
  <img src="images/lvs_marker_1.png" width="50%" >
</p>
<p align="center">
  Fig. 1. Netlist Browser for Klayout-LVS
</p>

After selecting Netlist Browser option, you could load the database file and visualize the LVS results.

<p align="center">
  <img src="images/lvs_marker_2.png" width="70%" >
</p>
<p align="center">
  Fig. 2. Loading LVS Netlist/database file - 1
</p>

<p align="center">
  <img src="images/lvs_marker_3.png" width="70%" >
</p>
<p align="center">
  Fig. 3. Loading LVS Netlist/database file - 2
</p>

<p align="center">
  <img src="images/lvs_marker_4.png" width="70%" >
</p>
<p align="center">
  Fig. 4. Visualize LVS results
</p>

Additionally, you can find the extracted netlist generated from your design at (`<device_name>_extracted.cir`) in the output run directory.

### GUI

The SG13G2 also facilitates LVS execution via Klayout menus as depicted below:

First, you need to add the LVS menus to your `KLAYOUT_PATH`, you could do that by executing the following command:

```bash
KLAYOUT_PATH=$PDKPATH/libs.tech/klayout:$PDKPATH/libs.tech/klayout/tech/ klayout -e
```

> **_NOTE:_** In this context, `PDKPATH` refers to the path leading to the IHP-Open-PDK/ihp-sg13g2 directory within the current repository.


Then, you will get the LVS menus for SG13G2, you could set your desired options as shown below:

> **_NOTE:_**  You need to select the path of the netlist will be used in the LVS run. If no path is specified, the tool will automatically search for the netlist file in the same directory as the layout file, considering files with the extensions .cdl, .spice, or .cir and has same name of the layout file.

<p align="center">
  <img src="images/lvs_menus.png" width="60%" >
</p>
<p align="center">
  Fig. 5. Visualization of LVS results on Klayout-GUI
</p>

Finally, you could run the LVS using `Run Klayout LVS` option.

Upon executing the LVS, the result database will appear on your layout interface, allowing you to verify the outcome of the run similarly as shown above in Fig. 4.
