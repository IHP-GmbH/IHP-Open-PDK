"""Module to automatically apply filler cells to a GDS file and store the result to a
parametrizable output file. This module is required because .lym files cannot alter and save
a GDS file in batch mode.

Can be used in Klayout's batch mode. For example:

klayout -n sg13g2 -zz -r filler.py \
        -rd output_file=filled-design.gds.gz \
        input-file.gds.gz

This script has optional arguments to disable fill for some areas:

* no_activ - Disable Activ and GatPoly fill
* no_metal - Disable Metal1 to Metal 5 fill
* no_topmetal - Disable TopMetal1 and TopMetal2 fill

These arguments don't take a value. See the following example.

klayout -n sg13g2 -zz -r filler.py \
        -rd output_file=filled-design.gds.gz \
        -rd no_activ \
        -rd no_metal \
        input-file.gds.gz
"""
# pylint: disable=import-error

import pathlib
import os
import sys
import pya

LIB = 'SG13_dev'

try:
    output_file
except NameError:
    print("Missing output_file argument. Please define '-rd output_file=<path-to-output-file>'")
    sys.exit(1)

NO_ACTIV = 'no_activ' in globals()
NO_METAL = 'no_metal' in globals()
NO_TOPMETAL = 'no_topmetal' in globals()

scripts = [(NO_ACTIV, 'ActGatP'), (NO_METAL, 'Metal'), (NO_TOPMETAL, 'TopMetal')]

for disabled, area in scripts:
    if disabled:
        print(f"Skip {area} fill because disabled by argument")
    else:
        print(f"Start filling {area}")
        path = pathlib.Path(os.environ['PDK_ROOT']) / pathlib.Path(os.environ['PDK']) / f"libs.tech/klayout/tech/macros/sg13g2_filler_{area}.lym"
        pya.Macro(path).run()

layout=pya.CellView.active().layout()
layout.write(output_file) # pylint: disable=undefined-variable
