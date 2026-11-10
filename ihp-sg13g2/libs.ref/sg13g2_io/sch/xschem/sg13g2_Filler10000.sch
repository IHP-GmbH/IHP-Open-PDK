v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -40 -160 40 -160 {lab=sub!}
N -190 -160 -100 -160 {lab=net_2}
N -165 -90 10 -90 {lab=net_1}
N -165 -240 10 -240 {lab=net_0}
N -190 -20 -100 -20 {lab=net_3}
N -40 -20 40 -20 {lab=sub!}
C {lab_wire.sym} 0 -160 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 0 -20 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/noconn.sym} 10 -240 3 0 {name=p1}
C {devices/noconn.sym} 10 -90 3 0 {name=p2}
C {devices/iopin.sym} -165 -240 2 0 {name=p3 lab=iovdd}
C {devices/iopin.sym} -190 -160 2 0 {name=p4 lab=iovss}
C {devices/iopin.sym} -165 -90 2 0 {name=p5 lab=vdd}
C {devices/iopin.sym} -190 -20 2 0 {name=p6 lab=vss}
C {ptap1.sym} -70 -160 3 0 {name=R0 model=ptap1 w=60.18e-6 l=60.18e-6}
C {ptap1.sym} -70 -20 3 0 {name=R1 model=ptap1 w=3.855e-6 l=3.855e-6}
C {devices/title-3.sym} -1330 760 0 0 {name=l1 author="IHP PDK AUTHORS"}
