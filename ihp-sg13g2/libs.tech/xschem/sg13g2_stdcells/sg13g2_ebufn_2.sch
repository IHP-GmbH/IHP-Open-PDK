v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 620 -260 640 -260 {}
N 120 0 340 0 {}
N 380 320 380 250 {}
N 120 0 120 -200 {}
N 580 120 580 40 {}
N 80 80 160 80 {}
N 340 0 340 -140 {}
N 620 0 620 -70 {}
N 380 190 380 160 {}
N 380 320 400 320 {}
N 220 -140 220 -260 {}
N 620 320 620 240 {}
N 380 160 380 -110 {}
N 640 210 640 120 {}
N 340 220 340 0 {}
N 200 40 580 40 {}
N 580 40 580 -100 {}
N 200 -170 200 -260 {}
N 200 320 200 250 {}
N 160 80 160 -140 {}
N 200 40 200 -110 {}
N 220 320 220 220 {}
N 620 180 620 150 {}
N 640 -200 640 -260 {}
N 620 120 640 120 {}
N 120 -200 580 -200 {}
N 380 -260 400 -260 {}
N 74 -260 200 -260 {}
N 540 210 580 210 {}
N 200 190 200 40 {}
N 400 320 620 320 {}
N 160 220 160 80 {}
N 620 -130 620 -170 {}
N 200 320 220 320 {}
N 80 0 120 0 {}
N 200 -260 220 -260 {}
N 200 220 220 220 {}
N 380 220 400 220 {}
N 620 210 640 210 {}
N 380 160 540 160 {}
N 220 320 380 320 {}
N 220 -260 380 -260 {}
N 380 -140 400 -140 {}
N 200 -140 220 -140 {}
N 640 320 640 210 {}
N 620 -100 640 -100 {}
N 640 -100 640 -200 {}
N 400 -260 620 -260 {}
N 620 90 620 0 {}
N 540 210 540 160 {}
N 60 320 200 320 {}
N 620 -230 620 -260 {}
N 620 0 670 0 {}
N 620 -200 640 -200 {}
N 400 320 400 220 {}
N 380 -170 380 -260 {}
N 620 320 640 320 {}
N 400 -140 400 -260 {}
C {devices/ipin.sym} 80 80 0 0 {name=p1 lab=A}
C {devices/ipin.sym} 80 0 0 0 {name=p2 lab=TE_B}
C {devices/opin.sym} 670 0 0 0 {name=p3 lab=Z}
C {devices/iopin.sym} 74 -260 2 0 {name=p4 lab=VDD}
C {devices/iopin.sym} 60 320 2 0 {name=p5 lab=VSS}
C {sg13_lv_nmos.sym} 180 220 0 0 {name=M1 w=640.00n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_nmos.sym} 360 220 0 0 {name=M2 w=640.00n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_nmos.sym} 600 120 0 0 {name=M3 w=1.48u l=130.00n ng=2 m=1 model=sg13_lv_nmos}
C {sg13_lv_nmos.sym} 600 210 0 0 {name=M4 w=1.48u l=130.00n ng=2 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} 180 -140 0 0 {name=M5 w=1.000u l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {sg13_lv_pmos.sym} 360 -140 0 0 {name=M6 w=1.000u l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {sg13_lv_pmos.sym} 600 -200 0 0 {name=M7 w=2.24u l=130.00n ng=2 m=1 model=sg13_lv_pmos}
C {sg13_lv_pmos.sym} 600 -100 0 0 {name=M8 w=2.24u l=130.00n ng=2 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -890 920 0 0 {name=l1 author="IHP PDK AUTHORS"}
