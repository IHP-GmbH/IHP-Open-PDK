v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 110 -370 190 -370 {}
N 360 -210 360 -240 {}
N 280 -210 360 -210 {}
N 190 40 190 -370 {}
N 360 10 360 -110 {}
N 240 -110 360 -110 {}
N 280 10 360 10 {}
N 360 40 360 10 {}
N 280 -270 280 -370 {}
N 360 170 360 40 {}
N 360 -240 360 -370 {}
N 240 -110 240 -240 {}
N 280 -240 360 -240 {}
N 280 170 360 170 {}
N 190 -370 280 -370 {}
N 110 170 280 170 {}
N 280 170 280 70 {}
N 190 40 240 40 {}
N 280 40 360 40 {}
N 280 -370 360 -370 {}
C {devices/iopin.sym} 110 -370 2 0 {name=p1 lab=VDD}
C {devices/iopin.sym} 110 170 2 0 {name=p2 lab=VSS}
C {sg13_lv_nmos.sym} 260 40 0 0 {name=M1 w=420.00n l=1.000u ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} 260 -240 0 0 {name=M2 w=1.000u l=1.000u ng=1 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -1010 780 0 0 {name=l1 author="IHP PDK AUTHORS"}
