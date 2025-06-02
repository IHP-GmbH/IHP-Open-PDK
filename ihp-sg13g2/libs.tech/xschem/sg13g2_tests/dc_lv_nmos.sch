v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 510 -650 1070 -350 {flags=graph
y1=-4.6e-12
y2=0.00025
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
sim_type=dc
autoload=1}
T {Ctrl-Click to execute launcher} 650 -330 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} 650 -210 0 0 0.3 0.3 {layer=11}
N 250 -160 250 -140 {
lab=GND}
N 250 -250 250 -220 {
lab=G}
N 380 -220 380 -160 {
lab=GND}
N 510 -220 510 -160 {
lab=GND}
N 380 -340 380 -280 {
lab=#net1}
N 510 -340 510 -280 {
lab=D}
N 380 -250 450 -250 {
lab=GND}
N 450 -250 450 -160 {
lab=GND}
N 380 -340 410 -340 {
lab=#net1}
N 470 -340 510 -340 {
lab=D}
N 250 -250 340 -250 {
lab=G}
C {devices/code_shown.sym} 0 -100 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value=".lib cornerMOSlv.lib mos_tt
"}
C {devices/code_shown.sym} 100 -610 0 0 {name=NGSPICE only_toplevel=true 
value="
.include dc_lv_nmos.save
.param temp=27
.control
save all 
op
write dc_lv_nmos.raw
set appendwrite
dc Vds 0 1.2 0.01 Vgs 0.3 1.0 0.1
write dc_lv_nmos.raw
.endc
"}
C {devices/gnd.sym} 380 -160 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 250 -140 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 250 -190 0 0 {name=Vgs value=1.2}
C {devices/vsource.sym} 510 -250 0 0 {name=Vds value=1.5}
C {devices/gnd.sym} 510 -160 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 450 -160 0 0 {name=l4 lab=GND}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/ammeter.sym} 440 -340 1 0 {name=Vd}
C {sg13g2_pr/annotate_fet_params.sym} 240 -400 0 0 {name=annot1 ref=M1}
C {lab_pin.sym} 250 -250 0 0 {name=p1 sig_type=std_logic lab=G}
C {lab_pin.sym} 510 -340 0 1 {name=p2 sig_type=std_logic lab=D}
C {devices/launcher.sym} 710 -260 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {sg13g2_pr/sg13_lv_nmos.sym} 360 -250 0 0 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {devices/launcher.sym} 710 -230 0 0 {name=h2
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw dc
xschem setprop rect 2 0 fullxzoom
"
}
C {launcher.sym} 710 -290 0 0 {name=h3
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
