#!/usr/bin/env python3

########################################################################
#
# Copyright 2024 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

"""Script that abuts every cell against every cell from a specified GDS in different orientations.
How to run:
> check_abutment.py <gds_file>
"""

import sys
import os

import numpy as np
import gdstk

UNIT_Y = np.float64(3.780)
UNIT_X = np.float64(0.480)

SKIP_CELLS = []

def get_cell_width(cell):
    return cell.get_polygons(layer=189, datatype=4)[0].bounding_box()[1][0] # prBoundary.bnd (189,4)

def get_cell_height(cell):
    return cell.get_polygons(layer=189, datatype=4)[0].bounding_box()[1][1]

def main(self, lib_gds):
    # Load library
    lib = gdstk.read_gds(lib_gds)

    # Create test library
    test_lib = gdstk.Library()
    test_top_area = test_lib.new_cell('sg13g2_stdcell_top')

    # Copy all cells
    for cell_tst in lib.cells:
        # Add the cell to our test library
        test_lib.add(cell_tst)

    # Scan all cells
    xt = 0.0

    for cell_tst in lib.cells:
        # Create test area
        test_area = test_lib.new_cell('abut_' + cell_tst.name)

        # Width of current cell
        width_tst = get_cell_width(cell_tst)

        # Test against all other cells
        y = 0

        for cell_nxt in lib.cells:
            # Get the cell width
            height_nxt = get_cell_height(cell_nxt)
            width_nxt  = get_cell_width(cell_nxt)

            # Use self
            if cell_nxt.name == cell_tst.name:
                cell_nxt = cell_tst

            # Refuse some cells
            if (abs(height_nxt - UNIT_Y) > 1e-3) or cell_nxt.name in SKIP_CELLS:
                print(f"[!] Skipped {cell_nxt.name}")
                continue

            # Add reference
            # First row
            test_area.add(gdstk.Reference(
                cell_nxt,
                origin = (-width_nxt, 2 * y * UNIT_Y),
            ))

            test_area.add(gdstk.Reference(
                cell_tst,
                origin = (0.0, 2 * y * UNIT_Y),
            ))

            test_area.add(gdstk.Reference(
                cell_nxt,
                origin = (width_tst, 2 * y * UNIT_Y),
            ))

            # Second row
            test_area.add(gdstk.Reference(
                cell_nxt,
                origin = (0.0, (2 * y + 2) * UNIT_Y),
                rotation = np.pi,
            ))

            test_area.add(gdstk.Reference(
                cell_tst,
                origin = (0.0, (2 * y + 2) * UNIT_Y),
                x_reflection = True,
            ))

            test_area.add(gdstk.Reference(
                cell_nxt,
                origin = (width_tst + width_nxt, (2 * y + 2) * UNIT_Y),
                rotation = np.pi,
            ))

            # Next cell
            y += 1

        # Add to top test cell
        test_top_area.add(gdstk.Reference(
            test_area,
            origin = (xt, 0.0),
        ))

        xt += 50.0

        # Save result
        script_location = os.path.dirname(__file__)
        output_gds = script_location + '/../drc/special/' + 'sg13g2_stdcell_abutment.gds'
        test_lib.write_gds(output_gds)
        
    print('Output GDS: ' + output_gds)        

if __name__ == '__main__':
    main(*sys.argv)
