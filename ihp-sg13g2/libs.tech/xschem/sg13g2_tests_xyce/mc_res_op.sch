v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Uncomment the valid library:
res_typ ... without statistical and without mismatch modelling
res_typ_mismatch ... with mismatch modelling
res_typ_stat ... with statistical modelling
res_typ_stat_mismatch ... with statistical and with mismatch modelling} -220 -900 0 0 0.3 0.3 {layer=11}
T {Ctrl-Click to execute launcher} -380 300 0 0 0.3 0.3 {layer=11}
T {Ctrl-Click to execute launcher} 210 -300 0 0 0.3 0.3 {layer=11}
N 180 260 180 320 {
lab=GND}
N 180 120 180 200 {
lab=Vcc}
N 180 120 300 120 {
lab=Vcc}
N 300 120 300 160 {
lab=Vcc}
N 300 220 300 240 {
lab=#net1}
N 300 300 300 320 {
lab=GND}
N 570 120 570 160 {
lab=Vcc}
N 570 220 570 240 {
lab=#net2}
N 570 300 570 320 {
lab=GND}
N 850 120 850 160 {
lab=Vcc}
N 850 220 850 240 {
lab=#net3}
N 850 300 850 320 {
lab=GND}
N 440 120 570 120 {
lab=Vcc}
N 710 120 850 120 {
lab=Vcc}
N 440 120 440 160 {
lab=Vcc}
N 440 220 440 240 {
lab=#net4}
N 440 300 440 320 {
lab=GND}
N 300 120 440 120 {lab=Vcc}
N 710 120 710 160 {
lab=Vcc}
N 710 220 710 240 {
lab=#net5}
N 710 300 710 320 {
lab=GND}
N 570 120 710 120 {lab=Vcc}
N 990 120 990 160 {
lab=Vcc}
N 990 220 990 240 {
lab=#net6}
N 990 300 990 320 {
lab=GND}
N 850 120 990 120 {lab=Vcc}
C {devices/gnd.sym} 300 320 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 180 230 0 0 {name=Vres value=1.5}
C {devices/gnd.sym} 180 320 0 0 {name=l3 lab=GND}
C {devices/title.sym} -130 440 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/lab_pin.sym} 180 170 2 0 {name=p1 sig_type=std_logic lab=Vcc}
C {devices/ammeter.sym} 300 190 0 0 {name=Vsil}
C {devices/gnd.sym} 570 320 0 0 {name=l2 lab=GND}
C {devices/ammeter.sym} 570 190 0 0 {name=Vppd}
C {devices/gnd.sym} 850 320 0 0 {name=l4 lab=GND}
C {sg13g2_pr/rhigh.sym} 850 270 0 0 {name=R3
w=1.0e-6
l=1.0e-6
model=rhigh
spiceprefix=X
m=1
R=3.061e+3
Imax=0.11e-4
}
C {devices/ammeter.sym} 850 190 0 0 {name=Vrh}
C {sg13g2_pr/rsil.sym} 300 270 0 0 {name=R1
w=0.5e-6
l=0.5e-5
model=rsil
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {sg13g2_pr/rppd.sym} 570 270 0 0 {name=R2
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {simulator_commands_shown.sym} 190 -540 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.SAMPLING
+useExpr=true
.options SAMPLES numsamples=3 SAMPLE_TYPE=MC 
.op
.dc Vres 1.5 1.5 0.1
.PRINT dc format=csv file=mc_res_op_xyce.csv I(Vsil) I(Vsil1) I(Vppd) I(Vppd1) I(Vrh) I(Vrh1)
"
"}
C {launcher.sym} 270 -320 0 0 {name=h2
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
C {simulator_commands_shown.sym} 190 -730 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
*.lib $::SG13G2_MODELS_XYCE/cornerRES.lib res_typ
*.lib $::SG13G2_MODELS_XYCE/cornerRES.lib res_typ_mismatch
*.lib $::SG13G2_MODELS_XYCE/cornerRES.lib res_typ_stat
.lib $::SG13G2_MODELS_XYCE/cornerRES.lib res_typ_stat_mismatch
)"}
C {simulator_commands_shown.sym} -380 -730 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
*.lib cornerRES.lib res_typ
*.lib cornerRES.lib res_typ_mismatch
*.lib cornerRES.lib res_typ_stat
.lib cornerRES.lib res_typ_stat_mismatch
"}
C {simulator_commands_shown.sym} -400 -560 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control 
let mc_runs = 3
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let rsilval=unitvec(mc_runs)
let rsilval1=unitvec(mc_runs)
let rppdval=unitvec(mc_runs)
let rppdval1=unitvec(mc_runs)
let rhighval=unitvec(mc_runs)
let rhighval1=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.I(Vsil)
let rsilval[run]= 1.5/\{$dt\}.I(Vsil)
let rsilval1[run]= 1.5/\{$dt\}.I(Vsil1)
let rppdval[run]= 1.5/\{$dt\}.I(Vppd)
let rppdval1[run]= 1.5/\{$dt\}.I(Vppd1)
let rhighval[run]= 1.5/\{$dt\}.I(Vrh)
let rhighval1[run]= 1.5/\{$dt\}.I(Vrh1)
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata mc_res_op.csv \{$scratch\}.rsilval \{$scratch\}.rsilval1 \{$scratch\}.rppdval \{$scratch\}.rppdval1 \{$scratch\}.rhighval \{$scratch\}.rhighval1
write mc_res_op.raw
echo
print \{$scratch\}.rsilval
print \{$scratch\}.rsilval1
print \{$scratch\}.rppdval
print \{$scratch\}.rppdval1
print \{$scratch\}.rhighval
print \{$scratch\}.rhighval1
.endc
"}
C {launcher.sym} -320 280 0 0 {name=h1
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
C {devices/gnd.sym} 440 320 0 0 {name=l6 lab=GND}
C {devices/ammeter.sym} 440 190 0 0 {name=Vsil1}
C {sg13g2_pr/rsil.sym} 440 270 0 0 {name=R4
w=0.5e-6
l=0.5e-5
model=rsil
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {devices/gnd.sym} 710 320 0 0 {name=l7 lab=GND}
C {devices/ammeter.sym} 710 190 0 0 {name=Vppd1}
C {sg13g2_pr/rppd.sym} 710 270 0 0 {name=R5
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {devices/gnd.sym} 990 320 0 0 {name=l8 lab=GND}
C {sg13g2_pr/rhigh.sym} 990 270 0 0 {name=R6
w=1.0e-6
l=1.0e-6
model=rhigh
spiceprefix=X
m=1
R=3.061e+3
Imax=0.11e-4
}
C {devices/ammeter.sym} 990 190 0 0 {name=Vrh1}
