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

ly = pya.Layout()

pcellNmos = ly.create_cell("nmos", "SG13_dev", { "l": 0.350e-6, "w": 6e-6, "ng": 3 })
pcellPmos = ly.create_cell("pmos", "SG13_dev", { "l": 0.350e-6, "w": 6e-6, "ng": 3 })
pcellCmim = ly.create_cell("cmim", "SG13_dev", {})
pcellSealring = ly.create_cell("sealring", "SG13_dev", {})
#pcellNpn13G2Base = ly.create_cell("npn13G2_base", "SG13_dev", {})
#pcellNpn13G2 = ly.create_cell("npn13G2", "SG13_dev", {})

#pcell = ly.create_cell("rsil", "SG13_dev", { "l": "3e-6", "w": "6e-6", "b": 1, "ps": "1e-6", "R": "1e-6"})

top = ly.create_cell("TOP")
top.insert(pya.DCellInstArray(pcellNmos, pya.DTrans()))
top.insert(pya.DCellInstArray(pcellPmos, pya.DTrans(pya.DVector(3, 0))))
top.insert(pya.DCellInstArray(pcellCmim, pya.DTrans(pya.DVector(0, -9))))
top.insert(pya.DCellInstArray(pcellSealring, pya.DTrans(pya.DVector(50, -9))))
#top.insert(pya.DCellInstArray(pcellNpn13G2Base, pya.DTrans(pya.DVector(10, 0))))
#top.insert(pya.DCellInstArray(pcellNpn13G2, pya.DTrans(pya.DVector(3, 6))))

output = "SG13_dev.gds"
ly.write(output)

print("IHP PyCells layout written to: " + output)

