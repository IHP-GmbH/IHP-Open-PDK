v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 2260 540 2940 970 {flags=graph,unlocked
y1=1.4821969e-321
y2=1.4e-14
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=-1.2
x2=1.2
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
sweep=p
color=4
node="\\"capacitance;i(v1) abs() v(p) deriv0() /\\""}
N 2020 680 2020 760 {lab=P}
N 1700 680 2020 680 {lab=P}
N 1700 680 1700 840 {lab=P}
N 1700 900 1700 950 {lab=GND}
N 1700 950 2020 950 {lab=GND}
N 2020 820 2020 950 {lab=GND}
C {vsource.sym} 1700 870 0 0 {name=V1 value="pwl 0 -1.2 400n 1.2" savecurrent=false}
C {gnd.sym} 2020 950 0 0 {name=l1 lab=GND}
C {lab_wire.sym} 2020 680 0 0 {name=p1 sig_type=std_logic lab=P}
C {launcher.sym} 2310 1000 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/tran_moscap_n_nx.raw tran"
}
C {sg13g2_pr/moscap_n.sym} 2020 760 0 0 {name=C1
l=1u
w=1u
m=1
model=sg13_moscap_n
spiceprefix=X
}
C {simulator_commands_shown.sym} 1650 310 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerMOSCAP.lib moscap_tt
"}
C {simulator_commands_shown.sym} 2010 310 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::MODELS_XYCE/cornerMOSCAP.lib moscap_tt
)"}
C {simulator_commands_shown.sym} 1650 420 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.control
save all 
tran 0.1n 400n
let C_abs = abs(i(v1)) / deriv(v(p))
write tran_moscap_n_nx.raw
.endc
"}
C {simulator_commands_shown.sym} 2000 410 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.option temp=27
.tran 0.01ns 400ns 0 0.01ns
.print tran format=raw file=tran_moscap_n_nx.raw V(P) I(V1)
"}
C {launcher.sym} 1710 590 0 0 {name=h3
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
C {launcher.sym} 2060 580 0 0 {name=h2
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
