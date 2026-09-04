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

"""Module to automatically generate a bondpad and create GDS and LEF files.

Every PDK reaches it through its own
<pdk>/libs.tech/klayout/tech/scripts/bondpad.py, which is a symlink to this file.
The technology is taken from KLayout itself, so run it with KLAYOUT_PATH scoped
to the PDK you want a bondpad for:

KLAYOUT_PATH=$PDK_ROOT/$PDK/libs.tech/klayout \
klayout -n <tech> -zz -r $PDK_ROOT/$PDK/libs.tech/klayout/tech/scripts/bondpad.py \
        -rd diameter=70.0 -rd shape=square -rd output=macros/bondpad_70x70.gds.gz \
        -rd lef_output=macros/bondpad_70x70.lef

LEF output features:
- MACRO with CLASS COVER for bondpad identification
- PIN on every metal the PCell actually drew, so the router may land on any of
  them
- OBS (obstructions) across the whole metal stack, so nothing routes under the
  pad
- SITE <tech>_ioSite and layer names matching the PDK's io LEF and tech.lef

"""
# pylint: disable=import-error
import os
import pathlib
import sys
import pya
import klayout.db

LIB = 'SG13_dev'
PCELL = 'bondpad'

# The PDK environment variable names the technology directly ('ihp-sg13g2' ->
# 'sg13g2'). It is only trusted when KLayout really has that technology, so a
# stale value cannot silently pick the wrong library. Without it the registry has
# to be unambiguous by itself: '-n <tech>' is not readable from a script that
# loads no layout, and KLAYOUT_PATH is what scopes the registry to one PDK.
def detect_tech():
    """Name of the technology to work in, or exit if it cannot be pinned down."""
    registered = [t for t in pya.Technology.technology_names() if t]

    pdk = os.environ.get('PDK', '').strip()
    if pdk:
        wanted = pdk.removeprefix('ihp-')
        if wanted in registered:
            return wanted
        print(f"Ignoring PDK={pdk!r}: KLayout has no technology {wanted!r}.")

    if len(registered) == 1:
        return registered[0]

    if registered:
        print(f"Cannot tell which of {len(registered)} registered technologies to build for: "
              f"{', '.join(registered)}.")
    else:
        print("No KLayout technology is registered, cannot tell which PDK to build for.")
    print("Set PDK, or scope KLAYOUT_PATH to exactly one PDK, for example:")
    print("  PDK=ihp-<tech> KLAYOUT_PATH=$PDK_ROOT/$PDK/libs.tech/klayout \\")
    print("  klayout -n <tech> -zz -r $PDK_ROOT/$PDK/libs.tech/klayout/tech/scripts/bondpad.py \\")
    print("          -rd diameter=<diameter> -rd output=<path-to-bondpad>")
    sys.exit(1)


TECH = detect_tech()

_TECH_DIR = pathlib.Path(pya.Technology.technology_by_name(TECH).default_base_path)
_MAP_FILE = _TECH_DIR / f"{TECH}.map"
_TECH_LEFS = sorted(_TECH_DIR.parents[2].glob(f"libs.ref/*/lef/{TECH}_tech.lef"))


def read_metal_stack():
    """Routing stack as (LEF name, GDS layer, GDS datatype), bottom to top.

    The names and their order come from the PDK's tech.lef, which is what the
    LEF written here has to agree with, and the GDS numbers from the PDK's layer
    map, which is what the generated layout has to be read through.

    """
    if len(_TECH_LEFS) != 1:
        print(f"Expected exactly one {TECH}_tech.lef under {_TECH_DIR.parents[2]}/libs.ref, "
              f"found {len(_TECH_LEFS)}.")
        sys.exit(1)

    if not _MAP_FILE.is_file():
        print(f"Missing layer map {_MAP_FILE}.")
        sys.exit(1)

    routing = []
    layer = None
    for line in _TECH_LEFS[0].read_text(encoding='utf-8').splitlines():
        fields = line.split()
        if len(fields) >= 2 and fields[0] == 'LAYER':
            layer = fields[1]
        elif layer and len(fields) >= 2 and fields[0] == 'TYPE' and fields[1] == 'ROUTING':
            routing.append(layer)
            layer = None

    gds = {}
    for line in _MAP_FILE.read_text(encoding='utf-8').splitlines():
        fields = line.split()
        if len(fields) >= 4 and 'NET' in fields[1].split(',') and fields[0] not in gds:
            gds[fields[0]] = (int(fields[2]), int(fields[3]))

    missing = [name for name in routing if name not in gds]
    if missing:
        print(f"No layer map entry for {', '.join(missing)} in {_MAP_FILE}.")
        sys.exit(1)

    if not routing:
        print(f"No routing layers found in {_TECH_LEFS[0]}.")
        sys.exit(1)

    return tuple((name, *gds[name]) for name in routing)


