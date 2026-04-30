v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -110 -30 -90 -30 {}
N -50 170 -50 -30 {}
N -90 200 -90 -30 {}
N -50 -30 -20 -30 {}
N -50 280 -50 230 {}
N -186 280 -50 280 {}
N -50 -30 -50 -240 {}
N 20 280 20 200 {}
N -50 -340 20 -340 {}
N -50 -300 -50 -340 {}
N -90 -30 -90 -270 {}
N -50 200 20 200 {}
N -200 -340 -50 -340 {}
N 20 -270 20 -340 {}
N -50 280 20 280 {}
N -50 -270 20 -270 {}
C {devices/opin.sym} -20 -30 0 0 {name=p1 lab=Y}
C {devices/iopin.sym} -186 280 2 0 {name=p2 lab=VSS}
C {devices/ipin.sym} -110 -30 0 0 {name=p3 lab=A}
C {devices/iopin.sym} -200 -340 2 0 {name=p4 lab=VDD}
C {sg13_lv_nmos.sym} -70 200 0 0 {name=M1 w=11.84u l=130.00n ng=16 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} -70 -270 0 0 {name=M2 w=17.92u l=130.00n ng=16 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -1340 860 0 0 {name=l1 author="IHP PDK AUTHORS"}
