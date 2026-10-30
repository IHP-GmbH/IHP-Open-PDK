v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -10 60 120 60 {lab=core}
N -180 60 -70 60 {lab=pad}
N -150 -120 130 -120 {lab=plus}
N 130 60 270 60 {lab=core}
N 120 60 120 220 {lab=core}
N 120 60 130 60 {lab=core}
N 130 -120 130 -60 {lab=plus}
N -150 250 -70 250 {lab=sub! netSet bn on R0}
N -70 110 -70 150 {lab=minus}
N -160 110 -70 110 {lab=minus}
N 130 0 130 60 {lab=core}
N -70 210 -70 250 {lab=sub! netSet bn on R0}
N 120 280 120 330 {lab=sub!}
C {lab_wire.sym} -110 250 0 0 {name=l1 sig_type=std_logic lab=sub! netSet bn on R0}
C {lab_wire.sym} -120 110 0 0 {name=l2 sig_type=std_logic lab=minus}
C {devices/iopin.sym} 270 60 2 0 {name=p1 lab=core}
C {devices/iopin.sym} -180 60 2 0 {name=p2 lab=pad}
C {devices/iopin.sym} -150 -120 2 0 {name=p3 lab=plus}
C {devices/iopin.sym} -160 110 2 0 {name=p4 lab=minus}
C {dpantenna.sym} 130 -30 0 0 {name=D0 model=dpantenna l=4.98u w=0.64u}
C {dantenna.sym} 120 250 0 0 {name=D1 model=dantenna l=3.1u w=0.64u}
C {rppd.sym} -40 60 3 0 {name=R0 body=sub! model=rppd w=1e-6 l=2e-6 m=1 b=0 mm_ok=1}
C {ptap1.sym} -70 180 0 0 {name=R1 model=ptap1 w=3.005e-6 l=3.005e-6}
C {devices/title-3.sym} -1270 1030 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {lab_wire.sym} 120 330 0 0 {name=l3 sig_type=std_logic lab=sub! netSet bn on R0}
