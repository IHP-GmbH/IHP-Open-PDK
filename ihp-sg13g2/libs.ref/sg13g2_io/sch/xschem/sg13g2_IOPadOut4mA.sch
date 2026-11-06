v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -740 -80 -630 -80 {lab=net_6}
N -10 80 100 80 {lab=net_3}
N -430 -160 -430 -220 {lab=iovdd}
N -890 -320 -810 -320 {lab=vss}
N -870 -360 -810 -360 {lab=vdd}
N -550 -160 -550 -220 {lab=vdd}
N -870 -400 -810 -400 {lab=iovdd}
N -510 80 -510 20 {lab=vss}
N -270 80 -170 80 {lab=net_8}
N -90 200 -90 140 {lab=iovss}
N -270 80 -270 -60 {lab=net_8}
N -880 -440 -810 -440 {lab=iovss}
N 330 20 330 -120 {lab=net_3}
N -90 -440 -90 -490 {lab=iovss}
N 100 -130 320 -130 {lab=net_3}
N -330 -60 -270 -60 {lab=net_8}
N -330 -80 -270 -80 {lab=net_0}
N -90 -150 -90 -210 {lab=iovdd}
N -270 -80 -270 -330 {lab=net_0}
N -270 -330 -230 -330 {lab=net_0}
N 320 -120 320 -130 {lab=net_3}
N 320 -120 330 -120 {lab=net_3}
N 320 -130 330 -130 {lab=net_3}
N 330 -130 490 -130 {lab=net_3}
N 290 -310 230 -310 {lab=iovss}
N 50 -330 100 -330 {lab=net_3}
N 100 80 100 -130 {lab=net_3}
N 100 -130 100 -330 {lab=net_3}
N 330 -130 330 -290 {lab=net_3}
N -940 340 -940 270 {lab=vss}
N 330 200 330 140 {lab=iovss}
N 290 60 230 60 {lab=iovdd}
N 330 -410 330 -470 {lab=iovdd}
N -810 460 -810 400 {lab=sub!}
N -940 460 -940 400 {lab=sub!}
N -810 340 -810 270 {lab=iovss}
C {lab_wire.sym} -430 -190 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -850 -320 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -840 -360 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -550 -190 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -840 -400 0 0 {name=l5 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -510 50 0 0 {name=l6 sig_type=std_logic lab=vss}
C {lab_wire.sym} -90 170 0 0 {name=l7 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -840 -440 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -90 -460 0 0 {name=l9 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -90 -180 0 0 {name=l10 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 260 -310 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -940 300 0 0 {name=l12 sig_type=std_logic lab=vss}
C {lab_wire.sym} 330 170 0 0 {name=l13 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 260 60 0 0 {name=l14 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 330 -440 0 0 {name=l15 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -810 430 0 0 {name=l16 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -940 430 0 0 {name=l17 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -810 300 0 0 {name=l18 sig_type=std_logic lab=iovss}
C {devices/iopin.sym} -870 -360 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -890 -320 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -870 -400 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -740 -80 0 0 {name=p4 lab=c2p}
C {devices/opin.sym} 490 -130 2 1 {name=p5 lab=pad}
C {devices/iopin.sym} -880 -440 2 0 {name=p6 lab=iovss}
C {sg13g2_Clamp_P2N2D.sym} -230 -330 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 290 -290 0 0 {name=X1}
C {sg13g2_GateLevelUpInv.sym} -630 -80 0 0 {name=X2}
C {sg13g2_Clamp_N2N2D.sym} -190 80 0 0 {name=X3}
C {sg13g2_DCNDiode.sym} 290 140 0 0 {name=X4}
C {ptap1.sym} -940 370 0 0 {name=R0 model=ptap1 w=4.68e-6 l=4.68e-6}
C {ptap1.sym} -810 370 0 0 {name=R1 model=ptap1 w=65.9e-6 l=65.9e-6}
C {devices/title-3.sym} -1470 860 0 0 {name=l1 author="IHP PDK AUTHORS"}
