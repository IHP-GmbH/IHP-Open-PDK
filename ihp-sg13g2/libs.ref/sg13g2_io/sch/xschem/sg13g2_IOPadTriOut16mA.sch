v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -770 -70 -660 -70 {lab=net_6}
N -360 -110 -330 -110 {lab=net_0}
N -360 -30 -330 -30 {lab=net_9}
N -490 -170 -490 -230 {lab=iovdd}
N -780 -260 -700 -260 {lab=vss}
N -760 -300 -700 -300 {lab=vdd}
N -510 -170 -510 -230 {lab=vdd}
N -760 -340 -700 -340 {lab=iovdd}
N -530 -170 -530 -230 {lab=vss}
N -770 -380 -700 -380 {lab=iovss}
N 150 60 150 -30 {lab=net_3}
N -170 240 -170 180 {lab=iovss}
N -30 -260 -10 -260 {lab=net_3}
N -170 -80 -170 -140 {lab=iovdd}
N 140 -30 150 -30 {lab=net_3}
N -10 -40 -10 -260 {lab=net_3}
N -10 120 -10 -40 {lab=net_3}
N -760 -30 -660 -30 {lab=net_7}
N -330 120 -250 120 {lab=net_9}
N -330 120 -330 -30 {lab=net_9}
N -330 -260 -310 -260 {lab=net_0}
N 150 -40 320 -40 {lab=net_3}
N 150 -40 150 -160 {lab=net_3}
N -330 -110 -330 -260 {lab=net_0}
N 110 -180 50 -180 {lab=iovss}
N -10 -40 140 -40 {lab=net_3}
N -170 -370 -170 -430 {lab=iovss}
N 140 -40 150 -40 {lab=net_3}
N -90 120 -10 120 {lab=net_3}
N 140 -30 140 -40 {lab=net_3}
N -760 440 -760 380 {lab=sub!}
N 150 240 150 180 {lab=iovss}
N 110 100 50 100 {lab=iovdd}
N 150 -280 150 -340 {lab=iovdd}
N -760 320 -760 240 {lab=iovss}
N -890 440 -890 380 {lab=sub!}
N -890 320 -890 250 {lab=vss}
C {lab_wire.sym} -490 -200 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -740 -260 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -730 -300 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -510 -200 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -730 -340 0 0 {name=l5 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -530 -200 0 0 {name=l6 sig_type=std_logic lab=vss}
C {lab_wire.sym} -740 -380 0 0 {name=l7 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -170 210 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -170 -110 0 0 {name=l9 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 80 -180 0 0 {name=l10 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -170 -400 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -760 410 0 0 {name=l12 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 150 210 0 0 {name=l13 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 80 100 0 0 {name=l14 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 150 -310 0 0 {name=l15 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -760 280 0 0 {name=l16 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -890 410 0 0 {name=l17 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -890 280 0 0 {name=l18 sig_type=std_logic lab=vss}
C {devices/iopin.sym} -760 -300 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -780 -260 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -760 -340 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -770 -70 0 0 {name=p4 lab=c2p}
C {devices/opin.sym} 320 -40 2 1 {name=p5 lab=pad}
C {devices/iopin.sym} -770 -380 2 0 {name=p6 lab=iovss}
C {devices/ipin.sym} -760 -30 0 0 {name=p7 lab=c2p_en}
C {sg13g2_Clamp_P8N8D.sym} -310 -260 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 110 -160 0 0 {name=X1}
C {sg13g2_GateDecode.sym} -660 -90 0 0 {name=X2}
C {sg13g2_Clamp_N8N8D.sym} -270 120 0 0 {name=X3}
C {sg13g2_DCNDiode.sym} 110 180 0 0 {name=X4}
C {ptap1.sym} -890 350 0 0 {name=R0 model=ptap1 w=4.585e-6 l=4.585e-6}
C {ptap1.sym} -760 350 0 0 {name=R1 model=ptap1 w=66.635e-6 l=66.635e-6}
C {devices/title-3.sym} -1530 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
