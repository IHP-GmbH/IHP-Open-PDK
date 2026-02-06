v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 410 -590 1210 -190 {flags=graph
y1=-1.2
y2=11
ypos1=0
ypos2=2
divy=1
subdivy=4
unity=1
x1=-0.001
x2=0.001
divx=1
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0

hilight_wave=0
color=4
node=net1
linewidth_mult=1.0}
N 40 -210 40 -190 {
lab=GND}
N 40 -350 40 -270 {
lab=#net1}
N 40 -350 200 -350 {
lab=#net1}
N 200 -350 200 -290 {
lab=#net1}
N 200 -230 200 -190 {lab=GND}
N 210 -250 280 -250 {lab=sub!}
N 280 -250 280 -190 {lab=sub!}
N 60 -130 90 -130 {lab=GND}
N 60 -130 60 -120 {lab=GND}
N 150 -130 180 -130 {lab=sub!}
N 180 -130 180 -120 {lab=sub!}
C {devices/gnd.sym} 40 -190 0 0 {name=l2 lab=GND}
C {devices/code_shown.sym} 0 -700 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerDIO.lib dio_tt
"}
C {devices/code_shown.sym} 0 -600 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 

dc I0 -1m 1m 1u
echo Evaluating breakdown voltages:
meas dc vbk_pos find v(net1) at=10u
meas dc vbk_neg find v(net1) at=-10u
write dc_schottky.raw

.endc
"}
C {devices/title.sym} 160 -40 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 490 -150 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/dc_schottky.raw dc"
}
C {isource.sym} 40 -240 2 0 {name=I0 value=1m}
C {devices/gnd.sym} 200 -190 0 0 {name=l1 lab=GND}
C {sg13g2_pr/schottky_nbl1.sym} 200 -260 0 0 {name=D1
model=schottky_nbl1
Nx=1
Ny=1
spiceprefix=X
}
C {sg13g2_pr/sub.sym} 280 -190 0 0 {name=l3 lab=sub!}
C {vsource.sym} 120 -130 1 0 {name=V1 value=0 savecurrent=false}
C {devices/gnd.sym} 60 -120 0 0 {name=l4 lab=GND}
C {sg13g2_pr/sub.sym} 180 -120 0 0 {name=l6 lab=sub!}
