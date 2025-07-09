v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 1130 -1380 1930 -980 {flags=graph
y1=-470

ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-15.9602
x2=7.7388
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0
color="8 4"
node="i(Vmda)
i(vmda1)"
y2=94}
N 570 -1040 570 -1020 {
lab=GND}
N 570 -1160 570 -1100 {
lab=Vin}
N 680 -1350 710 -1350 {
lab=Vin}
N 710 -1210 710 -1200 {
lab=GND}
N 710 -1280 710 -1270 {
lab=#net1}
N 710 -1350 710 -1340 {
lab=Vin}
N 630 -1350 630 -1330 {
lab=Vin}
N 630 -1270 630 -1240 {
lab=#net2}
N 630 -1240 680 -1240 {
lab=#net2}
N 680 -1360 680 -1350 {lab=Vin}
N 630 -1350 680 -1350 {
lab=Vin}
N 910 -1350 940 -1350 {
lab=Vin}
N 940 -1210 940 -1200 {
lab=GND}
N 940 -1280 940 -1270 {
lab=#net3}
N 940 -1350 940 -1340 {
lab=Vin}
N 860 -1350 860 -1330 {
lab=Vin}
N 860 -1270 860 -1240 {
lab=#net4}
N 860 -1240 910 -1240 {
lab=#net4}
N 910 -1360 910 -1350 {lab=Vin}
N 860 -1350 910 -1350 {
lab=Vin}
N 630 -840 630 -820 {lab=GND}
N 710 -1030 710 -980 {lab=Vin}
N 940 -1030 940 -980 {lab=Vin}
N 710 -1030 940 -1030 {lab=Vin}
N 710 -1070 710 -1030 {lab=Vin}
N 860 -950 910 -950 {lab=#net5}
N 860 -950 860 -880 {lab=#net5}
N 940 -920 940 -880 {lab=#net6}
N 710 -920 710 -880 {lab=#net7}
N 630 -950 680 -950 {lab=#net8}
N 630 -950 630 -900 {lab=#net8}
N 800 -820 800 -800 {lab=GND}
N 630 -820 800 -820 {lab=GND}
N 800 -820 940 -820 {lab=GND}
C {devices/gnd.sym} 570 -1020 0 0 {name=l2 lab=GND}
C {devices/code_shown.sym} 30 -1700 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.include sg13g2_esd.lib
"}
C {devices/code_shown.sym} 30 -1590 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
dc V1 -20.7 3 1m
echo "---------diodevdd_2kv---------"
echo "pad"
meas dc Vf WHEN i(Vmda)=0.01
meas dc Vr WHEN i(Vmda)=-0.01
echo "substrate"
meas dc Vf WHEN i(Vmda1)=0.01
meas dc Vr WHEN i(Vmda1)=-0.01

echo "---------diodevdd_4kv---------"
echo "pad"
meas dc Vf WHEN i(Vmda2)=0.01
meas dc Vr WHEN i(Vmda2)=-0.01
echo "substrate"
meas dc Vf WHEN i(Vmda3)=0.01
meas dc Vr WHEN i(Vmda4)=-0.01



echo "---------diodevss_2kv---------"
echo "pad"
meas dc Vf WHEN i(Vmda6)=0.01
meas dc Vr WHEN i(Vmda6)=-0.01
echo "substrate"
meas dc Vf WHEN i(Vmda7)=0.01
meas dc Vr WHEN i(Vmda7)=-0.01

echo "---------diodevss_4kv---------"
echo "pad"
meas dc Vf WHEN i(Vmda8)=0.01
meas dc Vr WHEN i(Vmda8)=-0.01
echo "substrate"
meas dc Vf WHEN i(Vmda9)=0.01
meas dc Vr WHEN i(Vmda9)=-0.01


write dc_esd.raw
.endc
"}
C {devices/launcher.sym} 1190 -910 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_esd.raw dc"
}
C {devices/gnd.sym} 710 -1200 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} 570 -1070 0 0 {name=V1 value=0.7}
C {devices/ammeter.sym} 710 -1310 0 0 {name=Vmda}
C {devices/ammeter.sym} 630 -1300 0 0 {name=Vmda1}
C {title-3.sym} 0 0 0 0 {name=l3 author="IHP PDK Authors" rev=1.0 lock=true}
C {sg13g2_pr/diodevdd_2kv.sym} 710 -1240 2 1 {name=D1
model=diodevdd_2kv
m=1
spiceprefix=X
}
C {lab_pin.sym} 570 -1160 1 0 {name=p1 sig_type=std_logic lab=Vin}
C {lab_pin.sym} 680 -1360 1 0 {name=p2 sig_type=std_logic lab=Vin}
C {devices/gnd.sym} 940 -1200 0 0 {name=l4 lab=GND}
C {devices/ammeter.sym} 940 -1310 0 0 {name=Vmda2}
C {devices/ammeter.sym} 860 -1300 0 0 {name=Vmda3}
C {sg13g2_pr/diodevdd_2kv.sym} 940 -1240 2 1 {name=D2
model=diodevdd_4kv
m=1
spiceprefix=X
}
C {lab_pin.sym} 910 -1360 1 0 {name=p3 sig_type=std_logic lab=Vin}
C {devices/ammeter.sym} 710 -850 0 0 {name=Vmda6}
C {devices/ammeter.sym} 630 -870 0 0 {name=Vmda7}
C {lab_pin.sym} 710 -1070 1 0 {name=p5 sig_type=std_logic lab=Vin}
C {sg13g2_pr/diodevss_2kv.sym} 710 -950 2 1 {name=D4
model=diodevss_2kv
spiceprefix=X
m=1
}
C {devices/gnd.sym} 800 -800 0 0 {name=l7 lab=GND}
C {devices/ammeter.sym} 940 -850 0 0 {name=Vmda8}
C {devices/ammeter.sym} 860 -850 0 0 {name=Vmda9}
C {sg13g2_pr/diodevss_2kv.sym} 940 -950 2 1 {name=D5
model=diodevss_4kv
spiceprefix=X
m=1
}
