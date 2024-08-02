v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1810 -120 1880 -120 {
lab=pad}
N 1810 100 1880 100 {
lab=pad}
N 1950 -60 2080 -60 {
lab=iovss}
N 2380 -120 2380 -80 {
lab=pad}
N 1880 -140 2380 -140 {
lab=pad}
N 1880 -120 1880 100 {
lab=pad}
N 1880 -140 1880 -120 {
lab=pad}
N 2380 -40 2380 10 {
lab=iovdd}
N 1880 100 2060 100 {
lab=pad}
N 2360 80 2380 80 {
lab=iovdd}
N 2380 10 2380 80 {
lab=iovdd}
N 2040 180 2360 180 {
lab=iovss}
N 2360 120 2360 180 {
lab=iovss}
N 1430 0 1430 100 {
lab=#net1}
N 1430 100 1510 100 {
lab=#net1}
N 1430 -120 1430 -40 {
lab=#net2}
N 1430 -120 1510 -120 {
lab=#net2}
N 1260 50 1260 140 {
lab=vss}
N 1260 -180 1260 -90 {
lab=vdd}
N 1480 -200 1480 10 {
lab=iovdd}
N 1300 -200 1480 -200 {
lab=iovdd}
N 1030 0 1130 0 {
lab=c2p}
N 1540 -260 1540 -200 {
lab=iovdd}
N 1480 -200 1540 -200 {
lab=iovdd}
N 1950 -60 1950 180 {
lab=iovss}
N 2040 180 2040 240 {
lab=iovss}
N 1950 180 2040 180 {
lab=iovss}
N 2380 -120 2470 -120 {
lab=pad}
N 2380 -140 2380 -120 {
lab=pad}
N 1540 -200 1660 -200 {
lab=iovdd}
N 1660 10 2380 10 {
lab=iovdd}
N 1660 180 1950 180 {
lab=iovss}
N 1040 -40 1130 -40 {
lab=c2p_en}
N 1300 -200 1300 -90 {
lab=iovdd}
N 1660 160 1660 180 {}
N 1660 10 1660 40 {}
N 1480 10 1660 10 {
lab=iovdd}
N 1660 -60 1950 -60 {}
N 1660 -200 1660 -180 {}
C {sg13g2_DCNDiode.sym} 2230 -60 0 0 {name=x8}
C {sg13g2_DCPDiode.sym} 2210 100 0 0 {name=x9}
C {devices/iopin.sym} 2040 240 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 2470 -120 0 0 {name=pad lab=pad}
C {devices/iopin.sym} 1260 140 1 0 {name=vss lab=vss}
C {devices/iopin.sym} 1030 0 2 0 {name=c2p lab=c2p}
C {devices/iopin.sym} 1260 -180 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 1540 -260 3 0 {name=iovdd lab=iovdd}
C {sg13g2_GateDecode.sym} 1280 -20 0 0 {name=x1}
C {devices/iopin.sym} 1040 -40 2 0 {name=c2p_en lab=c2p_en}
C {sg13g2_Clamp_N8N8D.sym} 1660 -120 0 0 {name=x2}
C {sg13g2_Clamp_P8N8D.sym} 1660 100 0 0 {name=x3}
