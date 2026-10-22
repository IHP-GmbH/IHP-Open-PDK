v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -320 -150 -320 -120 {lab=iovss}
N -100 -170 -100 -50 {lab=pad}
N 100 -50 200 -50 {lab=pad}
N -320 -350 -100 -350 {lab=iovdd}
N -140 -240 60 -240 {lab=gate}
N -100 -50 100 -50 {lab=pad}
N -100 -200 -10 -200 {lab=iovdd}
N 100 -350 200 -350 {lab=iovdd}
N -320 -200 -140 -200 {lab=gate}
N -100 -350 -100 -230 {lab=iovdd}
N -370 -150 -320 -150 {lab=iovss}
N -320 -210 -320 -200 {lab=gate}
N -420 -200 -320 -200 {lab=gate}
N -320 -350 -320 -270 {lab=iovdd}
N -100 -350 100 -350 {lab=iovdd}
N 100 -350 100 -230 {lab=iovdd}
N 100 -170 100 -50 {lab=pad}
N -140 -240 -140 -200 {lab=gate}
N 60 -240 60 -200 {lab=gate}
N -320 -60 -320 -10 {lab=sub!}
N 100 -200 190 -200 {lab=iovdd}
C {lab_wire.sym} -20 -200 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -320 -20 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 180 -200 0 0 {name=l3 sig_type=std_logic lab=iovdd}
C {devices/iopin.sym} 200 -350 2 0 {name=p1 lab=iovdd}
C {devices/iopin.sym} -370 -150 2 0 {name=p2 lab=iovss}
C {devices/iopin.sym} 200 -50 2 0 {name=p3 lab=pad}
C {devices/ipin.sym} -420 -200 0 0 {name=p4 lab=gate}
C {sg13_hv_pmos.sym} -120 -200 0 0 {name=P0 model=sg13_hv_pmos w=13.32u l=0.6u ng=2 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} 80 -200 0 0 {name=P1 model=sg13_hv_pmos w=13.32u l=0.6u ng=2 m=1 mm_ok=1}
C {dpantenna.sym} -320 -240 0 0 {name=D0 model=dpantenna l=0.48u w=0.48u}
C {ptap1.sym} -320 -90 0 0 {name=R0 model=ptap1 w=8.185e-6 l=8.185e-6}
C {devices/title-3.sym} -1360 700 0 0 {name=l1 author="IHP PDK AUTHORS"}
