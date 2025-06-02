v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 -280 -540 520 -140 {flags=graph

y2=0.00076
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
color="4 7"
node="i(vc)
i(vc1)"
y1=-3.3e-05
rainbow=0}
T {Nx - number of emitters} -210 110 0 0 0.2 0.2 {}
T {Ctrl-Click to execute launcher} 520 -100 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} 520 20 0 0 0.3 0.3 {layer=11}
N -300 60 -300 80 {
lab=GND}
N -300 -10 -300 0 {
lab=#net1}
N -170 20 -170 80 {
lab=GND}
N 40 20 40 80 {
lab=GND}
N -170 -80 -170 -40 {
lab=#net2}
N 40 -80 40 -40 {
lab=#net3}
N -170 -80 -140 -80 {
lab=#net2}
N -80 -80 40 -80 {
lab=#net3}
N -300 -10 -210 -10 {
lab=#net1}
N -140 40 -140 80 {
lab=GND}
N -120 -10 -80 -10 {
lab=tmp}
N -80 70 -80 80 {
lab=GND}
N -80 -10 -80 10 {
lab=tmp}
N -80 -20 -80 -10 {
lab=tmp}
N 400 70 400 90 {
lab=GND}
N 400 0 400 10 {
lab=#net4}
N 290 30 290 80 {
lab=GND}
N 250 0 250 80 {
lab=GND}
N 250 0 290 0 {
lab=GND}
N 290 -80 290 -30 {
lab=#net5}
N 210 -80 290 -80 {
lab=#net5}
N 40 -80 150 -80 {
lab=#net3}
N 330 -0 400 -0 {
lab=#net4}
C {devices/gnd.sym} -170 80 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -300 80 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 40 -10 0 0 {name=Vce value=1.5}
C {devices/gnd.sym} 40 80 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -140 80 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} -300 30 2 0 {name=I0 value=1u}
C {devices/ammeter.sym} -110 -80 1 0 {name=Vc}
C {res.sym} -80 40 0 0 {name=R1
value=10G
footprint=1206
device=resistor
m=1}
C {devices/gnd.sym} -80 80 0 0 {name=l6 lab=GND}
C {lab_wire.sym} -80 -20 0 0 {name=p1 sig_type=std_logic lab=tmp}
C {devices/gnd.sym} 400 90 0 0 {name=l7 lab=GND}
C {devices/isource.sym} 400 40 2 0 {name=I1 value=1u}
C {devices/gnd.sym} 290 80 0 0 {name=l8 lab=GND}
C {devices/gnd.sym} 250 80 0 0 {name=l9 lab=GND}
C {devices/ammeter.sym} 180 -80 3 0 {name=Vc1}
C {sg13g2_pr/npn13G2l.sym} 310 0 0 1 {name=Q1
model=npn13G2l
spiceprefix=X
Nx=1
El=2.5
}
C {sg13g2_pr/npn13G2l_5t.sym} -190 -10 0 0 {name=Q2
model=npn13G2l_5t
spiceprefix=X
Nx=1 
El=2.5
}
C {devices/code_shown.sym} -630 -410 0 0 {name=NGSPICE only_toplevel=true 
value="
.options savecurrents
.include dc_hbt_13g2l_5t.save
.param temp=27
.control
save all 
op
write dc_hbt_13g2l_5t.raw
set appendwrite
dc Vce 0 1.5 0.01
write dc_hbt_13g2l_5t.raw
.endc
"}
C {devices/code_shown.sym} -640 -520 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerHBT.lib hbt_typ
"}
C {sg13g2_pr/annotate_bip_params.sym} 450 -10 0 0 {name=annot1 ref=Q1}
C {sg13g2_pr/annotate_bip_params.sym} -420 -90 0 0 {name=annot2 ref=Q2}
C {devices/launcher.sym} 580 -30 0 0 {name=h3
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {devices/launcher.sym} 580 0 0 0 {name=h4
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw dc
xschem setprop rect 2 0 fullxzoom
"
}
C {launcher.sym} 580 -60 0 0 {name=h5
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
