# IHP-Open-PDK Issue Classification

This document classifies all issues in the IHP-Open-PDK repository by topic and label.
Issues are organized with **bugs prioritized first**, then grouped by category and state (open before closed).

## Summary

| Category | Open | Closed | Total |
|----------|------|--------|-------|
| DRC | 41 | 47 | 88 |
| LVS | 49 | 30 | 79 |
| PyCells | 10 | 22 | 32 |
| Simulation Models | 34 | 81 | 115 |
| Symbols | 5 | 13 | 18 |
| Digital Primitives | 12 | 28 | 40 |
| IO Cells | 8 | 6 | 14 |
| Documentation | 13 | 8 | 21 |
| Infrastructure | 4 | 7 | 11 |
| Other | 17 | 40 | 57 |
| **Total** | **193** | **282** | **475** |

**Bugs:** 63 open, 89 closed, 152 total

### Categories

- **DRC**: Design Rule Check issues — rule violations, density checks, fill patterns, DRC deck bugs
- **LVS**: Layout vs Schematic issues — extraction errors, netlist mismatches, device recognition
- **PyCells**: Parameterized cell issues — KLayout/Magic PCell generators, inductor/sealring cells
- **Simulation Models**: SPICE/Verilog-A model issues — ngspice/Xyce model bugs, convergence, noise, corners
- **Symbols**: Schematic symbol issues — xschem/Qucs-S symbol definitions, pin mappings, netlisting
- **Digital Primitives**: Standard cell and SRAM issues — liberty, LEF/DEF, Verilog, pin order, timing
- **IO Cells**: I/O pad library issues — pad cells, bondpads, level shifters, ESD structures
- **Documentation**: Documentation issues — process spec, layout rules, device datasheets
- **Infrastructure**: Tooling and setup issues — installation, CI, technology files, configuration
- **Other**: General questions, feature requests, and miscellaneous items

## Issue Classification Table

Issues are sorted with bugs first (open then closed), followed by non-bugs (open then closed), within each category.

