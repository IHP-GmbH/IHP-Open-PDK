v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -770 -70 -660 -70 {lab=net_6}
N -360 -110 -320 -110 {lab=net_0}
N -80 80 -40 80 {lab=net_3}
N -490 -170 -490 -230 {lab=iovdd}
N -780 -250 -700 -250 {lab=vss}
N -760 -290 -700 -290 {lab=vdd}
N -510 -170 -510 -230 {lab=vdd}
N -760 -330 -700 -330 {lab=iovdd}
N -530 -170 -530 -230 {lab=vss}
N -770 -370 -700 -370 {lab=iovss}
N -70 -210 -40 -210 {lab=net_3}
N -160 200 -160 140 {lab=iovss}
N -210 -260 -210 -320 {lab=iovdd}
N 150 40 150 -50 {lab=net_3}
N -320 80 -240 80 {lab=net_9}
N -40 -60 140 -60 {lab=net_3}
N 140 -50 150 -50 {lab=net_3}
N -320 -210 -270 -210 {lab=net_0}
N -760 -30 -660 -30 {lab=net_7}
N -360 -30 -320 -30 {lab=net_9}
N -40 80 -40 -60 {lab=net_3}
N -320 -110 -320 -210 {lab=net_0}
N 140 -60 150 -60 {lab=net_3}
N 150 -60 150 -180 {lab=net_3}
N 110 -200 50 -200 {lab=iovss}
N 150 -60 320 -60 {lab=net_3}
N -210 -100 -210 -160 {lab=iovss}
N -40 -60 -40 -210 {lab=net_3}
N -320 80 -320 -30 {lab=net_9}
N 140 -50 140 -60 {lab=net_3}
N -760 440 -760 380 {lab=sub!}
N 150 220 150 160 {lab=iovss}
N 110 80 50 80 {lab=iovdd}
N 150 -300 150 -360 {lab=iovdd}
N -760 320 -760 240 {lab=iovss}
N -890 440 -890 380 {lab=sub!}
N -890 320 -890 250 {lab=vss}
C {lab_wire.sym} -490 -200 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -740 -250 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -730 -290 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -510 -200 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -730 -330 0 0 {name=l5 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -530 -200 0 0 {name=l6 sig_type=std_logic lab=vss}
C {lab_wire.sym} -740 -370 0 0 {name=l7 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -160 170 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -210 -290 0 0 {name=l9 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 80 -200 0 0 {name=l10 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -210 -130 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -760 410 0 0 {name=l12 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 150 190 0 0 {name=l13 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 80 80 0 0 {name=l14 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 150 -330 0 0 {name=l15 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -760 280 0 0 {name=l16 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -890 410 0 0 {name=l17 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -890 280 0 0 {name=l18 sig_type=std_logic lab=vss}
C {devices/iopin.sym} -760 -290 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -780 -250 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -760 -330 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -770 -70 0 0 {name=p4 lab=c2p}
C {devices/opin.sym} 320 -60 2 1 {name=p5 lab=pad}
C {devices/iopin.sym} -770 -370 2 0 {name=p6 lab=iovss}
C {devices/ipin.sym} -760 -30 0 0 {name=p7 lab=c2p_en}
C {sg13g2_Clamp_P15N15D.sym} -290 -200 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 110 -180 0 0 {name=X1}
C {sg13g2_GateDecode.sym} -660 -90 0 0 {name=X2}
C {sg13g2_Clamp_N15N15D.sym} -260 80 0 0 {name=X3}
C {sg13g2_DCNDiode.sym} 110 160 0 0 {name=X4}
C {ptap1.sym} -890 350 0 0 {name=R0 model=ptap1 w=4.615e-6 l=4.615e-6}
C {ptap1.sym} -760 350 0 0 {name=R1 model=ptap1 w=66.56e-6 l=66.56e-6}
C {devices/title-3.sym} -1530 920 0 0 {name=l1 author="IHP PDK AUTHORS"}
