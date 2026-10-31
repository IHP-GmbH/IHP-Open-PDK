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
N -110 -30 -90 -30 {}
N -50 170 -50 -30 {}
N -90 200 -90 -30 {}
N -50 -30 -20 -30 {}
N -50 280 -50 230 {}
N -186 280 -50 280 {}
N -50 -30 -50 -240 {}
N 20 280 20 200 {}
N -50 -340 20 -340 {}
N -50 -300 -50 -340 {}
N -90 -30 -90 -270 {}
N -50 200 20 200 {}
N -200 -340 -50 -340 {}
N 20 -270 20 -340 {}
N -50 280 20 280 {}
N -50 -270 20 -270 {}
C {devices/opin.sym} -20 -30 0 0 {name=p1 lab=Y}
C {devices/lab_pin.sym} -186 280 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {devices/ipin.sym} -110 -30 0 0 {name=p3 lab=A}
C {devices/lab_pin.sym} -200 -340 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {sg13_hv_nmos.sym} -70 200 0 0 {name=M1 w=11.840u l=0.450u ng=16 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -70 -270 0 0 {name=M2 w=43.040u l=0.450u ng=16 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1340 860 0 0 {name=l1 author="IHP PDK AUTHORS"}
