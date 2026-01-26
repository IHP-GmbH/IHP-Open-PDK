"""Module to automatically generate a bondpad and create GDS and LEF files.

Can be used in Klayout's batch mode. For example:

# Generate GDS only:
klayout -n sg13cmos5l -zz -r bondpad.py \
        -rd diameter=70.0 -rd shape=square -rd output=macros/bondpad_70x70.gds.gz

# Generate both GDS and LEF:
klayout -n sg13cmos5l -zz -r bondpad.py \
        -rd diameter=70.0 -rd shape=square -rd output=macros/bondpad_70x70.gds.gz \
        -rd lef_output=macros/bondpad_70x70.lef

# LEF output features:
# - MACRO with CLASS COVER BUMP for bondpad identification
# - PIN PAD on TopMetal1 (bondable surface)
# - OBS (obstructions) for Metal1-Metal4 routing blockage
# - Proper SG13CMOS5L layer names matching tech.lef
"""
# pylint: disable=import-error
import pathlib
import sys
import pya
import klayout.db

LIB = 'SG13_dev'
PCELL = 'bondpad'

# SG13CMOS5L metal stack layer names (must match sg13cmos5l_tech.lef)
METAL_LAYERS = ['Metal1', 'Metal2', 'Metal3', 'Metal4', 'TopMetal1']


def generate_lef(cell_name: str, diameter: float, shape: str, lef_path: str,
                 passiv_enclosure: float = 2.1, bottom_metal: int = 1):
    """Generate LEF file for a bondpad macro.

    :param cell_name: Name of the macro (e.g., 'bondpad_70x70')
    :param diameter: Diameter/size of the bondpad in microns
    :param shape: Shape of the bondpad ('square', 'octagon', 'circle')
    :param lef_path: Output path for the LEF file
    :param passiv_enclosure: Passivation enclosure in TopMetal1 (default 2.1um)
    :param bottom_metal: Lowest metal layer index (1-4, default 1)
    """
    # Calculate bondpad dimensions
    # For square, size = diameter
    # For octagon, we use the same bounding box
    size = diameter

    # The pad opening is TopMetal1 minus passivation enclosure
    pad_opening = size - 2 * passiv_enclosure

    # Metal stack enclosures (inner metals are smaller due to design rules)
    # These are approximate values based on typical bondpad design
    metal_enclosures = {
        'TopMetal1': 0.0,      # Full size (bondable surface)
        'Metal4': 1.0,         # 1um enclosure from edge
        'Metal3': 1.5,         # Cascading enclosures
        'Metal2': 2.0,
        'Metal1': 2.5,
    }

    # Create directory
    pathlib.Path(lef_path).parent.mkdir(parents=True, exist_ok=True)

    with open(lef_path, 'w', encoding='utf-8') as f:
        # LEF header
        f.write("VERSION 5.7 ;\n")
        f.write("NOWIREEXTENSIONATPIN ON ;\n")
        f.write("DIVIDERCHAR \"/\" ;\n")
        f.write("BUSBITCHARS \"[]\" ;\n")
        f.write("\n")

        # MACRO definition
        f.write(f"MACRO {cell_name}\n")
        f.write("  CLASS COVER BUMP ;\n")
        f.write(f"  FOREIGN {cell_name} ;\n")
        f.write("  ORIGIN 0.000 0.000 ;\n")
        f.write(f"  SIZE {size:.3f} BY {size:.3f} ;\n")
        f.write("\n")

        # PIN definition - PAD on TopMetal1
        f.write("  PIN PAD\n")
        f.write("    DIRECTION INOUT ;\n")
        f.write("    USE SIGNAL ;\n")
        f.write("    PORT\n")
        f.write("      LAYER TopMetal1 ;\n")
        if shape == 'square':
            # Square bondpad - simple rectangle
            enc = metal_enclosures['TopMetal1']
            f.write(f"        RECT {enc:.3f} {enc:.3f} {size - enc:.3f} {size - enc:.3f} ;\n")
        elif shape == 'octagon':
            # Octagon - approximate with polygon
            # For LEF, we use a rectangle that inscribes the octagon
            enc = metal_enclosures['TopMetal1']
            # Octagon corner cut = size * (1 - 1/sqrt(2)) / 2 ≈ 0.146 * size
            corner = size * 0.146
            f.write(f"        RECT {corner + enc:.3f} {enc:.3f} {size - corner - enc:.3f} {size - enc:.3f} ;\n")
            f.write(f"        RECT {enc:.3f} {corner + enc:.3f} {size - enc:.3f} {size - corner - enc:.3f} ;\n")
        else:  # circle - approximate with rectangle
            enc = metal_enclosures['TopMetal1']
            f.write(f"        RECT {enc:.3f} {enc:.3f} {size - enc:.3f} {size - enc:.3f} ;\n")
        f.write("    END\n")
        f.write("  END PAD\n")
        f.write("\n")

        # OBS (Obstructions) - block routing on metal layers
        f.write("  OBS\n")

        # Add obstruction for each metal layer from bottom_metal to Metal4
        for i in range(bottom_metal - 1, 4):  # Metal1 (idx 0) to Metal4 (idx 3)
            layer_name = METAL_LAYERS[i]
            enc = metal_enclosures.get(layer_name, 2.0)
            f.write(f"    LAYER {layer_name} ;\n")
            f.write(f"      RECT {enc:.3f} {enc:.3f} {size - enc:.3f} {size - enc:.3f} ;\n")

        # Also add TopMetal1 as obstruction (except for PAD pin area)
        # This prevents routing over the bondpad
        f.write(f"    LAYER TopMetal1 ;\n")
        enc = metal_enclosures['TopMetal1']
        f.write(f"      RECT {enc:.3f} {enc:.3f} {size - enc:.3f} {size - enc:.3f} ;\n")

        f.write("  END\n")
        f.write(f"END {cell_name}\n")
        f.write("\n")
        f.write("END LIBRARY\n")

    print(f"LEF written to: {lef_path}")


