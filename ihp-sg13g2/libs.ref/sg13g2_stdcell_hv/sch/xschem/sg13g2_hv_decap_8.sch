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
N 170 -160 250 -160 {}
N 170 -480 250 -480 {}
N 250 -480 250 -510 {}
N 80 -160 80 -580 {}
N 250 -160 250 -190 {}
N 170 -510 250 -510 {}
N 0 -90 170 -90 {}
N 80 -580 170 -580 {}
N 0 -580 80 -580 {}
N 250 -510 250 -580 {}
N 170 -540 170 -580 {}
N 250 -90 250 -160 {}
N 170 -90 170 -130 {}
N 130 -340 130 -510 {}
N 250 -190 250 -340 {}
N 80 -160 130 -160 {}
N 170 -90 250 -90 {}
N 130 -340 250 -340 {}
N 170 -580 250 -580 {}
N 170 -190 250 -190 {}
C {devices/lab_pin.sym} 0 -580 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 0 -90 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} 150 -160 0 0 {name=M1 w=0.840u l=1.000u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} 150 -510 0 0 {name=M2 w=4.800u l=1.000u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1130 540 0 0 {name=l1 author="IHP PDK AUTHORS"}
