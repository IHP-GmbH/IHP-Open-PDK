v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 300 -40 380 -40 {lab=X}
N 360 140 360 280 {lab=VSS}
N 130 100 130 280 {lab=VSS}
N 130 280 300 280 {lab=VSS}
N -240 100 20 100 {lab=B1}
N -110 -400 -40 -400 {lab=VDD}
N 260 -270 260 -40 {lab=#net1}
N -30 190 -30 280 {lab=VSS}
N -440 280 -110 280 {lab=VSS}
N -110 -400 -110 -290 {lab=VDD}
N 360 -400 360 -270 {lab=VDD}
N -30 30 -30 190 {lab=VSS}
N 60 100 130 100 {lab=VSS}
N -110 190 -30 190 {lab=VSS}
N 300 140 360 140 {lab=VSS}
N 300 -400 360 -400 {lab=VDD}
N 300 -40 300 110 {lab=X}
N 130 -400 300 -400 {lab=VDD}
N 60 -190 60 -160 {lab=#net2}
N 130 -340 130 -130 {lab=VDD}
N 60 -30 60 70 {lab=#net1}
N 60 -310 60 -190 {lab=#net2}
N 130 -400 130 -340 {lab=VDD}
N -110 280 -30 280 {lab=VSS}
N -110 -190 60 -190 {lab=#net2}
N 20 -130 20 100 {lab=B1}
N -40 -400 -40 -260 {lab=VDD}
N -150 -260 -150 30 {lab=A1}
N 60 -100 60 -40 {lab=#net1}
N 60 -340 130 -340 {lab=VDD}
N 260 -40 260 140 {lab=#net1}
N -180 -340 -180 190 {lab=A2}
N 60 -40 60 -30 {lab=#net1}
N -180 -340 20 -340 {lab=A2}
N 60 -400 60 -370 {lab=VDD}
N 60 -400 130 -400 {lab=VDD}
N -110 -260 -40 -260 {lab=VDD}
N 300 -400 300 -300 {lab=VDD}
N 60 280 130 280 {lab=VSS}
N 60 -40 260 -40 {lab=#net1}
N -30 280 60 280 {lab=VSS}
N 60 -130 130 -130 {lab=VDD}
N 300 -270 360 -270 {lab=VDD}
N -110 -30 60 -30 {lab=#net1}
N -40 -400 60 -400 {lab=VDD}
N 300 280 360 280 {lab=VSS}
N -240 30 -150 30 {lab=A1}
N -430 -400 -110 -400 {lab=VDD}
N -110 -30 -110 0 {lab=#net1}
N -180 190 -150 190 {lab=A2}
N -110 -230 -110 -190 {lab=#net2}
N -240 190 -180 190 {lab=A2}
N -110 60 -110 160 {lab=#net3}
N 60 130 60 280 {lab=VSS}
N 300 -240 300 -40 {lab=X}
N -110 220 -110 280 {lab=VSS}
N 300 170 300 280 {lab=VSS}
N -110 30 -30 30 {lab=VSS}
C {devices/opin.sym} 380 -40 0 0 {name=p1 lab=X}
C {devices/ipin.sym} -240 30 0 0 {name=p2 lab=A1}
C {devices/ipin.sym} -240 190 0 0 {name=p3 lab=A2}
C {devices/ipin.sym} -240 100 0 0 {name=p4 lab=B1}
C {sg13_hv_nmos.sym} -130 30 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -130 190 0 0 {name=M2 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 40 100 0 0 {name=M3 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 280 140 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -130 -260 0 0 {name=M5 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 40 -340 0 0 {name=M6 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 40 -130 0 0 {name=M7 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 280 -270 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1280 820 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {lab_pin.sym} -430 -400 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -440 280 0 0 {name=p6 sig_type=std_logic lab=VSS}
