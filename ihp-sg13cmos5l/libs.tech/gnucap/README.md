# SG13CMOS5L Verilog-A Device Models

This directory contains a Verilog-A standard-compliant implementation of the
SG13CMOS5L device library, ported from the equivalent `ihp-sg13g2` directory.

The models are compiled with the gnucap-modelgen-verilog compiler. The
implementation is tested using the Gnucap simulator, and the automated test flow
cross-validates device behavior by comparing Gnucap simulation results against
reference Ngspice simulations using the SG13CMOS5L Ngspice device library.

## Relationship to ihp-sg13g2

SG13CMOS5L shares its MOS and resistor model cards with SG13G2: the files under
`libs.tech/ngspice/models/` for those devices are symlinks into the sibling
`ihp-sg13g2` checkout, so the model data is not merely equivalent but identical.

This directory follows the same convention already used by `libs.tech/xschem`,
`libs.tech/ngspice` and `libs.tech/xyce`: everything that would be a byte-for-byte
copy is a relative symlink into `../../../../ihp-sg13g2/libs.tech/gnucap/`, and only
files that genuinely differ are real files here. That includes the reference test
data under `tests/*/*/ref/`, which is valid for SG13CMOS5L precisely because the
underlying model cards are the same files.

Consequence: a standalone clone of `ihp-sg13cmos5l` is not enough. Clone it inside
an `IHP-Open-PDK` checkout as described in the top-level `README.md`, so that
`ihp-sg13g2` sits alongside it.

## Device coverage

Covered, with the full SG13G2 test suite:

- resistors: `rsil`, `rhigh`, `rppd`, plus `ptap1`, `ntap1` and `Rparasitic`
- MOSFETs: `sg13_lv_nmos`, `sg13_lv_pmos`, `sg13_hv_nmos`, `sg13_hv_pmos`,
  including the RF variants selected by `rfmode=1`

Not covered. The capacitors are absent from this PDK rather than unported:
SG13CMOS5L has no `cap_cmim`, `cap_rfcmim` or `cparasitic`. Its MoM capacitor
`cap_cmomi` is a different model from the SG13G2 one (Metal1..Metal4 rather than
Metal1..Metal5), so it is not covered by the SG13G2 Verilog-A model and will be
added together with the device itself. Diodes, ESD, `bondpad` and `pnpMPA` are
not yet ported to Verilog-A in SG13G2 either. See `ROAD_MAP.md`.

## Prerequisites

Install:

- [Gnucap](https://codeberg.org/gnucap/gnucap)
- [gnucap-modelgen-verilog](https://codeberg.org/gnucap/gnucap-modelgen-verilog)
- [Ngspice](https://sourceforge.net/projects/ngspice/files/ng-spice-rework/46/)

Verified working with:

- Gnucap: `resolve 2026.06.10`
- gnucap-modelgen-verilog: `gnucap-mg-vams`, same release
- Ngspice: `ngspice-46`

Set the following environment variables. `PDK_ROOT` must point at the
`IHP-Open-PDK` checkout that contains `ihp-sg13cmos5l`, which is not necessarily
the one you use for SG13G2 work:

```bash
export PDK_ROOT=/path/to/IHP-Open-PDK
export PDK=ihp-sg13cmos5l
```

The Ngspice testbenches need the OSDI objects that the model cards reference.
`libs.tech/ngspice/osdi/` symlinks them from `ihp-sg13g2`, where they are a build
product rather than a tracked file, so build them once:

```bash
cd $PDK_ROOT/ihp-sg13g2/libs.tech/verilog-a && ./openvaf-compile-va.sh
```

For plotting, create a virtual environment from the top-level `gnucap/` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r python/requirements.txt
```

## Build

From the top-level `gnucap/` directory, build all Verilog-A model plugins and
Gnucap simulator plugins:

```bash
make
```

Build only one group:

```bash
make models-plugins
make gnucap-plugins
```

Note on build time: `gnucap-mg-vams` expands the PSP103 RF paramsets into very
large generated C++ (over 100 MB for `sg13g2_moslv_rf_paramset`), so a cold
`make` takes on the order of half an hour. The resistor and `idc` targets build
in seconds, so when iterating build just those:

```bash
make -C models idc resistor_paramset
```

List available models or plugins, build one, or dump a paramset as a Verilog-A
module:

```bash
make -C models help
make -C models resistor_paramset
make -C models dump-resistor_paramset
make -C cpp help
make -C cpp measure_mean
```

## Testing

Each Gnucap test case `tests/gnucap/<testdir>/*.gc` writes its output to
`tests/gnucap/<testdir>/check/*.gc.out`, which is diffed against the reference data
in `tests/gnucap/<testdir>/ref/*.gc.out`. Each has an equivalent Ngspice test case
in `tests/ngspice/<testdir>/*.sp` used for cross-validation.

Results are reported as `PASS` (no diff), `FAIL` (see `check/*.diff`) or `MISS`
(no reference file found).

```bash
make check                      # build plugins, then run everything
make -C tests check             # run without rebuilding
make -C tests check-gnucap
make -C tests check-ngspice
make -C tests/gnucap check-resistor
make -C tests/ngspice check-resistor
make -C tests/gnucap help
```

Run a single test:

```bash
make -C tests/gnucap resistor/check/tb_res_basic_typ.gc.out
make -C tests/ngspice resistor/check/tb_res_basic_typ.sp.out
```

## Plotting

Generate all figures from the reference test data, or one test directory:

```bash
python python/plot_all.py
python python/plot_resistor.py
```

Figures are saved in `gnucap/figures/<testdir>`.

## Licensing

The rest of this PDK is Apache-2.0. The Gnucap simulator plugins under `cpp/` are
**GPL-3.0-or-later**: they link against Gnucap internals and include verbatim
Gnucap core sources. They are symlinks into `ihp-sg13g2`, where the original
files and their license headers live.

## Acknowledgements

The SG13G2 implementation this directory is ported from was funded through the
NGI0 Commons Fund, a fund established by NLnet with financial support from the
European Commission's Next Generation Internet programme, under the aegis of DG
Communications Networks, Content and Technology under grant agreement No.
101135429. Additional funding is made available by the Swiss State Secretariat
for Education, Research and Innovation (SERI).

For details, see the NLnet project page: <https://nlnet.nl/project/VeriBench/>.
