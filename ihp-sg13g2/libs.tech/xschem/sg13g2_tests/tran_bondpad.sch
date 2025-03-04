v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 500 -250 1300 150 {flags=graph
y1=-3.3
y2=0.72
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
y1=-3.3
y2=3.3
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


dataset=-1
unitx=1
logx=0
logy=0
color=4
node=in}
N -240 160 -240 170 {
lab=GND}
N 10 -200 10 -170 {lab=out}
N -60 -200 -60 -170 {lab=GND}
N -130 -200 -130 -170 {lab=in}
N -240 0 -110 0 {lab=in}
N -240 0 -240 100 {lab=in}
N -50 0 130 0 {lab=out}
N 130 0 130 70 {lab=out}
N 130 130 130 170 {lab=GND}
N 130 0 150 0 {lab=out}
N -270 0 -240 -0 {lab=in}
C {devices/code_shown.sym} -330 -490 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.include diodes.lib
.include sg13g2_bondpad.lib
"}
C {devices/code_shown.sym} 160 -430 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=127
.control
save all 
tran 50p 20n
write tran_bondpad.raw
.endc
"}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 220 -510 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/tran_bondpad.raw tran"
}
C {devices/lab_pin.sym} 150 0 2 0 {name=p2 sig_type=std_logic lab=out}
C {devices/gnd.sym} 130 170 0 0 {name=l6 lab=GND}
C {devices/gnd.sym} -240 170 0 0 {name=l7 lab=GND}
C {devices/vsource.sym} -240 130 0 0 {name=VinB value="dc 0 ac 0 pulse(-3.3, 3.3, 0, 100p, 100p, 2n, 4n ) "}
C {devices/lab_pin.sym} -270 0 0 0 {name=p3 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} -130 -170 0 0 {name=p5 sig_type=std_logic lab=in}
C {devices/lab_pin.sym} 10 -170 2 0 {name=p6 sig_type=std_logic lab=out}
C {devices/gnd.sym} -60 -170 0 0 {name=l8 lab=GND}
C {sg13g2_pr/dantenna.sym} 130 100 2 0 {name=D1
model=dantenna
l=200.78u
w=200.78u
spiceprefix=X
}
C {sg13g2_pr/dantenna.sym} -80 0 1 0 {name=D2
model=dantenna
l=200.78u
w=200.78u
spiceprefix=X
}
C {sg13g2_pr/bondpad.sym} -130 -240 0 0 {name=X1
model=bondpad
spiceprefix=X
size=80u
shape=0
padtype=0
}
C {sg13g2_pr/bondpad.sym} -60 -240 0 0 {name=X2
model=bondpad
spiceprefix=X
size=80u
shape=0
padtype=0
}
C {sg13g2_pr/bondpad.sym} 10 -240 0 0 {name=X3
model=bondpad
spiceprefix=X
size=80u
shape=0
padtype=0
}
