v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {i_n} 970 -410 0 0 0.2 0.2 {}
T {lvld_n} 1080 -390 0 0 0.2 0.2 {}
T {lvld} 1230 -380 0 0 0.2 0.2 {}
N 870 -520 870 -480 {
lab=vdd}
N 870 -450 910 -450 {
lab=vdd}
N 910 -520 910 -450 {
lab=vdd}
N 870 -520 910 -520 {
lab=vdd}
N 870 -570 870 -520 {
lab=vdd}
N 870 -250 870 -220 {
lab=vss}
N 870 -340 910 -340 {
lab=vss}
N 910 -340 910 -270 {
lab=vss}
N 870 -270 910 -270 {
lab=vss}
N 870 -310 870 -270 {
lab=vss}
N 870 -390 870 -370 {
lab=#net1}
N 780 -450 830 -450 {
lab=i}
N 780 -400 780 -340 {
lab=i}
N 780 -340 830 -340 {
lab=i}
N 720 -400 780 -400 {
lab=i}
N 780 -450 780 -400 {
lab=i}
N 1110 -250 1250 -250 {
lab=vss}
N 870 -270 870 -250 {
lab=vss}
N 1250 -280 1250 -250 {
lab=vss}
N 1250 -330 1280 -330 {
lab=vss}
N 1280 -330 1280 -280 {
lab=vss}
N 1250 -280 1280 -280 {
lab=vss}
N 1250 -300 1250 -280 {
lab=vss}
N 1110 -280 1110 -250 {
lab=vss}
N 870 -250 1110 -250 {
lab=vss}
N 1110 -330 1140 -330 {
lab=vss}
N 1140 -330 1140 -280 {
lab=vss}
N 1110 -280 1140 -280 {
lab=vss}
N 1110 -300 1110 -280 {
lab=vss}
N 870 -390 1010 -390 {
lab=#net1}
N 870 -420 870 -390 {
lab=#net1}
N 1010 -390 1010 -330 {
lab=#net1}
N 1010 -330 1070 -330 {
lab=#net1}
N 1110 -390 1110 -360 {
lab=#net2}
N 1250 -410 1250 -360 {
lab=#net3}
N 1070 -410 1250 -410 {
lab=#net3}
N 1250 -460 1250 -410 {
lab=#net3}
N 1070 -490 1070 -410 {
lab=#net3}
N 1110 -430 1210 -430 {
lab=#net2}
N 1110 -460 1110 -430 {
lab=#net2}
N 1210 -490 1210 -430 {
lab=#net2}
N 1110 -560 1110 -520 {
lab=iovdd}
N 1190 -560 1250 -560 {
lab=iovdd}
N 1250 -560 1250 -520 {
lab=iovdd}
N 1250 -490 1290 -490 {
lab=iovdd}
N 1290 -560 1290 -490 {
lab=iovdd}
N 1250 -560 1290 -560 {
lab=iovdd}
N 1110 -490 1150 -490 {
lab=iovdd}
N 1150 -560 1150 -490 {
lab=iovdd}
N 1110 -560 1150 -560 {
lab=iovdd}
N 1190 -600 1190 -560 {
lab=iovdd}
N 1150 -560 1190 -560 {
lab=iovdd}
N 1460 -410 1460 -360 {
lab=xxx}
N 1370 -490 1420 -490 {
lab=#net4}
N 1370 -390 1370 -330 {
lab=#net4}
N 1370 -330 1420 -330 {
lab=#net4}
N 1460 -410 1550 -410 {
lab=xxx}
N 1460 -460 1460 -410 {
lab=xxx}
N 1460 -270 1460 -250 {
lab=vss}
N 1250 -250 1460 -250 {
lab=vss}
N 1460 -330 1490 -330 {
lab=vss}
N 1490 -330 1490 -270 {
lab=vss}
N 1460 -270 1490 -270 {
lab=vss}
N 1460 -300 1460 -270 {
lab=vss}
N 1460 -540 1460 -520 {
lab=iovdd}
N 1290 -560 1460 -560 {
lab=iovdd}
N 1460 -490 1490 -490 {
lab=iovdd}
N 1490 -540 1490 -490 {
lab=iovdd}
N 1460 -540 1490 -540 {
lab=iovdd}
N 1460 -560 1460 -540 {
lab=iovdd}
N 780 -340 780 -160 {}
N 780 -160 1200 -160 {}
N 1200 -330 1200 -160 {}
N 1200 -330 1210 -330 {}
N 1110 -390 1370 -390 {}
N 1110 -430 1110 -390 {
lab=#net2}
N 1370 -490 1370 -390 {
lab=#net4}
C {sg13g2_pr/sg13_lv_nmos.sym} 850 -340 2 1 {name=M1
l=0.13u
w=2.75u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 850 -450 0 0 {name=M2
l=0.13u
w=4.75u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_nmos.sym} 1090 -330 2 1 {name=M3
l=0.45u
w=1.9u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_nmos.sym} 1230 -330 2 1 {name=M4
l=0.45u
w=1.9u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 1090 -490 0 0 {name=M5
l=0.45u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 1230 -490 0 0 {name=M6
l=0.45u
w=0.3u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_nmos.sym} 1440 -330 0 0 {name=M7
l=0.45u
w=1.9u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 1440 -490 0 0 {name=M8
l=0.45u
w=3.9u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {devices/iopin.sym} 720 -400 2 0 {name=i lab=i}
C {devices/iopin.sym} 870 -220 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 870 -570 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 1190 -600 3 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 1550 -410 0 0 {name=o lab=o}
