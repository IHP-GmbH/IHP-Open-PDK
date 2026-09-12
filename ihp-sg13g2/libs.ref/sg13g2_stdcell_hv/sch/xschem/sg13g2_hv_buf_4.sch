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
N 50 310 260 310 {}
N 260 -40 310 -40 {}
N 260 180 260 -40 {}
N 220 -40 220 -280 {}
N -186 310 -20 310 {}
N -20 310 -20 240 {}
N -60 -40 -60 -280 {}
N 260 210 330 210 {}
N -20 -380 50 -380 {}
N -186 -380 -20 -380 {}
N -20 -310 -20 -380 {}
N -60 210 -60 -40 {}
N -90 -40 -60 -40 {}
N 330 310 330 210 {}
N 50 -280 50 -380 {}
N -20 -40 -20 -250 {}
N 50 -380 260 -380 {}
N -20 -280 50 -280 {}
N 330 -280 330 -380 {}
N -20 310 50 310 {}
N -20 210 50 210 {}
N 260 -280 330 -280 {}
N 220 210 220 -40 {}
N 260 310 330 310 {}
N -20 -40 220 -40 {}
N 260 310 260 240 {}
N 260 -40 260 -250 {}
N 260 -310 260 -380 {}
N 260 -380 330 -380 {}
N 50 310 50 210 {}
N -20 180 -20 -40 {}
C {devices/ipin.sym} -90 -40 0 0 {name=p1 lab=A}
C {devices/opin.sym} 310 -40 0 0 {name=p2 lab=X}
C {devices/lab_pin.sym} -186 -380 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -186 310 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -40 210 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 240 210 0 0 {name=M2 w=2.960u l=0.450u ng=4 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -40 -280 0 0 {name=M3 w=4.030u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 240 -280 0 0 {name=M4 w=10.760u l=0.450u ng=4 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1180 840 0 0 {name=l1 author="IHP PDK AUTHORS"}
