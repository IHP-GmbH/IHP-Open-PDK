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
N 1594 -270 1840 -270 {}
N 1840 -270 1860 -270 {}
N 1840 -590 1860 -590 {}
N 1900 -680 1920 -680 {}
N 1920 -270 1920 -420 {}
N 1618 -680 1740 -680 {}
N 1900 -480 1900 -500 {}
N 1920 -590 1920 -680 {}
N 1740 -500 1900 -500 {}
N 1900 -300 1900 -390 {}
N 1740 -590 1760 -590 {}
N 1740 -500 1740 -560 {}
N 1920 -160 1920 -270 {}
N 1760 -590 1760 -680 {}
N 1900 -450 1900 -480 {}
N 1900 -480 1990 -480 {}
N 1700 -420 1860 -420 {}
N 1740 -680 1760 -680 {}
N 1840 -270 1840 -590 {}
N 1760 -680 1900 -680 {}
N 1608 -160 1900 -160 {}
N 1900 -620 1900 -680 {}
N 1900 -590 1920 -590 {}
N 1600 -590 1700 -590 {}
N 1900 -420 1920 -420 {}
N 1900 -160 1920 -160 {}
N 1900 -160 1900 -240 {}
N 1900 -500 1900 -560 {}
N 1900 -270 1920 -270 {}
N 1740 -620 1740 -680 {}
N 1700 -420 1700 -590 {}
C {devices/lab_pin.sym} 1618 -680 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 1608 -160 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {devices/opin.sym} 1990 -480 0 0 {name=p3 lab=Y}
C {devices/ipin.sym} 1594 -270 0 0 {name=p4 lab=B}
C {devices/ipin.sym} 1600 -590 0 0 {name=p5 lab=A}
C {sg13_hv_nmos.sym} 1880 -420 0 0 {name=M1 w=1.440u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 1880 -270 0 0 {name=M2 w=1.440u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 1720 -590 0 0 {name=M3 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 1880 -590 0 0 {name=M4 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} 540 460 0 0 {name=l1 author="IHP PDK AUTHORS"}
