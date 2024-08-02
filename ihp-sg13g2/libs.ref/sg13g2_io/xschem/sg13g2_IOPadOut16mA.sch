v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 700 -720 770 -720 {
lab=pad}
N 700 -500 770 -500 {
lab=pad}
N 840 -660 970 -660 {
lab=iovss}
N 1270 -720 1270 -680 {
lab=pad}
N 770 -740 1270 -740 {
lab=pad}
N 770 -720 770 -500 {
lab=pad}
N 770 -740 770 -720 {
lab=pad}
N 550 -590 550 -560 {
lab=iovdd}
N 550 -590 1270 -590 {
lab=iovdd}
N 1270 -640 1270 -590 {
lab=iovdd}
N 770 -500 950 -500 {
lab=pad}
N 1250 -520 1270 -520 {
lab=iovdd}
N 1270 -590 1270 -520 {
lab=iovdd}
N 550 -440 550 -420 {
lab=iovss}
N 930 -420 1250 -420 {
lab=iovss}
N 1250 -480 1250 -420 {
lab=iovss}
N 320 -600 320 -500 {
lab=#net1}
N 320 -500 400 -500 {
lab=#net1}
N 320 -720 320 -640 {
lab=#net2}
N 320 -720 400 -720 {
lab=#net2}
N 170 -540 170 -450 {
lab=vss}
N 140 -790 140 -700 {
lab=vdd}
N 190 -800 190 -700 {
lab=iovdd}
N 430 -800 550 -800 {
lab=iovdd}
N 550 -800 550 -780 {
lab=iovdd}
N 370 -590 550 -590 {
lab=iovdd}
N 370 -800 370 -590 {
lab=iovdd}
N 190 -800 370 -800 {
lab=iovdd}
N -80 -620 20 -620 {
lab=c2p}
N 430 -860 430 -800 {
lab=iovdd}
N 370 -800 430 -800 {
lab=iovdd}
N 840 -660 840 -420 {
lab=iovss}
N 550 -660 840 -660 {
lab=iovss}
N 550 -420 840 -420 {
lab=iovss}
N 930 -420 930 -360 {
lab=iovss}
N 840 -420 930 -420 {
lab=iovss}
N 1270 -720 1360 -720 {
lab=pad}
N 1270 -740 1270 -720 {
lab=pad}
C {sg13g2_Clamp_N8N8D.sym} 550 -720 0 0 {name=x1}
C {sg13g2_DCNDiode.sym} 1120 -660 0 0 {name=x3}
C {sg13g2_DCPDiode.sym} 1100 -500 0 0 {name=x4}
C {sg13g2_GateLevelUpInv.sym} 170 -620 0 0 {name=x5}
C {devices/iopin.sym} 930 -360 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 1360 -720 0 0 {name=pad lab=pad}
C {devices/iopin.sym} 170 -450 1 0 {name=vss lab=vss}
C {devices/iopin.sym} -80 -620 2 0 {name=c2p lab=c2p}
C {devices/iopin.sym} 140 -790 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 430 -860 3 0 {name=iovdd lab=iovdd}
C {sg13g2_Clamp_P8N8D.sym} 550 -500 0 0 {name=x2}
