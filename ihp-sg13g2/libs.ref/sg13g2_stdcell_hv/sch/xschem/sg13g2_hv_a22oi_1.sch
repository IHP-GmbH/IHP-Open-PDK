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
N -140 -210 -140 -270 {}
N -420 -270 -350 -270 {}
N -420 -240 -420 -270 {}
N -610 500 -210 500 {}
N -210 -100 -210 -180 {}
N -210 -240 -210 -270 {}
N 20 500 20 470 {}
N -460 -60 -460 -210 {}
N -460 440 -250 440 {}
N -610 -270 -420 -270 {}
N -140 60 -140 -210 {}
N -210 440 -130 440 {}
N -250 -30 -50 -30 {}
N -210 290 -130 290 {}
N -210 260 -210 190 {}
N -420 30 -420 -100 {}
N -210 190 20 190 {}
N 20 190 90 190 {}
N -210 -270 -140 -270 {}
N 20 290 100 290 {}
N -130 500 20 500 {}
N 20 260 20 190 {}
N -420 -210 -350 -210 {}
N -130 440 -130 290 {}
N -210 500 -210 470 {}
N -210 60 -140 60 {}
N -350 -270 -210 -270 {}
N -500 440 -460 440 {}
N -210 30 -210 -100 {}
N -210 410 -210 320 {}
N -50 440 -50 -30 {}
N -210 170 -210 90 {}
N -420 -100 -210 -100 {}
N -420 -100 -420 -180 {}
N -350 -210 -350 -270 {}
N -130 500 -130 440 {}
N -290 290 -250 290 {}
N 20 440 100 440 {}
N 20 500 100 500 {}
N 20 410 20 320 {}
N -420 170 -420 90 {}
N -350 60 -350 -210 {}
N -280 -210 -250 -210 {}
N -20 290 -20 -60 {}
N -490 -210 -460 -210 {}
N -420 60 -350 60 {}
N -210 500 -130 500 {}
N -50 440 -20 440 {}
N -210 -210 -140 -210 {}
N -210 190 -210 170 {}
N -250 -30 -250 -210 {}
N -420 170 -210 170 {}
N -460 440 -460 60 {}
N 100 500 100 440 {}
N -250 290 -250 60 {}
N 100 440 100 290 {}
N -460 -60 -20 -60 {}
C {devices/ipin.sym} -490 -210 0 0 {name=p1 lab=A1}
C {devices/ipin.sym} -280 -210 0 0 {name=p2 lab=A2}
C {devices/ipin.sym} -500 440 0 0 {name=p3 lab=B1}
C {devices/opin.sym} 90 190 0 0 {name=p4 lab=Y}
C {devices/lab_pin.sym} -610 -270 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -610 500 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {devices/ipin.sym} -290 290 0 0 {name=p7 lab=B2}
C {sg13_hv_nmos.sym} -230 290 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -230 440 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 0 290 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 0 440 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -440 -210 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -440 60 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -230 -210 0 0 {name=M7 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -230 60 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1510 1000 0 0 {name=l1 author="IHP PDK AUTHORS"}
