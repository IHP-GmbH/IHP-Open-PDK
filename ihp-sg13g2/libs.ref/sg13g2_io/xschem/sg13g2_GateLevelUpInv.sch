v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1030 -440 1030 -400 {
lab=vss}
N 1410 -400 1500 -400 {
lab=vss}
N 1500 -440 1500 -400 {
lab=vss}
N 1080 -610 1080 -580 {
lab=iovdd}
N 1530 -610 1550 -610 {
lab=iovdd}
N 1550 -610 1550 -580 {
lab=iovdd}
N 1500 -640 1500 -580 {
lab=vdd}
N 1180 -640 1500 -640 {
lab=vdd}
N 1030 -640 1030 -580 {
lab=vdd}
N 860 -510 900 -510 {
lab=core}
N 860 -510 860 -340 {
lab=core}
N 810 -510 860 -510 {
lab=core}
N 860 -340 1370 -340 {
lab=core}
N 1370 -510 1370 -340 {
lab=core}
N 1200 -510 1250 -510 {
lab=#net1}
N 1670 -510 1710 -510 {
lab=pgate}
N 1180 -690 1180 -640 {
lab=vdd}
N 1030 -640 1180 -640 {
lab=vdd}
N 1530 -680 1530 -610 {
lab=iovdd}
N 1080 -610 1530 -610 {
lab=iovdd}
N 1410 -400 1410 -310 {
lab=vss}
N 1030 -400 1410 -400 {
lab=vss}
C {sg13g2_LevelUpInv.sym} 1050 -510 0 0 {name=x1}
C {sg13g2_LevelUpInv.sym} 1520 -510 0 0 {name=x2}
C {devices/iopin.sym} 1180 -690 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 1530 -680 3 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 810 -510 2 0 {name=core lab=core}
C {devices/iopin.sym} 1410 -310 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 1710 -510 0 0 {name=pgate lab=pgate}
C {devices/iopin.sym} 1250 -510 0 0 {name=ngate lab=ngate}
