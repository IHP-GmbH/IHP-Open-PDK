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
N -450 -100 -450 -150 {}
N -450 -100 -430 -100 {}
N -450 -150 -390 -150 {}
N -390 -130 -390 -150 {}
N -390 -150 -390 -380 {}
N -370 -40 -370 -100 {}
N -390 -40 -390 -70 {}
N -310 -100 -270 -100 {}
N -470 -440 -310 -440 {}
N -370 -40 -230 -40 {}
N -390 -100 -370 -100 {}
N -390 -380 -350 -380 {}
N -310 -410 -310 -440 {}
N -290 -380 -290 -440 {}
N -310 -380 -290 -380 {}
N -310 -440 -290 -440 {}
N -310 -100 -310 -350 {}
N -390 -40 -370 -40 {}
N -230 -40 -230 -70 {}
N -210 -40 -210 -100 {}
N -230 -40 -210 -40 {}
N -230 -100 -210 -100 {}
N -230 -130 -230 -380 {}
N -230 -380 -180 -380 {}
N -290 -440 -140 -440 {}
N -140 -340 -140 -350 {}
N -140 -410 -140 -440 {}
N -470 -40 -390 -40 {}
N -140 -440 -120 -440 {}
N -140 -380 -120 -380 {}
N -140 -340 -70 -340 {}
N -120 -380 -120 -440 {}
C {devices/opin.sym} -70 -340 0 0 {name=p3 lab=L_HI}
C {devices/lab_pin.sym} -470 -440 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -470 -40 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {sg13_lv_nmos.sym} -410 -100 0 0 {name=M1 w=300n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_nmos.sym} -250 -100 0 0 {name=M2 w=795.00n l=130.00n ng=1 m=1 model=sg13_lv_nmos}
C {sg13_lv_pmos.sym} -330 -380 0 0 {name=M3 w=660.0n l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {sg13_lv_pmos.sym} -160 -380 0 0 {name=M4 w=1.155u l=130.00n ng=1 m=1 model=sg13_lv_pmos}
C {devices/title-3.sym} -1520 640 0 0 {name=l1 author="IHP PDK AUTHORS"}
