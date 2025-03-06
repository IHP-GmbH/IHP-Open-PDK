v {xschem version=3.4.5 file_version=1.2
* Copyright 2021 Stefan Frederik Schippers
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
E {}
B 2 530 -910 1330 -510 {flags=graph


ypos1=0
ypos2=2
divy=5
subdivy=8
unity=1
x1=6
x2=9
divx=5
subdivx=8
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=1
logy=1
y1=-0.26
y2=-7.3e-07
color=4
node=out
rainbow=1}
N 340 -260 340 -230 {
lab=GND}
N 340 -380 340 -320 {
lab=in}
N 690 -260 690 -230 {
lab=GND}
N 690 -380 690 -320 {
lab=out}
N 690 -390 690 -380 {
lab=out}
N 370 -400 370 -380 {
lab=in}
N 370 -380 500 -380 {
lab=in}
N 560 -380 690 -380 {
lab=out}
N 340 -380 370 -380 {
lab=in}
C {devices/title.sym} 160 -30 0 0 {name=l1 author="Copyright 2023 IHP PDK Authors"}
C {devices/vsource.sym} 340 -290 0 0 {name=V1 value="dc 0 ac 1"}
C {devices/gnd.sym} 340 -230 0 0 {name=l4 lab=GND}
C {devices/res.sym} 690 -290 0 0 {name=R2
value=100k
footprint=1206
device=resistor
m=1}
C {devices/gnd.sym} 690 -230 0 0 {name=l5 lab=GND}
C {devices/lab_pin.sym} 370 -400 1 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 690 -390 1 0 {name=p2 sig_type=std_logic lab=out}
C {devices/launcher.sym} 200 -740 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/ac_mim_cap.raw ac"
}
C {sg13g2_pr/cap_cmim.sym} 530 -380 1 0 {name=C1 model=cap_cmim w=10.0e-6 l=70.0e-6 m=1 spiceprefix=X}
C {simulator_commands_shown.sym} 1370 -730 0 0 {name=Simulator
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.ac dec 1001 1meg 1000meg
.print ac format=raw file=ac_mim_cap.raw V(in) V(out)
"
"}
C {launcher.sym} 1450 -570 0 0 {name=h1
descr=SimulateXyce
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,3,cmd) \{Xyce \\"$N\\"\}

# change the simulator to be used (Xyce)
set sim(spice,default) 3

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} 1380 -850 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerCAP.lib cap_typ
.lib $::SG13G2_MODELS_XYCE/cornerRES.lib res_typ
)"}
C {simulator_commands_shown.sym} 1370 -470 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerCAP.lib cap_typ
.lib cornerRES.lib res_typ
"}
C {launcher.sym} 1460 -110 0 0 {name=h2
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

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} 1380 -340 0 0 {name=Simulator1
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
ac dec 1000 1e6 1e9 
let mag=abs(out)
meas ac freq_at when mag = 0.707
let C = 1/(2*PI*freq_at*1e+5)
print C
write ac_mim_cap.raw 
.endc
"}
