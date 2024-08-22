v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 350 -260 1150 140 {flags=graph
y1=-5.2e-07
y2=2.9
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.8
divx=5
subdivx=1


dataset=-1
unitx=1
logx=0
logy=0

color="7 6"
node="gain
out"}
N -290 100 -290 120 {
lab=GND}
N 20 60 20 120 {
lab=GND}
N 280 60 280 120 {
lab=GND}
N 70 30 70 120 {
lab=GND}
N 20 30 70 30 {
lab=GND}
N 20 -70 70 -70 {
lab=#net1}
N 20 -20 20 0 {
lab=out}
N 20 -170 20 -100 {
lab=#net1}
N 70 -170 280 -170 {
lab=#net1}
N 280 -170 280 0 {
lab=#net1}
N 70 -170 70 -70 {
lab=#net1}
N -50 30 -20 30 {
lab=in}
N -50 -20 -50 30 {
lab=in}
N -50 -70 -20 -70 {
lab=in}
N -290 -20 -290 40 {
lab=in}
N -290 -20 -50 -20 {
lab=in}
N 20 -20 150 -20 {
lab=out}
N -310 -20 -290 -20 {
lab=in}
N 20 -170 70 -170 {
lab=#net1}
N 20 -40 20 -20 {
lab=out}
N -50 -70 -50 -20 {
lab=in}
C {devices/code_shown.sym} -300 170 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
"}
C {devices/code_shown.sym} -360 -260 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
dc Vin 0 1.8 1m
let gain = -deriv(V(out))/10
write dc_logic_not.raw
.endc
"}
C {devices/gnd.sym} 20 120 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -290 120 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -290 70 0 0 {name=Vin value="dc 0 ac 0 pulse(0, 1.8, 0, 100p, 100p, 2n, 4n ) "}
C {devices/vsource.sym} 280 30 0 0 {name=Vdd value=1.8}
C {devices/gnd.sym} 280 120 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 70 120 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 420 180 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/dc_logic_not.raw dc"
}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 30 2 1 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 -70 0 0 {name=M2
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} -310 -20 0 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 150 -20 2 0 {name=p2 sig_type=std_logic lab=out}
