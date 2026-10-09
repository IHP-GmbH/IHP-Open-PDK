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
N -190 100 -130 100 {}
N -130 510 10 510 {}
N -260 -150 -260 -230 {}
N -360 0 -360 -150 {}
N 10 510 10 480 {}
N -60 450 -30 450 {}
N -190 70 -190 -90 {}
N -320 -90 -190 -90 {}
N -190 440 -130 440 {}
N -190 -150 -130 -150 {}
N -360 0 -30 0 {}
N -500 510 -190 510 {}
N 10 260 120 260 {}
N -190 -90 -190 -120 {}
N -130 -150 -130 -230 {}
N -130 510 -130 440 {}
N -190 510 -130 510 {}
N 10 510 90 510 {}
N -230 260 -230 100 {}
N -320 -150 -260 -150 {}
N -380 30 -230 30 {}
N 10 360 90 360 {}
N -190 -230 -130 -230 {}
N -190 -180 -190 -230 {}
N -500 -230 -320 -230 {}
N -320 -180 -320 -230 {}
N 90 450 90 360 {}
N -260 -230 -190 -230 {}
N -190 260 -190 130 {}
N -230 30 -60 30 {}
N -320 -90 -320 -120 {}
N -190 510 -190 470 {}
N -130 100 -130 -150 {}
N 10 450 90 450 {}
N -230 440 -230 260 {}
N -230 30 -230 -150 {}
N 10 420 10 390 {}
N -380 0 -360 0 {}
N -60 450 -60 30 {}
N 10 330 10 260 {}
N -30 360 -30 0 {}
N -190 410 -190 260 {}
N 90 510 90 450 {}
N -320 -230 -260 -230 {}
N -190 260 10 260 {}
N -270 260 -230 260 {}
C {devices/ipin.sym} -380 0 0 0 {name=p1 lab=A1}
C {devices/ipin.sym} -380 30 0 0 {name=p2 lab=A2}
C {devices/ipin.sym} -270 260 0 0 {name=p3 lab=B1}
C {devices/opin.sym} 120 260 0 0 {name=p4 lab=Y}
C {devices/lab_pin.sym} -500 -230 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -500 510 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -210 440 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -10 360 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -10 450 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -340 -150 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -210 -150 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -210 100 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1440 1020 0 0 {name=l1 author="IHP PDK AUTHORS"}
