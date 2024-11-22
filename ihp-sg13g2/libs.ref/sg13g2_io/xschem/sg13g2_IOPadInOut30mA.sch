v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1440 -190 1510 -190 {
lab=pad}
N 1440 30 1510 30 {
lab=pad}
N 1580 -130 1710 -130 {
lab=iovss}
N 2010 -190 2010 -150 {
lab=pad}
N 1510 -210 2010 -210 {
lab=pad}
N 1510 -190 1510 30 {
lab=pad}
N 1510 -210 1510 -190 {
lab=pad}
N 2010 -110 2010 -60 {
lab=iovdd}
N 1510 30 1690 30 {
lab=pad}
N 1990 10 2010 10 {
lab=iovdd}
N 2010 -60 2010 10 {
lab=iovdd}
N 1670 110 1990 110 {
lab=iovss}
N 1990 50 1990 110 {
lab=iovss}
N 1060 -70 1060 30 {
lab=#net1}
N 1060 30 1140 30 {
lab=#net1}
N 1060 -190 1060 -110 {
lab=#net2}
N 1060 -190 1140 -190 {
lab=#net2}
N 890 40 890 70 {
lab=vss}
N 890 -200 890 -160 {
lab=vdd}
N 1110 -270 1110 -60 {
lab=iovdd}
N 930 -270 1110 -270 {
lab=iovdd}
N 660 -70 760 -70 {
lab=c2p}
N 1170 -330 1170 -270 {
lab=iovdd}
N 1110 -270 1170 -270 {
lab=iovdd}
N 1580 -130 1580 110 {
lab=iovss}
N 1670 110 1670 170 {
lab=iovss}
N 1580 110 1670 110 {
lab=iovss}
N 2070 -190 2100 -190 {
lab=pad}
N 2010 -210 2010 -190 {
lab=pad}
N 1170 -270 1290 -270 {
lab=iovdd}
N 1290 -60 2010 -60 {
lab=iovdd}
N 1290 110 1580 110 {
lab=iovss}
N 670 -110 760 -110 {
lab=c2p_en}
N 930 -270 930 -160 {
lab=iovdd}
N 1290 -270 1290 -250 {
lab=iovdd}
N 1290 -130 1580 -130 {
lab=iovss}
N 1290 -60 1290 -30 {
lab=iovdd}
N 1110 -60 1290 -60 {
lab=iovdd}
N 1290 90 1290 110 {
lab=iovss}
N 2070 -190 2070 -50 {
lab=pad}
N 2010 -190 2070 -190 {
lab=pad}
N 2070 -50 2150 -50 {
lab=pad}
N 2260 30 2260 110 {
lab=iovss}
N 1990 110 2260 110 {
lab=iovss}
N 1290 -270 2260 -270 {
lab=iovdd}
N 2260 -270 2260 -130 {
lab=iovdd}
N 2340 30 2340 250 {
lab=vss}
N 990 250 2340 250 {
lab=vss}
N 990 40 990 250 {
lab=vss}
N 890 40 990 40 {
lab=vss}
N 890 -20 890 40 {
lab=vss}
N 2340 -360 2340 -130 {
lab=vdd}
N 840 -360 2340 -360 {
lab=vdd}
N 840 -360 840 -200 {
lab=vdd}
N 840 -200 890 -200 {
lab=vdd}
N 890 -250 890 -200 {
lab=vdd}
N 2450 -50 2550 -50 {
lab=p2c}
C {sg13g2_DCNDiode.sym} 1860 -130 0 0 {name=x8}
C {sg13g2_DCPDiode.sym} 1840 30 0 0 {name=x9}
C {devices/iopin.sym} 1670 170 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 2100 -190 0 0 {name=pad lab=pad}
C {devices/iopin.sym} 890 70 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 660 -70 2 0 {name=c2p lab=c2p}
C {devices/iopin.sym} 890 -250 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 1170 -330 3 0 {name=iovdd lab=iovdd}
C {sg13g2_GateDecode.sym} 910 -90 0 0 {name=x1}
C {devices/iopin.sym} 670 -110 2 0 {name=c2p_en lab=c2p_en}
C {sg13g2_LevelDown.sym} 2300 -50 0 1 {name=x4}
C {devices/iopin.sym} 2550 -50 0 0 {name=p2c lab=p2c}
C {sg13g2_Clamp_N15N15D.sym} 1290 -190 0 0 {name=x5}
C {sg13g2_Clamp_P15N15D.sym} 1290 30 0 0 {name=x6}
