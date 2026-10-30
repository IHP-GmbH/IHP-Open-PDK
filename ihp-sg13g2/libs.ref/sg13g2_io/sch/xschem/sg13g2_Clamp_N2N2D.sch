v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -30 110 -30 190 {lab=gate}
N 170 20 250 20 {lab=pad}
N 170 110 240 110 {lab=sub!}
N 170 20 170 80 {lab=pad}
N 170 180 190 180 {lab=iovss}
N 170 140 170 180 {lab=iovss}
N -80 110 -30 110 {lab=gate}
N 190 280 190 320 {lab=sub!}
N 190 180 190 220 {lab=iovss}
N -30 110 130 110 {lab=gate}
N 150 180 170 180 {lab=iovss}
N -30 250 -30 300 {lab=sub!}
C {lab_wire.sym} 240 110 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 190 320 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} 250 20 0 0 {name=p1 lab=pad}
C {devices/ipin.sym} -80 110 0 0 {name=p2 lab=gate}
C {devices/iopin.sym} 150 180 2 0 {name=p3 lab=iovss}
C {sg13_hv_nmos.sym} 150 110 0 0 {name=N1 model=sg13_hv_nmos w=8.8u l=0.6u ng=2 m=1 mm_ok=1}
C {dantenna.sym} -30 220 0 0 {name=D0 model=dantenna l=0.78u w=0.78u}
C {ptap1.sym} 190 250 0 0 {name=R0 model=ptap1 w=7.47e-6 l=7.47e-6}
C {devices/title-3.sym} -1170 1060 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {lab_wire.sym} -30 300 0 0 {name=l3 sig_type=std_logic lab=sub!}
