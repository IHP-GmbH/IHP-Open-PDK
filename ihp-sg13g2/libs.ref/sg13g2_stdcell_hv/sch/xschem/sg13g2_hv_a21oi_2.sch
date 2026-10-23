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
N -200 -180 -130 -180 {}
N -130 -180 -130 -280 {}
N -260 -180 -260 -280 {}
N -200 -210 -200 -280 {}
N 100 510 100 420 {}
N -200 70 -130 70 {}
N -440 -280 -330 -280 {}
N -240 -20 -40 -20 {}
N -370 -50 -370 -180 {}
N -200 420 -130 420 {}
N -130 70 -130 -180 {}
N -370 -50 -10 -50 {}
N -240 -20 -240 -180 {}
N -330 -210 -330 -280 {}
N 30 510 100 510 {}
N -200 510 -200 450 {}
N -240 200 -240 70 {}
N 30 200 100 200 {}
N -330 -180 -260 -180 {}
N 30 290 100 290 {}
N -330 -280 -260 -280 {}
N -440 510 -200 510 {}
N -260 -280 -200 -280 {}
N 100 420 100 290 {}
N -130 510 30 510 {}
N -330 -120 -200 -120 {}
N -200 40 -200 -120 {}
N -200 -120 -200 -150 {}
N -130 510 -130 420 {}
N -430 -50 -370 -50 {}
N -430 -20 -240 -20 {}
N 30 420 100 420 {}
N 30 510 30 450 {}
N -200 390 -200 200 {}
N -200 -280 -130 -280 {}
N 30 390 30 320 {}
N 30 260 30 200 {}
N -200 200 30 200 {}
N -10 290 -10 -50 {}
N -330 -120 -330 -150 {}
N -40 420 -40 -20 {}
N -200 510 -130 510 {}
N -240 420 -240 200 {}
N -200 200 -200 100 {}
N -40 420 -10 420 {}
N -290 200 -240 200 {}
C {devices/ipin.sym} -430 -50 0 0 {name=p1 lab=A1}
C {devices/ipin.sym} -430 -20 0 0 {name=p2 lab=A2}
C {devices/ipin.sym} -290 200 0 0 {name=p3 lab=B1}
C {devices/opin.sym} 100 200 0 0 {name=p4 lab=Y}
C {devices/lab_pin.sym} -440 -280 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -440 510 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -220 420 0 0 {name=M1 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 10 290 0 0 {name=M2 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 10 420 0 0 {name=M3 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -350 -180 0 0 {name=M4 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -220 -180 0 0 {name=M5 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -220 70 0 0 {name=M6 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1420 1000 0 0 {name=l1 author="IHP PDK AUTHORS"}
