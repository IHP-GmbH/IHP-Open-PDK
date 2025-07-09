v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 -130 -610 670 -210 {flags=graph

y2=0.076
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=-40
x2=125
divx=5
subdivx=1

dataset=-1
unitx=1
logx=0
logy=0


y1=0.00058
rainbow=0
color="4 7 8"
node="i(vrh)
i(vppd)
i(vsil)"}
N -140 30 -140 90 {
lab=GND}
N -140 -110 -140 -30 {
lab=Vcc}
N -140 -110 90 -110 {
lab=Vcc}
N 90 -110 90 -70 {
lab=Vcc}
N 90 -10 90 10 {
lab=#net1}
N 90 70 90 90 {
lab=GND}
N 240 -110 240 -70 {
lab=Vcc}
N 240 -10 240 10 {
lab=#net2}
N 240 70 240 90 {
lab=GND}
N 420 -110 420 -70 {
lab=Vcc}
N 420 -10 420 10 {
lab=#net3}
N 420 70 420 90 {
lab=GND}
N 90 -110 240 -110 {
lab=Vcc}
N 240 -110 420 -110 {
lab=Vcc}
C {devices/code_shown.sym} -310 180 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerRES.lib res_typ_stat
"}
C {devices/code_shown.sym} 570 -100 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
op
echo Silicide resisotr value: 
print Vcc/I(Vsil)
echo Unsilicide poly resisotr value: 
print Vcc/I(Vppd)
echo High poly resisotr value: 
print Vcc/I(Vrh)
reset 
dc temp -40 125 1 
write dc_res_temp.raw
wrdata dc_res_temp.csv I(Vsil) I(Vppd) I(Vrh)
.endc
"}
C {devices/gnd.sym} 90 90 0 0 {name=l1 lab=GND}
C {devices/vsource.sym} -140 0 0 0 {name=Vres value=1.5}
C {devices/gnd.sym} -140 90 0 0 {name=l3 lab=GND}
C {devices/title.sym} -130 260 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} -70 -170 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/dc_res_temp.raw dc"
}
C {devices/lab_pin.sym} -140 -60 2 0 {name=p1 sig_type=std_logic lab=Vcc}
C {devices/ammeter.sym} 90 -40 0 0 {name=Vsil}
C {devices/gnd.sym} 240 90 0 0 {name=l2 lab=GND}
C {devices/ammeter.sym} 240 -40 0 0 {name=Vppd}
C {devices/gnd.sym} 420 90 0 0 {name=l4 lab=GND}
C {devices/ammeter.sym} 420 -40 0 0 {name=Vrh}
C {sg13g2_pr/rsil.sym} 90 40 0 0 {name=R1
w=0.5e-6
l=0.5e-6
model=rsil
body=sub!
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/sub.sym} -30 90 0 0 {name=l6 lab=sub!}
C {sg13g2_pr/ptap1.sym} -30 60 0 0 {name=R4
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {devices/gnd.sym} -30 30 2 0 {name=l7 lab=GND}
C {sg13g2_pr/rppd.sym} 240 40 0 0 {name=R2
w=0.5e-6
l=0.5e-6
model=rppd
body=sub!
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rhigh.sym} 420 40 0 0 {name=R3
w=0.5e-6
l=0.5e-6
model=rhigh
body=sub!
spiceprefix=X
b=0
m=1
}
