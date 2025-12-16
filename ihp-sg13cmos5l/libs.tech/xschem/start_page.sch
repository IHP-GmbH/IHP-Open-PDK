v {xschem version=3.4.8RC file_version=1.3
* Copyright 2023 IHP PDK Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.

}
G {}
K {}
V {}
S {}
F {}
E {}
P 4 5 430 -1040 430 -130 1830 -130 1830 -1040 430 -1040 {}
T {Useful stuff:} 430 -1080 0 0 0.6 0.6 {}
T {Load IHP SG13CMOS5L spice models for ngspice} 1190 -960 0 0 0.4 0.4 {}
T {Annotate operating points (voltages, currents) in schematic} 790 -260 0 0 0.4 0.4 {}
T {Read .raw file and load waves into Xschem graphs} 790 -210 0 0 0.4 0.4 {}
T {Load IHP SG13CMOS5L spice models for xyce} 1190 -650 0 0 0.4 0.4 {}
T {Create .save file, create netlist, simulate with ngspice} 790 -360 0 0 0.4 0.4 {}
T {Create netlist, simulate with xyce} 790 -310 0 0 0.4 0.4 {}
T {Simulation skeleton for ngspice} 1190 -780 0 0 0.4 0.4 {}
T {Simulation skeleton for xyce} 1190 -470 0 0 0.4 0.4 {}
T {Ctrl-Click to execute launcher} 440 -180 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} 440 -160 0 0 0.3 0.3 {layer=11}
T {DEVICE GALLERY} 70 -1030 0 0 0.6 0.6 {}
T {NGSPICE+Xyce testcases} 70 -920 0 0 0.6 0.6 {}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Copyright 2025 IHP PDK Authors"}
C {devices/launcher.sym} 150 -1140 0 0 {name=h1
descr="IHP-Open-PDK"
url="https://github.com/IHP-GmbH/IHP-Open-PDK/tree/main"}
C {simulator_commands_shown.sym} 440 -980 0 0 {
name=Libs_Ngspice
simulator=ngspice
only_toplevel=false
value="
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
.lib cornerRES.lib res_typ
.lib cornerDIO.lib dio_tt
"
      }
C {simulator_commands_shown.sym} 450 -620 0 0 {
name=Libs_Xyce
simulator=xyce
only_toplevel=false
value="tcleval(
.lib $::MODELS_XYCE/cornerMOSlv.lib mos_tt
.lib $::MODELS_XYCE/cornerMOShv.lib mos_tt
.lib $::MODELS_XYCE/cornerHBT.lib hbt_typ
.lib $::MODELS_XYCE/cornerRES.lib res_typ
.lib $::MODELS_XYCE/cornerDIO.lib dio_typ
)"
      }
C {devices/intuitive_interface_cheatsheet.sym} 1520 -1090 0 0 {name=x43}
C {devices/launcher.sym} 500 -250 0 0 {name=h2
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {devices/launcher.sym} 500 -200 0 0 {name=h3
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw dc
xschem setprop rect 2 0 fullxzoom
"
}
C {launcher.sym} 500 -350 0 0 {name=h4
descr=SimulateNGSPICE
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults
puts $sim(spice,1,cmd) 

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,1,cmd) \{ngspice  \\"$N\\" -a\}

# change the simulator to be used (Xyce)
set sim(spice,default) 0

# Create FET and BIP .save file
mkdir -p $netlist_dir
write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save

# run netlist and simulation
xschem netlist
simulate
"}
C {launcher.sym} 500 -300 0 0 {name=h5
descr=SimulateXyce
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,3,cmd) \{Xyce -plugin $env(PDK_ROOT)/$env(PDK)/libs.tech/xyce/plugins/Xyce_Plugin_PSP103_VA.so \\"$N\\"\}

# change the simulator to be used (Xyce)
set sim(spice,default) 3

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} 450 -460 0 0 {name=SimulatorXyce
simulator=xyce
only_toplevel=false
value="
.preprocess replaceground true
.option temp=27
.op
"
"}
C {simulator_commands_shown.sym} 450 -810 0 0 {name=SimulatorNGSPICE
simulator=ngspice
only_toplevel=false 
value="
.include <filename>.save
.param temp=27
.control
op
write <filename>.raw
.endc
"}
C {sg13cmos5l_pr/gallery.sym} 200 -980 0 0 {name=x1}
C {tests/IHP_testcases.sym} 200 -870 0 0 {name=x2}
