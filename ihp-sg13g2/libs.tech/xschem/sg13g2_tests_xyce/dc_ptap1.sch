v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 100 -460 900 -60 {flags=graph

y2=0.012
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=3
divx=5
subdivx=1

dataset=-1
unitx=1
logx=0
logy=0


y1=0
rainbow=0
color=4
node=i(vr)}
T {Here GND is only for simulation purpose. The actuall connection is to substrate.} -150 100 0 0 0.2 0.2 {}
N -180 80 -180 100 {
lab=GND}
N -180 -60 -180 -20 {
lab=#net1}
N 0 -60 0 -20 {
lab=Vcc}
N -180 -60 -100 -60 {
lab=#net1}
N -40 -60 0 -60 {
lab=Vcc}
N 0 -60 50 -60 {
lab=Vcc}
N -180 80 0 80 {
lab=GND}
N 0 40 0 80 {
lab=GND}
N -180 40 -180 80 {
lab=GND}
C {devices/code_shown.sym} -210 160 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerRES.lib  res_typ 
"}
C {devices/code_shown.sym} 290 -10 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
op
print Vcc/I(Vr)
reset 
dc Vres 0 3 0.01 
write dc_ptap1.raw
.endc
"}
C {devices/gnd.sym} -180 100 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 0 10 0 0 {name=Vres value=1.5}
C {devices/title.sym} -100 240 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -120 -200 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/dc_ptap1.raw dc"
}
C {devices/lab_pin.sym} 50 -60 2 0 {name=p1 sig_type=std_logic lab=Vcc}
C {sg13g2_pr/ptap1.sym} -180 10 0 0 {name=R1
model=ntap1
spiceprefix=X
R=262.847.0
Imax=0.3e-6
}
C {devices/ammeter.sym} -70 -60 1 0 {name=Vr}
