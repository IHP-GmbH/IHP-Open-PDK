
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
#pcellCmim = ly.create_cell("cmim", "IHP PyCells", { "l": "0.350e-6", "w": "6e-6"})
#pcell = ly.create_cell("rsil", "IHP PyCells", { "l": "3e-6", "w": "6e-6", "b": 1, "ps": "1e-6", "R": "1e-6"})

top = ly.create_cell("TOP")
top.insert(pya.DCellInstArray(pcellNmos, pya.DTrans()))
#top.insert(pya.DCellInstArray(pcellCmim, pya.DTrans()))

output = "ihp-pycells.gds"
ly.write(output)

print("IHP PyCells layout written to: " + output)

