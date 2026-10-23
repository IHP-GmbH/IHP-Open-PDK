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
N 1094 -190 1150 -190 {}
N 1470 -320 1540 -320 {}
N 1540 -650 1540 -790 {}
N 1540 -190 1540 -320 {}
N 1470 -190 1470 -290 {}
N 1300 -320 1320 -320 {}
N 1470 -430 1540 -430 {}
N 1170 -190 1170 -320 {}
N 1300 -350 1300 -380 {}
N 1110 -790 1430 -790 {}
N 1470 -650 1540 -650 {}
N 1150 -350 1150 -380 {}
N 1540 -790 1540 -920 {}
N 1470 -920 1540 -920 {}
N 1470 -510 1540 -510 {}
N 1320 -190 1320 -320 {}
N 1320 -190 1470 -190 {}
N 1300 -380 1470 -380 {}
N 1300 -190 1300 -290 {}
N 1540 -510 1540 -650 {}
N 1400 -510 1430 -510 {}
N 1090 -790 1110 -790 {}
N 1470 -790 1540 -790 {}
N 1470 -820 1470 -920 {}
N 1150 -380 1300 -380 {}
N 1470 -430 1470 -480 {}
N 1470 -350 1470 -380 {}
N 1150 -190 1170 -190 {}
N 1470 -380 1470 -430 {}
N 1094 -920 1470 -920 {}
N 1110 -320 1110 -790 {}
N 1230 -650 1260 -650 {}
N 1260 -320 1260 -650 {}
N 1260 -650 1430 -650 {}
N 1470 -540 1470 -620 {}
N 1470 -680 1470 -760 {}
N 1430 -320 1430 -510 {}
N 1170 -190 1300 -190 {}
N 1300 -190 1320 -190 {}
N 1470 -190 1540 -190 {}
N 1150 -320 1170 -320 {}
N 1150 -190 1150 -290 {}
C {devices/ipin.sym} 1230 -650 0 0 {name=p1 lab=B}
C {devices/lab_pin.sym} 1094 -920 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1094 -190 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {devices/opin.sym} 1540 -430 0 0 {name=p4 lab=Y}
C {devices/ipin.sym} 1090 -790 0 0 {name=p5 lab=A}
C {devices/ipin.sym} 1400 -510 0 0 {name=p6 lab=C}
C {sg13_hv_nmos.sym} 1130 -320 0 0 {name=M1 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1280 -320 0 0 {name=M2 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1450 -320 0 0 {name=M3 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 1450 -790 0 0 {name=M4 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1450 -650 0 0 {name=M5 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1450 -510 0 0 {name=M6 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} 70 320 0 0 {name=l1 author="IHP PDK AUTHORS"}
