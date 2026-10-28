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
N 300 -1190 320 -1190 {lab=VDD}
N 300 -1280 300 -1220 {lab=VDD}
N 300 -720 320 -720 {lab=VSS}
N 70 -1280 70 -1220 {lab=VDD}
N -150 -990 -150 -840 {lab=Sb}
N 210 -1070 260 -1070 {lab=A1}
N 490 -1150 490 -980 {lab=#net1}
N 70 -720 90 -720 {lab=VSS}
N -130 -810 -130 -720 {lab=VSS}
N 530 -1000 600 -1000 {lab=X}
N -220 -990 -190 -990 {lab=S}
N -320 -1280 -150 -1280 {lab=VDD}
N 70 -1190 90 -1190 {lab=VDD}
N -130 -1280 -130 -1160 {lab=VDD}
N -190 -1160 -190 -990 {lab=S}
N 320 -1190 320 -1070 {lab=VDD}
N 530 -840 550 -840 {lab=VSS}
N -330 -720 -150 -720 {lab=VSS}
N 70 -1160 70 -1100 {lab=#net2}
N 90 -1280 90 -1190 {lab=VDD}
N -150 -720 -130 -720 {lab=VSS}
N -150 -780 -150 -720 {lab=VSS}
N -190 -990 -190 -810 {lab=S}
N -20 -1070 30 -1070 {lab=A0}
N -150 -1280 -150 -1190 {lab=VDD}
N 300 -1070 320 -1070 {lab=VDD}
N -150 -990 -70 -990 {lab=Sb}
N 530 -1150 550 -1150 {lab=VDD}
N -20 -1190 30 -1190 {lab=S}
N 300 -1040 300 -1000 {lab=#net1}
N -150 -1130 -150 -990 {lab=Sb}
N 530 -1280 550 -1280 {lab=VDD}
N 490 -980 490 -840 {lab=#net1}
N 90 -1190 90 -1070 {lab=VDD}
N 70 -1000 70 -960 {lab=#net1}
N 300 -1000 300 -980 {lab=#net1}
N 70 -1070 90 -1070 {lab=VDD}
N 90 -720 300 -720 {lab=VSS}
N 530 -1280 530 -1180 {lab=VDD}
N 320 -1280 320 -1190 {lab=VDD}
N -150 -1280 -130 -1280 {lab=VDD}
N 300 -1160 300 -1100 {lab=#net3}
N -130 -720 70 -720 {lab=VSS}
N -130 -1280 70 -1280 {lab=VDD}
N 530 -1000 530 -870 {lab=X}
N 550 -1280 550 -1150 {lab=VDD}
N 550 -840 550 -720 {lab=VSS}
N 90 -1280 300 -1280 {lab=VDD}
N 530 -1120 530 -1000 {lab=X}
N 300 -980 300 -960 {lab=#net1}
N -150 -1160 -130 -1160 {lab=VDD}
N 210 -1190 260 -1190 {lab=Sb}
N -150 -810 -130 -810 {lab=VSS}
N 300 -980 490 -980 {lab=#net1}
N 320 -1280 530 -1280 {lab=VDD}
N 300 -930 320 -930 {lab=VSS}
N 70 -810 90 -810 {lab=VSS}
N 530 -810 530 -720 {lab=VSS}
N 300 -900 300 -840 {lab=#net4}
N 90 -930 90 -810 {lab=VSS}
N 300 -780 300 -720 {lab=VSS}
N 90 -810 90 -720 {lab=VSS}
N 70 -930 90 -930 {lab=VSS}
N 70 -1280 90 -1280 {lab=VDD}
N 320 -930 320 -810 {lab=VSS}
N 300 -810 320 -810 {lab=VSS}
N 300 -1280 320 -1280 {lab=VDD}
N 320 -720 530 -720 {lab=VSS}
N 210 -930 260 -930 {lab=A1}
N 70 -1000 300 -1000 {lab=#net1}
N 320 -810 320 -720 {lab=VSS}
N 530 -720 550 -720 {lab=VSS}
N 210 -810 260 -810 {lab=S}
N 70 -900 70 -840 {lab=#net5}
N 70 -780 70 -720 {lab=VSS}
N -20 -930 30 -930 {lab=A0}
N -20 -810 30 -810 {lab=Sb}
N 70 -1040 70 -1000 {lab=#net1}
C {lab_wire.sym} 240 -1070 0 0 {name=l1 sig_type=std_logic lab=A1}
C {lab_wire.sym} 0 -1070 0 0 {name=l2 sig_type=std_logic lab=A0}
C {lab_wire.sym} -110 -990 0 0 {name=l3 sig_type=std_logic lab=Sb}
C {lab_wire.sym} 0 -1190 0 0 {name=l4 sig_type=std_logic lab=S}
C {lab_wire.sym} 240 -1190 0 0 {name=l6 sig_type=std_logic lab=Sb}
C {lab_wire.sym} 240 -930 0 0 {name=l7 sig_type=std_logic lab=A1}
C {lab_wire.sym} 240 -810 0 0 {name=l8 sig_type=std_logic lab=S}
C {lab_wire.sym} 0 -930 0 0 {name=l9 sig_type=std_logic lab=A0}
C {lab_wire.sym} 0 -810 0 0 {name=l10 sig_type=std_logic lab=Sb}
C {devices/ipin.sym} -220 -990 0 0 {name=p1 lab=S}
C {devices/ipin.sym} -20 -1070 0 0 {name=p2 lab=A0}
C {devices/ipin.sym} 210 -1070 0 0 {name=p3 lab=A1}
C {devices/opin.sym} 600 -1000 0 0 {name=p4 lab=X}
C {devices/lab_pin.sym} -320 -1280 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -330 -720 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -170 -810 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 50 -930 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 50 -810 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 280 -930 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 280 -810 0 0 {name=M5 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 510 -840 0 0 {name=M6 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -170 -1160 0 0 {name=M7 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 50 -1190 0 0 {name=M8 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 50 -1070 0 0 {name=M9 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 280 -1190 0 0 {name=M10 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 280 -1070 0 0 {name=M11 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 510 -1150 0 0 {name=M12 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1110 -120 0 0 {name=l1 author="IHP PDK AUTHORS"}
