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
N 110 -130 110 -220 {}
N -300 -10 -90 -10 {}
N 110 190 110 110 {}
N 90 80 90 -10 {}
N -230 -130 -210 -130 {}
N -50 -130 -30 -130 {}
N -370 -270 -230 -270 {}
N -30 310 90 310 {}
N 90 -250 90 -270 {}
N 90 -270 110 -270 {}
N 90 160 90 140 {}
N 90 310 110 310 {}
N -50 250 -30 250 {}
N -230 310 -210 310 {}
N -230 250 -210 250 {}
N -270 70 -270 -130 {}
N -230 -160 -230 -270 {}
N -50 310 -30 310 {}
N 50 110 50 30 {}
N 90 -10 120 -10 {}
N -230 310 -230 280 {}
N -90 250 -90 -10 {}
N -230 30 -230 -100 {}
N -230 30 50 30 {}
N 90 -10 90 -100 {}
N 90 110 110 110 {}
N 110 310 110 190 {}
N -210 310 -50 310 {}
N 90 -160 90 -190 {}
N -50 220 -50 190 {}
N -356 310 -230 310 {}
N -230 -270 -210 -270 {}
N -50 -160 -50 -270 {}
N -270 250 -270 70 {}
N -210 -130 -210 -270 {}
N 90 310 90 220 {}
N -300 -220 50 -220 {}
N -30 -270 90 -270 {}
N -210 310 -210 250 {}
N -30 310 -30 250 {}
N -330 70 -270 70 {}
N -330 -10 -300 -10 {}
N -90 -10 -90 -130 {}
N 110 -220 110 -270 {}
N -30 -130 -30 -270 {}
N -230 220 -230 30 {}
N -50 310 -50 280 {}
N -210 -270 -50 -270 {}
N -50 190 50 190 {}
N -50 -270 -30 -270 {}
N 50 30 50 -130 {}
N 90 -130 110 -130 {}
N 90 -220 110 -220 {}
N -300 -10 -300 -220 {}
N 90 190 110 190 {}
N -50 190 -50 -100 {}
C {devices/ipin.sym} -330 70 0 0 {name=p1 lab=A}
C {devices/ipin.sym} -330 -10 0 0 {name=p2 lab=TE_B}
C {devices/opin.sym} 120 -10 0 0 {name=p3 lab=Z}
C {devices/lab_pin.sym} -370 -270 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -356 310 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -250 250 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -70 250 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 70 110 0 0 {name=M3 w=2.960u l=0.450u ng=4 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 70 190 0 0 {name=M4 w=2.960u l=0.450u ng=4 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -250 -130 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -70 -130 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 70 -220 0 0 {name=M7 w=10.760u l=0.450u ng=4 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 70 -130 0 0 {name=M8 w=10.760u l=0.450u ng=4 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1370 900 0 0 {name=l1 author="IHP PDK AUTHORS"}
