v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -10 10 -10 40 {lab=iovss}
N -10 100 -10 170 {lab=sub!}
N -30 -30 40 -30 {lab=sub!}
N -30 -160 -30 -60 {lab=pad}
N -120 -30 -70 -30 {lab=gate}
N -30 -160 100 -160 {lab=pad}
N -30 10 -10 10 {lab=iovss}
N -30 0 -30 10 {lab=iovss}
N -10 10 60 10 {lab=iovss}
N -160 -30 -120 -30 {lab=gate}
N -120 -30 -120 70 {lab=gate}
N -120 130 -120 180 {lab=sub!}
C {lab_wire.sym} -10 140 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 0 -30 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} 100 -160 2 0 {name=p1 lab=pad}
C {devices/ipin.sym} -160 -30 0 0 {name=p2 lab=gate}
C {devices/iopin.sym} 60 10 0 0 {name=p3 lab=iovss}
C {sg13_hv_nmos.sym} -50 -30 0 0 {name=N0[1:172] model=sg13_hv_nmos w=4.4u l=0.6u ng=1 m=1 mm_ok=1}
C {dantenna.sym} -120 100 0 0 {name=D0 model=dantenna l=0.48u w=0.48u}
C {ptap1.sym} -10 70 0 0 {name=R0 model=ptap1 w=8.1e-6 l=8.1e-6}
C {devices/title-3.sym} -1280 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {lab_wire.sym} -120 180 0 0 {name=l3 sig_type=std_logic lab=sub!}