METAL_STACK = read_metal_stack()


def layer_extent(layout, top_cell, gds_layer: int, gds_datatype: int):
    """Bounding box of one drawn layer in µm, or None when the layer is unused.

    The geometry is read back from the layout the PCell just produced rather
    than from a table of enclosures, so the LEF always describes the bondpad
    that was actually written, whatever diameter, shape and metal stack the
    PCell resolved.

    :param layout: Layout holding the generated bondpad.
    :param top_cell: Cell the bondpad PCell was instantiated into.
    :param gds_layer: GDS layer number, as listed in the PDK's .map file.
    :param gds_datatype: GDS datatype number.
    :returns: (left, bottom, right, top) in µm, or None.

    """
    box = top_cell.bbox_per_layer(layout.layer(gds_layer, gds_datatype))
    if box.empty():
        return None
    return (box.left * layout.dbu, box.bottom * layout.dbu,
            box.right * layout.dbu, box.top * layout.dbu)


def generate_lef(layout, top_cell, cell_name: str, lef_path: str, bottom_metal: int,
                 pin_name: str):
    """Generate a LEF file for a bondpad macro.

    The pin goes on every stack layer the PCell actually drew, at the extent it
    drew it, so a router may land on any of them. The obstruction covers the
    whole stack at macro size, including layers with no geometry, so nothing
    routes underneath the pad. The passivation opening is deliberately not
    described here: it is not a routing layer.

    :param layout: Layout holding the generated bondpad.
    :param top_cell: Cell the bondpad PCell was instantiated into.
    :param cell_name: Name of the macro (e.g. 'bondpad_70x70').
    :param lef_path: Output path for the LEF file.
    :param bottom_metal: Lowest layer to obstruct, as a 1-based index into the
                         PDK's METAL_STACK.
    :param pin_name: Name of the pad pin.

    """
    macro_box = top_cell.dbbox()

    drawn = [(name, extent) for name, gds_layer, gds_datatype in METAL_STACK
             if (extent := layer_extent(layout, top_cell, gds_layer, gds_datatype)) is not None]

    if not drawn:
        print("The generated bondpad has no metal geometry, cannot write a LEF.")
        sys.exit(1)

    pathlib.Path(lef_path).parent.mkdir(parents=True, exist_ok=True)

    with open(lef_path, 'w', encoding='utf-8') as lef:
        lef.write("VERSION 5.8 ;\n")
        lef.write("\n")

        lef.write(f"MACRO {cell_name}\n")
        lef.write("  CLASS COVER ;\n")
        lef.write("  ORIGIN 0.000 0.000 ;\n")
        lef.write(f"  FOREIGN {cell_name} 0.000 0.000 ;\n")
        lef.write(f"  SIZE {macro_box.width():.3f} BY {macro_box.height():.3f} ;\n")
        lef.write("  SYMMETRY X Y R90 ;\n")
        lef.write(f"  SITE {TECH}_ioSite ;\n")

        lef.write(f"  PIN {pin_name}\n")
        lef.write("    USE SIGNAL ;\n")
        lef.write("    PORT\n")
        for name, extent in drawn:
            lef.write(f"      LAYER {name} ;\n")
            lef.write("        RECT {:.3f} {:.3f} {:.3f} {:.3f} ;\n".format(*extent))
        lef.write("    END\n")
        lef.write(f"  END {pin_name}\n")
        lef.write("\n")

        lef.write("  OBS\n")
        for name, _, _ in METAL_STACK[bottom_metal - 1:]:
            lef.write(f"    LAYER {name} ;\n")
            lef.write(f"      RECT {macro_box.left:.3f} {macro_box.bottom:.3f} "
                      f"{macro_box.right:.3f} {macro_box.top:.3f} ;\n")
        lef.write("  END\n")

        lef.write(f"END {cell_name}\n")

    print(f"LEF written to: {lef_path}")


