v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -190 0 -150 0 {lab=A}
N -150 0 -150 60 {lab=A}
N -150 -120 -150 -90 {lab=VDD}
N -150 -30 -150 0 {lab=A}
N -270 -120 -150 -120 {lab=VDD}
N -150 120 -150 150 {lab=VSS}
C {devices/ipin.sym} -190 0 0 0 {name=p1 lab=A}
C {devices/iopin.sym} -270 -120 2 0 {name=p2 lab=VDD}
C {devices/iopin.sym} -150 150 1 0 {name=p3 lab=VSS}
C {devices/title-3.sym} -1180 960 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {dantenna.sym} -150 90 0 0 {name=D1
model=dantenna
l=0.78u
w=0.78u
spiceprefix=X
}
C {dpantenna.sym} -150 -60 0 0 {name=D2
model=dpantenna
l=1.34u
w=1.05u
spiceprefix=X
}
