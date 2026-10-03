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
N 370 -1180 370 -1220 {}
N 390 -1680 560 -1680 {}
N 40 -1620 330 -1620 {}
N 370 -1530 390 -1530 {}
N 210 -1180 230 -1180 {}
N 370 -1560 370 -1590 {}
N 370 -1400 520 -1400 {}
N 370 -1400 370 -1410 {}
N 90 -1250 110 -1250 {}
N 370 -1180 390 -1180 {}
N 560 -1250 580 -1250 {}
N 390 -1440 390 -1530 {}
N 560 -1680 580 -1680 {}
N 370 -1650 370 -1680 {}
N 370 -1330 370 -1400 {}
N 40 -1250 50 -1250 {}
N 210 -1250 230 -1250 {}
N 370 -1680 390 -1680 {}
N 170 -1530 330 -1530 {}
N 30 -1620 40 -1620 {}
N 110 -1180 210 -1180 {}
N 580 -1600 580 -1680 {}
N 40 -1250 40 -1620 {}
N 560 -1280 560 -1400 {}
N 390 -1530 390 -1620 {}
N 300 -1250 330 -1250 {}
N 390 -1180 560 -1180 {}
N 0 -1680 370 -1680 {}
N 90 -1280 90 -1330 {}
N 170 -1250 170 -1530 {}
N 230 -1180 230 -1250 {}
N 520 -1250 520 -1400 {}
N 90 -1330 210 -1330 {}
N 90 -1180 90 -1220 {}
N 560 -1400 600 -1400 {}
N 160 -1530 170 -1530 {}
N 390 -1180 390 -1250 {}
N 0 -1180 90 -1180 {}
N 390 -1620 390 -1680 {}
N 210 -1280 210 -1330 {}
N 330 -1250 330 -1440 {}
N 560 -1600 580 -1600 {}
N 370 -1620 390 -1620 {}
N 560 -1400 560 -1570 {}
N 210 -1330 370 -1330 {}
N 370 -1250 390 -1250 {}
N 370 -1470 370 -1500 {}
N 370 -1280 370 -1330 {}
N 90 -1180 110 -1180 {}
N 230 -1180 370 -1180 {}
N 520 -1400 520 -1600 {}
N 580 -1180 580 -1250 {}
N 210 -1180 210 -1220 {}
N 560 -1180 560 -1220 {}
N 560 -1630 560 -1680 {}
N 370 -1440 390 -1440 {}
N 560 -1180 580 -1180 {}
N 110 -1180 110 -1250 {}
C {devices/opin.sym} 600 -1400 0 0 {name=p1 lab=X}
C {devices/ipin.sym} 300 -1250 0 0 {name=p2 lab=C}
C {devices/ipin.sym} 160 -1530 0 0 {name=p3 lab=B}
C {devices/ipin.sym} 30 -1620 0 0 {name=p4 lab=A}
C {devices/lab_pin.sym} 0 -1680 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 0 -1180 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 70 -1250 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 190 -1250 0 0 {name=M2 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 350 -1250 0 0 {name=M3 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 540 -1250 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 350 -1620 0 0 {name=M5 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 350 -1530 0 0 {name=M6 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 350 -1440 0 0 {name=M7 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 540 -1600 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -950 -540 0 0 {name=l1 author="IHP PDK AUTHORS"}
