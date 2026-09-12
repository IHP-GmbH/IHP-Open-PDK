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
N -90 -340 40 -340 {}
N -210 -250 -150 -250 {}
N -110 -180 -110 -220 {}
N -270 -150 -240 -150 {}
N 40 -100 120 -100 {}
N -110 -100 -110 -120 {}
N -110 -100 -40 -100 {}
N 40 -100 40 -170 {}
N 40 -200 60 -200 {}
N -340 -340 -110 -340 {}
N -270 -200 -180 -200 {}
N -40 -100 40 -100 {}
N -40 -70 -40 -100 {}
N -180 -40 -80 -40 {}
N -180 -200 0 -200 {}
N -180 -40 -180 -200 {}
N -260 -250 -210 -250 {}
N -210 60 -210 -250 {}
N -210 60 0 60 {}
N -240 110 -150 110 {}
N -240 -150 -150 -150 {}
N -240 110 -240 -150 {}
N 40 30 40 20 {}
N -40 20 40 20 {}
N -40 20 -40 -10 {}
N -110 80 -110 20 {}
N -110 20 -40 20 {}
N -90 200 -90 110 {}
N -110 200 -90 200 {}
N -360 200 -110 200 {}
N 60 200 60 60 {}
N 40 -340 60 -340 {}
N 40 -230 40 -340 {}
N 60 -200 60 -340 {}
N -110 -250 -90 -250 {}
N -110 -280 -110 -340 {}
N -110 -340 -90 -340 {}
N -90 -250 -90 -340 {}
N -110 -150 -90 -150 {}
N -90 -150 -90 -250 {}
N -110 110 -90 110 {}
N -110 200 -110 140 {}
N -90 200 40 200 {}
N 40 60 60 60 {}
N 40 200 40 90 {}
N 40 200 60 200 {}
N 60 60 60 -40 {}
N -40 -40 60 -40 {}
C {devices/ipin.sym} -260 -250 0 0 {name=p1 lab=A1}
C {devices/ipin.sym} -270 -150 0 0 {name=p2 lab=A2}
C {devices/ipin.sym} -270 -200 0 0 {name=p3 lab=B1}
C {devices/opin.sym} 120 -100 0 0 {name=p4 lab=Y}
C {devices/lab_pin.sym} -340 -340 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -360 200 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -130 110 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -60 -40 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 20 60 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -130 -250 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -130 -150 0 0 {name=M5 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 20 -200 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1370 820 0 0 {name=l1 author="IHP PDK AUTHORS"}
