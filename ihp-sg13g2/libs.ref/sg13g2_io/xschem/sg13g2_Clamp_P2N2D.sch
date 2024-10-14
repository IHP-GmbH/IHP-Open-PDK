v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 710 -400 710 -370 {
lab=iovdd}
N 1030 -400 1140 -400 {
lab=iovdd}
N 1140 -400 1140 -370 {
lab=iovdd}
N 860 -400 860 -370 {
lab=iovdd}
N 740 -400 860 -400 {
lab=iovdd}
N 1000 -400 1000 -370 {
lab=iovdd}
N 930 -400 1000 -400 {
lab=iovdd}
N 710 -340 740 -340 {
lab=iovdd}
N 740 -400 740 -340 {
lab=iovdd}
N 710 -400 740 -400 {
lab=iovdd}
N 860 -340 890 -340 {
lab=iovdd}
N 890 -400 890 -340 {
lab=iovdd}
N 860 -400 890 -400 {
lab=iovdd}
N 1000 -340 1030 -340 {
lab=iovdd}
N 1030 -400 1030 -340 {
lab=iovdd}
N 1000 -400 1030 -400 {
lab=iovdd}
N 1140 -340 1160 -340 {
lab=iovdd}
N 1160 -400 1160 -340 {
lab=iovdd}
N 1140 -400 1160 -400 {
lab=iovdd}
N 710 -310 710 -280 {
lab=pad}
N 1000 -280 1140 -280 {
lab=pad}
N 1140 -310 1140 -280 {
lab=pad}
N 1000 -310 1000 -280 {
lab=pad}
N 910 -280 1000 -280 {
lab=pad}
N 860 -310 860 -280 {
lab=pad}
N 710 -280 860 -280 {
lab=pad}
N 640 -340 670 -340 {
lab=gate}
N 640 -340 640 -250 {
lab=gate}
N 960 -250 1100 -250 {
lab=gate}
N 1100 -340 1100 -250 {
lab=gate}
N 960 -340 960 -250 {
lab=gate}
N 820 -250 960 -250 {
lab=gate}
N 820 -340 820 -250 {
lab=gate}
N 640 -250 820 -250 {
lab=gate}
N 930 -450 930 -400 {
lab=iovdd}
N 890 -400 930 -400 {
lab=iovdd}
N 620 -340 640 -340 {
lab=gate}
N 620 -360 620 -340 {
lab=gate}
N 550 -340 620 -340 {
lab=gate}
N 620 -450 620 -420 {
lab=iovdd}
N 620 -450 930 -450 {
lab=iovdd}
N 930 -480 930 -450 {
lab=iovdd}
N 910 -280 910 -210 {
lab=pad}
N 860 -280 910 -280 {
lab=pad}
N 1030 -230 1030 -210 {
lab=iovdd}
C {sg13g2_pr/sg13_hv_pmos.sym} 840 -340 0 0 {name=M1
l=0.6u
w=6.66u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 980 -340 0 0 {name=M2
l=0.6u
w=6.66u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 1120 -340 0 0 {name=M3
l=0.6u
w=6.66u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 690 -340 0 0 {name=M4
l=0.6u
w=6.66u
ng=1
m=1
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/dpantenna.sym} 620 -390 0 0 {name=D1
model=dpantenna
l=0.64u
w=0.3u
spiceprefix=X
}
C {devices/iopin.sym} 910 -210 1 0 {name=pad lab=pad}
C {devices/iopin.sym} 930 -480 3 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 550 -340 2 0 {name=gate lab=gate}
C {devices/iopin.sym} 1030 -210 1 0 {name=iovss lab=iovss}
