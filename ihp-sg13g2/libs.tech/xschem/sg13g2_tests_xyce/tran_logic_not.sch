v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 620 -580 1420 -180 {flags=graph
y1=-0.19
y2=1.5
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=2e-08
divx=5
subdivx=1


dataset=-1
unitx=1
logx=0
logy=0
color="4 5"
node="out
in"}
N 340 140 340 160 {
lab=GND}
N 620 100 620 160 {
lab=GND}
N 880 100 880 160 {
lab=GND}
N 670 70 670 160 {
lab=GND}
N 620 70 670 70 {
lab=GND}
N 620 -30 670 -30 {
lab=#net1}
N 620 20 620 40 {
lab=out}
N 620 -130 620 -60 {
lab=#net1}
N 670 -130 880 -130 {
lab=#net1}
N 880 -130 880 40 {
lab=#net1}
N 670 -130 670 -30 {
lab=#net1}
N 550 70 580 70 {
lab=in}
N 550 20 550 70 {
lab=in}
N 550 -30 580 -30 {
lab=in}
N 340 20 340 80 {
lab=in}
N 620 20 750 20 {
lab=out}
N 320 20 340 20 {
lab=in}
N 340 20 550 20 {
lab=in}
N 550 -30 550 20 {
lab=in}
N 620 0 620 20 {
lab=out}
N 620 -130 670 -130 {
lab=#net1}
C {devices/gnd.sym} 620 160 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 340 160 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 340 110 0 0 {name=Vin value="pulse(0.0 1.2 0.0 100p 100p 2n 4n)"}
C {devices/vsource.sym} 880 70 0 0 {name=Vdd value=1.2}
C {devices/gnd.sym} 880 160 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 670 160 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 1010 -120 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/tran_logic_not.raw tran"
}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 70 2 1 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 -30 0 0 {name=M2
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} 320 20 0 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 750 20 2 0 {name=p2 sig_type=std_logic lab=out}
C {simulator_commands_shown.sym} -260 -520 0 0 {name=Simulator
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.tran 50p 20n
.measure tran_cont tdelaytp TRIG  v(in)=0.9 Fall=1 TARG v(out)=0.9 rise=1
.print tran format=raw file=tran_logic_not.raw V(out) V(in)
"
"}
C {launcher.sym} -180 -360 0 0 {name=h1
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
C {simulator_commands_shown.sym} -250 -640 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerMOSlv.lib mos_tt
)"}
C {simulator_commands_shown.sym} -260 -230 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerMOSlv.lib mos_tt
"}
C {launcher.sym} -180 30 0 0 {name=h2
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
C {simulator_commands_shown.sym} -250 -130 0 0 {name=Simulator1
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
tran 50p 20n
meas tran tdelay TRIG v(in) VAl=0.9 FALl=1 TARG v(out) VAl=0.9 RISE=1
write tran_logic_not.raw
.endc
"}
