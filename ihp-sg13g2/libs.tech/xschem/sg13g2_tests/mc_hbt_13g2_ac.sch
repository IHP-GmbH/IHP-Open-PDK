v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Nx - number of emitters} 20 20 0 0 0.2 0.2 {}
N -200 -30 -200 -10 {
lab=GND}
N -200 -100 -200 -90 {
lab=#net1}
N 60 -70 60 -10 {
lab=GND}
N 190 -70 190 -10 {
lab=GND}
N 60 -170 60 -130 {
lab=Vc}
N 190 -170 190 -130 {
lab=#net2}
N 60 -100 110 -100 {
lab=GND}
N 110 -100 110 -10 {
lab=GND}
N 60 -170 90 -170 {
lab=Vc}
N 150 -170 190 -170 {
lab=#net2}
N -200 -100 -130 -100 {
lab=#net1}
N 40 -170 60 -170 {
lab=Vc}
N -20 -100 20 -100 {
lab=Vb}
N -20 -130 -20 -100 {
lab=Vb}
N -70 -100 -20 -100 {
lab=Vb}
C {devices/code_shown.sym} -200 160 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ_stat
*.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
"}
C {devices/code_shown.sym} 300 -350 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.param mc_ok = 1

.control 
let mc_runs = 1000
let run = 0
shell rm mc_hbt_3dB.csv
***************** LOOP *********************
dowhile run < mc_runs
reset
set run=$&run
save all
ac dec 10 10k 1000meg 
meas ac vnom_at FIND Vc AT=100k 
let v3db = vnom_at*0.707
meas ac freq_3dB when Vc=v3db
print freq_3dB >> mc_hbt_3dB.csv
let run=run+1 
end
***************** LOOP *********************
.endc
"


}
C {devices/gnd.sym} 60 -10 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -200 -10 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 190 -100 0 0 {name=Vce value=5}
C {devices/gnd.sym} 190 -10 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 110 -10 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {sg13g2_pr/npn13G2.sym} 40 -100 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1}
C {devices/res.sym} 120 -170 1 0 {name=R1
value=40k
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 40 -170 0 0 {name=p1 sig_type=std_logic lab=Vc}
C {devices/vsource.sym} -200 -60 0 0 {name=Vce1 value="dc 0.8 ac 1m"}
C {devices/res.sym} -100 -100 1 0 {name=R2
value=33k
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} -20 -130 0 0 {name=p2 sig_type=std_logic lab=Vb}
