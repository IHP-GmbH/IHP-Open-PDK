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
pcellNpn13G2 = layout.create_cell("npn13G2", "SG13_dev", {})
pcellNpn13G2L = layout.create_cell("npn13G2L", "SG13_dev", {})
pcellNpn13G2V = layout.create_cell("npn13G2V", "SG13_dev", {})
pcellRsil = layout.create_cell("rsil", "SG13_dev", {})
pcellRhigh = layout.create_cell("rhigh", "SG13_dev", {})
pcellRppd = layout.create_cell("rppd", "SG13_dev", {})
pcellInductor2 = layout.create_cell("inductor2", "SG13_dev", {})
pcellInductor3 = layout.create_cell("inductor3", "SG13_dev", {})
pcellDAntenna = layout.create_cell("dantenna", "SG13_dev", {})
pcellDPAntenna = layout.create_cell("dpantenna", "SG13_dev", {})

pcellViaStack = layout.create_cell("via_stack", "SG13_dev", {})
pcellPtap1 = layout.create_cell("ptap1", "SG13_dev", {})
pcellNtap1 = layout.create_cell("ntap1", "SG13_dev", {})
pcellBondpad = layout.create_cell("bondpad", "SG13_dev", {})
pcellRfcmim = layout.create_cell("rfcmim", "SG13_dev", {})
pcellRfnmos = layout.create_cell("rfnmos", "SG13_dev", {})
pcellRfnmosHV = layout.create_cell("rfnmosHV", "SG13_dev", {})
pcellRfpmos = layout.create_cell("rfpmos", "SG13_dev", {})
pcellRfpmosHV = layout.create_cell("rfpmosHV", "SG13_dev", {})
pcellNoFillerStack = layout.create_cell("NoFillerStack", "SG13_dev", {})
pcellSVaricap = layout.create_cell("SVaricap", "SG13_dev", {})

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
top.insert(pya.DCellInstArray(pcellViaStack, pya.DTrans(pya.DVector(56, 0))))
top.insert(pya.DCellInstArray(pcellPtap1, pya.DTrans(pya.DVector(58, 0))))
top.insert(pya.DCellInstArray(pcellNtap1, pya.DTrans(pya.DVector(60, 0))))
top.insert(pya.DCellInstArray(pcellRfcmim, pya.DTrans(pya.DVector(68, 5))))
top.insert(pya.DCellInstArray(pcellRfnmos, pya.DTrans(pya.DVector(82, 0))))
top.insert(pya.DCellInstArray(pcellRfnmosHV, pya.DTrans(pya.DVector(86, 0))))
top.insert(pya.DCellInstArray(pcellRfpmos, pya.DTrans(pya.DVector(91, 0))))
top.insert(pya.DCellInstArray(pcellRfpmosHV, pya.DTrans(pya.DVector(96, 0))))
top.insert(pya.DCellInstArray(pcellSVaricap, pya.DTrans(pya.DVector(102, 0))))
top.insert(pya.DCellInstArray(pcellNoFillerStack, pya.DTrans(pya.DVector(106, 0))))
top.insert(pya.DCellInstArray(pcellInductor2, pya.DTrans(pya.DVector(40, -85))))
top.insert(pya.DCellInstArray(pcellInductor3, pya.DTrans(pya.DVector(49, -190))))
top.insert(pya.DCellInstArray(pcellSealring, pya.DTrans(pya.DVector(160, -190))))
top.insert(pya.DCellInstArray(pcellBondpad, pya.DTrans(pya.DVector(40, 60))))

output = "SG13_dev.gds"
layout.write(output)

print("IHP PyCells layout written to: " + output)

