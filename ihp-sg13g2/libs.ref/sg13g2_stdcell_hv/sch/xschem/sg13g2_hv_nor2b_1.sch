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
N 960 -920 960 -850 {lab=VDD}
N 610 -920 610 -870 {lab=VDD}
N 630 -370 780 -370 {lab=VSS}
N 940 -920 940 -880 {lab=VDD}
N 780 -540 780 -520 {lab=Y}
N 630 -920 940 -920 {lab=VDD}
N 740 -740 740 -490 {lab=A}
N 960 -850 960 -740 {lab=VDD}
N 570 -640 570 -490 {lab=B_N}
N 940 -710 940 -640 {lab=Y}
N 610 -370 630 -370 {lab=VSS}
N 780 -540 940 -540 {lab=Y}
N 880 -490 900 -490 {lab=B}
N 880 -640 880 -490 {lab=B}
N 610 -810 610 -640 {lab=B}
N 610 -460 610 -370 {lab=VSS}
N 940 -850 960 -850 {lab=VDD}
N 524 -920 610 -920 {lab=VDD}
N 740 -740 900 -740 {lab=A}
N 610 -640 610 -520 {lab=B}
N 780 -370 800 -370 {lab=VSS}
N 880 -850 880 -640 {lab=B}
N 940 -820 940 -770 {lab=#net1}
N 800 -490 800 -370 {lab=VSS}
N 780 -490 800 -490 {lab=VSS}
N 570 -840 570 -640 {lab=B_N}
N 780 -460 780 -370 {lab=VSS}
N 630 -490 630 -370 {lab=VSS}
N 940 -640 1010 -640 {lab=Y}
N 720 -740 740 -740 {lab=A}
N 940 -920 960 -920 {lab=VDD}
N 800 -370 940 -370 {lab=VSS}
N 500 -370 610 -370 {lab=VSS}
N 940 -460 940 -370 {lab=VSS}
N 940 -740 960 -740 {lab=VDD}
N 880 -850 900 -850 {lab=B}
N 960 -490 960 -370 {lab=VSS}
N 940 -490 960 -490 {lab=VSS}
N 940 -370 960 -370 {lab=VSS}
N 940 -540 940 -520 {lab=Y}
N 520 -640 570 -640 {lab=B_N}
N 940 -640 940 -540 {lab=Y}
N 610 -920 630 -920 {lab=VDD}
N 630 -920 630 -840 {lab=VDD}
N 610 -490 630 -490 {lab=VSS}
N 610 -840 630 -840 {lab=VDD}
N 610 -640 880 -640 {lab=B}
C {lab_wire.sym} 720 -640 0 0 {name=l1 sig_type=std_logic lab=B}
C {devices/opin.sym} 1010 -640 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} 520 -640 0 0 {name=p2 lab=B_N}
C {devices/ipin.sym} 720 -740 0 0 {name=p3 lab=A}
C {devices/lab_pin.sym} 524 -920 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 500 -370 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 590 -490 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 760 -490 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 920 -490 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 590 -840 0 0 {name=M4 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 920 -850 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 920 -740 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -490 240 0 0 {name=l1 author="IHP PDK AUTHORS"}
