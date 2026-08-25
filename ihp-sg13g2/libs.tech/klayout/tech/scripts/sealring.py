# =========================================================================================
# Copyright 2024 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================================

"""Module to automatically generate a sealring and create a new GDS file. Can be used in
Klayout's batch mode. For example:

klayout -n sg13g2 -zz -r sealring.py \
        -rd width=1300.0 -rd length=1300.0 -rd output=macros/sealring.gds.gz

"""
# pylint: disable=import-error
import pathlib
import sys
import re
import pya
import klayout.db

LIB = 'SG13_dev'
PCELL = 'sealring'

def generate_sealring(length: float, width: float, input_file: str | None, output: str,
                      offset_x: float, offset_y: float):
    """Function to create a new layout, add the sealring PCell to sealring_top
    and save it somewhere on the filesystem.

    :param length: Length (X-Axis) of the sealring.
    :type length: float
    :param width: Width (Y-Axis) of the sealring.
    :type width: float
    :param input_file: Path and name of an existing layout the sealring should be added to.
                       If omitted, a new layout with a 'sealring_top' cell is created.
    :type input_file: str | None
    :param output: Path and name of the file where the sealring should be written to.
    :type output: str
    :param offset_x: Translation in X direction in µm.
    :type offset_x: float
    :param offset_y: Translation in Y direction in µm.
    :type offset_y: float

    """
    layout = klayout.db.Layout(True)
    layout.dbu = 0.001

    if input_file:
        layout.read(input_file)

    lib = pya.Library.library_by_name(LIB, 'sg13g2')
    if lib is None:
        raise RuntimeError(
            "Could not find the 'SG13_dev' PCell library in the current KLayout environment.\n"
            "Please make sure the SG13G2 PDK is properly installed and configured in KLayout.\n"
            "This may involve:\n"
            "- Cloning the IHP-Open-PDK repository with all submodules (use --recursive)\n"
            "- Ensuring the SG13G2 technology is registered in KLayout (e.g. using -n sg13g2)\n"
            "- Running KLayout with a version that supports Python PCells and properly loads them\n"
            "- Verifying that 'SG13_dev' appears in the Library Browser under PCells"
        )

    pcell_decl = lib.layout().pcell_declaration(PCELL)

    # Remove space around the sealring from width/length arguments.
    params = pcell_decl.params_as_hash(pcell_decl.get_parameters())
    edge_box = float(re.sub('[a-zA-Z]+', '', params['edgeBox'].default))
    width = float(width) - edge_box * 2
    length = float(length) - edge_box * 2

    if input_file:
        top_cell = layout.top_cell()
    else:
        top_cell = layout.cell(layout.add_cell("sealring_top"))

    pcell = layout.add_pcell_variant(lib, pcell_decl.id(), {'w': f'{width}u', 'l': f'{length}u'})
    layout.cell(pcell)

    # Convert offset from µm to dbu
    dx = int(float(offset_x) * 1000)
    dy = int(float(offset_y) * 1000)

    # Insert the cell with translation
    top_cell.insert(klayout.db.CellInstArray(
        pcell,
        klayout.db.Trans(klayout.db.Vector(dx, dy))
    ))

    # Create directory where the sealring should be written to.
    pathlib.Path(output).parent.mkdir(parents=True, exist_ok=True)

    # Don't save PCell information in the "$$$CONTEXT_INFO$$$" cell
    # as this could cause issues further downstream
    options = pya.SaveLayoutOptions()
    options.write_context_info = False

    layout.write(output, options)

try:
    width
except NameError:
    print("Missing width argument. Please define '-rd width=<width>'")
    sys.exit(1)

try:
    length
except NameError:
    print("Missing length argument. Please define '-rd length=<length>'")
    sys.exit(1)

try:
    output
except NameError:
    print("Missing output argument. Please define '-rd output=<path-to-sealring>'")
    sys.exit(1)

try:
    offset_x
except NameError:
    offset_x = 0.0

try:
    offset_y
except NameError:
    offset_y = 0.0

# The optional '-rd input=<path-to-layout>' argument shadows the built-in input
# function, so copy it into a dedicated variable and don't use it any further.
input_file = None if callable(input) else input

generate_sealring(length=length, width=width, input_file=input_file, output=output,
                  offset_x=offset_x, offset_y=offset_y)  # pylint: disable=undefined-variable
