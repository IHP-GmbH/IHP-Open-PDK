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
N -360 330 -180 330 {}
N -360 -330 -180 -330 {}
N 100 250 100 0 {}
N -220 250 -220 0 {}
N -280 0 -220 0 {}
N -180 0 -180 -220 {}
N 300 0 300 -220 {}
N 300 0 370 0 {}
N 140 220 140 0 {}
N -180 0 -60 0 {}
N -60 0 -60 -250 {}
N 260 0 260 -250 {}
N 260 250 260 0 {}
N -20 0 100 0 {}
N 300 220 300 0 {}
N 140 0 260 0 {}
N -20 0 -20 -220 {}
N -220 0 -220 -250 {}
N -60 250 -60 0 {}
N 140 -330 180 -330 {}
N 140 -280 140 -330 {}
N 140 -250 180 -250 {}
N 180 -330 300 -330 {}
N 180 -250 180 -330 {}
N 140 330 180 330 {}
N 140 330 140 280 {}
N -180 220 -180 0 {}
N 140 250 180 250 {}
N 180 330 300 330 {}
N 180 330 180 250 {}
N 300 250 340 250 {}
N 340 330 340 250 {}
N 300 330 300 280 {}
N 300 -280 300 -330 {}
N 340 -250 340 -330 {}
N 300 -250 340 -250 {}
N 300 -330 340 -330 {}
N 300 330 340 330 {}
N -20 -250 20 -250 {}
N 20 -250 20 -330 {}
N -20 -280 -20 -330 {}
N -20 330 -20 280 {}
N 20 330 20 250 {}
N -20 250 20 250 {}
N 20 330 140 330 {}
N -20 330 20 330 {}
N -20 -330 20 -330 {}
N 20 -330 140 -330 {}
N 100 0 100 -250 {}
N 140 0 140 -220 {}
N -180 250 -140 250 {}
N -140 330 -140 250 {}
N -180 330 -180 280 {}
N -180 -280 -180 -330 {}
N -140 -250 -140 -330 {}
N -180 -250 -140 -250 {}
N -140 -330 -20 -330 {}
N -180 -330 -140 -330 {}
N -180 330 -140 330 {}
N -140 330 -20 330 {}
N -20 220 -20 0 {}
C {devices/ipin.sym} -280 0 0 0 {name=p1 lab=A}
C {devices/opin.sym} 370 0 0 0 {name=p2 lab=X}
C {devices/lab_pin.sym} -360 -330 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -360 330 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -200 250 0 0 {name=M1 w=0.420u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -40 250 0 0 {name=M2 w=0.420u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 120 250 0 0 {name=M3 w=0.420u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 280 250 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -200 -250 0 0 {name=M5 w=1.010u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -40 -250 0 0 {name=M6 w=2.400u l=0.625u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 120 -250 0 0 {name=M7 w=2.400u l=0.625u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 280 -250 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1250 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