| # | State | Label | Category | Description |
|---|-------|-------|----------|-------------|
| [#814](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/814) | 🔴 Open | bug | 🐛 DRC | Klayout DRC - rule Slt.e is not enforced |
| [#794](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/794) | 🔴 Open | bug | 🐛 DRC | SRAM - Magic DRC |
| [#793](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/793) | 🔴 Open | bug | 🐛 DRC | SRAM - KLayout DRC |
| [#734](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/734) | 🔴 Open | bug | 🐛 DRC | sg13g2_and2_1: Pin A generates M1.b violations |
| [#730](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/730) | 🔴 Open | bug | 🐛 DRC | AFil.d Issues |
| [#710](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/710) | 🔴 Open | bug | 🐛 DRC | DRC Density checks windowing problem |
| [#709](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/709) | 🔴 Open | bug | 🐛 DRC | Regression: cnt.b1 incorrectly reported |
| [#697](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/697) | 🔴 Open | bug | 🐛 DRC | Schottky LU.d1 |
| [#696](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/696) | 🔴 Open | bug | 🐛 DRC | Schottky diode DRC - NBL.d |
| [#689](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/689) | 🔴 Open | bug | 🐛 DRC | `Cnt.c` in SRAM cells |
| [#684](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/684) | 🔴 Open | bug | 🐛 DRC | sg13g2_io sg13g2_IOPadAnalog has minor DRC errors |
| [#683](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/683) | 🔴 Open | bug | 🐛 DRC | Offgrid shapes in sg13g2_io.gds |
| [#656](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/656) | 🔴 Open | bug | 🐛 DRC | New DRC deck - inconsistencies between marker database window and terminal output |
| [#654](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/654) | 🔴 Open | bug | 🐛 DRC | New DRC deck has issues with spaces in directory/file names |
| [#639](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/639) | 🔴 Open | bug | 🐛 DRC | PCell/SVaricap: NW.e DRC violation using `w=&#39;3.74u&#39;` and maximal ruleset |
| [#628](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/628) | 🔴 Open | bug, documentation | 🐛 DRC | Layout "CuPillarPad" from sg13g2_pr violates grid design rules |
| [#627](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/627) | 🔴 Open | bug | 🐛 DRC | Layout "inductor3" from sg13g2_pr violates design rules |
| [#471](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/471) | 🔴 Open | bug | 🐛 DRC | Metal slits are not rightly recognized in the DRC/LVS |
| [#434](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/434) | 🔴 Open | bug | 🐛 DRC | maximum DRC sees bLay ERRoR that KLayout dont see... |
| [#408](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/408) | 🔴 Open | bug, enhancement | 🐛 DRC | Fill pattern generation in Magic has multiple issues. |
| [#391](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/391) | 🔴 Open | bug | 🐛 DRC | Cant Solve 800x800 µm² coverage ratio DRC error |
| [#291](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/291) | 🔴 Open | bug | 🐛 DRC | DRC Validation cells errata |
| [#245](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/245) | 🔴 Open | bug | 🐛 DRC | Pad.kR rule vs openroad PAD |
| [#861](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/861) | 🔴 Open | bug | 🐛 LVS | The missing ThickGateOx (44/0) layer causes the Svaricap device extraction to fail in KLayout LVS |
| [#854](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/854) | 🔴 Open | bug | 🐛 LVS | Incorrect rhigh l and w extraction in klayout LVS |
| [#754](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/754) | 🔴 Open | bug | 🐛 LVS | LVS model mismatch between rfnmos/rfpmos xschem model name and KLayout model name |
| [#753](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/753) | 🔴 Open | bug | 🐛 LVS | klayout LVS does not check Nx parameter for SVaricap |
| [#729](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/729) | 🔴 Open | bug | 🐛 LVS | sg13g2 IO library spice file LVS mismatches |
| [#714](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/714) | 🔴 Open | bug | 🐛 LVS | Incorrect CDL for VSS I/O pad cell, or possibly an incorrect I/O cell layout. |
| [#712](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/712) | 🔴 Open | bug | 🐛 LVS | Incorrect extraction of resistor substrate in I/O cell library |
| [#707](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/707) | 🔴 Open | bug | 🐛 LVS | ESD diodes short VSS and substrate in LVS |
| [#582](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/582) | 🔴 Open | bug | 🐛 LVS | LVS/Extraction: Poly resistors need to account for third-terminal |
| [#555](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/555) | 🔴 Open | bug | 🐛 LVS | Discrepancy in LVS Netlist Extraction for Parallel Capacitors |
| [#527](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/527) | 🔴 Open | bug | 🐛 LVS | Magic does not extract Base of pnpMPA |
| [#512](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/512) | 🔴 Open | bug | 🐛 LVS | rfcmim LVS problems. |
| [#485](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/485) | 🔴 Open | bug | 🐛 LVS | i dont understand LVS for CAP_CMiM |
| [#459](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/459) | 🔴 Open | bug | 🐛 LVS | LVS Problem of two in series connected capacitors |
| [#443](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/443) | 🔴 Open | bug | 🐛 LVS | Klayout LVS of GDS vs two different CDL netlists is clean |
| [#433](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/433) | 🔴 Open | bug | 🐛 LVS | LVS sees two MOSFETs as one device |
| [#420](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/420) | 🔴 Open | bug | 🐛 LVS | LVS extracted netlist for npn13G2 with NE=2 also writes m=2 |
| [#414](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/414) | 🔴 Open | bug | 🐛 LVS | LVS issues related to svaricap device |
| [#347](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/347) | 🔴 Open | bug | 🐛 LVS | LVS behaviour with parallel MIM Capacitors |
| [#284](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/284) | 🔴 Open | bug | 🐛 LVS | LVS problem with pnpMPA |
| [#239](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/239) | 🔴 Open | bug | 🐛 LVS | SRAM macros failing LVS |
| [#723](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/723) | 🔴 Open | bug | 🐛 PyCells | klayout rf_cmim device does not enforce limits |
| [#716](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/716) | 🔴 Open | bug | 🐛 PyCells | klayout pcells for npn13g2L and npn13g2V do not respect restrictions on emitter length and width |
| [#649](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/649) | 🔴 Open | bug | 🐛 PyCells | In Klayout, multiplier for both pmos and nmos seems to do nothing. |
| [#760](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/760) | 🔴 Open | bug | 🐛 Simulation Models | Klayout - import netlist problems / difference between qucs-s and xschem device models |
| [#726](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/726) | 🔴 Open | bug | 🐛 Simulation Models | doc(npn13G2V): Mismatch between Spice model files and DRM for Nx parameter |
| [#657](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/657) | 🔴 Open | bug | 🐛 Simulation Models | SRAM Verilog models missing `timescale` directive |
| [#589](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/589) | 🔴 Open | bug | 🐛 Simulation Models | Parameter m (multiplier) missing in HBT xschem symbols (model files are fine) |
| [#560](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/560) | 🔴 Open | bug, external | 🐛 Simulation Models | Xyce plugins support limited to only 2 plugins |
| [#494](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/494) | 🔴 Open | bug | 🐛 Simulation Models | Problem with Netlist simplifier in KLayout |
| [#34](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/34) | 🔴 Open | bug | 🐛 Simulation Models | Unexpected behavior/values seen in small-signal models of thin-oxide devices. |
| [#718](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/718) | 🔴 Open | bug | 🐛 Symbols | capacitance equation in xschem `cmim` symbol doesn't look correct |
| [#835](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/835) | 🔴 Open | bug | 🐛 Digital Primitives | Abutment check for IO cells |
| [#676](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/676) | 🔴 Open | bug | 🐛 Digital Primitives | Maximum capacitance in liberty for output padcells seems way too low |
| [#615](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/615) | 🔴 Open | bug | 🐛 Digital Primitives | Wrong boundary layer/datatype in SRAM macro |
| [#298](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/298) | 🔴 Open | bug, documentation | 🐛 Digital Primitives | Inconsistencies in definitions of Rsil, Rppd, and Rhigh |
| [#183](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/183) | 🔴 Open | bug | 🐛 Digital Primitives | Missing Analog Pad cell from Liberty views |
| [#874](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/874) | 🔴 Open | bug | 🐛 IO Cells | ihp-sg13cmos5l: Bondpad has Metal5 |
| [#257](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/257) | 🔴 Open | bug | 🐛 Other | Local densities calculation using 800x800 [um] mislocated window  |
| [#209](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/209) | 🔴 Open | - | 🐛 Other | ifnone state-dependent path delay |
| [#842](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/842) | 🟢 Closed | bug | 🐛 DRC | DRC: Cnt.c.digibnd (modular) and Cnt.c.Digi (maximal) run simultaneously with different results |
| [#750](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/750) | 🟢 Closed | bug | 🐛 DRC | KLayout DRC Off-Grid checks are not performed |
| [#622](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/622) | 🟢 Closed | bug, external | 🐛 DRC | Bad obstruction dimension in LEF views of I/O Filler cells |
| [#602](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/602) | 🟢 Closed | bug | 🐛 DRC | inductor2 PCell produces offgrid errors if |
| [#569](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/569) | 🟢 Closed | bug | 🐛 DRC | HBT DRC and MPW |
| [#424](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/424) | 🟢 Closed | bug | 🐛 DRC | Metal1.filler in sealring |
| [#416](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/416) | 🟢 Closed | bug | 🐛 DRC | DRC shows spurious MnFil.a1 and TMnFil.a violations |
| [#404](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/404) | 🟢 Closed | bug | 🐛 DRC | Discrepancy between fill area and density computation area causes DRC error. |
| [#341](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/341) | 🟢 Closed | bug | 🐛 DRC | Error in DRC Maximal "GFill.j" |
| [#334](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/334) | 🟢 Closed | bug | 🐛 DRC | NoMet4Filler and NoMet5Filler missing in inductors_code.py |
| [#313](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/313) | 🟢 Closed | bug | 🐛 DRC | Seal.d errors |
| [#268](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/268) | 🟢 Closed | bug | 🐛 DRC | `M1.b` violation when `dllr_1` is abutted with other cells |
| [#246](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/246) | 🟢 Closed | bug | 🐛 DRC | NW.b violation when two ebufn_2 abutt themselves |
| [#235](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/235) | 🟢 Closed | bug | 🐛 DRC | Sealring Pcell dimenssion inconsistency |
| [#201](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/201) | 🟢 Closed | bug | 🐛 DRC | DRC seem to miss error on GatPoly Gat.b or Gat.b1 |
| [#184](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/184) | 🟢 Closed | bug | 🐛 DRC | Filler cells are missing in CDL/SPICE netlists |
| [#116](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/116) | 🟢 Closed | bug | 🐛 DRC | DRC violation in sealring |
| [#803](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/803) | 🟢 Closed | bug | 🐛 LVS | Extraction(cmim): bottom plate (Metal5)  doesn't act as a parasitic shield for top plate |
| [#802](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/802) | 🟢 Closed | bug | 🐛 LVS | Extraction(cmim): double capacitance count for top-plate capacitor |
| [#791](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/791) | 🟢 Closed | bug | 🐛 LVS | Magic techfile "extract" section RF MiM cap has the wrong order of arguments |
| [#773](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/773) | 🟢 Closed | bug | 🐛 LVS | KLayout LVS: `run_lvs.py` ignores arguments when `--net_only` is passed |
| [#772](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/772) | 🟢 Closed | bug | 🐛 LVS | KLayout LVS mismatch with extracted netlist |
| [#594](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/594) | 🟢 Closed | bug | 🐛 LVS | Polarity in ESD-Devices is wrong in LVS |
| [#456](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/456) | 🟢 Closed | bug | 🐛 LVS | Inductor PyCells not recognized by LVS |
| [#418](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/418) | 🟢 Closed | bug | 🐛 LVS | Device Present in Netlist but not showing during LVS |
| [#332](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/332) | 🟢 Closed | bug | 🐛 LVS | pTap guardring LVS issues |
| [#285](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/285) | 🟢 Closed | bug | 🐛 LVS | LVS seems to have problems to recognize RPPD in .GDS |
| [#98](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/98) | 🟢 Closed | bug | 🐛 LVS | Option GUI (alpha LVS) |
| [#90](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/90) | 🟢 Closed | bug | 🐛 LVS | RPPD not recognized on n-well (alpha LVS) |
| [#850](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/850) | 🟢 Closed | bug | 🐛 PyCells | `npn13G2` KLayout Pcell missing `HeatTrans` layer |
| [#741](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/741) | 🟢 Closed | bug | 🐛 PyCells | KLayout PyCell for rhigh: label contains rpnd, should be rhigh |
| [#640](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/640) | 🟢 Closed | bug | 🐛 PyCells | PCell/cmim: Minimum length of 1.14 µm is not valid |
| [#631](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/631) | 🟢 Closed | bug | 🐛 PyCells | Pcell label by libs.tech/klayout/python/sg13g2_pycell_lib/ihp/rppd_code.py |
| [#603](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/603) | 🟢 Closed | bug | 🐛 PyCells | via_stack PCell produces not connected aluminium if |
| [#290](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/290) | 🟢 Closed | bug | 🐛 PyCells | KLayout PCells Issue |
| [#289](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/289) | 🟢 Closed | bug | 🐛 PyCells | PCELL npn13G2 makes Min. nSD:block space to Cont (Note 2) = 0.00 |
| [#242](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/242) | 🟢 Closed | bug | 🐛 PyCells | Pcell "npn13G2_base" Layout Problem |
| [#188](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/188) | 🟢 Closed | bug | 🐛 PyCells | PCells in KLayout |
| [#54](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/54) | 🟢 Closed | bug | 🐛 PyCells | KLayout: PMOS and NMOS have different GatPoly Layers |
| [#876](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/876) | 🟢 Closed | - | 🐛 Simulation Models | Double entry of `nbv=1` in `ngspice/models/sg13g2_dschottky_nbl1_mod.lib` |
| [#752](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/752) | 🟢 Closed | bug | 🐛 Simulation Models | Question about MOSFET mismatch |
| [#743](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/743) | 🟢 Closed | bug | 🐛 Simulation Models | ngspice simulation with wrong destructive read on SRAM block |
| [#690](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/690) | 🟢 Closed | bug | 🐛 Simulation Models | diodes.lib weakness |
| [#650](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/650) | 🟢 Closed | bug | 🐛 Simulation Models | Inconsistent &amp; and &amp;&amp; usage in .lib for stdcells |
| [#611](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/611) | 🟢 Closed | bug | 🐛 Simulation Models | Bad syntax of diodevss_mod in ngspice |
| [#573](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/573) | 🟢 Closed | bug | 🐛 Simulation Models | Spice port order of Rev0.1.3 stdcells no longer compatible with xschem symbols |
| [#557](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/557) | 🟢 Closed | bug | 🐛 Simulation Models | Double prefix in stdcell names in verilog netlist created by xschem |
| [#551](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/551) | 🟢 Closed | bug | 🐛 Simulation Models | Simulation error for resistors in Xyce |
| [#496](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/496) | 🟢 Closed | bug | 🐛 Simulation Models | Simulation results are inconsistent across identical runs after May 11, 2025 PDK update |
| [#473](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/473) | 🟢 Closed | bug | 🐛 Simulation Models | Poly resistor contact resistance modelling. |
| [#445](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/445) | 🟢 Closed | bug | 🐛 Simulation Models | Resistors QA cells should be updated to include `PolyRes` layer |
| [#350](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/350) | 🟢 Closed | bug | 🐛 Simulation Models | m parameter in lv_mos models of Xyce in the current dev-branch dont work |
| [#318](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/318) | 🟢 Closed | bug | 🐛 Simulation Models | Noise Analysis Issue with PDK Resistor in Transimpedance Amplifier Design |
| [#288](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/288) | 🟢 Closed | bug | 🐛 Simulation Models | pnpMPA parameters cant be set or read |
| [#272](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/272) | 🟢 Closed | bug | 🐛 Simulation Models | Cut&amp;Paste error in statistical parameter file |
| [#262](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/262) | 🟢 Closed | bug | 🐛 Simulation Models | Misbehavior of BJTs npn13G2/npn13G2l/npn13G2v |
| [#231](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/231) | 🟢 Closed | bug | 🐛 Simulation Models | npn13g2 subckt simulation problem |
| [#205](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/205) | 🟢 Closed | bug | 🐛 Simulation Models | .spiceinit seems to produce errors in AC simulation |
| [#88](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/88) | 🟢 Closed | bug | 🐛 Simulation Models | dantenna &amp; dpantenna netlisting |
| [#61](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/61) | 🟢 Closed | bug | 🐛 Simulation Models | Discrepancy in pin order of stdcell spice models vs. xschem symbols |
| [#37](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/37) | 🟢 Closed | bug | 🐛 Simulation Models | it seems like the pnpMPA model and pnpMPA.sym have different pin-orders |
| [#24](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/24) | 🟢 Closed | bug | 🐛 Simulation Models | Simulation problem with diode model and elevated temperatures |
| [#499](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/499) | 🟢 Closed | bug | 🐛 Symbols | Application Error in IHP Menu of xschem |
| [#465](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/465) | 🟢 Closed | bug | 🐛 Symbols | Wrong format string in sg13g2_stdcells/sg13g2_dlhr_1.sym |
| [#180](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/180) | 🟢 Closed | bug | 🐛 Symbols | Stdcell schematics must contain multiplier = 1 |
| [#767](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/767) | 🟢 Closed | bug | 🐛 Digital Primitives | Incorrect units in max_cap for SRAMs |
| [#623](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/623) | 🟢 Closed | bug | 🐛 Digital Primitives | Missing Via obstruction layers in the LEF setup in the magic tech file |
| [#574](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/574) | 🟢 Closed | bug | 🐛 Digital Primitives | rppd instances in sg13g2_io.spi have no bulk terminal defined |
| [#442](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/442) | 🟢 Closed | bug | 🐛 Digital Primitives | sram macros adding shapes to 235/4 |
| [#345](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/345) | 🟢 Closed | bug | 🐛 Digital Primitives | KLayout: wrong LEF/DEF mapping for boundary |
| [#108](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/108) | 🟢 Closed | bug | 🐛 Digital Primitives | SG13G2 Standard Cells |
| [#94](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/94) | 🟢 Closed | bug | 🐛 Digital Primitives | Stdcell pin order |
| [#42](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/42) | 🟢 Closed | bug | 🐛 Digital Primitives | Major bug/problem in the a22oi_1 standard cell |
| [#250](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/250) | 🟢 Closed | bug | 🐛 IO Cells | Missing Cont in IO cells |
| [#115](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/115) | 🟢 Closed | bug | 🐛 IO Cells | Overlapping vias in IO cell |
| [#101](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/101) | 🟢 Closed | bug | 🐛 IO Cells | sg13g2_IOPadVdd |
| [#859](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/859) | 🟢 Closed | bug | 🐛 Infrastructure | Typo in klayout layer stack results in tract short |
| [#722](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/722) | 🟢 Closed | bug | 🐛 Other | TopMetal1 pitch seems too small |
| [#482](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/482) | 🟢 Closed | bug | 🐛 Other | Typo in netgen setup file. |
| [#439](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/439) | 🟢 Closed | bug | 🐛 Other | OpenEMS TLine Example and TLines in SG13G2 |
| [#339](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/339) | 🟢 Closed | bug | 🐛 Other | Use of deprecated feature imp in Python 3.12 |
| [#270](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/270) | 🟢 Closed | bug | 🐛 Other | adms-compile-va.sh script writes in a nonextisting directory:  |
| [#218](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/218) | 🟢 Closed | bug | 🐛 Other | Unexpected USE ANALOG |
| [#208](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/208) | 🟢 Closed | bug | 🐛 Other | LRM specify block delay path restrictions |
| [#167](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/167) | 🟢 Closed | bug | 🐛 Other | Fix pin labels in `a221oi_1` cell |
| [#166](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/166) | 🟢 Closed | bug, invalid | 🐛 Other | Routing issue in `dfrbp_1` flop |
| [#64](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/64) | 🟢 Closed | bug | 🐛 Other | Glitch in capacitance evaluation |
| [#5](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/5) | 🟢 Closed | bug | 🐛 Other | clk-pin not reacheable |
| [#4](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/4) | 🟢 Closed | bug | 🐛 Other | Wrong signal class for sg13g2_o21ai_1 cell |
| [#866](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/866) | 🔴 Open | - | DRC | scr1 layout in magic does not exempt LU.d |
| [#831](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/831) | 🔴 Open | - | DRC | Klayout DRC detects false errors with the Pad.gR rule |
| [#807](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/807) | 🔴 Open | - | DRC | density.drc: `extent.sized(0.0)` inflates chip area, underestimates global density |
| [#789](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/789) | 🔴 Open | - | DRC | DRC(isolbox): triggers Ant.h when using `diode_layer = &#39;t&#39;` |
| [#780](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/780) | 🔴 Open | - | DRC | consistency issues, DRC violations in `npn13G2` device TCL Pcell in Magic |
| [#713](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/713) | 🔴 Open | enhancement | DRC | Suggestion: provide a way to easily disable recommended DRC rules (or fix pad ring) |
| [#688](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/688) | 🔴 Open | - | DRC | Top-level DRC entry points |
| [#620](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/620) | 🔴 Open | enhancement | DRC | Vector instances (like C1[3..1] or M1[3:0]) cause problems in drc procedures |
| [#583](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/583) | 🔴 Open | question | DRC | `Rsil.e` violation in QA cells |
| [#493](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/493) | 🔴 Open | - | DRC | DRC of small CMIMs |
| [#440](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/440) | 🔴 Open | enhancement | DRC | minor enhancement to the log output of DRC rule deck |
| [#438](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/438) | 🔴 Open | enhancement | DRC | Relax metal filler rules |
| [#437](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/437) | 🔴 Open | enhancement | DRC | sealring PyCELL dont work on KLayout 3.0 |
| [#376](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/376) | 🔴 Open | documentation | DRC | MIM.i rule in magic tech |
| [#343](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/343) | 🔴 Open | documentation, question | DRC | Need clarification on rule LU.c/LU.c1 |
| [#308](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/308) | 🔴 Open | documentation | DRC | Documented seal ring rule does not match illustration and is probably incorrect |
| [#300](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/300) | 🔴 Open | documentation | DRC | QA cells: misunderstanding in Gat.b1 rule |
| [#99](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/99) | 🔴 Open | documentation | DRC | Slit rules in process spec |
| [#875](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/875) | 🔴 Open | - | LVS | LVS fails for isolated NMOS using isolbox |
| [#843](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/843) | 🔴 Open | - | LVS | LVS for rfnmos pcell with sg13_lv_nmos symbol |
| [#810](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/810) | 🔴 Open | - | LVS | Pin-Order mismatch between  sg13g2_stdcell.spice, sg13g2_stdcell.cdl and sg13g2_stdcell.lef |
| [#796](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/796) | 🔴 Open | - | LVS | LVS RuntimeError: "Terminal still connected after removing device" being faced in Klayout-LVS |
| [#788](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/788) | 🔴 Open | - | LVS | LVS not extracting isolated devices |
| [#786](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/786) | 🔴 Open | - | LVS | LVS flow for QUCS-S schematic vs xschem with inductor |
| [#784](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/784) | 🔴 Open | - | LVS | LVS: three terminal resistor device support |
| [#746](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/746) | 🔴 Open | - | LVS | resistor pcells and parameter extraction issues |
| [#711](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/711) | 🔴 Open | question | LVS | How to do parasitic extraction of open pdk standard cells |
| [#706](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/706) | 🔴 Open | - | LVS | Discrepancy in LVS Netlist Extraction for Parallel Resistors |
| [#701](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/701) | 🔴 Open | enhancement | LVS | `isolbox` update |
| [#692](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/692) | 🔴 Open | question | LVS | Can I do parasitic extraction using commerical tools? |
| [#667](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/667) | 🔴 Open | - | LVS | LVS Bugs |
| [#655](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/655) | 🔴 Open | - | LVS | Isolated ESD diodes are missing |
| [#634](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/634) | 🔴 Open | help wanted | LVS | Information required: Declaration of blank_circuit in LVS check (Klayout) |
| [#633](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/633) | 🔴 Open | enhancement | LVS | Incorrect LVS netlists created with xschem symbol updates. |
| [#597](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/597) | 🔴 Open | enhancement | LVS | Proposal to make correspondance between Ntap and Ptap annotation between Xschem and Klayout  LVS |
| [#516](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/516) | 🔴 Open | - | LVS | Klayout lvs with IHP : subckt ports not generated in .cir netlist |
| [#503](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/503) | 🔴 Open | - | LVS | Problem recognizing Rhigh with bends b&gt;0 |
| [#495](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/495) | 🔴 Open | - | LVS | Klayout LVS series resistor reduction rule modifies connectivity even if devices are not reduced. |
| [#484](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/484) | 🔴 Open | enhancement | LVS | LVS sees wrong placed net-label but thinks it dosent matter... |
| [#475](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/475) | 🔴 Open | - | LVS | LVS and TLines |
| [#469](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/469) | 🔴 Open | - | LVS | question: why does LVS dont accept distributed rppd? |
| [#468](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/468) | 🔴 Open | - | LVS | LVS for rppd works only with B=0 correct from Xschem |
| [#452](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/452) | 🔴 Open | question | LVS | How to connect the substrate contact of HBT NPN to substrate? |
| [#451](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/451) | 🔴 Open | - | LVS | LVS does not recognize an npn13G2l device with Nx=4 |
| [#336](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/336) | 🔴 Open | enhancement | LVS | Questions about LVS |
| [#254](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/254) | 🔴 Open | enhancement | LVS | LVS unexpectedly failing |
| [#858](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/858) | 🔴 Open | question | PyCells | Substrate 40/0 on pmos S/D |
| [#841](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/841) | 🔴 Open | - | PyCells | RF balun in IHP PDK |
| [#717](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/717) | 🔴 Open | documentation, question | PyCells | isolbox:  disagreement between documentation and pcell |
| [#685](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/685) | 🔴 Open | - | PyCells | Inductors in the PDK |
| [#609](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/609) | 🔴 Open | question | PyCells | HBT Bulk Connection to Substrate Layout |
| [#301](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/301) | 🔴 Open | - | PyCells | PyCell range constraint implementation |
| [#265](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/265) | 🔴 Open | enhancement | PyCells | Layout efficiency: Substrate tap, nwell tap, vias, improved MOSFET cells |
| [#834](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/834) | 🔴 Open | - | Simulation Models | resistor documentation not inline with ngspice library |
| [#765](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/765) | 🔴 Open | - | Simulation Models | Convergence issues in transient simulation with switched HBT devices |
| [#721](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/721) | 🔴 Open | question | Simulation Models | Are model definitions same for properitary and this open pdk ? |
| [#708](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/708) | 🔴 Open | - | Simulation Models | ESD diodes model do not match between individual models and pads |
| [#698](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/698) | 🔴 Open | enhancement | Simulation Models | Cell_footprint attribute in Liberty models. |
| [#680](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/680) | 🔴 Open | question | Simulation Models | Extraced spice netlist invalid |
| [#674](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/674) | 🔴 Open | - | Simulation Models | Transient simulation converges on one computer but not on another |
| [#626](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/626) | 🔴 Open | - | Simulation Models | Simulation Issue with sg13g2_sdfbbp_1: Cannot Test Falling Edge &amp; Potential Pin Order mismatch |
| [#593](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/593) | 🔴 Open | enhancement | Simulation Models | Request to update the layout parameterised cells in ihp 130nm |
| [#537](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/537) | 🔴 Open | enhancement | Simulation Models | Mismatch simulation in Xyce not possible |
| [#480](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/480) | 🔴 Open | - | Simulation Models | Error in OP annotation of npn13G2 transistors |
| [#462](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/462) | 🔴 Open | enhancement | Simulation Models | SRAM macro models - A_DLY pin |
| [#435](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/435) | 🔴 Open | enhancement | Simulation Models | `tt_stat` models are picking new random parameters per device instance |
| [#425](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/425) | 🔴 Open | - | Simulation Models | resistor warning from commercial PDK |
| [#368](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/368) | 🔴 Open | enhancement | Simulation Models | Issue with install.py scripts and .spiceinit |
| [#360](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/360) | 🔴 Open | question | Simulation Models | NGSPICE basic testcases : Unknown model type pspnqs103va |
| [#340](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/340) | 🔴 Open | question | Simulation Models | Need the Noise Test Circuits of HBTs |
| [#323](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/323) | 🔴 Open | - | Simulation Models | Discrepency between Ngspice and Xyce simulation |
| [#317](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/317) | 🔴 Open | - | Simulation Models | Ngspice cannot run transient with s2p files in matching networks |
| [#314](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/314) | 🔴 Open | - | Simulation Models | Simulation Issues with s2p File-based Inductors |
| [#310](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/310) | 🔴 Open | - | Simulation Models | Ngspice-42 or 43 Cannot calculate minimum noise figure (NFmin) if S2P file is used  |
| [#280](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/280) | 🔴 Open | enhancement | Simulation Models | [qucs-s] additional parameters for primitive devices and callbacks support |
| [#276](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/276) | 🔴 Open | enhancement, question | Simulation Models | m parameter for BJT models and Xschem-symbols |
| [#267](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/267) | 🔴 Open | enhancement | Simulation Models | Primitive device: PNP/NPN (vertical oder lateral) for CMOS-only |
| [#248](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/248) | 🔴 Open | enhancement | Simulation Models | Xyce sg13g2_moshv_stat.lib parameter question |
| [#89](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/89) | 🔴 Open | question | Simulation Models | A few more questions about nmos_code.py |
| [#38](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/38) | 🔴 Open | - | Simulation Models | gm/gds versus gate bias (lv_nmos) |
| [#827](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/827) | 🔴 Open | - | Symbols | xschem integration : mkdir commands in tcl scripts in ihp-sg13g2/libs.tech/xschem directory |
| [#817](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/817) | 🔴 Open | - | Symbols | Qucs-s: MOS transistors body terminals are placed off the grid |
| [#715](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/715) | 🔴 Open | enhancement | Symbols | `sub!` symbol for Qucs-S |
| [#580](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/580) | 🔴 Open | enhancement | Symbols | Updates to the xschem symbols definition |
| [#823](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/823) | 🔴 Open | enhancement | Digital Primitives | Switch default branch |
| [#761](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/761) | 🔴 Open | enhancement | Digital Primitives | Creating a stdcell version of low2high and high2low level shifters |
| [#647](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/647) | 🔴 Open | enhancement | Digital Primitives | Add prBoundary.boundary (189/4) bounding box to top-level SRAM macro cells |
| [#645](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/645) | 🔴 Open | enhancement | Digital Primitives | Add default bondpad to PDK |
| [#548](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/548) | 🔴 Open | enhancement | Digital Primitives | Remove „comp all“ and „name comp“ from the def2gds map file |
| [#431](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/431) | 🔴 Open | question | Digital Primitives | OpenLane support |
| [#311](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/311) | 🔴 Open | enhancement | Digital Primitives | Better alignment and clearer structures of std_cell |
| [#871](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/871) | 🔴 Open | enhancement | IO Cells | Breaker Cells for a Padframe with multiple Power Domains |
| [#464](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/464) | 🔴 Open | enhancement | IO Cells | Feature request: Pull-up / pull-down resistors for I/O cells |
| [#419](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/419) | 🔴 Open | enhancement | IO Cells | Feat Req: Add protection diodes to IO cell inputs (core side) |
| [#402](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/402) | 🔴 Open | enhancement | IO Cells | New "User Power" IO cell |
| [#401](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/401) | 🔴 Open | enhancement | IO Cells | Stronger IOPadAnalog connection |
| [#385](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/385) | 🔴 Open | enhancement | IO Cells | IOPadIOVss and IOPadVss don't have strong `TopMetal2` connections. |
| [#369](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/369) | 🔴 Open | documentation | IO Cells | Missing documentation / datasheets for IO cells |
| [#500](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/500) | 🔴 Open | documentation | Documentation | Missing max. voltage rating NPN13G2_BVCES |
| [#461](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/461) | 🔴 Open | documentation | Documentation | Question about maximum current in Rsil |
| [#458](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/458) | 🔴 Open | documentation, question | Documentation | Question about maximum currents/current densities |
| [#428](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/428) | 🔴 Open | documentation, question | Documentation | Documentation of Rppd |
| [#422](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/422) | 🔴 Open | documentation | Documentation | Capacitors for RF: more documentation needed |
| [#412](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/412) | 🔴 Open | documentation, question | Documentation | Angle checks |
| [#375](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/375) | 🔴 Open | documentation | Documentation | Process Spec 0.2: HV-NMOS/HV-PMOS spec unclear statement about validity conditions. |
| [#370](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/370) | 🔴 Open | documentation | Documentation | Process Specification Document: Unclear references for GatPoly in 2.13 |
| [#362](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/362) | 🔴 Open | documentation | Documentation | Vagueness in layer relations in layout_rules.pdf |
| [#346](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/346) | 🔴 Open | documentation | Documentation | DRM - pSD section - ThickGateOx mentionned but not shown |
| [#307](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/307) | 🔴 Open | - | Documentation | Discrepancy between documentation and layout on CuPillar |
| [#65](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/65) | 🔴 Open | documentation | Documentation | Missing Layer Annotation in PDK Spec PDF |
| [#33](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/33) | 🔴 Open | documentation | Documentation | matching data for transistors are missing in SG13G2_os_process_spec.pdf ... |
| [#868](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/868) | 🔴 Open | - | Infrastructure | Command in magic startup script breaks LibreLane |
| [#839](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/839) | 🔴 Open | - | Infrastructure | Update CODEOWNERS? |
| [#455](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/455) | 🔴 Open | enhancement | Infrastructure | Feature request: Improve XSection setup for KLayout (FEOL) |
| [#87](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/87) | 🔴 Open | enhancement | Infrastructure | Allow a centralised PDK installation of KLayout and the IHP PDK modules |
| [#830](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/830) | 🔴 Open | documentation, enhancement | Other | ciel is missing in readme |
| [#826](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/826) | 🔴 Open | - | Other | rppd device sheet resistance |
| [#824](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/824) | 🔴 Open | - | Other | utility_functions.py: sqrt not imported correctly |
| [#799](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/799) | 🔴 Open | question | Other | Temperature behaviour discrepancies between PDK's |
| [#774](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/774) | 🔴 Open | - | Other | How to use ntap1 / ptap1? |
| [#736](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/736) | 🔴 Open | enhancement | Other | Enhancement xscection: dedicated source layers |
| [#648](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/648) | 🔴 Open | question | Other | Usage of the substrate 40/0 layer and digisub 60/0 layer |
| [#502](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/502) | 🔴 Open | enhancement | Other | Enhancement: Via stack cell improvement |
| [#474](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/474) | 🔴 Open | - | Other | AttributeError: 'SimplePolygon' object has no attribute 'to_simple_polygon' when running pytest_c... |
| [#460](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/460) | 🔴 Open | question | Other | Use of the PDK for photonics? |
| [#322](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/322) | 🔴 Open | - | Other | Importing MOS library |
| [#299](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/299) | 🔴 Open | question | Other | Concern about the layout of the bipolar transistors |
| [#266](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/266) | 🔴 Open | enhancement | Other | Primitive device: MOMCAP |
| [#86](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/86) | 🔴 Open | enhancement | Other | Implement method of splitting substrate into local islands (using `DigiSub`) |
| [#46](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/46) | 🔴 Open | - | Other | VTH vs. W |
| [#847](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/847) | 🟢 Closed | - | DRC | Issued with magic support:  CONTBAR handled inconsistently, and slow DRC runtime |
| [#815](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/815) | 🟢 Closed | - | DRC | Klayout(DRC Options): can trigger a segfault if opened multiple times |
| [#779](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/779) | 🟢 Closed | - | DRC | KLayout DRC: rules `Sdiod.d` and `Sdiod.e` incorrectly applied |
| [#759](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/759) | 🟢 Closed | - | DRC | run_drc.py file does not exist |
| [#757](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/757) | 🟢 Closed | - | DRC | NMOS Current Density vs NFmin plot |
| [#679](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/679) | 🟢 Closed | - | DRC | NBL.f DRC error raised when placing two standard cell flip-flops above eachother |
| [#675](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/675) | 🟢 Closed | enhancement | DRC | Full DRC deck not yet implemented in klayout |
| [#664](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/664) | 🟢 Closed | - | DRC | newer DRC script gives me Seal.m error |
| [#662](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/662) | 🟢 Closed | enhancement | DRC | Issue with new DRC deck and npn13G2 transistor |
| [#652](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/652) | 🟢 Closed | enhancement | DRC | DRC script should accept zipped GDS files (gds.gz) |
| [#635](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/635) | 🟢 Closed | - | DRC | drc deck no longer compatible with klayout as of 0.30.3 |
| [#595](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/595) | 🟢 Closed | enhancement | DRC | issue with the active and gatpoly filler in case where Pwell.block is used |
| [#577](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/577) | 🟢 Closed | enhancement | DRC | Add DRC checks for S-varicap device in xschem |
| [#562](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/562) | 🟢 Closed | question | DRC | Questions about sealring For MPW shuttle runs |
| [#547](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/547) | 🟢 Closed | - | DRC | Problem With No Filler stack |
| [#518](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/518) | 🟢 Closed | - | DRC | Running into Pin.f violations |
| [#510](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/510) | 🟢 Closed | - | DRC | Default KLayout DRC report in script directory change to cell directory |
| [#498](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/498) | 🟢 Closed | - | DRC | sealring produces short-circuit in LVS |
| [#489](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/489) | 🟢 Closed | - | DRC | Sealring generator script fails with Klayout |
| [#436](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/436) | 🟢 Closed | - | DRC | DRC density error M1.j/k-M5.j/k |
| [#423](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/423) | 🟢 Closed | enhancement | DRC | Enhancement Req: Add `nofill` zones in IO cells |
| [#400](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/400) | 🟢 Closed | - | DRC | pSD.i violations in GDS generated from magic |
| [#337](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/337) | 🟢 Closed | enhancement | DRC | Can't Solve Fill Cell/Density DRC Error |
| [#305](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/305) | 🟢 Closed | - | DRC | KLAYOUT Not Integrating with IHP Open PDK [ LIBRARY AND DEVICES ARE NOT FOUND] |
| [#304](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/304) | 🟢 Closed | - | DRC | Undocumented layers in QA layouts for DRC |
| [#303](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/303) | 🟢 Closed | documentation | DRC | Incorrect illustration in DRC documentation |
| [#275](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/275) | 🟢 Closed | - | DRC | [DRC] Violating M2.b is sometimes not detected |
| [#271](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/271) | 🟢 Closed | - | DRC | LVS error after script Fill |
| [#221](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/221) | 🟢 Closed | enhancement | DRC | Separate KLayout DRC script and XML wrapper |
| [#9](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/9) | 🟢 Closed | documentation, enhancement | DRC | diode devices DRC and models |
| [#872](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/872) | 🟢 Closed | - | LVS | Xschem Inductor Netlist Not Generated for LVS |
| [#771](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/771) | 🟢 Closed | enhancement | LVS | Remove docopt dependency in `run_lvs.py` |
| [#581](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/581) | 🟢 Closed | question | LVS | Question about some layers in KLayout |
| [#530](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/530) | 🟢 Closed | - | LVS | The klayout GUI lvs file sg13g2_full.lylvs is not in-sync with batch sg13g2.lvs and the files in ... |
| [#504](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/504) | 🟢 Closed | - | LVS | Klayout extraction rules unpack hash as an array. |
| [#492](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/492) | 🟢 Closed | - | LVS | question about the extracted netlist from KLayout |
| [#406](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/406) | 🟢 Closed | enhancement | LVS | KLayout LVS scripts should be platform-agnostic |
| [#364](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/364) | 🟢 Closed | enhancement | LVS | LVS feature request: option for implicitly connecting nets |
| [#363](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/363) | 🟢 Closed | enhancement | LVS | Custom netlist parser makes LVS fail |
| [#203](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/203) | 🟢 Closed | - | LVS | how to use tolerances in LVS? |
| [#197](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/197) | 🟢 Closed | - | LVS | .spice net for LVS |
| [#196](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/196) | 🟢 Closed | - | LVS | a question to LVS from .spice |
| [#130](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/130) | 🟢 Closed | - | LVS | how was the layout versus scheme verification done ... |
| [#103](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/103) | 🟢 Closed | - | LVS | Series rhigh extraction (LVS alpha) |
| [#100](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/100) | 🟢 Closed | - | LVS | RPPD extraction (alpha LVS) |
| [#96](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/96) | 🟢 Closed | enhancement | LVS | Cap extraction (alpha LVS) |
| [#91](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/91) | 🟢 Closed | - | LVS | LVS vs. resistor positioning |
| [#12](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/12) | 🟢 Closed | - | LVS | wirebond-pads and ESD protection |
| [#833](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/833) | 🟢 Closed | - | PyCells | How to displaying unique NMOS/PMOS instance Names (MN1, MP1 etc.) in top-level layout in Klayout |
| [#769](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/769) | 🟢 Closed | - | PyCells | Inductor PCell doesn’t update estimated inductance and resistance when parameters change in KLayout |
| [#727](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/727) | 🟢 Closed | - | PyCells | Pycells are now dependent on an unknown python library called "cni"? |
| [#544](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/544) | 🟢 Closed | enhancement | PyCells | Remove `psutil` from the PCells |
| [#517](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/517) | 🟢 Closed | invalid | PyCells | Klayout:errors importing pycells |
| [#457](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/457) | 🟢 Closed | question | PyCells | Question about layouting rfcmim |
| [#415](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/415) | 🟢 Closed | - | PyCells | could the PCELL via_stack include GatePoly? |
| [#286](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/286) | 🟢 Closed | enhancement | PyCells | PCELL for npn13G2 seems broken |
| [#251](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/251) | 🟢 Closed | question | PyCells | Transmission Line, Balun, Transformers are missing.  |
| [#219](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/219) | 🟢 Closed | invalid, question | PyCells | KLAYOUT Unable to open SG13G2 Technology Files and Pycell Library |
| [#82](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/82) | 🟢 Closed | question | PyCells | nmos_code.py question |
| [#17](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/17) | 🟢 Closed | - | PyCells | cni.dlo module in pycell |
| [#857](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/857) | 🟢 Closed | invalid | Simulation Models | Capacitor model `cap_cmim` not honoring parameter `m=` |
| [#806](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/806) | 🟢 Closed | question | Simulation Models | Follow-up on Issue #314: Any workaround or solution for using s2p inductor models with QUCS-S + n... |
| [#805](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/805) | 🟢 Closed | - | Simulation Models | Flicker noise duplicated in my integrated noise report |
| [#804](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/804) | 🟢 Closed | - | Simulation Models | Channel thermal noise modelling |
| [#798](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/798) | 🟢 Closed | - | Simulation Models | rhigh thermal noise modelling across temperature |
| [#777](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/777) | 🟢 Closed | - | Simulation Models | `rfmode=1` reduces Cgg, Cgs, Cgd compared to `rfmode=0` for same DC bias for NMOS in QUCS-S |
| [#768](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/768) | 🟢 Closed | - | Simulation Models | QUCS-S + ngspice: Nutmeg equation fails when converting S21 to dB |
| [#763](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/763) | 🟢 Closed | - | Simulation Models | Transient simulation stops early when `rfmode=1` for `sg13_lv_nmos/pmos` in  XSCHEM+NGSPICE |
| [#749](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/749) | 🟢 Closed | - | Simulation Models | No output in ngspice noise analysis. |
| [#616](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/616) | 🟢 Closed | duplicate | Simulation Models | stdcells pinorder mismatch between symbols and spice -&gt; breaks simulation |
| [#612](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/612) | 🟢 Closed | - | Simulation Models | Inconsistent syntax in sg13g2_svaricaphv_mod.lib |
| [#606](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/606) | 🟢 Closed | - | Simulation Models | Only HV Mos and Res spice models:  Only the tt/typ corner shows temperature dependece |
| [#604](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/604) | 🟢 Closed | - | Simulation Models | Not attached @spiceprefix to @name for cap_cmim.sym and cap_rfcmim.sym at xschem |
| [#587](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/587) | 🟢 Closed | - | Simulation Models | xschem ngspice .include .save file |
| [#584](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/584) | 🟢 Closed | - | Simulation Models | Symbol and spice netlist don't match for Standardcells |
| [#570](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/570) | 🟢 Closed | - | Simulation Models | Phase Noise Estimation from Transient Simulation — Clarification on Noise Model Inclusion |
| [#566](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/566) | 🟢 Closed | - | Simulation Models | Cannot run simulation on test scheme |
| [#541](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/541) | 🟢 Closed | - | Simulation Models | Phase Noise Simulation Support for VCO at 140 GHz |
| [#524](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/524) | 🟢 Closed | - | Simulation Models | netgen tech file permutes HBT transistor collector and emitter. |
| [#523](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/523) | 🟢 Closed | - | Simulation Models | Differential EM Simulation using OpenEMS |
| [#521](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/521) | 🟢 Closed | enhancement | Simulation Models | Resistor models lacking parasitic capacitor when simulating with xyce |
| [#509](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/509) | 🟢 Closed | - | Simulation Models | Conflicts Between Verilog-A Component and PDK Elements Prevent Simulation |
| [#477](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/477) | 🟢 Closed | - | Simulation Models | GUARD RING FOR PMOS |
| [#448](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/448) | 🟢 Closed | question | Simulation Models | Unable to find definition of model (OSDI)  |
| [#403](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/403) | 🟢 Closed | duplicate | Simulation Models | transistor multiplier (m) effect does not appear in Xyce simulations |
| [#372](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/372) | 🟢 Closed | - | Simulation Models | pnpMPA model vs data |
| [#356](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/356) | 🟢 Closed | - | Simulation Models | ngspice Too few parameters for subcircuit type "npn13g2l" |
| [#352](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/352) | 🟢 Closed | - | Simulation Models | Compile for Xyce models fails |
| [#349](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/349) | 🟢 Closed | - | Simulation Models | Hybrid EM-Circuit Simulation Workflow for IHP SG13G2 |
| [#330](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/330) | 🟢 Closed | - | Simulation Models | Cannot retrieve lv_nmos model parameters (e.g. gds, cgs) |
| [#328](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/328) | 🟢 Closed | - | Simulation Models | Plotting MOS gm with Xyce  |
| [#327](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/327) | 🟢 Closed | - | Simulation Models | Unable to use PMOS with XYCE |
| [#315](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/315) | 🟢 Closed | - | Simulation Models | Undefined Parameter vbic_cje in NGSpice Netlist Simulation with SG13G2 Model Library |
| [#312](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/312) | 🟢 Closed | - | Simulation Models | Ngspice-42 or 43 Cannot calculate minimum noise figure (NFmin) if S2P file is used |
| [#309](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/309) | 🟢 Closed | - | Simulation Models | Signal Amplitude Depends on Simulation Duration in Ngspice 43 Transient Simulation |
| [#249](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/249) | 🟢 Closed | enhancement | Simulation Models | Can not run HBT example from Qucs-s using Xyce simulator |
| [#243](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/243) | 🟢 Closed | - | Simulation Models | Error in Qucs-s example simulation |
| [#236](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/236) | 🟢 Closed | - | Simulation Models | Xschem S-parameter simulation problem |
| [#234](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/234) | 🟢 Closed | question | Simulation Models | two Xyce example questions |
| [#232](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/232) | 🟢 Closed | - | Simulation Models | Xyce documetation could be improved: Xyce needs &gt;&gt;&gt; -plugin Xyce_Plugin_PSP103_VA.so &lt... |
| [#207](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/207) | 🟢 Closed | question | Simulation Models | Simulation of MOSFET noise with ngspice |
| [#191](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/191) | 🟢 Closed | question | Simulation Models | Resistor parameter `b` usage? |
| [#177](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/177) | 🟢 Closed | - | Simulation Models | sram: missing .lib files |
| [#164](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/164) | 🟢 Closed | - | Simulation Models | MOSFET PSP model usage of NF parameter |
| [#153](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/153) | 🟢 Closed | - | Simulation Models | qucs-s simulation with xyce |
| [#149](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/149) | 🟢 Closed | enhancement | Simulation Models | Statistical modeling with parameter mc_ok |
| [#148](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/148) | 🟢 Closed | - | Simulation Models | UDP and SDF forbids post-synthesis simulation with either Icarus Verilog or Verilator |
| [#143](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/143) | 🟢 Closed | question | Simulation Models | Does this have MEMRES model? |
| [#43](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/43) | 🟢 Closed | - | Simulation Models | LF-noise npn13g2 |
| [#41](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/41) | 🟢 Closed | - | Simulation Models | spef file resistor and capacitor value |
| [#39](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/39) | 🟢 Closed | - | Simulation Models | difference between npn13g2 and npn23g2l |
| [#30](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/30) | 🟢 Closed | question | Simulation Models | SOA checks for sg13g2 MOSFETs |
| [#27](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/27) | 🟢 Closed | - | Simulation Models | is it possible to get measured data of the sg13g2_pr.gds pnpMPA? |
| [#25](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/25) | 🟢 Closed | - | Simulation Models | sg13_lv_nmos ignores the "m" parameter |
| [#22](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/22) | 🟢 Closed | question | Simulation Models | question is the "sg13g2_pr.gds pnpMPA" usefull for band-gap references? |
| [#13](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/13) | 🟢 Closed | question | Simulation Models | ngspice models for varicap and schottky are missing |
| [#11](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/11) | 🟢 Closed | enhancement | Simulation Models | Resistor models lacking parasitic capacitor |
| [#3](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/3) | 🟢 Closed | enhancement | Simulation Models | missing model for `sg13_lv_nmos` |
| [#543](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/543) | 🟢 Closed | enhancement | Symbols | xschem: add upper limits for L in mosfets dimensions check |
| [#522](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/522) | 🟢 Closed | wontfix | Symbols | 5 terminal NMOS symbol with dedicated pin for n-well is missing |
| [#507](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/507) | 🟢 Closed | question | Symbols | Compatibility of PDK with Qucs-S Version 25.1.2 |
| [#497](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/497) | 🟢 Closed | - | Symbols | Can not run dc_hbt_12g2.sch in Xschem |
| [#421](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/421) | 🟢 Closed | question | Symbols | sub.sym: more description please |
| [#390](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/390) | 🟢 Closed | enhancement | Symbols | xschem NMOS symbol has the source up by default |
| [#389](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/389) | 🟢 Closed | enhancement | Symbols | Feature request: Add nmos3 / pmos3 symbols |
| [#32](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/32) | 🟢 Closed | enhancement | Symbols | symbols of mos-transistors better would use "l" and "w" instead of "L" and "W" because ... |
| [#31](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/31) | 🟢 Closed | - | Symbols | documentation: IHP-Open-PDK-main/ihp-sg13g2/libs.tech/xschem/README.md could be enhanced |
| [#20](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/20) | 🟢 Closed | - | Symbols | Xschem example circuits should not contain `pre_osdi` |
| [#860](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/860) | 🟢 Closed | - | Digital Primitives | 128x64 bit SRAM (single port) |
| [#832](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/832) | 🟢 Closed | - | Digital Primitives | OpenROAD: LEF58_ENCLOSURE with no CUTCLASS is not supported |
| [#744](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/744) | 🟢 Closed | - | Digital Primitives | SRAM macros with support for strobes |
| [#646](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/646) | 🟢 Closed | enhancement | Digital Primitives | Additional SRAM request |
| [#618](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/618) | 🟢 Closed | - | Digital Primitives | Librelane sg13g2_stdcell config.tcl isn't properly configured |
| [#506](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/506) | 🟢 Closed | question | Digital Primitives | MOS as Decap |
| [#410](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/410) | 🟢 Closed | question | Digital Primitives | sram: Missing cells in RM_IHPSG13_1P_1024x8_c2_bm_bist |
| [#392](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/392) | 🟢 Closed | - | Digital Primitives | SRAM: Purpose of BIST pins? |
| [#252](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/252) | 🟢 Closed | - | Digital Primitives | Use of the dummy liberty for I/O cells? |
| [#247](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/247) | 🟢 Closed | enhancement | Digital Primitives | Need automatic generation of layout assembly (simple in-line, all with all) to run abutment check... |
| [#237](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/237) | 🟢 Closed | enhancement | Digital Primitives | decap cells should be marked "CORE SPACER" in lef |
| [#173](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/173) | 🟢 Closed | enhancement | Digital Primitives | 32x32 SRAM |
| [#157](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/157) | 🟢 Closed | - | Digital Primitives | Cloning the submodule `digital` fails |
| [#126](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/126) | 🟢 Closed | - | Digital Primitives | Mention OpenROAD &amp; in support tools |
| [#112](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/112) | 🟢 Closed | enhancement | Digital Primitives | Smaller SRAMs |
| [#95](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/95) | 🟢 Closed | - | Digital Primitives | Use of wire_load_table prevent import to ORFS |
| [#92](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/92) | 🟢 Closed | - | Digital Primitives | Antenna diode definition in LEF |
| [#80](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/80) | 🟢 Closed | wontfix | Digital Primitives | Unsupported expression for cell sg13g2_sdfbbp_1 |
| [#72](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/72) | 🟢 Closed | - | Digital Primitives | ORFS do not insert decoupling cells |
| [#8](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/8) | 🟢 Closed | documentation | Digital Primitives | DCO enforced without defined what signed-off-by: means |
| [#813](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/813) | 🟢 Closed | - | IO Cells | bondpad have wrong origin |
| [#801](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/801) | 🟢 Closed | external | IO Cells | Reproducer for gds of IO cells |
| [#216](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/216) | 🟢 Closed | enhancement | IO Cells | IO cells AnalogPad - enhancement |
| [#840](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/840) | 🟢 Closed | documentation | Documentation | docs: add IO and Periphery library documentation#35 |
| [#770](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/770) | 🟢 Closed | documentation, question | Documentation | D_k of MIM Layer |
| [#658](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/658) | 🟢 Closed | documentation | Documentation | Constribution instructions - possibly outdated CLA text |
| [#463](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/463) | 🟢 Closed | documentation, question | Documentation | Questions about HBT Layout |
| [#366](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/366) | 🟢 Closed | - | Documentation | pull request on documentation |
| [#306](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/306) | 🟢 Closed | - | Documentation | Adding a link to the doc on this repo |
| [#199](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/199) | 🟢 Closed | documentation | Documentation | missing NW.d1 in Figure 5.1 of "SG13G2 Layout Rules Rev. 0.3" |
| [#81](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/81) | 🟢 Closed | documentation | Documentation | Incorrect pad recognition rule in Layout Rules Chapter 6.9 |
| [#740](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/740) | 🟢 Closed | question | Infrastructure | Klayout color palette has changed?  |
| [#542](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/542) | 🟢 Closed | enhancement | Infrastructure | CI: Cache KLayout |
| [#470](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/470) | 🟢 Closed | - | Infrastructure | fail to compile magic on fedora 42 |
| [#367](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/367) | 🟢 Closed | - | Infrastructure | Help, how to install/compile ADMS or openVAF on Windows? |
| [#321](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/321) | 🟢 Closed | - | Infrastructure | Manual for installation |
| [#264](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/264) | 🟢 Closed | - | Infrastructure | KLayout keybindings |
| [#849](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/849) | 🟢 Closed | - | Other | Netgen's setup does not permute W and L on MiM caps. |
| [#756](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/756) | 🟢 Closed | - | Other | CNI module |
| [#737](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/737) | 🟢 Closed | - | Other | testing automatic project handler |
| [#625](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/625) | 🟢 Closed | question | Other | Is timing characterization in the lib file is done with or without parasitics? |
| [#599](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/599) | 🟢 Closed | question | Other | Klayout + IHP PDK sg13g2 |
| [#550](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/550) | 🟢 Closed | - | Other | FFT Output Interpretation Issues: Resolution Effects, Frequency Shifts and Magnitude Scaling, |
| [#487](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/487) | 🟢 Closed | enhancement | Other | Tie Hi cell doesn't have contacts from rails to diffusion |
| [#472](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/472) | 🟢 Closed | - | Other | Klayout : problems opening .gds files |
| [#467](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/467) | 🟢 Closed | invalid | Other | question: if i try to draw on EXTBlock.drawing on KLayout 3.0.1 i get: ERRoR :: The selected Laye... |
| [#454](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/454) | 🟢 Closed | enhancement | Other | Feature request: D25 setup for KLayout |
| [#351](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/351) | 🟢 Closed | - | Other | Why is "ng" a divisor? And one more question... |
| [#325](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/325) | 🟢 Closed | question | Other | Query about RF Layout in KLayout |
| [#324](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/324) | 🟢 Closed | enhancement | Other | GSG / RF Signal Pad and DC Pads Missing |
| [#296](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/296) | 🟢 Closed | - | Other | Discrepancy in Bulk Substrate Thickness |
| [#240](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/240) | 🟢 Closed | - | Other | is there a IHP130nm.cfg for pygmid? |
| [#226](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/226) | 🟢 Closed | enhancement | Other | Missing requirements: `psutil` |
| [#223](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/223) | 🟢 Closed | question | Other | Rename all `sg13g2` occurrences to `ihp-sg13g2` |
| [#192](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/192) | 🟢 Closed | - | Other | top_lvl_pin |
| [#187](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/187) | 🟢 Closed | invalid | Other | PyPreprocessor &amp; new python version |
| [#186](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/186) | 🟢 Closed | enhancement | Other | large increase in area for ff compared to buf for upsize |
| [#169](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/169) | 🟢 Closed | question | Other | Any Recomended Python Versions? |
| [#158](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/158) | 🟢 Closed | - | Other | MOS Devices Tests Aren't Working. |
| [#114](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/114) | 🟢 Closed | question | Other | For loops that do not use loop variables in contactArray function. |
| [#59](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/59) | 🟢 Closed | - | Other | MC_OK variable for on chip variation across wafer and runs |
| [#52](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/52) | 🟢 Closed | enhancement | Other | Layout grid |
| [#10](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/10) | 🟢 Closed | question | Other | ihp pdk for ADS |
| [#2](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/2) | 🟢 Closed | invalid | Other | Invers operation correct? |
| [#1](https://github.com/IHP-GmbH/IHP-Open-PDK/issues/1) | 🟢 Closed | - | Other | Congratulations 🎉 |
