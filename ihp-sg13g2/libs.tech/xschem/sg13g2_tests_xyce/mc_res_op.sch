v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 380 40 380 100 {
lab=GND}
N 380 -100 380 -20 {
lab=Vcc}
N 380 -100 610 -100 {
lab=Vcc}
N 610 -100 610 -60 {
lab=Vcc}
N 610 0 610 20 {
lab=#net1}
N 610 80 610 100 {
lab=GND}
N 760 -100 760 -60 {
lab=Vcc}
N 760 0 760 20 {
lab=#net2}
N 760 80 760 100 {
lab=GND}
N 940 -100 940 -60 {
lab=Vcc}
N 940 0 940 20 {
lab=#net3}
N 940 80 940 100 {
lab=GND}
N 610 -100 760 -100 {
lab=Vcc}
N 760 -100 940 -100 {
lab=Vcc}
C {devices/gnd.sym} 610 100 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 380 10 0 0 {name=Vres value=1.5}
C {devices/gnd.sym} 380 100 0 0 {name=l3 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/lab_pin.sym} 380 -50 2 0 {name=p1 sig_type=std_logic lab=Vcc}
C {devices/ammeter.sym} 610 -30 0 0 {name=Vsil}
C {devices/gnd.sym} 760 100 0 0 {name=l2 lab=GND}
C {devices/ammeter.sym} 760 -30 0 0 {name=Vppd}
C {devices/gnd.sym} 940 100 0 0 {name=l4 lab=GND}
C {sg13g2_pr/rhigh.sym} 940 50 0 0 {name=R3
w=1.0e-6
l=1.0e-6
model=rhigh
spiceprefix=X
m=1
R=3.061e+3
Imax=0.11e-4
}
C {devices/ammeter.sym} 940 -30 0 0 {name=Vrh}
C {sg13g2_pr/rsil.sym} 610 50 0 0 {name=R1
w=0.5e-6
l=0.5e-5
model=rsil
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {sg13g2_pr/rppd.sym} 760 50 0 0 {name=R2
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {simulator_commands_shown.sym} 180 -610 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.SAMPLING
+useExpr=true
.options SAMPLES numsamples=1000 SAMPLE_TYPE=MC 
.op
*.dc Vres 1.5 1.5 0.1   * one point sweep 
.PRINT  dc format=csv file=mc_res_op_xyce.csv   V(Vcc)  I(Vsil) I(Vppd)  I(Vrh)
"
"}
C {launcher.sym} 260 -390 0 0 {name=h2
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
C {simulator_commands_shown.sym} 190 -730 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerRES.lib res_typ_stat
)"}
C {simulator_commands_shown.sym} -380 -730 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerRES.lib res_typ_stat
"}
C {launcher.sym} -340 100 0 0 {name=h3
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
C {simulator_commands_shown.sym} -410 -630 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.param mc_ok = 1
.control 
let mc_runs = 1000
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let rsilval=unitvec(mc_runs)
let rppdval=unitvec(mc_runs)
let rhighval=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.I(Vsil)
let rsilval[run]= 1.5/\{$dt\}.I(Vsil)
let rppdval[run]= 1.5/\{$dt\}.I(Vppd)
let rhighval[run]= 1.5/\{$dt\}.I(Vrh)
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata mc_res_op.csv \{$scratch\}.rsilval \{$scratch\}.rppdval \{$scratch\}.rhighval
write mc_res_op.raw
echo
print \{$scratch\}.rsilval
print \{$scratch\}.rppdval
print \{$scratch\}.rhighval
.endc
"}
