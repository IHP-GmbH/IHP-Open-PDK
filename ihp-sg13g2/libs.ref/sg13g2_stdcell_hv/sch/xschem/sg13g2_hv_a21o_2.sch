v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -180 280 -100 280 {lab=VSS}
N -100 30 -100 190 {lab=VSS}
N 50 280 250 280 {lab=VSS}
N -100 280 -20 280 {lab=VSS}
N -20 -160 50 -160 {lab=#net1}
N -20 280 50 280 {lab=VSS}
N -20 -220 -20 -190 {lab=#net2}
N -20 -400 -20 -360 {lab=#net1}
N -440 280 -180 280 {lab=VSS}
N -180 -220 -20 -220 {lab=#net2}
N -140 -400 -20 -400 {lab=#net1}
N -20 160 -20 280 {lab=VSS}
N -100 190 -100 280 {lab=VSS}
N -180 30 -100 30 {lab=VSS}
N 50 -330 50 -160 {lab=#net1}
N -270 -330 -270 190 {lab=A2}
N -430 -400 -180 -400 {lab=#net1}
N -20 130 50 130 {lab=VSS}
N -180 190 -100 190 {lab=VSS}
N 250 160 320 160 {lab=VSS}
N 250 -40 250 130 {lab=X}
N -180 -230 -180 -220 {lab=#net2}
N -20 -300 -20 -220 {lab=#net2}
N -180 -260 -140 -260 {lab=#net1}
N 210 -60 210 160 {lab=#net3}
N -270 190 -220 190 {lab=A2}
N -180 -400 -180 -290 {lab=#net1}
N -180 -400 -140 -400 {lab=#net1}
N 50 130 50 280 {lab=VSS}
N -270 -330 -60 -330 {lab=A2}
N -350 130 -60 130 {lab=B1}
N -350 190 -270 190 {lab=A2}
N 320 -400 320 -290 {lab=#net1}
N 250 -400 320 -400 {lab=#net1}
N -20 -60 210 -60 {lab=#net3}
N -340 30 -220 30 {lab=A1}
N -60 -160 -60 130 {lab=B1}
N 250 -40 310 -40 {lab=X}
N -20 -330 50 -330 {lab=#net1}
N 50 -400 50 -330 {lab=#net1}
N 250 -400 250 -320 {lab=#net1}
N 250 -290 320 -290 {lab=#net1}
N -220 -260 -220 30 {lab=A1}
N -140 -400 -140 -260 {lab=#net1}
N -20 -400 50 -400 {lab=#net1}
N 250 -260 250 -40 {lab=X}
N -20 -20 -20 100 {lab=#net3}
N 50 -400 250 -400 {lab=#net1}
N -180 -20 -20 -20 {lab=#net3}
N -180 -20 -180 0 {lab=#net3}
N -20 -130 -20 -60 {lab=#net3}
N 250 280 320 280 {lab=VSS}
N 210 -290 210 -60 {lab=#net3}
N -180 60 -180 160 {lab=#net4}
N 320 160 320 280 {lab=VSS}
N -180 220 -180 280 {lab=VSS}
N -20 -60 -20 -20 {lab=#net3}
N 250 190 250 280 {lab=VSS}
C {devices/opin.sym} 310 -40 0 0 {name=p1 lab=X}
C {devices/ipin.sym} -340 30 0 0 {name=p2 lab=A1}
C {devices/ipin.sym} -350 190 0 0 {name=p3 lab=A2}
C {devices/ipin.sym} -350 130 0 0 {name=p4 lab=B1}
C {sg13_hv_nmos.sym} -200 30 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -200 190 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -40 130 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 230 160 0 0 {name=M4 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -200 -260 0 0 {name=M5 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -40 -330 0 0 {name=M6 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -40 -160 0 0 {name=M7 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 230 -290 0 0 {name=M8 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1310 820 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {lab_pin.sym} -440 280 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {lab_pin.sym} -430 -400 0 0 {name=p6 sig_type=std_logic lab=VDD}
