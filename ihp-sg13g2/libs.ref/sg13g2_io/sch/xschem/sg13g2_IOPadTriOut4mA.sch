v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -770 -70 -660 -70 {lab=net_6}
N -160 -520 -160 -580 {lab=iovss}
N -90 240 -10 240 {lab=net_3}
N -490 -170 -490 -230 {lab=iovdd}
N -780 -330 -700 -330 {lab=vss}
N -760 -370 -700 -370 {lab=vdd}
N -510 -170 -510 -230 {lab=vdd}
N -760 -410 -700 -410 {lab=iovdd}
N -530 -170 -530 -230 {lab=vss}
N 170 160 170 -30 {lab=net_3}
N -770 -450 -700 -450 {lab=iovss}
N -160 -230 -160 -290 {lab=iovdd}
N -170 360 -170 300 {lab=iovss}
N -340 -410 -300 -410 {lab=net_0}
N -20 -410 -10 -410 {lab=net_3}
N 160 -30 170 -30 {lab=net_3}
N -340 -110 -340 -410 {lab=net_0}
N -10 -40 -10 -410 {lab=net_3}
N -360 -110 -340 -110 {lab=net_0}
N -360 -30 -340 -30 {lab=net_9}
N -760 -30 -660 -30 {lab=net_7}
N -340 240 -250 240 {lab=net_9}
N 170 -40 170 -330 {lab=net_3}
N 160 -40 170 -40 {lab=net_3}
N 130 -350 70 -350 {lab=iovss}
N 170 -40 340 -40 {lab=net_3}
N -10 240 -10 -40 {lab=net_3}
N -10 -40 160 -40 {lab=net_3}
N -340 240 -340 -30 {lab=net_9}
N 160 -30 160 -40 {lab=net_3}
N -760 440 -760 380 {lab=sub!}
N 170 340 170 280 {lab=iovss}
N 130 200 70 200 {lab=iovdd}
N 170 -450 170 -510 {lab=iovdd}
N -760 320 -760 240 {lab=iovss}
N -890 440 -890 380 {lab=sub!}
N -890 320 -890 250 {lab=vss}
C {lab_wire.sym} -160 -550 0 0 {name=l1 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -490 -200 0 0 {name=l2 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -740 -330 0 0 {name=l3 sig_type=std_logic lab=vss}
C {lab_wire.sym} -730 -370 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -510 -200 0 0 {name=l5 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -730 -410 0 0 {name=l6 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -530 -200 0 0 {name=l7 sig_type=std_logic lab=vss}
C {lab_wire.sym} -740 -450 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -160 -260 0 0 {name=l9 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -170 330 0 0 {name=l10 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 100 -350 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -760 410 0 0 {name=l12 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 170 310 0 0 {name=l13 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 100 200 0 0 {name=l14 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 170 -480 0 0 {name=l15 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -760 280 0 0 {name=l16 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -890 410 0 0 {name=l17 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -890 280 0 0 {name=l18 sig_type=std_logic lab=vss}
C {devices/iopin.sym} -760 -370 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -780 -330 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -760 -410 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -770 -70 0 0 {name=p4 lab=c2p}
C {devices/opin.sym} 340 -40 2 1 {name=p5 lab=pad}
C {devices/iopin.sym} -770 -450 2 0 {name=p6 lab=iovss}
C {devices/ipin.sym} -760 -30 0 0 {name=p7 lab=c2p_en}
C {sg13g2_Clamp_P2N2D.sym} -300 -410 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 130 -330 0 0 {name=X1}
C {sg13g2_GateDecode.sym} -660 -90 0 0 {name=X2}
C {sg13g2_Clamp_N2N2D.sym} -270 240 0 0 {name=X3}
C {sg13g2_DCNDiode.sym} 130 280 0 0 {name=X4}
C {ptap1.sym} -890 350 0 0 {name=R0 model=ptap1 w=4.625e-6 l=4.625e-6}
C {ptap1.sym} -760 350 0 0 {name=R1 model=ptap1 w=66.56e-6 l=66.56e-6}
C {devices/title-3.sym} -1530 820 0 0 {name=l1 author="IHP PDK AUTHORS"}
