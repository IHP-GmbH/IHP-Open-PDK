v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 170 140 170 -20 {lab=net_12}
N 170 140 270 140 {lab=net_12}
N -50 230 200 230 {lab=net_6}
N 200 230 200 -170 {lab=net_6}
N -110 -260 -60 -260 {lab=net_3}
N 200 -170 250 -170 {lab=net_6}
N -480 -260 -450 -260 {lab=net_2}
N -20 -20 170 -20 {lab=net_12}
N -60 -150 -60 -260 {lab=net_3}
N -330 -150 -60 -150 {lab=net_3}
N -330 0 -330 -150 {lab=net_3}
N -330 0 -260 0 {lab=net_3}
N -450 -260 -290 -260 {lab=net_2}
N -450 250 -450 -260 {lab=net_2}
N -450 250 -250 250 {lab=net_2}
N -300 -40 -260 -40 {lab=net_11}
N -300 210 -300 130 {lab=net_11}
N -300 210 -250 210 {lab=net_11}
N -300 130 -300 -40 {lab=net_11}
N -350 130 -300 130 {lab=net_11}
N 480 -170 560 -170 {lab=net_8}
N 500 140 560 140 {lab=net_16}
N 310 290 370 290 {lab=net_18}
N 370 290 370 230 {lab=net_18}
N 350 -50 350 -80 {lab=vss}
N 220 -300 330 -300 {lab=net_9}
N 330 -260 330 -300 {lab=net_9}
N 390 -260 390 -350 {lab=net_7}
N 230 -350 390 -350 {lab=net_7}
N 350 50 350 -10 {lab=vdd}
N -170 370 -170 330 {lab=vss}
N 410 50 410 -10 {lab=iovdd}
N -160 100 -160 60 {lab=vss}
N -170 150 -170 110 {lab=vdd}
N -160 -100 -160 -140 {lab=vdd}
N -210 -300 -210 -370 {lab=vdd}
N -210 -170 -210 -220 {lab=vss}
N 50 -300 50 -370 {lab=vss}
N 70 -300 70 -370 {lab=vdd}
C {lab_wire.sym} 350 -60 0 0 {name=l1 sig_type=std_logic lab=vss}
C {lab_wire.sym} 350 20 0 0 {name=l2 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -170 350 0 0 {name=l3 sig_type=std_logic lab=vss}
C {lab_wire.sym} 410 20 0 0 {name=l4 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -160 80 0 0 {name=l5 sig_type=std_logic lab=vss}
C {lab_wire.sym} -170 130 0 0 {name=l6 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -160 -120 0 0 {name=l7 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -210 -340 0 0 {name=l8 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -210 -200 0 0 {name=l9 sig_type=std_logic lab=vss}
C {lab_wire.sym} 50 -340 0 0 {name=l10 sig_type=std_logic lab=vss}
C {lab_wire.sym} 70 -340 0 0 {name=l11 sig_type=std_logic lab=vdd}
C {devices/opin.sym} 560 -170 0 0 {name=p1 lab=pgate}
C {devices/opin.sym} 560 140 0 0 {name=p2 lab=ngate}
C {devices/ipin.sym} -480 -260 0 0 {name=p3 lab=en}
C {devices/ipin.sym} -350 130 0 0 {name=p4 lab=core}
C {devices/iopin.sym} 230 -350 2 0 {name=p5 lab=iovdd}
C {devices/iopin.sym} 220 -300 2 0 {name=p6 lab=vdd}
C {devices/iopin.sym} 310 290 2 0 {name=p7 lab=vss}
C {sg13g2_io_tie.sym} 50 -300 0 0 {name=X0}
C {sg13g2_io_inv_x1.sym} -290 -260 0 0 {name=X1}
C {sg13g2_LevelUp.sym} 250 -160 0 0 {name=X2}
C {sg13g2_io_nor2_x1.sym} -260 -40 0 0 {name=X3}
C {sg13g2_LevelUp.sym} 270 150 0 0 {name=X4}
C {sg13g2_io_nand2_x1.sym} -250 230 0 0 {name=X5}
C {devices/title-3.sym} -1210 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