def generate_bondpad(diameter: float, shape: str, output: str,
                     lef_output: str | None = None, bottom_metal: int = 1,
                     pin_name: str = 'pad'):
    """Function to create a new layout, add the bondpad PCell to a top cell called
    similar to the filename and save it somewhere on the filesystem.

    :param diameter: Diameter of the bondpad in µm.
    :type diameter: float
    :param shape: Shape of the bondpad ('octagon', 'square' or 'circle').
    :type shape: str
    :param output: Path and name of the file where the bondpad should be written to.
    :type output: str
    :param lef_output: Optional path and name of a LEF file to write alongside the GDS.
    :type lef_output: str | None
    :param bottom_metal: Lowest layer to obstruct in the LEF, as a 1-based index
                         into the PDK's METAL_STACK.
    :type bottom_metal: int
    :param pin_name: Name of the pad pin in the LEF.
    :type pin_name: str

    """
    layout = klayout.db.Layout(True)
    layout.dbu = 0.001

    lib = pya.Library.library_by_name(LIB, TECH)
    if lib is None:
        raise RuntimeError(
            f"Could not find the '{LIB}' PCell library in the '{TECH}' KLayout environment.\n"
            f"Please make sure the {TECH.upper()} PDK is properly installed and configured "
            "in KLayout.\n"
            "This may involve:\n"
            "- Cloning the IHP-Open-PDK repository with all submodules (use --recursive)\n"
            f"- Ensuring the {TECH.upper()} technology is registered in KLayout "
            f"(e.g. using -n {TECH})\n"
            "- Running KLayout with a version that supports Python PCells and properly loads them\n"
            f"- Verifying that '{LIB}' appears in the Library Browser under PCells"
        )

    pcell_decl = lib.layout().pcell_declaration(PCELL)

    cell_name = pathlib.Path(output).resolve().name.split('.')[0]
    top_cell = layout.cell(layout.add_cell(cell_name))
    pcell = layout.add_pcell_variant(lib, pcell_decl.id(),
        {'diameter': f'{diameter}u', 'shape': shape})
    layout.cell(pcell)
    top_cell.insert(klayout.db.CellInstArray(pcell, klayout.db.Trans()))

    pathlib.Path(output).parent.mkdir(parents=True, exist_ok=True)

    layout.write(output)
    print(f"GDS written to: {output}")

    if lef_output:
        generate_lef(layout, top_cell, cell_name, lef_output, bottom_metal, pin_name)


try:
    diameter
except NameError:
    print("Missing diameter argument. Please define '-rd diameter=<diameter>'")
    sys.exit(1)

try:
    shape
except NameError:
    shape = 'octagon'  # pylint: disable=invalid-name

allowed_shapes = ('octagon', 'square', 'circle')
if shape not in allowed_shapes:
    print(f"Illegal bondpad shape. Allowed are {','.join(allowed_shapes)}")
    sys.exit(1)

try:
    output
except NameError:
    print("Missing output argument. Please define '-rd output=<path-to-bondpad>'")
    sys.exit(1)

try:
    lef_output
except NameError:
    lef_output = None  # pylint: disable=invalid-name

try:
    pin_name
except NameError:
    pin_name = 'pad'  # pylint: disable=invalid-name

try:
    bottom_metal = int(bottom_metal)
except NameError:
    bottom_metal = 1  # pylint: disable=invalid-name
except ValueError:
    print(f"Invalid bottom_metal={bottom_metal}. Must be an integer.")
    sys.exit(1)

if not 1 <= bottom_metal <= len(METAL_STACK):
    names = ', '.join(f"{i + 1}={n}" for i, (n, _, _) in enumerate(METAL_STACK))
    print(f"Invalid bottom_metal={bottom_metal}. Must be 1-{len(METAL_STACK)} ({names}).")
    sys.exit(1)

generate_bondpad(diameter, shape, output,  # pylint: disable=undefined-variable
                 lef_output=lef_output,
                 bottom_metal=bottom_metal,
                 pin_name=pin_name)
