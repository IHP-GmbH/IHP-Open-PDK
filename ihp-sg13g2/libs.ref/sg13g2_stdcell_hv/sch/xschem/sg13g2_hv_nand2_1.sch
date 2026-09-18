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
N 1170 -50 1170 90 {lab=VSS}
N 1150 -20 1150 60 {lab=#net1}
N 1150 -210 1170 -210 {lab=VDD}
N 1150 -180 1150 -140 {lab=Y}
N 650 190 1150 190 {lab=VSS}
N 1050 90 1110 90 {lab=B}
N 1150 120 1150 190 {lab=VSS}
N 650 -330 940 -330 {lab=VDD}
N 850 90 1050 90 {lab=B}
N 1150 -140 1150 -110 {lab=Y}
N 850 -50 900 -50 {lab=A}
N 940 -140 1150 -140 {lab=Y}
N 940 -330 960 -330 {lab=VDD}
N 940 -180 940 -140 {lab=Y}
N 1170 -330 1170 -210 {lab=VDD}
N 940 -330 940 -240 {lab=VDD}
N 900 -50 1110 -50 {lab=A}
N 1150 190 1170 190 {lab=VSS}
N 940 -210 960 -210 {lab=VDD}
N 1150 -330 1150 -240 {lab=VDD}
N 960 -330 960 -210 {lab=VDD}
N 1150 -330 1170 -330 {lab=VDD}
N 1170 90 1170 190 {lab=VSS}
N 1150 90 1170 90 {lab=VSS}
N 900 -210 900 -50 {lab=A}
N 1050 -210 1110 -210 {lab=B}
N 1150 -110 1260 -110 {lab=Y}
N 1050 -210 1050 90 {lab=B}
N 1150 -110 1150 -80 {lab=Y}
N 1150 -50 1170 -50 {lab=VSS}
N 960 -330 1150 -330 {lab=VDD}
C {lab_wire.sym} 880 -50 0 0 {name=l2 sig_type=std_logic lab=A}
C {devices/lab_pin.sym} 650 -330 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 650 190 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {devices/ipin.sym} 850 -50 0 0 {name=p3 lab=A}
C {devices/ipin.sym} 850 90 0 0 {name=p4 lab=B}
C {devices/opin.sym} 1260 -110 0 0 {name=p5 lab=Y}
C {sg13_hv_nmos.sym} 1130 -50 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1130 90 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 920 -210 0 0 {name=M3 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1130 -210 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -290 820 0 0 {name=l1 author="IHP PDK AUTHORS"}
