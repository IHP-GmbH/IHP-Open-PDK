v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Low voltage
CMOS devices} 40 -1690 0 0 0.6 0.6 {}
T {High voltage
CMOS devices} 40 -1560 0 0 0.6 0.6 {}
T {ESD devices} 40 -1420 0 0 0.6 0.6 {}
T {Diodes} 40 -1280 0 0 0.6 0.6 {}
T {Polysilicon
resistors} 40 -1170 0 0 0.6 0.6 {}
T {Tap devices} 40 -1010 0 0 0.6 0.6 {}
T {SVaricap} 40 -860 0 0 0.6 0.6 {}
T {Bondpad} 40 -740 0 0 0.6 0.6 {}
C {sg13g2_pr/sg13_lv_nmos.sym} 380 -1640 0 0 {name=M5
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 530 -1640 0 0 {name=M6
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_rf_nmos.sym} 690 -1640 0 0 {name=M7
l=0.72u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_rf_pmos.sym} 840 -1640 0 0 {name=M8
l=0.72u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_nmos.sym} 380 -1510 0 0 {name=M1
l=0.45u
w=0.3u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 530 -1510 0 0 {name=M2
l=0.4u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_rf_nmos.sym} 690 -1510 0 0 {name=M3
l=0.72u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_rf_pmos.sym} 840 -1510 0 0 {name=M4
l=0.72u
w=1.0u
ng=1
m=1
rfmode=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/nmoscl_2.sym} 400 -1390 0 0 {name=D7
model=nmoscl_2
m=1
spiceprefix=X
}
C {sg13g2_pr/nmoscl_4.sym} 540 -1390 0 0 {name=D8
model=nmoscl_4
m=1
spiceprefix=X
}
C {sg13g2_pr/diodevdd_2kv.sym} 660 -1390 0 0 {name=D2
model=diodevdd_2kv
m=1
spiceprefix=X
}
C {sg13g2_pr/diodevdd_4kv.sym} 810 -1390 0 0 {name=D3
model=diodevdd_4kv
m=1
spiceprefix=X
}
C {sg13g2_pr/diodevss_2kv.sym} 950 -1390 0 0 {name=D4
model=diodevss_2kv
spiceprefix=X
m=1
}
C {sg13g2_pr/diodevss_4kv.sym} 1090 -1390 0 0 {name=D5
model=diodevss_4kv
spiceprefix=X
m=1
}
C {sg13g2_pr/dpantenna.sym} 400 -1260 0 0 {name=D6
model=dpantenna
l=0.78u
w=0.78u
spiceprefix=X
}
C {sg13g2_pr/dantenna.sym} 540 -1260 0 0 {name=D1
model=dantenna
l=0.78u
w=0.78u
spiceprefix=X
}
C {sg13g2_pr/rhigh.sym} 390 -1140 0 0 {name=R3
w=0.5e-6
l=0.5e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rppd.sym} 550 -1140 0 0 {name=R4
w=0.5e-6
l=0.5e-6
model=rppd
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rsil.sym} 710 -1140 0 0 {name=R5
w=0.5e-6
l=0.5e-6
model=rsil
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/ntap1.sym} 400 -990 0 0 {name=R1
model=ntap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {sg13g2_pr/ptap1.sym} 540 -990 0 0 {name=R2
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {sg13g2_pr/sub.sym} 680 -990 0 0 {name=l1 lab=sub!}
C {sg13g2_pr/sg13_svaricap.sym} 400 -840 0 0 {name=C3 model=sg13_hv_svaricap W=7.0e-6 L=0.3e-6 Nx=1 spiceprefix=X}
C {sg13g2_pr/bondpad.sym} 400 -710 0 0 {name=X1
model=bondpad
spiceprefix=X
size=80u
shape=0
padtype=0
}
C {title-3.sym} 0 0 0 0 {name=l2 author="IHP Open PDK Authors 2025" title="Device gallery" rev=1.0 lock=true}
