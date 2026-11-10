v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -150 100 -150 140 {lab=cathode}
N -60 -90 -20 -90 {lab=sub!}
N 40 -90 80 -90 {lab=anode}
N -140 -250 -60 -250 {lab=guard}
N -50 100 -50 140 {lab=cathode}
N -50 100 40 100 {lab=cathode}
N -150 100 -50 100 {lab=cathode}
N -150 200 -150 260 {lab=#net1}
N -50 200 -50 260 {lab=#net2}
C {lab_wire.sym} -40 -90 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {devices/noconn.sym} -60 -250 0 0 {name=p1}
C {devices/iopin.sym} 40 100 0 0 {name=p2 lab=cathode}
C {devices/iopin.sym} 80 -90 0 0 {name=p3 lab=anode}
C {devices/iopin.sym} -140 -250 2 0 {name=p4 lab=guard}
C {dantenna.sym} -150 170 0 0 {name=D0 model=dantenna l=27.78u w=1.26u}
C {dantenna.sym} -50 170 0 0 {name=D1 model=dantenna l=27.78u w=1.26u}
C {ptap1.sym} 10 -90 1 0 {name=R0 model=ptap1 w=11.885e-6 l=11.885e-6}
C {devices/title-3.sym} -1290 840 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {lab_wire.sym} -150 250 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -50 250 0 0 {name=l3 sig_type=std_logic lab=sub!}
