v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 160 -190 160 -170 {
lab=vdd}
N 160 -140 220 -140 {
lab=vdd}
N 220 -190 220 -140 {
lab=vdd}
N 160 -190 220 -190 {
lab=vdd}
N 160 -220 160 -190 {
lab=vdd}
N 80 -140 120 -140 {
lab=i}
N 80 -90 80 -40 {
lab=i}
N 40 -90 80 -90 {
lab=i}
N 80 -140 80 -90 {
lab=i}
N 160 -90 160 -70 {
lab=nq}
N 160 20 160 50 {
lab=vss}
N 160 -40 210 -40 {
lab=vss}
N 210 -40 210 20 {
lab=vss}
N 160 20 210 20 {
lab=vss}
N 160 -10 160 20 {
lab=vss}
N 80 -40 120 -40 {
lab=i}
N 160 -90 260 -90 {
lab=nq}
N 160 -110 160 -90 {
lab=nq}
C {sg13g2_pr/sg13_lv_pmos.sym} 140 -140 0 0 {name=M2
l=0.13u
w=4.41u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 140 -40 2 1 {name=M1
l=0.13u
w=3.93u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {devices/ipin.sym} 40 -90 0 0 {name=i lab=i}
C {devices/iopin.sym} 160 -220 0 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 160 50 0 0 {name=vss lab=vss}
C {devices/opin.sym} 260 -90 0 0 {name=nq lab=nq}
