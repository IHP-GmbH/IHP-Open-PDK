"""Module to automatically generate a bondpad and create a new GDS file. Can be used in
Klayout's batch mode. For example:

klayout -n sg13g2 -zz -r bondpad.py \
        -rd diameter=70.0 -rd shape=square -rd output=macros/bondpad_70x70.gds.gz

"""
# pylint: disable=import-error
import pathlib
import sys
import pya
import klayout.db

LIB = 'SG13_dev'
PCELL = 'bondpad'

def generate_bondpad(diameter: float, shape: str, output: str):
    """Function to create a new layout, add the bondpad PCell to a top cell called
    similar to the filename and save it somewhere on the filesystem.

    :param width: Diameter of the bondpad.
    :type width: float
    :param height: Shape of the bondpad.
    :type heigth: str
    :param output: Path and name of the file where the bondpad should be written to.
    :type output: str

    """
    layout = klayout.db.Layout(True)
    layout.dbu = 0.001

    lib = pya.Library.library_by_name(LIB)
    pcell_decl = lib.layout().pcell_declaration(PCELL)

    cell_name = pathlib.Path(output).resolve().name.split('.')[0]
    top_cell = layout.cell(layout.add_cell(cell_name))
    pcell = layout.add_pcell_variant(lib, pcell_decl.id(),
        {'diameter': f'{diameter}u', 'shape': shape})
    layout.cell(pcell)
    top_cell.insert(klayout.db.CellInstArray(pcell, klayout.db.Trans()))

    # Create directory where the bondpad should be written to.
    pathlib.Path(output).parent.mkdir(parents=True, exist_ok=True)

    layout.write(output)

try:
    diameter
except NameError:
    print("Missing width argument. Please define '-rd diameter=<diameter>'")
    sys.exit(1)

try:
    shape
except NameError:
    shape = 'octagon' # pylint: disable=invalid-name

allowed_shapes = ('octagon', 'square', 'circle')
if shape not in allowed_shapes:
    print(f"Illegal bondpad shape. Allowed are {','.join(allowed_shapes)}")
    sys.exit(1)

try:
    output
except NameError:
    print("Missing output argument. Please define '-rd output=<path-to-bondpad>'")
    sys.exit(1)

generate_bondpad(diameter, shape, output) # pylint: disable=undefined-variable
