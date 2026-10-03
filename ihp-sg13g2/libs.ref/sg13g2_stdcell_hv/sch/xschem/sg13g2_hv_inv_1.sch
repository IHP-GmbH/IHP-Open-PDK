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
N 20 -150 20 -170 {}
N 20 -400 60 -400 {}
N 20 -230 20 -400 {}
N -80 -400 -20 -400 {}
N -20 -200 -20 -400 {}
N 20 -600 40 -600 {}
N 20 -630 20 -650 {}
N -20 -400 -20 -600 {}
N 20 -400 20 -570 {}
N 20 -650 40 -650 {}
N 40 -600 40 -650 {}
N 20 -200 40 -200 {}
N -106 -650 20 -650 {}
N 40 -150 40 -200 {}
N -106 -150 20 -150 {}
N 20 -150 40 -150 {}
C {devices/opin.sym} 60 -400 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} -80 -400 0 0 {name=p2 lab=A}
C {devices/lab_pin.sym} -106 -650 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -106 -150 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 0 -200 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 0 -600 0 0 {name=M2 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1270 480 0 0 {name=l1 author="IHP PDK AUTHORS"}
