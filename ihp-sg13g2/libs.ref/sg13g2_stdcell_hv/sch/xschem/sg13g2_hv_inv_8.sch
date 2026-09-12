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
N 510 -1320 510 -1590 {}
N 550 -1590 620 -1590 {}
N 384 -1670 550 -1670 {}
N 550 -1670 620 -1670 {}
N 384 -980 550 -980 {}
N 620 -1590 620 -1670 {}
N 550 -1620 550 -1670 {}
N 550 -1090 550 -1320 {}
N 470 -1320 510 -1320 {}
N 510 -1060 510 -1320 {}
N 550 -1320 550 -1560 {}
N 550 -1060 620 -1060 {}
N 550 -1320 590 -1320 {}
N 550 -980 620 -980 {}
N 620 -980 620 -1060 {}
N 550 -980 550 -1030 {}
C {devices/opin.sym} 590 -1320 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} 470 -1320 0 0 {name=p2 lab=A}
C {devices/lab_pin.sym} 384 -1670 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 384 -980 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 530 -1060 0 0 {name=M1 w=5.920u l=0.450u ng=8 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 530 -1590 0 0 {name=M2 w=21.520u l=0.450u ng=8 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -750 -440 0 0 {name=l1 author="IHP PDK AUTHORS"}
