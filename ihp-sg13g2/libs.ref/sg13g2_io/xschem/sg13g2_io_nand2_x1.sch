v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -20 -160 -20 -110 {
lab=nq}
N 60 -110 190 -110 {
lab=nq}
N 190 -160 190 -110 {
lab=nq}
N 60 -90 60 -70 {
lab=nq}
N -20 -110 60 -110 {
lab=nq}
N 60 -10 60 40 {
lab=#net1}
N -20 -250 -20 -220 {
lab=vdd}
N 70 -280 190 -280 {
lab=vdd}
N 190 -240 190 -220 {
lab=vdd}
N 70 -340 70 -280 {
lab=vdd}
N -20 -280 70 -280 {
lab=vdd}
N 60 120 60 160 {
lab=vss}
N -30 -40 20 -40 {
lab=i1}
N -130 -190 -60 -190 {
lab=i0}
N 90 -190 150 -190 {
lab=i1}
N -20 -190 30 -190 {
lab=vdd}
N 30 -250 30 -190 {
lab=vdd}
N -20 -250 30 -250 {
lab=vdd}
N -20 -280 -20 -250 {
lab=vdd}
N 190 -190 240 -190 {
lab=vdd}
N 240 -240 240 -190 {
lab=vdd}
N 190 -240 240 -240 {
lab=vdd}
N 190 -280 190 -240 {
lab=vdd}
N 60 70 120 70 {
lab=vss}
N 120 70 120 120 {
lab=vss}
N 60 120 120 120 {
lab=vss}
N 60 100 60 120 {
lab=vss}
N 60 -40 150 -40 {
lab=vss}
N 150 -40 150 120 {
lab=vss}
N 120 120 150 120 {
lab=vss}
N -130 70 20 70 {
lab=i0}
N -130 -190 -130 70 {
lab=i0}
N -180 70 -130 70 {
lab=i0}
N -30 -130 -30 -40 {
lab=i1}
N -60 -40 -30 -40 {
lab=i1}
N -30 -130 90 -130 {
lab=i1}
N 90 -190 90 -130 {
lab=i1}
N 60 -90 300 -90 {
lab=nq}
N 60 -110 60 -90 {
lab=nq}
C {sg13g2_pr/sg13_lv_pmos.sym} 170 -190 0 0 {name=M2
l=0.13u
w=4.41u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 40 -40 2 1 {name=M3
l=0.13u
w=3.93u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 40 70 2 1 {name=M4
l=0.13u
w=3.93u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -40 -190 0 0 {name=M5
l=0.13u
w=4.41u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/iopin.sym} 70 -340 0 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 60 160 0 0 {name=vss lab=vss}
C {devices/ipin.sym} -180 70 0 0 {name=i0 lab=i0}
C {devices/ipin.sym} -60 -40 0 0 {name=i1 lab=i1}
C {devices/opin.sym} 300 -90 0 0 {name=nq lab=nq}
