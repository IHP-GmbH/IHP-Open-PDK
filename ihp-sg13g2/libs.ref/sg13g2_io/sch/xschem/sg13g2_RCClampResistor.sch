v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -550 230 -480 230 {lab=pin1}
N -420 230 -230 230 {lab=#net1}
N -170 230 0 230 {lab=#net2}
N 60 230 130 230 {lab=#net3}
N 130 230 130 290 {lab=#net3}
N -520 290 130 290 {lab=#net3}
N -520 290 -520 370 {lab=#net3}
N -520 370 -480 370 {lab=#net3}
N -420 370 -230 370 {lab=#net4}
N -170 370 0 370 {lab=#net5}
N 60 370 130 370 {lab=#net6}
N 130 370 130 440 {lab=#net6}
N -520 440 130 440 {lab=#net6}
N -520 440 -520 540 {lab=#net6}
N -520 540 -480 540 {lab=#net6}
N -420 540 -230 540 {lab=#net7}
N -170 540 0 540 {lab=#net8}
N 60 540 130 540 {lab=#net9}
N 130 540 130 590 {lab=#net9}
N -520 590 130 590 {lab=#net9}
N -520 590 -520 690 {lab=#net9}
N -520 690 -480 690 {lab=#net9}
N -420 690 -230 690 {lab=#net10}
N -170 690 0 690 {lab=#net11}
N 60 690 130 690 {lab=#net12}
N 130 690 130 760 {lab=#net12}
N -520 760 130 760 {lab=#net12}
N -520 760 -520 860 {lab=#net12}
N -520 860 -480 860 {lab=#net12}
N -420 860 -230 860 {lab=#net13}
N -170 860 0 860 {lab=#net14}
N 60 860 140 860 {lab=#net15}
N -420 1000 -230 1000 {lab=#net16}
N -170 1000 0 1000 {lab=#net17}
N 60 1000 130 1000 {lab=#net18}
N 130 1000 130 1060 {lab=#net18}
N -520 1060 130 1060 {lab=#net18}
N -520 1060 -520 1140 {lab=#net18}
N -520 1140 -480 1140 {lab=#net18}
N -420 1140 -230 1140 {lab=#net19}
N -170 1140 0 1140 {lab=#net20}
N 60 1140 130 1140 {lab=#net21}
N 130 1140 130 1210 {lab=#net21}
N -520 1210 130 1210 {lab=#net21}
N -520 1210 -520 1310 {lab=#net21}
N -520 1310 -480 1310 {lab=#net21}
N -420 1310 -230 1310 {lab=#net22}
N -170 1310 0 1310 {lab=#net23}
N 60 1310 130 1310 {lab=#net24}
N 130 1310 130 1360 {lab=#net24}
N -520 1360 130 1360 {lab=#net24}
N -520 1360 -520 1460 {lab=#net24}
N -520 1460 -480 1460 {lab=#net24}
N -420 1460 -230 1460 {lab=#net25}
N -170 1460 100 1460 {lab=pin2}
N 140 860 140 920 {lab=#net15}
N -520 920 140 920 {lab=#net15}
N -520 920 -520 1000 {lab=#net15}
N -520 1000 -480 1000 {lab=#net15}
C {devices/iopin.sym} -550 230 2 0 {name=p1 lab=pin1}
C {devices/iopin.sym} 100 1460 0 0 {name=p2 lab=pin2}
C {rppd.sym} -450 230 3 0 {name=R0 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 230 3 0 {name=R1 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 690 3 0 {name=R10 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} 30 690 3 0 {name=R11 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -450 860 3 0 {name=R12 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 860 3 0 {name=R13 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} 30 860 3 0 {name=R14 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -450 1000 3 0 {name=R15 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 1000 3 0 {name=R16 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} 30 1000 3 0 {name=R17 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -450 1140 3 0 {name=R18 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 1140 3 0 {name=R19 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} 30 230 3 0 {name=R2 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} 30 1140 3 0 {name=R20 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -450 1310 3 0 {name=R21 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 1310 3 0 {name=R22 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} 30 1310 3 0 {name=R23 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -450 1460 3 0 {name=R24 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 1460 3 0 {name=R25 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -450 370 3 0 {name=R3 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 370 3 0 {name=R4 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} 30 370 3 0 {name=R5 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -450 540 3 0 {name=R6 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -200 540 3 0 {name=R7 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} 30 540 3 0 {name=R8 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {rppd.sym} -450 690 3 0 {name=R9 body=sub! model=rppd w=1e-6 l=20e-6 m=1 b=0 mm_ok=1}
C {devices/title.sym} -830 1960 0 0 {name=l1 author="IHP PDK AUTHORS"}
