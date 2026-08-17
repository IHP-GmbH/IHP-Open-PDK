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
N -360 290 -180 290 {}
N -370 -300 -180 -300 {}
N 100 210 100 0 {}
N -220 210 -220 0 {}
N 300 0 320 0 {}
N 300 180 300 0 {}
N 140 180 140 0 {}
N -180 0 -60 0 {}
N 100 0 100 -220 {}
N 140 0 140 -190 {}
N 260 210 260 0 {}
N -20 0 100 0 {}
N 300 0 300 -190 {}
N 140 0 260 0 {}
N 260 0 260 -220 {}
N -60 210 -60 0 {}
N -220 0 -220 -220 {}
N 140 -300 180 -300 {}
N 140 -250 140 -300 {}
N -60 0 -60 -220 {}
N 140 -220 180 -220 {}
N 180 -300 300 -300 {}
N 180 -220 180 -300 {}
N 140 290 180 290 {}
N 140 290 140 240 {}
N -180 180 -180 0 {}
N 140 210 180 210 {}
N 180 290 300 290 {}
N 180 290 180 210 {}
N 300 210 340 210 {}
N 340 290 340 210 {}
N 300 290 300 240 {}
N 300 -250 300 -300 {}
N 340 -220 340 -300 {}
N 300 -220 340 -220 {}
N 300 -300 340 -300 {}
N 300 290 340 290 {}
N -180 0 -180 -190 {}
N -240 0 -220 0 {}
N -20 -220 20 -220 {}
N 20 -220 20 -300 {}
N -20 -250 -20 -300 {}
N -20 290 -20 240 {}
N 20 290 20 210 {}
N -20 210 20 210 {}
N 20 290 140 290 {}
N -20 290 20 290 {}
N -20 -300 20 -300 {}
N 20 -300 140 -300 {}
N -20 0 -20 -190 {}
N -180 210 -140 210 {}
N -140 290 -140 210 {}
N -180 290 -180 240 {}
N -180 -250 -180 -300 {}
N -140 -220 -140 -300 {}
N -180 -220 -140 -220 {}
N -140 -300 -20 -300 {}
N -180 -300 -140 -300 {}
N -180 290 -140 290 {}
N -140 290 -20 290 {}
N -20 180 -20 0 {}
C {devices/ipin.sym} -240 0 0 0 {name=p1 lab=A}
C {devices/opin.sym} 320 0 0 0 {name=p2 lab=X}
C {devices/lab_pin.sym} -370 -300 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -360 290 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -200 210 0 0 {name=M1 w=0.420u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -40 210 0 0 {name=M2 w=0.420u l=0.500u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 120 210 0 0 {name=M3 w=0.420u l=0.500u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 280 210 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -200 -220 0 0 {name=M5 w=1.010u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -40 -220 0 0 {name=M6 w=2.400u l=0.500u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 120 -220 0 0 {name=M7 w=2.400u l=0.500u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 280 -220 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1270 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
