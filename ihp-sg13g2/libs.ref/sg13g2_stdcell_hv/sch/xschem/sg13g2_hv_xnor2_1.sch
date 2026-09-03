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
N 140 530 160 530 {lab=VSS}
N 280 240 280 370 {lab=Y}
N -20 -30 -20 10 {lab=VDD}
N -140 -30 -140 10 {lab=VDD}
N -180 40 -180 520 {lab=A}
N 170 -80 170 0 {lab=VDD}
N -100 -30 -20 -30 {lab=VDD}
N 280 -80 280 -20 {lab=VDD}
N -20 240 -20 390 {lab=#net1}
N 160 530 160 600 {lab=VSS}
N 280 240 330 240 {lab=Y}
N 280 -80 300 -80 {lab=VDD}
N 280 400 300 400 {lab=VSS}
N 240 10 240 240 {lab=#net1}
N 150 130 150 170 {lab=Y}
N 160 600 280 600 {lab=VSS}
N 170 -80 280 -80 {lab=VDD}
N -220 40 -180 40 {lab=A}
N 0 600 140 600 {lab=VSS}
N -100 -80 -100 -30 {lab=VDD}
N 90 530 100 530 {lab=A}
N -180 520 -60 520 {lab=A}
N -20 600 0 600 {lab=VSS}
N 150 0 170 0 {lab=VDD}
N 280 530 300 530 {lab=VSS}
N 140 470 140 500 {lab=#net2}
N 280 560 280 600 {lab=VSS}
N 150 100 170 100 {lab=VDD}
N 150 -80 150 -30 {lab=VDD}
N 150 170 280 170 {lab=Y}
N -140 100 -20 100 {lab=#net1}
N 280 430 280 470 {lab=#net2}
N 140 470 280 470 {lab=#net2}
N 280 600 300 600 {lab=VSS}
N -20 550 -20 600 {lab=VSS}
N 140 600 160 600 {lab=VSS}
N 0 520 0 600 {lab=VSS}
N 280 10 300 10 {lab=VDD}
N -60 40 -60 420 {lab=B}
N 300 400 300 530 {lab=VSS}
N 280 40 280 170 {lab=Y}
N 280 470 280 500 {lab=#net2}
N -140 -30 -100 -30 {lab=VDD}
N -20 240 240 240 {lab=#net1}
N 100 100 110 100 {lab=B}
N 100 0 110 0 {lab=A}
N -100 -80 150 -80 {lab=VDD}
N 140 560 140 600 {lab=VSS}
N -360 600 -20 600 {lab=VSS}
N -20 520 0 520 {lab=VSS}
N -20 420 0 420 {lab=VSS}
N 170 0 170 100 {lab=VDD}
N 300 -80 300 10 {lab=VDD}
N 300 530 300 600 {lab=VSS}
N 240 240 240 400 {lab=#net1}
N 280 170 280 240 {lab=Y}
N 150 30 150 70 {lab=#net3}
N -360 -80 -100 -80 {lab=VDD}
N -140 70 -140 100 {lab=#net1}
N 150 -80 170 -80 {lab=VDD}
N -20 100 -20 240 {lab=#net1}
N -20 70 -20 100 {lab=#net1}
N -100 420 -60 420 {lab=B}
N 0 420 0 520 {lab=VSS}
N -20 450 -20 490 {lab=#net4}
N -140 40 -80 40 {lab=VDD}
N -20 40 80 40 {lab=VDD}
C {lab_wire.sym} 80 40 0 0 {name=l1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 100 530 0 0 {name=l2 sig_type=std_logic lab=A}
C {lab_wire.sym} -80 40 0 0 {name=l3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 240 530 0 0 {name=l4 sig_type=std_logic lab=B}
C {lab_wire.sym} 100 100 0 0 {name=l5 sig_type=std_logic lab=B}
C {lab_wire.sym} 100 0 0 0 {name=l6 sig_type=std_logic lab=A}
C {devices/ipin.sym} -220 40 0 0 {name=p1 lab=A}
C {devices/opin.sym} 330 240 0 0 {name=p2 lab=Y}
C {devices/ipin.sym} -100 420 0 0 {name=p3 lab=B}
C {devices/lab_pin.sym} -360 -80 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -360 600 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -40 420 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -40 520 0 0 {name=M2 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 120 530 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 260 400 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 260 530 0 0 {name=M5 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -160 40 0 0 {name=M6 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -40 40 0 0 {name=M7 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 130 0 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 130 100 0 0 {name=M9 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 260 10 0 0 {name=M10 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1270 1140 0 0 {name=l1 author="IHP PDK AUTHORS"}
