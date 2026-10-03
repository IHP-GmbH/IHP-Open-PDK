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
N 390 -240 410 -240 {}
N 390 210 410 210 {}
N 230 90 230 30 {}
N 230 90 350 90 {}
N 250 290 390 290 {}
N 410 290 410 210 {}
N -210 210 -210 -340 {}
N 390 290 390 240 {}
N 230 290 250 290 {}
N 350 90 350 -240 {}
N 230 180 230 150 {}
N 350 210 350 90 {}
N 250 -400 390 -400 {}
N -290 290 -170 290 {}
N -170 290 -170 240 {}
N -80 -230 190 -230 {}
N 230 290 230 240 {}
N 110 290 230 290 {}
N 90 290 90 240 {}
N -40 290 -40 240 {}
N -170 210 -150 210 {}
N -170 290 -150 290 {}
N -150 290 -150 210 {}
N -20 290 90 290 {}
N -40 210 -20 210 {}
N -40 290 -20 290 {}
N -20 290 -20 210 {}
N -40 150 90 150 {}
N 90 210 110 210 {}
N 90 290 110 290 {}
N 110 290 110 210 {}
N 230 210 250 210 {}
N 250 290 250 210 {}
N 230 150 230 90 {}
N 230 -30 230 -80 {}
N 230 -140 230 -200 {}
N 230 -260 230 -310 {}
N 390 -30 440 -30 {}
N -210 -340 190 -340 {}
N 90 180 90 150 {}
N 90 150 230 150 {}
N -170 180 -170 150 {}
N -40 180 -40 150 {}
N 190 210 190 0 {}
N -240 -340 -210 -340 {}
N 50 210 50 -110 {}
N 150 0 190 0 {}
N 390 -30 390 -210 {}
N -80 210 -80 -230 {}
N 230 -370 230 -400 {}
N 390 -270 390 -400 {}
N 250 -340 250 -400 {}
N 390 180 390 -30 {}
N -280 -400 230 -400 {}
N -170 150 -40 150 {}
N -150 290 -40 290 {}
N -100 -230 -80 -230 {}
N 50 -110 190 -110 {}
N 30 -110 50 -110 {}
N 390 290 410 290 {}
N 230 -400 250 -400 {}
N 230 -340 250 -340 {}
N 390 -400 410 -400 {}
N 230 -110 250 -110 {}
N 230 0 250 0 {}
N 250 0 250 -110 {}
N 410 -240 410 -400 {}
N 230 -230 250 -230 {}
N 250 -110 250 -230 {}
N 250 -230 250 -340 {}
C {devices/opin.sym} 440 -30 0 0 {name=p1 lab=X}
C {devices/ipin.sym} -240 -340 0 0 {name=p2 lab=A}
C {devices/ipin.sym} -100 -230 0 0 {name=p3 lab=B}
C {devices/ipin.sym} 30 -110 0 0 {name=p4 lab=C}
C {devices/ipin.sym} 150 0 0 0 {name=p5 lab=D}
C {devices/lab_pin.sym} -280 -400 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -290 290 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -190 210 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -60 210 0 0 {name=M2 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 70 210 0 0 {name=M3 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 210 210 0 0 {name=M4 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 370 210 0 0 {name=M5 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 210 -340 0 0 {name=M6 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 210 -230 0 0 {name=M7 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 210 -110 0 0 {name=M8 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 210 0 0 0 {name=M9 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 370 -240 0 0 {name=M10 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1170 820 0 0 {name=l1 author="IHP PDK AUTHORS"}
