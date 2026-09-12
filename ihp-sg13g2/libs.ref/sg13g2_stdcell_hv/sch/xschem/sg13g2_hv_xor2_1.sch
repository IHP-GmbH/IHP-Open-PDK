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
N 800 -480 1140 -480 {lab=VSS}
N 800 -1120 800 -940 {lab=VDD}
N 1140 -690 1140 -480 {lab=VSS}
N 610 -1120 610 -600 {lab=A}
N 1340 -530 1340 -480 {lab=VSS}
N 1140 -480 1160 -480 {lab=VSS}
N 650 -600 670 -600 {lab=VSS}
N 780 -570 780 -480 {lab=VSS}
N 670 -480 780 -480 {lab=VSS}
N 780 -800 1100 -800 {lab=#net1}
N 780 -1190 780 -1150 {lab=VDD}
N 1340 -800 1500 -800 {lab=X}
N 1140 -800 1240 -800 {lab=X}
N 1140 -800 1140 -750 {lab=X}
N 1340 -800 1340 -750 {lab=X}
N 1240 -1060 1340 -1060 {lab=#net2}
N 800 -1190 1140 -1190 {lab=VDD}
N 1260 -1190 1340 -1190 {lab=VDD}
N 1140 -1090 1140 -1060 {lab=#net2}
N 1090 -1120 1100 -1120 {lab=A}
N 1240 -940 1260 -940 {lab=VDD}
N 780 -600 800 -600 {lab=VSS}
N 780 -480 800 -480 {lab=VSS}
N 1360 -1190 1360 -1120 {lab=VDD}
N 800 -600 800 -480 {lab=VSS}
N 710 -940 740 -940 {lab=B}
N 1100 -940 1100 -800 {lab=#net1}
N 1100 -800 1100 -720 {lab=#net1}
N 1340 -1120 1360 -1120 {lab=VDD}
N 800 -1190 800 -1120 {lab=VDD}
N 1280 -560 1300 -560 {lab=A}
N 780 -800 780 -650 {lab=#net1}
N 780 -910 780 -800 {lab=#net1}
N 780 -650 780 -630 {lab=#net1}
N 650 -480 670 -480 {lab=VSS}
N 780 -1120 800 -1120 {lab=VDD}
N 1290 -1120 1300 -1120 {lab=B}
N 1340 -720 1360 -720 {lab=VSS}
N 1340 -1190 1360 -1190 {lab=VDD}
N 1360 -560 1360 -480 {lab=VSS}
N 1100 -940 1200 -940 {lab=#net1}
N 540 -480 650 -480 {lab=VSS}
N 1160 -1190 1260 -1190 {lab=VDD}
N 1340 -690 1340 -590 {lab=#net3}
N 1140 -1120 1160 -1120 {lab=VDD}
N 670 -600 670 -480 {lab=VSS}
N 1160 -720 1160 -480 {lab=VSS}
N 740 -940 740 -600 {lab=B}
N 1240 -910 1240 -800 {lab=X}
N 1140 -1060 1240 -1060 {lab=#net2}
N 1340 -1190 1340 -1150 {lab=VDD}
N 780 -1090 780 -970 {lab=#net4}
N 1140 -1190 1140 -1150 {lab=VDD}
N 610 -1120 740 -1120 {lab=A}
N 780 -940 800 -940 {lab=VDD}
N 1340 -480 1360 -480 {lab=VSS}
N 650 -570 650 -480 {lab=VSS}
N 1240 -1060 1240 -970 {lab=#net2}
N 1340 -560 1360 -560 {lab=VSS}
N 1280 -720 1300 -720 {lab=B}
N 1160 -480 1340 -480 {lab=VSS}
N 1360 -720 1360 -560 {lab=VSS}
N 590 -1120 610 -1120 {lab=A}
N 650 -650 650 -630 {lab=#net1}
N 780 -1190 800 -1190 {lab=VDD}
N 554 -1190 780 -1190 {lab=VDD}
N 1140 -720 1160 -720 {lab=VSS}
N 1240 -800 1340 -800 {lab=X}
N 1340 -1090 1340 -1060 {lab=#net2}
N 650 -650 780 -650 {lab=#net1}
N 1260 -1190 1260 -940 {lab=VDD}
N 1160 -1190 1160 -1120 {lab=VDD}
N 1140 -1190 1160 -1190 {lab=VDD}
C {lab_wire.sym} 1100 -1120 0 0 {name=l1 sig_type=std_logic lab=A}
C {lab_wire.sym} 1290 -560 0 0 {name=l2 sig_type=std_logic lab=A}
C {lab_wire.sym} 1300 -1120 0 0 {name=l3 sig_type=std_logic lab=B}
C {lab_wire.sym} 1290 -720 0 0 {name=l4 sig_type=std_logic lab=B}
C {devices/opin.sym} 1500 -800 0 0 {name=p1 lab=X}
C {devices/ipin.sym} 710 -940 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 590 -1120 0 0 {name=p3 lab=A}
C {devices/lab_pin.sym} 554 -1190 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 540 -480 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 630 -600 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 760 -600 0 0 {name=M2 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1120 -720 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1320 -720 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1320 -560 0 0 {name=M5 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 760 -1120 0 0 {name=M6 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 760 -940 0 0 {name=M7 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1120 -1120 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1220 -940 0 0 {name=M9 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1320 -1120 0 0 {name=M10 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -230 40 0 0 {name=l1 author="IHP PDK AUTHORS"}
