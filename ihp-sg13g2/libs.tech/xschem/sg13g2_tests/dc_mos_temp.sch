v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 150 -520 950 -120 {flags=graph
y1=-2e-05
y2=9.5e-05
ypos1=0
ypos2=2

subdivy=1
unity=1
x1=-40
x2=125

subdivx=1


dataset=-1
unitx=1
logx=0
logy=0
color="7 4 6 8"
node="i(vm2)
i(vm1)
i(vm3)
i(vm4)"
divx=10
divy=10}
N -280 180 -280 200 {
lab=GND}
N -280 110 -280 120 {
lab=Vgs}
N -20 140 -20 200 {
lab=GND}
N -280 0 -280 60 {
lab=GND}
N -280 -100 -280 -60 {
lab=Vds}
N -20 110 30 110 {
lab=GND}
N 30 110 30 200 {
lab=GND}
N -280 110 -250 110 {
lab=Vgs}
N -130 110 -60 110 {
lab=Vgs}
N -280 -100 -270 -100 {
lab=Vds}
N -20 -20 -20 0 {
lab=Vds}
N -20 60 -20 80 {
lab=#net1}
N 190 140 190 200 {
lab=GND}
N 190 110 240 110 {
lab=GND}
N 240 110 240 200 {
lab=GND}
N 80 110 150 110 {
lab=Vgs}
N 190 -20 190 0 {
lab=Vds}
N 190 60 190 80 {
lab=#net2}
N 660 140 660 200 {
lab=GND}
N 660 110 710 110 {
lab=GND}
N 710 110 710 200 {
lab=GND}
N 550 110 620 110 {
lab=Vgsp}
N 660 -20 660 0 {
lab=Vdsp}
N 660 60 660 80 {
lab=#net3}
N 870 140 870 200 {
lab=GND}
N 870 110 920 110 {
lab=GND}
N 920 110 920 200 {
lab=GND}
N 760 110 830 110 {
lab=Vgsp}
N 870 -20 870 0 {
lab=Vdsp}
N 870 60 870 80 {
lab=#net4}
N 390 180 390 200 {
lab=GND}
N 390 110 390 120 {
lab=Vgsp}
N 390 0 390 60 {
lab=GND}
N 390 -100 390 -60 {
lab=Vdsp}
N 390 110 420 110 {
lab=Vgsp}
N 390 -100 400 -100 {
lab=Vdsp}
C {devices/code_shown.sym} -330 -530 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
"}
C {devices/code_shown.sym} -320 -410 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all
dc temp -40 125 1
write mos_temp.raw
wrdata mos_temp.csv I(Vm1) I(Vm2) I(Vm3) I(Vm4)
.endc
"}
C {devices/gnd.sym} -20 200 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -280 200 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} -280 150 0 0 {name=Vgs value=0.75}
C {devices/vsource.sym} -280 -30 0 0 {name=Vds value=1.2}
C {devices/gnd.sym} -280 60 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 30 200 0 0 {name=l4 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -220 -150 0 0 {name=h5
descr="load waves Ctrl + left click" 
tclcommand="xschem raw_read $netlist_dir/mos_temp.raw dc"
}
C {sg13g2_pr/sg13_lv_nmos.sym} -40 110 2 1 {name=M1
l=0.35u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {devices/lab_pin.sym} -250 110 2 0 {name=p1 sig_type=std_logic lab=Vgs}
C {devices/lab_pin.sym} -130 110 0 0 {name=p2 sig_type=std_logic lab=Vgs}
C {devices/lab_pin.sym} -270 -100 2 0 {name=p3 sig_type=std_logic lab=Vds}
C {devices/ammeter.sym} -20 30 0 0 {name=Vm1}
C {devices/lab_pin.sym} -20 -20 2 0 {name=p4 sig_type=std_logic lab=Vds}
C {devices/gnd.sym} 190 200 0 0 {name=l6 lab=GND}
C {devices/gnd.sym} 240 200 0 0 {name=l7 lab=GND}
C {devices/lab_pin.sym} 80 110 0 0 {name=p5 sig_type=std_logic lab=Vgs}
C {devices/ammeter.sym} 190 30 0 0 {name=Vm2}
C {devices/lab_pin.sym} 190 -20 2 0 {name=p6 sig_type=std_logic lab=Vds}
C {sg13g2_pr/sg13_hv_nmos.sym} 170 110 2 1 {name=M2
l=0.35u
w=1.0u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {devices/gnd.sym} 660 200 0 0 {name=l8 lab=GND}
C {devices/gnd.sym} 710 200 0 0 {name=l9 lab=GND}
C {devices/lab_pin.sym} 550 110 0 0 {name=p7 sig_type=std_logic lab=Vgsp}
C {devices/ammeter.sym} 660 30 0 0 {name=Vm3}
C {devices/lab_pin.sym} 660 -20 2 0 {name=p8 sig_type=std_logic lab=Vdsp}
C {devices/gnd.sym} 870 200 0 0 {name=l10 lab=GND}
C {devices/gnd.sym} 920 200 0 0 {name=l11 lab=GND}
C {devices/lab_pin.sym} 760 110 0 0 {name=p9 sig_type=std_logic lab=Vgsp}
C {devices/ammeter.sym} 870 30 0 0 {name=Vm4}
C {devices/lab_pin.sym} 870 -20 2 0 {name=p10 sig_type=std_logic lab=Vdsp}
C {sg13g2_pr/sg13_lv_pmos.sym} 640 110 2 1 {name=M3
l=0.35u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 850 110 2 1 {name=M4
l=0.35u
w=1.0u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/gnd.sym} 390 200 0 0 {name=l12 lab=GND}
C {devices/vsource.sym} 390 150 0 0 {name=Vgs1 value=-0.75}
C {devices/vsource.sym} 390 -30 0 0 {name=Vds2 value=-1.5}
C {devices/gnd.sym} 390 60 0 0 {name=l13 lab=GND}
C {devices/lab_pin.sym} 420 110 2 0 {name=p11 sig_type=std_logic lab=Vgsp}
C {devices/lab_pin.sym} 400 -100 2 0 {name=p12 sig_type=std_logic lab=Vdsp}
