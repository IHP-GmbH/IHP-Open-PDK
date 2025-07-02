v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 -290 -610 510 -210 {flags=graph

y2=0.041
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1
divx=5
subdivx=1

dataset=-1
unitx=1
logx=0
logy=0


y1=0
rainbow=0
color="7 8 4"
node="i(vrh)
i(vppd)
i(vsil)"}
N -290 120 -290 180 {
lab=GND}
N -290 -20 -290 60 {
lab=Vcc}
N -290 -20 -60 -20 {
lab=Vcc}
N -60 -20 -60 20 {
lab=Vcc}
N -60 80 -60 100 {
lab=#net1}
N -60 160 -60 180 {
lab=GND}
N 90 -20 90 20 {
lab=Vcc}
N 90 80 90 100 {
lab=#net2}
N 90 160 90 180 {
lab=GND}
N 270 -20 270 20 {
lab=Vcc}
N 270 80 270 100 {
lab=#net3}
N 270 160 270 180 {
lab=GND}
N -60 -20 90 -20 {
lab=Vcc}
N 90 -20 270 -20 {
lab=Vcc}
C {devices/gnd.sym} -60 180 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} -290 90 0 0 {name=Vres value=1.5}
C {devices/gnd.sym} -290 180 0 0 {name=l3 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -220 -170 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/dc_res_temp.raw dc"
}
C {devices/lab_pin.sym} -290 30 2 0 {name=p1 sig_type=std_logic lab=Vcc}
C {devices/ammeter.sym} -60 50 0 0 {name=Vsil}
C {devices/gnd.sym} 90 180 0 0 {name=l2 lab=GND}
C {devices/ammeter.sym} 90 50 0 0 {name=Vppd}
C {devices/gnd.sym} 270 180 0 0 {name=l4 lab=GND}
C {devices/ammeter.sym} 270 50 0 0 {name=Vrh}
C {simulator_commands_shown.sym} 1020 -300 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.dc Vres 0 1 1m
.print dc format=raw file=dc_res_temp.raw I(Vsil) I(Vppd) I(Vrh)
"}
C {launcher.sym} 1170 -100 0 0 {name=h2
descr=SimulateXyce
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,3,cmd) \{Xyce -plugin  $env(PDK_ROOT)/$env(PDK)/libs.tech/xyce/plugins/Xyce_Plugin_r3_cmc.so \\"$N\\"\}

# change the simulator to be used (Xyce)
set sim(spice,default) 3

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} 960 -420 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerRES.lib res_typ
)"}
C {simulator_commands_shown.sym} 570 -420 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerRES.lib res_typ
"}
C {launcher.sym} 640 -90 0 0 {name=h3
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
C {simulator_commands_shown.sym} 560 -310 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
dc Vres 0 1 1m
write dc_res_temp.raw
.endc
"}
C {sg13g2_pr/sub.sym} -170 180 0 0 {name=l6 lab=sub!}
C {sg13g2_pr/ptap1.sym} -170 150 0 0 {name=R1
model=ptap1
spiceprefix=X
w=10.78e-6
l=10.78e-6
}
C {sg13g2_pr/rsil.sym} -60 130 0 0 {name=R2
w=0.5e-6
l=0.5e-6
model=rsil
body=sub!
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rppd.sym} 90 130 0 0 {name=R3
w=0.5e-6
l=0.5e-6
model=rppd
body=sub!
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rhigh.sym} 270 130 0 0 {name=R4
w=0.5e-6
l=0.5e-6
model=rhigh
body=sub!
spiceprefix=X
b=0
m=1
}
C {devices/gnd.sym} -170 120 2 0 {name=l7 lab=GND}
