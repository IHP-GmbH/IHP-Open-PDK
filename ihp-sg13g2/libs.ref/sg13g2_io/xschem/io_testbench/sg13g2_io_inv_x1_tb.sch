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
N -600 120 -600 140 {
lab=GND}
N -220 10 -220 70 {
lab=GND}
N 100 50 100 110 {
lab=GND}
N 100 -180 100 -10 {
lab=#net1}
N -600 0 -600 60 {
lab=in}
N -90 -30 40 -30 {
lab=out}
N -440 -30 -330 -30 {
lab=in}
N -620 0 -600 0 {
lab=in}
N -220 -180 -220 -80 {
lab=#net1}
N -220 -180 100 -180 {
lab=#net1}
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
C {devices/gnd.sym} -220 70 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -600 140 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -600 90 0 0 {name=Vin value="dc 0 ac 0 pulse(0, 1.2, 0, 100p, 100p, 2n, 4n ) "}
C {devices/vsource.sym} 100 20 0 0 {name=Vdd value=1.2}
C {devices/gnd.sym} 100 110 0 0 {name=l3 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 230 -170 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/tran_logic_not.raw tran"
}
C {devices/lab_pin.sym} -620 0 0 0 {name=p1 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 40 -30 2 0 {name=p2 sig_type=std_logic lab=out}
C {sg13g2_io_inv_x1.sym} -180 -30 0 0 {name=x1}
C {devices/lab_pin.sym} -440 -30 0 0 {name=p3 sig_type=std_logic lab=in}
