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
N 110 -370 190 -370 {}
N 360 -210 360 -240 {}
N 280 -210 360 -210 {}
N 190 40 190 -370 {}
N 360 10 360 -110 {}
N 240 -110 360 -110 {}
N 280 10 360 10 {}
N 360 40 360 10 {}
N 280 -270 280 -370 {}
N 360 170 360 40 {}
N 360 -240 360 -370 {}
N 240 -110 240 -240 {}
N 280 -240 360 -240 {}
N 280 170 360 170 {}
N 190 -370 280 -370 {}
N 110 170 280 170 {}
N 280 170 280 70 {}
N 190 40 240 40 {}
N 280 40 360 40 {}
N 280 -370 360 -370 {}
C {devices/lab_pin.sym} 110 -370 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 110 170 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 260 40 0 0 {name=M1 w=0.420u l=1.000u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 260 -240 0 0 {name=M2 w=2.400u l=1.000u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1010 780 0 0 {name=l1 author="IHP PDK AUTHORS"}
