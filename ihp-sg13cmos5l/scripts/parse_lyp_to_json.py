#!/usr/bin/env python3
"""
Parse KLayout .lyp files and generate JSON layer databases.
Creates two outputs:
  - ihp-sg13g2_layers.json: Full PDK layer database
  - ihp-sg13cmos5l_layers.json: SG13CMOS5L PDK (CMOS only, M1-M4-TM1)
"""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# Layers to KEEP in SG13CMOS5L PDK (GDS layer numbers)
KEEP_LAYERS = {
    1,   # Activ - Active area
    5,   # GatPoly - Gate polysilicon
    6,   # Cont - Contacts
    7,   # nSD - N-source/drain
    8,   # Metal1 - Routing metal 1
    9,   # Passiv - Passivation
    10,  # Metal2 - Routing metal 2
    14,  # pSD - P-source/drain
    19,  # Via1 - M1-M2 via
    24,  # RES - Resistor ID
    28,  # SalBlock - SAL isolation
    29,  # Via2 - M2-M3 via
    30,  # Metal3 - Routing metal 3
    31,  # NWell - N-well
    32,  # nBuLay - N-buried layer
    40,  # Substrate - Silicon substrate
    44,  # ThickGateOx - Thick gate oxide
    46,  # PWell - P-well
    49,  # Via3 - M3-M4 via
    50,  # Metal4 - Routing metal 4
    66,  # Via4 - M4-M5 via
    67,  # Metal5 - Routing metal 5
    83,  # AntVia1 - Antenna via 1
    84,  # AntMetal2 - Antenna metal 2
    128, # PolyRes - Poly resistor
    132, # AntMetal1 - Antenna metal 1
    146, # ThinFilmRes - Thin film resistor
    160, # NoMetFiller - No metal filler
    189, # prBoundary - PR boundary
}

def parse_source(source: str) -> tuple:
    """Parse source string like '1/0' into (layer, datatype)."""
    match = re.match(r'(\d+)/(\d+)', source)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def parse_lyp_file(lyp_path: Path) -> dict:
    """Parse a .lyp file and return structured layer data."""
    tree = ET.parse(lyp_path)
    root = tree.getroot()

    layers = {}
    custom_dither_patterns = []
    custom_line_styles = []

    for prop in root.findall('properties'):
        name_elem = prop.find('name')
        source_elem = prop.find('source')

        if name_elem is None or source_elem is None:
            continue

        name = name_elem.text
        source = source_elem.text
        gds_layer, datatype = parse_source(source)

        if gds_layer is None:
            continue

        # Extract layer base name and purpose
        if '.' in name:
            base_name, purpose = name.rsplit('.', 1)
        else:
            base_name, purpose = name, "drawing"

        # Extract display properties
        props = {
            "purpose": purpose,
            "frame_color": prop.findtext('frame-color', ''),
            "fill_color": prop.findtext('fill-color', ''),
            "frame_brightness": int(prop.findtext('frame-brightness', '0')),
            "fill_brightness": int(prop.findtext('fill-brightness', '0')),
            "dither_pattern": prop.findtext('dither-pattern', ''),
            "line_style": prop.findtext('line-style', ''),
            "valid": prop.findtext('valid', 'true') == 'true',
            "visible": prop.findtext('visible', 'true') == 'true',
            "transparent": prop.findtext('transparent', 'false') == 'true',
            "width": int(prop.findtext('width', '1')),
            "marked": prop.findtext('marked', 'false') == 'true',
            "animation": int(prop.findtext('animation', '0')),
        }

        # Initialize layer entry if needed
        gds_key = str(gds_layer)
        if gds_key not in layers:
            layers[gds_key] = {
                "name": base_name,
                "gds_layer": gds_layer,
                "datatypes": {}
            }

        # Add datatype entry
        layers[gds_key]["datatypes"][str(datatype)] = props

    # Parse custom dither patterns
    for pattern in root.findall('custom-dither-pattern'):
        pattern_data = {
            "name": pattern.findtext('name', ''),
            "order": int(pattern.findtext('order', '0')),
            "lines": [line.text for line in pattern.find('pattern').findall('line')]
        }
        custom_dither_patterns.append(pattern_data)

    # Parse custom line styles
    for style in root.findall('custom-line-style'):
        style_data = {
            "name": style.findtext('name', ''),
            "order": int(style.findtext('order', '0')),
            "pattern": style.findtext('pattern', '')
        }
        custom_line_styles.append(style_data)

    return {
        "layers": layers,
        "custom_dither_patterns": custom_dither_patterns,
        "custom_line_styles": custom_line_styles
    }


