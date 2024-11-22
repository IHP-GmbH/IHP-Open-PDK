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

def get_resized_layer(layout, cell, layer_number, layer_datatype, offset):
    layer = layout.layer(layer_number, layer_datatype)
    return pya.Region(cell.begin_shapes_rec(layer).dup()).size(offset, offset)

def fill_topmetal(layout, cell, width, height, distance, tile_size=800.0):
    TM1Fil_c = get_resized_layer(layout, cell, 126, 0, 3.0)
    TM1Fil_d = get_resized_layer(layout, cell, 26, 0, 4.9)

    chip = pya.DBox(0, 0, 1050, 1050)

    fill_box = pya.DBox(0, 0, width / layout.dbu, height / layout.dbu)
    fill_cell = layout.create_cell("TM1_FILL_CELL").shapes(layout.layer(126,
        22)).insert(fill_box)

    class TilingOperator(pya.TileOutputReceiver):
        def __init__(self, layout, top_cell, *args):
            self.layout = layout
            self.top_cell = top_cell
            self.args =  args
            print("hi")

        def put(self, ix, iy, tile, obj, dbu, clip):
            print("ho")
            print(tile)
            print(obj)
            print(*self.args)
            self.top_cell.fill_region(obj, *self.args)
            print("done")

    tp = pya.TilingProcessor()
    tp.frame = chip
    tp.dbu = layout.dbu
    tp.ncpus = 16
    tp.tile_size(tile_size, tile_size)
    tp.input("tm1fil_c", TM1Fil_c)
    tp.input("tm1fil_d", TM1Fil_d)
    tp.input("tm1_filler", layout, cell.cell_index(), layout.layer(126, 22))
    tp.input("tm1_nofill", layout, cell.cell_index(), layout.layer(126, 23))
    tp.input("tm1_slit", layout, cell.cell_index(), layout.layer(126, 24))
    tp.input("trans", layout, cell.cell_index(), layout.layer(26, 0))
    tp.input("tm1_pattern", fill_cell.cell.begin_shapes_rec(layout.layer(126, 22)))
    tp.var("dist", distance / layout.dbu)
    tp.output("to_fill",
            TilingOperator(
                layout,
                cell,
                fill_cell.cell.cell_index(),
                fill_box,
                None))
    tp.queue("""
var exclude = tm1fil_c + tm1fil_d + tm1_filler + tm1_nofill + tm1_slit + trans;
var fill_region = _tile & _frame - exclude.sized(dist);
_output(to_fill, fill_region)""")
    tp.execute("TopMetal1 fill")


layout = pya.CellView.active().layout()
top_cell = layout.top_cell()

layout.start_changes()
fill_topmetal(layout, top_cell, 5.0, 10.0, 3.0)
layout.end_changes()

layout.write(output_file) # pylint: disable=undefined-variable
