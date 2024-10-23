v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 480 -20 480 40 {
lab=GND}
N 480 -50 530 -50 {
lab=GND}
N 530 -50 530 40 {
lab=GND}
N 480 -200 480 -180 {
lab=GND}
N 480 -100 480 -80 {
lab=Vgs}
N 400 -50 440 -50 {
lab=Vgs}
N 400 -100 400 -50 {
lab=Vgs}
N 400 -100 480 -100 {
lab=Vgs}
N 380 -100 400 -100 {
lab=Vgs}
N 480 -120 480 -100 {
lab=Vgs}
C {devices/code_shown.sym} 260 110 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_tt_stat
"}
C {devices/code_shown.sym} -300 -440 0 0 {name=NGSPICE only_toplevel=true 
value="
.param mm_ok=1
.param mc_ok=1
.param temp=27

.control
let mc_runs = 1000
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let vg=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

*dc Vds 0 3 0.01
op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.Vgs
let Vg[run]=\{$dt\}.Vgs
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata sg13_hv_pmos_cs.csv \{$scratch\}.vg
write sg13_hv_pmos_cs.raw
echo
print \{$scratch\}.vg

.endc
"}
C {devices/gnd.sym} 480 40 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 530 40 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} 480 -150 2 0 {name=I0 value=10u}
C {devices/gnd.sym} 480 -200 2 0 {name=l2 lab=GND}
C {devices/lab_pin.sym} 380 -100 0 0 {name=p1 sig_type=std_logic lab=Vgs}
C {sg13g2_pr/sg13_hv_pmos.sym} 460 -50 2 1 {name=M1
l=1.0u
w=2.0u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
