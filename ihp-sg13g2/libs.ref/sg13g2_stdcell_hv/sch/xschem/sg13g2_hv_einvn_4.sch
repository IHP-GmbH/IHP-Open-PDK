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
N 970 -1270 970 -1350 {}
N 1210 -1530 1280 -1530 {}
N 1210 -1490 1210 -1530 {}
N 880 -1530 930 -1530 {}
N 1210 -1650 1210 -1690 {}
N 720 -1270 970 -1270 {}
N 880 -1530 880 -1720 {}
N 970 -1800 990 -1800 {}
N 990 -1800 1210 -1800 {}
N 1140 -1360 1140 -1530 {}
N 1170 -1480 1170 -1620 {}
N 970 -1530 1140 -1530 {}
N 720 -1800 970 -1800 {}
N 1210 -1750 1210 -1800 {}
N 990 -1670 990 -1800 {}
N 930 -1530 930 -1670 {}
N 1210 -1270 1210 -1330 {}
N 990 -1270 1210 -1270 {}
N 970 -1410 970 -1530 {}
N 800 -1480 1170 -1480 {}
N 970 -1380 990 -1380 {}
N 800 -1530 880 -1530 {}
N 1140 -1360 1170 -1360 {}
N 1170 -1460 1170 -1480 {}
N 1210 -1800 1230 -1800 {}
N 970 -1670 990 -1670 {}
N 1210 -1460 1230 -1460 {}
N 1210 -1720 1230 -1720 {}
N 880 -1720 1170 -1720 {}
N 1210 -1620 1230 -1620 {}
N 1230 -1720 1230 -1800 {}
N 990 -1270 990 -1380 {}
N 930 -1380 930 -1530 {}
N 1230 -1620 1230 -1720 {}
N 1210 -1390 1210 -1430 {}
N 970 -1530 970 -1640 {}
N 1210 -1530 1210 -1590 {}
N 1210 -1270 1230 -1270 {}
N 1210 -1360 1230 -1360 {}
N 970 -1270 990 -1270 {}
N 1230 -1360 1230 -1460 {}
N 1230 -1270 1230 -1360 {}
N 970 -1700 970 -1800 {}
C {lab_wire.sym} 1060 -1530 0 0 {name=l1 sig_type=std_logic lab=TE}
C {devices/ipin.sym} 800 -1530 0 0 {name=p1 lab=TE_B}
C {devices/ipin.sym} 800 -1480 0 0 {name=p2 lab=A}
C {devices/opin.sym} 1280 -1530 0 0 {name=p3 lab=Z}
C {devices/lab_pin.sym} 720 -1800 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 720 -1270 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 950 -1380 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1190 -1460 0 0 {name=M2 w=2.960u l=0.450u ng=4 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1190 -1360 0 0 {name=M3 w=2.960u l=0.450u ng=4 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 950 -1670 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1190 -1720 0 0 {name=M5 w=10.760u l=0.450u ng=4 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1190 -1620 0 0 {name=M6 w=10.760u l=0.450u ng=4 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -250 -660 0 0 {name=l1 author="IHP PDK AUTHORS"}
