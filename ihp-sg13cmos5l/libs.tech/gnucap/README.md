# SG13CMOS5L Verilog-A Device Models

This directory contains a Verilog-A standard-compliant implementation of the
SG13CMOS5L device library, ported from the equivalent `ihp-sg13g2` directory.

The models are compiled with the gnucap-modelgen-verilog compiler. Two test
suites run over them: one drives Gnucap against the Verilog-A models, the other
drives Ngspice against this PDK's Ngspice device library. Each side diffs its own
output against checked-in reference data; nothing in `make check` diffs one
simulator against the other. The cross-validation between the two happened when
those references were produced upstream, and what the suite enforces from then on
is that neither simulator drifts away from them.

## Relationship to ihp-sg13g2

SG13CMOS5L shares its MOS and resistor model cards with SG13G2: the files under
`libs.tech/ngspice/models/` for those devices are symlinks into the sibling
`ihp-sg13g2` checkout, so the model data is not merely equivalent but identical.

This directory follows the same convention already used by `libs.tech/xschem`,
`libs.tech/ngspice` and `libs.tech/xyce`: everything that would be a byte-for-byte
copy is a relative symlink into the sibling `ihp-sg13g2/libs.tech/gnucap/` (the
number of `../` depends on how deep the file sits), and only files that genuinely
differ are real files here. That includes most of the reference test data under
`tests/*/*/ref/`, which is valid for SG13CMOS5L precisely because the underlying
model cards are the same files.

The capacitors are the exception, on both counts. `models/capacitor_paramset.va`,
every `tb_cap_cmom*` testbench and both `capacitor/ref/` directories are real
files here rather than symlinks. For `cap_cmomi` the reason is the stack: it is
built on Metal1..Metal4 and its testbench instantiates `mmax=4` where SG13G2
uses 5, which moves the measured cutoff. For `cap_cmomf` there is nothing to
symlink at all, since SG13G2 reserved the name but never shipped the device.
That is also why the Ngspice `.spiceinit` in `tests/ngspice/capacitor` is a real
file: the shared one loads only `cap_cmomi.osdi`. `consts.params` and
`tb_cap_cmomi_typ.gc` are still symlinked like everything else.

Worth being explicit about what each half of the suite therefore proves. For the
resistors and the MOS the Gnucap side reads only symlinks, models, testbenches
and references all resolving into `ihp-sg13g2`, so a green run there says the
links resolve and the toolchain works rather than anything specific to this PDK.
The Ngspice side is the one that exercises SG13CMOS5L, because each `.spiceinit`
puts `$PDK_ROOT/$PDK/libs.tech/ngspice/models` on the Ngspice `sourcepath`.
Running it under `PDK=ihp-sg13cmos5l` and reproducing SG13G2's reference output
is the actual cross-PDK comparison, and it holds only for as long as the model
cards stay shared. The capacitor inverts this: both halves are SG13CMOS5L's own
there, so what the pair proves is that the two simulators agree on this PDK's
device, not that this PDK agrees with SG13G2.

Consequence: a standalone clone of `ihp-sg13cmos5l` is not enough. Clone it inside
an `IHP-Open-PDK` checkout as described in the top-level `README.md`, so that
`ihp-sg13g2` sits alongside it.

## Device coverage

Modelled in Verilog-A and exercised by the test suite:

- resistors: `rsil`, `rhigh`, `rppd`
- MOSFETs: `sg13_lv_nmos`, `sg13_lv_pmos`, `sg13_hv_nmos`, `sg13_hv_pmos`,
  including the RF variants selected by `rfmode=1`
- capacitors: `cap_cmomi` and `cap_cmomf`, the interdigitated and the metal
  fringe MoM cap, both on this PDK's Metal1..Metal4 stack. The two testbenches
  use the same 5 um x 5 um M1..M4 geometry so their numbers compare directly:
  the fringe device is the denser of the pair, 1.287 fF/um2 against 1.09.

Modelled but not exercised: `ptap1` and `ntap1` have paramsets in
`models/resistor_paramset.va`, and no testbench on either side instantiates them.
`Rparasitic` is covered on the Gnucap side only; the Ngspice testbench has it
commented out, because `res_rpara` is missing from `cornerRES.lib`. Both gaps are
inherited from SG13G2.

Not modelled. Some of these are devices this PDK does not have: there is no
`cap_cmim`, `cap_rfcmim` or `cparasitic` here, nor the `npn13G2*` HBTs,
`schottky_nbl1`, `isolbox` or inductors. The rest are devices SG13CMOS5L does
have that SG13G2 has not ported to Verilog-A either, so the gap is inherited:
the moscaps, diodes, ESD, `svaricap`, `bondpad` and `pnpMPA`. See `ROAD_MAP.md`.

## Prerequisites

Install:

- [Gnucap](https://codeberg.org/gnucap/gnucap)
- [gnucap-modelgen-verilog](https://codeberg.org/gnucap/gnucap-modelgen-verilog)
- [Ngspice](https://sourceforge.net/projects/ngspice/files/ng-spice-rework/46/)
- [OpenVAF](https://openvaf.semimod.de), for the OSDI step below

Verified working with:

- Gnucap: `resolve 2026.06.10`
- gnucap-modelgen-verilog: `gnucap-mg-vams`, same release
- Ngspice: `ngspice-46`
- OpenVAF: `openvaf-r`

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
in `tests/gnucap/<testdir>/ref/*.gc.out`. Most have a counterpart Ngspice test
case in `tests/ngspice/<testdir>/*.sp`, which is diffed against its own reference
in the same way. The two are counterparts by construction, not by anything the
Makefiles do at run time.

Results are reported as `PASS` (no diff), `FAIL` (see `check/*.diff`) or `MISS`
(no reference file found). The whole suite always runs to the end, and the
aggregate targets then exit nonzero if anything was `FAIL` or `MISS`, so these
are usable as a regression gate rather than only as something to read.

```bash
make check                      # build plugins, then run everything
make -C tests check             # run without rebuilding
make -C tests check-gnucap
make -C tests check-ngspice
make -C tests/gnucap check-resistor
make -C tests/ngspice check-resistor
make -C tests/gnucap help
```

`make -C tests check` assumes the plugins are already built; on a fresh checkout
there is no `plugins/` directory yet, and every testbench opens by loading a
`.so` from it, so run `make check` at least once first.

From the repository root there is also:

```bash
make test-gnucap
```

which is `make check` under `PDK=ihp-sg13cmos5l`. It skips with a message,
rather than failing, when the toolchain is missing or `PDK_ROOT` does not point
at a checkout holding both PDKs, so that contributors working on DRC or LVS are
not blocked by a simulator they do not have.

Run a single test:

```bash
make -C tests/gnucap resistor/check/tb_res_basic_typ.gc.out
make -C tests/ngspice resistor/check/tb_res_basic_typ.sp.out
```

## Plotting

Generate all figures from the reference test data, or only some test directories:

```bash
python python/plot_all.py
python python/plot_all.py resistor
```

Figures are saved in `gnucap/figures/<testdir>`.

Always go through `plot_all.py`. The `plot_<testdir>.py` modules beside it are
symlinks into `ihp-sg13g2`, and Python puts the *resolved* directory of the
script it runs first on `sys.path`, so running one of them directly picks up that
PDK's `dirs.py` and writes the figures into `ihp-sg13g2/libs.tech/gnucap/figures`
from that PDK's test data. `plot_all.py` is a real file here, so importing them
through it keeps everything on this tree.

## Licensing

The rest of this PDK is Apache-2.0, and this directory is not uniformly so. Most
of `models/` carries an Apache-2.0 header, but four other sets of terms reach the
plugins it builds, so it is worth naming them and where they live rather than
leaving a reader to find them in the headers.

**GPL-3.0-or-later.** The Gnucap simulator plugins under `cpp/` link against
Gnucap internals and include verbatim Gnucap core sources. They are symlinks into
`ihp-sg13g2`, where the originals and their headers live. Three GPLv3+ files are
real files here rather than symlinks: `tests/Makefile`, `tests/gnucap/Makefile`
and `tests/ngspice/Makefile`, derived from the SG13G2 originals and keeping their
`(c) Felix Salfelder 2024 / Lukas Deutz 2026` headers. They had to be copied
because the test directory list, the exit-status handling and the help text
differ here.

**AGPL-3.0-or-later.** `models/resistor.va` is `(c) 2025 Arpad Buermen`,
generated by the Verilog-A Distiller. It is a symlink into `ihp-sg13g2` like the
`cpp/` files, but unlike them it is not optional: `models/resistor_paramset.va`
pulls it in with `` `include ``, so it is compiled into the `resistor_paramset`
plugin. AGPL-3.0-or-later is a different license from GPL-3.0-or-later, not a
variant of it.

**Third-party compact models under `libs.tech/verilog-a/`.** Both are symlinks
into `ihp-sg13g2`, and neither is Apache-2.0 outright.

`r3_cmc` has two layers. The original model is `(c) 2020 Silicon Integration
Initiative` under the **Educational Community License 2.0**. `r3_cmc/LICENSE.txt`
is the short notice for it and points at the license text rather than carrying
it. ECL-2.0 is not Apache-2.0, its patent grant is narrower. IHP's modifications
on top are Apache-2.0, which is the header in `r3_cmc.va`.

`psp103` is not under a named open-source license. The header in `psp103.va`
carries only a copyright notice, naming NXP Semiconductors, CEA-Leti, Delft
University of Technology and Arizona State University over different periods. The
terms are the Compact Model Coalition In-Code Statement at the top of
`psp103/releasenotesPSP103.8.2.txt`. It permits redistribution of source and
binaries under four numbered conditions, covering what may be charged for,
acknowledgement in product documentation, and retention of the notice in both
source and binary redistributions. That last one reaches the compiled plugins in
`plugins/models/`, so read the statement in full before redistributing anything
built here; it is short, and paraphrasing it here would only invite relying on
the paraphrase.

## Acknowledgements

The SG13G2 implementation this directory is ported from was funded through the
NGI0 Commons Fund, a fund established by NLnet with financial support from the
European Commission's Next Generation Internet programme, under the aegis of DG
Communications Networks, Content and Technology under grant agreement No.
101135429. Additional funding is made available by the Swiss State Secretariat
for Education, Research and Innovation (SERI).

For details, see the NLnet project page: <https://nlnet.nl/project/VeriBench/>.
