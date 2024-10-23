v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 150 -510 950 -110 {flags=graph
y1=-5e-05
y2=1.4e-11
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=-1.2
x2=0
divx=5
subdivx=1
node=i(vd)
color=4
dataset=-1
unitx=1
logx=0
logy=0
}
T {The Vds source is inverted in 
order to plot positive value of 
the current, which corresponds 
to real value of Ic} -290 -110 0 0 0.3 0.3 {}
N -110 70 -110 90 {
lab=GND}
N -110 -0 -110 10 {
lab=#net1}
N 20 30 20 90 {
lab=GND}
N 150 30 150 90 {
lab=GND}
N 20 0 70 0 {
lab=GND}
N 70 0 70 90 {
lab=GND}
N 20 -110 50 -110 {
lab=#net2}
N 110 -110 150 -110 {
lab=#net3}
N -110 0 -20 0 {
lab=#net1}
N 20 -110 20 -30 {
lab=#net2}
N 150 -110 150 -30 {
lab=#net3}
C {devices/code_shown.sym} -200 160 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
"}
C {devices/code_shown.sym} 290 -10 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
dc Vds 0 -1.2 -0.01 Vgs -0.35 -1.1 -0.05
write dc_lv_pmos.raw
.endc
"}
C {devices/gnd.sym} 20 90 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -110 90 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -110 40 0 0 {name=Vgs value=-0.75}
C {devices/vsource.sym} 150 0 0 0 {name=Vds value=-1.5}
C {devices/gnd.sym} 150 90 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 70 90 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -230 -150 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/dc_lv_pmos.raw dc"
}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 2 1 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/ammeter.sym} 80 -110 1 0 {name=Vd}
