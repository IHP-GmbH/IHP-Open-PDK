v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 910 -360 940 -360 {
lab=pad}
N 820 -320 860 -320 {
lab=iovdd}
N 860 -460 860 -320 {
lab=iovdd}
N 860 -460 1300 -460 {
lab=iovdd}
N 1300 -460 1300 -380 {
lab=iovdd}
N 1240 -380 1300 -380 {
lab=iovdd}
N 1240 -340 1360 -340 {
lab=iovss}
N 1360 -500 1360 -340 {
lab=iovss}
N 500 -500 1360 -500 {
lab=iovss}
N 500 -500 500 -340 {
lab=iovss}
N 500 -340 520 -340 {
lab=iovss}
N 860 -180 910 -180 {
lab=pad}
N 910 -250 910 -180 {
lab=pad}
N 820 -360 910 -360 {
lab=pad}
N 510 -180 560 -180 {
lab=p2c}
N 670 -100 670 -60 {
lab=vss}
N 750 -80 750 -60 {
lab=iovss}
N 670 -290 670 -260 {
lab=vdd}
N 750 -270 750 -260 {
lab=iovdd}
N 910 -250 990 -250 {
lab=pad}
N 910 -360 910 -250 {
lab=pad}
N 750 -80 1360 -80 {
lab=iovss}
N 750 -100 750 -80 {
lab=iovss}
N 1360 -340 1360 -80 {
lab=iovss}
N 750 -270 860 -270 {
lab=iovdd}
N 750 -290 750 -270 {
lab=iovdd}
N 860 -320 860 -270 {
lab=iovdd}
C {sg13g2_DCNDiode.sym} 670 -340 0 0 {name=x1}
C {sg13g2_DCPDiode.sym} 1090 -360 0 0 {name=x2}
C {sg13g2_LevelDown.sym} 710 -180 0 0 {name=x3}
C {devices/iopin.sym} 750 -290 0 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 670 -290 0 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 670 -60 0 0 {name=vss lab=vss}
C {devices/iopin.sym} 750 -60 0 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 510 -180 2 0 {name=p2c lab=p2c}
C {devices/iopin.sym} 990 -250 0 0 {name=pad lab=pad}
