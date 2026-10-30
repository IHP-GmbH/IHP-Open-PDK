v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 180 70 610 70 {lab=vdd}
N 180 70 180 280 {lab=vdd}
N 670 280 690 280 {lab=#net1}
N 610 360 610 380 {lab=iovss}
N 390 280 550 280 {lab=#net2}
N 610 70 610 200 {lab=vdd}
N 180 280 210 280 {lab=vdd}
N 130 80 160 80 {lab=iovss}
N -140 160 690 160 {lab=#net1}
N 160 80 160 380 {lab=iovss}
N -310 90 -270 90 {lab=iovdd}
N -320 150 -270 150 {lab=vss}
N 610 380 750 380 {lab=iovss}
N 160 380 160 450 {lab=iovss}
N 160 510 160 570 {lab=sub!}
N -10 510 -10 550 {lab=sub!}
N -10 390 -10 450 {lab=vss}
N 690 160 690 280 {lab=#net1}
N -140 90 -110 90 {lab=#net1}
N 610 70 720 70 {lab=vdd}
N 160 380 610 380 {lab=iovss}
N 130 70 180 70 {lab=vdd}
N -140 90 -140 160 {lab=#net1}
N 610 380 610 390 {lab=iovss}
N 130 80 130 110 {lab=iovss}
C {lab_wire.sym} 160 540 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -10 530 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -10 420 0 0 {name=l3 sig_type=std_logic lab=vss}
C {devices/noconn.sym} -270 90 3 0 {name=p1}
C {devices/noconn.sym} -270 150 3 0 {name=p2}
C {devices/iopin.sym} 750 380 2 0 {name=p3 lab=iovss}
C {devices/iopin.sym} -310 90 2 0 {name=p4 lab=iovdd}
C {devices/iopin.sym} -320 150 2 0 {name=p5 lab=vss}
C {devices/iopin.sym} 720 70 0 0 {name=p6 lab=vdd}
C {sg13g2_Clamp_N43N43D4R.sym} -130 90 0 0 {name=X1}
C {sg13g2_RCClampInverter.sym} 590 200 0 0 {name=X3}
C {sg13g2_RCClampResistor.sym} 250 220 0 0 {name=X4}
C {ptap1.sym} -10 480 0 0 {name=R0 model=ptap1 w=4.9e-6 l=4.9e-6}
C {ptap1.sym} 160 480 0 0 {name=R1 model=ptap1 w=44.385e-6 l=44.385e-6}
C {devices/title-3.sym} -1030 1200 0 0 {name=l1 author="IHP PDK AUTHORS"}
