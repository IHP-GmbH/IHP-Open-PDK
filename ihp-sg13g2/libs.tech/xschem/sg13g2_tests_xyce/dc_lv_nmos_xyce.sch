v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 520 -280 1320 120 {flags=graph
y1=-1.3e-11
y2=9.1e-05
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.2
divx=5
subdivx=1
node=i(vd)
color=4
dataset=-1
unitx=1
logx=0
logy=0
}
N -240 120 -240 180 {
lab=GND}
N -240 50 -240 60 {
lab=#net1}
N -110 80 -110 180 {
lab=GND}
N 20 80 20 180 {
lab=GND}
N -110 -20 -110 20 {
lab=#net2}
N 20 -20 20 20 {
lab=#net3}
N -110 50 -60 50 {
lab=GND}
N -60 50 -60 180 {
lab=GND}
N -110 -20 -80 -20 {
lab=#net2}
N -20 -20 20 -20 {
lab=#net3}
N -240 50 -150 50 {
lab=#net1}
N -110 180 -110 210 {
lab=GND}
N -60 180 20 180 {
lab=GND}
N -240 180 -110 180 {
lab=GND}
N -110 180 -60 180 {
lab=GND}
C {devices/vsource.sym} -240 90 0 0 {name=Vgs value=0.0}
C {devices/vsource.sym} 20 50 0 0 {name=Vds value=0}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 600 190 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/dc_lv_nmos.raw dc"
}
C {devices/ammeter.sym} -50 -20 1 0 {name=Vd}
C {simulator_commands_shown.sym} 60 -310 0 0 {name=Simulator
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.step  vgs 0.0 0.8 0.05
.dc vds 0 1.2 0.01
.print dc format=raw file=dc_lv_nmos.raw i(Vd)
"
"}
C {launcher.sym} 210 -110 0 0 {name=h1
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
C {simulator_commands_shown.sym} 0 -430 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerMOSlv.lib mos_tt
)"}
C {simulator_commands_shown.sym} -390 -430 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerMOSlv.lib mos_tt
"}
C {launcher.sym} -320 -100 0 0 {name=h2
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
C {simulator_commands_shown.sym} -400 -320 0 0 {name=Simulator1
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
op
dc Vds 0 1.2 0.01 Vgs 0.0 0.8 0.05
write dc_lv_nmos.raw
.endc
"}
C {sg13g2_pr/sg13_lv_nmos.sym} -130 50 2 1 {name=M1
l=0.45u
w=5.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {gnd.sym} -110 210 0 0 {name=l1 lab=GND}
