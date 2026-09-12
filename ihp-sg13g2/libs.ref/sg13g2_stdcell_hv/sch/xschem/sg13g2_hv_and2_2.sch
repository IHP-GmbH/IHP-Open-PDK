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
N -180 -830 -120 -830 {lab=xxx}
N -40 -660 -10 -660 {lab=A}
N 30 -940 80 -940 {lab=xxx}
N -180 -800 -180 -750 {lab=#net1}
N -260 -640 -220 -640 {lab=B}
N -120 -940 30 -940 {lab=xxx}
N 30 -400 70 -400 {lab=VSS}
N 270 -940 270 -810 {lab=xxx}
N 220 -780 220 -620 {lab=X}
N 30 -750 30 -620 {lab=#net1}
N -10 -660 -10 -530 {lab=A}
N 220 -370 220 -270 {lab=VSS}
N 220 -940 270 -940 {lab=xxx}
N 30 -370 30 -270 {lab=VSS}
N 30 -270 70 -270 {lab=VSS}
N 260 -400 260 -270 {lab=VSS}
N 180 -620 180 -400 {lab=#net1}
N -326 -940 -180 -940 {lab=xxx}
N 220 -400 260 -400 {lab=VSS}
N -340 -270 30 -270 {lab=VSS}
N 30 -840 80 -840 {lab=xxx}
N 30 -530 70 -530 {lab=VSS}
N 30 -620 30 -560 {lab=#net1}
N 220 -620 220 -430 {lab=X}
N 80 -940 80 -840 {lab=xxx}
N -220 -400 -10 -400 {lab=B}
N -180 -940 -120 -940 {lab=xxx}
N 220 -940 220 -840 {lab=xxx}
N -120 -940 -120 -830 {lab=xxx}
N -180 -940 -180 -860 {lab=xxx}
N -220 -640 -220 -400 {lab=B}
N 220 -270 260 -270 {lab=VSS}
N 220 -620 270 -620 {lab=X}
N 70 -270 220 -270 {lab=VSS}
N 30 -620 180 -620 {lab=#net1}
N 30 -810 30 -750 {lab=#net1}
N 30 -500 30 -430 {lab=#net2}
N -220 -830 -220 -640 {lab=B}
N 30 -940 30 -870 {lab=xxx}
N 180 -810 180 -620 {lab=#net1}
N -180 -750 30 -750 {lab=#net1}
N -10 -840 -10 -660 {lab=A}
N 220 -810 270 -810 {lab=xxx}
N 70 -400 70 -270 {lab=VSS}
N 70 -530 70 -400 {lab=VSS}
N 80 -940 220 -940 {lab=xxx}
C {devices/ipin.sym} -40 -660 0 0 {name=p1 lab=A}
C {devices/ipin.sym} -260 -640 0 0 {name=p2 lab=B}
C {devices/opin.sym} 270 -620 0 0 {name=p3 lab=X}
C {devices/lab_pin.sym} -326 -940 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -340 -270 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 10 -530 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 10 -400 0 0 {name=M2 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 200 -400 0 0 {name=M3 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -200 -830 0 0 {name=M4 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 10 -840 0 0 {name=M5 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 200 -810 0 0 {name=M6 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1290 280 0 0 {name=l1 author="IHP PDK AUTHORS"}
