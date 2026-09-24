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
N 110 210 130 210 {}
N 110 60 190 60 {}
N -210 60 -180 60 {}
N -70 -90 -70 -210 {}
N 110 -30 130 -30 {}
N -70 320 110 320 {}
N -90 320 -90 290 {}
N -90 260 -70 260 {}
N -90 230 -90 210 {}
N -90 -90 -70 -90 {}
N -180 60 -130 60 {}
N -180 -130 70 -130 {}
N -70 -210 110 -210 {}
N 70 130 70 -30 {}
N -90 320 -70 320 {}
N -90 -210 -70 -210 {}
N 110 100 110 60 {}
N 110 -60 110 -100 {}
N 110 60 110 0 {}
N 110 320 110 240 {}
N 110 -160 110 -210 {}
N 110 320 130 320 {}
N 130 -130 130 -210 {}
N 130 320 130 210 {}
N -340 320 -90 320 {}
N 130 -30 130 -130 {}
N 110 -210 130 -210 {}
N 110 130 130 130 {}
N -90 210 -90 -60 {}
N 110 -130 130 -130 {}
N -130 260 -130 60 {}
N -130 60 -130 -90 {}
N 40 -30 70 -30 {}
N 130 210 130 130 {}
N -90 -120 -90 -210 {}
N -90 210 70 210 {}
N -180 60 -180 -130 {}
N 110 180 110 160 {}
N -340 -210 -90 -210 {}
N -70 320 -70 260 {}
C {lab_wire.sym} -10 210 0 0 {name=l1 sig_type=std_logic lab=TE}
C {devices/ipin.sym} -210 60 0 0 {name=p1 lab=TE_B}
C {devices/ipin.sym} 40 -30 0 0 {name=p2 lab=A}
C {devices/opin.sym} 190 60 0 0 {name=p3 lab=Z}
C {devices/lab_pin.sym} -340 -210 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -340 320 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -110 260 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 90 130 0 0 {name=M2 w=5.920u l=0.450u ng=8 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 90 210 0 0 {name=M3 w=5.920u l=0.450u ng=8 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -110 -90 0 0 {name=M4 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 90 -130 0 0 {name=M5 w=21.520u l=0.450u ng=8 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 90 -30 0 0 {name=M6 w=21.520u l=0.450u ng=8 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1330 940 0 0 {name=l1 author="IHP PDK AUTHORS"}
