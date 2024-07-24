v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 40 -120 40 -90 {
lab=#net1}
N -30 0 -30 20 {
lab=nq}
N 40 0 120 0 {
lab=nq}
N -30 90 -30 110 {
lab=vss}
N 40 110 120 110 {
lab=vss}
N 120 100 120 110 {
lab=vss}
N 40 -20 40 0 {
lab=nq}
N -30 0 40 0 {
lab=nq}
N 40 -200 40 -180 {
lab=vdd}
N 40 -150 100 -150 {
lab=vdd}
N 100 -200 100 -150 {
lab=vdd}
N 40 -200 100 -200 {
lab=vdd}
N 40 -230 40 -200 {
lab=vdd}
N 40 -60 120 -60 {
lab=vdd}
N 120 -200 120 -60 {
lab=vdd}
N 100 -200 120 -200 {
lab=vdd}
N 40 110 40 160 {
lab=vss}
N -30 110 40 110 {
lab=vss}
N -30 -60 -0 -60 {
lab=i0}
N -110 50 -70 50 {
lab=i1}
N -30 50 0 50 {
lab=vss}
N 0 50 -0 90 {
lab=vss}
N -30 90 -0 90 {
lab=vss}
N -30 80 -30 90 {
lab=vss}
N 120 50 150 50 {
lab=vss}
N 120 100 150 100 {
lab=vss}
N 40 -20 210 -20 {
lab=nq}
N 40 -30 40 -20 {
lab=nq}
N 120 80 120 100 {
lab=vss}
N 120 0 120 20 {
lab=nq}
N 150 50 150 100 {
lab=vss}
N -110 -150 -0 -150 {
lab=i1}
N -110 -150 -110 50 {
lab=i1}
N -120 50 -110 50 {
lab=i1}
N -30 -60 -30 -10 {}
N -50 -60 -30 -60 {
lab=i0}
N -30 -10 30 -10 {}
N 30 -10 30 50 {}
N 30 50 80 50 {}
C {sg13g2_pr/sg13_lv_nmos.sym} -50 50 2 1 {name=M1
l=0.13u
w=3.93u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 20 -150 0 0 {name=M2
l=0.13u
w=4.41u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 100 50 2 1 {name=M3
l=0.13u
w=3.93u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 20 -60 0 0 {name=M4
l=0.13u
w=4.41u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/iopin.sym} 40 160 0 0 {name=vss lab=vss}
C {devices/iopin.sym} 40 -230 0 0 {name=vdd lab=vdd}
C {devices/ipin.sym} -50 -60 0 0 {name=i0 lab=i0}
C {devices/ipin.sym} -120 50 0 0 {name=i2 lab=i1}
C {devices/opin.sym} 210 -20 0 0 {name=nq lab=nq}
