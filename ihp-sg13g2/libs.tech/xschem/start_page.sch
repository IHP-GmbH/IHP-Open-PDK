v {xschem version=3.4.5 file_version=1.2
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
L 7 2140 -730 2140 -60 {}
T {NGSPICE} 100 -350 0 0 0.6 0.6 {}
T {NGSPICE + XYCE} 380 -350 0 0 0.6 0.6 {}
T {STANDARD CELLS} 740 -350 0 0 0.6 0.6 {}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Copyright 2024 IHP PDK Authors"}
C {devices/launcher.sym} 90 -410 0 0 {name=h1
descr="IHP-Open-PDK"
url="https://github.com/IHP-GmbH/IHP-Open-PDK/tree/main"}
C {sg13g2_tests/IHP_testcases.sym} 160 -280 0 0 {name=x1}
C {sg13g2_tests_xyce/IHP_testcases.sym} 510 -280 0 0 {name=x2}
C {sg13g2_stdcells/IHP130_stdcells.sym} 870 -280 0 0 {name=x3}
