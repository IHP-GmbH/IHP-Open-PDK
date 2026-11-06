v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 120 -60 250 -60 {lab=net_2}
N -70 190 -60 190 {lab=net_2}
N -70 -50 -70 -60 {lab=net_2}
N -180 -370 -180 -430 {lab=iovss}
N -610 -190 -530 -190 {lab=vss}
N -590 -230 -530 -230 {lab=vdd}
N -150 100 -150 40 {lab=iovss}
N -310 -120 -310 -180 {lab=iovdd}
N -590 -270 -530 -270 {lab=iovdd}
N -140 -370 -140 -430 {lab=iovdd}
N -80 -280 -60 -280 {lab=net_2}
N -70 -60 -60 -60 {lab=net_2}
N -60 -60 -60 -280 {lab=net_2}
N 120 -60 120 -190 {lab=net_2}
N -310 80 -310 20 {lab=iovss}
N -600 -320 -530 -320 {lab=iovss}
N -460 -60 -370 -60 {lab=net_6}
N 120 60 120 -50 {lab=net_2}
N -70 -50 -60 -50 {lab=net_2}
N 110 -50 120 -50 {lab=net_2}
N -190 -60 -70 -60 {lab=net_2}
N -60 190 -60 -50 {lab=net_2}
N 80 -210 20 -210 {lab=iovss}
N -60 -60 110 -60 {lab=net_2}
N 110 -60 120 -60 {lab=net_2}
N 110 -50 110 -60 {lab=net_2}
N -690 190 -690 130 {lab=sub!}
N 120 240 120 180 {lab=iovss}
N 80 100 20 100 {lab=iovdd}
N 120 -310 120 -370 {lab=iovdd}
N -690 70 -690 -10 {lab=iovss}
N -820 190 -820 130 {lab=sub!}
N -820 70 -820 0 {lab=vss}
C {lab_wire.sym} -180 -400 0 0 {name=l1 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -570 -190 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -560 -230 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -150 70 0 0 {name=l4 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -310 -150 0 0 {name=l5 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -560 -270 0 0 {name=l6 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -140 -400 0 0 {name=l7 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -310 50 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -560 -320 0 0 {name=l9 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 50 -210 0 0 {name=l10 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -690 160 0 0 {name=l11 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 120 210 0 0 {name=l12 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 50 100 0 0 {name=l13 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 120 -340 0 0 {name=l14 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -690 30 0 0 {name=l15 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -820 160 0 0 {name=l16 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -820 40 0 0 {name=l17 sig_type=std_logic lab=vss}
C {devices/noconn.sym} -530 -230 3 0 {name=p1}
C {devices/iopin.sym} -590 -230 2 0 {name=p2 lab=vdd}
C {devices/iopin.sym} -610 -190 2 0 {name=p3 lab=vss}
C {devices/iopin.sym} -590 -270 2 0 {name=p4 lab=iovdd}
C {devices/iopin.sym} -460 -60 2 0 {name=p5 lab=padres}
C {devices/iopin.sym} 250 -60 0 0 {name=p6 lab=pad}
C {devices/iopin.sym} -600 -320 2 0 {name=p7 lab=iovss}
C {sg13g2_Clamp_P20N0D.sym} -180 -370 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 80 -190 0 0 {name=X2}
C {sg13g2_SecondaryProtection.sym} -310 -140 0 0 {name=X3}
C {sg13g2_Clamp_N20N0D.sym} -160 100 0 0 {name=X4}
C {sg13g2_DCNDiode.sym} 80 180 0 0 {name=X5}
C {ptap1.sym} -820 100 0 0 {name=R0 model=ptap1 w=4.885e-6 l=4.885e-6}
C {ptap1.sym} -690 100 0 0 {name=R1 model=ptap1 w=65.575e-6 l=65.575e-6}
C {devices/title-3.sym} -1530 780 0 0 {name=l1 author="IHP PDK AUTHORS"}
