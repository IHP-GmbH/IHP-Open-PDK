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
N -70 -100 20 -100 {}
N -110 -320 20 -320 {}
N -140 -50 -110 -50 {}
N 20 170 20 130 {}
N -130 -250 -130 -320 {}
N -130 170 -110 170 {}
N 20 -250 40 -250 {}
N -130 170 -130 100 {}
N 40 170 40 100 {}
N -110 -50 -110 -60 {}
N -130 -320 -110 -320 {}
N -130 100 -110 100 {}
N -210 -320 -130 -320 {}
N -110 -280 -110 -320 {}
N -20 -60 -20 -250 {}
N -130 -250 -110 -250 {}
N -210 170 -130 170 {}
N 20 -280 20 -320 {}
N -110 70 -110 -50 {}
N -110 170 20 170 {}
N 20 170 40 170 {}
N -70 100 -70 -100 {}
N -20 100 -20 -60 {}
N -110 170 -110 130 {}
N -110 -60 -20 -60 {}
N 20 -100 20 -220 {}
N 20 -320 40 -320 {}
N -70 -100 -70 -250 {}
N 20 100 40 100 {}
N 40 -250 40 -320 {}
N -110 -60 -110 -220 {}
N 20 70 20 -100 {}
C {devices/lab_pin.sym} -210 -320 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -210 170 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {devices/iopin.sym} -140 -50 2 0 {name=p3 lab=SH}
C {sg13_hv_nmos.sym} -90 100 0 1 {name=M1 w=0.300u l=0.700u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_nmos.sym} 0 100 0 0 {name=M2 w=0.300u l=0.450u ng=1 m=1 model=sg13_hv_nmos}
C {sg13_hv_pmos.sym} -90 -250 0 1 {name=M3 w=0.720u l=0.700u ng=1 m=1 model=sg13_hv_pmos}
C {sg13_hv_pmos.sym} 0 -250 0 0 {name=M4 w=1.080u l=0.450u ng=1 m=1 model=sg13_hv_pmos}
C {devices/title-3.sym} -1330 800 0 0 {name=l1 author="IHP PDK AUTHORS"}
