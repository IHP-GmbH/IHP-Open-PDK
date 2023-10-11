v {xschem version=3.4.4 file_version=1.2
}
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
N -290 90 -290 110 {
lab=GND}
N -290 20 -290 30 {
lab=in}
N -160 50 -160 110 {
lab=GND}
N 100 50 100 110 {
lab=GND}
N 100 -50 100 -10 {
lab=#net1}
N -210 20 -200 20 {
lab=in}
N -110 20 -110 50 {
lab=#net2}
N -160 20 -110 20 {
lab=#net2}
N -110 -100 -110 -80 {
lab=#net3}
N -160 -80 -110 -80 {
lab=#net3}
N -160 -50 -160 -10 {
lab=out}
N -160 -180 -160 -110 {
lab=#net1}
N -160 -180 100 -180 {
lab=#net1}
N 100 -180 100 -50 {
lab=#net1}
N -110 -180 -110 -160 {
lab=#net1}
N -230 20 -210 20 {
lab=in}
N -230 -80 -230 20 {
lab=in}
N -230 -80 -200 -80 {
lab=in}
N -290 -30 -290 20 {
lab=in}
N -290 -30 -230 -30 {
lab=in}
N -160 -30 -30 -30 {
lab=out}
N -310 -30 -290 -30 {
lab=in}
C {devices/code_shown.sym} -290 190 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerMOSlv.lib mos_tt
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
"}
C {devices/code_shown.sym} 160 -70 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
pre_osdi ./psp103_nqs.osdi
save all 
tran 50p 20n
meas tran tdelay TRIG v(in) VAL=0.9 FALL=1 TARG v(out) VAL=0.9 RISE=1
write ../raw/tran_logic_not.raw
.endc
"}
C {devices/gnd.sym} -160 110 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -290 110 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -290 60 0 0 {name=Vin value="dc 0 ac 0 pulse(0, 1.8, 0, 100p, 100p, 2n, 4n ) "}
C {devices/vsource.sym} 100 20 0 0 {name=Vdd value=1.8}
C {devices/gnd.sym} 100 110 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -110 110 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 230 -170 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/../raw/tran_logic_not.raw tran"
}
C {sg13g2_pr/sg13_lv_nmos.sym} -180 20 2 1 {name=M1
L=0.45u
W=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/ptap1.sym} -110 80 0 0 {name=R1
model=ptap1
spiceprefix=X
R=262.847.0
Imax=0.3e-6
}
C {sg13g2_pr/ntap1.sym} -110 -130 0 0 {name=R2
model=ntap1
spiceprefix=X
R=262.847.0
Imax=0.3e-6
}
C {sg13g2_pr/sg13_lv_pmos.sym} -180 -80 0 0 {name=M2
L=0.45u
W=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} -310 -30 0 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} -30 -30 2 0 {name=p2 sig_type=std_logic lab=out}
