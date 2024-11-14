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
T {NGSPICE + XYCE} 40 -350 0 0 0.6 0.6 {}
T {STANDARD CELLS} 40 -210 0 0 0.6 0.6 {}
T {Example circuits and testbenches using NGSPICE and XYCE simulators.
Since NGSPICE and XYCE are not 100% compatible not every simulation is supported in booth.
Some are not yet implemented
} 360 -290 0 0 0.3 0.3 {}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Copyright 2024 IHP PDK Authors"}
C {devices/launcher.sym} 90 -410 0 0 {name=h1
descr="IHP-Open-PDK"
url="https://github.com/IHP-GmbH/IHP-Open-PDK/tree/main"}
C {sg13g2_stdcells/IHP130_stdcells.sym} 170 -130 0 0 {name=x3}
C {sg13g2_tests/IHP_testcases.sym} 170 -270 0 0 {name=x1}
