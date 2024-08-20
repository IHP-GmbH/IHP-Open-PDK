v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 410 -230 1210 170 {flags=graph
y1=-3e-06
y2=2.3e-06
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-12
x2=1
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0
color="7 8"
node="i(Vmdp)
i(Vmda)"}
N -500 20 -500 40 {
lab=GND}
N -500 -100 -500 -40 {
lab=#net1}
N -500 -100 -170 -100 {
lab=#net1}
N -170 -30 -170 0 {
lab=#net2}
N -170 -100 -170 -90 {
lab=#net1}
N -150 300 -150 330 {
lab=GND}
N -190 300 -190 320 {
lab=GND}
C {devices/gnd.sym} -500 40 0 0 {name=l2 lab=GND}
C {devices/code_shown.sym} -520 -180 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.include $::SG13G2_MODELS/diodes.lib
"}
C {devices/code_shown.sym} 40 60 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
op
print I(Vmdp) 
reset 
dc V1 -12 1 1m
write dc_diode_op.raw
wrdata dc_diode.csv I(Vmdp)
.endc
"}
C {devices/title.sym} -350 520 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -470 -260 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_diode_op.raw dc"
}
C {devices/gnd.sym} -150 330 0 0 {name=l3 lab=GND}
C {devices/vsource.sym} -500 -10 0 0 {name=V1 value=0.7}
C {devices/ammeter.sym} -170 -60 0 0 {name=Vmdp}
C {sg13g2_DCNDiode.sym} -170 150 1 0 {name=x1}
C {devices/gnd.sym} -190 320 0 0 {name=l1 lab=GND}
