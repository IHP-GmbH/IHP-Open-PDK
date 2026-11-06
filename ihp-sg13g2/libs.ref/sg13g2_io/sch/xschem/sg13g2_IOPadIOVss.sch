v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 480 90 480 0 {lab=net_2}
N 120 130 120 40 {lab=sub!}
N 120 -20 120 -100 {lab=vss}
N 440 130 440 60 {lab=iovdd}
N 440 -20 440 -100 {lab=iovss}
N 480 -260 570 -260 {lab=net_3}
N -140 -220 -40 -220 {lab=vss}
N -140 -180 -40 -180 {lab=vdd}
N 0 130 0 40 {lab=sub!}
N 480 0 480 -80 {lab=net_2}
N 0 -20 0 -100 {lab=iovss}
N 480 300 480 210 {lab=iovss}
N 480 0 570 0 {lab=net_2}
N 480 -200 480 -260 {lab=net_3}
C {lab_wire.sym} 120 80 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 120 -60 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} 440 100 0 0 {name=l3 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 440 -60 0 0 {name=l4 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -90 -220 0 0 {name=l5 sig_type=std_logic lab=vss}
C {lab_wire.sym} -90 -180 0 0 {name=l6 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 0 80 0 0 {name=l7 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 0 -60 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 480 260 0 0 {name=l9 sig_type=std_logic lab=iovss}
C {devices/noconn.sym} -40 -220 3 0 {name=p1}
C {devices/noconn.sym} -40 -180 3 0 {name=p2}
C {devices/iopin.sym} 570 0 2 0 {name=p3 lab=iovss}
C {devices/iopin.sym} -140 -220 2 0 {name=p4 lab=vss}
C {devices/iopin.sym} 570 -260 2 0 {name=p5 lab=iovdd}
C {devices/iopin.sym} -140 -180 2 0 {name=p6 lab=vdd}
C {sg13g2_DCPDiode.sym} 440 -80 0 0 {name=X2}
C {sg13g2_DCNDiode.sym} 440 210 0 0 {name=X3}
C {ptap1.sym} 0 10 0 0 {name=R0 model=ptap1 w=74.075e-6 l=74.075e-6}
C {ptap1.sym} 120 10 0 0 {name=R1 model=ptap1 w=4.9e-6 l=4.9e-6}
C {devices/title-3.sym} -1030 900 0 0 {name=l1 author="IHP PDK AUTHORS"}
