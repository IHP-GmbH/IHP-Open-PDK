v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 500 -250 1300 150 {flags=graph
y1=-0.0651089
y2=2.58689
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
color=4
node=out}
B 2 500 -670 1300 -270 {flags=graph
y1=0
y2=1.8
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=2e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=a
color=6
dataset=-1
unitx=1
logx=0
logy=0
}
B 2 500 -1080 1300 -680 {flags=graph
y1=0
y2=1.8
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=2e-08
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=b

dataset=-1
unitx=1
logx=0
logy=0
color=7}
N 100 70 100 130 {
lab=GND}
N 410 -50 410 130 {
lab=GND}
N 150 40 150 130 {
lab=GND}
N 100 40 150 40 {
lab=GND}
N -50 -190 0 -190 {
lab=#net1}
N -50 -290 -50 -220 {
lab=#net1}
N 0 -290 0 -190 {
lab=#net1}
N -190 40 -170 40 {
lab=A}
N 180 -190 230 -190 {
lab=#net1}
N 180 -290 180 -220 {
lab=#net1}
N 230 -290 230 -190 {
lab=#net1}
N 100 -40 200 -40 {
lab=GND}
N 200 -40 200 40 {
lab=GND}
N 100 -10 100 10 {
lab=#net2}
N -50 -160 -50 -140 {
lab=out}
N 100 -140 180 -140 {
lab=out}
N 180 -160 180 -140 {
lab=out}
N 100 -90 100 -70 {
lab=out}
N -50 -140 100 -140 {
lab=out}
N 60 -190 140 -190 {
lab=B}
N 60 -190 60 -40 {
lab=B}
N -90 40 60 40 {
lab=A}
N -90 -190 -90 40 {
lab=A}
N -170 40 -90 40 {
lab=A}
N -170 120 -170 130 {
lab=GND}
N -170 40 -170 60 {
lab=A}
N -290 -40 -270 -40 {
lab=B}
N -270 40 -270 50 {
lab=GND}
N -270 -40 -270 -20 {
lab=B}
N -270 -40 60 -40 {
lab=B}
N 230 -290 410 -290 {
lab=#net1}
N 410 -290 410 -110 {
lab=#net1}
N 100 -90 240 -90 {
lab=out}
N -50 -290 0 -290 {
lab=#net1}
N 0 -290 180 -290 {
lab=#net1}
N 180 -290 230 -290 {
lab=#net1}
N 100 -140 100 -90 {
lab=out}
C {devices/code_shown.sym} -290 190 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_ff
"}
C {devices/code_shown.sym} -330 -530 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=127
.control
save all 
tran 50p 20n
meas tran tdelay TRIG v(b) VAl=0.9 FALl=1 TARG v(out) VAl=0.9 RISE=1
write tran_logic_nand.raw
.endc
"}
C {devices/gnd.sym} 100 130 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -170 130 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -170 90 0 0 {name=VinA value="dc 0 ac 0 pulse(0, 1.2, 2n, 100p, 100p, 4n, 6n ) "}
C {devices/vsource.sym} 410 -80 0 0 {name=Vdd value=1.2}
C {devices/gnd.sym} 410 130 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 150 130 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -270 -610 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/tran_logic_nand.raw tran"
}
C {sg13g2_pr/sg13_lv_nmos.sym} 80 40 2 1 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -70 -190 0 0 {name=M2
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/lab_pin.sym} -190 40 0 0 {name=p1 sig_type=std_logic lab=A}
C {devices/lab_pin.sym} 240 -90 2 0 {name=p2 sig_type=std_logic lab=out}
C {sg13g2_pr/sg13_lv_pmos.sym} 160 -190 0 0 {name=M3
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 80 -40 2 1 {name=M4
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {devices/gnd.sym} 200 40 0 0 {name=l6 lab=GND}
C {devices/gnd.sym} -270 50 0 0 {name=l7 lab=GND}
C {devices/vsource.sym} -270 10 0 0 {name=VinB value="dc 0 ac 0 pulse(0, 1.2, 0, 100p, 100p, 2n, 4n ) "}
C {devices/lab_pin.sym} -290 -40 0 0 {name=p3 sig_type=std_logic lab=B}
