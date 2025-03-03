v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 -510 -670 290 -270 {flags=graph
y1=0.6
y2=0.88
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-40
x2=125
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0
node="vd
vdp"
color="8 7"
dataset=-1
unitx=1
logx=0
logy=0
}
N -500 40 -500 60 {
lab=GND}
N -500 -80 -500 -20 {
lab=Vd}
N -500 -80 -220 -80 {
lab=Vd}
N -220 -80 -220 -40 {
lab=Vd}
N -220 20 -220 60 {
lab=GND}
N -220 -80 -200 -80 {
lab=Vd}
N -70 40 -70 60 {
lab=GND}
N -70 -80 -70 -20 {
lab=Vdp}
N -70 -80 210 -80 {
lab=Vdp}
N 210 -80 210 -40 {
lab=Vdp}
N 210 20 210 60 {
lab=GND}
N 210 -80 230 -80 {
lab=Vdp}
C {devices/gnd.sym} -220 60 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -500 60 0 0 {name=l2 lab=GND}
C {devices/lab_pin.sym} -200 -80 0 1 {name=p1 sig_type=std_logic lab=Vd}
C {sg13g2_pr/dantenna.sym} -220 -10 2 0 {name=XD1
model=dantenna
l=780n
w=780n
}
C {devices/isource.sym} -500 10 2 0 {name=I0 value=200n}
C {devices/title.sym} -360 130 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -450 -220 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_diode_temp.raw dc"
}
C {devices/gnd.sym} 210 60 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -70 60 0 0 {name=l4 lab=GND}
C {devices/lab_pin.sym} 230 -80 0 1 {name=p2 sig_type=std_logic lab=Vdp}
C {devices/isource.sym} -70 10 2 0 {name=I1 value=200n}
C {sg13g2_pr/dpantenna.sym} 210 -10 2 0 {name=XD2
model=dpantenna
l=780n
w=780n
}
C {simulator_commands_shown.sym} 880 -510 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.dc temp -40 125 1
.print dc format=raw file=dc_diode_temp.raw V(Vd) V(Vdp)
"}
C {launcher.sym} 1030 -310 0 0 {name=h2
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
C {simulator_commands_shown.sym} 820 -630 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.include $::SG13G2_MODELS_XYCE/diodes.lib
)"}
C {simulator_commands_shown.sym} 430 -630 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.include diodes.lib
"}
C {launcher.sym} 500 -300 0 0 {name=h3
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
C {simulator_commands_shown.sym} 420 -520 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
dc temp -40 125 1
write dc_diode_temp.raw
wrdata dc_diode_temp.csv Vd Vdp
.endc
"}
