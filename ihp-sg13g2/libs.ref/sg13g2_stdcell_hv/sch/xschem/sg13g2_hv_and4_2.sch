v {xschem version=3.4.8RC file_version=1.3}
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
F {}
E {}
N 1850 -1390 1850 -1120 {lab=X}
N 1620 -1680 1620 -1280 {lab=A}
N 1850 -1060 1850 -960 {lab=VSS}
N 1660 -1680 1740 -1680 {lab=VDD}
N 1340 -1680 1340 -1100 {lab=C}
N 1380 -1650 1380 -1590 {lab=#net1}
N 1200 -1010 1620 -1010 {lab=D}
N 1320 -1800 1320 -1680 {lab=VDD}
N 1660 -1800 1740 -1800 {lab=VDD}
N 1380 -1680 1460 -1680 {lab=VDD}
N 1520 -1800 1600 -1800 {lab=VDD}
N 1300 -1100 1340 -1100 {lab=C}
N 1920 -1800 1920 -1680 {lab=VDD}
N 1660 -1590 1660 -1390 {lab=#net1}
N 1660 -1280 1740 -1280 {lab=VSS}
N 1200 -1680 1200 -1010 {lab=D}
N 1740 -1010 1740 -960 {lab=VSS}
N 1740 -1100 1740 -1010 {lab=VSS}
N 1240 -1680 1320 -1680 {lab=VDD}
N 1240 -1800 1320 -1800 {lab=VDD}
N 1660 -1160 1660 -1130 {lab=#net2}
N 1660 -1250 1660 -1220 {lab=#net3}
N 1660 -1650 1660 -1590 {lab=#net1}
N 1660 -1070 1660 -1040 {lab=#net4}
N 1850 -960 1920 -960 {lab=VSS}
N 1810 -1390 1810 -1090 {lab=#net1}
N 1660 -1390 1660 -1310 {lab=#net1}
N 1920 -1090 1920 -960 {lab=VSS}
N 980 -960 1660 -960 {lab=VSS}
N 1660 -1100 1740 -1100 {lab=VSS}
N 1850 -1390 1920 -1390 {lab=X}
N 1660 -960 1740 -960 {lab=VSS}
N 1660 -1010 1740 -1010 {lab=VSS}
N 1740 -1800 1740 -1680 {lab=VDD}
N 1520 -1590 1660 -1590 {lab=#net1}
N 1740 -1190 1740 -1100 {lab=VSS}
N 1850 -1650 1850 -1390 {lab=X}
N 1660 -980 1660 -960 {lab=VSS}
N 1150 -1010 1200 -1010 {lab=D}
N 1340 -1100 1620 -1100 {lab=C}
N 1480 -1680 1480 -1190 {lab=B}
N 1480 -1190 1620 -1190 {lab=B}
N 1380 -1800 1380 -1710 {lab=VDD}
N 1850 -1090 1920 -1090 {lab=VSS}
N 1240 -1650 1240 -1590 {lab=#net1}
N 1380 -1590 1520 -1590 {lab=#net1}
N 1850 -1800 1920 -1800 {lab=VDD}
N 1740 -1800 1850 -1800 {lab=VDD}
N 1520 -1680 1600 -1680 {lab=VDD}
N 1240 -1590 1380 -1590 {lab=#net1}
N 1560 -1280 1620 -1280 {lab=A}
N 1810 -1680 1810 -1390 {lab=#net1}
N 1740 -1280 1740 -1190 {lab=VSS}
N 1660 -1190 1740 -1190 {lab=VSS}
N 1600 -1800 1600 -1680 {lab=VDD}
N 1740 -960 1850 -960 {lab=VSS}
N 1850 -1800 1850 -1710 {lab=VDD}
N 1520 -1650 1520 -1590 {lab=#net1}
N 1320 -1800 1380 -1800 {lab=VDD}
N 1600 -1800 1660 -1800 {lab=VDD}
N 1520 -1800 1520 -1710 {lab=VDD}
N 1850 -1680 1920 -1680 {lab=VDD}
N 1660 -1800 1660 -1710 {lab=VDD}
N 1460 -1800 1520 -1800 {lab=VDD}
N 1240 -1800 1240 -1710 {lab=VDD}
N 1420 -1190 1480 -1190 {lab=B}
N 970 -1800 1240 -1800 {lab=VDD}
N 1460 -1800 1460 -1680 {lab=VDD}
N 1660 -1390 1810 -1390 {lab=#net1}
N 1380 -1800 1460 -1800 {lab=VDD}
C {devices/ipin.sym} 1560 -1280 0 0 {name=p1 lab=A}
C {devices/ipin.sym} 1420 -1190 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 1300 -1100 0 0 {name=p3 lab=C}
C {devices/ipin.sym} 1150 -1010 0 0 {name=p4 lab=D}
C {devices/opin.sym} 1920 -1390 0 0 {name=p5 lab=X}
C {devices/lab_pin.sym} 970 -1800 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 980 -960 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 1640 -1280 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1640 -1190 0 0 {name=M2 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1640 -1100 0 0 {name=M3 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1640 -1010 0 0 {name=M4 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1830 -1090 0 0 {name=M5 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 1220 -1680 0 0 {name=M6 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1360 -1680 0 0 {name=M7 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1500 -1680 0 0 {name=M8 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1640 -1680 0 0 {name=M9 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1830 -1680 0 0 {name=M10 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} 190 -500 0 0 {name=l1 author="IHP PDK AUTHORS"}
