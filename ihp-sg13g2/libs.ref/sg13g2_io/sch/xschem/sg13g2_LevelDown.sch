v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 550 160 690 160 {lab=iovss}
N 690 -210 690 -70 {lab=iovdd}
N 550 -10 550 70 {lab=#net1}
N 690 160 730 160 {lab=iovss}
N 550 130 550 160 {lab=iovss}
N 110 160 150 160 {lab=vss}
N -40 -210 -40 -170 {lab=vdd}
N 110 -210 110 -170 {lab=vdd}
N -60 -210 -60 -140 {lab=vdd}
N 400 240 400 300 {lab=sub!}
N 110 130 110 160 {lab=vss}
N 50 -140 110 -140 {lab=sub!}
N -60 -210 -40 -210 {lab=vdd}
N 110 -110 110 -10 {lab=#net2}
N 50 100 110 100 {lab=sub!}
N 420 130 420 160 {lab=iovss}
N -40 -10 -40 70 {lab=core}
N -170 -140 -170 -90 {lab=vdd}
N 460 -10 460 100 {lab=#net1}
N 590 -10 630 -10 {lab=#net3}
N -40 -210 110 -210 {lab=vdd}
N 0 -140 0 -10 {lab=#net2}
N -60 -140 -40 -140 {lab=vdd}
N -60 160 -60 180 {lab=vss}
N -60 160 -40 160 {lab=vss}
N -60 240 -60 300 {lab=sub!}
N -40 -110 -40 -10 {lab=core}
N -70 -10 -40 -10 {lab=core}
N 170 40 170 100 {lab=#net4}
N 110 -210 150 -210 {lab=vdd}
N -100 100 -40 100 {lab=sub!}
N 110 -10 110 70 {lab=#net2}
N 0 -10 0 100 {lab=#net2}
N 460 -140 460 -70 {lab=#net1}
N 790 -10 860 -10 {lab=pad}
N 150 100 170 100 {lab=#net4}
N -40 130 -40 160 {lab=vss}
N 0 -10 110 -10 {lab=#net2}
N -40 160 110 160 {lab=vss}
N 690 -210 740 -210 {lab=iovdd}
N 360 100 420 100 {lab=sub!}
N 400 -140 420 -140 {lab=iovdd}
N 520 -210 520 -140 {lab=iovdd}
N 150 -140 170 -140 {lab=#net1}
N 490 100 550 100 {lab=sub!}
N 520 -140 550 -140 {lab=iovdd}
N 550 -210 690 -210 {lab=iovdd}
N -240 -210 -240 -170 {lab=vdd}
N 550 -210 550 -170 {lab=iovdd}
N 420 160 550 160 {lab=iovss}
N 400 -210 420 -210 {lab=iovdd}
N 420 -210 420 -170 {lab=iovdd}
N 590 -140 590 -10 {lab=#net3}
N 550 -110 550 -10 {lab=#net1}
N 420 -210 520 -210 {lab=iovdd}
N 400 -210 400 -140 {lab=iovdd}
N 520 -210 550 -210 {lab=iovdd}
N 420 40 420 70 {lab=#net4}
N 460 -10 550 -10 {lab=#net1}
N 690 70 690 160 {lab=iovss}
N -170 -210 -60 -210 {lab=vdd}
N 590 -10 590 100 {lab=#net3}
N 170 40 420 40 {lab=#net4}
N 400 160 400 180 {lab=iovss}
N 400 160 420 160 {lab=iovss}
N -200 -140 -170 -140 {lab=vdd}
N -290 -210 -290 -140 {lab=vdd}
N -290 -210 -240 -210 {lab=vdd}
N -240 -210 -170 -210 {lab=vdd}
N -240 -90 -170 -90 {lab=vdd}
N 420 -110 420 40 {lab=#net4}
N -240 -110 -240 -90 {lab=vdd}
N -290 -140 -240 -140 {lab=vdd}
N 170 -140 170 -70 {lab=#net1}
N -170 -210 -170 -140 {lab=vdd}
N 460 -70 460 -10 {lab=#net1}
N 170 -70 460 -70 {lab=#net1}
N 670 -70 690 -70 {lab=iovdd}
N 670 70 690 70 {lab=iovss}
C {lab_wire.sym} 400 270 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 80 -140 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 80 100 0 0 {name=l3 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -60 270 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -70 100 0 0 {name=l5 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 390 100 0 0 {name=l6 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 520 100 0 0 {name=l7 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} 740 -210 2 1 {name=p1 lab=iovdd}
C {devices/iopin.sym} 150 -210 2 1 {name=p2 lab=vdd}
C {devices/opin.sym} -70 -10 0 1 {name=p3 lab=core}
C {devices/iopin.sym} 730 160 2 1 {name=p4 lab=iovss}
C {devices/iopin.sym} 150 160 2 1 {name=p5 lab=vss}
C {devices/ipin.sym} 860 -10 0 1 {name=p6 lab=pad}
C {sg13_hv_nmos.sym} 130 -140 0 1 {name=N0 model=sg13_hv_nmos w=2.65u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_lv_nmos.sym} -20 100 0 1 {name=N1 model=sg13_lv_nmos w=2.75u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} 130 100 0 1 {name=N2 model=sg13_hv_nmos w=2.65u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} 440 100 0 1 {name=N3 model=sg13_hv_nmos w=1.3u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} 570 100 0 1 {name=N4 model=sg13_hv_nmos w=1.3u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} -220 -140 0 1 {name=P0 model=sg13_hv_pmos w=4.65u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_lv_pmos.sym} -20 -140 0 1 {name=P1 model=sg13_lv_pmos w=4.75u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 440 -140 0 1 {name=P2 model=sg13_hv_pmos w=4.6u l=0.45u ng=2 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 570 -140 0 1 {name=P3 model=sg13_hv_pmos w=4.6u l=0.45u ng=2 m=1 mm_ok=1}
C {sg13g2_SecondaryProtection.sym} 670 -90 0 0 {name=X0}
C {ptap1.sym} -60 210 0 0 {name=R0 model=ptap1 w=1.42e-6 l=1.42e-6}
C {ptap1.sym} 400 210 0 0 {name=R1 model=ptap1 w=0.985e-6 l=0.985e-6}
C {devices/title-3.sym} -970 920 0 0 {name=l1 author="IHP PDK AUTHORS"}
