v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 900 -330 900 -300 {
lab=pad}
N 990 -330 1090 -330 {
lab=pad}
N 1090 -330 1090 -300 {
lab=pad}
N 900 -230 900 -200 {
lab=iovss}
N 990 -200 1090 -200 {
lab=iovss}
N 1090 -220 1090 -200 {
lab=iovss}
N 1090 -270 1140 -270 {
lab=iovss}
N 1140 -270 1140 -220 {
lab=iovss}
N 1090 -220 1140 -220 {
lab=iovss}
N 1090 -240 1090 -220 {
lab=iovss}
N 900 -270 930 -270 {
lab=iovss}
N 930 -270 930 -230 {
lab=iovss}
N 900 -230 930 -230 {
lab=iovss}
N 900 -240 900 -230 {
lab=iovss}
N 990 -160 990 -120 {
lab=iovss}
N 900 -200 990 -200 {
lab=iovss}
N 990 -370 990 -330 {
lab=pad}
N 900 -330 990 -330 {
lab=pad}
N 830 -270 860 -270 {
lab=gate}
N 830 -310 830 -270 {
lab=gate}
N 830 -310 1050 -310 {
lab=gate}
N 1050 -310 1050 -270 {
lab=gate}
N 780 -270 830 -270 {
lab=gate}
N 780 -270 780 -250 {
lab=gate}
N 690 -270 780 -270 {
lab=gate}
N 780 -190 780 -160 {
lab=iovss}
N 780 -160 990 -160 {
lab=iovss}
N 990 -200 990 -160 {
lab=iovss}
N 850 -380 850 -350 {
lab=iovss}
C {sg13g2_pr/sg13_hv_nmos.sym} 1070 -270 2 1 {name=M1
l=0.6u
w=4.4u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_nmos.sym} 880 -270 2 1 {name=M2
l=0.6u
w=4.4u
ng=1
m=1
model=sg13_hv_nmos
spiceprefix=X
}
C {sg13g2_pr/dantenna.sym} 780 -220 0 0 {name=D1
model=dantenna
l=0.64u
w=0.3u
spiceprefix=X
}
C {devices/iopin.sym} 990 -120 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 690 -270 2 0 {name=gate lab=gate}
C {devices/iopin.sym} 990 -370 3 0 {name=pad lab=pad}
C {devices/iopin.sym} 850 -380 3 0 {name=iovdd lab=iovdd}
