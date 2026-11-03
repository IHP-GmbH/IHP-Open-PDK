v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -130 130 -30 130 {lab=vss}
N -30 80 -30 130 {lab=vss}
N -30 50 100 50 {lab=sub!}
N -160 -220 -30 -220 {lab=vdd}
N -30 -220 -30 -150 {lab=vdd}
N -30 -220 40 -220 {lab=vdd}
N 40 -220 40 -120 {lab=vdd}
N -190 -40 -100 -40 {lab=i}
N -30 130 100 130 {lab=vss}
N -30 -40 -30 20 {lab=nq}
N -100 -120 -100 -40 {lab=i}
N -100 50 -70 50 {lab=i}
N -100 -120 -70 -120 {lab=i}
N -100 -40 -100 50 {lab=i}
N -30 -40 70 -40 {lab=nq}
N -30 -120 40 -120 {lab=vdd}
N -30 -90 -30 -40 {lab=nq}
N 100 120 100 130 {lab=vss}
N 100 50 100 60 {lab=sub!}
C {lab_wire.sym} 40 50 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} -130 130 2 0 {name=p1 lab=vss}
C {devices/ipin.sym} -190 -40 0 0 {name=p2 lab=i}
C {devices/iopin.sym} -160 -220 2 0 {name=p3 lab=vdd}
C {devices/opin.sym} 70 -40 0 0 {name=p4 lab=nq}
C {sg13_lv_nmos.sym} -50 50 0 0 {name=N0 model=sg13_lv_nmos w=3.93u l=0.13u ng=1 m=1 mm_ok=1}
C {sg13_lv_pmos.sym} -50 -120 0 0 {name=P0 model=sg13_lv_pmos w=4.41u l=0.13u ng=1 m=1 mm_ok=1}
C {ptap1.sym} 100 90 2 1 {name=R0 model=ptap1 w=0.79e-6 l=0.79e-6}
C {devices/title-3.sym} -1170 870 0 0 {name=l1 author="IHP PDK AUTHORS"}
