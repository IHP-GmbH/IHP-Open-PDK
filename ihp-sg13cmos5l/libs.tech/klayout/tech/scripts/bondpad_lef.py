#!/usr/bin/env python3
"""Standalone bondpad LEF generator for SG13CMOS5L PDK.

This script generates LEF files for bondpad macros without requiring KLayout.
It produces LEF-only output suitable for OpenROAD/LibreLane P&R flows.

Usage:
    python bondpad_lef.py --size 70 --shape square --output bondpad_70x70.lef
    python bondpad_lef.py --size 80 --shape octagon --output bondpad_80x80_oct.lef
    python bondpad_lef.py --size 70 --bottom-metal 2 --output bondpad_70x70_m2.lef

For GDS+LEF generation, use bondpad.py with KLayout instead.
"""

import argparse
import pathlib
import sys

# SG13CMOS5L metal stack layer names (must match sg13cmos5l_tech.lef)
METAL_LAYERS = ['Metal1', 'Metal2', 'Metal3', 'Metal4', 'TopMetal1']

# Default metal enclosures from bondpad edge (in microns)
# These create a stair-step pattern with smaller metals toward the bottom
DEFAULT_ENCLOSURES = {
    'TopMetal1': 0.0,   # Full size (bondable surface)
    'Metal4': 1.0,      # 1.0um enclosure
    'Metal3': 1.5,      # 1.5um enclosure
    'Metal2': 2.0,      # 2.0um enclosure
    'Metal1': 2.5,      # 2.5um enclosure
}


def generate_bondpad_lef(
    cell_name: str,
    size: float,
    shape: str = 'square',
    bottom_metal: int = 1,
    passiv_enclosure: float = 2.1,
    metal_enclosures: dict = None,
    output_path: str = None,
) -> str:
    """Generate LEF content for a bondpad macro.

    Args:
        cell_name: Name of the macro (e.g., 'bondpad_70x70')
        size: Size of the bondpad in microns (square/octagon diameter)
        shape: Shape of the bondpad ('square', 'octagon', 'circle')
        bottom_metal: Lowest metal layer index (1-4)
        passiv_enclosure: Passivation enclosure in TopMetal1
        metal_enclosures: Custom enclosures dict (layer_name -> um)
        output_path: Output file path (if None, returns string)

    Returns:
        LEF content as string (if output_path is None)
    """
    if metal_enclosures is None:
        metal_enclosures = DEFAULT_ENCLOSURES.copy()

    lines = []

    # LEF header
    lines.append("VERSION 5.7 ;")
    lines.append("NOWIREEXTENSIONATPIN ON ;")
    lines.append("DIVIDERCHAR \"/\" ;")
    lines.append("BUSBITCHARS \"[]\" ;")
    lines.append("")

    # MACRO definition
    lines.append(f"MACRO {cell_name}")
    lines.append("  CLASS COVER BUMP ;")
    lines.append(f"  FOREIGN {cell_name} ;")
    lines.append("  ORIGIN 0.000 0.000 ;")
    lines.append(f"  SIZE {size:.3f} BY {size:.3f} ;")
    lines.append("")

    # PIN definition - PAD on TopMetal1
    lines.append("  PIN PAD")
    lines.append("    DIRECTION INOUT ;")
    lines.append("    USE SIGNAL ;")
    lines.append("    PORT")
    lines.append("      LAYER TopMetal1 ;")

    enc = metal_enclosures.get('TopMetal1', 0.0)
    if shape == 'square':
        lines.append(f"        RECT {enc:.3f} {enc:.3f} {size - enc:.3f} {size - enc:.3f} ;")
    elif shape == 'octagon':
        # Octagon corner cut = size * (1 - 1/sqrt(2)) / 2 ≈ 0.146 * size
        corner = size * 0.146
        lines.append(f"        RECT {corner + enc:.3f} {enc:.3f} {size - corner - enc:.3f} {size - enc:.3f} ;")
        lines.append(f"        RECT {enc:.3f} {corner + enc:.3f} {size - enc:.3f} {size - corner - enc:.3f} ;")
    else:  # circle - approximate with rectangle
        lines.append(f"        RECT {enc:.3f} {enc:.3f} {size - enc:.3f} {size - enc:.3f} ;")

    lines.append("    END")
    lines.append("  END PAD")
    lines.append("")

    # OBS (Obstructions) - block routing on metal layers
    lines.append("  OBS")

    # Add obstruction for each metal layer from bottom_metal to TopMetal1
    for i in range(bottom_metal - 1, len(METAL_LAYERS)):
        layer_name = METAL_LAYERS[i]
        enc = metal_enclosures.get(layer_name, 0.0)
        lines.append(f"    LAYER {layer_name} ;")
        lines.append(f"      RECT {enc:.3f} {enc:.3f} {size - enc:.3f} {size - enc:.3f} ;")

    lines.append("  END")
    lines.append(f"END {cell_name}")
    lines.append("")
    lines.append("END LIBRARY")

    lef_content = '\n'.join(lines)

    if output_path:
        pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(lef_content)
        print(f"LEF written to: {output_path}")
        return output_path
    else:
        return lef_content


def main():
    parser = argparse.ArgumentParser(
        description='Generate bondpad LEF for SG13CMOS5L PDK',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--size', '-s', type=float, required=True,
        help='Bondpad size in microns (e.g., 70 for 70x70um)'
    )
    parser.add_argument(
        '--shape', choices=['square', 'octagon', 'circle'], default='square',
        help='Bondpad shape (default: square)'
    )
    parser.add_argument(
        '--name', '-n', type=str, default=None,
        help='Macro name (default: bondpad_<size>x<size>)'
    )
    parser.add_argument(
        '--output', '-o', type=str, required=True,
        help='Output LEF file path'
    )
    parser.add_argument(
        '--bottom-metal', type=int, default=1, choices=[1, 2, 3, 4],
        help='Lowest metal layer (1-4, default: 1)'
    )
    parser.add_argument(
        '--passiv-enclosure', type=float, default=2.1,
        help='Passivation enclosure in TopMetal1 (default: 2.1um)'
    )

    args = parser.parse_args()

    # Generate cell name if not provided
    cell_name = args.name
    if cell_name is None:
        size_str = f"{int(args.size)}x{int(args.size)}"
        shape_suffix = '' if args.shape == 'square' else f'_{args.shape}'
        cell_name = f"bondpad_{size_str}{shape_suffix}"

    # Validate size
    if args.size < 10 or args.size > 200:
        print(f"Warning: Unusual bondpad size {args.size}um (typical: 50-100um)")

    # Generate LEF
    generate_bondpad_lef(
        cell_name=cell_name,
        size=args.size,
        shape=args.shape,
        bottom_metal=args.bottom_metal,
        passiv_enclosure=args.passiv_enclosure,
        output_path=args.output,
    )


if __name__ == '__main__':
    main()
