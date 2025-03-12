v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 472.5 50 1272.5 450 {flags=graph


ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1


divx=5
subdivx=4
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=0
logy=0


autoload=0

color= 4
node="Ctot"
y2=3.3e-15
y1=1.3e-15
x1=0
x2=10u}
N -0 75 110 75 {lab=GND}
N 110 272.5 110 280 {lab=GND}
N -0 220 0 272.5 {lab=GND}
N 0 272.5 110 272.5 {lab=GND}
N 40 10 40 105 {lab=#net1}
N 110 240 110 272.5 {lab=GND}
N -155 105 -40 105 {lab=#net2}
N 40 10 170 10 {lab=#net1}
N 110 240 170 240 {lab=GND}
N 110 75 110 240 {lab=GND}
N 170 215 170 240 {lab=GND}
N -155 220 -0 220 {lab=GND}
N -155 192.5 -155 220 {lab=GND}
N -0 135 -0 220 {lab=GND}
N -155 105 -155 140 {lab=#net2}
N 170 10 170 160 {lab=#net1}
C {devices/code_shown.sym} -517.5 382.5 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.lib $::SG13G2_MODELS/cornerMOShv.lib mos_tt
"}
C {devices/code_shown.sym} 202.5 -75 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
tran 1n 10u 100n
let Ctot = -i(v1)/1e6
**write tran_mosvar.raw
write tran_mosvar.raw
.endc
"}
C {devices/launcher.sym} 480 -22.5 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/tran_mosvar.raw tran"
}
C {devices/gnd.sym} 110 280 0 0 {name=l2 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 105 0 0 {name=C1 model=sg13_hv_svaricap W=3.74e-6 L=0.3e-6 Nx=1 spiceprefix=X}
C {devices/vsource.sym} 170 187.5 0 0 {name=V1 value="dc 0 ac 0 pulse(-2.5, 2.5, 0, 10u, 100p, 1u, 11u ) "}
C {devices/vsource.sym} -155 167.5 0 0 {name=V2 value="dc 0 ac 0 pulse(-2.5, 2.5, 0, 10u, 100p, 1u, 11u ) "}
