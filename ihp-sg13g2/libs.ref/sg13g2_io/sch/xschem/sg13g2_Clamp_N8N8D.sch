v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 170 -130 170 -90 {lab=pad}
N 170 40 190 40 {lab=iovss}
N 170 -30 170 40 {lab=iovss}
N 190 40 190 100 {lab=iovss}
N -70 -60 -70 10 {lab=gate}
N 170 -130 240 -130 {lab=pad}
N -70 -60 130 -60 {lab=gate}
N 190 160 190 220 {lab=sub!}
N -120 -60 -70 -60 {lab=gate}
N 170 -60 250 -60 {lab=sub!}
N 20 40 170 40 {lab=iovss}
N -70 70 -70 110 {lab=#net1}
C {lab_wire.sym} 190 190 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 210 -60 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} 240 -130 0 0 {name=p1 lab=pad}
C {devices/ipin.sym} -120 -60 0 0 {name=p2 lab=gate}
C {devices/iopin.sym} 20 40 0 0 {name=p3 lab=iovss}
C {sg13_hv_nmos.sym} 150 -60 0 0 {name=N0 model=sg13_hv_nmos w=35.2u l=0.6u ng=8 m=1 mm_ok=1}
C {dantenna.sym} -70 40 0 0 {name=D0 model=dantenna l=0.78u w=0.78u}
C {ptap1.sym} 190 130 0 0 {name=R0 model=ptap1 w=7.47e-6 l=7.47e-6}
C {devices/title-3.sym} -1190 920 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {lab_wire.sym} -70 100 0 0 {name=l3 sig_type=std_logic lab=sub!}
