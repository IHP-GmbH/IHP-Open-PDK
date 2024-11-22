v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 110 -60 130 -60 {
lab=#net1}
N 110 10 110 50 {
lab=#net1}
N -0 10 110 10 {
lab=#net1}
N -0 -30 -0 10 {
lab=#net1}
N 110 -60 110 10 {
lab=#net1}
N -60 -60 -40 -60 {
lab=#net2}
N 80 110 170 110 {
lab=vss}
N -0 -110 -0 -90 {
lab=vdd}
N 80 -110 170 -110 {
lab=vdd}
N 170 -110 170 -90 {
lab=vdd}
N 80 -140 80 -110 {
lab=vdd}
N 30 -110 80 -110 {
lab=vdd}
N 80 110 80 140 {
lab=vss}
N 30 110 80 110 {
lab=vss}
N -60 -20 -60 60 {
lab=#net2}
N -490 -20 -430 -20 {
lab=pad}
N -280 40 -280 80 {
lab=iovss}
N -280 -130 -280 -80 {
lab=iovdd}
N -490 -20 -490 40 {
lab=pad}
N 170 -0 270 0 {
lab=core}
N 170 -30 170 -0 {
lab=core}
N 170 80 170 110 {
lab=vss}
N 170 -0 170 20 {
lab=core}
N 110 50 130 50 {
lab=#net1}
N 0 90 0 110 {
lab=vss}
N 0 10 -0 30 {
lab=#net1}
N -60 60 -40 60 {
lab=#net2}
N -0 60 30 60 {
lab=vss}
N 30 60 30 110 {
lab=vss}
N 0 110 30 110 {
lab=vss}
N 170 50 200 50 {
lab=vss}
N 200 50 200 110 {
lab=vss}
N 170 110 200 110 {
lab=vss}
N -0 -60 30 -60 {
lab=vdd}
N 30 -110 30 -60 {
lab=vdd}
N -0 -110 30 -110 {
lab=vdd}
N 170 -60 200 -60 {
lab=vdd}
N 200 -110 200 -60 {
lab=vdd}
N 170 -110 200 -110 {
lab=vdd}
N -130 -20 -60 -20 {
lab=#net2}
N -60 -60 -60 -20 {
lab=#net2}
C {sg13g2_pr/sg13_hv_nmos.sym} -20 60 2 1 {name=M1
l=0.45u
w=2.65u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} -20 -60 0 0 {name=M2
l=0.45u
w=4.65u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 150 50 2 1 {name=M3
l=0.13u
w=2.75u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 150 -60 0 0 {name=M4
l=0.13u
w=4.75u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_SecondaryProtection.sym} -280 -20 0 0 {}
C {devices/iopin.sym} 80 -140 0 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 80 140 0 0 {name=vss lab=vss}
C {devices/iopin.sym} -280 -130 0 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} -280 80 0 0 {name=iovss lab=iovss}
C {devices/iopin.sym} -490 40 0 0 {name=pad lab=pad}
C {devices/iopin.sym} 270 0 0 0 {name=core lab=core}
