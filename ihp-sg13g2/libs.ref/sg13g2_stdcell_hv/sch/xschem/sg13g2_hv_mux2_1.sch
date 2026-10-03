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
N 280 -1030 280 -1150 {}
N 200 -1180 200 -1240 {}
N -30 -1180 -30 -1240 {}
N -200 -680 -200 -790 {}
N 100 -1030 160 -1030 {}
N 200 -770 280 -770 {}
N 280 -680 410 -680 {}
N -250 -680 -250 -760 {}
N 200 -940 200 -960 {}
N 410 -680 410 -740 {}
N -250 -1170 -250 -1240 {}
N -200 -1140 -200 -1240 {}
N -390 -1240 -250 -1240 {}
N 200 -890 280 -890 {}
N -250 -820 -250 -970 {}
N 410 -770 480 -770 {}
N 50 -770 50 -890 {}
N 200 -1030 280 -1030 {}
N -30 -1060 -30 -1120 {}
N 50 -1240 200 -1240 {}
N -250 -680 -200 -680 {}
N -370 -680 -250 -680 {}
N -200 -680 -30 -680 {}
N -320 -970 -290 -970 {}
N -140 -1030 -70 -1030 {}
N -200 -1240 -30 -1240 {}
N 280 -1150 280 -1240 {}
N -30 -1240 50 -1240 {}
N -120 -1150 -70 -1150 {}
N 200 -960 200 -1000 {}
N -290 -790 -290 -970 {}
N -30 -1030 50 -1030 {}
N -30 -920 -30 -960 {}
N 200 -940 370 -940 {}
N -30 -1150 50 -1150 {}
N -250 -970 -250 -1110 {}
N 410 -960 440 -960 {}
N 370 -770 370 -940 {}
N 200 -680 280 -680 {}
N -290 -970 -290 -1140 {}
N 200 -1150 280 -1150 {}
N 200 -1060 200 -1120 {}
N -250 -1240 -200 -1240 {}
N 410 -1130 480 -1130 {}
N 480 -1130 480 -1240 {}
N 480 -680 480 -770 {}
N 410 -800 410 -960 {}
N 410 -960 410 -1100 {}
N -250 -970 -200 -970 {}
N -250 -1140 -200 -1140 {}
N 200 -920 200 -940 {}
N 110 -1150 160 -1150 {}
N -250 -790 -200 -790 {}
N 200 -1240 280 -1240 {}
N 410 -1240 480 -1240 {}
N 410 -680 480 -680 {}
N 50 -1150 50 -1240 {}
N 280 -1240 410 -1240 {}
N -30 -770 50 -770 {}
N -30 -680 50 -680 {}
N 200 -800 200 -860 {}
N 50 -680 50 -770 {}
N 200 -680 200 -740 {}
N 50 -680 200 -680 {}
N -30 -890 50 -890 {}
N 50 -1030 50 -1150 {}
N 280 -680 280 -770 {}
N 110 -890 160 -890 {}
N 370 -940 370 -1130 {}
N -30 -960 200 -960 {}
N 280 -770 280 -890 {}
N 410 -1160 410 -1240 {}
N 110 -770 160 -770 {}
N -30 -800 -30 -860 {}
N -30 -680 -30 -740 {}
N -120 -890 -70 -890 {}
N -120 -770 -70 -770 {}
N -30 -960 -30 -1000 {}
C {lab_wire.sym} 130 -1030 0 0 {name=l1 sig_type=std_logic lab=A1}
C {lab_wire.sym} -100 -1030 0 0 {name=l2 sig_type=std_logic lab=A0}
C {lab_wire.sym} -100 -1150 0 0 {name=l3 sig_type=std_logic lab=S}
C {lab_wire.sym} -220 -970 0 0 {name=l4 sig_type=std_logic lab=Sb}
C {lab_wire.sym} 140 -1150 0 0 {name=l5 sig_type=std_logic lab=Sb}
C {lab_wire.sym} 140 -890 0 0 {name=l6 sig_type=std_logic lab=A1}
C {lab_wire.sym} 140 -770 0 0 {name=l7 sig_type=std_logic lab=S}
C {lab_wire.sym} -100 -890 0 0 {name=l8 sig_type=std_logic lab=A0}
C {lab_wire.sym} -100 -770 0 0 {name=l9 sig_type=std_logic lab=Sb}
C {devices/ipin.sym} -320 -970 0 0 {name=p1 lab=S}
C {devices/ipin.sym} -140 -1030 0 0 {name=p2 lab=A0}
C {devices/ipin.sym} 100 -1030 0 0 {name=p3 lab=A1}
C {devices/opin.sym} 440 -960 0 0 {name=p4 lab=X}
C {devices/lab_pin.sym} -390 -1240 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -370 -680 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -270 -790 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -50 -890 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -50 -770 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 180 -890 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 180 -770 0 0 {name=M5 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 390 -770 0 0 {name=M6 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -270 -1140 0 0 {name=M7 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -50 -1150 0 0 {name=M8 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -50 -1030 0 0 {name=M9 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 180 -1150 0 0 {name=M10 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 180 -1030 0 0 {name=M11 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 390 -1130 0 0 {name=M12 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1210 -80 0 0 {name=l1 author="IHP PDK AUTHORS"}
