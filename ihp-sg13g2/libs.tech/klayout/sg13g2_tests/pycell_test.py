########################################################################
#
# Copyright 2024 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

# To run this code, use (Sh/Bash syntax):
#
# (in the location of this file):
# KLAYOUT_PATH=$(pwd)/.. klayout -zz -r pycell_test.py
#
# To run KLayout with the new library in place, run:
#
# KLAYOUT_PATH=$(pwd)/.. klayout ihp-pycells.gds -e

layout = pya.Layout()

pcellNmos = layout.create_cell("nmos", "SG13_dev", { "l": 0.350e-6, "w": 6e-6, "ng": 3 })
pcellPmos = layout.create_cell("pmos", "SG13_dev", { "l": 0.350e-6, "w": 6e-6, "ng": 3 })
pcellCmim = layout.create_cell("cmim", "SG13_dev", {})
pcellSealring = layout.create_cell("sealring", "SG13_dev", {})
pcellNpn13G2Base = layout.create_cell("npn13G2_base", "SG13_dev", {})
pcellNpn13G2 = layout.create_cell("npn13G2", "SG13_dev", {})
pcellNpn13G2L = layout.create_cell("npn13G2L", "SG13_dev", {})
pcellNpn13G2V = layout.create_cell("npn13G2V", "SG13_dev", {})
pcellRsil = layout.create_cell("rsil", "SG13_dev", {})
pcellRhigh = layout.create_cell("rhigh", "SG13_dev", {})
pcellRppd = layout.create_cell("rppd", "SG13_dev", {})
pcellInductor2 = layout.create_cell("inductor2", "SG13_dev", {})
pcellInductor2_sc = layout.create_cell("inductor2_sc", "SG13_dev", {})
pcellInductor2_sp = layout.create_cell("inductor2_sp", "SG13_dev", {})
pcellInductor3 = layout.create_cell("inductor3", "SG13_dev", {})
pcellInductor3_sc = layout.create_cell("inductor3_sc", "SG13_dev", {})
pcellInductor3_sp = layout.create_cell("inductor3_sp", "SG13_dev", {})
pcellDAntenna = layout.create_cell("dantenna", "SG13_dev", {})
pcellDPAntenna = layout.create_cell("dpantenna", "SG13_dev", {})

top = layout.create_cell("TOP")

top.insert(pya.DCellInstArray(pcellNmos, pya.DTrans()))
top.insert(pya.DCellInstArray(pcellPmos, pya.DTrans(pya.DVector(4, 0))))
top.insert(pya.DCellInstArray(pcellNpn13G2, pya.DTrans(pya.DVector(11, 3.1))))
top.insert(pya.DCellInstArray(pcellNpn13G2L, pya.DTrans(pya.DVector(16, -0.3))))
top.insert(pya.DCellInstArray(pcellNpn13G2V, pya.DTrans(pya.DVector(25, -0.3))))
top.insert(pya.DCellInstArray(pcellRhigh, pya.DTrans(pya.DVector(36, 0.2))))
top.insert(pya.DCellInstArray(pcellRppd, pya.DTrans(pya.DVector(38, 0.2))))
top.insert(pya.DCellInstArray(pcellRsil, pya.DTrans(pya.DVector(40, 0.2))))
top.insert(pya.DCellInstArray(pcellCmim, pya.DTrans(pya.DVector(43, 0.2))))
top.insert(pya.DCellInstArray(pcellDAntenna, pya.DTrans(pya.DVector(52, -0.3))))
top.insert(pya.DCellInstArray(pcellDPAntenna, pya.DTrans(pya.DVector(54, 0))))
top.insert(pya.DCellInstArray(pcellInductor2, pya.DTrans(pya.DVector(40, -85))))
top.insert(pya.DCellInstArray(pcellInductor2_sc, pya.DTrans(pya.DVector(125, -85))))
top.insert(pya.DCellInstArray(pcellInductor2_sp, pya.DTrans(pya.DVector(210, -85))))
top.insert(pya.DCellInstArray(pcellInductor3, pya.DTrans(pya.DVector(49, -190))))
top.insert(pya.DCellInstArray(pcellInductor3_sc, pya.DTrans(pya.DVector(152, -190))))
top.insert(pya.DCellInstArray(pcellInductor3_sp, pya.DTrans(pya.DVector(255, -190))))
top.insert(pya.DCellInstArray(pcellSealring, pya.DTrans(pya.DVector(310, -190))))

output = "SG13_dev.gds"
layout.write(output)

print("IHP PyCells layout written to: " + output)

