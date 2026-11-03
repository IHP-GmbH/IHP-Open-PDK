v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -900 120 -790 120 {lab=net_6}
N -460 240 -460 140 {lab=net_8}
N -490 140 -460 140 {lab=net_8}
N -590 40 -590 -20 {lab=iovdd}
N -1000 -60 -920 -60 {lab=vss}
N -980 -100 -920 -100 {lab=vdd}
N -710 40 -710 -20 {lab=vdd}
N -980 -140 -920 -140 {lab=iovdd}
N -670 280 -670 220 {lab=vss}
N -990 -180 -920 -180 {lab=iovss}
N -230 240 -180 240 {lab=net_0}
N -210 -40 -180 -40 {lab=net_0}
N -460 -40 -410 -40 {lab=net_3}
N -180 160 -180 -40 {lab=net_0}
N -20 170 -20 160 {lab=net_0}
N -10 160 -10 -40 {lab=net_0}
N -310 360 -310 300 {lab=iovss}
N -460 240 -390 240 {lab=net_8}
N -10 160 180 160 {lab=net_0}
N -460 120 -460 -40 {lab=net_3}
N -490 120 -460 120 {lab=net_3}
N -350 70 -350 10 {lab=iovss}
N -350 -90 -350 -140 {lab=iovdd}
N -10 320 -10 170 {lab=net_0}
N -50 -60 -110 -60 {lab=iovss}
N -180 160 -20 160 {lab=net_0}
N -180 240 -180 160 {lab=net_0}
N -20 160 -10 160 {lab=net_0}
N -20 170 -10 170 {lab=net_0}
N -790 600 -790 540 {lab=sub!}
N -10 500 -10 440 {lab=iovss}
N -50 360 -110 360 {lab=iovdd}
N -10 -160 -10 -220 {lab=iovdd}
N -790 480 -790 400 {lab=iovss}
N -920 600 -920 540 {lab=sub!}
N -920 480 -920 410 {lab=vss}
C {lab_wire.sym} -590 10 0 0 {name=l1 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -960 -60 0 0 {name=l2 sig_type=std_logic lab=vss}
C {lab_wire.sym} -950 -100 0 0 {name=l3 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -710 10 0 0 {name=l4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} -950 -140 0 0 {name=l5 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -670 250 0 0 {name=l6 sig_type=std_logic lab=vss}
C {lab_wire.sym} -960 -180 0 0 {name=l7 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -310 330 0 0 {name=l8 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -350 40 0 0 {name=l9 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -350 -120 0 0 {name=l10 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -80 -60 0 0 {name=l11 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -790 570 0 0 {name=l12 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -10 470 0 0 {name=l13 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -80 360 0 0 {name=l14 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -10 -190 0 0 {name=l15 sig_type=std_logic lab=iovdd}
C {lab_wire.sym} -790 440 0 0 {name=l16 sig_type=std_logic lab=iovss}
C {lab_wire.sym} -920 570 0 0 {name=l17 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -920 440 0 0 {name=l18 sig_type=std_logic lab=vss}
C {devices/iopin.sym} -980 -100 2 0 {name=p1 lab=vdd}
C {devices/iopin.sym} -1000 -60 2 0 {name=p2 lab=vss}
C {devices/iopin.sym} -980 -140 2 0 {name=p3 lab=iovdd}
C {devices/ipin.sym} -900 120 0 0 {name=p4 lab=c2p}
C {devices/opin.sym} 180 160 2 1 {name=p5 lab=pad}
C {devices/iopin.sym} -990 -180 2 0 {name=p6 lab=iovss}
C {sg13g2_DCPDiode.sym} -50 -40 0 0 {name=X0}
C {sg13g2_Clamp_P15N15D.sym} -430 -30 0 0 {name=X1}
C {sg13g2_GateLevelUpInv.sym} -790 120 0 0 {name=X2}
C {sg13g2_Clamp_N15N15D.sym} -410 240 0 0 {name=X3}
C {sg13g2_DCNDiode.sym} -50 440 0 0 {name=X4}
C {ptap1.sym} -920 510 0 0 {name=R0 model=ptap1 w=4.68e-6 l=4.68e-6}
C {ptap1.sym} -790 510 0 0 {name=R1 model=ptap1 w=65.675e-6 l=65.675e-6}
C {devices/title-3.sym} -1660 1080 0 0 {name=l1 author="IHP PDK AUTHORS"}
