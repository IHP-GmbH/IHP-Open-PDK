v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -80 0 -80 -80 {lab=net_5}
N -160 -110 -120 -110 {lab=net_6}
N -160 20 -160 -10 {lab=net_6}
N -160 70 -120 70 {lab=net_6}
N -80 -110 -30 -110 {lab=net_11}
N -30 -110 -30 -180 {lab=net_11}
N -80 -180 -30 -180 {lab=net_11}
N -80 -140 -80 -180 {lab=net_11}
N -80 70 -20 70 {lab=sub!}
N -80 140 -80 100 {lab=net_3}
N -130 -180 -80 -180 {lab=net_11}
N -130 140 -80 140 {lab=net_3}
N -80 140 170 140 {lab=net_3}
N 420 140 420 120 {lab=net_3}
N 770 140 770 120 {lab=net_3}
N 170 140 170 120 {lab=net_3}
N 650 -10 770 -10 {lab=sub!}
N 170 140 420 140 {lab=net_3}
N 650 140 770 140 {lab=net_3}
N 420 90 480 90 {lab=sub!}
N 170 60 170 -60 {lab=net_8}
N 170 -60 210 -60 {lab=net_8}
N 420 60 420 -30 {lab=net_2}
N 250 -130 310 -130 {lab=net_2}
N 310 -30 310 -130 {lab=net_2}
N 420 -30 420 -60 {lab=net_2}
N 310 -30 420 -30 {lab=net_2}
N 340 -130 380 -130 {lab=net_8}
N 340 -60 340 -130 {lab=net_8}
N 210 -60 210 -100 {lab=net_8}
N 210 -60 340 -60 {lab=net_8}
N -80 40 -80 0 {lab=net_5}
N 330 90 330 0 {lab=net_5}
N -80 0 330 0 {lab=net_5}
N -160 70 -160 20 {lab=net_6}
N 100 90 100 20 {lab=net_6}
N -160 20 100 20 {lab=net_6}
N 210 -160 210 -200 {lab=net_10}
N 420 -160 420 -190 {lab=net_10}
N 210 -240 420 -240 {lab=net_10}
N 180 -240 210 -240 {lab=net_10}
N 150 -130 210 -130 {lab=net_10}
N 150 -130 150 -200 {lab=net_10}
N 210 -200 210 -240 {lab=net_10}
N 150 -200 210 -200 {lab=net_10}
N 420 -130 470 -130 {lab=net_10}
N 470 -130 470 -190 {lab=net_10}
N 420 -190 420 -240 {lab=net_10}
N 420 -190 470 -190 {lab=net_10}
N 420 -240 650 -240 {lab=net_10}
N 570 -170 610 -170 {lab=net_2}
N 420 140 650 140 {lab=net_3}
N 770 60 770 -10 {lab=net_0}
N 170 90 230 90 {lab=sub!}
N 650 140 650 20 {lab=net_3}
N 700 -170 700 -240 {lab=net_10}
N 650 -200 650 -240 {lab=net_10}
N 650 -240 700 -240 {lab=net_10}
N 650 -170 700 -170 {lab=net_10}
N 570 -10 570 -60 {lab=net_2}
N 650 -40 650 -80 {lab=net_1}
N 570 -10 610 -10 {lab=net_2}
N 420 -60 420 -100 {lab=net_2}
N 570 -60 570 -170 {lab=net_2}
N 420 -60 570 -60 {lab=net_2}
N -160 -10 -160 -110 {lab=net_6}
N -210 -10 -160 -10 {lab=net_6}
N 650 -80 650 -140 {lab=net_1}
N 650 -80 740 -80 {lab=net_1}
N 330 90 380 90 {lab=net_5}
N 100 90 130 90 {lab=net_6}
C {lab_wire.sym} -50 70 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 710 -10 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 450 90 0 0 {name=l3 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 200 90 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {devices/ipin.sym} -210 -10 0 0 {name=p1 lab=i}
C {devices/opin.sym} 740 -80 0 0 {name=p2 lab=o}
C {devices/iopin.sym} -130 140 2 0 {name=p3 lab=vss}
C {devices/iopin.sym} -130 -180 2 0 {name=p4 lab=vdd}
C {devices/iopin.sym} 180 -240 2 0 {name=p5 lab=iovdd}
C {sg13_hv_nmos.sym} 630 -10 0 0 {name=N0 model=sg13_hv_nmos w=1.9u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_lv_nmos.sym} -100 70 0 0 {name=N1 model=sg13_lv_nmos w=2.75u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} 150 90 0 0 {name=N2 model=sg13_hv_nmos w=1.9u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} 400 90 0 0 {name=N3 model=sg13_hv_nmos w=1.9u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 630 -170 0 0 {name=P0 model=sg13_hv_pmos w=3.9u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 230 -130 0 1 {name=P1 model=sg13_hv_pmos w=0.3u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 400 -130 0 0 {name=P2 model=sg13_hv_pmos w=0.3u l=0.45u ng=1 m=1 mm_ok=1}
C {sg13_lv_pmos.sym} -100 -110 0 0 {name=P3 model=sg13_lv_pmos w=4.75u l=0.13u ng=1 m=1 mm_ok=1}
C {ptap1.sym} 770 90 2 0 {name=R0 model=ptap1 w=1.025e-6 l=1.025e-6}
C {devices/title-3.sym} -970 840 0 0 {name=l1 author="IHP PDK AUTHORS"}
