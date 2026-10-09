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
N 220 200 220 -50 {}
N -290 300 -20 300 {}
N 60 300 260 300 {}
N -20 300 60 300 {}
N -60 -50 -60 -300 {}
N 260 200 330 200 {}
N -20 300 -20 230 {}
N -20 -330 -20 -400 {}
N 260 -400 330 -400 {}
N 60 -400 260 -400 {}
N -20 -400 60 -400 {}
N 260 -330 260 -400 {}
N 330 300 330 200 {}
N 60 300 60 200 {}
N -20 200 60 200 {}
N -20 -300 60 -300 {}
N 260 -300 330 -300 {}
N 330 -300 330 -400 {}
N 60 -300 60 -400 {}
N 260 300 260 230 {}
N -100 -50 -60 -50 {}
N -60 200 -60 -50 {}
N 260 -50 300 -50 {}
N -20 -50 220 -50 {}
N -20 -50 -20 -270 {}
N 220 -50 220 -300 {}
N 260 300 330 300 {}
N 260 170 260 -50 {}
N -20 170 -20 -50 {}
N -280 -400 -20 -400 {}
N 260 -50 260 -270 {}
C {devices/ipin.sym} -100 -50 0 0 {name=p1 lab=A}
C {devices/opin.sym} 300 -50 0 0 {name=p2 lab=X}
C {devices/lab_pin.sym} -280 -400 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -290 300 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -40 200 0 0 {name=M1 w=0.640u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 240 200 0 0 {name=M2 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -40 -300 0 0 {name=M3 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 240 -300 0 0 {name=M4 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1230 840 0 0 {name=l1 author="IHP PDK AUTHORS"}
