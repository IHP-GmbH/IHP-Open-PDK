v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 580 470 580 210 {}
N 620 -50 620 -130 {}
N 620 470 690 470 {}
N 550 210 580 210 {}
N 620 440 620 210 {}
N 620 610 620 500 {}
N 620 210 650 210 {}
N 620 210 620 10 {}
N 620 -20 690 -20 {}
N 454 -130 620 -130 {}
N 454 610 620 610 {}
N 690 610 690 470 {}
N 580 210 580 -20 {}
N 620 610 690 610 {}
N 690 -20 690 -130 {}
N 620 -130 690 -130 {}
C {devices/ipin.sym} 550 210 0 0 {name=p1 lab=A}
C {devices/opin.sym} 650 210 0 0 {name=p2 lab=Y}
C {devices/iopin.sym} 454 -130 2 0 {name=p3 lab=VDD}
C {devices/iopin.sym} 454 610 2 0 {name=p4 lab=VSS}
C {sg13_lv_nmos.sym} 600 470 0 0 {name=M1 w=2.96u l=130.00n ng=4 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} 600 -20 0 0 {name=M2 w=4.48u l=130.00n ng=4 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -680 1120 0 0 {name=l1 author="IHP PDK AUTHORS"}
