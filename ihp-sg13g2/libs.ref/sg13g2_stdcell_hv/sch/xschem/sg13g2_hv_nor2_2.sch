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
N 940 -630 950 -630 {}
N 710 -630 740 -630 {}
N 950 -540 950 -630 {}
N 940 -660 940 -710 {}
N 780 -350 800 -350 {}
N 780 -380 780 -460 {}
N 940 -570 940 -600 {}
N 780 -460 940 -460 {}
N 870 -340 900 -340 {}
N 940 -460 940 -490 {}
N 780 -280 780 -320 {}
N 690 -280 780 -280 {}
N 940 -540 950 -540 {}
N 940 -370 940 -460 {}
N 800 -280 800 -350 {}
N 940 -280 940 -310 {}
N 740 -630 900 -630 {}
N 950 -280 950 -340 {}
N 940 -710 950 -710 {}
N 900 -340 900 -540 {}
N 940 -490 940 -510 {}
N 940 -280 950 -280 {}
N 940 -340 950 -340 {}
N 690 -710 940 -710 {}
N 800 -280 940 -280 {}
N 740 -350 740 -630 {}
N 950 -630 950 -710 {}
N 780 -280 800 -280 {}
N 940 -490 1010 -490 {}
C {devices/opin.sym} 1010 -490 0 0 {name=p1 lab=Y}
C {devices/ipin.sym} 870 -340 0 0 {name=p2 lab=B}
C {devices/ipin.sym} 710 -630 0 0 {name=p3 lab=A}
C {devices/lab_pin.sym} 690 -710 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 690 -280 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 760 -350 0 0 {name=M1 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 920 -340 0 0 {name=M2 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 920 -630 0 0 {name=M3 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 920 -540 0 0 {name=M4 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -400 380 0 0 {name=l1 author="IHP PDK AUTHORS"}
