v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1750 -150 1810 -150 {
lab=#net1}
N 1610 -250 1610 -200 {
lab=iovdd}
N 1970 -250 1970 -210 {
lab=iovdd}
N 1610 -100 1610 -50 {
lab=iovss}
N 1910 -50 1970 -50 {
lab=iovss}
N 1970 -90 1970 -50 {
lab=iovss}
N 2150 -150 2180 -150 {
lab=iovdd}
N 2150 -250 2150 -150 {
lab=iovdd}
N 2110 -150 2150 -150 {
lab=iovdd}
N 1970 -250 2150 -250 {
lab=iovdd}
N 1890 -250 1970 -250 {
lab=iovdd}
N 1890 -320 1890 -250 {
lab=iovdd}
N 1610 -250 1890 -250 {
lab=iovdd}
N 1910 -50 1910 30 {
lab=iovss}
N 1610 -50 1910 -50 {
lab=iovss}
N 1990 -320 1990 -290 {
lab=vdd}
N 2030 0 2030 30 {
lab=vss}
N 2180 -260 2180 -170 {
lab=#net2}
N 1450 -260 2180 -260 {
lab=#net2}
N 1450 -260 1450 -150 {
lab=#net2}
C {sg13g2_Clamp_N43N43D4R.sym} 1960 -150 0 0 {}
C {sg13g2_RCClampResistor.sym} 2330 -160 0 1 {name=x1}
C {sg13g2_RCClampInverter.sym} 1600 -150 0 0 {name=x2}
C {devices/iopin.sym} 1910 30 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 1890 -320 3 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 2030 30 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 1990 -320 3 0 {name=vdd lab=vdd}
