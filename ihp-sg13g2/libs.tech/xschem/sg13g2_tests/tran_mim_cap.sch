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
B 2 30 -920 830 -520 {flags=graph
y1=-2
y2=4.5
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=6e-06
divx=5
subdivx=1
node="g
g2"
color="4 5"
dataset=-1
unitx=1
logx=0
logy=0
}
N 40 -470 40 -440 { lab=0}
N 40 -320 40 -250 { lab=G}
N 40 -190 40 -160 { lab=0}
N 330 -250 330 -230 { lab=REF}
N 330 -320 330 -310 { lab=G}
N 40 -320 330 -320 { lab=G}
N 40 -380 40 -320 { lab=G}
N 470 -470 470 -440 { lab=0}
N 470 -320 470 -250 { lab=G2}
N 470 -190 470 -160 { lab=0}
N 610 -250 610 -230 { lab=REF}
N 610 -320 610 -310 { lab=G2}
N 470 -320 610 -320 { lab=G2}
N 470 -380 470 -320 { lab=G2}
N 300 -460 300 -440 { lab=REF}
C {devices/code_shown.sym} 710 -360 0 0 {name=NGSPICE
only_toplevel=true
value="
.control
save all
tran 10n 6u
write test_mim_cap.raw
.endc
" }
C {devices/title.sym} 160 -30 0 0 {name=l1 author="Copyright 2023 IHP PDK Authors"}
C {devices/lab_pin.sym} 40 -280 0 0 {name=p4 lab=G}
C {devices/isource.sym} 40 -410 0 0 {name=I1 value="pwl 0 0 1000n 0 1010n 100n"}
C {devices/lab_pin.sym} 40 -470 0 0 {name=p1 lab=0}
C {devices/lab_pin.sym} 40 -160 0 0 {name=p2 lab=0}
C {devices/res.sym} 330 -280 0 0 {name=R1
value=1G
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 330 -230 0 0 {name=p5 lab=REF}
C {devices/lab_pin.sym} 470 -280 0 0 {name=p9 lab=G2}
C {devices/isource.sym} 470 -410 0 0 {name=I3 value="pwl 0 0 1000n 0 1010n 100n"}
C {devices/lab_pin.sym} 470 -470 0 0 {name=p11 lab=0}
C {devices/lab_pin.sym} 470 -160 0 0 {name=p12 lab=0}
C {devices/res.sym} 610 -280 0 0 {name=R3
value=1G
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 610 -230 0 0 {name=p13 lab=REF}
C {devices/capa.sym} 470 -220 0 0 {name=C1
m=1
value=0.07452p
footprint=1206
device="ceramic capacitor"}
C {devices/vsource.sym} 300 -410 0 0 {name=V1 value=-2}
C {devices/lab_pin.sym} 300 -380 0 0 {name=p14 lab=0}
C {devices/lab_pin.sym} 300 -460 0 1 {name=p15 lab=REF}
C {devices/code_shown.sym} 0 -110 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
"}
C {devices/launcher.sym} 780 -450 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/test_mim_cap.raw tran"
}
C {sg13g2_pr/cap_cmim.sym} 40 -220 0 0 {name=C2
model=cap_cmim
w=7.0e-6
l=7.0e-6
m=1
spiceprefix=X}
