v {xschem version=3.4.5 file_version=1.2
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
N -440 90 -440 110 {
lab=GND}
N -160 50 -160 110 {
lab=GND}
N 100 50 100 110 {
lab=GND}
N -110 20 -110 110 {
lab=GND}
N -160 20 -110 20 {
lab=GND}
N -160 -80 -110 -80 {
lab=#net1}
N -160 -30 -160 -10 {
lab=out}
N -160 -180 -160 -110 {
lab=#net1}
N -110 -180 100 -180 {
lab=#net1}
N 100 -180 100 -10 {
lab=#net1}
N -110 -180 -110 -80 {
lab=#net1}
N -230 20 -200 20 {
lab=in}
N -230 -30 -230 20 {
lab=in}
N -230 -80 -200 -80 {
lab=in}
N -440 -30 -440 30 {
lab=in}
N -160 -30 -30 -30 {
lab=out}
N -460 -30 -440 -30 {
lab=in}
N -440 -30 -230 -30 {
lab=in}
N -160 -180 -110 -180 {
lab=#net1}
N -230 -80 -230 -30 {
lab=in}
N -160 -50 -160 -30 {
lab=out}
C {devices/code_shown.sym} -300 170 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
"}
C {devices/code_shown.sym} 160 -70 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
tran 50p 20n
meas tran tdelay TRIG v(in) VAl=0.9 FALl=1 TARG v(out) VAl=0.9 RISE=1
write tran_logic_not.raw
.endc
"}
C {devices/gnd.sym} -160 110 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -440 110 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -440 60 0 0 {name=Vin value="dc 0 ac 0 pulse(0, 1.2, 0, 100p, 100p, 2n, 4n ) "}
C {devices/vsource.sym} 100 20 0 0 {name=Vdd value=1.2}
C {devices/gnd.sym} 100 110 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -110 110 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 230 -170 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/tran_logic_not.raw tran"
}
C {sg13g2_pr/sg13_lv_nmos.sym} -180 20 2 1 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -180 -80 0 0 {name=M2
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} -460 -30 0 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} -30 -30 2 0 {name=p2 sig_type=std_logic lab=out}
