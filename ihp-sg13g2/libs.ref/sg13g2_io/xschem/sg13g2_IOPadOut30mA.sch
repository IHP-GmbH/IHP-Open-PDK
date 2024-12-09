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
N 1480 -40 1480 -10 {
lab=iovdd}
N 1480 -40 2200 -40 {
lab=iovdd}
N 2200 -90 2200 -40 {
lab=iovdd}
N 1700 50 1880 50 {
lab=pad}
N 2180 30 2200 30 {
lab=iovdd}
N 2200 -40 2200 30 {
lab=iovdd}
N 1480 110 1480 130 {
lab=iovss}
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
N 1100 10 1100 100 {
lab=vss}
N 1070 -240 1070 -150 {
lab=vdd}
N 1120 -250 1120 -150 {
lab=iovdd}
N 1360 -250 1480 -250 {
lab=iovdd}
N 1480 -250 1480 -230 {
lab=iovdd}
N 1300 -40 1480 -40 {
lab=iovdd}
N 1300 -250 1300 -40 {
lab=iovdd}
N 1120 -250 1300 -250 {
lab=iovdd}
N 850 -70 950 -70 {
lab=c2p}
N 1360 -310 1360 -250 {
lab=iovdd}
N 1300 -250 1360 -250 {
lab=iovdd}
N 1770 -110 1770 130 {
lab=iovss}
N 1480 -110 1770 -110 {
lab=iovss}
N 1480 130 1770 130 {
lab=iovss}
N 1860 130 1860 190 {
lab=iovss}
N 1770 130 1860 130 {
lab=iovss}
N 2200 -170 2290 -170 {
lab=pad}
N 2200 -190 2200 -170 {
lab=pad}
C {sg13g2_Clamp_N15N15D.sym} 1480 -170 0 0 {name=x1}
C {sg13g2_Clamp_P15N15D.sym} 1480 50 0 0 {name=x2}
C {sg13g2_DCNDiode.sym} 2050 -110 0 0 {name=x8}
C {sg13g2_DCPDiode.sym} 2030 50 0 0 {name=x9}
C {sg13g2_GateLevelUpInv.sym} 1100 -70 0 0 {name=x10}
C {devices/iopin.sym} 1860 190 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 2290 -170 0 0 {name=pad lab=pad}
C {devices/iopin.sym} 1100 100 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 850 -70 2 0 {name=c2p lab=c2p}
C {devices/iopin.sym} 1070 -240 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 1360 -310 3 0 {name=iovdd lab=iovdd}
