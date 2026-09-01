# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased] - 2026-09-01

### Added

#### New Devices / PyCells
- `cap_cmomf`: new metal fringe MoM capacitor PCell for KLayout ([#1093](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1093))
- `cap_mom`: interdigitated MoM capacitor for SG13G2 KLayout ([#1049](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1049))
- `cap_cmomi`: computed capacitance display, feed-aware C estimation, live coerce callback, and density fill exclusion ([#1076](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1076), [#1108](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1108))
- MOSCAP (MOS capacitor) PCell initial version ([#1050](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1050))
- `cmim` KLayout PCell: added labels
- HBT test structures GDS: initial version
- pnpMPA measurement test structures GDS ([#1009](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1009))
- RF MOSFET PyCells: initial version
- `NoFillerStack` PCell: initial version
- `ptap1` PCell: initial version
- PDK modules: initial integration of PDK extensions in Xschem and KLayout

#### LVS
- KLayout LVS: `--disable_tap_extraction` option ([#1032](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1032))
- KLayout LVS: `--purge-devices` CLI parameter; `PURGE` conditional honored in `rfmos_model_mapping.lvs` ([#1105](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1105))

#### SRAM
- SRAM: automated cross-view validation
- SRAM: new macro `RM_IHPSG13_1P_2048x32_c2_bm_bist` ([#1029](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1029))
- SRAM: updated `RM_IHPSG13_2P_64x22_c2` macro ([#1028](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1028))
- SRAM: added `1P_8192x32_c4` macro
- SRAM: added BIST macro `RM_IHPSG13_1P_512x32_c2_bm_bist` ([#429](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/429))
- SRAM: add timescale in `64x16` ([#1104](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1104))

#### Tools / Infrastructure
- Regression test for `sprintf` utility function ([#1120](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1120))
- gnucap: statistics reporting ([#998](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/998))
- Bug report issue template ([#1019](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1019))
- KLayout scripts: added copyright header
- AWS Palace: added `gds2palace` submodule
- ITF file: initial version
- DRM: added version 0.4
- IO cells: added datasheets
- Qucs-S: schematics for standard cells ([#939](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/939))
- GDSFactory: added README and integration guide ([#691](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/691))
- LibreLane: standalone DRC support ([#728](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/728))
- Added Schottky diode (`SBD`) symbol and documentation ([#682](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/682))
- npn13G2 symbols: updated ([#902](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/902))

### Changed

#### Devices / PyCells
- Sealring KLayout script: renamed `height` parameter to `length` (backward-compatible deprecation path) ([#1110](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1110), [#1127](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1127))
- `cap_cmomi` LVS: terminals made equivalent, dropped marker flags ([#1084](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1084))
- RPPD PyCell: handle EXTBlock notch spacing separately ([#1002](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1002))
- `sprintf` utility function simplified and crash fixed ([#1120](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1120))
- `svaricap`: `nwell-psub` diode `vj` parameter adjusted for 125 °C transient simulation ([#1102](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1102))
- Poly resistor `rhigh`: aligned corner and global statistical parameter to process specification ([#1081](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1081))
- pmos/pmosHV: removed `Substrate.drw` 40/0 layer ([#942](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/942))
- KLayout layer property file: reverted `Text.drw` layer to white
- `rsil`: removed unsupported `b` (bends) parameter ([#944](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/944))
- `svaricap`: updates to PyCell and symbol ([#941](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/941))
- `rfcmim`: added `m` multiplier parameter in Xschem symbol ([#979](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/979))
- xschem: `mm_ok` flag introduced across sg13g2_pr symbols ([#993](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/993))
- `pnpMPA` xschem symbol: changed default `w` to align with tech file value

#### LVS / DRC
- KLayout LVS: removed unconditional global device purging from rule deck ([#1105](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1105), [#1126](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1126))
- KLayout LVS: inductor metal stack now configurable per PDK ([#1068](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1068))
- KLayout LVS: metal resistors mapped to `R` prefix ([#1046](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1046))
- KLayout DRC: removed irrelevant off-grid checks ([#1025](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1025))
- KLayout DRC: `latchUp` flag set to true by default
- KLayout DRC: JSON-based override of defaults ([#900](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/900))
- KLayout LVS: via handling refactored to support `cmos5l_ihp` ([#1039](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1039))
- DRC: `LU.b` – report portions of N+Activ beyond 20 µm max space ([#949](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/949))
- Magic LVS: added inductors recognition ([#873](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/873))

#### Simulation / Tools
- Xschem: parallel-simulation scripts run through Tcl's `exec` ([#1118](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1118))
- Palace submodule bumped to upstream HEAD for scikit-rf 2.0 fix ([#1040](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1040))
- gnucap: `make check` properly builds before running tests ([#1077](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1077))
- LibreLane: updated variables in shared SCL and CSL config files ([#999](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/999))
- LibreLane: `PAD_SPICE_MODELS` points to correct `sg13g2_io.spice` path ([#1095](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1095))
- LibreLane: updated tracks configuration ([#892](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/892))
- LibreLane: Magic filler flow added ([#883](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/883))
- Standard cell symlinks changed from absolute to relative paths ([#1097](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1097))
- Standard cells relocated into `libs.ref` with updated Xschem view selection ([#1031](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1031))
- PCell preprocessor: each process gets its own preprocessing directory ([#1090](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1090))
- KLayout tech file: added comprehensive list of grid values ([#1044](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1044))
- LEF tech: fixed pitch values ([#890](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/890))
- KLayout version centralized in `versions.txt` ([#983](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/983))
- KLayout PCells: tech association fix ([#930](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/930), [#943](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/943))
- Xschem path: appended `xschem/` to `XSCHEM_LIBRARY_PATH`
- Qucs-S: individual XMLs for standard cells ([#904](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/904))
- Xschem: improved evaluation precision ([#907](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/907))
- Parallelization improvements in simulation scripts ([#629](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/629))

### Fixed

#### LVS / DRC
- KLayout LVS: fixed LVS testing regression (#1126)
- LVS: fixed SBD under CMIM issue; added testcase ([#1030](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1030))
- KLayout DRC: fixed CNT-A modular detection ([#887](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/887))
- KLayout DRC: fixed filler space/notch violations ([#924](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/924))
- KLayout DRC: fixed Metal density min/max values

#### Extraction / Magic
- Magic: fixed `cap_rfcmim` missing substrate terminal extraction ([#1111](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1111))
- Magic: corrected metal surround around `contbar` contacts in resistors; simplified `Cntb` DRC checks ([#973](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/973))
- Magic: fixed incorrect GDS read-in of devices marked by text tags ([#970](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/970))
- Magic: fixed SPICE import for subcell references ([#889](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/889))
- Magic: fixed SCR1 DRC errors ([#867](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/867))
- Magic: fixed BJT extraction issues ([#863](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/863))
- Magic: fixed mimcap extraction ([#851](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/851), [#853](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/853))
- Magic: fixed metal fill generation ([#881](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/881), [#908](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/908))
- Magic: fixed LibreLane startup script incompatibility

#### PyCells
- Isolbox PyCell: fixed `diode_layer` parameter evaluation ([#1071](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1071))
- MOSCAP PyCell: fixed callback issue ([#1088](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1088))
- RPPD PyCell: fixed EXTB.b DRC violation ([#997](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/997))
- rhigh PyCell: fixed pSD.b and EXTB.b space violations in devices with bends
- rppd/rhigh PyCells: handle large poly spacing and even-number bends ([#988](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/988))
- rfcmim Qucs-S symbol fix ([#992](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/992))
- Sealring PCell: fixed corruption caused by compound scaling factor in NLCB ([#1064](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1064))
- nmos clamp: fix applied ([#600](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/600))
- Primitive GDS: rolled back incorrect `idiode*` removal

#### Simulation / Tests
- Ngspice Monte Carlo tests fix ([#1061](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1061))
- Fixed tkinter requirements ([#1015](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/1015))
- npn13G2 annotation fix ([#621](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/621))
- rhigh: fix poly resistor model ([#742](https://github.com/IHP-GmbH/IHP-Open-PDK/pull/742))

---

## [Unreleased] - 2024-10-14

### Added
- Xschem install script: added Python shebang line
- Qucs-S install script: added Python shebang line
- Qucs-s install script: added checking for qucs-s binary
- Add vbic examples for Xyce/adms
- Add moshv lib and examples for Xyce
- Initial list of tool versions
- Added cross-platform compatibility for logger
- Added initial version of multiplier check for netlists in stdcells
- Add CODEOWNERS file
    - Krzysztof and Sergei are the maintainer of this repository. Add them as CODEOWNER to auto-assign them in Pull Requests.
- KLayout XSection: added initial README
- Initial version of KLayout cross-section (XS) settings
- Added HBT models for Xyce simulator
- Added smaller SRAM macros
- KLayout Pycells: added NWell to 'dpantenna' device
- Added pnpMPA measurements documentation
- Added 'Digital' IHP130 cells as submodule

### Changed
- Update ISSUE_TEMPLATE.md
    - removed explicit env items, user should put his own related settings
- Updated procedure to avoid constant openning cmd window on Windows to execute task list.
- Update versions.txt
    - added OpenVAF
- Klayout PyCell integration
    - Added support for or'ed #ifdef defines
    - Took over windows compatibility work from Andreas Krinke <andreas.krinke@gmx.de>
    - Fixed pypreprocessor issues
    - Fixed misleading import
    - Fixed documentation
    - Add pypreprocessor IHP clone submodule
    - Added evalution of names used for conditional compilation against process-chain
    - Added catching of PyCell static/dynamic compilation errors for correction of file-path stack-dump
    - Added diagnositc logging of process-chain as well as set defines
    - Eleminate pre-definition of used defines by pre-scanning cell code
    - Fixed issue from IHP open source server regarding remove of tmp-file
    - Implemented 'conditional compilation' for PyCell code, see documentation in ihp-sg13g2/libs.tech/klayout/python/sg13g2_pycell_lib/__init__.py
    - Simplified referencing python modules by setting search path
    - Re-implemented clone() for shapes using deepcopy
    - Implemented tagging of shapes feature from SKILL Pcell counter-part
    - Fixed npn13G2L/npn13G2V to be equal to SKILL Pcell counter-part
    - Introduced library code/documentation as submodule from pycell4klayout-api repo
    - Added support for fgAnd, fgNot andfgSize
    - Fixed dbLayerSize
    - Fixed pin label creation by removing extra text generation
    - Added missing self-argument in class Box
    - Fix wrong assignment: re-assign pins, terms and nets from PyCell-instances to cell-instances for multi-cell instances of the same PyCell
    - Fixed merge-error
    - Added PyCell parameter type bool
    - Added partial implementation for PyCell API class Net
    - Added partial implementation for PyCell API class Path
    - Added partial implementation for PyCell API class ShapeFilter
    - Added support for Net's
    - Added generic registering of IHP PyCell's in Klayout
    - Added support for inductor2, inductor2_sc, inductor2_sp, inductor3, inductor3_sc and inductor3_sp
    - Added partial implementation of class Pin from PyCell API
    - Added partial implementation of class Term from PyCell API
    - Added support for pins/terminals
    - Added support for XOR geometric transformation
    - Added support for text alignment/orientation
    - Fixed dbLayerXorList from geometry.py
    - Added support of npn13G2L and npn13G2V
    - Extended documentation
- Update KLayout DRC scripts
    - fixes regression that missed DRC errors, e.g. for M1.b
    - improves running the DRC on Windows
    - prints message for each rule during run
    - new options, increased accuracy of width and overlap checks
    - fixes bug regarding µm/dbu conversion
    - new options, increased accuracy of space and separation checks
    - fixes incorrect DRC errors, e.g. for pSD.d, pSD.d1
    - maximal DRC script supports ~75% of rules
    - rename DRC script parameters for OpenROAD compatibility
        - logfile -> log_file
        - gdsfile -> in_gds
        - outfile -> report_file
    - DRC script parameter "cell" is now optional
    - output number of DRC errors at the end
    - DRC script no longer depends on layout dbu
        - all lengths are given in micrometers
    - add limits to rule descriptions, e.g., "Min. GatPoly width = 0.13"
- Improve Windows compatibility of PyCell code
    - remove dependency on psutil, which is difficult to install on Windows
- Updated Qucs-S examples, install.py for Qucs
- Use Xyce vbic build-in model instead Verilog-A model
- Change example file names
- Xyce library extension moslv
- Update README.md
    - added tool versions part
    - Aligned file names
    - added note on XSection in PDK contents
    - updated year in Apache license header
    - Added 'Digital' tool in PDK contents
    - Added LVS in PDK contents section
- pmosHV Pycell: various updates to align to the implementation in commercial PDK
- Pycell4klayout-api updated to the latest version
- Sealring Pycell: area for registration
- libs.tech: openroad: Add missing SRAMs
    - A4defa8ab added missing .lib files for recently added SRAMs. Update the export.yml with all files for these RAMs.
- Xyce HBT models: commented vbe_max, vbc_max, vce_max parameters - these are not used
- libs.tech: Python tool to generate export.yml
    - The export.yml file communicates all exportable files, with additional meta data, to OpenROAD. It can automatically check if files changed or new exist and sync those.
- libs.ref: Don't ignore sub-directories
    - The .gitignore in the root level ignores directories like lib/. This will prevent checking in new libs as Git would ignore those.
- Update README.md
    - added note on current status
    - screenshot as an example
- KLayout Pycells: small typo correction in npn13G2* devices
- Update README.md
    - Added requirement to set PDK_ROOT
- Ngspice models: changed '.parameters' to '.param' in corner*.lib files
- Option list duplication removed
- Update xschemrc
    - Adding `append XSCHEM_LIBRARY_PATH :${XSCHEM_SHAREDIR}/xschem_library/devices` line
- Update path to standard symbols
- .spiceinit PDK env. variable added + fixes
- .spiceinit PDK env. variable added
- Update .gitmodules
    - Changed SSH to HTTPS mode
- Updating custom writer for LVS runset
- Major change in ngspice model referencing, xschem testcases update, qucs-s examples updated
- Construct full lvs rule deck for SG13G2 tech
- libs.tech: Klayout: tech: sg13g2.lyt: Use empty lef-files
    - OpenROAD-flow-scripts will search and replace for <lef-files>.*</lef-files>. Therefore, keep it empty in this syntax.
- libs.tech: Klayout: tech: Add map file
    - This file was copied from the OpenROAD-flow-scripts repository and should be maintained and kept here.
- libs.tech: Klayout: tech: Add layer map
    - OpenROAD requires the sg13g2.map file to correctly place each layer. Fix this here to not overwrite manually changes in OpenROAD-Flow-Scripts.
- KLayout Pycells: updated device library name
- KLayout tech file: setting up technology specific grids, smallest (req) = 5nm
- IO cells: renamed 'liberty' folder to 'lib' to align across cellsets (stdcell, sram)
- IO cells: aligned Liberty file names
- libs.tech: klayout: Add macro to report layer density
    - This script calculates and reports the density for multiple important layers and can help to see which layers will violatie fill rules. Based-on: Krzystof Herman <herman@ihp-microelectronics.com>
- libs.tech: klayout: drc: Use correct border
    - The DRC report had multiple violations included which are relate to unclean calculation of the chip border. Based-on: Andreas Krinke <andreas.krinke@tu-dresden.de>
- libs.tech: klayout: Add Python script to generate Sealring files
    - This script can be called in Klayout's batch mode and generates a GDS file with a sealring included. The width and height of the ring are configurable via arguments.
    - Example call: 
    ```
    klayout -n sg13g2 -zz -r sealring.py \
    -rd width=1300.0 -rd height=1300.0 \
    -rd output=macros/sealring.gds.gz
    ```
- DbCreateRect outside if..else
- Via stack PCell integration
- KLayout Pycells: some fixes and cleanup for npn13G2
- IO cells: renamed CDL file to align
- Dantenna and dpantenna PCells integration
- Xschem testcases *.sch files updated to support lower-case w and l
- Xschemrc res_drc function updated
- DRC checks for xschem added in xschemrc (mosfets, hbt, diode, res, mim), symbols modified, some testcases modified
- @spiceprefix added for mos devices and diodes, RF symbols added for HV mosfets
- Lv symbols modified for lvs, @spiceprofix added
- Change hv pcells name
- KLayout Pycells: updated 'Ae' text string in npn13G2* cells to be consistent w/ internal implementation
- Hv added to init
- Hv-mos pcell integration
- Lvs-symbol
- Some updates on top of #121
    - Remove labels on ESD diodes so they are now recognized as regular d(p)antenna diodes
    - Increase width to minimum 0.48µm to account for new rule not yet in DRC check.
- Layout rule manual updated
- Update README.md
    - OpenROAD, OpenROAD flow scripts, Qucs-S added as supported EDA tools.

### Fixed
- Stdcells LEF: USE ANALOG changed to USE SIGNAL
- pnpMPA: fixed pin order in model, updated xschem symbol and testbench
- libs.ref: sg13g2_io: verilog: Fix specify syntax
    - The input and output definition in the Verilog specify block were positioned in the wrong order (output to input). Change and also implement the tri-state better.
- LVS rule decks: Fix GF180 remnants in log strings
- pnpMPA docs: fixed typos in file naming
- libs.tech: klayout: macros: Fix intentation
- libs.tech: klayout: Fix Metal density min/max values
    - Global min./max. Metal(n) density values are 35% and 60%. The previous 25% and 75% are only valid for 800x800 chip areas.
- Fix class name in hv-pmos pcell
- Fix hv pcell integration in init file

### Removed
- Qucs-S symbols: removed .INCLUDE, removed temperature sensing terminal from standard npn13G2* devices
- Pycells: removed via_stack device, it's obsolete
- Remove merged.lef from klayout setup
    - Removing reference to merged.lef which does not exist.
- Delete ihp-sg13g2/libs.tech/pycell directory
- KLayout tech JSON: removed all layers definitions, these are taken from .lyp file
- KLayout DRC: removed obsolete deck file (now we have min and max in separate files)

[unreleased]: https://github.com///compare/v0.1.0..HEAD

<!-- generated by git-cliff -->
