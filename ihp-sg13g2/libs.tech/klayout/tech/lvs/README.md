Klayout-LVS
===========

Explains how to use the SG13G2 LVS.

# Table of contents
- [Klayout-LVS](#klayout-lvs)
- [Table of contents](#table-of-contents)
  - [Folder Structure](#folder-structure)
  - [Prerequisites](#prerequisites)
  - [Devices Status](#devices-status)
  - [Usage](#usage)
    - [CLI](#cli)
      - [Options](#options)
      - [LVS Outputs](#lvs-outputs)


## Folder Structure

```text
📁 lvs
 ┣ 📁testing                        Testing environment directory for SG13G2 LVS. 
 ┣ 📁rule_decks                     All LVS rule decks used in SG13G2.
 ┣ generic_tech.lvs                 Main LVS runset that call all rule decks.
 ┣ 📜README.md                      This file to document the LVS run for SG13G2.
 ┗ 📜run_lvs.py                     Main python script used for SG13G2 LVS.
 ```

## Prerequisites
You need the following set of tools installed to be able to run SG13G2 LVS:

- Python 3.9+
- KLayout 0.28.14+

## Devices Status

The following table explains the list of available SG13G2 devices we have supported in our LVS runset.

| Device Category | Device Name | Tested            |
|-----------------|-------------|-------------------|
| MOSFET          | nmos        |                   |
| Capacitors      | cap_cmim    |:white_check_mark: |

## Usage

You have the option to execute the SG13G2-LVS through either a Python script via the command-line interface [CLI](#cli) or by the Klayout graphical user interface [GUI](#gui), as detailed in the subsequent usage sections.

### CLI

The `run_lvs.py` script takes your gds and netlist files to run LVS rule decks with switches to select subsets of all checks.

```bash
    run_lvs.py (--help| -h)
    run_lvs.py (--layout=<layout_path>) (--netlist=<netlist_path>) [--thr=<thr>]
    [--run_dir=<run_dir_path>] [--topcell=<topcell_name>] [--run_mode=<run_mode>]
    [--verbose] [--lvs_sub=<sub_name>] [--no_net_names] [--spice_comments] [--scale]
    [--schematic_simplify] [--net_only] [--top_lvl_pins] [--combine] [--purge] [--purge_nets]
```

#### Options

- `--help -h`                           Print this help message.

- `--layout=<layout_path>`              The input GDS file path.

- `--netlist=<netlist_path>`            The input netlist file path.

- `--thr=<thr>`                         The number of threads used in run.

- `--run_dir=<run_dir_path>`            Run directory to save all the results [default: pwd]

- `--topcell=<topcell_name>`            Topcell name to use.

- `--run_mode=<run_mode>`               Select Allowed klayout mode. (flat, deep). [default: flat]

- `--verbose`                           Detailed rule execution log for debugging.

- `--lvs_sub=<sub_name>`                Substrate name used in your design.

- `--no_net_names`                      Discard net names in extracted netlist.

- `--spice_comments`                    Enable netlist comments in extracted netlist.

- `--scale`                             Enable scale of 1e6 in extracted netlist.

- `--schematic_simplify`                Enable schematic simplification in input netlist.

- `--net_only`                          Enable netlist object creation only in extracted netlist.

- `--top_lvl_pins`                      Enable top level pins only in extracted netlist.

- `--combine`                           Enable netlist combine only in extracted netlist.

- `--purge`                             Enable netlist purge all only in extracted netlist.

- `--purge_nets`                        Enable netlist purge nets only in extracted netlist.


#### LVS Outputs

You could find the run results at your run directory if you previously specified it through `--run_dir=<run_dir_path>`. Default path of run directory is `lvs_run_<date>_<time>` in current directory.

**Folder Structure of run results**

```text
📁 lvs_run_<date>_<time>
 ┣ 📜 lvs_run_<date>_<time>.log
 ┗ 📜 <your_design_name>.cir
 ┗ 📜 <your_design_name>.lvsdb
 ```
<!-- 
The result is a database file (`<your_design_name>.lvsdb`) contains LVS extractions and comparison results.
You could view it on your file using: `klayout <input_gds_file> -mn <resut_db_file> `, or you could view it on your gds file via netlist browser option in tools menu using klayout GUI as shown below.

<p align="center">
  <img src="../../images/lvs_marker.png" width="60%" >
</p>
<p align="center">
  Fig. 1. Klayout GUI netlist browser
</p>

After selecting Netlist Browser option, you could load the database file and visualize the LVS results.

<p align="center">
  <img src="../../images/lvs_results.png" width="80%" >
</p>
<p align="center">
  Fig. 2. Visualization of LVS results on Klayout-GUI
</p>

You can also locate the extracted netlist generated from your design at `<your_design_name>.cir` within the output directory of the run.

### GUI

The SG13G2 also facilitates LVS execution via Klayout menus, integrated with Klayout through the PDK [installation](../../README.md#installation) as depicted below:

<p align="center">
  <img src="../../images/lvs_menus.png" width="60%" >
</p>
<p align="center">
  Fig. 3. Visualization of LVS results on Klayout-GUI
</p>

Upon executing the LVS using the `Run Klayout LVS` option, the result database will appear on your layout interface, allowing you to verify the outcome of the run similarly as shown above in Fig. 2.

## Demo-Example

The example shows a `sg13g2_and2_1` implemented using SG13G2 technology.

### Schematic

Figure 4 displays the device's [schematic](./testing/testcases/unit/lidar_device/lidar.sch) created using xschem.

<p align="center">
  <img src="../../images/sg13g2_and2_1_sch.png" width="80%" >
</p>
<p align="center">
  Fig. 4. Schematic for `sg13g2_and2_1` standard cell.
</p>

**Note**: The netlist will be produced in the selected output directory. It is recommended to launch the tool using the following command:

```bash
xschem sg13g2_and2_1.sch -o .
```

This command ensures that the output netlist is generated in the current directory.

Following that, you can generate the netlist from this schematic for LVS testing. This can be accomplished by using the 'netlist' option available in the xschem-GUI, as demonstrated in Figure 5.

<p align="center">
  <img src="../../images/netlist_ext.png" width="100%" >
</p>
<p align="center">
  Fig. 5. Netlist extraction step from xschem for `sg13g2_and2_1`.
</p>

The following netlist is generated from xschem:

```
```

### Layout

Figure 6 displays the device's [layout](./testing/testcases/unit/std_cells/sg13g2_and2_1.gds) created using Klayout.

<p align="center">
  <img src="../../images/sg13g2_and2_1_layout.png" width="100%" >
</p>
<p align="center">
  Fig. 5. Layout for and2_1 standard cell.
</p>

### LVS-Testing

#### CLI

```bash
    python3 run_lvs.py --layout=testing/testcases/unit/std_cells/sg13g2_and2_1.gds --netlist=testing/testcases/unit/std_cells/sg13g2_and2_1.cdl --run_dir=lvs_and2_1_run
```

Please refer to [Usage](#usage) section for more details.

#### GUI

You could also run the LVS using Klayout-Menus supported for SG13G2 as explained above in Fig. 3. -->
