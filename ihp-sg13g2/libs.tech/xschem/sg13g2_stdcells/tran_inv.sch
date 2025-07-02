v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 -160 -630 640 -230 {flags=graph
y1=-0.11
y2=2.1
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=2e-08
divx=5
subdivx=1


dataset=-1
unitx=1
logx=0
logy=0
color="4 5"
node="out
in"}
N -180 90 -180 110 {
lab=GND}
N -180 -30 -180 30 {
lab=in}
N -180 -30 -140 -30 {
lab=in}
N 0 -30 60 -30 {
lab=out}
N -200 -30 -180 -30 {
lab=in}
N 0 -30 0 0 {
lab=out}
N -60 -30 0 -30 {
lab=out}
C {devices/code_shown.sym} -290 170 0 0 {name=MODEL
only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerMOSlv.lib mos_tt
.include $::PDK_ROOT/ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice
"
place=header}
C {devices/code_shown.sym} 160 -70 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
vvdd vdd 0 dc 1.8
vvss vss 0 0
.control
save all 
tran 50p 20n
meas tran tdelay TRIG v(in) VAL=0.9 FALL=1 TARG v(out) VAL=0.9 RISE=1
write tran_inv.raw
.endc
"}
C {devices/gnd.sym} -180 110 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -180 60 0 0 {name=Vin value="dc 0 ac 0 pulse(0, 1.8, 0, 100p, 100p, 2n, 4n ) "}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2024 IHP PDK Authors"}
C {devices/launcher.sym} 230 -170 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/tran_logic_not.raw tran"
}
C {devices/lab_pin.sym} -200 -30 0 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 60 -30 2 0 {name=p2 sig_type=std_logic lab=out}
C {sg13g2_stdcells/sg13g2_inv_1.sym} -100 -30 0 0 {name=x1 VDD=VDD VSS=VSS prefix=sg13g2_ }
C {devices/parax_cap.sym} 0 10 0 0 {name=C1 gnd=GND value=4f m=1}
