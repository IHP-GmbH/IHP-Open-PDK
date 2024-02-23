########################################################################
#
# Copyright 2023 IHP PDK Authors
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

pcellNmos = ly.create_cell("nmos", "IHP PyCells", { "l": 0.350e-6, "w": 6e-6, "ng": 3 })
pcellPmos = ly.create_cell("pmos", "IHP PyCells", { "l": 0.350e-6, "w": 6e-6, "ng": 3 })
pcellCmim = ly.create_cell("cmim", "IHP PyCells", { "l": "0.350e-6", "w": "6e-6"})
pcellNpn13G2Base = ly.create_cell(
        "npn13G2_base",
        "IHP PyCells",
        {
            "STI": "0.44u",
            "baspolyx": "0.3u",
            "bipwinx": "0.07u",
            "bipwiny": "0.1u",
            "empolyx": "0.15u",
            "empolyy": "0.18u",
            "le": "0.9u",
            "we": "0.07u",
            "Nx": 1,
            "Text": "npn13G2",
            "CMetY1": "0.0",
            "CMetY2": "0.0"
        })

#pcell = ly.create_cell("rsil", "IHP PyCells", { "l": "3e-6", "w": "6e-6", "b": 1, "ps": "1e-6", "R": "1e-6"})

top = ly.create_cell("TOP")
top.insert(pya.DCellInstArray(pcellNmos, pya.DTrans()))
top.insert(pya.DCellInstArray(pcellPmos, pya.DTrans(pya.DVector(3, 0))))
top.insert(pya.DCellInstArray(pcellCmim, pya.DTrans(pya.DVector(0, 3))))
top.insert(pya.DCellInstArray(pcellNpn13G2Base, pya.DTrans(pya.DVector(0, 6))))

output = "ihp-pycells.gds"
ly.write(output)

print("IHP PyCells layout written to: " + output)

