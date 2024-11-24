v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 -280 -540 520 -140 {flags=graph

y2=0.00076
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.5
divx=5
subdivx=1

dataset=-1
unitx=1
logx=0
logy=0
color="4 7"
node="i(Vc)
i(vc1)"
y1=-3.3e-05
rainbow=0}
T {Nx - number of emitters} -210 110 0 0 0.2 0.2 {}
N -300 60 -300 80 {
lab=GND}
N -300 -10 -300 0 {
lab=#net1}
N -170 20 -170 80 {
lab=GND}
N 40 20 40 80 {
lab=GND}
N -170 -80 -170 -40 {
lab=#net2}
N 40 -80 40 -40 {
lab=#net3}
N -170 -80 -140 -80 {
lab=#net2}
N -80 -80 40 -80 {
lab=#net3}
N -300 -10 -210 -10 {
lab=#net1}
N -140 40 -140 80 {
lab=GND}
N -120 -10 -80 -10 {
lab=tmp}
N -80 70 -80 80 {
lab=GND}
N -80 -10 -80 10 {
lab=tmp}
N -80 -20 -80 -10 {
lab=tmp}
N 400 70 400 90 {
lab=GND}
N 400 0 400 10 {
lab=#net4}
N 290 30 290 80 {
lab=GND}
N 250 0 250 80 {
lab=GND}
N 250 0 290 0 {
lab=GND}
N 290 -80 290 -30 {
lab=#net5}
N 210 -80 290 -80 {
lab=#net5}
N 40 -80 150 -80 {
lab=#net3}
N 330 -0 400 -0 {
lab=#net4}
C {devices/code_shown.sym} -750 -480 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
"}
C {devices/code_shown.sym} -650 -380 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
op
print I(Vc)
print V(tmp)
reset 
dc Vce 0 1.5 0.01 
write test_npn_13G2.raw
.endc
"}
C {devices/gnd.sym} -170 80 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -300 80 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 40 -10 0 0 {name=Vce value=1.5}
C {devices/gnd.sym} 40 80 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} -140 80 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/isource.sym} -300 30 2 0 {name=I0 value=1u}
C {devices/ammeter.sym} -110 -80 1 0 {name=Vc}
C {res.sym} -80 40 0 0 {name=R1
value=10G
footprint=1206
device=resistor
m=1}
C {devices/gnd.sym} -80 80 0 0 {name=l6 lab=GND}
C {lab_wire.sym} -80 -20 0 0 {name=p1 sig_type=std_logic lab=tmp}
C {devices/launcher.sym} 600 -160 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/test_npn_13G2.raw dc"
}
C {devices/gnd.sym} 400 90 0 0 {name=l7 lab=GND}
C {devices/isource.sym} 400 40 2 0 {name=I1 value=1u}
C {devices/gnd.sym} 290 80 0 0 {name=l8 lab=GND}
C {devices/gnd.sym} 250 80 0 0 {name=l9 lab=GND}
C {devices/ammeter.sym} 180 -80 3 0 {name=Vc1}
C {sg13g2_pr/npn13G2v.sym} 310 0 0 1 {name=Q1
model=npn13G2v
spiceprefix=X
Nx=1
}
C {sg13g2_pr/npn13G2v_5t.sym} -190 -10 0 0 {name=Q2
model=npn13G2v_5t
spiceprefix=X
Nx=1
drc=hbt_drc}
