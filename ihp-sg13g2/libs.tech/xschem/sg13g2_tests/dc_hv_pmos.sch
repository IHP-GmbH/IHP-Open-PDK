v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 150 -510 950 -110 {flags=graph
y1=-1.1e-05
y2=-0
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=-2
x2=0
divx=5
subdivx=1


dataset=-1
unitx=1
logx=0
logy=0
color=4
node=i(vd)}
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
N -110 0 -20 0 {
lab=#net1}
N 20 -110 50 -110 {
lab=#net2}
N 20 -110 20 -30 {
lab=#net2}
N 110 -110 150 -110 {
lab=#net3}
N 150 -110 150 -30 {
lab=#net3}
C {devices/code_shown.sym} -200 160 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_tt
"}
C {devices/code_shown.sym} 290 -10 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all
op 
print I(Vd)
dc Vds 0 -2 -0.01 Vgs -0.45 -1.1 -0.05
write dc_hv_pmos.raw
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
tclcommand="xschem raw_read $netlist_dir/dc_hv_pmos.raw dc"
}
C {sg13g2_pr/sg13_hv_pmos.sym} 0 0 2 1 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/ammeter.sym} 80 -110 1 0 {name=Vd}
