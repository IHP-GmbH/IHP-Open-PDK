v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
B 2 140 -850 940 -450 {flags=graph
y1=0.021
y2=0.13
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=4
x2=8
divx=5
subdivx=8
xlabmag=1.0
ylabmag=1.0
node=vc
color=4
dataset=-1
unitx=1
logx=1
logy=0
}
T {Nx - number of emitters} 400 -200 0 0 0.2 0.2 {}
N 180 -250 180 -230 {
lab=GND}
N 180 -320 180 -310 {
lab=#net1}
N 440 -290 440 -230 {
lab=GND}
N 570 -290 570 -230 {
lab=GND}
N 440 -390 440 -350 {
lab=Vc}
N 570 -390 570 -350 {
lab=#net2}
N 440 -320 490 -320 {
lab=GND}
N 490 -320 490 -230 {
lab=GND}
N 440 -390 470 -390 {
lab=Vc}
N 530 -390 570 -390 {
lab=#net2}
N 390 -320 400 -320 {
lab=Vb}
N 180 -320 200 -320 {
lab=#net1}
N 420 -390 440 -390 {
lab=Vc}
N 200 -320 250 -320 {
lab=#net1}
N 310 -320 390 -320 {
lab=Vb}
N 360 -350 360 -320 {
lab=Vb}
C {devices/code_shown.sym} 100 -150 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
*.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ_stat
.lib $::SG13G2_MODELS/cornerHBT.lib hbt_typ
"}
C {devices/code_shown.sym} 710 -380 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control 
save all
op
print Vc Vb I(Vce)
ac dec 10 10k 100meg 
meas ac vnom_at FIND Vc AT=100k 
let v3db = vnom_at*0.707
meas ac freq_at when Vc=v3db
write ac_hbt_13g2.raw
.endc
"}
C {devices/gnd.sym} 440 -230 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} 180 -230 0 0 {name=l2 lab=GND}
C {devices/vsource.sym} 570 -320 0 0 {name=Vce value=5}
C {devices/gnd.sym} 570 -230 0 0 {name=l3 lab=GND}
C {devices/gnd.sym} 490 -230 0 0 {name=l4 lab=GND}
C {devices/title.sym} 170 -50 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {sg13g2_pr/npn13G2.sym} 420 -320 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1}
C {devices/res.sym} 500 -390 1 0 {name=R1
value=40k
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 420 -390 0 0 {name=p1 sig_type=std_logic lab=Vc}
C {devices/vsource.sym} 180 -280 0 0 {name=Vce1 value="dc 0.8 ac 1m"}
C {devices/res.sym} 280 -320 1 0 {name=R2
value=33k
footprint=1206
device=resistor
m=1}
C {devices/lab_pin.sym} 360 -350 0 0 {name=p2 sig_type=std_logic lab=Vb}
C {devices/launcher.sym} 160 -400 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/ac_hbt_13g2.raw ac"
}
