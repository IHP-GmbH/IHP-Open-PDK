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
N -230 120 -230 60 {}
N -230 -200 10 -200 {}
N 10 30 10 -200 {}
N 50 120 50 60 {}
N -230 120 -170 120 {}
N -510 120 -230 120 {}
N 50 30 110 30 {}
N -170 -520 50 -520 {}
N -170 -430 -170 -520 {}
N 10 -200 10 -430 {}
N -230 -460 -230 -520 {}
N -230 30 -170 30 {}
N -230 -430 -170 -430 {}
N -170 120 -170 30 {}
N -500 -520 -230 -520 {}
N -320 -200 -270 -200 {}
N -230 -520 -170 -520 {}
N 50 -430 110 -430 {}
N 50 -460 50 -520 {}
N -230 -200 -230 -400 {}
N -270 30 -270 -200 {}
N -270 -200 -270 -430 {}
N 50 -200 50 -400 {}
N 50 0 50 -200 {}
N 50 -200 90 -200 {}
N 50 120 110 120 {}
N 110 -430 110 -520 {}
N -230 0 -230 -200 {}
N 50 -520 110 -520 {}
N -170 120 50 120 {}
N 110 120 110 30 {}
C {devices/ipin.sym} -320 -200 0 0 {name=p1 lab=A}
C {devices/opin.sym} 90 -200 0 0 {name=p2 lab=X}
C {devices/lab_pin.sym} -500 -520 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -510 120 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -250 30 0 0 {name=M1 w=2.220u l=0.450u ng=3 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 30 30 0 0 {name=M2 w=5.920u l=0.450u ng=8 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -250 -430 0 0 {name=M3 w=8.070u l=0.450u ng=3 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 30 -430 0 0 {name=M4 w=21.520u l=0.450u ng=8 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1450 680 0 0 {name=l1 author="IHP PDK AUTHORS"}
