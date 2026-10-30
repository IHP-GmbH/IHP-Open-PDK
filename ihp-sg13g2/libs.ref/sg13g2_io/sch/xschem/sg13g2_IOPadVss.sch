v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -140 -160 200 -160 {lab=net_4}
N -140 150 210 150 {lab=net_2}
N -410 300 -410 210 {lab=iovss}
N -140 -100 -140 -160 {lab=net_4}
N -140 530 -140 420 {lab=iovss}
N -180 340 -180 270 {lab=iovdd}
N -510 -90 -590 -90 {lab=iovss}
N -580 -30 -510 -30 {lab=vdd}
N -540 440 -540 360 {lab=sub!}
N -140 300 -140 150 {lab=vss}
N -180 70 -180 0 {lab=iovss}
N -140 150 -140 20 {lab=net_2}
N -410 440 -410 360 {lab=sub!}
N -540 300 -540 210 {lab=vss}
C {lab_wire.sym} -410 260 0 0 {name=l1 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -140 480 0 0 {name=l2 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -180 300 0 0 {name=l3 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -550 -90 0 0 {name=l4 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -540 -30 0 0 {name=l5 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -540 400 0 0 {name=l6 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -140 220 0 0 {name=l7 sig_type=std_logic lab=vss}
C {lab_wire.sym} -180 40 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -410 400 0 0 {name=l9 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -540 260 0 0 {name=l10 sig_type=std_logic lab=vss}
C {devices/noconn.sym} -510 -90 3 0 {name=p1}
C {devices/noconn.sym} -510 -30 3 0 {name=p2}
C {devices/iopin.sym} -590 -90 2 0 {name=p3 lab=iovss}
C {devices/iopin.sym} 210 150 2 0 {name=p4 lab=vss}
C {devices/iopin.sym} 200 -160 2 0 {name=p5 lab=iovdd}
C {devices/iopin.sym} -580 -30 2 0 {name=p6 lab=vdd}
C {sg13g2_DCNDiode.sym} -180 420 0 0 {name=X1}
C {sg13g2_DCPDiode.sym} -180 20 0 0 {name=X2}
C {ptap1.sym} -540 330 0 0 {name=R0 model=ptap1 w=4.85e-6 l=4.85e-6}
C {ptap1.sym} -410 330 0 0 {name=R1 model=ptap1 w=73e-6 l=73e-6}
C {devices/title-3.sym} -1440 1060 0 0 {name=l1 author="IHP PDK AUTHORS"}
