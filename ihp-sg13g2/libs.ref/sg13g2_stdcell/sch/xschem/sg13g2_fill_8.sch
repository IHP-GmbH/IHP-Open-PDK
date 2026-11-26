v {xschem version=3.4.8RC file_version=1.3
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
F {}
E {}
N 750 -660 920 -660 {lab=VSS}
N 750 -890 920 -890 {lab=VDD}
C {devices/lab_pin.sym} 750 -890 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 750 -660 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {devices/title-3.sym} -410 100 0 0 {name=l1 author="IHP PDK AUTHORS"}
C {noconn.sym} 920 -660 0 1 {name=l2}
C {noconn.sym} 920 -890 0 1 {name=l3}
