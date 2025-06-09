v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Nx - number of emitters} -110 90 0 0 0.2 0.2 {}
T {Ctrl-Click to execute launcher} 420 120 0 0 0.3 0.3 {layer=11}
T {Nx - number of emitters} 140 90 0 0 0.2 0.2 {}
T {Uncomment the valid library:
hbt_typ ... without statistical and without mismatch modelling
hbt_typ_mismatch ... with mismatch modelling
hbt_typ_stat ... with statistical modelling
hbt_typ_stat_mismatch ... with statistical and with mismatch modelling} -190 -580 0 0 0.3 0.3 {layer=11}
N -200 30 -200 50 {
lab=GND}
N -200 -40 -200 -30 {
lab=#net1}
N -70 -10 -70 50 {
lab=GND}
N 60 -10 60 50 {
lab=GND}
N -70 -110 -70 -70 {
lab=#net2}
N 60 -110 60 -70 {
lab=#net3}
N -70 -40 -20 -40 {
lab=GND}
N -20 -40 -20 50 {
lab=GND}
N -70 -110 -40 -110 {
lab=#net2}
N 20 -110 60 -110 {
lab=#net3}
N -200 -40 -110 -40 {
lab=#net1}
N 60 -110 90 -110 {lab=#net3}
N 150 -110 190 -110 {lab=#net4}
N 190 -110 190 -70 {lab=#net4}
N 130 -40 130 50 {lab=GND}
N 130 -40 190 -40 {lab=GND}
N 190 -10 190 50 {lab=GND}
N 310 30 310 50 {
lab=GND}
N 310 -40 310 -30 {
lab=#net5}
N 230 -40 310 -40 {lab=#net5}
C {devices/code_shown.sym} -190 -440 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
*.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
*.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ_mismatch
*.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ_stat
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ_stat_mismatch
"}
C {devices/code_shown.sym} 400 -590 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27

.control 
save all
let mc_runs = 3
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let Ic=unitvec(mc_runs)
let Ic1=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.I(Vc)
let Ic[run]= \{$dt\}.I(Vc)
let Ic1[run]= \{$dt\}.I(Vc1)
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata mc_hbt_op.csv \{$scratch\}.Ic \{$scratch\}.Ic1
write mc_hbt_op.raw
echo
print \{$scratch\}.Ic
print \{$scratch\}.Ic1

.endc
"}
C {devices/gnd.sym} -70 50 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -200 50 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 60 -40 0 0 {name=Vce value=1.5}
C {devices/gnd.sym} 60 50 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -20 50 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} -200 0 2 0 {name=I0 value=1u}
C {devices/ammeter.sym} -10 -110 1 0 {name=Vc}
C {sg13g2_pr/npn13G2.sym} -90 -40 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1
}
C {launcher.sym} 480 100 0 0 {name=h1
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
C {sg13g2_pr/npn13G2.sym} 210 -40 0 1 {name=Q2
model=npn13G2
spiceprefix=X
Nx=1
}
C {devices/ammeter.sym} 120 -110 3 1 {name=Vc1}
C {devices/gnd.sym} 130 50 0 0 {name=l6 lab=GND}
C {devices/gnd.sym} 190 50 0 0 {name=l7 lab=GND}
C {devices/gnd.sym} 310 50 0 0 {name=l8 lab=GND}
C {devices/isource.sym} 310 0 2 0 {name=I1 value=1u}
