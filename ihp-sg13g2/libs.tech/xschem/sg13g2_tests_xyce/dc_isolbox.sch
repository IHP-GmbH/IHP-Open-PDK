v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 470 -540 1270 -140 {flags=graph
y1=-25
y2=16
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

color="4 6"
node="nwell_net

isosub_net"
hilight_wave=0}
N 40 -140 40 -120 {
lab=GND}
N 200 -140 200 -120 {
lab=GND}
N 40 -280 40 -200 {
lab=isosub_net}
N 40 -280 200 -280 {
lab=isosub_net}
N 200 -280 200 -260 {
lab=isosub_net}
N 200 -200 280 -200 {
lab=nwell_net}
N 200 -280 280 -280 {
lab=isosub_net}
N 280 -200 280 -180 {
lab=nwell_net}
C {devices/gnd.sym} 40 -120 0 0 {name=l2 lab=GND}
C {devices/title.sym} 190 -50 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 540 -100 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_isolbox.raw dc"
}
C {isource.sym} 40 -170 2 0 {name=I0 value=1m}
C {devices/gnd.sym} 200 -120 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 280 -280 2 0 {name=p1 sig_type=std_logic lab=isosub_net}
C {lab_pin.sym} 280 -200 2 0 {name=p2 sig_type=std_logic lab=nwell_net}
C {sg13g2_pr/isolbox.sym} 200 -200 0 0 {name=D1
model=isolbox
l=3.0u
w=3.0u
spiceprefix=X
}
C {noconn.sym} 280 -180 3 0 {name=l3}
C {simulator_commands_shown.sym} 430 -730 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.dc I0 -1m 1m 1u
.meas dc vbk_pos find v(isosub_net) at=1u
.meas dc vbk_neg find v(isosub_net) at=-1u
.print dc format=raw file=dc_isolbox.raw V(nwell_net) V(isosub_net)
"
"}
C {launcher.sym} 510 -570 0 0 {name=h2
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
C {simulator_commands_shown.sym} 420 -830 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.include $::MODELS_XYCE/diodes.lib
)"}
C {simulator_commands_shown.sym} 0 -710 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.include diodes.lib
"}
C {launcher.sym} 70 -380 0 0 {name=h3
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
C {simulator_commands_shown.sym} -10 -600 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
dc I0 -1m 1m 1u
echo Evaluating breakdown voltages:
meas dc vbk_pos find v(isosub_net) at=1u
meas dc vbk_neg find v(isosub_net) at=-1u
write dc_isolbox.raw
wrdata isolbox.csv nwell_net isosub_net
.endc
"}
