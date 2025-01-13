v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 1630 -1710 2430 -1310 {flags=graph
y1=-0.65

ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-0.02
x2=0.02
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0


y2=11
color=4
node=vin1}
B 2 1620 -1290 2420 -890 {flags=graph
y1=0

ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-0.02
x2=0.02
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0
color=10
node=vin2
y2=0.01}
N 1740 -510 1740 -490 {
lab=GND}
N 1740 -630 1740 -570 {
lab=Vin1}
N 1850 -500 1850 -490 {
lab=GND}
N 1850 -570 1850 -560 {
lab=#net1}
N 1850 -640 1850 -630 {
lab=Vin1}
N 2030 -510 2030 -490 {
lab=GND}
N 2030 -630 2030 -570 {
lab=Vin2}
N 2120 -500 2120 -490 {
lab=GND}
N 2120 -570 2120 -560 {
lab=#net2}
N 2120 -640 2120 -630 {
lab=Vin2}
C {devices/gnd.sym} 1740 -490 0 0 {name=l2 lab=GND}
C {devices/launcher.sym} 1690 -850 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_esd_nmos_cl.raw dc"
}
C {title-3.sym} 0 0 0 0 {name=l3 author="IHP PDK Authors" rev=1.0 lock=true}
C {lab_pin.sym} 1740 -630 1 0 {name=p1 sig_type=std_logic lab=Vin1}
C {devices/gnd.sym} 1850 -490 0 0 {name=l9 lab=GND}
C {devices/ammeter.sym} 1850 -600 0 0 {name=Vmda1}
C {lab_pin.sym} 1850 -640 1 0 {name=p8 sig_type=std_logic lab=Vin1}
C {sg13g2_pr/nmoscl_2.sym} 1850 -530 2 1 {name=D7
model=nmoscl_2
m=1
spiceprefix=X
}
C {isource.sym} 1740 -540 2 0 {name=I0 value=0}
C {devices/gnd.sym} 2030 -490 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 2030 -630 1 0 {name=p2 sig_type=std_logic lab=Vin2}
C {devices/gnd.sym} 2120 -490 0 0 {name=l4 lab=GND}
C {devices/ammeter.sym} 2120 -600 0 0 {name=Vmda2}
C {lab_pin.sym} 2120 -640 1 0 {name=p3 sig_type=std_logic lab=Vin2}
C {sg13g2_pr/nmoscl_2.sym} 2120 -530 2 1 {name=D1
model=nmoscl_4
m=1
spiceprefix=X
}
C {isource.sym} 2030 -540 2 0 {name=I1 value=0}
C {launcher.sym} 530 -1240 0 0 {name=h2
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
C {simulator_commands_shown.sym} 450 -1660 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerMOSlv.lib mos_tt
)"}
C {simulator_commands_shown.sym} 40 -1670 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerMOSlv.lib mos_tt
"}
C {launcher.sym} 120 -1240 0 0 {name=h3
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
C {simulator_commands_shown.sym} 40 -1560 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value=".param temp=27
.control
save all 
dc I0 -20m 20m 10u
*dc I1 -20m 20m 10u

echo ---------nmoscl_2---------
meas dc Vf FIND v(Vin1) AT=0.01
meas dc Vr FIND v(Vin1) AT=-0.01

echo ---------nmoscl_4---------
*meas dc Vf FIND v(Vin2) AT=0.01
*meas dc Vr FIND v(Vin2) AT=-0.01

write dc_esd_nmos_cl.raw
.endc
"}
C {simulator_commands_shown.sym} 450 -1500 0 0 {name=Simulator3
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.dc I0 -20m 20m 10u
.measure dc_cont nmoscl_2_VF FIND V(Vin1) AT=0.01
.measure dc_cont nmoscl_2_VR FIND V(Vin1) AT=-0.01

.measure dc_cont nmoscl_4_VF FIND V(Vin2) AT=0.01
.measure dc_cont nmoscl_4_VR FIND V(Vin2) AT=-0.01

.print dc format=raw file=dc_esd_nmos_cl.raw i(Vmda1)  i(Vmda2) v(Vin1) v(Vin2) 
"
"}
