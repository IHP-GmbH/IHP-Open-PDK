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
N 2050 -1640 2110 -1640 {lab=VDD}
N 2090 -1120 2090 -960 {lab=VSS}
N 1890 -1680 1970 -1680 {lab=VDD}
N 1830 -1800 1890 -1800 {lab=VDD}
N 1480 -1010 1850 -1010 {lab=D}
N 1970 -1800 2050 -1800 {lab=VDD}
N 2010 -1440 2010 -1120 {lab=#net1}
N 2050 -1090 2050 -960 {lab=VSS}
N 1260 -960 1890 -960 {lab=VSS}
N 2050 -1800 2110 -1800 {lab=VDD}
N 2050 -1370 2100 -1370 {lab=X}
N 1890 -960 1970 -960 {lab=VSS}
N 1970 -1010 1970 -960 {lab=VSS}
N 1890 -1190 1970 -1190 {lab=VSS}
N 2110 -1800 2110 -1640 {lab=VDD}
N 1610 -1100 1850 -1100 {lab=C}
N 1520 -1680 1600 -1680 {lab=VDD}
N 1600 -1800 1600 -1680 {lab=VDD}
N 1890 -1590 1890 -1440 {lab=#net1}
N 1890 -1160 1890 -1130 {lab=#net2}
N 1890 -1250 1890 -1220 {lab=#net3}
N 1890 -1650 1890 -1590 {lab=#net1}
N 1890 -1070 1890 -1040 {lab=#net4}
N 1520 -1590 1650 -1590 {lab=#net1}
N 1770 -1590 1890 -1590 {lab=#net1}
N 1550 -1100 1610 -1100 {lab=C}
N 1850 -1680 1850 -1280 {lab=A}
N 1890 -1010 1970 -1010 {lab=VSS}
N 1970 -1800 1970 -1680 {lab=VDD}
N 1600 -1800 1650 -1800 {lab=VDD}
N 1790 -1280 1850 -1280 {lab=A}
N 1710 -1800 1770 -1800 {lab=VDD}
N 1890 -980 1890 -960 {lab=VSS}
N 1480 -1680 1480 -1010 {lab=D}
N 1650 -1650 1650 -1590 {lab=#net1}
N 2010 -1640 2010 -1440 {lab=#net1}
N 2050 -1120 2090 -1120 {lab=VSS}
N 2050 -1800 2050 -1670 {lab=VDD}
N 1970 -1100 1970 -1010 {lab=VSS}
N 1890 -1800 1970 -1800 {lab=VDD}
N 1650 -1590 1770 -1590 {lab=#net1}
N 1730 -1190 1850 -1190 {lab=B}
N 2050 -960 2090 -960 {lab=VSS}
N 1970 -960 2050 -960 {lab=VSS}
N 1970 -1280 1970 -1190 {lab=VSS}
N 1890 -1440 1890 -1310 {lab=#net1}
N 1520 -1800 1520 -1710 {lab=VDD}
N 1650 -1800 1650 -1710 {lab=VDD}
N 1890 -1440 2010 -1440 {lab=#net1}
N 2050 -1370 2050 -1150 {lab=X}
N 1260 -1800 1520 -1800 {lab=VDD}
N 1890 -1800 1890 -1710 {lab=VDD}
N 2050 -1610 2050 -1370 {lab=X}
N 1400 -1010 1480 -1010 {lab=D}
N 1520 -1650 1520 -1590 {lab=#net1}
N 1520 -1800 1600 -1800 {lab=VDD}
N 1770 -1650 1770 -1590 {lab=#net1}
N 1770 -1800 1770 -1710 {lab=VDD}
N 1890 -1280 1970 -1280 {lab=VSS}
N 1970 -1190 1970 -1100 {lab=VSS}
N 1610 -1680 1610 -1100 {lab=C}
N 1890 -1100 1970 -1100 {lab=VSS}
N 1770 -1680 1830 -1680 {lab=VDD}
N 1830 -1800 1830 -1680 {lab=VDD}
N 1770 -1800 1830 -1800 {lab=VDD}
N 1730 -1680 1730 -1190 {lab=B}
N 1680 -1190 1730 -1190 {lab=B}
N 1650 -1680 1710 -1680 {lab=VDD}
N 1710 -1800 1710 -1680 {lab=VDD}
N 1650 -1800 1710 -1800 {lab=VDD}
C {devices/ipin.sym} 1790 -1280 0 0 {name=p1 lab=A}
C {devices/ipin.sym} 1680 -1190 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 1550 -1100 0 0 {name=p3 lab=C}
C {devices/ipin.sym} 1400 -1010 0 0 {name=p4 lab=D}
C {devices/opin.sym} 2100 -1370 0 0 {name=p5 lab=X}
C {devices/lab_pin.sym} 1260 -1800 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1260 -960 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 1870 -1280 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1870 -1190 0 0 {name=M2 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1870 -1100 0 0 {name=M3 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1870 -1010 0 0 {name=M4 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 2030 -1120 0 0 {name=M5 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 1500 -1680 0 0 {name=M6 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1630 -1680 0 0 {name=M7 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1750 -1680 0 0 {name=M8 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1870 -1680 0 0 {name=M9 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 2030 -1640 0 0 {name=M10 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} 430 -500 0 0 {name=l1 author="IHP PDK AUTHORS"}
