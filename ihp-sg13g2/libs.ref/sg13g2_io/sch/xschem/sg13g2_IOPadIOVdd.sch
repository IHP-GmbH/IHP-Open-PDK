v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 170 90 480 90 {lab=net_3}
N 370 190 420 190 {lab=net_4}
N 130 100 150 100 {lab=net_2}
N 170 190 190 190 {lab=net_3}
N 150 300 150 100 {lab=net_2}
N 170 190 170 90 {lab=net_3}
N 130 90 170 90 {lab=net_3}
N 480 110 480 90 {lab=net_3}
N 530 300 620 300 {lab=net_2}
N 530 340 530 300 {lab=net_2}
N 590 310 590 190 {lab=net_1}
N -130 310 -130 110 {lab=net_1}
N -130 310 590 310 {lab=net_1}
N -310 90 -270 90 {lab=net_0}
N -250 190 -250 120 {lab=net_5}
N 480 90 590 90 {lab=net_3}
N 480 300 480 270 {lab=net_2}
N 480 300 530 300 {lab=net_2}
N 530 440 530 400 {lab=sub!}
N 150 300 480 300 {lab=net_2}
N 540 190 590 190 {lab=net_1}
N -130 110 -110 110 {lab=net_1}
N -330 120 -250 120 {lab=net_5}
N -250 300 -250 250 {lab=sub!}
N 130 130 130 100 {lab=net_2}
C {lab_wire.sym} 530 420 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -250 280 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/noconn.sym} -270 90 3 0 {name=p1}
C {devices/iopin.sym} 590 90 2 1 {name=p2 lab=iovdd}
C {devices/iopin.sym} -310 90 2 0 {name=p3 lab=vdd}
C {devices/iopin.sym} 620 300 2 1 {name=p4 lab=iovss}
C {devices/iopin.sym} -330 120 2 0 {name=p5 lab=vss}
C {sg13g2_Clamp_N43N43D4R.sym} -130 110 0 0 {name=X1}
C {sg13g2_RCClampInverter.sym} 460 110 0 0 {name=X2}
C {sg13g2_RCClampResistor.sym} 230 130 0 0 {name=X3}
C {ptap1.sym} -250 220 0 0 {name=R0 model=ptap1 w=4.9e-6 l=4.9e-6}
C {ptap1.sym} 530 370 0 0 {name=R1 model=ptap1 w=44.535e-6 l=44.535e-6}
C {devices/title-3.sym} -1110 1140 0 0 {name=l1 author="IHP PDK AUTHORS"}
