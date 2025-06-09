v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Uncomment the valid library:
hbt_typ ... without statistical and without mismatch modelling
hbt_typ_mismatch ... with mismatch modelling 
hbt_typ_stat ... with statistical modelling
hbt_typ_stat_mismatch ... with statistical and with mismatch modelling} -210 -1040 0 0 0.3 0.3 {layer=11}
T {Ctrl-Click to execute launcher} -360 -10 0 0 0.3 0.3 {layer=11}
T {Ctrl-Click to execute launcher} 220 -440 0 0 0.3 0.3 {layer=11}
T {Nx - number of emitters} 310 -20 0 0 0.2 0.2 {}
T {Nx - number of emitters} 560 -20 0 0 0.2 0.2 {}
N 220 -80 220 -60 {
lab=GND}
N 220 -150 220 -140 {
lab=#net1}
N 350 -120 350 -60 {
lab=GND}
N 480 -120 480 -60 {
lab=GND}
N 350 -220 350 -180 {
lab=#net2}
N 480 -220 480 -180 {
lab=#net3}
N 350 -150 400 -150 {
lab=GND}
N 400 -150 400 -60 {
lab=GND}
N 350 -220 380 -220 {
lab=#net2}
N 440 -220 480 -220 {
lab=#net3}
N 220 -150 310 -150 {
lab=#net1}
N 480 -220 510 -220 {lab=#net3}
N 570 -220 610 -220 {lab=#net4}
N 610 -220 610 -180 {lab=#net4}
N 550 -150 550 -60 {lab=GND}
N 550 -150 610 -150 {lab=GND}
N 610 -120 610 -60 {lab=GND}
N 730 -80 730 -60 {
lab=GND}
N 730 -150 730 -140 {
lab=#net5}
N 650 -150 730 -150 {lab=#net5}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {simulator_commands_shown.sym} 200 -680 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.SAMPLING
+useExpr=true
.options SAMPLES numsamples=3 SAMPLE_TYPE=MC 
.op
.dc Vce 1.5 1.5 0.1
.PRINT dc format=csv file=mc_hbt_op_xyce.csv I(Vc) I(Vc1)
"
"}
C {launcher.sym} 280 -460 0 0 {name=h2
descr=SimulateXyce
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,3,cmd) \{Xyce -plugin $env(PDK_ROOT)/$env(PDK)/libs.tech/xyce/plugins/Xyce_Plugin_r3_cmc.so \\"$N\\"\}

# change the simulator to be used (Xyce)
set sim(spice,default) 3

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} 200 -870 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
*.lib $::SG13G2_MODELS_XYCE/cornerHBT.lib hbt_typ
*.lib $::SG13G2_MODELS_XYCE/cornerHBT.lib hbt_typ_mismatch *not implemented!
*.lib $::SG13G2_MODELS_XYCE/cornerHBT.lib hbt_typ_stat
.lib $::SG13G2_MODELS_XYCE/cornerHBT.lib hbt_typ_stat_mismatch
)"}
C {simulator_commands_shown.sym} -370 -870 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
*.lib cornerHBT.lib hbt_typ
*.lib cornerHBT.lib hbt_typ_mismatch
*.lib cornerHBT.lib hbt_typ_stat
.lib cornerHBT.lib hbt_typ_stat_mismatch
"}
C {simulator_commands_shown.sym} -390 -700 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27

.control 
save all
let mc_runs = 3
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let Ic=unitvec(mc_runs)
let Ic1=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.I(Vc)
let Ic[run]= \{$dt\}.I(Vc)
let Ic1[run]= \{$dt\}.I(Vc1)
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata mc_hbt_op.csv \{$scratch\}.Ic \{$scratch\}.Ic1
write mc_hbt_op.raw
echo
print \{$scratch\}.Ic
print \{$scratch\}.Ic1

.endc
"
}
C {launcher.sym} -300 -30 0 0 {name=h1
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
C {devices/gnd.sym} 350 -60 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 220 -60 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 480 -150 0 0 {name=Vce value=1.5}
C {devices/gnd.sym} 480 -60 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 400 -60 0 0 {name=l4 lab=GND}
C {devices/isource.sym} 220 -110 2 0 {name=I0 value=1u}
C {devices/ammeter.sym} 410 -220 1 0 {name=Vc}
C {sg13g2_pr/npn13G2.sym} 330 -150 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1
}
C {sg13g2_pr/npn13G2.sym} 630 -150 0 1 {name=Q2
model=npn13G2
spiceprefix=X
Nx=1
}
C {devices/ammeter.sym} 540 -220 3 1 {name=Vc1}
C {devices/gnd.sym} 550 -60 0 0 {name=l6 lab=GND}
C {devices/gnd.sym} 610 -60 0 0 {name=l7 lab=GND}
C {devices/gnd.sym} 730 -60 0 0 {name=l8 lab=GND}
C {devices/isource.sym} 730 -110 2 0 {name=I1 value=1u}