def create_full_pdk_json(parsed_data: dict, source_file: str) -> dict:
    """Create the full PDK JSON database."""
    return {
        "pdk_name": "ihp-sg13g2",
        "description": "IHP SG13G2 130nm BiCMOS PDK - Full layer set",
        "source_file": source_file,
        "generated_at": datetime.now().isoformat(),
        "layer_count": len(parsed_data["layers"]),
        "layers": parsed_data["layers"],
        "custom_dither_patterns": parsed_data["custom_dither_patterns"],
        "custom_line_styles": parsed_data["custom_line_styles"]
    }


def create_sg13cmos5l_pdk_json(parsed_data: dict) -> dict:
    """Create the SG13CMOS5L PDK JSON database with only kept layers."""
    sg13cmos5l_layers = {}

    for gds_key, layer_data in parsed_data["layers"].items():
        gds_layer = int(gds_key)
        if gds_layer in KEEP_LAYERS:
            # Copy layer data and add included flag
            sg13cmos5l_layers[gds_key] = {
                **layer_data,
                "included": True
            }

    return {
        "pdk_name": "ihp-sg13cmos5l",
        "description": "IHP SG13CMOS5L PDK - CMOS-only with M1-M4-TM1 metal stack",
        "base_pdk": "ihp-sg13g2",
        "generated_at": datetime.now().isoformat(),
        "layer_count": len(sg13cmos5l_layers),
        "notes": [
            "This is an editable file - modify 'included' flags to add/remove layers",
            "Run generate_layer_files.py after modifications to regenerate KLayout files"
        ],
        "layers": sg13cmos5l_layers,
        "custom_dither_patterns": parsed_data["custom_dither_patterns"],
        "custom_line_styles": parsed_data["custom_line_styles"]
    }


def main():
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent  # IHP-Open-PDK

    full_pdk_lyp = repo_root / "ihp-sg13g2" / "libs.tech" / "klayout" / "tech" / "sg13g2.lyp"
    output_dir = script_dir.parent / "layer_tracking"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Parsing {full_pdk_lyp}...")
    parsed_data = parse_lyp_file(full_pdk_lyp)

    total_layers = len(parsed_data["layers"])
    total_datatypes = sum(len(l["datatypes"]) for l in parsed_data["layers"].values())
    print(f"Found {total_layers} unique GDS layers with {total_datatypes} total layer/datatype combinations")

    # Create full PDK JSON
    full_json = create_full_pdk_json(parsed_data, str(full_pdk_lyp.relative_to(repo_root)))
    full_json_path = output_dir / "ihp-sg13g2_layers.json"
    with open(full_json_path, 'w') as f:
        json.dump(full_json, f, indent=2)
    print(f"Created {full_json_path}")

    # Create SG13CMOS5L PDK JSON
    sg13cmos5l_json = create_sg13cmos5l_pdk_json(parsed_data)
    sg13cmos5l_json_path = output_dir / "ihp-sg13cmos5l_layers.json"
    with open(sg13cmos5l_json_path, 'w') as f:
        json.dump(sg13cmos5l_json, f, indent=2)
    print(f"Created {sg13cmos5l_json_path} with {sg13cmos5l_json['layer_count']} layers")

    # Summary
    kept_datatypes = sum(
        len(l["datatypes"]) for l in sg13cmos5l_json["layers"].values()
    )
    print(f"\nSummary:")
    print(f"  Full PDK: {total_layers} layers, {total_datatypes} variants")
    print(f"  SG13CMOS5L PDK: {sg13cmos5l_json['layer_count']} layers, {kept_datatypes} variants")


if __name__ == "__main__":
    main()
