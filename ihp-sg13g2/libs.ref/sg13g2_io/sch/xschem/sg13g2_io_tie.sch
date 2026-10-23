v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -130 170 -130 120 {lab=sub!}
N -150 20 -130 20 {lab=net_1}
N -130 60 -130 20 {lab=net_1}
N -170 -40 -70 -40 {lab=net_0}
C {lab_wire.sym} -130 140 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {devices/noconn.sym} -70 -40 3 0 {name=p1}
C {devices/iopin.sym} -170 -40 2 0 {name=p2 lab=vdd}
C {devices/iopin.sym} -150 20 2 0 {name=p3 lab=vss}
C {ptap1.sym} -130 90 0 0 {name=R0 model=ptap1 w=0.79e-6 l=0.79e-6}
C {devices/title-3.sym} -1370 940 0 0 {name=l1 author="IHP PDK AUTHORS"}
