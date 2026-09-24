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
N -80 -620 60 -620 {}
N -60 -300 100 -300 {}
N 380 -620 380 -700 {}
N -176 -820 -80 -820 {}
N 100 -570 100 -620 {}
N -60 -730 -60 -820 {}
N 270 -820 380 -820 {}
N -80 -730 -60 -730 {}
N -80 -380 -60 -380 {}
N 120 -360 120 -450 {}
N 270 -730 270 -820 {}
N 100 -300 120 -300 {}
N 250 -620 250 -700 {}
N 100 -760 100 -820 {}
N 250 -730 270 -730 {}
N 100 -730 120 -730 {}
N 120 -450 120 -540 {}
N 400 -730 400 -820 {}
N 380 -820 400 -820 {}
N 380 -730 400 -730 {}
N 120 -300 120 -360 {}
N -80 -620 -80 -700 {}
N 20 -450 60 -450 {}
N -60 -300 -60 -380 {}
N -80 -410 -80 -620 {}
N -60 -820 100 -820 {}
N 100 -390 100 -420 {}
N 100 -620 100 -700 {}
N 100 -540 120 -540 {}
N -80 -820 -60 -820 {}
N 100 -480 100 -510 {}
N -190 -300 -80 -300 {}
N -120 -380 -120 -620 {}
N -80 -300 -60 -300 {}
N 60 -540 60 -620 {}
N 380 -620 420 -620 {}
N 190 -730 210 -730 {}
N 380 -760 380 -820 {}
N 100 -300 100 -330 {}
N 250 -620 380 -620 {}
N 320 -730 340 -730 {}
N 100 -620 250 -620 {}
N -120 -620 -120 -730 {}
N -80 -300 -80 -350 {}
N 100 -360 120 -360 {}
N 120 -820 250 -820 {}
N 20 -360 60 -360 {}
N -160 -620 -120 -620 {}
N 100 -450 120 -450 {}
N 250 -820 270 -820 {}
N 250 -760 250 -820 {}
N -80 -760 -80 -820 {}
N 120 -730 120 -820 {}
N 100 -820 120 -820 {}
N 60 -620 60 -730 {}
C {lab_wire.sym} 40 -450 0 0 {name=l1 sig_type=std_logic lab=B}
C {lab_wire.sym} 200 -730 0 0 {name=l2 sig_type=std_logic lab=B}
C {lab_wire.sym} 330 -730 0 0 {name=l3 sig_type=std_logic lab=C}
C {lab_wire.sym} 40 -360 0 0 {name=l4 sig_type=std_logic lab=C}
C {devices/ipin.sym} -160 -620 0 0 {name=p1 lab=A_N}
C {devices/ipin.sym} 20 -450 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 20 -360 0 0 {name=p3 lab=C}
C {devices/opin.sym} 420 -620 0 0 {name=p4 lab=Y}
C {devices/lab_pin.sym} -176 -820 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -190 -300 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -100 -380 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 80 -540 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 80 -450 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 80 -360 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -100 -730 0 0 {name=M5 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 80 -730 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 230 -730 0 0 {name=M7 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 360 -730 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1130 320 0 0 {name=l1 author="IHP PDK AUTHORS"}
