v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 260 130 280 130 {lab=iovss}
N 260 60 260 130 {lab=iovss}
N 100 30 220 30 {lab=gate}
N 260 30 340 30 {lab=sub!}
N 50 30 100 30 {lab=gate}
N 260 -140 380 -140 {lab=pad}
N 280 130 280 190 {lab=iovss}
N 100 30 100 90 {lab=gate}
N 280 250 280 320 {lab=sub!}
N 260 -140 260 0 {lab=pad}
N 230 130 260 130 {lab=iovss}
N 100 150 100 220 {lab=#net1}
C {lab_wire.sym} 300 30 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 280 280 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} 380 -140 2 0 {name=p1 lab=pad}
C {devices/ipin.sym} 50 30 0 0 {name=p2 lab=gate}
C {devices/iopin.sym} 230 130 2 0 {name=p3 lab=iovss}
C {sg13_hv_nmos.sym} 240 30 0 0 {name=N0 model=sg13_hv_nmos w=66u l=0.6u ng=15 m=1 mm_ok=1}
C {dantenna.sym} 100 120 0 0 {name=D0 model=dantenna l=0.78u w=0.78u}
C {ptap1.sym} 280 220 0 0 {name=R0 model=ptap1 w=7.47e-6 l=7.47e-6}
C {devices/title-3.sym} -1030 980 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {lab_wire.sym} 100 200 0 0 {name=l3 sig_type=std_logic lab=sub!}
