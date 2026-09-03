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
N -80 140 -80 80 {}
N 160 50 160 -150 {}
N 200 20 200 -150 {}
N -120 -150 -120 -350 {}
N 200 140 200 80 {}
N -10 140 200 140 {}
N -350 140 -80 140 {}
N 200 50 270 50 {}
N -80 -420 -10 -420 {}
N -80 -150 -80 -320 {}
N -80 -380 -80 -420 {}
N -80 50 -10 50 {}
N -10 140 -10 50 {}
N -80 -350 -10 -350 {}
N 270 140 270 50 {}
N -350 -420 -80 -420 {}
N -80 20 -80 -150 {}
N 200 140 270 140 {}
N 160 -150 160 -350 {}
N -80 -150 160 -150 {}
N 200 -150 200 -320 {}
N -120 50 -120 -150 {}
N 200 -150 240 -150 {}
N -190 -150 -120 -150 {}
N -80 140 -10 140 {}
N 270 -350 270 -420 {}
N 200 -380 200 -420 {}
N 200 -420 270 -420 {}
N -10 -420 200 -420 {}
N -10 -350 -10 -420 {}
N 200 -350 270 -350 {}
C {devices/ipin.sym} -190 -150 0 0 {name=p1 lab=A}
C {devices/opin.sym} 240 -150 0 0 {name=p2 lab=X}
C {devices/lab_pin.sym} -350 -420 0 0 {name=p3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -350 140 0 0 {name=p4 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -100 50 0 0 {name=M1 w=4.440u l=0.450u ng=6 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 180 50 0 0 {name=M2 w=11.840u l=0.450u ng=16 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -100 -350 0 0 {name=M3 w=16.140u l=0.450u ng=6 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 180 -350 0 0 {name=M4 w=43.040u l=0.450u ng=16 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1290 740 0 0 {name=l1 author="IHP PDK AUTHORS"}
