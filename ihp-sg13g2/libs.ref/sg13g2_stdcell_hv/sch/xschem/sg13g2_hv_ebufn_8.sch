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
N -260 200 -260 10 {}
N -330 -30 -330 -210 {}
N -260 -190 -260 -290 {}
N 70 -240 70 -290 {}
N -120 -30 -120 -160 {}
N 70 -30 130 -30 {}
N -300 50 -300 -160 {}
N -60 -160 -60 -290 {}
N -330 -210 30 -210 {}
N -120 230 -120 -30 {}
N 70 290 70 200 {}
N -240 -290 -80 -290 {}
N 30 70 30 10 {}
N -80 290 -80 260 {}
N -240 -160 -240 -290 {}
N -60 290 -60 230 {}
N -60 -290 70 -290 {}
N 70 70 90 70 {}
N -240 290 -80 290 {}
N 70 -30 70 -80 {}
N -350 -30 -330 -30 {}
N -330 -30 -120 -30 {}
N -300 230 -300 50 {}
N -80 -290 -60 -290 {}
N -260 290 -240 290 {}
N -350 50 -300 50 {}
N 70 -140 70 -180 {}
N -390 -290 -260 -290 {}
N -80 -190 -80 -290 {}
N -260 230 -240 230 {}
N -80 230 -60 230 {}
N -80 200 -80 170 {}
N -80 290 -60 290 {}
N -80 170 -80 -130 {}
N 30 10 30 -110 {}
N -240 290 -240 230 {}
N -80 -160 -60 -160 {}
N 70 290 90 290 {}
N -260 -160 -240 -160 {}
N 70 170 90 170 {}
N 70 40 70 -30 {}
N -60 290 70 290 {}
N 90 170 90 70 {}
N -260 10 -260 -130 {}
N -260 10 30 10 {}
N 90 290 90 170 {}
N -80 170 30 170 {}
N 70 140 70 100 {}
N 70 -110 90 -110 {}
N 70 -290 90 -290 {}
N 90 -210 90 -290 {}
N 90 -110 90 -210 {}
N 70 -210 90 -210 {}
N -260 290 -260 260 {}
N -400 290 -260 290 {}
N -260 -290 -240 -290 {}
C {devices/ipin.sym} -350 50 0 0 {name=p1 lab=A}
C {devices/ipin.sym} -350 -30 0 0 {name=p2 lab=TE_B}
C {devices/opin.sym} 130 -30 0 0 {name=p3 lab=Z}
C {devices/lab_pin.sym} -390 -290 0 0 {name=p4 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -400 290 0 0 {name=p5 sig_type=std_logic lab=VSS}
C {sg13_hv_nmos.sym} -280 230 0 0 {name=M1 w=1.480u l=0.450u ng=2 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} -100 230 0 0 {name=M2 w=0.740u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 50 70 0 0 {name=M3 w=5.920u l=0.450u ng=8 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 50 170 0 0 {name=M4 w=5.920u l=0.450u ng=8 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -280 -160 0 0 {name=M5 w=5.380u l=0.450u ng=2 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} -100 -160 0 0 {name=M6 w=2.690u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 50 -210 0 0 {name=M7 w=21.520u l=0.450u ng=8 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 50 -110 0 0 {name=M8 w=21.520u l=0.450u ng=8 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1390 880 0 0 {name=l1 author="IHP PDK AUTHORS"}
