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
N 590 -740 590 -910 {}
N 100 -740 270 -740 {}
N 10 -740 60 -740 {}
N 180 -270 180 -360 {}
N 100 -270 180 -270 {}
N 60 -540 60 -740 {}
N 100 -970 100 -1030 {}
N 270 -940 340 -940 {}
N 100 -940 170 -940 {}
N 180 -200 180 -270 {}
N 180 -360 180 -450 {}
N 500 -1030 590 -1030 {}
N 430 -940 500 -940 {}
N 340 -1030 430 -1030 {}
N 100 -1030 170 -1030 {}
N 100 -360 180 -360 {}
N 10 -360 60 -360 {}
N 100 -200 180 -200 {}
N 100 -450 180 -450 {}
N 100 -390 100 -420 {}
N 430 -740 430 -910 {}
N 100 -540 180 -540 {}
N 500 -940 500 -1030 {}
N 590 -1030 660 -1030 {}
N 100 -480 100 -510 {}
N 430 -1030 500 -1030 {}
N 100 -300 100 -330 {}
N 660 -940 660 -1030 {}
N 590 -740 630 -740 {}
N 270 -1030 340 -1030 {}
N -130 -1030 100 -1030 {}
N 210 -940 230 -940 {}
N 430 -970 430 -1030 {}
N 270 -740 430 -740 {}
N 540 -940 550 -940 {}
N 100 -570 100 -740 {}
N 380 -940 390 -940 {}
N -130 -200 100 -200 {}
N 10 -450 60 -450 {}
N 60 -740 60 -940 {}
N 590 -970 590 -1030 {}
N 170 -1030 270 -1030 {}
N 270 -740 270 -910 {}
N 430 -740 590 -740 {}
N 170 -940 170 -1030 {}
N 10 -270 60 -270 {}
N 590 -940 660 -940 {}
N 100 -200 100 -240 {}
N 180 -450 180 -540 {}
N 100 -740 100 -910 {}
N 270 -970 270 -1030 {}
N 340 -940 340 -1030 {}
C {lab_wire.sym} 40 -360 0 0 {name=l1 sig_type=std_logic lab=C}
C {lab_wire.sym} 220 -940 0 0 {name=l2 sig_type=std_logic lab=B}
C {lab_wire.sym} 540 -940 0 0 {name=l3 sig_type=std_logic lab=D}
C {lab_wire.sym} 380 -940 0 0 {name=l4 sig_type=std_logic lab=C}
C {lab_wire.sym} 40 -450 0 0 {name=l5 sig_type=std_logic lab=B}
C {lab_wire.sym} 40 -270 0 0 {name=l6 sig_type=std_logic lab=D}
C {devices/ipin.sym} 10 -740 0 0 {name=p1 lab=A}
C {devices/ipin.sym} 10 -450 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 10 -360 0 0 {name=p3 lab=C}
C {devices/opin.sym} 630 -740 0 0 {name=p4 lab=Y}
C {devices/ipin.sym} 10 -270 0 0 {name=p5 lab=D}
C {devices/lab_pin.sym} -130 -1030 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -130 -200 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 80 -540 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 80 -450 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 80 -360 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 80 -270 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 80 -940 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 250 -940 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 410 -940 0 0 {name=M7 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 570 -940 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -990 260 0 0 {name=l1 author="IHP PDK AUTHORS"}
