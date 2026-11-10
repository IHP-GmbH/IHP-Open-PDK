v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -200 -70 -200 -20 {lab=sub!}
N -220 -250 -150 -250 {lab=sub!}
N -220 -170 -200 -170 {lab=iovss}
N -220 -190 -220 -170 {lab=iovss}
N -220 -320 -220 -280 {lab=out}
N -220 -410 -160 -410 {lab=out}
N -220 -550 -220 -410 {lab=out}
N -200 -170 -200 -130 {lab=iovss}
N -220 -650 -220 -610 {lab=supply}
N -220 -580 -150 -580 {lab=supply}
N -150 -650 -150 -580 {lab=supply}
N -220 -650 -150 -650 {lab=supply}
N -500 -430 -370 -430 {lab=in}
N -30 -250 40 -250 {lab=sub!}
N -540 -320 -540 -170 {lab=iovss}
N -30 -320 -30 -280 {lab=out}
N -460 -320 -460 -170 {lab=iovss}
N -670 -170 -540 -170 {lab=iovss}
N -220 -320 -30 -320 {lab=out}
N -260 -290 -260 -250 {lab=in}
N -500 -320 -500 -270 {lab=sub!}
N -260 -580 -260 -430 {lab=in}
N -500 -430 -500 -360 {lab=in}
N -670 -430 -500 -430 {lab=in}
N -220 -410 -220 -320 {lab=out}
N -540 -170 -460 -170 {lab=iovss}
N -720 -650 -220 -650 {lab=supply}
N -260 -430 -260 -290 {lab=in}
N -260 -290 -70 -290 {lab=in}
N -70 -290 -70 -250 {lab=in}
N -220 -220 -220 -190 {lab=iovss}
N -220 -190 -30 -190 {lab=iovss}
N -30 -220 -30 -190 {lab=iovss}
N -370 -320 -370 -270 {lab=sub!}
N -460 -170 -410 -170 {lab=iovss}
N -410 -320 -410 -170 {lab=iovss}
N -410 -170 -330 -170 {lab=iovss}
N -330 -320 -330 -170 {lab=iovss}
N -540 -320 -530 -320 {lab=iovss}
N -470 -320 -460 -320 {lab=iovss}
N -410 -320 -400 -320 {lab=iovss}
N -340 -320 -330 -320 {lab=iovss}
N -370 -430 -260 -430 {lab=in}
N -370 -430 -370 -360 {lab=in}
N -330 -170 -220 -170 {lab=iovss}
C {lab_wire.sym} -200 -40 0 0 {name=l1 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -180 -250 0 0 {name=l2 sig_type=std_logic lab=sub!}
C {lab_wire.sym} 0 -250 0 0 {name=l3 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -500 -300 0 0 {name=l4 sig_type=std_logic lab=sub!}
C {lab_wire.sym} -370 -300 0 0 {name=l5 sig_type=std_logic lab=sub!}
C {devices/ipin.sym} -670 -430 0 0 {name=p1 lab=in}
C {devices/opin.sym} -160 -410 2 1 {name=p2 lab=out}
C {devices/iopin.sym} -720 -650 2 0 {name=p3 lab=supply}
C {devices/iopin.sym} -670 -170 2 0 {name=p4 lab=iovss}
C {sg13_hv_nmos.sym} -500 -340 1 0 {name=N0 model=sg13_hv_nmos w=63u l=9.5u ng=7 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} -370 -340 1 0 {name=N1 model=sg13_hv_nmos w=63u l=9.5u ng=7 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} -240 -250 0 0 {name=N2 model=sg13_hv_nmos w=54u l=0.5u ng=6 m=1 mm_ok=1}
C {sg13_hv_nmos.sym} -50 -250 0 0 {name=N3 model=sg13_hv_nmos w=54u l=0.5u ng=6 m=1 mm_ok=1}
C {sg13_hv_pmos.sym} -240 -580 0 0 {name=P0 model=sg13_hv_pmos w=350u l=0.5u ng=50 m=1 mm_ok=1}
C {ptap1.sym} -200 -100 0 0 {name=R0 model=ptap1 w=8.305e-6 l=8.305e-6}
C {devices/title-3.sym} -1590 540 0 0 {name=l1 author="IHP PDK AUTHORS"}
