v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 20 80 240 80 {lab=net_2}
N 20 -10 20 80 {lab=net_2}
N 300 -160 300 -30 {lab=net_0}
N -200 0 -80 0 {lab=net_1}
N -180 -160 -80 -160 {lab=net_0}
N 80 -160 80 -30 {lab=net_0}
N -60 10 200 10 {lab=net_1}
N 240 -160 240 -60 {lab=net_0}
N 20 -160 20 -60 {lab=net_0}
N 80 -160 240 -160 {lab=net_0}
N -90 60 -90 120 {lab=net_3}
N 20 -30 80 -30 {lab=net_0}
N -80 -30 -80 0 {lab=net_1}
N -80 -30 -60 -30 {lab=net_1}
N 240 -30 300 -30 {lab=net_0}
N 20 -160 80 -160 {lab=net_0}
N -60 -30 -60 10 {lab=net_1}
N -80 -160 -80 -90 {lab=net_0}
N -60 -30 -20 -30 {lab=net_1}
N -80 -160 20 -160 {lab=net_0}
N 200 -30 200 10 {lab=net_1}
N -90 180 -90 240 {lab=sub!}
N -200 60 -90 60 {lab=net_3}
N 240 -160 300 -160 {lab=net_0}
N 240 80 340 80 {lab=net_2}
N 240 0 240 80 {lab=net_2}
C {lab_wire.sym} -90 210 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} -180 -160 2 0 {name=p1 lab=iovdd}
C {devices/iopin.sym} -200 60 2 0 {name=p2 lab=iovss}
C {devices/iopin.sym} 340 80 0 0 {name=p3 lab=pad}
C {devices/ipin.sym} -200 0 0 0 {name=p4 lab=gate}
C {sg13_hv_pmos.sym} 0 -30 0 0 {name=P0 model=sg13_hv_pmos w=99.9u l=0.6u ng=15 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 220 -30 0 0 {name=P1 model=sg13_hv_pmos w=99.9u l=0.6u ng=15 m=1 mm_ok=1}
C {dpantenna.sym} -80 -60 0 0 {name=D0 model=dpantenna l=0.78u w=0.78u}
C {ptap1.sym} -90 150 0 0 {name=R0 model=ptap1 w=8.185e-6 l=8.185e-6}
C {devices/title-3.sym} -1180 920 0 0 {name=l1 author="IHP PDK AUTHORS"}
