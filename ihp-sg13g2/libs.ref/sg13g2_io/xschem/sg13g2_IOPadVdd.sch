v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 70 -160 70 -60 {
lab=vdd}
N 680 -190 680 -100 {
lab=iovdd}
N 680 20 680 80 {
lab=iovss}
N 430 -40 520 -40 {
lab=#net1}
N 70 -40 130 -40 {
lab=#net2}
N 820 -250 820 -40 {
lab=vdd}
N 520 -250 820 -250 {
lab=vdd}
N 290 10 290 60 {
lab=vss}
N 520 -290 520 -250 {
lab=vdd}
N 290 -160 290 -90 {
lab=vdd}
N 70 -160 290 -160 {
lab=vdd}
N 290 -250 290 -160 {
lab=vdd}
N 290 -250 520 -250 {
lab=vdd}
C {sg13g2_RCClampResistor.sym} -80 -50 0 0 {name=x6}
C {devices/iopin.sym} 520 -290 0 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 680 -190 0 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 290 60 0 0 {name=vss lab=vss}
C {devices/iopin.sym} 680 80 0 0 {name=iovss lab=iovss}
C {sg13g2_RCClampInverter.sym} 280 -40 0 0 {name=x1}
C {sg13g2_Clamp_N43N43D4R.sym} 670 -40 0 0 {}
