v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Uncomment the valid library:
res_typ ... without statistical and without mismatch modelling
res_typ_mismatch ... with mismatch modelling
res_typ_stat ... with statistical modelling
res_typ_stat_mismatch ... with statistical and with mismatch modelling} 370 -480 0 0 0.3 0.3 {layer=11}
T {Ctrl-Click to execute launcher} 370 -200 0 0 0.3 0.3 {layer=11}
N 380 40 380 100 {
lab=GND}
N 380 -100 380 -20 {
lab=Vcc}
N 490 -100 490 -60 {
lab=Vcc}
N 490 0 490 20 {
lab=#net1}
N 490 80 490 100 {
lab=GND}
N 770 -100 770 -60 {
lab=Vcc}
N 770 0 770 20 {
lab=#net2}
N 770 80 770 100 {
lab=GND}
N 1050 -100 1050 -60 {
lab=Vcc}
N 1050 0 1050 20 {
lab=#net3}
N 1050 80 1050 100 {
lab=GND}
N 380 -100 490 -100 {
lab=Vcc}
N 630 -100 630 -60 {
lab=Vcc}
N 630 0 630 20 {
lab=#net4}
N 630 80 630 100 {
lab=GND}
N 630 -100 770 -100 {lab=Vcc}
N 490 -100 630 -100 {
lab=Vcc}
N 910 -100 910 -60 {
lab=Vcc}
N 910 0 910 20 {
lab=#net5}
N 910 80 910 100 {
lab=GND}
N 770 -100 910 -100 {lab=Vcc}
N 910 -100 1050 -100 {
lab=Vcc}
N 1190 -100 1190 -60 {
lab=Vcc}
N 1190 0 1190 20 {
lab=#net6}
N 1190 80 1190 100 {
lab=GND}
N 1050 -100 1190 -100 {
lab=Vcc}
C {devices/code_shown.sym} 370 -340 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
*.lib $::SG13G2_MODELS/cornerRES.lib res_typ
*.lib $::SG13G2_MODELS/cornerRES.lib res_typ_mismatch
*.lib $::SG13G2_MODELS/cornerRES.lib res_typ_stat
.lib $::SG13G2_MODELS/cornerRES.lib res_typ_stat_mismatch
"}
C {devices/code_shown.sym} -490 -480 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control 
let mc_runs = 3
let run = 0
set curplot=new
set scratch=$curplot
setplot $scratch
let rsilval=unitvec(mc_runs)
let rsilval1=unitvec(mc_runs)
let rppdval=unitvec(mc_runs)
let rppdval1=unitvec(mc_runs)
let rhighval=unitvec(mc_runs)
let rhighval1=unitvec(mc_runs)

***************** LOOP *********************
dowhile run < mc_runs

op
set run=$&run
set dt=$curplot
setplot $scratch
let out\{$run\}=\{$dt\}.I(Vsil)
let rsilval[run]= 1.5/\{$dt\}.I(Vsil)
let rsilval1[run]= 1.5/\{$dt\}.I(Vsil1)
let rppdval[run]= 1.5/\{$dt\}.I(Vppd)
let rppdval1[run]= 1.5/\{$dt\}.I(Vppd1)
let rhighval[run]= 1.5/\{$dt\}.I(Vrh)
let rhighval1[run]= 1.5/\{$dt\}.I(Vrh1)
setplot $dt
reset
let run=run+1 
end
***************** LOOP *********************

wrdata mc_res_op.csv \{$scratch\}.rsilval \{$scratch\}.rsilval1 \{$scratch\}.rppdval \{$scratch\}.rppdval1 \{$scratch\}.rhighval \{$scratch\}.rhighval1
write mc_res_op.raw
echo
print \{$scratch\}.rsilval
print \{$scratch\}.rsilval1
print \{$scratch\}.rppdval
print \{$scratch\}.rppdval1
print \{$scratch\}.rhighval
print \{$scratch\}.rhighval1
.endc
"}
C {devices/gnd.sym} 490 100 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 380 10 0 0 {name=Vres value=1.5}
C {devices/gnd.sym} 380 100 0 0 {name=l3 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/lab_pin.sym} 380 -50 2 0 {name=p1 sig_type=std_logic lab=Vcc}
C {devices/ammeter.sym} 490 -30 0 0 {name=Vsil}
C {devices/gnd.sym} 770 100 0 0 {name=l2 lab=GND}
C {devices/ammeter.sym} 770 -30 0 0 {name=Vppd}
C {devices/gnd.sym} 1050 100 0 0 {name=l4 lab=GND}
C {sg13g2_pr/rhigh.sym} 1050 50 0 0 {name=R3
w=1.0e-6
l=1.0e-6
model=rhigh
spiceprefix=X
m=1
R=3.061e+3
Imax=0.11e-4
}
C {devices/ammeter.sym} 1050 -30 0 0 {name=Vrh}
C {sg13g2_pr/rsil.sym} 490 50 0 0 {name=R1
w=0.5e-6
l=0.5e-5
model=rsil
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {sg13g2_pr/rppd.sym} 770 50 0 0 {name=R2
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {launcher.sym} 430 -160 0 0 {name=h3
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
C {devices/gnd.sym} 630 100 0 0 {name=l6 lab=GND}
C {devices/ammeter.sym} 630 -30 0 0 {name=Vsil1}
C {sg13g2_pr/rsil.sym} 630 50 0 0 {name=R4
w=0.5e-6
l=0.5e-5
model=rsil
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {devices/gnd.sym} 910 100 0 0 {name=l7 lab=GND}
C {devices/ammeter.sym} 910 -30 0 0 {name=Vppd1}
C {sg13g2_pr/rppd.sym} 910 50 0 0 {name=R5
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
m=1
R=7.0
Imax=0.3e-6
}
C {devices/gnd.sym} 1190 100 0 0 {name=l8 lab=GND}
C {sg13g2_pr/rhigh.sym} 1190 50 0 0 {name=R6
w=1.0e-6
l=1.0e-6
model=rhigh
spiceprefix=X
m=1
R=3.061e+3
Imax=0.11e-4
}
C {devices/ammeter.sym} 1190 -30 0 0 {name=Vrh1}
