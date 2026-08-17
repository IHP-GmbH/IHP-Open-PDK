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
N 630 -160 650 -160 {}
N 630 -430 630 -610 {}
N 480 -160 480 -260 {}
N 320 -160 340 -160 {}
N 320 -360 460 -360 {}
N 460 -650 460 -710 {}
N 460 -710 480 -710 {}
N 380 -620 420 -620 {}
N 320 -160 320 -230 {}
N 630 -640 650 -640 {}
N 630 -160 630 -210 {}
N 460 -430 460 -480 {}
N 630 -430 690 -430 {}
N 630 -670 630 -710 {}
N 480 -160 630 -160 {}
N 590 -240 590 -430 {}
N 460 -360 460 -430 {}
N 320 -260 340 -260 {}
N 320 -290 320 -360 {}
N 460 -260 480 -260 {}
N 340 -160 460 -160 {}
N 630 -240 650 -240 {}
N 200 -160 320 -160 {}
N 480 -510 480 -620 {}
N 340 -160 340 -260 {}
N 650 -160 650 -240 {}
N 650 -640 650 -710 {}
N 410 -510 420 -510 {}
N 260 -260 280 -260 {}
N 410 -260 420 -260 {}
N 460 -160 460 -230 {}
N 460 -620 480 -620 {}
N 480 -620 480 -710 {}
N 460 -160 480 -160 {}
N 460 -510 480 -510 {}
N 590 -430 590 -640 {}
N 630 -270 630 -430 {}
N 630 -710 650 -710 {}
N 220 -710 460 -710 {}
N 480 -710 630 -710 {}
N 460 -540 460 -590 {}
N 460 -430 590 -430 {}
C {lab_wire.sym} 420 -510 0 0 {name=l1 sig_type=std_logic lab=B}
C {lab_wire.sym} 420 -260 0 0 {name=l2 sig_type=std_logic lab=A}
C {devices/opin.sym} 690 -430 0 0 {name=p1 lab=X}
C {devices/ipin.sym} 260 -260 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 380 -620 0 0 {name=p3 lab=A}
C {devices/lab_pin.sym} 220 -710 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 200 -160 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 300 -260 0 0 {name=M1 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 440 -260 0 0 {name=M2 w=0.550u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 610 -240 0 0 {name=M3 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 440 -620 0 0 {name=M4 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 440 -510 0 0 {name=M5 w=2.015u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 610 -640 0 0 {name=M6 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -810 440 0 0 {name=l1 author="IHP PDK AUTHORS"}
