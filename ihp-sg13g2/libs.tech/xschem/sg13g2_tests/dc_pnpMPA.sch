v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 -280 -540 520 -140 {flags=graph
y1=0.65
y2=0.9
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=-7.30266
x2=-3.57959
divx=5
subdivx=8
node=e1
color=4
dataset=0
unitx=1
logx=1
logy=0
hilight_wave=-1}
N -300 60 -300 80 {
lab=GND}
N -300 -10 -300 0 {
lab=#net1}
N -40 20 -40 80 {
lab=GND}
N -170 -80 -170 -40 {
lab=E1}
N -40 -80 -40 -40 {
lab=#net2}
N -170 -80 -140 -80 {
lab=E1}
N -80 -80 -40 -80 {
lab=#net2}
N -300 -10 -210 -10 {
lab=#net1}
C {devices/code_shown.sym} -310 180 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
"}
C {devices/code_shown.sym} 180 0 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all
op
dc I0 5n 100u 0.05u
write test_pnpMPA.raw
.endc
"}
C {devices/gnd.sym} -170 80 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -300 80 0 0 {name=l2 lab=GND}
C {devices/gnd.sym} -40 80 0 0 {name=l3 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 70 -70 0 0 {name=h5
descr="load/unload waves" 
tclcommand="xschem raw_read $netlist_dir/test_pnpMPA.raw dc"
}
C {sg13g2_pr/pnpMPA.sym} -190 -10 0 0 {name=Q1
model=pnpMPA
spiceprefix=X
w=1.0u
l=2.0u}
C {devices/ammeter.sym} -110 -80 1 0 {name=Ve}
C {devices/ammeter.sym} -300 30 0 0 {name=Vb}
C {devices/ammeter.sym} -170 50 0 0 {name=Vc}
C {devices/isource.sym} -40 -10 2 0 {name=I0 value=1u}
C {devices/lab_pin.sym} -170 -60 0 0 {name=p1 sig_type=std_logic lab=E1}
