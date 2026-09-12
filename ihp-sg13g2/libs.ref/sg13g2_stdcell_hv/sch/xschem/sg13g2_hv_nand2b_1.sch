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
N 750 -1300 770 -1300 {}
N 910 -1000 910 -1110 {}
N 930 -810 930 -870 {}
N 910 -810 910 -840 {}
N 590 -1200 910 -1200 {}
N 750 -810 750 -940 {}
N 910 -1110 970 -1110 {}
N 910 -970 930 -970 {}
N 660 -970 710 -970 {}
N 910 -810 930 -810 {}
N 430 -1380 590 -1380 {}
N 710 -970 710 -1300 {}
N 910 -1110 910 -1200 {}
N 590 -1300 610 -1300 {}
N 770 -810 770 -970 {}
N 750 -1000 750 -1110 {}
N 590 -1330 590 -1380 {}
N 910 -1330 910 -1380 {}
N 434 -810 750 -810 {}
N 910 -900 910 -940 {}
N 590 -1380 610 -1380 {}
N 930 -870 930 -970 {}
N 930 -1300 930 -1380 {}
N 870 -1110 870 -1300 {}
N 870 -970 870 -1110 {}
N 910 -1380 930 -1380 {}
N 610 -1300 610 -1380 {}
N 610 -1380 750 -1380 {}
N 770 -810 910 -810 {}
N 770 -1380 910 -1380 {}
N 550 -870 870 -870 {}
N 910 -1200 910 -1270 {}
N 750 -810 770 -810 {}
N 910 -870 930 -870 {}
N 750 -970 770 -970 {}
N 590 -1200 590 -1270 {}
N 750 -1380 770 -1380 {}
N 770 -1300 770 -1380 {}
N 550 -870 550 -1300 {}
N 910 -1300 930 -1300 {}
N 750 -1110 870 -1110 {}
N 750 -1330 750 -1380 {}
N 480 -1300 550 -1300 {}
N 750 -1110 750 -1270 {}
C {devices/opin.sym} 970 -1110 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} 480 -1300 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 660 -970 0 0 {name=p3 lab=A_N}
C {devices/lab_pin.sym} 430 -1380 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 434 -810 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 730 -970 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 890 -970 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 890 -870 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 570 -1300 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 730 -1300 0 0 {name=M5 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 890 -1300 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -550 -220 0 0 {name=l1 author="IHP PDK AUTHORS"}
