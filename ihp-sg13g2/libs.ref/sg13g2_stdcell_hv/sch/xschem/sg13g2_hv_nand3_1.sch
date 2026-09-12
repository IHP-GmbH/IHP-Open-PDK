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
N 470 -620 470 -700 {}
N 100 -270 180 -270 {}
N 100 -180 100 -240 {}
N 350 -820 470 -820 {}
N 280 -620 280 -700 {}
N 100 -760 100 -820 {}
N 280 -730 350 -730 {}
N 100 -730 170 -730 {}
N 180 -270 180 -390 {}
N 180 -390 180 -520 {}
N 100 -520 180 -520 {}
N 100 -420 100 -490 {}
N 30 -270 60 -270 {}
N 280 -620 470 -620 {}
N 100 -550 100 -620 {}
N 100 -300 100 -360 {}
N 100 -620 100 -700 {}
N 470 -620 520 -620 {}
N 180 -180 180 -270 {}
N -46 -820 100 -820 {}
N 220 -730 240 -730 {}
N 470 -760 470 -820 {}
N 60 -520 60 -730 {}
N 410 -730 430 -730 {}
N 20 -730 60 -730 {}
N 100 -820 170 -820 {}
N 30 -390 60 -390 {}
N 470 -820 540 -820 {}
N 470 -730 540 -730 {}
N 540 -730 540 -820 {}
N 100 -620 280 -620 {}
N 350 -730 350 -820 {}
N 280 -820 350 -820 {}
N 100 -180 180 -180 {}
N 170 -730 170 -820 {}
N -50 -180 100 -180 {}
N 100 -390 180 -390 {}
N 170 -820 280 -820 {}
N 280 -760 280 -820 {}
C {lab_wire.sym} 40 -270 0 0 {name=l1 sig_type=std_logic lab=C}
C {lab_wire.sym} 230 -730 0 0 {name=l2 sig_type=std_logic lab=B}
C {lab_wire.sym} 420 -730 0 0 {name=l3 sig_type=std_logic lab=C}
C {lab_wire.sym} 40 -390 0 0 {name=l4 sig_type=std_logic lab=B}
C {devices/ipin.sym} 20 -730 0 0 {name=p1 lab=A}
C {devices/ipin.sym} 30 -390 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 30 -270 0 0 {name=p3 lab=C}
C {devices/opin.sym} 520 -620 0 0 {name=p4 lab=Y}
C {devices/lab_pin.sym} -46 -820 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -50 -180 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 80 -520 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 80 -390 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 80 -270 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 80 -730 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 260 -730 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 450 -730 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1010 380 0 0 {name=l1 author="IHP PDK AUTHORS"}
