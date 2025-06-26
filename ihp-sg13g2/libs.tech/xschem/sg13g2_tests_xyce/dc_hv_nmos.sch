v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 150 -490 950 -90 {flags=graph
y1=0
y2=0.00012
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=3
divx=5
subdivx=1
node=i(vd)
color=4
dataset=-1
unitx=1
logx=0
logy=0
}
N -110 70 -110 90 {
lab=GND}
N -110 -0 -110 10 {
lab=#net1}
N 20 30 20 90 {
lab=GND}
N 150 30 150 90 {
lab=GND}
N 20 -70 20 -30 {
lab=#net2}
N 150 -70 150 -30 {
lab=#net3}
N 20 0 70 0 {
lab=GND}
N 70 0 70 90 {
lab=GND}
N 20 -70 50 -70 {
lab=#net2}
N 110 -70 150 -70 {
lab=#net3}
N -110 0 -20 0 {
lab=#net1}
C {devices/gnd.sym} 20 90 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -110 90 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -110 40 0 0 {name=Vgs value=0}
C {devices/vsource.sym} 150 0 0 0 {name=Vds value=0}
C {devices/gnd.sym} 150 90 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 70 90 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -200 -160 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/dc_hv_nmos.raw dc"
}
C {devices/ammeter.sym} 80 -70 1 0 {name=Vd}
C {sg13g2_pr/sg13_hv_nmos.sym} 0 0 0 0 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {simulator_commands_shown.sym} -350 -610 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.step  vgs 0.3 1.5 0.05
.dc vds 0 3.0 0.01
.print dc format=raw file=dc_hv_nmos.raw i(Vd)
"
"}
C {launcher.sym} -190 -400 0 0 {name=h2
descr=SimulateXyce
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults

########################## Xyce #####################################
set plugin_dir "$env(PDK_ROOT)/$env(PDK)/libs.tech/xyce/plugins/"
set plugin_file_name "sg13g2-plugins.txt"
set plugin_file $plugin_dir$plugin_file_name
set fh [open $plugin_file r]
set plugin_list \{\}
while \{[gets $fh line] >= 0\} \{
   set line [string trim $line]
   lappend plugin_list $plugin_dir$line
\}
close $fh
set plugin_args [join $plugin_list ","]
set sim(spice,3,cmd) [list Xyce -plugin $plugin_args "\\\\$N"]
# change the simulator to be used (Xyce)
set sim(spice,default) 3
########################## Xyce #####################################

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} -350 -730 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerMOShv.lib mos_tt
)"}
C {simulator_commands_shown.sym} -800 -730 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerMOShv.lib mos_tt
"}
C {launcher.sym} -720 -400 0 0 {name=h3
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
C {simulator_commands_shown.sym} -800 -620 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
dc Vds 0 3.0 0.01 Vgs 0.3 1.5 0.05
write dc_hv_nmos.raw
.endc
"}
