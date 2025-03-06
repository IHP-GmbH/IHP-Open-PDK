v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 -510 -700 290 -300 {flags=graph
y1=-3.1e-06
y2=2.3e-06
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-12
x2=1
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0
color="7 8"
node="i(Vmdp)
i(Vmda)"}
N -440 -40 -440 -20 {
lab=GND}
N -440 -160 -440 -100 {
lab=#net1}
N -440 -160 -290 -160 {
lab=#net1}
N -290 -20 -290 -10 {
lab=GND}
N -110 -20 -110 -10 {
lab=GND}
N -290 -90 -290 -80 {
lab=#net2}
N -290 -160 -290 -150 {
lab=#net1}
N -110 -90 -110 -80 {
lab=#net3}
N -110 -160 -110 -150 {
lab=#net1}
N -290 -160 -110 -160 {
lab=#net1}
C {devices/gnd.sym} -440 -20 0 0 {name=l2 lab=GND}
C {devices/title.sym} -360 130 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -470 -260 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_diode_op.raw dc"
}
C {devices/gnd.sym} -110 -10 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -290 -10 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} -440 -70 0 0 {name=V1 value=0.7}
C {devices/ammeter.sym} -290 -120 0 0 {name=Vmda}
C {devices/ammeter.sym} -110 -120 0 0 {name=Vmdp}
C {sg13g2_pr/dpantenna.sym} -290 -50 2 0 {name=D2
model=dpantenna
l=0.78u
w=0.78u
spiceprefix=X
}
C {sg13g2_pr/dantenna.sym} -110 -50 2 0 {name=D1
model=dantenna
l=0.78u
w=0.78u
spiceprefix=X
}
C {simulator_commands_shown.sym} 870 -530 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.dc v1 -12 1 1m
.print dc format=raw file=dc_diode_op.raw I(Vmdp) I(Vmda)
"
"}
C {launcher.sym} 1020 -330 0 0 {name=h2
descr=SimulateXyce
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,3,cmd) \{Xyce \\"$N\\"\}

# change the simulator to be used (Xyce)
set sim(spice,default) 3

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} 810 -650 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.include $::SG13G2_MODELS_XYCE/diodes.lib
)"}
C {simulator_commands_shown.sym} 420 -650 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.include diodes.lib
"}
C {launcher.sym} 490 -320 0 0 {name=h3
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
C {simulator_commands_shown.sym} 410 -540 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
op
print I(Vmda) I(Vmdp) 
reset 
dc V1 -12 1 1m
write dc_diode_op.raw
wrdata dc_diode.csv I(Vmda) I(Vmdp)
.endc
"}
