v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 170 -160 250 -160 {}
N 170 -480 250 -480 {}
N 250 -480 250 -510 {}
N 80 -160 80 -580 {}
N 250 -160 250 -190 {}
N 170 -510 250 -510 {}
N 0 -90 170 -90 {}
N 80 -580 170 -580 {}
N 0 -580 80 -580 {}
N 250 -510 250 -580 {}
N 170 -540 170 -580 {}
N 250 -90 250 -160 {}
N 170 -90 170 -130 {}
N 130 -340 130 -510 {}
N 250 -190 250 -340 {}
N 80 -160 130 -160 {}
N 170 -90 250 -90 {}
N 130 -340 250 -340 {}
N 170 -580 250 -580 {}
N 170 -190 250 -190 {}
C {devices/iopin.sym} 0 -580 2 0 {name=p1 lab=VDD}
C {devices/iopin.sym} 0 -90 2 0 {name=p2 lab=VSS}
C {sg13_lv_nmos.sym} 150 -160 0 0 {name=M1 w=840.00n l=1.000u ng=2 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} 150 -510 0 0 {name=M2 w=2.000u l=1.000u ng=2 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -1130 540 0 0 {name=l1 author="IHP PDK AUTHORS"}
