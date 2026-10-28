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
N -130 -790 -130 -730 {lab=xxx}
N -10 -700 -10 -540 {lab=A}
N 30 -540 30 -460 {lab=#net1}
N -130 -790 -80 -790 {lab=xxx}
N -80 -790 30 -790 {lab=xxx}
N -200 -340 -170 -340 {lab=B}
N 220 -790 290 -790 {lab=xxx}
N 30 -790 80 -790 {lab=xxx}
N -350 -270 30 -270 {lab=VSS}
N 220 -340 290 -340 {lab=VSS}
N -80 -790 -80 -700 {lab=xxx}
N 220 -540 220 -370 {lab=X}
N 30 -400 30 -370 {lab=#net2}
N 50 -270 220 -270 {lab=VSS}
N 220 -650 220 -540 {lab=X}
N 50 -430 50 -340 {lab=VSS}
N 30 -310 30 -270 {lab=VSS}
N 290 -790 290 -680 {lab=xxx}
N 180 -680 180 -540 {lab=#net1}
N -170 -700 -170 -340 {lab=B}
N 30 -700 80 -700 {lab=xxx}
N -350 -790 -130 -790 {lab=xxx}
N -170 -340 -10 -340 {lab=B}
N -50 -540 -10 -540 {lab=A}
N 80 -790 220 -790 {lab=xxx}
N 30 -790 30 -730 {lab=xxx}
N 30 -540 180 -540 {lab=#net1}
N -130 -640 30 -640 {lab=#net1}
N 30 -340 50 -340 {lab=VSS}
N 30 -640 30 -540 {lab=#net1}
N 220 -790 220 -710 {lab=xxx}
N 220 -270 290 -270 {lab=VSS}
N 30 -270 50 -270 {lab=VSS}
N 220 -540 260 -540 {lab=X}
N 220 -310 220 -270 {lab=VSS}
N -130 -700 -80 -700 {lab=xxx}
N 50 -340 50 -270 {lab=VSS}
N 180 -540 180 -340 {lab=#net1}
N 30 -670 30 -640 {lab=#net1}
N 80 -790 80 -700 {lab=xxx}
N 290 -340 290 -270 {lab=VSS}
N 30 -430 50 -430 {lab=VSS}
N -10 -540 -10 -430 {lab=A}
N 220 -680 290 -680 {lab=xxx}
N -130 -670 -130 -640 {lab=#net1}
C {devices/ipin.sym} -50 -540 0 0 {name=p1 lab=A}
C {devices/ipin.sym} -200 -340 0 0 {name=p2 lab=B}
C {devices/opin.sym} 260 -540 0 0 {name=p3 lab=X}
C {devices/lab_pin.sym} -350 -790 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -350 -270 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 10 -430 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 10 -340 0 0 {name=M2 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 200 -340 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -150 -700 0 0 {name=M4 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 10 -700 0 0 {name=M5 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 200 -680 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1280 360 0 0 {name=l1 author="IHP PDK AUTHORS"}
