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
N -110 80 90 80 {}
N 90 -60 90 -230 {}
N 50 -230 50 -430 {}
N 50 -30 50 -230 {}
N -190 80 -190 0 {}
N -190 -60 -190 -230 {}
N 90 -30 170 -30 {}
N -190 -30 -110 -30 {}
N -110 -530 90 -530 {}
N 90 -530 160 -530 {}
N -190 -530 -110 -530 {}
N -110 80 -110 -30 {}
N -190 80 -110 80 {}
N -190 -230 -190 -400 {}
N 170 80 170 -30 {}
N 90 -460 90 -530 {}
N -190 -430 -110 -430 {}
N 90 -430 160 -430 {}
N 160 -430 160 -530 {}
N -400 -530 -190 -530 {}
N -110 -430 -110 -530 {}
N -260 -230 -230 -230 {}
N 90 -230 120 -230 {}
N -190 -230 50 -230 {}
N 90 -230 90 -400 {}
N 90 80 170 80 {}
N -386 80 -190 80 {}
N -230 -30 -230 -230 {}
N 90 80 90 0 {}
N -190 -460 -190 -530 {}
N -230 -230 -230 -430 {}
C {devices/ipin.sym} -260 -230 0 0 {name=p1 lab=A}
C {devices/opin.sym} 120 -230 0 0 {name=p2 lab=X}
C {devices/lab_pin.sym} -400 -530 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -386 80 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -210 -30 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 70 -30 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -210 -430 0 0 {name=M3 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 70 -430 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1370 660 0 0 {name=l1 author="IHP PDK AUTHORS"}
