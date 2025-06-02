v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 150 -510 950 -110 {flags=graph
y1=-5e-05
y2=1.4e-11
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=-1.2
x2=0
divx=5
subdivx=1
node=i(vd)
color=4
dataset=-1
unitx=1
logx=0
logy=0
sim_type=dc
autoload=1}
T {The Vds source is inverted in 
order to plot positive value of 
the current, which corresponds 
to real value of Ic} -290 -110 0 0 0.3 0.3 {}
T {Ctrl-Click to execute launcher} 630 -90 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} 630 30 0 0 0.3 0.3 {layer=11}
N -110 70 -110 90 {
lab=GND}
N -110 -0 -110 10 {
lab=#net1}
N 20 30 20 90 {
lab=GND}
N 150 30 150 90 {
lab=GND}
N 20 0 70 0 {
lab=GND}
N 70 0 70 90 {
lab=GND}
N 20 -110 50 -110 {
lab=#net2}
N 110 -110 150 -110 {
lab=#net3}
N -110 0 -20 0 {
lab=#net1}
N 20 -110 20 -30 {
lab=#net2}
N 150 -110 150 -30 {
lab=#net3}
C {devices/code_shown.sym} -200 160 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
"}
C {devices/code_shown.sym} 220 -10 0 0 {name=NGSPICE only_toplevel=true 
value="
.options savecurrents
.include dc_lv_pmos.save
.param temp=27
.control
save all
op
write dc_lv_pmos.raw
set appendwrite
dc Vds 0 -1.2 -0.01 Vgs -0.35 -1.1 -0.05
write dc_lv_pmos.raw
.endc
"}
C {devices/gnd.sym} 20 90 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -110 90 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -110 40 0 0 {name=Vgs value=-0.75}
C {devices/vsource.sym} 150 0 0 0 {name=Vds value=-1.5}
C {devices/gnd.sym} 150 90 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 70 90 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 2 1 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/ammeter.sym} 80 -110 1 0 {name=Vd}
C {sg13g2_pr/annotate_fet_params.sym} 10 -270 0 0 {name=annot1 ref=M1}
C {devices/launcher.sym} 690 -20 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {devices/launcher.sym} 690 10 0 0 {name=h2
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw dc
xschem setprop rect 2 0 fullxzoom
"
}
C {launcher.sym} 690 -50 0 0 {name=h3
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
