v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -480 -100 -480 -60 {
lab=vptap}
N -370 -100 -370 -60 {
lab=vptap}
N -480 -100 -370 -100 {
lab=vptap}
N -370 -120 -370 -100 {
lab=vptap}
N 170 -100 170 -70 {
lab=pguard}
N 0 -20 0 -10 {
lab=!sub}
N -0 -100 -0 -80 {
lab=#net1}
N 330 -30 330 -10 {
lab=GND}
N 330 -100 330 -90 {
lab=#net2}
N 330 -100 370 -100 {
lab=#net2}
N 430 -100 480 -100 {
lab=nguard}
N 480 -100 480 -70 {
lab=nguard}
N 480 -120 480 -100 {
lab=nguard}
N -250 -100 -250 -60 {
lab=vntap}
N -140 -100 -140 -60 {
lab=vntap}
N -250 -100 -140 -100 {
lab=vntap}
N -140 -120 -140 -100 {
lab=vntap}
N 0 -100 50 -100 {
lab=#net1}
N 110 -100 170 -100 {
lab=pguard}
N 170 -130 170 -100 {
lab=pguard}
N 10 120 70 120 {
lab=!sub}
N -80 120 -50 120 {
lab=GND}
C {devices/code_shown.sym} -530 -310 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control
save all 
op
print all
.endc
"}
C {devices/code_shown.sym} -330 -350 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
"}
C {isource.sym} -480 -30 2 0 {name=I0 value=1}
C {lab_wire.sym} -370 -120 0 0 {name=p1 sig_type=std_logic lab=vptap}
C {sg13g2_pr/ptap1.sym} -370 -30 0 0 {name=R2
model=ptap1
spiceprefix=X
w=20.0e-6
l=20.0e-6
}
C {ammeter.sym} 80 -100 3 1 {name=Vmeas savecurrent=true spice_ignore=0}
C {isource.sym} 0 -50 2 1 {name=I1 value=1}
C {lab_wire.sym} 170 -130 0 1 {name=p2 sig_type=std_logic lab=pguard}
C {ammeter.sym} 400 -100 3 1 {name=Vmeas1 savecurrent=true spice_ignore=0}
C {isource.sym} 330 -60 2 0 {name=I2 value=1}
C {lab_wire.sym} 480 -120 0 0 {name=p3 sig_type=std_logic lab=nguard}
C {gnd.sym} 480 -10 0 0 {name=l2 lab=GND}
C {gnd.sym} 330 -10 0 0 {name=l3 lab=GND}
C {sg13g2_pr/pgring.sym} 170 -40 0 0 {name=Rp1
model=pgring
spiceprefix=X
a=20.0e-6
b=20.0e-6
}
C {sg13g2_pr/ngring.sym} 480 -40 0 0 {name=Rn1
model=ngring
spiceprefix=X
a=20.0e-6
b=20.0e-6
}
C {isource.sym} -250 -30 2 0 {name=I3 value=1}
C {lab_wire.sym} -140 -120 0 0 {name=p4 sig_type=std_logic lab=vntap}
C {gnd.sym} -140 0 0 0 {name=l7 lab=GND}
C {gnd.sym} -250 0 0 0 {name=l8 lab=GND}
C {sg13g2_pr/ntap1.sym} -140 -30 0 0 {name=R1
model=ntap1
spiceprefix=X
w=1.0e-6
l=1.0e-6
}
C {sg13g2_pr/sub.sym} 0 -10 0 0 {name=l1 lab=!sub}
C {sg13g2_pr/sub.sym} 170 -10 0 0 {name=l6 lab=!sub}
C {gnd.sym} -80 120 0 0 {name=l9 lab=GND}
C {sg13g2_pr/sub.sym} 70 120 0 0 {name=l10 lab=!sub}
C {res.sym} -20 120 1 0 {name=R3
value=10
footprint=1206
device=resistor
m=1}
C {sg13g2_pr/sub.sym} -480 0 0 0 {name=l4 lab=!sub}
C {sg13g2_pr/sub.sym} -370 0 0 0 {name=l5 lab=!sub}
