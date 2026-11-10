v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -740 -80 -630 -80 {lab=net_6}
N -330 -60 -290 -60 {lab=net_8}
N 70 210 70 -40 {lab=net_3}
N -430 -160 -430 -220 {lab=iovdd}
N -850 -330 -770 -330 {lab=vss}
N -830 -370 -770 -370 {lab=vdd}
N -550 -160 -550 -220 {lab=vdd}
N -830 -410 -770 -410 {lab=iovdd}
N -510 80 -510 20 {lab=vss}
N -840 -450 -770 -450 {lab=iovss}
N 340 -30 350 -30 {lab=net_3}
N -120 330 -120 270 {lab=iovss}
N 40 -360 70 -360 {lab=net_3}
N -100 -180 -100 -240 {lab=iovdd}
N -100 -470 -100 -530 {lab=iovss}
N -40 210 70 210 {lab=net_3}
N 350 110 350 -30 {lab=net_3}
N -290 -360 -240 -360 {lab=net_0}
N -290 210 -200 210 {lab=net_8}
N -290 -80 -290 -360 {lab=net_0}
N 350 -40 540 -40 {lab=net_3}
N 350 -40 350 -230 {lab=net_3}
N -290 210 -290 -60 {lab=net_8}
N 310 -250 250 -250 {lab=iovss}
N 70 -40 340 -40 {lab=net_3}
N 70 -40 70 -360 {lab=net_3}
N 340 -40 350 -40 {lab=net_3}
N -330 -80 -290 -80 {lab=net_0}
N 340 -30 340 -40 {lab=net_3}
N -760 440 -760 380 {lab=sub!}
N 350 290 350 230 {lab=iovss}
N 310 150 250 150 {lab=iovdd}
N 350 -350 350 -410 {lab=iovdd}
N -760 320 -760 240 {lab=iovss}
N -890 440 -890 380 {lab=sub!}
N -890 320 -890 250 {lab=vss}
C {lab_wire.sym} -430 -190 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -810 -330 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -800 -370 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -550 -190 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -800 -410 0 0 {name=l5 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -510 50 0 0 {name=l6 sig_type=std_logic lab=vss}
C {lab_wire.sym} -800 -450 0 0 {name=l7 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -120 300 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -100 -210 0 0 {name=l9 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -100 -500 0 0 {name=l10 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 280 -250 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -760 410 0 0 {name=l12 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 350 260 0 0 {name=l13 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 280 150 0 0 {name=l14 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 350 -380 0 0 {name=l15 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -760 280 0 0 {name=l16 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -890 410 0 0 {name=l17 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -890 280 0 0 {name=l18 sig_type=std_logic lab=vss}
C {devices/iopin.sym} -830 -370 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -850 -330 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -830 -410 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -740 -80 0 0 {name=p4 lab=c2p}
C {devices/opin.sym} 540 -40 2 1 {name=p5 lab=pad}
C {devices/iopin.sym} -840 -450 2 0 {name=p6 lab=iovss}
C {sg13g2_Clamp_P8N8D.sym} -240 -360 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 310 -230 0 0 {name=X1}
C {sg13g2_GateLevelUpInv.sym} -630 -80 0 0 {name=X2}
C {sg13g2_Clamp_N8N8D.sym} -220 210 0 0 {name=X3}
C {sg13g2_DCNDiode.sym} 310 230 0 0 {name=X4}
C {ptap1.sym} -890 350 0 0 {name=R0 model=ptap1 w=4.71e-6 l=4.71e-6}
C {ptap1.sym} -760 350 0 0 {name=R1 model=ptap1 w=66.56e-6 l=66.56e-6}
C {devices/title-3.sym} -1430 840 0 0 {name=l1 author="IHP PDK AUTHORS"}
