v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Uncomment the valid library:
mos_tt ... without statistical and without mismatch modelling
mos_tt_mismatch ... with mismatch modelling
mos_tt_stat ... with statistical modelling
mos_tt_stat_mismatch ... with statistical and with mismatch modelling} 380 -580 0 0 0.3 0.3 {layer=11}
T {Ctrl-Click to execute launcher} 380 -300 0 0 0.3 0.3 {layer=11}
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
N 750 -20 750 40 {
lab=GND}
N 750 -50 800 -50 {
lab=GND}
N 800 -50 800 40 {
lab=GND}
N 750 -200 750 -180 {
lab=GND}
N 750 -100 750 -80 {
lab=Vgs1}
N 670 -50 710 -50 {
lab=Vgs1}
N 670 -100 670 -50 {
lab=Vgs1}
N 670 -100 750 -100 {
lab=Vgs1}
N 650 -100 670 -100 {
lab=Vgs1}
N 750 -120 750 -100 {
lab=Vgs1}
C {devices/code_shown.sym} -300 -440 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27

.control

let mc_runs = 3
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let vg=unitvec(mc_runs)
let vg1=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

*dc Vds 0 3 0.01
op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.Vgs
let Vg[run]=\{$dt\}.Vgs
let Vg1[run]=\{$dt\}.Vgs1
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata sg13_hv_nmos_cs.csv \{$scratch\}.vg \{$scratch\}.vg1
write sg13_hv_nmos_cs.raw
echo
print \{$scratch\}.vg \{$scratch\}.vg1

.endc
"}
C {devices/gnd.sym} 480 40 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 530 40 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} 480 -150 0 0 {name=I0 value=10u}
C {devices/gnd.sym} 480 -200 2 0 {name=l2 lab=GND}
C {devices/lab_pin.sym} 380 -100 0 0 {name=p1 sig_type=std_logic lab=Vgs}
C {sg13g2_pr/sg13_hv_nmos.sym} 460 -50 0 0 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/gnd.sym} 750 40 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 800 40 0 0 {name=l6 lab=GND}
C {devices/isource.sym} 750 -150 0 0 {name=I1 value=10u}
C {devices/gnd.sym} 750 -200 2 0 {name=l7 lab=GND}
C {devices/lab_pin.sym} 650 -100 0 0 {name=p2 sig_type=std_logic lab=Vgs1}
C {sg13g2_pr/sg13_hv_nmos.sym} 730 -50 0 0 {name=M2
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/code_shown.sym} 380 -440 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
*.lib $::SG13G2_MODELS/cornerMOShv.lib mos_tt
*.lib $::SG13G2_MODELS/cornerMOShv.lib mos_tt_mismatch
*.lib $::SG13G2_MODELS/cornerMOShv.lib mos_tt_stat
.lib $::SG13G2_MODELS/cornerMOShv.lib mos_tt_stat_mismatch
"}
C {launcher.sym} 440 -260 0 0 {name=h3
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
