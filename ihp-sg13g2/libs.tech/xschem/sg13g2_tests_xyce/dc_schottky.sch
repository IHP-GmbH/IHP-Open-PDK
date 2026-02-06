v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 510 -550 1310 -150 {flags=graph
y1=-1.2
y2=11
ypos1=0
ypos2=2
divy=1
subdivy=4
unity=1
x1=-0.001
x2=0.001
divx=1
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0

hilight_wave=0
color=4
node=net1
linewidth_mult=1.0}
N 50 -210 50 -190 {
lab=GND}
N 50 -350 50 -270 {
lab=#net1}
N 50 -350 210 -350 {
lab=#net1}
N 210 -350 210 -290 {
lab=#net1}
N 210 -230 210 -190 {lab=GND}
N 220 -250 290 -250 {lab=sub!}
N 290 -250 290 -190 {lab=sub!}
N 70 -130 100 -130 {lab=GND}
N 70 -130 70 -120 {lab=GND}
N 160 -130 190 -130 {lab=sub!}
N 190 -130 190 -120 {lab=sub!}
C {devices/gnd.sym} 50 -190 0 0 {name=l2 lab=GND}
C {devices/launcher.sym} 590 -110 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_schottky.raw dc"
}
C {isource.sym} 50 -240 0 0 {name=I0 value=1m}
C {devices/gnd.sym} 210 -190 0 0 {name=l1 lab=GND}
C {sg13g2_pr/schottky_nbl1.sym} 210 -260 0 0 {name=D1
model=schottky_nbl1
Nx=1
Ny=1
spiceprefix=X
}
C {sg13g2_pr/sub.sym} 290 -190 0 0 {name=l3 lab=sub!}
C {vsource.sym} 130 -130 1 0 {name=V1 value=0 savecurrent=false}
C {devices/gnd.sym} 70 -120 0 0 {name=l4 lab=GND}
C {sg13g2_pr/sub.sym} 190 -120 0 0 {name=l6 lab=sub!}
C {devices/title.sym} 240 -50 0 0 {name=l8 author="Copyright 2023 IHP PDK Authors"}
C {simulator_commands_shown.sym} 440 -750 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.dc I0 -1m 1m 1u
.meas dc vbk_pos find v(net1) at=1u
.meas dc vbk_neg find v(net1) at=-1u
.print dc format=raw file=dc_schottky.raw V(net1) 
"
"}
C {launcher.sym} 520 -590 0 0 {name=h2
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
C {simulator_commands_shown.sym} 430 -850 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::MODELS_XYCE/cornerDIO.lib dio_tt
)"}
C {simulator_commands_shown.sym} 0 -870 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerDIO.lib dio_tt
"}
C {launcher.sym} 70 -540 0 0 {name=h3
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
C {simulator_commands_shown.sym} -10 -760 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
dc I0 -1m 1m 1u
echo Evaluating breakdown voltages:
meas dc vbk_pos find v(net1) at=10u
meas dc vbk_neg find v(net1) at=-10u
write dc_schottky.raw
.endc
"}
