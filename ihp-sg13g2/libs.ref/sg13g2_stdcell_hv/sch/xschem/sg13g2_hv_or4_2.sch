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
N 470 -350 490 -350 {}
N -50 130 -50 -230 {}
N 470 130 490 130 {}
N 230 210 250 210 {}
N 230 50 430 50 {}
N 470 210 490 210 {}
N 430 130 430 50 {}
N 470 -70 470 -320 {}
N 230 50 230 30 {}
N 490 -350 490 -470 {}
N -130 210 -130 160 {}
N -110 210 -10 210 {}
N 230 210 230 160 {}
N -80 -230 -50 -230 {}
N 110 210 110 160 {}
N -10 210 -10 160 {}
N -130 130 -110 130 {}
N -130 210 -110 210 {}
N -110 210 -110 130 {}
N -10 130 10 130 {}
N -10 210 10 210 {}
N 10 210 10 130 {}
N 110 130 130 130 {}
N 110 210 130 210 {}
N 130 210 130 130 {}
N 230 130 250 130 {}
N 250 210 250 130 {}
N 250 210 470 210 {}
N 50 -110 70 -110 {}
N -10 100 -10 70 {}
N 230 -30 230 -80 {}
N 230 -140 230 -200 {}
N 230 -260 230 -310 {}
N 230 100 230 70 {}
N 190 130 190 0 {}
N -130 100 -130 70 {}
N -50 -230 190 -230 {}
N -170 130 -170 -340 {}
N 110 100 110 70 {}
N 110 70 230 70 {}
N 10 210 110 210 {}
N 470 100 470 -70 {}
N 70 -110 190 -110 {}
N -10 70 110 70 {}
N -284 210 -130 210 {}
N -210 -340 -170 -340 {}
N 130 210 230 210 {}
N 160 0 190 0 {}
N 490 210 490 130 {}
N 250 -230 250 -340 {}
N 230 -370 230 -470 {}
N 230 -470 250 -470 {}
N -170 -340 190 -340 {}
N 470 -470 490 -470 {}
N 230 70 230 50 {}
N -274 -470 230 -470 {}
N -130 70 -10 70 {}
N 70 130 70 -110 {}
N 470 210 470 160 {}
N 470 -70 510 -70 {}
N 470 -380 470 -470 {}
N 430 50 430 -350 {}
N 230 -340 250 -340 {}
N 230 -230 250 -230 {}
N 230 -110 250 -110 {}
N 230 0 250 0 {}
N 250 0 250 -110 {}
N 250 -340 250 -470 {}
N 250 -470 470 -470 {}
N 250 -110 250 -230 {}
C {devices/opin.sym} 510 -70 0 0 {name=p1 lab=X}
C {devices/ipin.sym} -210 -340 0 0 {name=p2 lab=A}
C {devices/ipin.sym} -80 -230 0 0 {name=p3 lab=B}
C {devices/ipin.sym} 50 -110 0 0 {name=p4 lab=C}
C {devices/ipin.sym} 160 0 0 0 {name=p5 lab=D}
C {devices/lab_pin.sym} -274 -470 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -284 210 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -150 130 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -30 130 0 0 {name=M2 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 90 130 0 0 {name=M3 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 210 130 0 0 {name=M4 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 450 130 0 0 {name=M5 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 210 -340 0 0 {name=M6 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 210 -230 0 0 {name=M7 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 210 -110 0 0 {name=M8 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 210 0 0 0 {name=M9 w=2.400u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 450 -350 0 0 {name=M10 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1140 760 0 0 {name=l1 author="IHP PDK AUTHORS"}
