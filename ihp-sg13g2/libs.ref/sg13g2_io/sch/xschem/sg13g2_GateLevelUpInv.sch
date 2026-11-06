v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -80 -80 -80 -110 {lab=net_3}
N -190 10 -160 10 {lab=net_0}
N 240 -80 240 -110 {lab=net_3}
N -240 10 -190 10 {lab=net_0}
N -80 -110 240 -110 {lab=net_3}
N -20 -160 300 -160 {lab=net_1}
N 300 -80 300 -160 {lab=net_1}
N -80 130 -80 100 {lab=net_4}
N -80 130 240 130 {lab=net_4}
N 240 130 240 100 {lab=net_4}
N -190 180 -190 10 {lab=net_0}
N -190 180 150 180 {lab=net_0}
N 150 180 150 10 {lab=net_0}
N 150 10 160 10 {lab=net_0}
N 70 10 90 10 {lab=net_2}
N 390 10 430 10 {lab=net_5}
N -110 130 -80 130 {lab=net_4}
N -120 -110 -80 -110 {lab=net_3}
N -140 -160 -20 -160 {lab=net_1}
N -20 -80 -20 -160 {lab=net_1}
C {devices/opin.sym} 430 10 0 0 {name=p1 lab=pgate}
C {devices/ipin.sym} -240 10 0 0 {name=p2 lab=core}
C {devices/opin.sym} 70 10 0 0 {name=p3 lab=ngate}
C {devices/iopin.sym} -110 130 2 0 {name=p4 lab=vss}
C {devices/iopin.sym} -120 -110 2 0 {name=p5 lab=vdd}
C {devices/iopin.sym} -140 -160 2 0 {name=p6 lab=iovdd}
C {sg13g2_LevelUpInv.sym} -160 20 0 0 {name=X0}
C {sg13g2_LevelUpInv.sym} 160 20 0 0 {name=X1}
C {devices/title-3.sym} -1150 900 0 0 {name=l1 author="IHP PDK AUTHORS"}
