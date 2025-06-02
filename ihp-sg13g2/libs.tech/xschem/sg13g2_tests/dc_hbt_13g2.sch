v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 -60 -530 740 -130 {flags=graph

y2=0.0027
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
node=i(vc)
y1=-1.9e-05
rainbow=0}
T {Nx - number of emitters} -210 110 0 0 0.2 0.2 {}
T {Ctrl-Click to execute launcher} 350 -100 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} 350 20 0 0 0.3 0.3 {layer=11}
N -300 60 -300 80 {
lab=GND}
N -300 -10 -300 0 {
lab=#net1}
N -170 20 -170 80 {
lab=GND}
N -40 20 -40 80 {
lab=GND}
N -170 -80 -170 -40 {
lab=#net2}
N -40 -80 -40 -40 {
lab=#net3}
N -170 -10 -120 -10 {
lab=GND}
N -120 -10 -120 80 {
lab=GND}
N -170 -80 -140 -80 {
lab=#net2}
N -80 -80 -40 -80 {
lab=#net3}
N -300 -10 -210 -10 {
lab=#net1}
C {devices/code_shown.sym} -310 180 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerHBT.lib hbt_typ
"}
C {devices/code_shown.sym} 20 0 0 0 {name=NGSPICE only_toplevel=true 
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
C {devices/gnd.sym} -170 80 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -300 80 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -40 -10 0 0 {name=Vce value=1.5}
C {devices/gnd.sym} -40 80 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -120 80 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} -300 30 2 0 {name=I0 value=1u}
C {devices/ammeter.sym} -110 -80 1 0 {name=Vc}
C {sg13g2_pr/npn13G2.sym} -190 -10 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1
}
C {sg13g2_pr/annotate_bip_params.sym} -300 -190 0 0 {name=annot1 ref=Q1}
C {devices/launcher.sym} 410 -30 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {devices/launcher.sym} 410 0 0 0 {name=h2
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw dc
xschem setprop rect 2 0 fullxzoom
"
}
C {launcher.sym} 410 -60 0 0 {name=h3
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
