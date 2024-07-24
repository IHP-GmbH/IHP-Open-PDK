v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 0 10 -0 30 {
lab=core}
N 0 90 -0 130 {
lab=iovss}
N 0 -140 0 -90 {
lab=iovdd}
N -60 0 0 -0 {
lab=core}
N -0 -30 0 -0 {
lab=core}
N -180 0 -120 -0 {
lab=xxx}
N 0 10 120 10 {
lab=core}
N 0 -0 0 10 {
lab=core}
C {sg13g2_pr/rppd.sym} -90 0 1 1 {name=R1
w=1e-6
l=2e-6
model=rppd
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/dantenna.sym} 0 60 0 0 {name=D1
model=dantenna
l=3.1u
w=0.64u
spiceprefix=X
}
C {sg13g2_pr/dpantenna.sym} 0 -60 0 0 {name=D2
model=dpantenna
l=0.64u
w=4.98u
spiceprefix=X
}
C {devices/iopin.sym} 0 -140 0 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 0 130 0 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 120 10 0 0 {name=core lab=core}
C {devices/iopin.sym} -180 0 0 0 {name=pad lab=pad}
