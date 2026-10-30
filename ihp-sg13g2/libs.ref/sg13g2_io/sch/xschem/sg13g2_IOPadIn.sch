v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 280 10 280 -30 {lab=net_3}
N 270 -30 280 -30 {lab=net_3}
N -450 -170 -370 -170 {lab=vss}
N -430 -210 -370 -210 {lab=vdd}
N -110 120 -110 60 {lab=iovss}
N -430 -250 -370 -250 {lab=iovdd}
N -190 -120 -190 -180 {lab=vdd}
N -110 -120 -110 -180 {lab=iovdd}
N -190 120 -190 60 {lab=vss}
N -440 -290 -370 -290 {lab=iovss}
N -370 -30 -280 -30 {lab=net_0}
N -30 -40 270 -40 {lab=net_3}
N 240 -110 180 -110 {lab=iovss}
N 270 -40 280 -40 {lab=net_3}
N 280 -40 280 -90 {lab=net_3}
N 280 -40 410 -40 {lab=net_3}
N 270 -30 270 -40 {lab=net_3}
N -530 210 -530 150 {lab=sub!}
N 280 190 280 130 {lab=iovss}
N 240 50 180 50 {lab=iovdd}
N 280 -210 280 -270 {lab=iovdd}
N -530 90 -530 10 {lab=iovss}
N -660 210 -660 150 {lab=sub!}
N -660 90 -660 20 {lab=vss}
C {lab_wire.sym} -410 -170 0 0 {name=l1 sig_type=std_logic lab=vss}
C {lab_wire.sym} -400 -210 0 0 {name=l2 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -110 90 0 0 {name=l3 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -400 -250 0 0 {name=l4 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -190 -150 0 0 {name=l5 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -110 -150 0 0 {name=l6 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -190 90 0 0 {name=l7 sig_type=std_logic lab=vss}
C {lab_wire.sym} -400 -290 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 210 -110 0 0 {name=l9 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -530 180 0 0 {name=l10 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 280 160 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} 210 50 0 0 {name=l12 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} 280 -240 0 0 {name=l13 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -530 50 0 0 {name=l14 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -660 180 0 0 {name=l15 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -660 60 0 0 {name=l16 sig_type=std_logic lab=vss}
C {devices/iopin.sym} -430 -210 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -450 -170 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -430 -250 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} 410 -40 2 0 {name=p4 lab=pad}
C {devices/iopin.sym} -440 -290 2 0 {name=p5 lab=iovss}
C {devices/opin.sym} -370 -30 2 0 {name=p6 lab=p2c}
C {sg13g2_LevelDown.sym} -110 -120 0 1 {name=X0}
C {sg13g2_DCPDiode.sym} 240 -90 0 0 {name=X1}
C {sg13g2_DCNDiode.sym} 240 130 0 0 {name=X2}
C {ptap1.sym} -660 120 0 0 {name=R0 model=ptap1 w=4.61e-6 l=4.61e-6}
C {ptap1.sym} -530 120 0 0 {name=R1 model=ptap1 w=73.145e-6 l=73.145e-6}
C {devices/title-3.sym} -1370 840 0 0 {name=l1 author="IHP PDK AUTHORS"}
