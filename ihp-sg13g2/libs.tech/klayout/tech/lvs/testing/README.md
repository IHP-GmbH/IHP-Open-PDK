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
- KLayout 0.30.2+

We have tested this using the following setup:
- Python 3.12.4
- KLayout 0.30.3

## Installation

To install the required Python packages, execute the following command:

```bash
pip install -r ../../../../../../requirements.txt
```

## LVS Schematic Syntax Reference

This table summarizes the supported schematic-side device syntax used by the LVS.

| Group | Device | Netlist Form | LVS-Checked Parameters | Note | Unit Test |
|---|---|---|---|---|---|
| **MOSFET** | `sg13_lv_nmos` | `MN1 D G S B sg13_lv_nmos w=150n l=130n m=1 ng=1` | `W`, `L`, `rfmode` | [`M1`](#note-m1) | [CDL](./testcases/unit/mos_devices/netlist/sg13_lv_nmos.cdl) / [GDS](./testcases/unit/mos_devices/layout/sg13_lv_nmos.gds) |
|  | `sg13_hv_nmos` | `MN1 D G S B sg13_hv_nmos w=0.6u l=0.45u m=1 ng=1` | `W`, `L`, `rfmode` | [`M1`](#note-m1) | [CDL](./testcases/unit/mos_devices/netlist/sg13_hv_nmos.cdl) / [GDS](./testcases/unit/mos_devices/layout/sg13_hv_nmos.gds) |
|  | `sg13_lv_pmos` | `MP1 D G S B sg13_lv_pmos w=150n l=130n m=1 ng=1` | `W`, `L`, `rfmode` | [`M1`](#note-m1) | [CDL](./testcases/unit/mos_devices/netlist/sg13_lv_pmos.cdl) / [GDS](./testcases/unit/mos_devices/layout/sg13_lv_pmos.gds) |
|  | `sg13_hv_pmos` | `MP1 D G S B sg13_hv_pmos w=0.3u l=0.4u m=1 ng=1` | `W`, `L`, `rfmode` | [`M1`](#note-m1) | [CDL](./testcases/unit/mos_devices/netlist/sg13_hv_pmos.cdl) / [GDS](./testcases/unit/mos_devices/layout/sg13_hv_pmos.gds) |
| **RF-MOSFET** | `rfnmos` | `MN1 D G S B sg13_lv_nmos rfmode=1 w=1.0u l=0.72u ng=1 m=1` | `W`, `L`, `rfmode` | [`RF1`](#note-rf1) | [CDL](./testcases/unit/rfmos_devices/netlist/rfnmos.cdl) / [GDS](./testcases/unit/rfmos_devices/layout/rfnmos.gds) |
|  | `rfnmosHV` | `MN1 D G S B sg13_hv_nmos rfmode=1 w=1.0u l=0.72u ng=1 m=1` | `W`, `L`, `rfmode` | [`RF1`](#note-rf1) | [CDL](./testcases/unit/rfmos_devices/netlist/rfnmoshv.cdl) / [GDS](./testcases/unit/rfmos_devices/layout/rfnmoshv.gds) |
|  | `rfpmos` | `MP1 D G S B sg13_lv_pmos rfmode=1 w=1.0u l=0.72u ng=1 m=1` | `W`, `L`, `rfmode` | [`RF1`](#note-rf1) | [CDL](./testcases/unit/rfmos_devices/netlist/rfpmos.cdl) / [GDS](./testcases/unit/rfmos_devices/layout/rfpmos.gds) |
|  | `rfpmosHV` | `MP1 D G S B sg13_hv_pmos rfmode=1 w=1.0u l=0.72u ng=1 m=1` | `W`, `L`, `rfmode` | [`RF1`](#note-rf1) | [CDL](./testcases/unit/rfmos_devices/netlist/rfpmoshv.cdl) / [GDS](./testcases/unit/rfmos_devices/layout/rfpmoshv.gds) |
| **BJT** | `npn13G2` | `Q1 C B E S npn13G2 le=900n we=70n Nx=1 m=1` | `we`, `le`, `m`, `Nx` | [`B1`](#note-b1) | [CDL](./testcases/unit/bjt_devices/netlist/npn13G2.cdl) / [GDS](./testcases/unit/bjt_devices/layout/npn13G2.gds) |
|  | `npn13G2L` | `Q1 C B E S npn13G2l le=1.0u we=70n Nx=1 m=1` | `we`, `le`, `m`, `Nx` | [`B1`](#note-b1) | [CDL](./testcases/unit/bjt_devices/netlist/npn13G2l.cdl) / [GDS](./testcases/unit/bjt_devices/layout/npn13G2l.gds) |
|  | `npn13G2V` | `Q1 C B E S npn13G2v le=1.0u we=120n Nx=1 m=1` | `we`, `le`, `m`, `Nx` | [`B1`](#note-b1) | [CDL](./testcases/unit/bjt_devices/netlist/npn13G2v.cdl) / [GDS](./testcases/unit/bjt_devices/layout/npn13G2v.gds) |
|  | `pnpMPA` | `Q1 C B E pnpMPA w=0.70u l=2.0u m=1` | `we`, `le`, `m` | [`B1`](#note-b1) | [CDL](./testcases/unit/bjt_devices/netlist/pnpMPA.cdl) / [GDS](./testcases/unit/bjt_devices/layout/pnpMPA.gds) |
| **Diode** | `dantenna` | `D1 A C SUB dantenna w=780n l=780n a=608.4f p=3.12u m=1` | `A`, `P`, `m` | [`D1`](#note-d1) | [CDL](./testcases/unit/diode_devices/netlist/dantenna.cdl) / [GDS](./testcases/unit/diode_devices/layout/dantenna.gds) |
|  | `dpantenna` | `D1 A C SUB dpantenna w=780n l=780n a=608.4f p=3.12u m=1` | `A`, `P`, `m` | [`D1`](#note-d1) | [CDL](./testcases/unit/diode_devices/netlist/dpantenna.cdl) / [GDS](./testcases/unit/diode_devices/layout/dpantenna.gds) |
|  | `schottky_nbl1` | `D1 A C SUB schottky_nbl1 m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/diode_devices/netlist/schottky_nbl1.cdl) / [GDS](./testcases/unit/diode_devices/layout/schottky_nbl1.gds) |
|  | `isolbox` | `D1 S I Bn isolbox l=6.0u w=6.0u` | `a`, `p` | [`I1`](#note-i1) | [CDL](./testcases/unit/diode_devices/netlist/isolbox.cdl) / [GDS](./testcases/unit/diode_devices/layout/isolbox.gds) |
| **Resistor** | `rsil` | `R1 N1 N2 SUB rsil w=0.5u l=0.5u b=0 m=1`<br>`or`<br>`R1 N1 N2 3.1583k $SUB=sub! $[rsil] w=0.5e-6 l=0.96e-6 b=0` | `w`, `l`, `ps`, `b`, `m` | [`R1`](#note-r1), [`R2`](#note-r2) | [CDL](./testcases/unit/res_devices/netlist/rsil.cdl) / [GDS](./testcases/unit/res_devices/layout/rsil.gds) |
|  | `rppd` | `R1 N1 N2 SUB rppd w=0.5u l=0.5u b=0 m=1`<br>`or`<br>`R1 N1 N2 3.1583k $SUB=sub! $[rppd] w=0.5e-6 l=0.96e-6 b=0` | `w`, `l`, `ps`, `b`, `m` | [`R1`](#note-r1), [`R2`](#note-r2) | [CDL](./testcases/unit/res_devices/netlist/rppd.cdl) / [GDS](./testcases/unit/res_devices/layout/rppd.gds) |
|  | `rhigh` | `R1 N1 N2 SUB rhigh w=0.5u l=0.96u b=0 m=1`<br>`or`<br>`R1 N1 N2 3.1583k $SUB=sub! $[rhigh] w=0.5e-6 l=0.96e-6 b=0` | `w`, `l`, `ps`, `b`, `m` | [`R1`](#note-r1), [`R2`](#note-r2) | [CDL](./testcases/unit/res_devices/netlist/rhigh.cdl) / [GDS](./testcases/unit/res_devices/layout/rhigh.gds) |
|  | `res_metal*`, `res_topmetal*` | `R1 N1 N2 res_metal1 l=1u w=5u R=20k`<br>`or`<br>`R1 N1 N2 20k $[res_metal1] l=1u w=5u` | `W`, `L` | [`R3`](#note-r3) | [CDL](./testcases/unit/res_devices/netlist/res_metal1.cdl) / [GDS](./testcases/unit/res_devices/layout/res_metal1.gds) |
| **Capacitor** | `cap_cmim` | `C1 PLUS MINUS cap_cmim w=6.99u l=6.99u m=1 C=74.620f`<br>`or`<br>`C1 PLUS MINUS 74.620f $[cap_cmim] w=6.99u l=6.99u m=1` | `w`, `l`, `m`, `A`, `P` | [`C1`](#note-c1) | [CDL](./testcases/unit/cap_devices/netlist/cap_cmim.cdl) / [GDS](./testcases/unit/cap_devices/layout/cap_cmim.gds) |
|  | `rfcmim` | `C1 N1 N2 SUB rfcmim w=7u l=7u wfeed=3u m=1 C=74.823f` | `w`, `l`, `m`, `A`, `P`, `wfeed` | [`C3`](#note-c3) | [CDL](./testcases/unit/cap_devices/netlist/rfcmim.cdl) / [GDS](./testcases/unit/cap_devices/layout/rfcmim.gds) |
|  | `sg13_hv_svaricap` | `C1 G1 W G2 SUB sg13_hv_svaricap l=0.3u w=3.74u Nx=1` | `w`, `l`, `Nx` | - | [CDL](./testcases/unit/cap_devices/netlist/sg13_hv_svaricap.cdl) / [GDS](./testcases/unit/cap_devices/layout/sg13_hv_svaricap.gds) |
| **ESD** | `diodevdd_2kv` | `D1 N1 N2 SUB diodevdd_2kv m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/diodevdd_2kv.cdl) / [GDS](./testcases/unit/esd_devices/layout/diodevdd_2kv.gds) |
|  | `diodevdd_4kv` | `D1 N1 N2 SUB diodevdd_4kv m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/diodevdd_4kv.cdl) / [GDS](./testcases/unit/esd_devices/layout/diodevdd_4kv.gds) |
|  | `diodevss_2kv` | `D1 N1 N2 SUB diodevss_2kv m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/diodevss_2kv.cdl) / [GDS](./testcases/unit/esd_devices/layout/diodevss_2kv.gds) |
|  | `diodevss_4kv` | `D1 N1 N2 SUB diodevss_4kv m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/diodevss_4kv.cdl) / [GDS](./testcases/unit/esd_devices/layout/diodevss_4kv.gds) |
|  | `idiodevdd_2kv` | `D1 N1 N2 SUB idiodevdd_2kv m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/idiodevdd_2kv.cdl) / [GDS](./testcases/unit/esd_devices/layout/idiodevdd_2kv.gds) |
|  | `idiodevdd_4kv` | `D1 N1 N2 SUB idiodevdd_4kv m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/idiodevdd_4kv.cdl) / [GDS](./testcases/unit/esd_devices/layout/idiodevdd_4kv.gds) |
|  | `idiodevss_2kv` | `D1 N1 N2 SUB idiodevss_2kv m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/idiodevss_2kv.cdl) / [GDS](./testcases/unit/esd_devices/layout/idiodevss_2kv.gds) |
|  | `idiodevss_4kv` | `D1 N1 N2 SUB idiodevss_4kv m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/idiodevss_4kv.cdl) / [GDS](./testcases/unit/esd_devices/layout/idiodevss_4kv.gds) |
|  | `nmoscl_2` | `D1 N1 N2 nmoscl_2 m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/nmoscl_2.cdl) / [GDS](./testcases/unit/esd_devices/layout/nmoscl_2.gds) |
|  | `nmoscl_4` | `D1 N1 N2 nmoscl_4 m=1` | `m` | [`FD1`](#note-fd1) | [CDL](./testcases/unit/esd_devices/netlist/nmoscl_4.cdl) / [GDS](./testcases/unit/esd_devices/layout/nmoscl_4.gds) |
| **Inductor** | `inductor` | `L1 N1 N2 SUB inductor w=2u s=2.1u d=25.35u nr_r=1` | `w`, `s`, `d`, `nr_r` | - | [CDL](./testcases/unit/ind_devices/netlist/inductor.cdl) / [GDS](./testcases/unit/ind_devices/layout/inductor.gds) |
|  | `inductor3` | `L1 N1 N2 N3 SUB inductor3 w=2u s=2.1u d=25.35u nr_r=2` | `w`, `s`, `d`, `nr_r` | - | [CDL](./testcases/unit/ind_devices/netlist/inductor3.cdl) / [GDS](./testcases/unit/ind_devices/layout/inductor3.gds) |
| **Tap** | `ntap1` | `R1 TIE WELL ntap1 A=608.4f Perim=3.12u` | `A`, `P` | [`T1`](#note-t1) | [CDL](./testcases/unit/tap_devices/netlist/ntap1.cdl) / [GDS](./testcases/unit/tap_devices/layout/ntap1.gds) |
|  | `ptap1` | `R1 TIE WELL ptap1 A=608.4f P=3.12u` | `A`, `P` | [`T1`](#note-t1) | [CDL](./testcases/unit/tap_devices/netlist/ptap1.cdl) / [GDS](./testcases/unit/tap_devices/layout/ptap1.gds) |

### Notes

- <a id="note-m1"></a>`M1`: `rfmode` defaults to `0` if it is not provided. The `m` parameter is folded into total extracted width.
- <a id="note-rf1"></a>`RF1`: RF MOS devices reuse the base MOS model name with `rfmode=1`.
- <a id="note-b1"></a>`B1`: The netlist may use either `we/le` or `w/l`.
- <a id="note-d1"></a>`D1`: The netlist may use either `A/P` or `W/L`.
- <a id="note-i1"></a>`I1`: `isolbox` compares `A/P`; if `A/P` are missing they are derived from `W/L`.
- <a id="note-fd1"></a>`FD1`: Fixed devices compare only `m`. If `m` is omitted, it defaults to `1`.
- <a id="note-r1"></a>`R1`: Poly resistors are 3-terminal devices (`N1 N2 SUB`).
- <a id="note-r2"></a>`R2`: Poly-resistor netlists may also use `$SUB=<net>` and a bracketed model token such as `$[rhigh]`. The resistance value is not compared.
- <a id="note-r3"></a>`R3`: Metal-resistor netlists accept either `w/l` or `width/length`. The resistance value is not used for LVS matching.
- <a id="note-c1"></a>`C1`: `cap_cmim` compares `w/l`, `A/P`, and `m`. If `A/P` are missing they are derived from `W/L`.
- <a id="note-c3"></a>`C3`: `rfcmim` compares `w/l`, `A/P`, `m`, and `wfeed`. If `A/P` are missing they are derived from `W/L`.
- <a id="note-t1"></a>`T1`: Tap devices may use either `A/P` (`Perim`) or `W/L`; LVS compares `A/P`.

## Devices Regression Usage

```bash
run_regression.py (--help | -h)
run_regression.py [--device=<device>] [--run_dir=<run_dir_path>] [--mp=<num>]
```

Example:

```bash
  python3 run_regression.py --device=MOS --run_dir=test_mos
```

**Options**

- `--help -h`                  Print this help message.
    
- `--device=<device>`          Select device category you want to run regression on.

- `--run_dir=<run_dir_path>`   Run directory to save all the results. By default, a timestamped run directory is created in the current directory.

- `--mp=<num>`                 Number of worker threads. By default, uses `cpu_count`.


Another approach for testing SG13G2 devices, you could make a full test for SG13G2 LVS rule deck, by executing the following command in current testing directory:

```bash
  make test-LVS-main
```

## Cells Regression Usage

```bash
run_regression_cells.py (--help | -h)
run_regression_cells.py [--cell=<cell>] [--run_dir=<run_dir_path>] [--mp=<num>]
```

Example:

```bash
python3 run_regression_cells.py --cell=sg13g2_inv_1 --run_dir=test_inv
```

**Options**

- `--help -h`                  Print this help message.
    
- `--cell=<cell>`              Specify the cell to run; all cells run if not specified.

- `--run_dir=<run_dir_path>`   Run directory to save all the results. By default, a timestamped run directory is created in the current directory.

- `--mp=<num>`                 Number of worker threads. By default, uses `cpu_count`.


Another approach for testing SG13G2 cells, you could make a full test for SG13G2 cells, by executing the following command in current testing directory:

```bash
  make test-LVS-cells
```


## LVS Outputs

You can find regression run results in the directory provided through `--run_dir`.
If `--run_dir` is not provided, the scripts create a timestamped run directory in the current working directory.

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