def generate_bondpad(diameter: float, shape: str, output: str,
                     lef_output: str = None, bottom_metal: int = 1):
    """Function to create a new layout, add the bondpad PCell to a top cell called
    similar to the filename and save it somewhere on the filesystem.

    :param diameter: Diameter of the bondpad in microns.
    :param shape: Shape of the bondpad ('square', 'octagon', 'circle').
    :param output: Path and name of the GDS file to write.
    :param lef_output: Optional path for LEF file output.
    :param bottom_metal: Lowest metal layer (1-4, default 1).
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
    print(f"GDS written to: {output}")

    # Generate LEF if requested
    if lef_output:
        generate_lef(cell_name, diameter, shape, lef_output,
                     bottom_metal=bottom_metal)

# Handle command-line arguments passed via -rd

try:
    diameter  # noqa: F821 - defined by klayout -rd
except NameError:
    print("Missing diameter argument. Please define '-rd diameter=<diameter>'")
    sys.exit(1)

try:
    shape  # noqa: F821 - defined by klayout -rd
except NameError:
    shape = 'octagon'  # pylint: disable=invalid-name

allowed_shapes = ('octagon', 'square', 'circle')
if shape not in allowed_shapes:
    print(f"Illegal bondpad shape. Allowed are {','.join(allowed_shapes)}")
    sys.exit(1)

try:
    output  # noqa: F821 - defined by klayout -rd
except NameError:
    print("Missing output argument. Please define '-rd output=<path-to-bondpad>'")
    sys.exit(1)

# Optional LEF output
try:
    lef_output  # noqa: F821 - defined by klayout -rd
except NameError:
    lef_output = None  # pylint: disable=invalid-name

# Optional bottom metal (default: Metal1)
try:
    bottom_metal  # noqa: F821 - defined by klayout -rd
    bottom_metal = int(bottom_metal)
except NameError:
    bottom_metal = 1  # pylint: disable=invalid-name

if bottom_metal < 1 or bottom_metal > 4:
    print(f"Invalid bottom_metal={bottom_metal}. Must be 1-4.")
    sys.exit(1)

# Generate bondpad GDS and optionally LEF
generate_bondpad(diameter, shape, output,  # pylint: disable=undefined-variable
                 lef_output=lef_output,
                 bottom_metal=bottom_metal)
