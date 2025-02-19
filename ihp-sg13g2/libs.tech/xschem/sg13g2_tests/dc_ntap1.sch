v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 270 -270 1070 130 {flags=graph

y2=0.54
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=3
divx=5
subdivx=1

dataset=-1
unitx=1
logx=0
logy=0


y1=0
rainbow=0
color=4
node=i(vr)}
N -100 80 -100 180 {
lab=#net1}
N -100 -60 -100 -20 {
lab=#net2}
N 80 -60 80 -20 {
lab=Vcc}
N -100 -60 -20 -60 {
lab=#net2}
N 40 -60 80 -60 {
lab=Vcc}
N 80 -60 130 -60 {
lab=Vcc}
N -100 80 80 80 {
lab=#net1}
N 80 40 80 80 {
lab=#net1}
N -100 40 -100 80 {
lab=#net1}
N -350 80 -100 80 {
lab=#net1}
N -350 -60 -350 -20 {
lab=#net2}
N -350 -60 -100 -60 {
lab=#net2}
N -220 180 -200 180 {
lab=GND}
N -140 180 -100 180 {
lab=#net1}
N -350 40 -350 80 {
lab=#net1}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -40 -200 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/dc_ntap1.raw dc"
}
C {simulator_commands_shown.sym} -230 -660 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerRES.lib res_typ
"}
C {launcher.sym} -160 -330 0 0 {name=h3
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
C {simulator_commands_shown.sym} -240 -550 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
op
print Vcc/I(Vr)
reset 
dc Vres 0 3 0.01 
write dc_ntap1.raw
.endc
"}
C {devices/gnd.sym} -220 180 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 80 10 0 0 {name=Vres value=1.5}
C {devices/lab_pin.sym} 130 -60 2 0 {name=p2 sig_type=std_logic lab=Vcc}
C {devices/ammeter.sym} 10 -60 1 0 {name=Vr}
C {devices/vsource.sym} -170 180 3 0 {name=Vres2 value=0}
C {sg13g2_pr/ntap1.sym} -100 10 0 0 {name=R4
model=ntap1
spiceprefix=X
w=1.0e-6
l=0.78e-6
}
C {sg13g2_pr/ntap1.sym} -350 10 0 0 {name=R5
model=ntap1
spiceprefix=X
w=10.0e-6
l=1.0e-6
}
