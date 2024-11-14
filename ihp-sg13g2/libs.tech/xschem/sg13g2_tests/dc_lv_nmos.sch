v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 460 -320 1260 80 {flags=graph
y1=-1.2e-12
y2=0.00011
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
N -300 80 -300 140 {
lab=GND}
N -300 10 -300 20 {
lab=#net1}
N -170 40 -170 140 {
lab=GND}
N -40 40 -40 140 {
lab=GND}
N -170 -60 -170 -20 {
lab=#net2}
N -40 -60 -40 -20 {
lab=#net3}
N -170 10 -120 10 {
lab=GND}
N -120 10 -120 140 {
lab=GND}
N -170 -60 -140 -60 {
lab=#net2}
N -80 -60 -40 -60 {
lab=#net3}
N -300 10 -210 10 {
lab=#net1}
N -170 140 -170 170 {
lab=GND}
N -120 140 -40 140 {
lab=GND}
N -300 140 -170 140 {
lab=GND}
N -170 140 -120 140 {
lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/vsource.sym} -300 50 0 0 {name=Vgs value=0.0}
C {devices/vsource.sym} -40 10 0 0 {name=Vds value=0}
C {devices/launcher.sym} 540 150 0 0 {name=h1
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/dc_lv_nmos.raw dc"
}
C {devices/ammeter.sym} -110 -60 1 0 {name=Vd}
C {simulator_commands_shown.sym} 0 -350 0 0 {name=Simulator1
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
C {launcher.sym} 150 -150 0 0 {name=h2
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
C {simulator_commands_shown.sym} -60 -470 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerMOSlv.lib mos_tt
)"}
C {simulator_commands_shown.sym} -450 -470 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerMOSlv.lib mos_tt
"}
C {launcher.sym} -380 -140 0 0 {name=h3
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
C {simulator_commands_shown.sym} -460 -360 0 0 {name=Simulator2
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
C {sg13g2_pr/sg13_lv_nmos.sym} -190 10 2 1 {name=M2
l=0.13u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {gnd.sym} -170 170 0 0 {name=l6 lab=GND}
