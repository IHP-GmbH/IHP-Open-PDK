v {xschem version=3.4.4 file_version=1.2
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
N 70 -300 70 -270 {
lab=GND}
N 70 -420 70 -360 {
lab=in}
N 420 -300 420 -270 {
lab=GND}
N 420 -420 420 -360 {
lab=out}
N 420 -430 420 -420 {
lab=out}
N 100 -440 100 -420 {
lab=in}
N 100 -420 230 -420 {
lab=in}
N 290 -420 420 -420 {
lab=out}
N 70 -420 100 -420 {
lab=in}
C {devices/code_shown.sym} 530 -530 0 0 {name=NGSPICE
only_toplevel=true
value="
.param mc_ok = 1
.control 
let mc_runs = 1000
let run = 0
shell rm mc_cmim.csv
***************** LOOP *********************
dowhile run < mc_runs
reset
set run=$&run
save all
ac dec 1000 1e6 100e9 
let mag=abs(out)
meas ac freq_at when mag = 0.707
let C = 1/(2*PI*freq_at*1e+5)
print C >> mc_cmim.csv
let run=run+1 
end
***************** LOOP *********************
.endc
" }
C {devices/title.sym} 160 -30 0 0 {name=l1 author="Copyright 2023 IHP PDK Authors"}
C {devices/vsource.sym} 70 -330 0 0 {name=V1 value="dc 0 ac 1"}
C {devices/code_shown.sym} 30 -140 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerCAP.lib cap_wcs_stat
"}
C {devices/gnd.sym} 70 -270 0 0 {name=l4 lab=GND}
C {devices/res.sym} 420 -330 0 0 {name=R2
value=100k
footprint=1206
device=resistor
m=1}
C {devices/gnd.sym} 420 -270 0 0 {name=l5 lab=GND}
C {devices/lab_pin.sym} 100 -440 1 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 420 -430 1 0 {name=p2 sig_type=std_logic lab=out}
C {sg13g2_pr/cap_cmim.sym} 260 -420 1 0 {name=C1 model=cap_cmim w=7.0e-6 l=7.0e-6 MF=1 spiceprefix=X}
