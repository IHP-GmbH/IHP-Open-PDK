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
N 1010 -1170 1010 -1220 {}
N 840 -1140 860 -1140 {}
N 860 -630 860 -710 {}
N 1180 -1040 1180 -1110 {}
N 1180 -630 1180 -690 {}
N 860 -1220 1010 -1220 {}
N 1010 -1140 1030 -1140 {}
N 1180 -1140 1200 -1140 {}
N 1010 -1040 1180 -1040 {}
N 1180 -960 1180 -1040 {}
N 1200 -1140 1200 -1220 {}
N 1180 -960 1210 -960 {}
N 950 -1140 970 -1140 {}
N 1200 -720 1200 -810 {}
N 840 -1170 840 -1220 {}
N 724 -1220 840 -1220 {}
N 840 -630 840 -680 {}
N 860 -630 1180 -630 {}
N 1180 -1170 1180 -1220 {}
N 1010 -1040 1010 -1110 {}
N 1120 -720 1140 -720 {}
N 1120 -960 1120 -1140 {}
N 1180 -630 1200 -630 {}
N 770 -960 800 -960 {}
N 1030 -1220 1180 -1220 {}
N 1180 -810 1200 -810 {}
N 1200 -630 1200 -720 {}
N 1120 -1140 1140 -1140 {}
N 840 -960 1120 -960 {}
N 1030 -1140 1030 -1220 {}
N 840 -960 840 -1110 {}
N 1180 -1220 1200 -1220 {}
N 860 -1140 860 -1220 {}
N 840 -630 860 -630 {}
N 840 -740 840 -960 {}
N 950 -810 1140 -810 {}
N 800 -710 800 -960 {}
N 1120 -720 1120 -960 {}
N 1180 -840 1180 -960 {}
N 950 -810 950 -1140 {}
N 1180 -750 1180 -780 {}
N 1180 -720 1200 -720 {}
N 840 -710 860 -710 {}
N 840 -1220 860 -1220 {}
N 900 -810 950 -810 {}
N 800 -960 800 -1140 {}
N 710 -630 840 -630 {}
N 1010 -1220 1030 -1220 {}
C {lab_wire.sym} 1130 -720 0 0 {name=l1 sig_type=std_logic lab=A}
C {devices/opin.sym} 1210 -960 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} 900 -810 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 770 -960 0 0 {name=p3 lab=A_N}
C {devices/lab_pin.sym} 724 -1220 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 710 -630 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 820 -710 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1160 -810 0 0 {name=M2 w=1.440u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1160 -720 0 0 {name=M3 w=1.440u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 820 -1140 0 0 {name=M4 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 990 -1140 0 0 {name=M5 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1160 -1140 0 0 {name=M6 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -290 -40 0 0 {name=l1 author="IHP PDK AUTHORS"}
