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
N 640 -1440 670 -1440 {lab=xxx}
N 470 -1170 470 -1070 {lab=VSS}
N 430 -1070 470 -1070 {lab=VSS}
N 240 -1440 240 -1070 {lab=B}
N 350 -1170 390 -1170 {lab=A}
N 640 -1410 640 -1240 {lab=X}
N -180 -1520 110 -1520 {lab=xxx}
N 640 -990 670 -990 {lab=VSS}
N 430 -1170 470 -1170 {lab=VSS}
N 640 -1520 670 -1520 {lab=xxx}
N 640 -1520 640 -1470 {lab=xxx}
N 110 -1520 160 -1520 {lab=xxx}
N 240 -1070 390 -1070 {lab=B}
N 430 -1040 430 -1000 {lab=#net1}
N 470 -890 640 -890 {lab=VSS}
N 470 -970 470 -890 {lab=VSS}
N 670 -1520 670 -1440 {lab=xxx}
N 110 -1310 280 -1310 {lab=#net2}
N 480 -1520 480 -1440 {lab=xxx}
N 280 -1520 330 -1520 {lab=xxx}
N 70 -970 390 -970 {lab=C}
N 600 -1240 600 -990 {lab=#net2}
N 110 -1520 110 -1470 {lab=xxx}
N 640 -890 670 -890 {lab=VSS}
N 640 -1240 710 -1240 {lab=X}
N 390 -1440 390 -1170 {lab=A}
N 640 -1240 640 -1020 {lab=X}
N 160 -1520 160 -1440 {lab=xxx}
N 430 -1240 430 -1200 {lab=#net2}
N 470 -1070 470 -970 {lab=VSS}
N 430 -970 470 -970 {lab=VSS}
N -190 -890 430 -890 {lab=VSS}
N 30 -970 70 -970 {lab=C}
N 330 -1520 330 -1440 {lab=xxx}
N 480 -1520 640 -1520 {lab=xxx}
N 110 -1440 160 -1440 {lab=xxx}
N 670 -990 670 -890 {lab=VSS}
N 330 -1520 430 -1520 {lab=xxx}
N 70 -1440 70 -970 {lab=C}
N 280 -1440 330 -1440 {lab=xxx}
N 600 -1440 600 -1240 {lab=#net2}
N 160 -1520 280 -1520 {lab=xxx}
N 430 -1140 430 -1100 {lab=#net3}
N 280 -1520 280 -1470 {lab=xxx}
N 430 -1440 480 -1440 {lab=xxx}
N 430 -1410 430 -1310 {lab=#net2}
N 430 -1520 430 -1470 {lab=xxx}
N 200 -1070 240 -1070 {lab=B}
N 640 -960 640 -890 {lab=VSS}
N 280 -1410 280 -1310 {lab=#net2}
N 430 -1520 480 -1520 {lab=xxx}
N 430 -1240 600 -1240 {lab=#net2}
N 280 -1310 430 -1310 {lab=#net2}
N 110 -1410 110 -1310 {lab=#net2}
N 430 -890 470 -890 {lab=VSS}
N 430 -940 430 -890 {lab=VSS}
N 430 -1310 430 -1240 {lab=#net2}
C {devices/opin.sym} 710 -1240 0 0 {name=p1 lab=X}
C {devices/ipin.sym} 30 -970 0 0 {name=p2 lab=C}
C {devices/ipin.sym} 200 -1070 0 0 {name=p3 lab=B}
C {devices/ipin.sym} 350 -1170 0 0 {name=p4 lab=A}
C {devices/lab_pin.sym} -180 -1520 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -190 -890 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 410 -1170 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 410 -1070 0 0 {name=M2 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 410 -970 0 0 {name=M3 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 620 -990 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 90 -1440 0 0 {name=M5 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 260 -1440 0 0 {name=M6 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 410 -1440 0 0 {name=M7 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 620 -1440 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -990 -320 0 0 {name=l1 author="IHP PDK AUTHORS"}
