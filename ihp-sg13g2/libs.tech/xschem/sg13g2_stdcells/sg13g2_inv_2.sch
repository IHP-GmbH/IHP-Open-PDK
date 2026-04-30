v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -350 -810 -280 -810 {}
N -350 -1080 -350 -1100 {}
N -440 -810 -390 -810 {}
N -350 -470 -350 -520 {}
N -350 -1050 -330 -1050 {}
N -470 -470 -350 -470 {}
N -350 -550 -330 -550 {}
N -390 -550 -390 -810 {}
N -330 -1050 -330 -1100 {}
N -330 -470 -330 -550 {}
N -350 -1100 -330 -1100 {}
N -350 -580 -350 -810 {}
N -470 -1100 -350 -1100 {}
N -350 -810 -350 -1020 {}
N -390 -810 -390 -1050 {}
N -350 -470 -330 -470 {}
C {devices/opin.sym} -280 -810 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} -440 -810 0 0 {name=p2 lab=A}
C {devices/iopin.sym} -470 -1100 2 0 {name=p3 lab=VDD}
C {devices/iopin.sym} -470 -470 2 0 {name=p4 lab=VSS}
C {sg13_lv_nmos.sym} -370 -550 0 0 {name=M1 w=1.48u l=130.00n ng=2 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} -370 -1050 0 0 {name=M2 w=2.24u l=130.00n ng=2 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -1630 100 0 0 {name=l1 author="IHP PDK AUTHORS"}
