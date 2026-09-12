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
N 1490 -280 1510 -280 {}
N 1490 -360 1510 -360 {}
N 1660 -780 1680 -780 {}
N 1660 -520 1760 -520 {}
N 1680 -280 1680 -360 {}
N 1660 -360 1680 -360 {}
N 1340 -360 1360 -360 {}
N 1340 -390 1340 -430 {}
N 1680 -680 1680 -780 {}
N 1680 -780 1680 -840 {}
N 1660 -580 1680 -580 {}
N 1680 -580 1680 -680 {}
N 1660 -280 1660 -330 {}
N 1660 -710 1660 -750 {}
N 1340 -430 1490 -430 {}
N 1660 -430 1660 -520 {}
N 1300 -780 1620 -780 {}
N 1340 -280 1360 -280 {}
N 1660 -520 1660 -550 {}
N 1360 -280 1490 -280 {}
N 1510 -280 1660 -280 {}
N 1490 -280 1490 -330 {}
N 1490 -390 1490 -430 {}
N 1450 -360 1450 -680 {}
N 1340 -280 1340 -330 {}
N 1620 -360 1620 -580 {}
N 1660 -840 1680 -840 {}
N 1490 -430 1660 -430 {}
N 1580 -580 1620 -580 {}
N 1250 -280 1340 -280 {}
N 1660 -680 1680 -680 {}
N 1254 -840 1660 -840 {}
N 1660 -810 1660 -840 {}
N 1410 -680 1450 -680 {}
N 1300 -360 1300 -780 {}
N 1660 -610 1660 -650 {}
N 1450 -680 1620 -680 {}
N 1270 -780 1300 -780 {}
N 1660 -390 1660 -430 {}
N 1360 -280 1360 -360 {}
N 1510 -280 1510 -360 {}
N 1660 -280 1680 -280 {}
C {devices/ipin.sym} 1410 -680 0 0 {name=p1 lab=B}
C {devices/lab_pin.sym} 1254 -840 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1250 -280 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {devices/opin.sym} 1760 -520 0 0 {name=p4 lab=Y}
C {devices/ipin.sym} 1270 -780 0 0 {name=p5 lab=A}
C {devices/ipin.sym} 1580 -580 0 0 {name=p6 lab=C}
C {sg13_hv_nmos.sym} 1320 -360 0 0 {name=M1 w=0.770u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1470 -360 0 0 {name=M2 w=0.770u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1640 -360 0 0 {name=M3 w=0.770u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 1640 -780 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1640 -680 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1640 -580 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} 250 320 0 0 {name=l1 author="IHP PDK AUTHORS"}
