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
N -350 -810 -280 -810 {}
N -350 -1080 -350 -1100 {}
N -440 -810 -390 -810 {}
N -350 -470 -350 -520 {}
N -350 -1050 -330 -1050 {}
N -470 -470 -350 -470 {}
N -350 -550 -330 -550 {}
N -390 -550 -390 -810 {}
N -330 -1050 -330 -1100 {}
N -330 -470 -330 -550 {}
N -350 -1100 -330 -1100 {}
N -350 -580 -350 -810 {}
N -470 -1100 -350 -1100 {}
N -350 -810 -350 -1020 {}
N -390 -810 -390 -1050 {}
N -350 -470 -330 -470 {}
C {devices/opin.sym} -280 -810 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} -440 -810 0 0 {name=p2 lab=A}
C {devices/lab_pin.sym} -470 -1100 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -470 -470 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -370 -550 0 0 {name=M1 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -370 -1050 0 0 {name=M2 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1630 100 0 0 {name=l1 author="IHP PDK AUTHORS"}
