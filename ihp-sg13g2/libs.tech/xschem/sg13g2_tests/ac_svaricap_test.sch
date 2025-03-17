v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 257.5 295 1057.5 695 {flags=graph


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
y2=1.2e-13
y1=1e-13
x1=1e+09
x2=1e+11}
N -80 105 -40 105 {lab=#net1}
N -340 115 -340 150 {lab=#net2}
N -340 210 -340 235 {lab=#net3}
N 110 585 110 630 {lab=#net4}
N 110 690 110 730 {lab=GND}
N -0 130 -0 170 {lab=GND}
N 0 -20 0 20 {lab=GND}
N 0 -160 0 -120 {lab=GND}
N -80 255 -40 255 {lab=#net1}
N 0 280 0 320 {lab=GND}
N -80 415 -40 415 {lab=#net1}
N 0 440 0 480 {lab=GND}
N -80 585 -40 585 {lab=#net1}
N 0 610 0 650 {lab=GND}
N -80 -335 -40 -335 {lab=#net1}
N 0 -310 0 -270 {lab=GND}
N -80 415 -80 585 {lab=#net1}
N -80 -45 -80 105 {lab=#net1}
N -80 105 -80 255 {lab=#net1}
N -80 255 -80 415 {lab=#net1}
N 40 -335 110 -335 {lab=#net4}
N 40 585 110 585 {lab=#net4}
N 110 415 110 585 {lab=#net4}
N 40 -185 110 -185 {lab=#net4}
N 110 -335 110 -185 {lab=#net4}
N 40 -45 110 -45 {lab=#net4}
N 110 -185 110 -45 {lab=#net4}
N -80 -185 -40 -185 {lab=#net1}
N -80 -335 -80 -185 {lab=#net1}
N -80 -45 -40 -45 {lab=#net1}
N -80 -185 -80 -45 {lab=#net1}
N 40 105 110 105 {lab=#net4}
N 110 -45 110 105 {lab=#net4}
N 40 255 110 255 {lab=#net4}
N 110 105 110 255 {lab=#net4}
N 40 415 110 415 {lab=#net4}
N 110 255 110 415 {lab=#net4}
N -225 -365 -0 -365 {lab=#net2}
N -225 -215 0 -215 {lab=#net2}
N -135 75 0 75 {lab=#net2}
N -135 225 -0 225 {lab=#net2}
N -135 75 -135 225 {lab=#net2}
N -225 75 -135 75 {lab=#net2}
N -140 385 0 385 {lab=#net2}
N -140 555 -0 555 {lab=#net2}
N -140 385 -140 555 {lab=#net2}
N -225 385 -140 385 {lab=#net2}
N -80 585 -80 630 {lab=#net1}
N -80 690 -80 730 {lab=GND}
N -225 -365 -225 -215 {lab=#net2}
N -225 -75 -225 75 {lab=#net2}
N -225 115 -225 385 {lab=#net2}
N -225 -75 -0 -75 {lab=#net2}
N -225 -215 -225 -75 {lab=#net2}
N -340 115 -225 115 {lab=#net2}
N -225 75 -225 115 {lab=#net2}
N -340 290 -340 365 {lab=GND}
C {devices/code_shown.sym} -797.5 487.5 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.lib $::SG13G2_MODELS/cornerMOShv.lib mos_tt
"}
C {devices/code_shown.sym} 202.5 -75 0 0 {name=NGSPICE only_toplevel=true 
value="
*.param temp=27
.control
save all 

ac lin 100 1GHz 100GHz
let I1=(i(V3))
let Ctot=imag(I1)/(2*3.1415*frequency)
let Q=real(I1)

write ac_mosvar.raw
*plot i(v1)
.endc
"}
C {devices/launcher.sym} 480 -12.5 0 0 {name=h5
descr="Load IV curve" 
tclcommand="xschem raw_read $netlist_dir/ac_mosvar.raw ac"
}
C {devices/gnd.sym} 0 165 0 0 {name=l2 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 105 0 0 {name=C1 model=sg13_hv_svaricap W=3.74e-6 L=0.3e-6 Nx=5 spiceprefix=X}
C {devices/vsource.sym} -340 262.5 0 0 {name=V1 value="dc 1 ac 0"}
C {devices/ind.sym} -340 180 0 0 {name=L3
value=1m
footprint=1206
device=inductor}
C {devices/gnd.sym} -340 365 0 0 {name=l5 lab=GND}
C {devices/vsource.sym} 110 660 0 0 {name=V3 value="dc 0 ac 0"}
C {devices/gnd.sym} 110 730 0 0 {name=l8 lab=GND}
C {devices/gnd.sym} 0 15 0 0 {name=l1 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 -45 0 0 {name=C2 model=sg13_hv_svaricap W=3.74e-6 L=0.3e-6 Nx=10 spiceprefix=X}
C {devices/gnd.sym} 0 -125 0 0 {name=l4 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 -185 0 0 {name=C3 model=sg13_hv_svaricap W=3.74e-6 L=0.3e-6 Nx=10 spiceprefix=X}
C {devices/gnd.sym} 0 315 0 0 {name=l6 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 255 0 0 {name=C4 model=sg13_hv_svaricap W=3.74e-6 L=0.3e-6 Nx=5 spiceprefix=X}
C {devices/gnd.sym} 0 475 0 0 {name=l7 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 415 0 0 {name=C5 model=sg13_hv_svaricap W=3.74e-6 L=0.3e-6 Nx=5 spiceprefix=X}
C {devices/gnd.sym} 0 645 0 0 {name=l9 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 585 0 0 {name=C6 model=sg13_hv_svaricap W=3.74e-6 L=0.3e-6 Nx=5 spiceprefix=X}
C {devices/gnd.sym} 0 -275 0 0 {name=l10 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 -335 0 0 {name=C7 model=sg13_hv_svaricap W=3.74e-6 L=0.3e-6 Nx=10 spiceprefix=X}
C {devices/vsource.sym} -80 660 0 0 {name=V2 value="dc 0 ac 1"}
C {devices/gnd.sym} -80 730 0 0 {name=l11 lab=GND}
