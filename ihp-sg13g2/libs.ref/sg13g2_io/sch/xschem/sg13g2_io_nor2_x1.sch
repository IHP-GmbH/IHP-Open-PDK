v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -150 150 -150 -200 {lab=net_2}
N 60 20 60 -90 {lab=net_1}
N -150 -200 20 -200 {lab=net_2}
N 120 -120 120 -200 {lab=net_6}
N 60 -150 60 -170 {lab=net_7}
N 60 80 60 20 {lab=net_1}
N 160 200 160 150 {lab=net_4}
N 60 20 160 20 {lab=net_1}
N 60 260 60 290 {lab=net_3}
N 60 290 160 290 {lab=net_3}
N -110 260 -110 180 {lab=net_3}
N -260 150 -150 150 {lab=net_2}
N 60 260 60 180 {lab=net_3}
N 160 290 160 260 {lab=net_3}
N 60 -120 120 -120 {lab=net_6}
N -250 260 -110 260 {lab=net_3}
N 60 150 160 150 {lab=sub!}
N -110 150 -60 150 {lab=sub!}
N 60 -230 60 -280 {lab=net_6}
N -110 120 -110 80 {lab=net_1}
N 60 120 60 80 {lab=net_1}
N -110 260 60 260 {lab=net_3}
N -280 -280 60 -280 {lab=net_6}
N -110 80 60 80 {lab=net_1}
N 60 -200 120 -200 {lab=net_6}
N 60 -280 120 -280 {lab=net_6}
N 20 20 20 -120 {lab=net_5}
N 120 -200 120 -280 {lab=net_6}
N 20 150 20 20 {lab=net_5}
N -260 20 20 20 {lab=net_5}
C {lab_wire.sym} 110 150 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -80 150 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} -280 -280 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -250 260 2 0 {name=p2 lab=vss}
C {devices/ipin.sym} -260 20 0 0 {name=p3 lab=i1}
C {devices/ipin.sym} -260 150 0 0 {name=p4 lab=i0}
C {devices/opin.sym} 160 20 0 0 {name=p5 lab=nq}
C {sg13_lv_nmos.sym} -130 150 0 0 {name=N0 model=sg13_lv_nmos w=3.93u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_lv_nmos.sym} 40 150 0 0 {name=N1 model=sg13_lv_nmos w=3.93u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_lv_pmos.sym} 40 -200 0 0 {name=P0 model=sg13_lv_pmos w=4.41u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_lv_pmos.sym} 40 -120 0 0 {name=P1 model=sg13_lv_pmos w=4.41u l=0.13u ng=1 m=1 mm_ok=1}
C {ptap1.sym} 160 230 2 1 {name=R0 model=ptap1 w=0.81e-6 l=0.81e-6}
C {devices/title-3.sym} -1310 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
