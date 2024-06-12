"""Module to automatically generate a sealring and create a new GDS file. Can be used in
Klayout's batch mode. For example:

klayout -n sg13g2 -zz -r sealring.py \
        -rd width=1300.0 -rd height=1300.0 -rd output=macros/sealring.gds.gz

"""
# pylint: disable=import-error
import pathlib
import sys
import re
import pya
import klayout.db

LIB = 'SG13_dev'
PCELL = 'sealring'

def generate_sealring(width: float, heigth: float, output: str):
    """Function to create a new layout, add the sealring PCell to sealring_top
    and save it somewhere on the filesystem.

    :param width: Width (X-Axis) of the sealring.
    :type width: float
    :param height: Heigth (Y-Axis) of the sealring.
    :type heigth: float
    :param output: Path and name of the file where the sealring should be written to.
    :type output: str

    """
    layout = klayout.db.Layout(True)
    layout.dbu = 0.001

    lib = pya.Library.library_by_name(LIB)
    pcell_decl = lib.layout().pcell_declaration(PCELL)

    # Remove space around the sealring from width/height arguments.
    params = pcell_decl.params_as_hash(pcell_decl.get_parameters())
    edge_box = float(re.sub('[a-zA-Z]+', '', params['edgeBox'].default))
    width = float(width) - edge_box * 2
    heigth = float(heigth) - edge_box * 2

    top_cell = layout.cell(layout.add_cell("sealring_top"))
    pcell = layout.add_pcell_variant(lib, pcell_decl.id(), {'w': f'{width}u', 'l': f'{heigth}u'})
    layout.cell(pcell)
    top_cell.insert(klayout.db.CellInstArray(pcell, klayout.db.Trans()))

    # Create directory where the sealring should be written to.
    pathlib.Path(output).parent.mkdir(parents=True, exist_ok=True)

    layout.write(output)

try:
    width
except NameError:
    print("Missing width argument. Please define '-rd width=<width>'")
    sys.exit(1)

try:
    height
except NameError:
    print("Missing height argument. Please define '-rd height=<height>'")
    sys.exit(1)

try:
    output
except NameError:
    print("Missing output argument. Please define '-rd output=<path-to-sealring>'")
    sys.exit(1)

generate_sealring(width, height, output) # pylint: disable=undefined-variable
