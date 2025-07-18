v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 -350 -250 450 150 {flags=graph

y2=0.0024
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.5
divx=5
subdivx=1

dataset=-1
unitx=1
logx=0
logy=0
color=4
node=i(Vc)
y1=-5.5e-05
rainbow=0}
T {Nx - number of emitters} 660 0 0 0 0.2 0.2 {}
T {Ctrl-Click to execute launcher} -680 50 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} -680 200 0 0 0.3 0.3 {layer=11}
N 570 -50 570 -30 {
lab=GND}
N 570 -120 570 -110 {
lab=#net1}
N 700 -90 700 -30 {
lab=GND}
N 830 -90 830 -30 {
lab=GND}
N 700 -190 700 -150 {
lab=#net2}
N 830 -190 830 -150 {
lab=#net3}
N 700 -120 750 -120 {
lab=GND}
N 750 -120 750 -30 {
lab=GND}
N 700 -190 730 -190 {
lab=#net2}
N 790 -190 830 -190 {
lab=#net3}
N 570 -120 660 -120 {
lab=#net1}
C {devices/gnd.sym} 700 -30 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 570 -30 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 830 -120 0 0 {name=Vce value=0.0}
C {devices/gnd.sym} 830 -30 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 750 -30 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} 570 -80 2 0 {name=I0 value=1u}
C {devices/ammeter.sym} 760 -190 1 0 {name=Vc}
C {sg13g2_pr/npn13G2.sym} 680 -120 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1
le=0.9e-6}
C {simulator_commands_shown.sym} 100 -570 0 0 {name=Simulator
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.step I0 0 5u 0.1u
.dc Vce 0 1.5 0.01
.print dc format=raw file=dc_hbt_13g2.raw I(Vc)
"
"}
C {launcher.sym} -620 120 0 0 {name=h1
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
C {simulator_commands_shown.sym} 40 -680 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerHBT.lib hbt_typ
)"}
C {simulator_commands_shown.sym} -350 -690 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerHBT.lib hbt_typ
"}
C {simulator_commands_shown.sym} -360 -580 0 0 {name=Simulator1
simulator=ngspice
only_toplevel=false 
value="
.options savecurrents
.include dc_hbt_13g2.save
.param temp=27
.control
save all 
op
write dc_hbt_13g2.raw
set appendwrite
dc Vce 0 1.5 0.01 I0 0 5u 0.1u
write dc_hbt_13g2.raw
.endc
"}
C {devices/launcher.sym} -620 150 0 0 {name=h3
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {devices/launcher.sym} -620 180 0 0 {name=h4
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw dc
xschem setprop rect 2 0 fullxzoom
"
}
C {launcher.sym} -620 90 0 0 {name=h6
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

# Create FET and BIP .save file
mkdir -p $netlist_dir
write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save

# run netlist and simulation
xschem netlist
simulate
"}
C {sg13g2_pr/annotate_bip_params.sym} 550 -300 0 0 {name=annot1 ref=Q1}
