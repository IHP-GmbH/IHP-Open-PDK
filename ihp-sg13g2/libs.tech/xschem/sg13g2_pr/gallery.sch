v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {HBT Devices} 30 -1720 0 0 0.6 0.6 {}
T {HBT Devices w/  
temperature output} 30 -1620 0 0 0.6 0.6 {}
T {Low voltage 
CMOS devices} 20 -1500 0 0 0.6 0.6 {}
T {High voltage 
CMOS devices} 20 -1370 0 0 0.6 0.6 {}
T {ESD devices} 20 -1230 0 0 0.6 0.6 {}
T {Diodes} 20 -1090 0 0 0.6 0.6 {}
T {Polysilicon 
resistors} 20 -980 0 0 0.6 0.6 {}
T {Tap devices} 20 -820 0 0 0.6 0.6 {}
T {SVaricap} 20 -670 0 0 0.6 0.6 {}
T {Bondpad} 20 -550 0 0 0.6 0.6 {}
T {Isolation box} 20 -390 0 0 0.6 0.6 {}
T {MiM capacitor} 20 -220 0 0 0.6 0.6 {}
T {PNP lateral device} 20 -100 0 0 0.6 0.6 {}
C {sg13g2_pr/bondpad.sym} 400 -520 0 0 {name=X1
model=bondpad
spiceprefix=X
size=80u
shape=0
padtype=0
}
C {sg13g2_pr/cap_cmim.sym} 400 -200 0 0 {name=C1
model=cap_cmim
w=7.0e-6
l=7.0e-6
m=1
spiceprefix=X}
C {sg13g2_pr/cap_rfcmim.sym} 560 -200 0 0 {name=C2 
model=cap_rfcmim
w=10.0e-6
l=10.0e-6
wfeed=5.0e-6
spiceprefix=X}
C {sg13g2_pr/dantenna.sym} 540 -1070 0 0 {name=D1
model=dantenna
l=0.78u
w=0.78u
spiceprefix=X
}
C {sg13g2_pr/diodevdd_2kv.sym} 660 -1200 0 0 {name=D2
model=diodevdd_2kv
m=1
spiceprefix=X
}
C {sg13g2_pr/diodevdd_4kv.sym} 810 -1200 0 0 {name=D3
model=diodevdd_4kv
m=1
spiceprefix=X
}
C {sg13g2_pr/diodevss_2kv.sym} 950 -1200 0 0 {name=D4
model=diodevss_2kv
spiceprefix=X
m=1
}
C {sg13g2_pr/diodevss_4kv.sym} 1090 -1200 0 0 {name=D5
model=diodevss_4kv
spiceprefix=X
m=1
}
C {sg13g2_pr/dpantenna.sym} 400 -1070 0 0 {name=D6
model=dpantenna
l=0.78u
w=0.78u
spiceprefix=X
}
C {sg13g2_pr/nmoscl_2.sym} 400 -1200 0 0 {name=D7
model=nmoscl_2
m=1
spiceprefix=X
}
C {sg13g2_pr/nmoscl_4.sym} 540 -1200 0 0 {name=D8
model=nmoscl_4
m=1
spiceprefix=X
}
C {sg13g2_pr/npn13G2.sym} 390 -1710 0 0 {name=Q1
model=npn13G2
spiceprefix=X
Nx=1
}
C {sg13g2_pr/npn13G2l.sym} 560 -1710 0 0 {name=Q2
model=npn13G2l
spiceprefix=X
Nx=1
El=1.0
}
C {sg13g2_pr/npn13G2v.sym} 720 -1710 0 0 {name=Q3
model=npn13G2v
spiceprefix=X
Nx=1
El=1
}
C {sg13g2_pr/ntap1.sym} 400 -800 0 0 {name=R1
model=ntap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {sg13g2_pr/ptap1.sym} 540 -800 0 0 {name=R2
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {sg13g2_pr/rhigh.sym} 390 -950 0 0 {name=R3
w=0.5e-6
l=0.5e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rppd.sym} 550 -950 0 0 {name=R4
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rsil.sym} 710 -950 0 0 {name=R5
w=0.5e-6
l=0.5e-6
model=rsil
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/sg13_hv_nmos.sym} 380 -1330 0 0 {name=M1
l=0.45u
w=0.3u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 530 -1330 0 0 {name=M2
l=0.4u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_rf_nmos.sym} 690 -1330 0 0 {name=M3
l=0.72u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_rf_pmos.sym} 840 -1330 0 0 {name=M4
l=0.72u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 380 -1450 0 0 {name=M5
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 530 -1450 0 0 {name=M6
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_rf_nmos.sym} 690 -1450 0 0 {name=M7
l=0.72u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_rf_pmos.sym} 840 -1450 0 0 {name=M8
l=0.72u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_svaricap.sym} 400 -650 0 0 {name=C3 model=sg13_hv_svaricap W=7.0e-6 L=0.3e-6 Nx=1 spiceprefix=X}
C {sg13g2_pr/isolbox.sym} 400 -360 0 0 {name=D9
model=isolbox
l=3.0u
w=3.0u
spiceprefix=X
}
C {sg13g2_pr/sub.sym} 680 -800 0 0 {name=l1 lab=sub!}
C {title-3.sym} 0 0 0 0 {name=l2 author="IHP Open PDK Authors 2025" title="Device gallery" rev=1.0 lock=true}
C {sg13g2_pr/npn13G2_5t.sym} 390 -1580 0 0 {name=Q4
model=npn13G2_5t
spiceprefix=X
Nx=1
}
C {sg13g2_pr/npn13G2l_5t.sym} 560 -1580 0 0 {name=Q5
model=npn13G2l_5t
spiceprefix=X
Nx=1 
El=2.5
}
C {sg13g2_pr/npn13G2v_5t.sym} 720 -1580 0 0 {name=Q6
model=npn13G2v_5t
spiceprefix=X
Nx=1
El=1
drc=hbt_drc}
C {sg13g2_pr/pnpMPA.sym} 390 -80 0 0 {name=Q7
model=pnpMPA
spiceprefix=X
w=1.0e-6
l=2.0e-6
m=1
}
C {sg13g2_pr/schottky_nbl1.sym} 680 -1070 0 0 {name=D10
model=schottky_nbl1
Nx=1
Ny=1
spiceprefix=X
}
