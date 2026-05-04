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
N -180 280 -100 280 {}
N -100 190 -100 30 {}
N 50 280 250 280 {}
N -100 280 -20 280 {}
N -20 -160 50 -160 {}
N -20 280 50 280 {}
N -20 -190 -20 -220 {}
N -20 -360 -20 -400 {}
N -440 280 -180 280 {}
N -180 -220 -20 -220 {}
N -140 -400 -20 -400 {}
N -20 280 -20 160 {}
N -100 280 -100 190 {}
N -180 30 -100 30 {}
N 50 -160 50 -330 {}
N -270 190 -270 -330 {}
N -430 -400 -180 -400 {}
N -20 130 50 130 {}
N -180 190 -100 190 {}
N 250 160 320 160 {}
N 250 130 250 -40 {}
N -180 -220 -180 -230 {}
N -20 -220 -20 -300 {}
N -180 -260 -140 -260 {}
N 210 160 210 -60 {}
N -270 190 -220 190 {}
N -180 -290 -180 -400 {}
N -180 -400 -140 -400 {}
N 50 280 50 130 {}
N -270 -330 -60 -330 {}
N -350 130 -60 130 {}
N -350 190 -270 190 {}
N 320 -290 320 -400 {}
N 250 -400 320 -400 {}
N -20 -60 210 -60 {}
N -340 30 -220 30 {}
N -60 130 -60 -160 {}
N 250 -40 310 -40 {}
N -20 -330 50 -330 {}
N 50 -330 50 -400 {}
N 250 -320 250 -400 {}
N 250 -290 320 -290 {}
N -220 30 -220 -260 {}
N -140 -260 -140 -400 {}
N -20 -400 50 -400 {}
N 250 -40 250 -260 {}
N -20 100 -20 -20 {}
N 50 -400 250 -400 {}
N -180 -20 -20 -20 {}
N -180 0 -180 -20 {}
N -20 -60 -20 -130 {}
N 250 280 320 280 {}
N 210 -60 210 -290 {}
N -180 160 -180 60 {}
N 320 280 320 160 {}
N -180 280 -180 220 {}
N -20 -20 -20 -60 {}
N 250 280 250 190 {}
C {devices/opin.sym} 310 -40 0 0 {name=p1 lab=X}
C {devices/ipin.sym} -340 30 0 0 {name=p2 lab=A1}
C {devices/ipin.sym} -350 190 0 0 {name=p3 lab=A2}
C {devices/ipin.sym} -350 130 0 0 {name=p4 lab=B1}
C {devices/iopin.sym} -430 -400 2 0 {name=p5 lab=VDD}
C {devices/iopin.sym} -440 280 2 0 {name=p6 lab=VSS}
C {sg13_lv_nmos.sym} -200 30 0 0 {name=M1 w=740.00n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_nmos.sym} -200 190 0 0 {name=M2 w=740.00n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_nmos.sym} -40 130 0 0 {name=M3 w=740.00n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_nmos.sym} 230 160 0 0 {name=M4 w=1.48u l=130.00n ng=2 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} -200 -260 0 0 {name=M5 w=1.000u l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {sg13_lv_pmos.sym} -40 -330 0 0 {name=M6 w=1.000u l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {sg13_lv_pmos.sym} -40 -160 0 0 {name=M7 w=1.000u l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {sg13_lv_pmos.sym} 230 -290 0 0 {name=M8 w=2.24u l=130.00n ng=2 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -1310 820 0 0 {name=l1 author="IHP PDK AUTHORS"}
