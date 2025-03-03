v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1050 -90 1050 -30 {
lab=GND}
N 1050 -120 1100 -120 {
lab=GND}
N 1100 -120 1100 -30 {
lab=GND}
N 1050 -270 1050 -250 {
lab=GND}
N 1050 -170 1050 -150 {
lab=Vgs}
N 970 -120 1010 -120 {
lab=Vgs}
N 970 -170 970 -120 {
lab=Vgs}
N 970 -170 1050 -170 {
lab=Vgs}
N 950 -170 970 -170 {
lab=Vgs}
N 1050 -190 1050 -170 {
lab=Vgs}
C {devices/gnd.sym} 1050 -30 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 1100 -30 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} 1050 -220 0 0 {name=I0 value=10u}
C {devices/gnd.sym} 1050 -270 2 0 {name=l2 lab=GND}
C {devices/lab_pin.sym} 950 -170 0 0 {name=p1 sig_type=std_logic lab=Vgs}
C {sg13g2_pr/sg13_lv_nmos.sym} 1030 -120 2 1 {name=M1
l=1.0u
w=2.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {simulator_commands_shown.sym} 110 -520 0 0 {name=Simulator1
simulator=xyce
only_toplevel=false 
value="
.preprocess replaceground true
.param mc_ok=1
.SAMPLING
+useExpr=true
.options SAMPLES numsamples=1000 SAMPLE_TYPE=MC 
.op
.PRINT  dc format=csv file=mc_nmos_cs_xyce.csv   V(Vgs)
"
"}
C {launcher.sym} 200 -300 0 0 {name=h2
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
C {simulator_commands_shown.sym} 120 -640 0 0 {name=Libs_Xyce
simulator=xyce
only_toplevel=false 
value="tcleval(
.lib $::SG13G2_MODELS_XYCE/cornerMOSlv.lib mos_tt_stat
)"}
C {simulator_commands_shown.sym} -430 -580 0 0 {name=Libs_Ngspice
simulator=ngspice
only_toplevel=false 
value="
.lib cornerMOSlv.lib mos_tt_stat
"}
C {launcher.sym} -330 200 0 0 {name=h3
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
C {simulator_commands_shown.sym} -410 -470 0 0 {name=Simulator2
simulator=ngspice
only_toplevel=false 
value=".param mm_ok=1
.param mc_ok=1
.param temp=27

.control

let mc_runs = 10
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let vg=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

*dc Vds 0 3 0.01
op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.Vgs
let Vg[run]=\{$dt\}.Vgs
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata sg13_lv_nmos_cs.csv \{$scratch\}.vg
write sg13_lv_nmos_cs.raw
echo
print \{$scratch\}.vg

.endc
"}
