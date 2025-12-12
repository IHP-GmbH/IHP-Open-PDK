#!/usr/bin/env python3
"""
Generate KLayout layer files from JSON database.
Reads ihp-sg13cmos5l_layers.json and generates:
  - sg13cmos5l.lyp (layer properties)
  - sg13cmos5l.lyt (technology config)
  - sg13cmos5l.map (LEF/DEF layer mapping)
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime
import argparse


def load_layer_database(json_path: Path) -> dict:
    """Load the layer database from JSON."""
    with open(json_path) as f:
        return json.load(f)


def generate_lyp(db: dict, output_path: Path):
    """Generate .lyp file from layer database."""
    root = ET.Element('layer-properties')

    # Add XML declaration comment
    comment = ET.Comment(f'''
 IHP SG13CMOS5L PDK Layer Properties
 Generated: {datetime.now().isoformat()}

 Copyright 2024 IHP PDK Authors
 Licensed under the Apache License, Version 2.0
''')
    root.insert(0, comment)

    # Add layer properties
    for gds_key in sorted(db["layers"].keys(), key=lambda x: int(x)):
        layer_data = db["layers"][gds_key]

        # Skip if not included
        if not layer_data.get("included", True):
            continue

        gds_layer = layer_data["gds_layer"]
        base_name = layer_data["name"]

        for dt_key in sorted(layer_data["datatypes"].keys(), key=lambda x: int(x)):
            dt_data = layer_data["datatypes"][dt_key]

            props = ET.SubElement(root, 'properties')
            ET.SubElement(props, 'frame-color').text = dt_data.get("frame_color", "#ffffff")
            ET.SubElement(props, 'fill-color').text = dt_data.get("fill_color", "#ffffff")
            ET.SubElement(props, 'frame-brightness').text = str(dt_data.get("frame_brightness", 0))
            ET.SubElement(props, 'fill-brightness').text = str(dt_data.get("fill_brightness", 0))
            ET.SubElement(props, 'dither-pattern').text = dt_data.get("dither_pattern", "I1")
            ET.SubElement(props, 'line-style').text = dt_data.get("line_style", "C0")
            ET.SubElement(props, 'valid').text = str(dt_data.get("valid", True)).lower()
            ET.SubElement(props, 'visible').text = str(dt_data.get("visible", True)).lower()
            ET.SubElement(props, 'transparent').text = str(dt_data.get("transparent", False)).lower()
            ET.SubElement(props, 'width').text = str(dt_data.get("width", 1))
            ET.SubElement(props, 'marked').text = str(dt_data.get("marked", False)).lower()
            ET.SubElement(props, 'animation').text = str(dt_data.get("animation", 0))
            ET.SubElement(props, 'name').text = f"{base_name}.{dt_data['purpose']}"
            ET.SubElement(props, 'source').text = f"{gds_layer}/{dt_key}"

    # Add custom dither patterns
    for pattern in db.get("custom_dither_patterns", []):
        cdp = ET.SubElement(root, 'custom-dither-pattern')
        pat_elem = ET.SubElement(cdp, 'pattern')
        for line in pattern.get("lines", []):
            ET.SubElement(pat_elem, 'line').text = line
        ET.SubElement(cdp, 'order').text = str(pattern.get("order", 0))
        ET.SubElement(cdp, 'name').text = pattern.get("name", "")

    # Add custom line styles
    for style in db.get("custom_line_styles", []):
        cls = ET.SubElement(root, 'custom-line-style')
        ET.SubElement(cls, 'pattern').text = style.get("pattern", "")
        ET.SubElement(cls, 'order').text = str(style.get("order", 0))
        ET.SubElement(cls, 'name').text = style.get("name", "")

    # Format and write
    xml_str = ET.tostring(root, encoding='unicode')
    # Add XML declaration
    xml_str = "<?xml version='1.0' encoding='UTF-8'?>\n" + xml_str

    # Pretty print
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ')
    # Remove extra blank lines and fix declaration
    lines = [l for l in pretty_xml.split('\n') if l.strip()]
    lines[0] = "<?xml version='1.0' encoding='UTF-8'?>"

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
        f.write('\n')

    print(f"Generated {output_path}")


def generate_lyt(db: dict, output_path: Path):
    """Generate .lyt file from layer database."""
    # Connectivity definitions for SG13CMOS5L PDK (M1-M4-TM1 stack)
    connectivity_connections = [
        ("GatPoly,Cont,Metal1", False),
        ("Diff,Cont,Metal1", False),
        ("Metal1,Via1,Metal2", False),
        ("Metal2,Via2,Metal3", False),
        ("Metal3,Via3,Metal4", False),
        ("Metal4,TopVia1,TopMetal1", False),
        # Metal5/Via4 and TopMetal2 not available in SG13CMOS5L PDK
        # ("Metal4,Via4,Metal5", True),
        # ("Metal5,TopVia1,TopMetal1", True),
        # ("TopMetal1,TopVia2,TopMetal2", True),
    ]

    connectivity_symbols = [
        ("SalBlock='28/0'", False),
        ("Activ='1/0-Salblock'", False),
        ("GatPoly='5/0-SalBlock'", False),
        ("Diff='Activ-GatPoly'", False),
        ("Cont='6/0'", False),
        ("Metal1='8/0-8/29'", False),
        ("Via1='19/0'", False),
        ("Metal2='10/0-10/29'", False),
        ("Via2='29/0'", False),
        ("Metal3='30/0-30/29'", False),
        ("Via3='49/0'", False),
        ("Metal4='50/0-50/29'", False),
        ("TopVia1='125/0'", False),
        ("TopMetal1='126/0-126/29'", False),
        # Metal5/Via4 and TopMetal2 not available in SG13CMOS5L PDK
        # ("Via4='66/0'", True),
        # ("Metal5='67/0-67/29'", True),
        # ("TopVia2='133/0'", True),
        # ("TopMetal2='134/0-134/29'", True),
    ]

    lyt_content = f'''<?xml version="1.0" encoding="utf-8"?>
<!--
 IHP SG13CMOS5L PDK Technology Definition
 Generated: {datetime.now().isoformat()}

 Copyright 2024 IHP PDK Authors
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
     https://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<technology>
 <name>sg13cmos5l</name>
 <description>IHP SG13CMOS5L PDK (M1-M4-TM1 stack)</description>
 <group/>
 <dbu>0.001</dbu>
 <base-path></base-path>
 <original-base-path></original-base-path>
 <layer-properties_file>sg13cmos5l.lyp</layer-properties_file>
 <add-other-layers>true</add-other-layers>
 <default-grids>0.01,0.005!</default-grids>
 <reader-options>
  <gds2>
   <box-mode>1</box-mode>
   <allow-big-records>true</allow-big-records>
   <allow-multi-xy-records>true</allow-multi-xy-records>
  </gds2>
  <common>
   <create-other-layers>true</create-other-layers>
   <layer-map>layer_map()</layer-map>
   <enable-properties>true</enable-properties>
   <enable-text-objects>true</enable-text-objects>
  </common>
  <lefdef>
   <read-all-layers>true</read-all-layers>
   <layer-map>layer_map()</layer-map>
   <dbu>0.001</dbu>
   <produce-net-names>true</produce-net-names>
   <net-property-name>#1</net-property-name>
   <produce-inst-names>true</produce-inst-names>
   <inst-property-name>#1</inst-property-name>
   <produce-pin-names>false</produce-pin-names>
   <pin-property-name>#1</pin-property-name>
   <produce-cell-outlines>true</produce-cell-outlines>
   <cell-outline-layer>OUTLINE</cell-outline-layer>
   <produce-placement-blockages>true</produce-placement-blockages>
   <placement-blockage-layer>PLACEMENT_BLK</placement-blockage-layer>
   <produce-regions>true</produce-regions>
   <region-layer>REGIONS</region-layer>
   <produce-via-geometry>true</produce-via-geometry>
   <via_geometry-suffix-string/>
   <via_geometry-datatype-string>0</via_geometry-datatype-string>
   <produce-pins>true</produce-pins>
   <pins-suffix-string>.PIN</pins-suffix-string>
   <pins-datatype-string>2</pins-datatype-string>
   <produce-lef-pins>true</produce-lef-pins>
   <lef_pins-suffix-string>.PIN</lef_pins-suffix-string>
   <lef_pins-datatype-string>2</lef_pins-datatype-string>
   <produce-fills>true</produce-fills>
   <fills-suffix-string>.FILL</fills-suffix-string>
   <fills-datatype-string>5</fills-datatype-string>
   <produce-obstructions>true</produce-obstructions>
   <obstructions-suffix>.OBS</obstructions-suffix>
   <obstructions-datatype>3</obstructions-datatype>
   <produce-blockages>true</produce-blockages>
   <blockages-suffix>.BLK</blockages-suffix>
   <blockages-datatype>4</blockages-datatype>
   <produce-labels>true</produce-labels>
   <labels-suffix>.LABEL</labels-suffix>
   <labels-datatype>1</labels-datatype>
   <produce-lef-labels>true</produce-lef-labels>
   <lef-labels-suffix>.LABEL</lef-labels-suffix>
   <lef-labels-datatype>1</lef-labels-datatype>
   <produce-routing>true</produce-routing>
   <routing-suffix-string/>
   <routing-datatype-string>0</routing-datatype-string>
   <produce-special-routing>true</produce-special-routing>
   <special-routing-suffix-string/>
   <special-routing-datatype-string>0</special-routing-datatype-string>
   <via-cellname-prefix>VIA_</via-cellname-prefix>
   <read-lef-with-def>true</read-lef-with-def>
   <macro-resolution-mode>default</macro-resolution-mode>
   <separate-groups>false</separate-groups>
   <map-file>sg13cmos5l.map</map-file>
   <lef-files></lef-files>
  </lefdef>
  <mebes>
   <invert>false</invert>
   <subresolution>true</subresolution>
   <produce-boundary>true</produce-boundary>
   <num-stripes-per-cell>64</num-stripes-per-cell>
   <num-shapes-per-cell>0</num-shapes-per-cell>
   <data-layer>1</data-layer>
   <data-datatype>0</data-datatype>
   <data-name>DATA</data-name>
   <boundary-layer>0</boundary-layer>
   <boundary-datatype>0</boundary-datatype>
   <boundary-name>BORDER</boundary-name>
   <layer-map>layer_map()</layer-map>
   <create-other-layers>true</create-other-layers>
  </mebes>
  <dxf>
   <dbu>0.001</dbu>
   <unit>1</unit>
   <text-scaling>100</text-scaling>
   <circle-points>100</circle-points>
   <circle-accuracy>0</circle-accuracy>
   <contour-accuracy>0</contour-accuracy>
   <polyline-mode>0</polyline-mode>
   <render-texts-as-polygons>false</render-texts-as-polygons>
   <keep-other-cells>false</keep-other-cells>
   <keep-layer-names>false</keep-layer-names>
   <create-other-layers>true</create-other-layers>
   <layer-map>layer_map()</layer-map>
  </dxf>
  <cif>
   <wire-mode>0</wire-mode>
   <dbu>0.001</dbu>
   <layer-map>layer_map()</layer-map>
   <create-other-layers>true</create-other-layers>
   <keep-layer-names>false</keep-layer-names>
  </cif>
  <mag>
   <lambda>1</lambda>
   <dbu>0.001</dbu>
   <layer-map>layer_map()</layer-map>
   <create-other-layers>true</create-other-layers>
   <keep-layer-names>false</keep-layer-names>
   <merge>true</merge>
   <lib-paths>
   </lib-paths>
  </mag>
 </reader-options>
 <writer-options>
  <format>GDS2</format>
  <gds2>
   <write-timestamps>true</write-timestamps>
   <write-cell-properties>false</write-cell-properties>
   <write-file-properties>false</write-file-properties>
   <no-zero-length-paths>false</no-zero-length-paths>
   <multi-xy-records>false</multi-xy-records>
   <resolve-skew-arrays>false</resolve-skew-arrays>
   <max-vertex-count>8000</max-vertex-count>
   <max-cellname-length>32000</max-cellname-length>
   <libname>LIB</libname>
  </gds2>
  <oasis>
   <compression-level>2</compression-level>
   <write-cblocks>true</write-cblocks>
   <strict-mode>true</strict-mode>
   <write-std-properties>1</write-std-properties>
   <subst-char>*</subst-char>
   <permissive>false</permissive>
  </oasis>
  <cif>
   <polygon-mode>0</polygon-mode>
  </cif>
  <cif>
   <dummy-calls>false</dummy-calls>
   <blank-separator>false</blank-separator>
  </cif>
  <mag>
   <lambda>0</lambda>
   <tech/>
   <write-timestamp>true</write-timestamp>
  </mag>
 </writer-options>
 <connectivity>
'''
    # Add connections
    for conn, commented in connectivity_connections:
        if commented:
            lyt_content += f'  <!-- <connection>{conn}</connection> -->\n'
        else:
            lyt_content += f'  <connection>{conn}</connection>\n'

    # Add symbols
    for sym, commented in connectivity_symbols:
        if commented:
            lyt_content += f"  <!-- <symbols>{sym}</symbols> -->\n"
        else:
            lyt_content += f"  <symbols>{sym}</symbols>\n"

    lyt_content += ''' </connectivity>
</technology>
'''

    with open(output_path, 'w') as f:
        f.write(lyt_content)

    print(f"Generated {output_path}")


def generate_map(db: dict, output_path: Path):
    """Generate .map file from layer database (M1-M4-TM1 stack)."""
    map_content = f'''#************************************************************************
#************************************************************************
# File: sg13cmos5l.map
# Generated: {datetime.now().strftime('%B %d, %Y')}
#************************************************************************
#************************************************************************
#
# IHP SG13CMOS5L PDK Layer Mapping
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
#
#*************************************************************************
#-------------------------------------------------------------------------
# EDI Stream layer mapping table for SG13CMOS5L PDK (M1-M4-TM1 stack)
# Version: 1.0
# Use only in combination with valid GDSII data of all used blocks!
#-------------------------------------------------------------------------
#EDI Layer Name  EDI Layer Type               GDS Layer Number   GDS Layer Type
#==============  ==============               ================   ==============

Metal1           NET,SPNET,PIN,LEFPIN,VIA     8                  0
Metal1           PIN,LEFPIN                   8                  2
Metal1           FILL                         8                  22
Metal1           LEFOBS                       8                  4

NAME             Metal1/PIN                   8                  25

Via1             PIN                          19                 0
Via1             LEFPIN                       19                 0
Via1             VIA                          19                 0

Metal2           NET,SPNET,PIN,LEFPIN,VIA     10                 0
Metal2           PIN,LEFPIN                   10                 2
Metal2           FILL                         10                 22
Metal2           LEFOBS                       10                 4

NAME             Metal2/PIN                   10                 25

Via2             PIN                          29                 0
Via2             LEFPIN                       29                 0
Via2             VIA                          29                 0

Metal3           NET,SPNET,PIN,LEFPIN,VIA     30                 0
Metal3           PIN,LEFPIN                   30                 2
Metal3           FILL                         30                 22
Metal3           LEFOBS                       30                 4

NAME             Metal3/PIN                   30                 25

Via3             PIN                          49                 0
Via3             LEFPIN                       49                 0
Via3             VIA                          49                 0

Metal4           NET,SPNET,PIN,LEFPIN,VIA     50                 0
Metal4           PIN,LEFPIN                   50                 2
Metal4           FILL                         50                 22
Metal4           LEFOBS                       50                 4

NAME             Metal4/PIN                   50                 25

TopVia1          PIN                          125                0
TopVia1          LEFPIN                       125                0
TopVia1          VIA                          125                0

TopMetal1        NET,SPNET,PIN,LEFPIN,VIA     126                0
TopMetal1        PIN,LEFPIN                   126                2
TopMetal1        FILL                         126                22
TopMetal1        LEFOBS                       126                4

NAME             TopMetal1/PIN                126                25

# Via4, Metal5, TopVia2, TopMetal2 not available in SG13CMOS5L PDK (M1-M4-TM1 stack)

COMP             ALL                          189                0

NAME             COMP                         63                 0

DIEAREA          ALL                          189                4
'''

    with open(output_path, 'w') as f:
        f.write(map_content)

    print(f"Generated {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate KLayout layer files from JSON database'
    )
    parser.add_argument(
        '--json', '-j',
        type=Path,
        help='Path to layer JSON database (default: layer_tracking/ihp-sg13cmos5l_layers.json)'
    )
    parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        help='Output directory for generated files (default: libs.tech/klayout/tech/)'
    )
    parser.add_argument(
        '--lyp-only',
        action='store_true',
        help='Generate only .lyp file'
    )
    parser.add_argument(
        '--lyt-only',
        action='store_true',
        help='Generate only .lyt file'
    )
    parser.add_argument(
        '--map-only',
        action='store_true',
        help='Generate only .map file'
    )

    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).parent
    pdk_root = script_dir.parent

    json_path = args.json or (pdk_root / "layer_tracking" / "ihp-sg13cmos5l_layers.json")
    output_dir = args.output_dir or (pdk_root / "libs.tech" / "klayout" / "tech")

    if not json_path.exists():
        print(f"Error: JSON database not found at {json_path}")
        print("Run parse_lyp_to_json.py first to create the database.")
        return 1

    print(f"Loading layer database from {json_path}")
    db = load_layer_database(json_path)

    # Determine which files to generate
    gen_all = not (args.lyp_only or args.lyt_only or args.map_only)

    if gen_all or args.lyp_only:
        generate_lyp(db, output_dir / "sg13cmos5l.lyp")

    if gen_all or args.lyt_only:
        generate_lyt(db, output_dir / "sg13cmos5l.lyt")

    if gen_all or args.map_only:
        generate_map(db, output_dir / "sg13cmos5l.map")

    print("\nGeneration complete!")
    return 0


if __name__ == "__main__":
    exit(main())
