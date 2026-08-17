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
N -100 -270 -80 -270 {}
N -140 150 -140 0 {}
N 140 260 140 240 {}
N 140 0 200 0 {}
N 140 -120 140 -160 {}
N -100 -170 -100 -270 {}
N 100 120 100 -90 {}
N 140 90 140 0 {}
N 20 -90 100 -90 {}
N 160 210 160 120 {}
N 140 180 140 150 {}
N 140 -190 160 -190 {}
N 140 -90 160 -90 {}
N 140 210 160 210 {}
N -350 -270 -100 -270 {}
N -100 260 -80 260 {}
N -80 -140 -80 -270 {}
N -80 260 -80 150 {}
N -270 -190 -190 -190 {}
N -100 120 -100 0 {}
N -100 -140 -80 -140 {}
N -100 0 -100 -110 {}
N -100 150 -80 150 {}
N 140 0 140 -60 {}
N -140 0 -140 -140 {}
N -100 0 70 0 {}
N 70 210 100 210 {}
N -190 0 -140 0 {}
N -190 0 -190 -190 {}
N -190 -190 100 -190 {}
N -80 -270 140 -270 {}
N -100 260 -100 180 {}
N 140 120 160 120 {}
N 140 -220 140 -270 {}
N -350 260 -100 260 {}
N -80 260 140 260 {}
N 70 210 70 0 {}
N 140 260 160 260 {}
N 160 260 160 210 {}
N 160 -190 160 -270 {}
N 160 -90 160 -190 {}
N 140 -270 160 -270 {}
C {lab_wire.sym} -20 0 0 0 {name=l1 sig_type=std_logic lab=TE}
C {devices/ipin.sym} -270 -190 0 0 {name=p1 lab=TE_B}
C {devices/ipin.sym} 20 -90 0 0 {name=p2 lab=A}
C {devices/opin.sym} 200 0 0 0 {name=p3 lab=Z}
C {devices/lab_pin.sym} -350 -270 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -350 260 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -120 150 0 0 {name=M1 w=0.420u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 120 120 0 0 {name=M2 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 120 210 0 0 {name=M3 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -120 -140 0 0 {name=M4 w=1.535u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 120 -190 0 0 {name=M5 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 120 -90 0 0 {name=M6 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1330 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
