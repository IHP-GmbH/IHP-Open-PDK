v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -740 -80 -630 -80 {lab=net_6}
N -740 -40 -630 -40 {lab=net_7}
N -460 -180 -460 -240 {lab=iovdd}
N -760 -340 -660 -340 {lab=vss}
N -730 -380 -660 -380 {lab=vdd}
N -480 -180 -480 -240 {lab=vdd}
N -430 350 -430 290 {lab=iovss}
N -730 -420 -660 -420 {lab=iovdd}
N -500 -180 -500 -240 {lab=vss}
N -510 110 -510 50 {lab=vdd}
N -430 110 -430 50 {lab=iovdd}
N -510 350 -510 290 {lab=vss}
N 70 -420 110 -420 {lab=net_3}
N -740 -460 -660 -460 {lab=iovss}
N 270 -120 280 -120 {lab=net_3}
N -70 80 -70 20 {lab=iovss}
N -220 -420 -210 -420 {lab=net_0}
N -70 -240 -70 -300 {lab=iovdd}
N -740 200 -600 200 {lab=net_13}
N -220 -120 -220 -420 {lab=net_0}
N -70 -590 -70 -530 {lab=iovss}
N -330 -40 -150 -40 {lab=net_9}
N 110 190 110 -40 {lab=net_3}
N -330 -120 -220 -120 {lab=net_0}
N 280 10 280 -120 {lab=net_3}
N 280 -130 280 -300 {lab=net_3}
N -350 190 110 190 {lab=net_3}
N 10 -40 110 -40 {lab=net_3}
N 110 -130 110 -420 {lab=net_3}
N 240 -320 180 -320 {lab=iovss}
N 280 -130 410 -130 {lab=net_3}
N 270 -130 280 -130 {lab=net_3}
N 110 -130 270 -130 {lab=net_3}
N 110 -40 110 -130 {lab=net_3}
N 270 -120 270 -130 {lab=net_3}
N -760 320 -760 240 {lab=iovss}
N 280 190 280 130 {lab=iovss}
N 240 50 180 50 {lab=iovdd}
N 280 -420 280 -480 {lab=iovdd}
N -760 440 -760 380 {lab=sub!}
N -920 440 -920 380 {lab=sub!}
N -920 320 -920 250 {lab=vss}
C {lab_wire.sym} -460 -210 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -710 -340 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -700 -380 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -480 -210 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -430 320 0 0 {name=l5 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -700 -420 0 0 {name=l6 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -500 -210 0 0 {name=l7 sig_type=std_logic lab=vss}
C {lab_wire.sym} -510 80 0 0 {name=l8 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -430 80 0 0 {name=l9 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -510 320 0 0 {name=l10 sig_type=std_logic lab=vss}
C {lab_wire.sym} -700 -460 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -70 50 0 0 {name=l12 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -70 -270 0 0 {name=l13 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -70 -560 0 0 {name=l14 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 210 -320 0 0 {name=l15 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -760 280 0 0 {name=l16 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 280 160 0 0 {name=l17 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 210 50 0 0 {name=l18 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 280 -450 0 0 {name=l19 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -760 410 0 0 {name=l20 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -920 410 0 0 {name=l21 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -920 280 0 0 {name=l22 sig_type=std_logic lab=vss}
C {devices/iopin.sym} -730 -380 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -760 -340 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -730 -420 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -740 -80 0 0 {name=p4 lab=c2p}
C {devices/ipin.sym} -740 -40 0 0 {name=p5 lab=c2p_en}
C {devices/iopin.sym} 410 -130 0 0 {name=p6 lab=pad}
C {devices/iopin.sym} -740 -460 2 0 {name=p7 lab=iovss}
C {devices/opin.sym} -740 200 2 0 {name=p8 lab=p2c}
C {sg13g2_Clamp_P8N8D.sym} -210 -420 0 0 {name=X0}
C {sg13g2_DCPDiode.sym} 240 -300 0 0 {name=X1}
C {sg13g2_GateDecode.sym} -630 -100 0 0 {name=X2}
C {sg13g2_Clamp_N8N8D.sym} -170 -40 0 0 {name=X3}
C {sg13g2_LevelDown.sym} -430 110 0 1 {name=X4}
C {sg13g2_DCNDiode.sym} 240 130 0 0 {name=X5}
C {ptap1.sym} -920 350 0 0 {name=R0 model=ptap1 w=4.355e-6 l=4.355e-6}
C {ptap1.sym} -760 350 0 0 {name=R1 model=ptap1 w=66.71e-6 l=66.71e-6}
C {devices/title-3.sym} -1510 800 0 0 {name=l1 author="IHP PDK AUTHORS"}
