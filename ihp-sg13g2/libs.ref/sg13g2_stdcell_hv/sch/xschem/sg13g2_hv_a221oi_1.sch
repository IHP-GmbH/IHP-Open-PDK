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
N 330 -140 330 -210 {}
N -120 120 -120 80 {}
N -120 -170 -120 -210 {}
N 270 -170 270 -210 {}
N -120 -140 -50 -140 {}
N 270 20 270 -60 {}
N 70 120 270 120 {}
N 320 620 320 470 {}
N 270 50 330 50 {}
N 270 -210 330 -210 {}
N 270 -60 270 -110 {}
N 270 -140 330 -140 {}
N -190 -140 -160 -140 {}
N -340 -210 -120 -210 {}
N -120 120 70 120 {}
N 270 120 270 80 {}
N 210 -140 230 -140 {}
N 330 50 330 -140 {}
N -120 20 -120 -60 {}
N 130 210 130 -210 {}
N -50 50 -50 -140 {}
N 70 300 70 240 {}
N 70 180 70 120 {}
N -120 -60 270 -60 {}
N -50 -210 130 -210 {}
N -120 -210 -50 -210 {}
N -50 -140 -50 -210 {}
N -120 50 -50 50 {}
N 70 210 130 210 {}
N -120 400 -120 300 {}
N 130 -210 270 -210 {}
N -120 300 70 300 {}
N 280 440 280 300 {}
N -340 620 -120 620 {}
N 80 300 280 300 {}
N -190 50 -160 50 {}
N -120 620 -40 620 {}
N 70 300 80 300 {}
N -120 520 -120 460 {}
N 80 520 80 460 {}
N 80 550 160 550 {}
N 160 620 160 550 {}
N 280 620 320 620 {}
N -120 620 -120 580 {}
N 80 620 80 580 {}
N 80 400 80 300 {}
N 280 470 320 470 {}
N 160 550 160 430 {}
N 80 620 160 620 {}
N 280 300 360 300 {}
N -190 430 -160 430 {}
N -190 550 -160 550 {}
N 20 430 40 430 {}
N 20 550 40 550 {}
N 230 470 240 470 {}
N -120 -60 -120 -110 {}
N 210 50 230 50 {}
N -40 550 -40 430 {}
N 280 620 280 500 {}
N -40 620 -40 550 {}
N -120 550 -40 550 {}
N 80 430 160 430 {}
N 160 620 280 620 {}
N -40 620 80 620 {}
N -120 430 -40 430 {}
N -30 210 30 210 {}
C {lab_wire.sym} -180 430 0 0 {name=l1 sig_type=std_logic lab=A1}
C {lab_wire.sym} -180 550 0 0 {name=l2 sig_type=std_logic lab=A2}
C {lab_wire.sym} 30 430 0 0 {name=l3 sig_type=std_logic lab=B1}
C {lab_wire.sym} 30 550 0 0 {name=l4 sig_type=std_logic lab=B2}
C {lab_wire.sym} 240 470 0 0 {name=l5 sig_type=std_logic lab=C1}
C {devices/ipin.sym} -190 -140 0 0 {name=p1 lab=A1}
C {devices/ipin.sym} 210 -140 0 0 {name=p2 lab=A2}
C {devices/ipin.sym} -190 50 0 0 {name=p3 lab=B1}
C {devices/opin.sym} 360 300 0 0 {name=p4 lab=Y}
C {devices/ipin.sym} 210 50 0 0 {name=p5 lab=B2}
C {devices/ipin.sym} -30 210 0 0 {name=p6 lab=C1}
C {devices/lab_pin.sym} -340 -210 0 0 {name=p7 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -340 620 0 0 {name=p8 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -140 430 0 0 {name=M1 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -140 550 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 60 430 0 0 {name=M3 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 60 550 0 0 {name=M4 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 260 470 0 0 {name=M5 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -140 -140 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -140 50 0 0 {name=M7 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 50 210 0 0 {name=M8 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 250 -140 0 0 {name=M9 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 250 50 0 0 {name=M10 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1240 1080 0 0 {name=l1 author="IHP PDK AUTHORS"}
