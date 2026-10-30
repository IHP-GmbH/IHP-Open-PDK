v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -150 -180 -80 -180 {lab=sub!}
N -150 -40 -70 -40 {lab=sub!}
N -280 -40 -210 -40 {lab=net_3}
N -290 -180 -210 -180 {lab=net_2}
N -265 -250 -100 -250 {lab=net_0}
N -265 -110 -100 -110 {lab=net_1}
C {lab_wire.sym} -120 -180 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -110 -40 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {devices/noconn.sym} -100 -250 3 0 {name=p1}
C {devices/noconn.sym} -100 -110 3 0 {name=p2}
C {devices/iopin.sym} -265 -250 2 0 {name=p3 lab=iovdd}
C {devices/iopin.sym} -290 -180 2 0 {name=p4 lab=iovss}
C {devices/iopin.sym} -280 -40 2 0 {name=p5 lab=vss}
C {devices/iopin.sym} -265 -110 2 0 {name=p6 lab=vdd}
C {ptap1.sym} -180 -180 3 0 {name=R0 model=ptap1 w=37.625e-6 l=37.625e-6}
C {ptap1.sym} -180 -40 3 0 {name=R1 model=ptap1 w=2.42e-6 l=2.42e-6}
C {devices/title-3.sym} -1430 740 0 0 {name=l1 author="IHP PDK AUTHORS"}
