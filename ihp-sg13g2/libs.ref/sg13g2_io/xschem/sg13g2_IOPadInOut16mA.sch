v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1630 -170 1700 -170 {
lab=pad}
N 1630 50 1700 50 {
lab=pad}
N 1770 -110 1900 -110 {
lab=iovss}
N 2200 -170 2200 -130 {
lab=pad}
N 1700 -190 2200 -190 {
lab=pad}
N 1700 -170 1700 50 {
lab=pad}
N 1700 -190 1700 -170 {
lab=pad}
N 2200 -90 2200 -40 {
lab=iovdd}
N 1700 50 1880 50 {
lab=pad}
N 2180 30 2200 30 {
lab=iovdd}
N 2200 -40 2200 30 {
lab=iovdd}
N 1860 130 2180 130 {
lab=iovss}
N 2180 70 2180 130 {
lab=iovss}
N 1250 -50 1250 50 {
lab=#net1}
N 1250 50 1330 50 {
lab=#net1}
N 1250 -170 1250 -90 {
lab=#net2}
N 1250 -170 1330 -170 {
lab=#net2}
N 1080 60 1080 90 {
lab=vss}
N 1080 -180 1080 -140 {
lab=vdd}
N 1300 -250 1300 -40 {
lab=iovdd}
N 1120 -250 1300 -250 {
lab=iovdd}
N 850 -50 950 -50 {
lab=c2p}
N 1360 -310 1360 -250 {
lab=iovdd}
N 1300 -250 1360 -250 {
lab=iovdd}
N 1770 -110 1770 130 {
lab=iovss}
N 1860 130 1860 190 {
lab=iovss}
N 1770 130 1860 130 {
lab=iovss}
N 2260 -170 2290 -170 {
lab=pad}
N 2200 -190 2200 -170 {
lab=pad}
N 1360 -250 1480 -250 {
lab=iovdd}
N 1480 -40 2200 -40 {
lab=iovdd}
N 1480 130 1770 130 {
lab=iovss}
N 860 -90 950 -90 {
lab=c2p_en}
N 1120 -250 1120 -140 {
lab=iovdd}
N 1480 -250 1480 -230 {
lab=iovdd}
N 1480 -110 1770 -110 {
lab=iovss}
N 1480 -40 1480 -10 {
lab=iovdd}
N 1300 -40 1480 -40 {
lab=iovdd}
N 1480 110 1480 130 {
lab=iovss}
N 2260 -170 2260 -30 {
lab=pad}
N 2200 -170 2260 -170 {
lab=pad}
N 2260 -30 2340 -30 {
lab=pad}
N 2450 50 2450 130 {
lab=iovss}
N 2180 130 2450 130 {
lab=iovss}
N 1480 -250 2450 -250 {
lab=iovdd}
N 2450 -250 2450 -110 {
lab=iovdd}
N 2530 50 2530 270 {
lab=vss}
N 1180 270 2530 270 {
lab=vss}
N 1180 60 1180 270 {
lab=vss}
N 1080 60 1180 60 {
lab=vss}
N 1080 0 1080 60 {
lab=vss}
N 2530 -340 2530 -110 {
lab=vdd}
N 1030 -340 2530 -340 {
lab=vdd}
N 1030 -340 1030 -180 {
lab=vdd}
N 1030 -180 1080 -180 {
lab=vdd}
N 1080 -230 1080 -180 {
lab=vdd}
N 2640 -30 2740 -30 {
lab=c2p}
C {sg13g2_DCNDiode.sym} 2050 -110 0 0 {name=x8}
C {sg13g2_DCPDiode.sym} 2030 50 0 0 {name=x9}
C {devices/iopin.sym} 1860 190 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 2290 -170 0 0 {name=pad lab=pad}
C {devices/iopin.sym} 1080 90 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 850 -50 2 0 {name=c2p lab=c2p}
C {devices/iopin.sym} 1080 -230 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 1360 -310 3 0 {name=iovdd lab=iovdd}
C {sg13g2_GateDecode.sym} 1100 -70 0 0 {name=x1}
C {devices/iopin.sym} 860 -90 2 0 {name=c2p_en lab=c2p_en}
C {sg13g2_Clamp_N8N8D.sym} 1480 -170 0 0 {name=x2}
C {sg13g2_Clamp_P8N8D.sym} 1480 50 0 0 {name=x3}
C {sg13g2_LevelDown.sym} 2490 -30 0 1 {name=x4}
C {devices/iopin.sym} 2740 -30 0 0 {name=p2c lab=p2c}
