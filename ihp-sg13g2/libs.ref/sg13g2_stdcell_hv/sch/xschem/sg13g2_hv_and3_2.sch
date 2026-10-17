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
N 440 -1470 510 -1470 {}
N 330 -1220 330 -1320 {}
N 280 -1120 330 -1120 {}
N 140 -1500 140 -1550 {}
N -10 -1470 40 -1470 {}
N 440 -1120 510 -1120 {}
N 280 -1220 330 -1220 {}
N -150 -1550 -10 -1550 {}
N 400 -1380 400 -1470 {}
N 190 -1470 190 -1550 {}
N 280 -1390 280 -1440 {}
N 280 -1150 280 -1190 {}
N 280 -1320 330 -1320 {}
N 510 -1040 510 -1120 {}
N 280 -1040 330 -1040 {}
N 440 -1300 440 -1440 {}
N 100 -1220 100 -1470 {}
N -10 -1500 -10 -1550 {}
N 330 -1040 330 -1120 {}
N 440 -1040 510 -1040 {}
N 440 -1150 440 -1300 {}
N 280 -1380 280 -1390 {}
N -10 -1390 140 -1390 {}
N 400 -1120 400 -1380 {}
N 200 -1320 240 -1320 {}
N 40 -1550 140 -1550 {}
N -80 -1120 -50 -1120 {}
N 280 -1380 400 -1380 {}
N 440 -1300 500 -1300 {}
N 280 -1350 280 -1380 {}
N 240 -1320 240 -1470 {}
N 140 -1550 190 -1550 {}
N -10 -1390 -10 -1440 {}
N 510 -1470 510 -1550 {}
N 70 -1220 100 -1220 {}
N 190 -1550 280 -1550 {}
N -10 -1550 40 -1550 {}
N -136 -1040 280 -1040 {}
N 330 -1120 330 -1220 {}
N 280 -1550 330 -1550 {}
N 280 -1500 280 -1550 {}
N 140 -1390 280 -1390 {}
N 40 -1470 40 -1550 {}
N 140 -1470 190 -1470 {}
N -50 -1120 240 -1120 {}
N 330 -1550 440 -1550 {}
N 100 -1220 240 -1220 {}
N 280 -1250 280 -1290 {}
N 280 -1470 330 -1470 {}
N 140 -1390 140 -1440 {}
N 330 -1470 330 -1550 {}
N -50 -1120 -50 -1470 {}
N 440 -1500 440 -1550 {}
N 440 -1550 510 -1550 {}
N 280 -1040 280 -1090 {}
N 330 -1040 440 -1040 {}
N 440 -1040 440 -1090 {}
C {devices/opin.sym} 500 -1300 0 0 {name=p1 lab=X}
C {devices/ipin.sym} -80 -1120 0 0 {name=p2 lab=C}
C {devices/ipin.sym} 70 -1220 0 0 {name=p3 lab=B}
C {devices/ipin.sym} 200 -1320 0 0 {name=p4 lab=A}
C {devices/lab_pin.sym} -150 -1550 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -136 -1040 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 260 -1320 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 260 -1220 0 0 {name=M2 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 260 -1120 0 0 {name=M3 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 420 -1120 0 0 {name=M4 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -30 -1470 0 0 {name=M5 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 120 -1470 0 0 {name=M6 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 260 -1470 0 0 {name=M7 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 420 -1470 0 0 {name=M8 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1070 -420 0 0 {name=l1 author="IHP PDK AUTHORS"}
