v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -80 -80 -80 0 {lab=#net1}
N -160 -110 -120 -110 {lab=i}
N -160 -10 -160 20 {lab=i}
N -160 70 -120 70 {lab=i}
N -80 -110 -30 -110 {lab=vdd}
N -30 -180 -30 -110 {lab=vdd}
N -80 -180 -30 -180 {lab=vdd}
N -80 -180 -80 -140 {lab=vdd}
N -80 70 -30 70 {lab=sub!}
N -80 100 -80 140 {lab=vss}
N -130 -180 -80 -180 {lab=vdd}
N -130 140 -80 140 {lab=vss}
N 210 140 420 140 {lab=vss}
N 420 120 420 140 {lab=vss}
N 650 50 770 50 {lab=sub!}
N 650 80 650 140 {lab=vss}
N 650 140 770 140 {lab=vss}
N 420 90 480 90 {lab=sub!}
N 420 -30 420 60 {lab=#net2}
N 250 -130 310 -130 {lab=#net2}
N 310 -130 310 -30 {lab=#net2}
N 420 -60 420 -30 {lab=#net2}
N 310 -30 420 -30 {lab=#net2}
N 340 -130 380 -130 {lab=#net3}
N 340 -130 340 -60 {lab=#net3}
N 210 -100 210 -60 {lab=#net3}
N 210 -60 340 -60 {lab=#net3}
N -80 0 -80 40 {lab=#net1}
N 100 0 100 90 {lab=#net1}
N -80 0 100 0 {lab=#net1}
N -160 20 -160 70 {lab=i}
N 330 20 330 90 {lab=i}
N -160 20 330 20 {lab=i}
N 210 -200 210 -160 {lab=iovdd}
N 420 -190 420 -160 {lab=iovdd}
N 210 -240 420 -240 {lab=iovdd}
N 180 -240 210 -240 {lab=iovdd}
N 150 -130 210 -130 {lab=iovdd}
N 150 -200 150 -130 {lab=iovdd}
N 210 -240 210 -200 {lab=iovdd}
N 150 -200 210 -200 {lab=iovdd}
N 420 -130 470 -130 {lab=iovdd}
N 470 -190 470 -130 {lab=iovdd}
N 420 -240 420 -190 {lab=iovdd}
N 420 -190 470 -190 {lab=iovdd}
N 420 -240 650 -240 {lab=iovdd}
N 570 -170 610 -170 {lab=#net2}
N 570 -60 570 50 {lab=#net2}
N 770 130 770 140 {lab=vss}
N 700 -240 700 -170 {lab=iovdd}
N 650 -240 650 -200 {lab=iovdd}
N 650 -240 700 -240 {lab=iovdd}
N 650 -170 700 -170 {lab=iovdd}
N 650 -80 650 20 {lab=o}
N 570 50 610 50 {lab=#net2}
N 420 -100 420 -60 {lab=#net2}
N 570 -170 570 -60 {lab=#net2}
N 420 -60 570 -60 {lab=#net2}
N -160 -110 -160 -10 {lab=i}
N -210 -10 -160 -10 {lab=i}
N 650 -140 650 -80 {lab=o}
N 650 -80 740 -80 {lab=o}
N 420 140 650 140 {lab=vss}
N 330 90 380 90 {lab=i}
N 100 90 170 90 {lab=#net1}
N 770 50 770 70 {lab=sub!}
N 210 90 260 90 {lab=sub!}
N 210 -60 210 60 {lab=#net3}
N 210 120 210 140 {lab=vss}
N -80 140 210 140 {lab=vss}
C {lab_wire.sym} -30 70 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 710 50 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 450 90 0 0 {name=l3 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 260 90 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} 180 -240 2 0 {name=p1 lab=iovdd}
C {devices/iopin.sym} -130 140 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -130 -180 2 0 {name=p3 lab=vdd}
C {devices/ipin.sym} -210 -10 0 0 {name=p4 lab=i}
C {devices/opin.sym} 740 -80 0 0 {name=p5 lab=o}
C {sg13_hv_nmos.sym} 630 50 0 0 {name=N0 model=sg13_hv_nmos w=1.9u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_lv_nmos.sym} -100 70 0 0 {name=N1 model=sg13_lv_nmos w=2.75u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} 190 90 0 0 {name=N2 model=sg13_hv_nmos w=1.9u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} 400 90 0 0 {name=N3 model=sg13_hv_nmos w=1.9u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 630 -170 0 0 {name=P0 model=sg13_hv_pmos w=3.9u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 230 -130 0 1 {name=P1 model=sg13_hv_pmos w=0.3u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 400 -130 0 0 {name=P2 model=sg13_hv_pmos w=0.3u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_lv_pmos.sym} -100 -110 0 0 {name=P3 model=sg13_lv_pmos w=4.75u l=0.13u ng=1 m=1 mm_ok=1}
C {ptap1.sym} 770 100 2 1 {name=R0 model=ptap1 w=0.955e-6 l=0.955e-6}
C {devices/title-3.sym} -660 720 0 0 {name=l1 author="IHP PDK AUTHORS"}
