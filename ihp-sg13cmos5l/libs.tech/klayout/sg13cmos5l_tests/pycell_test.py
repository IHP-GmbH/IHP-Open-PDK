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

# PCell test script for IHP SG13CMOS5L Slim PDK
#
# To run this code, use (Sh/Bash syntax):
#
# (in the location of this file):
# KLAYOUT_PATH=$(pwd)/.. klayout -zz -r pycell_test.py
#
# To run KLayout with the new library in place, run:
#
# KLAYOUT_PATH=$(pwd)/.. klayout ihp-pycells.gds -e

layout = pya.Layout()

# Basic MOSFET devices
pcellNmos = layout.create_cell("nmos", "SG13_dev", { "l": 0.350e-6, "w": 6e-6, "ng": 3 })
pcellPmos = layout.create_cell("pmos", "SG13_dev", { "l": 0.350e-6, "w": 6e-6, "ng": 3 })

# Resistors (CMOS-compatible, M1-only)
pcellRsil = layout.create_cell("rsil", "SG13_dev", {})
pcellRhigh = layout.create_cell("rhigh", "SG13_dev", {})
pcellRppd = layout.create_cell("rppd", "SG13_dev", {})

# Varicap (CMOS-compatible)
pcellSVaricap = layout.create_cell("SVaricap", "SG13_dev", {})

# Via stack (M1-M5 only)
pcellViaStack = layout.create_cell("via_stack", "SG13_dev", {})

# Substrate taps
pcellPtap1 = layout.create_cell("ptap1", "SG13_dev", {})
pcellNtap1 = layout.create_cell("ntap1", "SG13_dev", {})

# Bondpad (Metal5 top)
pcellBondpad = layout.create_cell("bondpad", "SG13_dev", {})

# Sealring (M1-M5 only)
pcellSealring = layout.create_cell("sealring", "SG13_dev", {})

# Create top cell and place instances
top = layout.create_cell("TOP")

# Row 1: Basic devices
top.insert(pya.DCellInstArray(pcellNmos, pya.DTrans()))
top.insert(pya.DCellInstArray(pcellPmos, pya.DTrans(pya.DVector(4, 0))))

# Row 2: Resistors
top.insert(pya.DCellInstArray(pcellRhigh, pya.DTrans(pya.DVector(0, 10))))
top.insert(pya.DCellInstArray(pcellRppd, pya.DTrans(pya.DVector(3, 10))))
top.insert(pya.DCellInstArray(pcellRsil, pya.DTrans(pya.DVector(6, 10))))

# Row 3: Via stack and taps
top.insert(pya.DCellInstArray(pcellViaStack, pya.DTrans(pya.DVector(0, 20))))
top.insert(pya.DCellInstArray(pcellPtap1, pya.DTrans(pya.DVector(4, 20))))
top.insert(pya.DCellInstArray(pcellNtap1, pya.DTrans(pya.DVector(8, 20))))

# Row 4: Varicap
top.insert(pya.DCellInstArray(pcellSVaricap, pya.DTrans(pya.DVector(0, 30))))

# Large structures
top.insert(pya.DCellInstArray(pcellBondpad, pya.DTrans(pya.DVector(40, 0))))
top.insert(pya.DCellInstArray(pcellSealring, pya.DTrans(pya.DVector(100, -100))))

output = "SG13CMOS5L_dev.gds"
layout.write(output)

print("IHP SG13CMOS5L PyCells layout written to: " + output)
