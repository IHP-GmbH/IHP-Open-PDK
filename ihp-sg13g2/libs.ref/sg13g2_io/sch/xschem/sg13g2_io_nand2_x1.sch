v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -230 210 -40 210 {lab=i0}
N -130 80 -40 80 {lab=i1}
N -40 -140 -40 80 {lab=i1}
N -250 -220 -190 -220 {lab=vdd}
N -140 -220 0 -220 {lab=vdd}
N -190 -20 0 -20 {lab=nq}
N 0 110 0 180 {lab=#net1}
N -190 -110 -190 -20 {lab=nq}
N 0 -110 0 -30 {lab=nq}
N -190 -220 -190 -170 {lab=vdd}
N 0 -220 0 -170 {lab=vdd}
N -190 -220 -140 -220 {lab=vdd}
N -190 -140 -140 -140 {lab=vdd}
N -140 -220 -140 -140 {lab=vdd}
N -260 210 -230 210 {lab=i0}
N 0 -220 60 -220 {lab=vdd}
N 60 -220 60 -140 {lab=vdd}
N 0 -30 0 -20 {lab=nq}
N 0 -140 60 -140 {lab=vdd}
N -250 270 0 270 {lab=vss}
N 0 80 170 80 {lab=sub!}
N 0 240 0 270 {lab=vss}
N -230 -140 -230 210 {lab=i0}
N 0 210 80 210 {lab=sub!}
N 0 -20 0 50 {lab=nq}
N 0 -30 100 -30 {lab=nq}
N -0 270 170 270 {lab=vss}
N 170 200 170 270 {lab=vss}
N 170 80 170 140 {lab=sub!}
C {lab_wire.sym} 40 210 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 160 80 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/ipin.sym} -260 210 0 0 {name=p1 lab=i0}
C {devices/ipin.sym} -130 80 0 0 {name=p2 lab=i1}
C {devices/iopin.sym} -250 -220 2 0 {name=p3 lab=vdd}
C {devices/iopin.sym} -250 270 2 0 {name=p4 lab=vss}
C {devices/opin.sym} 100 -30 0 0 {name=p5 lab=nq}
C {sg13_lv_nmos.sym} -20 80 0 0 {name=N0 model=sg13_lv_nmos w=3.93u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_lv_nmos.sym} -20 210 0 0 {name=N1 model=sg13_lv_nmos w=3.93u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_lv_pmos.sym} -210 -140 0 0 {name=P0 model=sg13_lv_pmos w=4.41u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_lv_pmos.sym} -20 -140 0 0 {name=P1 model=sg13_lv_pmos w=4.41u l=0.13u ng=1 m=1 mm_ok=1}
C {ptap1.sym} 170 170 2 1 {name=R0 model=ptap1 w=0.81e-6 l=0.81e-6}
