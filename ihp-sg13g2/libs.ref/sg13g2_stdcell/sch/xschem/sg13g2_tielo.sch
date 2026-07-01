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
N -80 220 -50 220 {}
N -140 -40 -120 -40 {}
N -80 220 -80 10 {}
N 150 300 150 250 {}
N 90 -70 90 -110 {}
N 90 -10 100 -10 {}
N -260 300 -10 300 {}
N 110 -40 110 -110 {}
N -80 -40 -60 -40 {}
N -10 190 -10 -40 {}
N -140 10 -80 10 {}
N -80 -70 -80 -110 {}
N 10 300 10 220 {}
N -10 300 -10 250 {}
N 150 90 220 90 {}
N -10 220 10 220 {}
N -10 -40 50 -40 {}
N 100 220 110 220 {}
N -80 10 -80 -10 {}
N -80 -110 -60 -110 {}
N 100 220 100 -10 {}
N -250 -110 -80 -110 {}
N 90 -40 110 -40 {}
N -60 -110 90 -110 {}
N -10 300 10 300 {}
N 150 300 170 300 {}
N 150 190 150 90 {}
N 90 -110 110 -110 {}
N 150 220 170 220 {}
N 10 300 150 300 {}
N -60 -40 -60 -110 {}
N 170 300 170 220 {}
N -140 10 -140 -40 {}
C {devices/opin.sym} 220 90 0 0 {name=p3 lab=L_LO}
C {devices/lab_pin.sym} -250 -110 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -260 300 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {sg13_lv_nmos.sym} -30 220 0 0 {name=M1 w=385.00n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_nmos.sym} 130 220 0 0 {name=M2 w=880.0n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} -100 -40 0 0 {name=M3 w=300n l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {sg13_lv_pmos.sym} 70 -40 0 0 {name=M4 w=1.045u l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -1270 980 0 0 {name=l1 author="IHP PDK AUTHORS"}
