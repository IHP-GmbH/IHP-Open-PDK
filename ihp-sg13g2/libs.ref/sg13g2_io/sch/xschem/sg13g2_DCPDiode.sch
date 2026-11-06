v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -280 -10 -240 -10 {lab=net_1}
N -240 -10 -240 -50 {lab=net_1}
N -290 -150 -240 -150 {lab=net_0}
N -300 -290 10 -290 {lab=net_2}
N 10 -80 10 -170 {lab=sub!}
N 10 -230 10 -290 {lab=net_2}
N -240 -150 -110 -150 {lab=net_0}
N -240 -10 -110 -10 {lab=net_1}
N -240 -110 -240 -150 {lab=net_0}
N -110 -10 -110 -50 {lab=net_1}
N -110 -110 -110 -150 {lab=net_0}
C {lab_wire.sym} 10 -120 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {devices/iopin.sym} -290 -150 2 0 {name=p1 lab=cathode}
C {devices/iopin.sym} -280 -10 2 0 {name=p2 lab=anode}
C {devices/iopin.sym} -300 -290 2 0 {name=p3 lab=guard}
C {dpantenna.sym} -240 -80 0 0 {name=D0 model=dpantenna l=27.78u w=1.26u}
C {dpantenna.sym} -110 -80 0 0 {name=D1 model=dpantenna l=27.78u w=1.26u}
C {ptap1.sym} 10 -200 0 0 {name=R0 model=ptap1 w=5.79e-6 l=5.79e-6}
C {devices/title-3.sym} -1390 740 0 0 {name=l1 author="IHP PDK AUTHORS"}
