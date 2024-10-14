v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 10 30 50 30 {
lab=vss}
N 50 -10 360 -10 {
lab=iovdd}
N 360 -10 360 10 {
lab=iovdd}
N 350 10 360 10 {
lab=iovdd}
N 350 50 430 50 {
lab=iovss}
N -350 10 -320 10 {
lab=iovss}
N 50 -60 50 -10 {
lab=iovdd}
N -20 -10 50 -10 {
lab=iovdd}
N 10 30 10 90 {
lab=vss}
N -20 30 10 30 {
lab=vss}
N 430 50 430 160 {
lab=iovss}
N -350 160 430 160 {
lab=iovss}
N -350 10 -350 160 {
lab=iovss}
N -400 10 -350 10 {
lab=iovss}
N 150 -120 240 -120 {
lab=vdd}
C {sg13g2_DCNDiode.sym} -170 10 2 1 {name=x1}
C {sg13g2_DCPDiode.sym} 200 30 0 0 {name=x2}
C {devices/iopin.sym} -400 10 2 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 50 -60 0 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 10 90 0 0 {name=vss lab=vss}
C {devices/iopin.sym} 240 -120 0 0 {name=vdd lab=vdd}
