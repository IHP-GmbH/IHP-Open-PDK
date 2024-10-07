v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 820 -500 870 -500 {
lab=#net1}
N 870 -570 870 -500 {
lab=#net1}
N 870 -570 1000 -570 {
lab=#net1}
N 820 -460 870 -460 {
lab=#net2}
N 870 -460 870 -410 {
lab=#net2}
N 870 -410 1000 -410 {
lab=#net2}
N 690 -730 690 -560 {
lab=iovdd}
N 950 -730 1120 -730 {
lab=iovdd}
N 1120 -730 1120 -630 {
lab=iovdd}
N 950 -470 1120 -470 {
lab=iovdd}
N 950 -730 950 -470 {
lab=iovdd}
N 690 -730 950 -730 {
lab=iovdd}
N 910 -510 1120 -510 {
lab=iovss}
N 910 -510 910 -280 {
lab=iovss}
N 910 -280 1120 -280 {
lab=iovss}
N 1120 -350 1120 -280 {
lab=iovss}
N 1410 -410 1410 -280 {
lab=iovss}
N 1290 -280 1410 -280 {
lab=iovss}
N 1300 -570 1350 -570 {
lab=pad}
N 1350 -510 1350 -410 {
lab=pad}
N 1300 -410 1350 -410 {
lab=pad}
N 1710 -490 1710 -430 {
lab=pad}
N 1460 -510 1710 -510 {
lab=pad}
N 1350 -570 1350 -510 {
lab=pad}
N 1710 -390 1790 -390 {
lab=iovdd}
N 1790 -530 1790 -390 {
lab=iovdd}
N 1390 -530 1790 -530 {
lab=iovdd}
N 1390 -730 1390 -530 {
lab=iovdd}
N 1260 -730 1390 -730 {
lab=iovdd}
N 1460 -650 1460 -510 {
lab=pad}
N 1350 -510 1460 -510 {
lab=pad}
N 1760 -730 1760 -670 {
lab=iovdd}
N 1390 -730 1760 -730 {
lab=iovdd}
N 1760 -630 1820 -630 {
lab=iovss}
N 1820 -630 1820 -280 {
lab=iovss}
N 1410 -280 1820 -280 {
lab=iovss}
N 670 -400 670 -290 {
lab=vss}
N 640 -640 640 -560 {
lab=vdd}
N 450 -480 520 -480 {
lab=c2p}
N 1290 -280 1290 -250 {
lab=iovss}
N 1120 -280 1290 -280 {
lab=iovss}
N 1260 -780 1260 -730 {
lab=iovdd}
N 1120 -730 1260 -730 {
lab=iovdd}
N 1710 -490 1730 -490 {
lab=pad}
N 1710 -510 1710 -490 {
lab=pad}
C {sg13g2_Clamp_N2N2D.sym} 1150 -570 0 0 {name=x1}
C {sg13g2_Clamp_P2N2D.sym} 1150 -410 0 0 {name=x2}
C {sg13g2_GateLevelUpInv.sym} 670 -480 0 0 {name=x5}
C {devices/iopin.sym} 640 -640 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 670 -290 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 1290 -250 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 1260 -780 3 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 450 -480 2 0 {name=c2p lab=c2p}
C {devices/iopin.sym} 1730 -490 0 0 {name=pad lab=pad}
C {sg13g2_DCPDiode.sym} 1610 -650 0 0 {name=x3}
C {sg13g2_DCNDiode.sym} 1560 -410 0 0 {name=x4}
