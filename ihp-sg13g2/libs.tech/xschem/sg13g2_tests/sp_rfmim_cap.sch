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
L 4 270 -320 270 -200 {}
L 4 280 -330 300 -320 {}
L 4 280 -310 300 -320 {}
L 4 280 -330 280 -310 {}
L 4 270 -320 280 -320 {}
L 4 770 -320 770 -200 {}
L 4 760 -320 770 -320 {}
L 4 760 -330 760 -310 {}
L 4 740 -320 760 -330 {}
L 4 740 -320 760 -310 {}
B 2 130 -1130 930 -730 {flags=graph

y2=5.3
ypos1=0
ypos2=2
divy=5
subdivy=8
unity=1
x1=1e+09
x2=2e+11
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=cseries
color=4
dataset=-1
unitx=1
logx=0
logy=1
y1=1.9}
B 2 950 -1130 1750 -730 {flags=graph
y1=0.26
y2=0.47
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=1e+09
x2=2e+11
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=rseries
color=4
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 1800 -1130 2600 -730 {flags=graph
y1=0.051
y2=1
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=1e+09
x2=2e+11
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0
color=4
node=s_2_1}
P 4 6 300 -320 300 -470 740 -470 740 -180 300 -180 300 -330 {}
T {use ac switch to load the waves:
xschem raw_read $netlist_dir/sp_rfmim_cap.raw ac} 840 -630 0 0 0.3 0.3 {}
N 80 -260 80 -230 {
lab=GND}
N 80 -380 80 -320 {
lab=in}
N 690 -260 690 -230 {
lab=GND}
N 690 -380 690 -320 {
lab=out}
N 370 -260 370 -230 {
lab=GND}
N 370 -380 370 -320 {
lab=in}
N 830 -260 830 -230 {
lab=GND}
N 830 -380 830 -320 {
lab=out}
N 690 -390 690 -380 {
lab=out}
N 370 -400 370 -380 {
lab=in}
N 690 -380 830 -380 {
lab=out}
N 370 -380 500 -380 {
lab=in}
N 560 -380 690 -380 {
lab=out}
N 80 -380 370 -380 {
lab=in}
N 530 -350 530 -230 {
lab=GND}
C {devices/code_shown.sym} 50 -660 0 0 {name=NGSPICE
only_toplevel=true
value="
.control
save all
sp lin 500 1e9 200e9 0
let Cseries = 1e+15/(2*PI*frequency*imag(1/Y_2_1))
let Rseries = -real(1/Y_2_1)
let s21=vdb(s_2_1)
write sp_rfmim_cap.raw
.endc
" }
C {devices/title.sym} 160 -30 0 0 {name=l1 author="Copyright 2023 IHP PDK Authors"}
C {devices/res.sym} 370 -290 0 0 {name=R1
value=1Meg
footprint=1206
device=resistor
m=1}
C {devices/vsource.sym} 80 -290 0 0 {name=V1 value="dc 0 ac 1 portnum 1 z0 50"}
C {devices/code_shown.sym} 30 -140 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerCAP.lib cap_wcs
"}
C {devices/gnd.sym} 370 -230 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 80 -230 0 0 {name=l4 lab=GND}
C {devices/res.sym} 690 -290 0 0 {name=R2
value=1Meg
footprint=1206
device=resistor
m=1}
C {devices/gnd.sym} 690 -230 0 0 {name=l5 lab=GND}
C {devices/vsource.sym} 830 -290 0 0 {name=V2 value="dc 0 ac 0 portnum 2 z0 50"}
C {devices/gnd.sym} 830 -230 0 0 {name=l6 lab=GND}
C {devices/lab_pin.sym} 370 -400 1 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 690 -390 1 0 {name=p2 sig_type=std_logic lab=out}
C {devices/launcher.sym} 900 -650 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/sp_rfmim_cap.raw ac"
}
C {devices/gnd.sym} 530 -230 0 0 {name=l2 lab=GND}
C {sg13g2_pr/cap_rfcmim.sym} 530 -380 3 0 {name=C1 
model=cap_rfcmim
w=2.0e-6
l=2.0e-6
wfeed=5.0e-6
spiceprefix=X}
