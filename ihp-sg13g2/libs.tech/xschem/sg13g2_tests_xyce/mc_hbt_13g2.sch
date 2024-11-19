v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Nx - number of emitters} -110 80 0 0 0.2 0.2 {}
N -200 30 -200 50 {
lab=GND}
N -200 -40 -200 -30 {
lab=#net1}
N -70 -10 -70 50 {
lab=GND}
N 60 -10 60 50 {
lab=GND}
N -70 -110 -70 -70 {
lab=#net2}
N 60 -110 60 -70 {
lab=#net3}
N -70 -40 -20 -40 {
lab=GND}
N -20 -40 -20 50 {
lab=GND}
N -70 -110 -40 -110 {
lab=#net2}
N 20 -110 60 -110 {
lab=#net3}
N -200 -40 -110 -40 {
lab=#net1}
C {devices/code_shown.sym} -200 160 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ_stat
*.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
"}
C {devices/code_shown.sym} 400 -590 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.param mc_ok = 1

.control 
save all
let mc_runs = 1000
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let Ic=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.I(Vc)
let Ic[run]= \{$dt\}.I(Vc)
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata mc_hbt_op.csv \{$scratch\}.Ic
write mc_hbt_op.raw
echo
print \{$scratch\}.Ic

.endc
"}
C {devices/gnd.sym} -70 50 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -200 50 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 60 -40 0 0 {name=Vce value=1.5}
C {devices/gnd.sym} 60 50 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -20 50 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} -200 0 2 0 {name=I0 value=1u}
C {sg13g2_pr/npn13G2.sym} -90 -40 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1}
C {devices/ammeter.sym} -10 -110 1 0 {name=Vc}
