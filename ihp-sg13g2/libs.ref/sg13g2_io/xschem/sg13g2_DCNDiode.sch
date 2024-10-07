v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -40 -20 10 -20 {
lab=cathode}
N 10 30 10 90 {
lab=cathode}
N -50 90 10 90 {
lab=cathode}
N -140 -20 -100 -20 {
lab=anode}
N -140 30 -140 90 {
lab=anode}
N -140 90 -110 90 {
lab=anode}
N 10 30 50 30 {
lab=cathode}
N 10 -20 10 30 {
lab=cathode}
N -180 30 -140 30 {
lab=anode}
N -140 -20 -140 30 {
lab=anode}
N -20 140 40 140 {
lab=guard}
N -180 30 -180 50 {
lab=anode}
C {sg13g2_pr/dantenna.sym} -70 -20 1 0 {name=D1
model=dantenna
l=1.26u
w=27.78u
spiceprefix=X
}
C {sg13g2_pr/dantenna.sym} -80 90 1 0 {name=D2
model=dantenna
w=27.78u
l=1.26u 
spiceprefix=X
}
C {devices/iopin.sym} 50 30 0 0 {name=cathode lab=cathode}
C {devices/iopin.sym} -180 50 0 0 {name=anode lab=anode}
C {devices/iopin.sym} 40 140 0 0 {name=guard lab=guard}
