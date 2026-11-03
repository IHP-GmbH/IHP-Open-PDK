v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 150 0 230 0 {lab=net_0}
N 390 0 460 0 {lab=net_0}
N 30 -80 30 -160 {lab=net_0}
N 150 -30 150 -160 {lab=net_0}
N 230 -160 390 -160 {lab=net_0}
N 390 -30 390 -160 {lab=net_0}
N 230 0 230 -160 {lab=net_0}
N 30 -160 150 -160 {lab=net_0}
N -10 0 30 0 {lab=net_1}
N 350 60 350 0 {lab=net_1}
N -30 90 90 90 {lab=net_3}
N 70 60 350 60 {lab=net_1}
N 70 0 110 0 {lab=net_1}
N 30 0 70 0 {lab=net_1}
N 390 170 390 100 {lab=net_2}
N 150 -160 230 -160 {lab=net_0}
N 460 -160 580 -160 {lab=net_0}
N 70 60 70 0 {lab=net_1}
N 30 0 30 -20 {lab=net_1}
N 150 100 150 30 {lab=net_2}
N 390 100 390 30 {lab=net_2}
N 90 250 90 190 {lab=sub!}
N 150 100 390 100 {lab=net_2}
N 460 0 460 -160 {lab=net_0}
N 390 -160 460 -160 {lab=net_0}
N 90 130 90 90 {lab=net_3}
N 390 170 440 170 {lab=net_2}
C {lab_wire.sym} 90 220 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} 580 -160 2 0 {name=p1 lab=iovdd}
C {devices/iopin.sym} -30 90 2 0 {name=p2 lab=iovss}
C {devices/iopin.sym} 440 170 0 0 {name=p3 lab=pad}
C {devices/ipin.sym} -10 0 0 0 {name=p4 lab=gate}
C {sg13_hv_pmos.sym} 130 0 0 0 {name=P0 model=sg13_hv_pmos w=53.28u l=0.6u ng=8 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 370 0 0 0 {name=P2 model=sg13_hv_pmos w=53.28u l=0.6u ng=8 m=1 mm_ok=1}
C {dpantenna.sym} 30 -50 0 0 {name=D0 model=dpantenna l=0.48u w=0.48u}
C {ptap1.sym} 90 160 0 0 {name=R0 model=ptap1 w=8.185e-6 l=8.185e-6}
C {devices/title-3.sym} -970 920 0 0 {name=l1 author="IHP PDK AUTHORS"}
