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
N 770 -430 930 -430 {lab=Y}
N 770 -330 770 -270 {lab=VSS}
N 930 -760 950 -760 {lab=VDD}
N 590 -970 590 -890 {lab=VDD}
N 930 -970 930 -890 {lab=VDD}
N 930 -970 950 -970 {lab=VDD}
N 870 -860 890 -860 {lab=B}
N 930 -430 930 -390 {lab=Y}
N 730 -760 890 -760 {lab=A}
N 590 -270 610 -270 {lab=VSS}
N 610 -970 930 -970 {lab=VDD}
N 700 -760 730 -760 {lab=A}
N 610 -360 610 -270 {lab=VSS}
N 930 -860 950 -860 {lab=VDD}
N 930 -330 930 -270 {lab=VSS}
N 870 -360 890 -360 {lab=B}
N 590 -330 590 -270 {lab=VSS}
N 930 -570 930 -430 {lab=Y}
N 590 -570 870 -570 {lab=B}
N 790 -270 930 -270 {lab=VSS}
N 950 -860 950 -760 {lab=VDD}
N 610 -970 610 -860 {lab=VDD}
N 930 -270 950 -270 {lab=VSS}
N 930 -570 990 -570 {lab=Y}
N 770 -270 790 -270 {lab=VSS}
N 770 -360 790 -360 {lab=VSS}
N 730 -760 730 -360 {lab=A}
N 790 -360 790 -270 {lab=VSS}
N 550 -570 550 -360 {lab=B_N}
N 930 -730 930 -570 {lab=Y}
N 590 -570 590 -390 {lab=B}
N 470 -970 590 -970 {lab=VDD}
N 770 -430 770 -390 {lab=Y}
N 590 -970 610 -970 {lab=VDD}
N 870 -570 870 -360 {lab=B}
N 550 -860 550 -570 {lab=B_N}
N 930 -360 950 -360 {lab=VSS}
N 950 -360 950 -270 {lab=VSS}
N 470 -270 590 -270 {lab=VSS}
N 870 -860 870 -570 {lab=B}
N 500 -570 550 -570 {lab=B_N}
N 590 -830 590 -570 {lab=B}
N 950 -970 950 -860 {lab=VDD}
N 590 -360 610 -360 {lab=VSS}
N 590 -860 610 -860 {lab=VDD}
N 930 -830 930 -790 {lab=#net1}
N 610 -270 770 -270 {lab=VSS}
C {lab_wire.sym} 680 -570 0 0 {name=l1 sig_type=std_logic lab=B}
C {devices/opin.sym} 990 -570 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} 500 -570 0 0 {name=p2 lab=B_N}
C {devices/ipin.sym} 700 -760 0 0 {name=p3 lab=A}
C {devices/lab_pin.sym} 470 -970 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 470 -270 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 570 -360 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 750 -360 0 0 {name=M2 w=1.440u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 910 -360 0 0 {name=M3 w=1.440u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 570 -860 0 0 {name=M4 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 910 -860 0 0 {name=M5 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 910 -760 0 0 {name=M6 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -520 260 0 0 {name=l1 author="IHP PDK AUTHORS"}
