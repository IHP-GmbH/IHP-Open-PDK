v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -740 -80 -630 -80 {lab=net_6}
N -740 -40 -630 -40 {lab=net_7}
N -460 -180 -460 -240 {lab=iovdd}
N -870 -320 -790 -320 {lab=vss}
N -850 -360 -790 -360 {lab=vdd}
N -480 -180 -480 -240 {lab=vdd}
N -440 360 -440 300 {lab=iovss}
N -850 -400 -790 -400 {lab=iovdd}
N -500 -180 -500 -240 {lab=vss}
N -520 120 -520 60 {lab=vdd}
N -440 120 -440 60 {lab=iovdd}
N -520 360 -520 300 {lab=vss}
N -860 -440 -780 -440 {lab=iovss}
N -700 210 -610 210 {lab=net_13}
N -230 -260 -210 -260 {lab=net_0}
N -150 -170 -150 -210 {lab=iovss}
N -930 320 -930 260 {lab=sub!}
N -150 -310 -150 -370 {lab=iovdd}
N -930 200 -930 130 {lab=vss}
N -20 -40 130 -40 {lab=net_3}
N -330 -40 -180 -40 {lab=net_9}
N -330 -120 -230 -120 {lab=net_0}
N -100 60 -100 20 {lab=iovss}
N -230 -120 -230 -260 {lab=net_0}
N -360 200 130 200 {lab=net_3}
N 330 -80 340 -80 {lab=net_3}
N 130 -40 130 -90 {lab=net_3}
N 130 -90 130 -260 {lab=net_3}
N 290 -210 230 -210 {lab=iovss}
N -10 -260 130 -260 {lab=net_3}
N 130 200 130 -40 {lab=net_3}
N 130 -90 330 -90 {lab=net_3}
N 340 -90 530 -90 {lab=net_3}
N 330 270 330 210 {lab=iovss}
N 290 130 230 130 {lab=iovdd}
N 330 -310 330 -370 {lab=iovdd}
N 330 -90 330 -190 {lab=net_3}
N 340 -80 340 -90 {lab=net_3}
N 330 90 330 -80 {lab=net_3}
N 330 -90 340 -90 {lab=net_3}
N -800 200 -800 130 {lab=iovss}
N -800 320 -800 260 {lab=sub!}
C {lab_wire.sym} -460 -210 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -830 -320 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -820 -360 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -480 -210 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -440 330 0 0 {name=l5 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -820 -400 0 0 {name=l6 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -500 -210 0 0 {name=l7 sig_type=std_logic lab=vss}
C {lab_wire.sym} -520 90 0 0 {name=l8 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -440 90 0 0 {name=l9 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -520 330 0 0 {name=l10 sig_type=std_logic lab=vss}
C {lab_wire.sym} -820 -440 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -150 -190 0 0 {name=l12 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -930 290 0 0 {name=l13 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -150 -340 0 0 {name=l14 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -930 160 0 0 {name=l15 sig_type=std_logic lab=vss}
C {lab_wire.sym} -100 40 0 0 {name=l16 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 260 -210 0 0 {name=l17 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 330 240 0 0 {name=l18 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 260 130 0 0 {name=l19 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 330 -340 0 0 {name=l20 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -800 160 0 0 {name=l21 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -800 290 0 0 {name=l22 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} -850 -360 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -870 -320 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -850 -400 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -740 -80 0 0 {name=p4 lab=c2p}
C {devices/ipin.sym} -740 -40 0 0 {name=p5 lab=c2p_en}
C {devices/iopin.sym} 530 -90 0 0 {name=p6 lab=pad}
C {devices/iopin.sym} -860 -440 2 0 {name=p7 lab=iovss}
C {devices/opin.sym} -700 210 2 0 {name=p8 lab=p2c}
C {sg13g2_Clamp_P15N15D.sym} -230 -250 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 290 -190 0 0 {name=X1}
C {sg13g2_GateDecode.sym} -630 -100 0 0 {name=X2}
C {sg13g2_Clamp_N15N15D.sym} -200 -40 0 0 {name=X3}
C {sg13g2_LevelDown.sym} -440 120 0 1 {name=X4}
C {sg13g2_DCNDiode.sym} 290 210 0 0 {name=X5}
C {ptap1.sym} -930 230 0 0 {name=R0 model=ptap1 w=4.375e-6 l=4.375e-6}
C {ptap1.sym} -800 230 0 0 {name=R1 model=ptap1 w=65.675e-6 l=65.675e-6}
C {devices/title-3.sym} -1450 840 0 0 {name=l1 author="IHP PDK AUTHORS"}
