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
N 460 -290 460 -360 {}
N 480 -710 630 -710 {}
N 480 -160 630 -160 {}
N 590 -410 590 -600 {}
N 300 -160 320 -160 {}
N 320 -160 460 -160 {}
N 460 -410 460 -480 {}
N 630 -600 650 -600 {}
N 460 -650 460 -710 {}
N 630 -710 650 -710 {}
N 390 -620 420 -620 {}
N 300 -160 300 -230 {}
N 650 -600 650 -710 {}
N 460 -710 480 -710 {}
N 630 -160 630 -250 {}
N 210 -160 300 -160 {}
N 220 -710 460 -710 {}
N 630 -630 630 -710 {}
N 590 -280 590 -410 {}
N 300 -260 320 -260 {}
N 300 -290 300 -360 {}
N 460 -260 480 -260 {}
N 460 -360 460 -410 {}
N 630 -280 650 -280 {}
N 480 -160 480 -260 {}
N 630 -160 650 -160 {}
N 650 -160 650 -280 {}
N 400 -510 420 -510 {}
N 230 -260 260 -260 {}
N 410 -260 420 -260 {}
N 460 -160 460 -230 {}
N 460 -620 480 -620 {}
N 460 -160 480 -160 {}
N 460 -510 480 -510 {}
N 480 -620 480 -710 {}
N 320 -160 320 -260 {}
N 630 -310 630 -410 {}
N 630 -410 680 -410 {}
N 460 -410 590 -410 {}
N 480 -510 480 -620 {}
N 460 -540 460 -590 {}
N 300 -360 460 -360 {}
N 630 -410 630 -570 {}
C {lab_wire.sym} 410 -510 0 0 {name=l1 sig_type=std_logic lab=B}
C {lab_wire.sym} 420 -260 0 0 {name=l2 sig_type=std_logic lab=A}
C {devices/opin.sym} 680 -410 0 0 {name=p1 lab=X}
C {devices/ipin.sym} 230 -260 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 390 -620 0 0 {name=p3 lab=A}
C {devices/lab_pin.sym} 220 -710 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 210 -160 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 280 -260 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 440 -260 0 0 {name=M2 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 610 -280 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 440 -620 0 0 {name=M4 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 440 -510 0 0 {name=M5 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 610 -600 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -810 440 0 0 {name=l1 author="IHP PDK AUTHORS"}
