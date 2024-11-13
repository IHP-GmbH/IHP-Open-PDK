v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 -290 -610 510 -210 {flags=graph

y2=0.00084
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=0
divx=5
subdivx=1

dataset=-1
unitx=1
logx=0
logy=0


y1=8.3e-08
rainbow=0
color=4
node=i(vrh)}
N 0 100 0 120 {
lab=GND}
N 0 0 0 40 {
lab=out}
N 0 0 40 0 {
lab=out}
N -40 0 0 0 {
lab=out}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -220 -170 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/dc_res_temp.raw dc"
}
C {simulator_commands_shown.sym} 540 -550 0 0 {name=Simulator
simulator=Xyce
only_toplevel=false 
value="

.AC lin 10000 1k 1meg
P1 in 0 port=1 
P2 out 0 port=2 z0=50 

.LIN format=touchstone2 Dataformat=ri file=file.s2p 
"
"}
C {launcher.sym} 610 -320 0 0 {name=h1
descr=Simulate with Xyce
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,3,cmd) \{Xyce  \\"$N\\"\}

# change the simulator to be used (Xyce)
set sim(spice,default) 3

# run netlist and simulation
xschem netlist
simulate
"}
C {capa.sym} 0 70 0 0 {name=C1
m=1
value=10n
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} -100 0 0 0 {name=p1 sig_type=std_logic lab=in}
C {lab_pin.sym} 40 0 2 0 {name=p2 sig_type=std_logic lab=out}
C {ind.sym} -70 0 1 0 {name=L1
m=1
value=10u
footprint=1206
device=inductor}
C {gnd.sym} 0 120 0 0 {name=l4 lab=GND}
