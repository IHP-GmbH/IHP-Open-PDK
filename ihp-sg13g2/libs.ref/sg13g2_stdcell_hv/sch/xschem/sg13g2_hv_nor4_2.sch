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
N -820 -490 -760 -490 {}
N -420 -570 -400 -570 {}
N -250 -600 -250 -640 {}
N -600 -640 -510 -640 {}
N -760 -490 -740 -490 {}
N -510 -810 -510 -830 {}
N -510 -730 -510 -750 {}
N -490 -780 -490 -860 {}
N -760 -570 -740 -570 {}
N -250 -490 -230 -490 {}
N -510 -860 -490 -860 {}
N -420 -490 -420 -540 {}
N -600 -570 -580 -570 {}
N -760 -600 -760 -640 {}
N -400 -490 -250 -490 {}
N -250 -490 -250 -540 {}
N -740 -490 -600 -490 {}
N -510 -640 -420 -640 {}
N -510 -1010 -490 -1010 {}
N -510 -640 -510 -670 {}
N -510 -780 -490 -780 {}
N -510 -700 -490 -700 {}
N -400 -490 -400 -570 {}
N -600 -490 -580 -490 {}
N -490 -700 -490 -780 {}
N -760 -640 -600 -640 {}
N -580 -490 -420 -490 {}
N -680 -940 -550 -940 {}
N -680 -780 -550 -780 {}
N -670 -570 -640 -570 {}
N -510 -890 -510 -910 {}
N -490 -860 -490 -940 {}
N -830 -570 -800 -570 {}
N -680 -860 -550 -860 {}
N -680 -700 -550 -700 {}
N -600 -490 -600 -540 {}
N -420 -600 -420 -640 {}
N -580 -490 -580 -570 {}
N -490 -940 -490 -1010 {}
N -420 -640 -250 -640 {}
N -510 -970 -510 -1010 {}
N -490 -570 -460 -570 {}
N -310 -570 -290 -570 {}
N -250 -640 -170 -640 {}
N -510 -940 -490 -940 {}
N -760 -490 -760 -540 {}
N -420 -490 -400 -490 {}
N -740 -490 -740 -570 {}
N -600 -600 -600 -640 {}
N -230 -490 -230 -570 {}
N -250 -570 -230 -570 {}
N -820 -1010 -510 -1010 {}
C {lab_wire.sym} -620 -940 0 0 {name=l1 sig_type=std_logic lab=A}
C {lab_wire.sym} -620 -780 0 0 {name=l2 sig_type=std_logic lab=C}
C {lab_wire.sym} -660 -570 0 0 {name=l3 sig_type=std_logic lab=B}
C {lab_wire.sym} -820 -570 0 0 {name=l4 sig_type=std_logic lab=A}
C {lab_wire.sym} -620 -860 0 0 {name=l5 sig_type=std_logic lab=B}
C {lab_wire.sym} -620 -700 0 0 {name=l6 sig_type=std_logic lab=D}
C {lab_wire.sym} -480 -570 0 0 {name=l7 sig_type=std_logic lab=C}
C {lab_wire.sym} -300 -570 0 0 {name=l8 sig_type=std_logic lab=D}
C {devices/opin.sym} -170 -640 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} -680 -940 0 0 {name=p2 lab=A}
C {devices/ipin.sym} -680 -860 0 0 {name=p3 lab=B}
C {devices/ipin.sym} -680 -780 0 0 {name=p4 lab=C}
C {devices/ipin.sym} -680 -700 0 0 {name=p5 lab=D}
C {devices/lab_pin.sym} -820 -1010 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -820 -490 0 0 {name=p7 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -780 -570 0 0 {name=M1 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -620 -570 0 0 {name=M2 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -440 -570 0 0 {name=M3 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -270 -570 0 0 {name=M4 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -530 -940 0 0 {name=M5 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -530 -860 0 0 {name=M6 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -530 -780 0 0 {name=M7 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -530 -700 0 0 {name=M8 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1750 140 0 0 {name=l1 author="IHP PDK AUTHORS"}
