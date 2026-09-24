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
N -760 -600 -760 -650 {}
N -816 -490 -760 -490 {}
N -250 -650 -250 -680 {}
N -420 -570 -360 -570 {}
N -250 -600 -250 -640 {}
N -760 -650 -590 -650 {}
N -250 -820 -250 -840 {}
N -250 -740 -250 -760 {}
N -180 -790 -180 -870 {}
N -250 -870 -180 -870 {}
N -760 -570 -700 -570 {}
N -420 -490 -420 -540 {}
N -590 -570 -540 -570 {}
N -420 -490 -360 -490 {}
N -250 -790 -180 -790 {}
N -250 -490 -250 -540 {}
N -180 -870 -180 -950 {}
N -760 -490 -700 -490 {}
N -420 -600 -420 -650 {}
N -250 -950 -180 -950 {}
N -180 -950 -180 -1020 {}
N -360 -490 -360 -570 {}
N -540 -490 -420 -490 {}
N -250 -710 -180 -710 {}
N -250 -640 -250 -650 {}
N -590 -490 -540 -490 {}
N -420 -950 -290 -950 {}
N -420 -790 -290 -790 {}
N -660 -570 -630 -570 {}
N -250 -900 -250 -920 {}
N -830 -570 -800 -570 {}
N -420 -870 -290 -870 {}
N -360 -490 -250 -490 {}
N -420 -710 -290 -710 {}
N -590 -490 -590 -540 {}
N -590 -650 -420 -650 {}
N -590 -600 -590 -650 {}
N -540 -490 -540 -570 {}
N -180 -710 -180 -790 {}
N -700 -490 -590 -490 {}
N -250 -640 -170 -640 {}
N -250 -980 -250 -1020 {}
N -490 -570 -460 -570 {}
N -310 -570 -290 -570 {}
N -420 -650 -250 -650 {}
N -250 -1020 -180 -1020 {}
N -760 -490 -760 -540 {}
N -250 -490 -200 -490 {}
N -700 -490 -700 -570 {}
N -510 -1020 -250 -1020 {}
N -200 -490 -200 -570 {}
N -250 -570 -200 -570 {}
C {lab_wire.sym} -360 -950 0 0 {name=l1 sig_type=std_logic lab=A}
C {lab_wire.sym} -360 -790 0 0 {name=l2 sig_type=std_logic lab=C}
C {lab_wire.sym} -640 -570 0 0 {name=l3 sig_type=std_logic lab=B}
C {lab_wire.sym} -820 -570 0 0 {name=l4 sig_type=std_logic lab=A}
C {lab_wire.sym} -360 -870 0 0 {name=l5 sig_type=std_logic lab=B}
C {lab_wire.sym} -360 -710 0 0 {name=l6 sig_type=std_logic lab=D}
C {lab_wire.sym} -480 -570 0 0 {name=l7 sig_type=std_logic lab=C}
C {lab_wire.sym} -300 -570 0 0 {name=l8 sig_type=std_logic lab=D}
C {devices/opin.sym} -170 -640 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} -420 -950 0 0 {name=p2 lab=A}
C {devices/ipin.sym} -420 -870 0 0 {name=p3 lab=B}
C {devices/ipin.sym} -420 -790 0 0 {name=p4 lab=C}
C {devices/ipin.sym} -420 -710 0 0 {name=p5 lab=D}
C {devices/lab_pin.sym} -510 -1020 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -816 -490 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -780 -570 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -610 -570 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -440 -570 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -270 -570 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -270 -950 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -270 -870 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -270 -790 0 0 {name=M7 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -270 -710 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1750 120 0 0 {name=l1 author="IHP PDK AUTHORS"}
