v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 800 -280 1600 120 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1e-4
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="pad_res"
color="4"
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 800 -720 1600 -320 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1e-4
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="out"
color="7"
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 800 160 1600 560 {flags=graph
y1=0
y2=2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1e-4
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="vdd"
color="12"
dataset=-1
unitx=1
logx=0
logy=0
}
N -340 130 -340 140 {
lab=GND}
N -10 50 -10 80 {
lab=GND}
N -230 -110 -230 -70 {
lab=GND}
N -10 -170 -10 -70 {
lab=vdd}
N -230 -170 -10 -170 {
lab=vdd}
N -340 -10 -340 70 {
lab=pad_res}
N -340 -10 -160 -10 {
lab=pad_res}
N -410 -10 -340 -10 {
lab=pad_res}
N 170 -120 170 -10 {
lab=out}
N 140 -10 170 -10 {
lab=out}
N -10 -170 30 -170 {
lab=vdd}
C {sg13g2_SecondaryProtection.sym} -10 -10 0 1 {name=x1}
C {devices/gnd.sym} -340 140 0 0 {name=l7 lab=GND}
C {devices/vsource.sym} -340 100 0 0 {name=VinB value="dc 0 ac 0 pulse(0, 1.2, 1n, 1u, 1u, 24u, 50u ) "}
C {lab_pin.sym} -340 30 0 0 {name=p5 sig_type=std_logic lab=pad_res}
C {devices/gnd.sym} -10 80 0 0 {name=l4 lab=GND}
C {devices/vsource.sym} -230 -140 0 0 {name=Vdd value=1.2}
C {devices/gnd.sym} -230 -70 0 0 {name=l20 lab=GND}
C {devices/code_shown.sym} -970 -50 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
.include $::SG13G2_MODELS/diodes.lib

.include $::SG13G2_MODELS/resistors_mod.lib
.include $::SG13G2_MODELS/resistors_parm.lib



"}
C {devices/code_shown.sym} -930 -250 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=127
.control
save all 
tran 2u 100u
*meas tran tdelay TRIG v(b) VAl=0.9 FALl=1 TARG v(out) VAl=0.9 RISE=1
write tran_io_secondary_protection.raw

.endc
"}
C {devices/title.sym} -1100 230 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {lab_pin.sym} -410 -10 0 0 {name=p1 sig_type=std_logic lab=pad_res}
C {lab_pin.sym} 170 -120 0 0 {name=p2 sig_type=std_logic lab=out}
C {lab_pin.sym} 30 -170 2 0 {name=p3 sig_type=std_logic lab=vdd}
C {launcher.sym} 260 70 0 0 {name=h1
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/tran_io_secondary_protection.raw tran"}
