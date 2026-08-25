# SG13G2 Verilog-A Device Models

This directory contains a Verilog-A standard-compliant implementation of the
SG13G2 IHP-Open-PDK device library.  
  
The Makefiles described below manage the build and test flow for Verilog-A 
device models. 
 
The models are compiled with the gnucap-modelgen-verilog compiler, and support 
for the OpenVAF model compiler is planned. 

The implementation is tested using the Gnucap simulator. The automated test flow 
cross-validates device behavior by comparing Gnucap simulation results against 
reference Ngspice simulations using the existing IHP-Open-PDK Ngspice device 
library.

## Directory Structure

```text
gnucap/
├── Makefile             # Top-level entry point: build, test, clean
├── gnucap.mk            # Gnucap Makefile configuration
├── models/              # Verilog-A model library
│   └── Makefile         # Builds Verilog-A model plugins
├── cpp/                 # C++ source for Gnucap simulator plugins
│   └── Makefile         # Builds Gnucap simulator plugins
├── tests/               # Test suite
│   ├── Makefile         # Runs the test suite
│   ├── gnucap/          # Test suite for Gnucap
│   │   ├── Makefile     # Runs Gnucap test suite  
│   │   └── {resistor, capacitor, moslv, ...}/ # Device-specific test directories 
│   │       └── ref/     # Gnucap reference data
│   └── ngspice/         # Test suite for Ngspice
│       ├── Makefile     # Runs Ngspice test suite        
│       └── {resistor, capacitor, moslv, ...}/ # Device-specific test directories 
│           └── ref/     # Ngspice reference data 
├── plugins/             # Plugin built directory
│   ├── models/          # Generated Verilog-A model plugins (.so)
│   └── gnucap/          # Generated Gnucap plugins (.so)
└── python/              # Post-processing and plotting scripts
```

## Prerequisites

Install:

- [Gnucap](https://codeberg.org/gnucap/gnucap)
- [gnucap-modelgen-verilog](https://codeberg.org/gnucap/gnucap-modelgen-verilog)
- [Ngspice](https://sourceforge.net/projects/ngspice/files/ng-spice-rework/46/)
- [OpenVAF](https://openvaf.semimod.de), for the OSDI step below

Tested with:
- Gnucap: `resolve 2026.06.10`
- gnucap-modelgen-verilog: `gnucap-mg-vams`, same release
- Ngspice: `ngspice-46`
- OpenVAF: `openvaf 23.5.0` (`openvaf-r`)

To run Ngspice testbench, add the following environment variables to your  
`~/.bashrc`: 

```bash
# Path to your local IHP Open PDK checkout
export PDK_ROOT=/path/to/IHP-Open-PDK
# IHP process design kit name
export PDK=ihp-sg13g2
```

Replace `/path/to/IHP-Open-PDK` with the path to your local IHP-Open-PDK 
repository.

The Ngspice testbenches also need the OSDI objects that the model cards
reference. Those are a build product rather than a tracked file, so on a fresh
checkout `libs.tech/ngspice/osdi/` does not exist yet and the Ngspice half of the
suite stops on its first test. Build them once with [OpenVAF](https://openvaf.semimod.de):

```bash
cd $PDK_ROOT/$PDK/libs.tech/verilog-a && ./openvaf-compile-va.sh
```

To plot and compare test results between Gnucap and Ngspice, install the 
required Python dependencies. From the top-level `gnucap/` directory, create a 
virtual Python environment and install dependencies with:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r python/requirements.txt
```

Activate the environment before running plotting scripts:
```bash
source .venv/bin/activate
```

## Build Gnucap Model and Simulator Plugins

From the top-level `gnucap/` directory, build all Verilog-A model plugins and 
Gnucap simulator plugins:

```bash
make
```

Build only Verilog-A model plugins:

```bash
make models-plugins
```

Build only Gnucap simulator plugins:

```bash
make gnucap-plugins
```

### Build Verilog-A Model Plugin

Build a specific model plugin:

```bash
make -C models <model>
```

List available models: 

```bash
make -C models help
```
Example:

```bash
make -C models resistor_paramset
```
Dump a paramset as a Verilog-A module:

```bash
make -C models dump-<model>
```

### Build Gnucap Simulator Plugin

Build a specific Gnucap simulator plugin:

```bash
make -C cpp <plugin>
```

List available plugins:

```bash
make -C cpp help
```

Example:

```bash
make -C cpp measure_mean
```

## Testing

Each Gnucap test case `tests/gnucap/<testdir>/*.gc` writes its output to 
`tests/gnucap/<testdir>/check/*.gc.out`. The output is diffed against the reference 
data in `tests/gnucap/<testdir>/ref/*.gc.out` for regression testing.

Each Gnucap test case has an equivalent Ngspice test case in 
`tests/ngspice/<testdir>/*.sp`, which writes its output to 
`tests/ngspice/<testdir>/check/*.sp.out`. The output is diffed against the 
reference data in `tests/ngspice/<testdir>/ref/*.sp.out`, which is used for 
comparison and cross-validation.

Test results are reported as:

- `PASS` -> no diff 
- `FAIL` -> diff detected; see `tests/gnucap/<testdir>/check/*.gc.diff`
- `MISS` -> no reference file found

### Run All Tests

From the top-level `gnucap/` directory, build the required plugins and run the 
full test suite with Gnucap and Ngspice:

```bash
make check
```

Run the test suite without rebuilding the required model and Gnucap plugins:

```bash
make -C tests check
```

Run the full test suite with Gnucap or Ngspice only:

```bash
make -C tests check-gnucap
make -C tests check-ngspice
```

### Run Device-Specific Tests

Run all tests in a specific test directory `<testdir>` with Gnucap or Ngspice:

```bash
make -C tests/gnucap check-<testdir>
make -C tests/ngspice check-<testdir>
```

Example:

```bash
make -C tests/gnucap check-resistor
make -C tests/ngspice check-resistor
```

List available test directories for Gnucap or Ngspice:

```bash
make -C tests/gnucap help
make -C tests/ngspice help
```

Run a single test with Gnucap or Ngspice:

```bash
make -C tests/gnucap <testdir>/check/<test>.gc.out
make -C tests/ngspice <testdir>/check/<test>.sp.out
```

Example:

```bash
make -C tests/gnucap resistor/check/tb_res_basic_typ.gc.out
make -C tests/ngspice resistor/check/tb_res_basic_typ.sp.out
```

## Plotting

Generate all figures from the reference test data:

```bash
python python/plot_all.py

```

Generate figures for a specific test directory run

```bash
python python/plot_<testdir>.py
```

Figures are saved in the `gnucap/figures/<testdir>`.

## Acknowledgements

This contribution to IHP-OPEN-PDK repository was funded through the NGI0 
Commons Fund, a fund established by NLnet with financial support from the 
European Commission's Next Generation Internet programme, under the aegis 
of DG Communications Networks, Content and Technology under grant agreement 
No. 101135429. Additional funding is made available by the Swiss State 
Secretariat for Education, Research and Innovation (SERI).

For details, see the NLnet project page: <https://nlnet.nl/project/VeriBench/>. 



