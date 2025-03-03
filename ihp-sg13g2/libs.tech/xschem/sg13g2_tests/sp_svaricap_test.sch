v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -80 105 -40 105 {lab=#net1}
N 80 -110 80 -90 {lab=#net2}
N -0 -110 80 -110 {lab=#net2}
N -0 -110 0 80 {lab=#net2}
N -0 135 0 235 {lab=GND}
N -80 105 -80 140 {lab=#net1}
N -110 105 -80 105 {lab=#net1}
N -80 200 -80 225 {lab=#net3}
N 70 105 100 105 {lab=#net4}
N 70 105 70 135 {lab=#net4}
N 40 105 70 105 {lab=#net4}
N 70 280 70 320 {lab=GND}
N 160 105 195 105 {lab=#net5}
N -235 105 -235 150 {lab=#net6}
N -235 105 -170 105 {lab=#net6}
N 195 105 195 150 {lab=#net5}
N -235 210 -235 245 {lab=GND}
N 195 210 195 250 {lab=GND}
N 70 195 70 225 {lab=#net7}
N -80 280 -80 310 {lab=GND}
N 80 -35 80 0 {lab=GND}
C {devices/code_shown.sym} -517.5 382.5 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.lib $::SG13G2_MODELS/cornerMOShv.lib mos_tt
"}
C {devices/code_shown.sym} 382.5 -85 0 0 {name=NGSPICE only_toplevel=true 
value="
*.param temp=27
.param Vg=0
.control
save all 
let points=71
set vgsp="$&points"
set scratch=$curplot

let c_diff=vector($vgsp)
let r_diff=vector($vgsp)
let q_diff=vector($vgsp)
let Vg=vector($vgsp)
let ind=0
#let Vgate=vector($vgsp)
while ind<$vgsp
  let v1_act= 0.0+ind*0.1
  *let Vgate=v1_act
  alter Vg1 = v1_act
  print Vg1
  alter Vg2 = v1_act
  sp lin 1 15.8GHz 15.8GHz
  let s11_diff=(s_1_1+s_2_2-s_1_2-s_2_1)/2
  let z11_diff=2*50*(1+s11_diff)/(1-s11_diff)
  let c_diff[ind]=-1/imag(z11_diff)/(2*pi*15.8e9)
  let r_diff[ind]=real(z11_diff)
  let q_diff[ind]=-imag(z11_diff)/real(z11_diff)
  let Vg[ind]=v1_act-3.5
  let ind=ind+1
  destroy sp1
end
setplot $scratch
wrdata sg13_lv_svaricap_cdiff.csv \{$scratch\}.vg \{$scratch\}.c_diff
wrdata sg13_lv_svaricap_qdiff.csv \{$scratch\}.vg \{$scratch\}.q_diff
echo
print \{$scratch\}.vg \{$scratch\}.c_diff


*plot i(v1)
.endc
"}
C {devices/gnd.sym} 0 235 0 0 {name=l2 lab=GND}
C {sg13g2_pr/sg13_svaricap.sym} 0 105 0 0 {name=C1 model=sg13_hv_svaricap W=9.74e-6 L=0.8e-6 Nx=10 spiceprefix=X}
C {devices/vsource.sym} 80 -62.5 0 0 {name=V1 value=3.5}
C {devices/vsource.sym} -80 252.5 0 0 {name=Vg1 value="dc Vg"}
C {devices/gnd.sym} 80 0 0 0 {name=l1 lab=GND}
C {devices/capa-2.sym} -140 105 1 0 {name=C2
value=1m
footprint=1206
device=polarized_capacitor}
C {devices/ind.sym} -80 170 0 0 {name=L3
value=1m
footprint=1206
device=inductor}
C {devices/capa-2.sym} 130 105 3 0 {name=C3
value=1m
footprint=1206
device=polarized_capacitor}
C {devices/ind.sym} 70 165 0 0 {name=L4
value=1m
footprint=1206
device=inductor}
C {devices/vsource.sym} 70 252.5 0 0 {name=Vg2 value=" dc Vg"}
C {devices/gnd.sym} -80 310 0 0 {name=l5 lab=GND}
C {devices/gnd.sym} 70 320 0 0 {name=l6 lab=GND}
C {devices/vsource.sym} -235 180 0 0 {name=V2 value="dc 0 ac 1 portnum 1 z0 50"}
C {devices/vsource.sym} 195 180 0 0 {name=V3 value="dc 0 ac 1 portnum 2 z0 50"}
C {devices/gnd.sym} -235 245 0 0 {name=l7 lab=GND}
C {devices/gnd.sym} 195 250 0 0 {name=l8 lab=GND}
