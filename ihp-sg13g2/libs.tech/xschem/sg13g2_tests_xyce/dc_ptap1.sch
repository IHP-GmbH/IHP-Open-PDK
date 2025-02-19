v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 100 -460 900 -60 {flags=graph

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
N -180 80 -180 100 {
lab=sub!}
N -180 -60 -180 -20 {
lab=#net1}
N 0 -60 0 -20 {
lab=Vcc}
N -180 -60 -100 -60 {
lab=#net1}
N -40 -60 0 -60 {
lab=Vcc}
N 0 -60 50 -60 {
lab=Vcc}
N -180 80 0 80 {
lab=sub!}
N 0 40 0 80 {
lab=sub!}
N -180 40 -180 80 {
lab=sub!}
N -430 40 -430 80 {
lab=sub!}
N -430 80 -180 80 {
lab=sub!}
N -430 -60 -430 -20 {
lab=#net1}
N -430 -60 -180 -60 {
lab=#net1}
N -300 180 -280 180 {
lab=GND}
N -220 180 -200 180 {
lab=sub!}
C {devices/gnd.sym} -300 180 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 0 10 0 0 {name=Vres value=1.5}
C {devices/title.sym} -100 240 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -120 -200 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/dc_ptap1.raw dc"
}
C {devices/lab_pin.sym} 50 -60 2 0 {name=p1 sig_type=std_logic lab=Vcc}
C {devices/ammeter.sym} -70 -60 1 0 {name=Vr}
C {simulator_commands_shown.sym} 80 -690 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.dc Vres 0 3 10m
.print dc format=raw file=dc_ptap1.raw I(Vr) 
"}
C {launcher.sym} 230 -490 0 0 {name=h2
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
C {simulator_commands_shown.sym} 20 -810 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerRES.lib res_typ
)"}
C {simulator_commands_shown.sym} -370 -810 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerRES.lib res_typ
"}
C {launcher.sym} -300 -480 0 0 {name=h3
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
C {simulator_commands_shown.sym} -380 -700 0 0 {name=Simulator2
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
write dc_ptap1.raw
.endc
"}
C {sg13g2_pr/ptap1.sym} -430 10 0 0 {name=R5
model=ptap1
spiceprefix=X
w=10.0e-6
l=1.0e-6
}
C {sg13g2_pr/ptap1.sym} -180 10 0 0 {name=R1
model=ptap1
spiceprefix=X
w=1.0e-6
l=0.78e-6
}
C {sg13g2_pr/sub.sym} -180 100 0 0 {name=l2 lab=sub!}
C {sg13g2_pr/sub.sym} -200 180 0 0 {name=l3 lab=sub!}
C {devices/vsource.sym} -250 180 3 0 {name=Vres1 value=0}
