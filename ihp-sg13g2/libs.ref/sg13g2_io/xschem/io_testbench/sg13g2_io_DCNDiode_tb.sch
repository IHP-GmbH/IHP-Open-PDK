v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 110 -470 910 -70 {flags=graph
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
N 140 -30 230 -30 {
lab=GND}
N 140 100 140 140 {
lab=GND}
N 140 10 140 40 {
lab=#net1}
N -330 130 -330 140 {
lab=GND}
N -330 30 -330 70 {
lab=in}
N -270 -10 -160 -10 {
lab=#net2}
N -380 30 -330 30 {
lab=in}
N -330 -10 -330 30 {
lab=in}
C {sg13g2_DCNDiode.sym} -10 -10 0 0 {name=x1}
C {gnd.sym} 230 -30 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 140 70 0 0 {name=Vdd2 value=1.2}
C {devices/gnd.sym} 140 140 0 0 {name=l2 lab=GND}
C {devices/code_shown.sym} -30 220 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
tran 50p 20n
*meas tran tdelay TRIG v(in) VAl=0.9 FALl=1 TARG v(out) VAl=0.9 RISE=1
write tran_logic_not.raw

wrdata tran_DCNDiode.csv I(Vmeas)
PLOT I(Vmeas)
display
.endc
"}
C {devices/code_shown.sym} -430 220 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.include $::SG13G2_MODELS/diodes.lib
"}
C {devices/title.sym} -520 520 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -330 -210 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/tran_DCNDiode_op.raw dc"
}
C {devices/gnd.sym} -330 140 0 0 {name=l7 lab=GND}
C {devices/vsource.sym} -330 100 0 0 {name=Vin value="dc 0 ac 0 pulse(0, 1.2, 0, 100p, 100p, 2n, 4n ) "}
C {ammeter.sym} -300 -10 3 0 {name=Vmeas savecurrent=true spice_ignore=0}
C {lab_pin.sym} -380 30 0 0 {name=p1 sig_type=std_logic lab=in}
