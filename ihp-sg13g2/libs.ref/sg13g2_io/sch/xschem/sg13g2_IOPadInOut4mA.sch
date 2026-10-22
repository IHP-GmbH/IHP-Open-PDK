v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -750 -170 -640 -170 {lab=net_6}
N -750 -130 -640 -130 {lab=net_7}
N -470 -270 -470 -330 {lab=iovdd}
N -890 -390 -810 -390 {lab=vss}
N -870 -430 -810 -430 {lab=vdd}
N -490 -270 -490 -330 {lab=vdd}
N -210 350 -210 290 {lab=iovss}
N -870 -470 -810 -470 {lab=iovdd}
N -510 -270 -510 -330 {lab=vss}
N -290 110 -290 50 {lab=vdd}
N -210 110 -210 50 {lab=iovdd}
N -290 350 -290 290 {lab=vss}
N -880 -510 -810 -510 {lab=iovss}
N -80 -10 -80 -70 {lab=iovss}
N -340 -130 -160 -130 {lab=net_9}
N 0 -130 130 -130 {lab=net_3}
N 130 -70 130 -130 {lab=net_3}
N 60 -370 130 -370 {lab=net_3}
N 290 -70 300 -70 {lab=net_3}
N 300 -70 370 -70 {lab=net_3}
N 290 -60 300 -60 {lab=net_3}
N -340 -210 -280 -210 {lab=net_0}
N 130 -130 130 -370 {lab=net_3}
N 120 -70 130 -70 {lab=net_3}
N -130 190 120 190 {lab=net_3}
N 260 -260 200 -260 {lab=iovss}
N 120 190 120 -70 {lab=net_3}
N 290 -60 290 -70 {lab=net_3}
N 300 -70 300 -240 {lab=net_3}
N 130 -70 290 -70 {lab=net_3}
N -600 200 -380 200 {lab=net_13}
N 300 120 300 -60 {lab=net_3}
N -810 320 -810 240 {lab=iovss}
N 300 300 300 240 {lab=iovss}
N 260 160 200 160 {lab=iovdd}
N 300 -360 300 -420 {lab=iovdd}
N -810 440 -810 380 {lab=sub!}
N -940 440 -940 380 {lab=sub!}
N -940 320 -940 250 {lab=vss}
N -280 -370 -220 -370 {lab=net_0}
N -280 -210 -280 -370 {lab=net_0}
N -160 -480 -80 -480 {lab=iovss}
N -140 -250 -80 -250 {lab=iovdd}
C {lab_wire.sym} -470 -300 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -850 -390 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -840 -430 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -490 -300 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -210 320 0 0 {name=l5 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -840 -470 0 0 {name=l6 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -510 -300 0 0 {name=l7 sig_type=std_logic lab=vss}
C {lab_wire.sym} -290 80 0 0 {name=l8 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -210 80 0 0 {name=l9 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -290 320 0 0 {name=l10 sig_type=std_logic lab=vss}
C {lab_wire.sym} -840 -510 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -80 -40 0 0 {name=l12 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 230 -260 0 0 {name=l13 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -810 280 0 0 {name=l14 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 300 270 0 0 {name=l15 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 230 160 0 0 {name=l16 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 300 -390 0 0 {name=l17 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -810 410 0 0 {name=l18 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -940 410 0 0 {name=l19 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -940 280 0 0 {name=l20 sig_type=std_logic lab=vss}
C {lab_wire.sym} -120 -480 0 0 {name=l21 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -110 -250 0 0 {name=l22 sig_type=std_logic lab=iovdd}
C {devices/iopin.sym} -870 -430 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -890 -390 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -870 -470 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -750 -170 0 0 {name=p4 lab=c2p}
C {devices/ipin.sym} -750 -130 0 0 {name=p5 lab=c2p_en}
C {devices/iopin.sym} 370 -70 0 0 {name=p6 lab=pad}
C {devices/iopin.sym} -880 -510 2 0 {name=p7 lab=iovss}
C {devices/opin.sym} -600 200 2 0 {name=p8 lab=p2c}
C {sg13g2_Clamp_P2N2D.sym} -220 -370 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 260 -240 0 0 {name=X1}
C {sg13g2_GateDecode.sym} -640 -190 0 0 {name=X2}
C {sg13g2_Clamp_N2N2D.sym} -180 -130 0 0 {name=X3}
C {sg13g2_LevelDown.sym} -210 110 0 1 {name=X4}
C {sg13g2_DCNDiode.sym} 260 240 0 0 {name=X5}
C {ptap1.sym} -940 350 0 0 {name=R0 model=ptap1 w=4.355e-6 l=4.355e-6}
C {ptap1.sym} -810 350 0 0 {name=R1 model=ptap1 w=65.68e-6 l=65.68e-6}
C {devices/title-3.sym} -1530 840 0 0 {name=l1 author="IHP PDK AUTHORS"}
