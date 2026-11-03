v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -320 -50 -320 50 {lab=iovss}
N -70 120 -70 190 {lab=sub!}
N -90 -50 -20 -50 {lab=sub!}
N -240 -50 -130 -50 {lab=#net1}
N -70 50 -70 60 {lab=iovss}
N -420 50 -320 50 {lab=iovss}
N -320 -50 -300 -50 {lab=iovss}
N -90 50 -70 50 {lab=iovss}
N -90 -20 -90 50 {lab=iovss}
N -90 -190 -90 -80 {lab=pad}
N -90 -190 30 -190 {lab=pad}
N -320 50 -90 50 {lab=iovss}
C {lab_wire.sym} -70 160 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -60 -50 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} 30 -190 2 0 {name=p1 lab=pad}
C {devices/iopin.sym} -420 50 2 0 {name=p2 lab=iovss}
C {sg13_hv_nmos.sym} -110 -50 0 0 {name=N0 model=sg13_hv_nmos w=88u l=0.6u ng=20 m=1 mm_ok=1}
C {rppd.sym} -270 -50 3 0 {name=R0 body=sub! model=rppd w=0.5e-6 l=3.54e-6 m=1 b=0 mm_ok=1}
C {ptap1.sym} -70 90 0 0 {name=R1 model=ptap1 w=7.47e-6 l=7.47e-6}
C {devices/title-3.sym} -1450 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
