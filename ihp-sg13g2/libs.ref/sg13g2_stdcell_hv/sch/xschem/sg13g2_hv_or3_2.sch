v {xschem version=3.4.7 file_version=1.2}
* Copyright 2023 IHP PDK Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
}

G {}
K {}
V {}
S {}
E {}
N 300 -1440 330 -1440 {}
N 280 -1210 280 -1270 {}
N 550 -1440 580 -1440 {}
N 0 -1680 370 -1680 {}
N 130 -1210 150 -1210 {}
N 370 -1560 370 -1590 {}
N 550 -1580 570 -1580 {}
N 260 -1210 280 -1210 {}
N 130 -1270 150 -1270 {}
N 260 -1210 260 -1240 {}
N 550 -1290 570 -1290 {}
N 330 -1270 330 -1440 {}
N 80 -1620 330 -1620 {}
N 550 -1680 570 -1680 {}
N 370 -1650 370 -1680 {}
N 370 -1390 370 -1410 {}
N 130 -1210 130 -1240 {}
N 260 -1270 280 -1270 {}
N 370 -1390 510 -1390 {}
N 220 -1270 220 -1530 {}
N 260 -1350 370 -1350 {}
N 570 -1580 570 -1680 {}
N 220 -1530 330 -1530 {}
N 370 -1440 390 -1440 {}
N 130 -1350 260 -1350 {}
N 390 -1680 550 -1680 {}
N 510 -1390 510 -1580 {}
N 280 -1210 370 -1210 {}
N 80 -1270 90 -1270 {}
N 370 -1210 370 -1240 {}
N 550 -1440 550 -1550 {}
N 150 -1210 150 -1270 {}
N 510 -1290 510 -1390 {}
N 0 -1210 130 -1210 {}
N 550 -1210 550 -1260 {}
N 80 -1270 80 -1620 {}
N 370 -1210 390 -1210 {}
N 390 -1210 550 -1210 {}
N 150 -1210 260 -1210 {}
N 390 -1620 390 -1680 {}
N 200 -1530 220 -1530 {}
N 370 -1300 370 -1350 {}
N 570 -1210 570 -1290 {}
N 370 -1620 390 -1620 {}
N 390 -1440 390 -1530 {}
N 370 -1270 390 -1270 {}
N 370 -1470 370 -1500 {}
N 550 -1210 570 -1210 {}
N 550 -1320 550 -1440 {}
N 370 -1350 370 -1390 {}
N 390 -1530 390 -1620 {}
N 370 -1680 390 -1680 {}
N 550 -1610 550 -1680 {}
N 390 -1210 390 -1270 {}
N 370 -1530 390 -1530 {}
N 130 -1300 130 -1350 {}
N 260 -1300 260 -1350 {}
N 50 -1620 80 -1620 {}
C {devices/opin.sym} 580 -1440 0 0 {name=p1 lab=X}
C {devices/ipin.sym} 300 -1440 0 0 {name=p2 lab=C}
C {devices/ipin.sym} 200 -1530 0 0 {name=p3 lab=B}
C {devices/ipin.sym} 50 -1620 0 0 {name=p4 lab=A}
C {devices/lab_pin.sym} 0 -1680 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 0 -1210 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 110 -1270 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 240 -1270 0 0 {name=M2 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 350 -1270 0 0 {name=M3 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 530 -1290 0 0 {name=M4 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 350 -1620 0 0 {name=M5 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 350 -1530 0 0 {name=M6 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 350 -1440 0 0 {name=M7 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 530 -1580 0 0 {name=M8 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -960 -560 0 0 {name=l1 author="IHP PDK AUTHORS"}
