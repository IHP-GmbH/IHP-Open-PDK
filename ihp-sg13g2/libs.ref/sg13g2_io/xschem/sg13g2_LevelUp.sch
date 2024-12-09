v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -90 -10 -90 10 {
lab=i_n}
N -160 -60 -130 -60 {
lab=i}
N -160 -10 -160 40 {
lab=i}
N -160 40 -130 40 {
lab=i}
N -200 -10 -160 -10 {
lab=i}
N -160 -60 -160 -10 {
lab=i}
N -90 -100 -90 -90 {
lab=vdd}
N -90 90 -90 110 {
lab=vss}
N 70 -10 70 20 {
lab=lvld}
N 220 -0 220 20 {
lab=lvld_n}
N 390 -10 390 20 {
lab=o}
N -90 -10 -0 -10 {
lab=i_n}
N -90 -30 -90 -10 {
lab=i_n}
N -0 -10 0 50 {
lab=i_n}
N 0 50 30 50 {
lab=i_n}
N 260 110 390 110 {
lab=vss}
N 390 80 390 110 {
lab=vss}
N 70 80 70 110 {
lab=vss}
N -90 110 70 110 {
lab=vss}
N 220 80 220 110 {
lab=vss}
N 180 110 220 110 {
lab=vss}
N 70 50 110 50 {
lab=vss}
N 110 50 110 110 {
lab=vss}
N 70 110 110 110 {
lab=vss}
N 220 50 260 50 {
lab=vss}
N 260 50 260 110 {
lab=vss}
N 220 110 260 110 {
lab=vss}
N 390 50 430 50 {
lab=vss}
N 430 50 430 110 {
lab=vss}
N 390 110 430 110 {
lab=vss}
N 70 -140 70 -110 {
lab=iovdd}
N 250 -140 390 -140 {
lab=iovdd}
N 390 -140 390 -100 {
lab=iovdd}
N 220 -140 220 -110 {
lab=iovdd}
N 180 -140 220 -140 {
lab=iovdd}
N 70 -80 110 -80 {
lab=iovdd}
N 110 -140 110 -80 {
lab=iovdd}
N 70 -140 110 -140 {
lab=iovdd}
N 220 -80 250 -80 {
lab=iovdd}
N 250 -140 250 -80 {
lab=iovdd}
N 220 -140 250 -140 {
lab=iovdd}
N 390 -70 430 -70 {
lab=iovdd}
N 430 -140 430 -70 {
lab=iovdd}
N 390 -140 430 -140 {
lab=iovdd}
N 320 -70 350 -70 {
lab=lvld_n}
N 320 0 320 50 {
lab=lvld_n}
N 320 50 350 50 {
lab=lvld_n}
N 220 -0 320 0 {
lab=lvld_n}
N 220 -30 220 -0 {
lab=lvld_n}
N 320 -70 320 0 {
lab=lvld_n}
N 10 -80 30 -80 {
lab=lvld_n}
N 10 -80 10 -30 {
lab=lvld_n}
N 10 -30 220 -30 {
lab=lvld_n}
N 220 -50 220 -30 {
lab=lvld_n}
N 70 -10 150 -10 {
lab=lvld}
N 70 -50 70 -10 {
lab=lvld}
N 150 -80 150 -10 {
lab=lvld}
N 150 -80 180 -80 {
lab=lvld}
N 390 -10 470 -10 {
lab=o}
N 390 -40 390 -10 {
lab=o}
N 180 110 180 150 {
lab=vss}
N 110 110 180 110 {
lab=vss}
N 180 -180 180 -140 {
lab=iovdd}
N 110 -140 180 -140 {
lab=iovdd}
N -160 40 -160 100 {
lab=i}
N -160 100 180 100 {
lab=i}
N 180 50 180 100 {
lab=i}
N -90 -60 -70 -60 {
lab=vdd}
N -70 -100 -70 -60 {
lab=vdd}
N -90 -100 -70 -100 {
lab=vdd}
N -90 -120 -90 -100 {
lab=vdd}
N -90 40 -70 40 {
lab=vss}
N -70 40 -70 90 {
lab=vss}
N -90 90 -70 90 {
lab=vss}
N -90 70 -90 90 {
lab=vss}
C {sg13g2_pr/sg13_lv_nmos.sym} -110 40 2 1 {name=M1
l=0.13u
w=2.75u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -110 -60 0 0 {name=M2
l=0.13u
w=4.75u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_nmos.sym} 50 50 0 0 {name=M3
l=0.45u
w=1.9u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_nmos.sym} 200 50 0 0 {name=M4
l=0.45u
w=1.9u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_nmos.sym} 370 50 0 0 {name=M5
l=0.45u
w=1.9u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 50 -80 0 0 {name=M6
l=0.45u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 200 -80 0 0 {name=M7
l=0.45u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 370 -70 0 0 {name=M8
l=0.45u
w=3.9u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/iopin.sym} 180 150 0 0 {name=vss lab=vss}
C {devices/iopin.sym} 180 -180 0 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} -90 -120 0 0 {name=vdd lab=vdd}
C {devices/ipin.sym} -200 -10 0 0 {name=i lab=i}
C {devices/opin.sym} 470 -10 0 0 {name=o lab=o}
C {devices/lab_pin.sym} -50 -10 0 0 {name=p1 sig_type=std_logic lab=i_n}
C {devices/lab_pin.sym} 100 -10 0 0 {name=p2 sig_type=std_logic lab=lvld}
C {devices/lab_pin.sym} 220 -20 0 0 {name=p3 sig_type=std_logic lab=lvld_n}
