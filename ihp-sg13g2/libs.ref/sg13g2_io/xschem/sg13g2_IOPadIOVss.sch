v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 2010 -220 2010 -150 {
lab=iovss}
N 1670 -130 1710 -130 {
lab=iovss}
N 1670 30 1690 30 {
lab=iovss}
N 1670 130 1670 170 {
lab=iovss}
N 1670 -130 1670 30 {
lab=iovss}
N 1990 10 2100 10 {
lab=iovdd}
N 2100 -110 2100 10 {
lab=iovdd}
N 2010 -110 2100 -110 {
lab=iovdd}
N 1990 50 1990 130 {
lab=iovss}
N 1670 130 1990 130 {
lab=iovss}
N 1670 30 1670 130 {
lab=iovss}
N 1670 -220 1670 -130 {
lab=iovss}
N 1670 -220 2010 -220 {
lab=iovss}
N 2100 -270 2100 -110 {
lab=iovdd}
N 1780 -320 1780 -270 {
lab=vdd}
N 1850 150 1850 200 {
lab=vdd}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_DCNDiode.sym} 1860 -130 0 0 {name=x8}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_DCPDiode.sym} 1840 30 0 0 {name=x9}
C {devices/iopin.sym} 1670 170 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 2100 -270 3 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 1780 -320 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 1850 200 1 0 {name=vss lab=vss}
