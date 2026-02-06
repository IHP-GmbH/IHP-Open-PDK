v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 1030 -1700 1830 -1300 {flags=graph
y1=-11

ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-0.02
x2=0.02
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0


y2=0.65
color=4
node=vin1}
B 2 1020 -1280 1820 -880 {flags=graph
y1=0.28

ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-0.02
x2=0.02
divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0
color=10
node=vin2
y2=0.29}
N 560 -930 560 -910 {
lab=GND}
N 560 -1050 560 -990 {
lab=Vin1}
N 670 -920 670 -910 {
lab=GND}
N 670 -990 670 -980 {
lab=#net1}
N 670 -1060 670 -1050 {
lab=Vin1}
N 850 -930 850 -910 {
lab=GND}
N 850 -1050 850 -990 {
lab=Vin2}
N 940 -920 940 -910 {
lab=GND}
N 940 -990 940 -980 {
lab=#net2}
N 940 -1060 940 -1050 {
lab=Vin2}
C {devices/gnd.sym} 560 -910 0 0 {name=l2 lab=GND}
C {devices/code_shown.sym} 30 -1700 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
"}
C {devices/code_shown.sym} 40 -1570 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
dc I0 -20m 20m 10u
*dc I1 -20m 20m 10u

echo ---------nmoscl_2---------
meas dc Vf FIND v(Vin1) AT=0.01
meas dc Vr FIND v(Vin1) AT=-0.01

echo ---------nmoscl_4---------
*meas dc Vf FIND v(Vin2) AT=0.01
*meas dc Vr FIND v(Vin2) AT=-0.01

write dc_esd_nmos_cl.raw
.endc
"}
C {devices/launcher.sym} 1090 -840 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_esd_nmos_cl.raw dc"
}
C {title-3.sym} 0 0 0 0 {name=l3 author="IHP PDK Authors" rev=1.0 lock=true}
C {lab_pin.sym} 560 -1050 1 0 {name=p1 sig_type=std_logic lab=Vin1}
C {devices/gnd.sym} 670 -910 0 0 {name=l9 lab=GND}
C {devices/ammeter.sym} 670 -1020 0 0 {name=Vmda1}
C {lab_pin.sym} 670 -1060 1 0 {name=p8 sig_type=std_logic lab=Vin1}
C {isource.sym} 560 -960 2 0 {name=I0 value=1m}
C {devices/gnd.sym} 850 -910 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 850 -1050 1 0 {name=p2 sig_type=std_logic lab=Vin2}
C {devices/gnd.sym} 940 -910 0 0 {name=l4 lab=GND}
C {devices/ammeter.sym} 940 -1020 0 0 {name=Vmda2}
C {lab_pin.sym} 940 -1060 1 0 {name=p3 sig_type=std_logic lab=Vin2}
C {isource.sym} 850 -960 2 0 {name=I1 value=1m}
C {sg13g2_pr/nmoscl_2.sym} 670 -950 2 0 {name=D1
model=nmoscl_2
m=1
spiceprefix=X
}
C {sg13g2_pr/nmoscl_4.sym} 940 -950 2 0 {name=D2
model=nmoscl_4
m=1
spiceprefix=X
}
