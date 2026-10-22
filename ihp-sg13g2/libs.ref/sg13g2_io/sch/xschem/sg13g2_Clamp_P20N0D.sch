v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -90 -70 -90 -90 {lab=net_2}
N -210 -220 -90 -220 {lab=net_0}
N -90 -70 -60 -70 {lab=net_2}
N 260 60 330 60 {lab=net_1}
N -90 -150 -90 -220 {lab=net_0}
N 20 -100 20 -220 {lab=net_0}
N -50 180 -50 110 {lab=sub!}
N 20 -70 90 -70 {lab=net_0}
N -50 50 -50 -10 {lab=net_3}
N -120 -10 -50 -10 {lab=net_3}
N 20 60 20 -40 {lab=net_1}
N 90 -70 90 -220 {lab=net_0}
N 20 -220 90 -220 {lab=net_0}
N -60 -30 -60 -70 {lab=net_2}
N -90 -220 20 -220 {lab=net_0}
N -60 -70 -20 -70 {lab=net_2}
N -60 -30 220 -30 {lab=net_2}
N 220 -30 220 -70 {lab=net_2}
N 260 -100 260 -220 {lab=net_0}
N 90 -220 260 -220 {lab=net_0}
N 260 -70 320 -70 {lab=net_0}
N 320 -70 320 -220 {lab=net_0}
N 260 -220 320 -220 {lab=net_0}
N 20 60 260 60 {lab=net_1}
N 260 60 260 -40 {lab=net_1}
C {lab_wire.sym} -50 140 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} -120 -10 2 0 {name=p1 lab=iovss}
C {devices/iopin.sym} 330 60 0 0 {name=p2 lab=pad}
C {devices/iopin.sym} -210 -220 2 0 {name=p3 lab=iovdd}
C {sg13_hv_pmos.sym} 0 -70 0 0 {name=P0 model=sg13_hv_pmos w=133.2u l=0.6u ng=20 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 240 -70 0 0 {name=P1 model=sg13_hv_pmos w=133.2u l=0.6u ng=20 m=1 mm_ok=1}
C {rppd.sym} -90 -120 2 0 {name=R0 body=iovdd model=rppd w=0.5e-6 l=12.9e-6 m=1 b=0 mm_ok=1}
C {ptap1.sym} -50 80 0 0 {name=R1 model=ptap1 w=8.185e-6 l=8.185e-6}
C {devices/title-3.sym} -1190 860 0 0 {name=l1 author="IHP PDK AUTHORS"}
