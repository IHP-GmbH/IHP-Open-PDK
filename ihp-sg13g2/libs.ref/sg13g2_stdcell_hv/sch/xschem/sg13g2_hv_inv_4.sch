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
N 580 470 580 210 {}
N 620 -50 620 -130 {}
N 620 470 690 470 {}
N 550 210 580 210 {}
N 620 440 620 210 {}
N 620 610 620 500 {}
N 620 210 650 210 {}
N 620 210 620 10 {}
N 620 -20 690 -20 {}
N 454 -130 620 -130 {}
N 454 610 620 610 {}
N 690 610 690 470 {}
N 580 210 580 -20 {}
N 620 610 690 610 {}
N 690 -20 690 -130 {}
N 620 -130 690 -130 {}
C {devices/ipin.sym} 550 210 0 0 {name=p1 lab=A}
C {devices/opin.sym} 650 210 0 0 {name=p2 lab=Y}
C {devices/lab_pin.sym} 454 -130 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 454 610 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 600 470 0 0 {name=M1 w=2.960u l=0.450u ng=4 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 600 -20 0 0 {name=M2 w=10.760u l=0.450u ng=4 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -680 1120 0 0 {name=l1 author="IHP PDK AUTHORS"}
