v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 360 -410 1160 -10 {flags=graph
y1=0.048
y2=0.062
ypos1=0
ypos2=2
divy=10
subdivy=4
unity=1
x1=7


subdivx=8


dataset=-1
unitx=1
logx=1
logy=0




divx=10



rainbow=0
hilight_wave=0




x2=10
color="7 8"
node="vout2
vout1"}
T {The testbench compares AC response of the same transistor alternating rfmode parameter. 
The sizes and the bias point are the same for each mosfet. The rfflag enables modeling of some
more parasitics parameters, what improves the model quality in RF band (above 1 GHz )} 370 20 0 0 0.3 0.3 {}
N 30 30 30 50 {
lab=GND}
N 30 -40 30 -30 {
lab=#net1}
N 160 -10 160 50 {
lab=GND}
N 290 -10 290 50 {
lab=GND}
N 160 -110 160 -70 {
lab=Vout1}
N 290 -110 290 -70 {
lab=#net2}
N 160 -40 210 -40 {
lab=GND}
N 210 -40 210 50 {
lab=GND}
N 160 -110 190 -110 {
lab=Vout1}
N 250 -110 290 -110 {
lab=#net2}
N 110 -40 120 -40 {
lab=#net3}
N 30 -40 50 -40 {
lab=#net1}
N 150 -110 160 -110 {
lab=Vout1}
N -300 40 -300 60 {
lab=GND}
N -300 -30 -300 -20 {
lab=#net4}
N -170 0 -170 60 {
lab=GND}
N -40 0 -40 60 {
lab=GND}
N -170 -100 -170 -60 {
lab=Vout2}
N -40 -100 -40 -60 {
lab=#net5}
N -170 -30 -120 -30 {
lab=GND}
N -120 -30 -120 60 {
lab=GND}
N -170 -100 -140 -100 {
lab=Vout2}
N -80 -100 -40 -100 {
lab=#net5}
N -220 -30 -210 -30 {
lab=#net6}
N -300 -30 -280 -30 {
lab=#net4}
N -180 -100 -170 -100 {
lab=Vout2}
C {devices/gnd.sym} 160 50 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 30 50 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 30 0 0 0 {name=Vgs value="dc 0.45 ac 1 "}
C {devices/vsource.sym} 290 -40 0 0 {name=Vds value=1.2}
C {devices/gnd.sym} 290 50 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 210 50 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 420 130 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/ac_lv_nmosrf.raw ac"}
C {devices/lab_pin.sym} 150 -110 1 0 {name=p1 sig_type=std_logic lab=Vout1}
C {devices/gnd.sym} -170 60 0 0 {name=l6 lab=GND}
C {devices/gnd.sym} -300 60 0 0 {name=l7 lab=GND}
C {devices/vsource.sym} -300 10 0 0 {name=Vgs1 value="dc 0.45 ac 1 "}
C {devices/vsource.sym} -40 -30 0 0 {name=Vds2 value=1.2}
C {devices/gnd.sym} -40 60 0 0 {name=l8 lab=GND}
C {devices/gnd.sym} -120 60 0 0 {name=l9 lab=GND}
C {devices/lab_pin.sym} -180 -100 1 0 {name=p2 sig_type=std_logic lab=Vout2}
C {sg13g2_pr/sg13_lv_rf_nmos.sym} -190 -30 2 1 {name=M1
l=0.35u
w=1.0u
ng=1
m=1
rfmode=0
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_rf_nmos.sym} 140 -40 2 1 {name=M2
l=0.35u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_lv_nmos
spiceprefix=X
}
C {simulator_commands_shown.sym} -720 -500 0 0 {name=Simulator
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.ac dec 1001 10meg 10000meg
.print ac format=raw file=ac_lv_nmosrf.raw V(Vout1) V(Vout2)
"
"}
C {launcher.sym} -640 -340 0 0 {name=h1
descr=SimulateXyce
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,3,cmd) \{Xyce -plugin $env(PDK_ROOT)/$env(PDK)/libs.tech/xyce/plugins/Xyce_Plugin_PSP103_VA.so \\"$N\\"\}

# change the simulator to be used (Xyce)
set sim(spice,default) 3

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} -710 -620 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerMOSlv.lib mos_tt
)"}
C {simulator_commands_shown.sym} -720 -210 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerMOSlv.lib mos_tt
"}
C {launcher.sym} -640 110 0 0 {name=h2
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
C {simulator_commands_shown.sym} -710 -110 0 0 {name=Simulator1
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all
ac dec 1001 10meg 10000meg 
let vd1 = abs(Vout1)
let vd2 = abs(Vout2)
meas ac Vout_1_5GHz find vd1 at=5000meg
meas ac Vout_2_5GHz find vd2 at=5000meg
write ac_lv_nmosrf.raw
.endc
"}
C {res.sym} -250 -30 1 0 {name=R1
value=400
footprint=1206
device=resistor
m=1}
C {res.sym} -110 -100 1 0 {name=R2
value=400
footprint=1206
device=resistor
m=1}
C {res.sym} 80 -40 1 0 {name=R3
value=400
footprint=1206
device=resistor
m=1}
C {res.sym} 220 -110 1 0 {name=R4
value=400
footprint=1206
device=resistor
m=1}
