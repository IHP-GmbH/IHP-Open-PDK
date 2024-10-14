v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1620 -190 1690 -190 {
lab=pad}
N 1620 30 1690 30 {
lab=pad}
N 1760 -130 1890 -130 {
lab=iovss}
N 2190 -190 2190 -150 {
lab=pad}
N 1690 -210 2190 -210 {
lab=pad}
N 1690 -190 1690 30 {
lab=pad}
N 1690 -210 1690 -190 {
lab=pad}
N 2190 -110 2190 -60 {
lab=iovdd}
N 1690 30 1870 30 {
lab=pad}
N 2170 10 2190 10 {
lab=iovdd}
N 2190 -60 2190 10 {
lab=iovdd}
N 1850 110 2170 110 {
lab=iovss}
N 2170 50 2170 110 {
lab=iovss}
N 1240 -70 1240 30 {
lab=#net1}
N 1240 30 1320 30 {
lab=#net1}
N 1240 -190 1240 -110 {
lab=#net2}
N 1240 -190 1320 -190 {
lab=#net2}
N 1070 -20 1070 70 {
lab=vss}
N 1070 -250 1070 -160 {
lab=vdd}
N 1290 -270 1290 -60 {
lab=iovdd}
N 1110 -270 1290 -270 {
lab=iovdd}
N 840 -70 940 -70 {
lab=c2p}
N 1350 -330 1350 -270 {
lab=iovdd}
N 1290 -270 1350 -270 {
lab=iovdd}
N 1760 -130 1760 110 {
lab=iovss}
N 1850 110 1850 170 {
lab=iovss}
N 1760 110 1850 110 {
lab=iovss}
N 2190 -190 2280 -190 {
lab=pad}
N 2190 -210 2190 -190 {
lab=pad}
N 1350 -270 1470 -270 {
lab=iovdd}
N 1470 -60 2190 -60 {
lab=iovdd}
N 1470 110 1760 110 {
lab=iovss}
N 850 -110 940 -110 {
lab=c2p_en}
N 1110 -270 1110 -160 {
lab=iovdd}
N 1470 90 1470 110 {
lab=iovss}
N 1470 -60 1470 -30 {
lab=iovdd}
N 1290 -60 1470 -60 {
lab=iovdd}
N 1470 -130 1760 -130 {
lab=iovss}
N 1470 -270 1470 -250 {
lab=iovdd}
C {sg13g2_DCNDiode.sym} 2040 -130 0 0 {name=x8}
C {sg13g2_DCPDiode.sym} 2020 30 0 0 {name=x9}
C {devices/iopin.sym} 1850 170 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 2280 -190 0 0 {name=pad lab=pad}
C {devices/iopin.sym} 1070 70 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 840 -70 2 0 {name=c2p lab=c2p}
C {devices/iopin.sym} 1070 -250 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 1350 -330 3 0 {name=iovdd lab=iovdd}
C {sg13g2_GateDecode.sym} 1090 -90 0 0 {name=x1}
C {devices/iopin.sym} 850 -110 2 0 {name=c2p_en lab=c2p_en}
C {sg13g2_Clamp_N15N15D.sym} 1470 -190 0 0 {name=x2}
C {sg13g2_Clamp_P15N15D.sym} 1470 30 0 0 {name=x3}
