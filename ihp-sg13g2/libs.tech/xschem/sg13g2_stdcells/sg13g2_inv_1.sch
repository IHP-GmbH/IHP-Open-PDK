v {xschem version=3.4.6 file_version=1.2
* Copyright 2025 IHP PDK Authors
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
N 40 -0 40 20 {lab=Y}
N 40 -0 80 -0 {lab=Y}
N 40 -20 40 -0 {lab=Y}
N -40 0 0 0 {lab=A}
N 0 0 0 50 {lab=A}
N 40 -100 40 -80 {lab=VDD}
N 50 -100 50 -50 {lab=VDD}
N 50 50 50 100 {lab=VSS}
N 40 80 40 100 {lab=VSS}
N 40 -100 50 -100 {lab=VDD}
N 40 -50 50 -50 {lab=VDD}
N 0 -50 0 0 {lab=A}
N 40 50 50 50 {lab=VSS}
N 40 100 50 100 {lab=VSS}
N -70 -100 40 -100 {lab=VDD}
N -70 100 40 100 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 20 50 0 0 {name=MN0
l=130.00n
w=740.00n
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 20 -50 0 0 {name=MP0
l=130.00n
w=1.12u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {opin.sym} 80 0 0 0 {name=p1 lab=Y}
C {ipin.sym} -40 0 0 0 {name=p2 lab=A}
C {iopin.sym} -70 -100 0 1 {name=p3 lab=VDD}
C {iopin.sym} -70 100 0 1 {name=p4 lab=VSS}
