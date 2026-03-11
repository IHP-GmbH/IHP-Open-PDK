########################################################################
#
# Copyright 2025 IHP PDK Authors
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

#
# To test this code, 
#   - Either run it in the KLayout Macro Development environment
#   - Or use the shell comamnd (bash syntax):
#       (in the location of this file):
#       KLAYOUT_PATH=$(pwd)/.. klayout -zz -r native_pcell_viatest.py
#

import os
from pathlib import Path
import sys
from typing import *

import pya


try:
    from drc_testcase import (DRCTestCase, DRCResult)
except ModuleNotFoundError:
    directory_containing_this_script = os.path.realpath(os.path.dirname(__file__))
    sys.path.append(directory_containing_this_script)
    from drc_testcase import (DRCTestCase, DRCResult)


NATIVE_LIB_NAME = 'SG13_native_pcell_lib'
TECH_NAME = 'sg13g2'


def run_drc_testcase(layout_path: str | Path, testcase: DRCTestCase) -> DRCResult:
    return testcase.run(run_dir_base="native_pcell_test_run_dir", layout_path=layout_path)


def test_library_registered():
    assert NATIVE_LIB_NAME in pya.Library.library_names()
    assert pya.Library.library_by_name(NATIVE_LIB_NAME, TECH_NAME) is not None


def add_cell_and_instance(layout: pya.Layout, 
                          pcell_name: str,
                          parent_cell: pya.Cell, 
                          params: Dict[str, Any],
                          position: pya.DVector) -> pya.DCellInstArray:
    cell = layout.create_cell(pcell_name, NATIVE_LIB_NAME, params)
    inst = pya.DCellInstArray(cell, pya.DTrans(position))
    parent_cell.insert(inst)
    return inst


def add_via_testcases(layout: pya.Layout, 
                      top_cell: pya.Cell, 
                      y_offset: float,
                      testcases: List[DRCTestCase]) -> float:
    x_offset = 0.0
    max_y = 0.0

    region = pya.Region()

    from sg13g2_pycell_lib.sg13_tech_info import TechInfo
    via_names = [via.name for via in TechInfo.instance().vias]
    for via in via_names:
        for nx, ny in ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (1, 2), (4, 2), (5, 2), (1, 4), (2, 4), (2, 5)):
            inst = add_cell_and_instance(
                layout=layout, 
                pcell_name='Via',
                parent_cell=top_cell, 
                params={'via': via, 'nx': nx, 'ny': ny},
                position=pya.DVector(x_offset, y_offset)                
            )
            bbox = inst.bbox(layout)
            x_offset = bbox.right + bbox.width() / 2 + 5.0
            max_y = max(max_y, bbox.top + bbox.height() / 2 + 4)
        y_offset = max_y
        x_offset = 0.0
        max_height = 0.0
        
    testcases.append(
        DRCTestCase(name='Via Tests',
                    top_cell=top_cell, 
                    density_checks=False,
                    offgrid_checks=True,
                    blacklist_rules=['LU.b', 'Act.d', 'M1.d', 'M2.d', 'M3.d', 'M4.d', 'M5.d',])
    )
    
    return max_y


def create_testcases(layout: pya.Layout) -> List[DRCTestCase]:
    testcases = []

    y_offset = 0

    top_cell_via = layout.create_cell('Via')
    y_offset = add_via_testcases(layout, top_cell_via, y_offset, testcases)
    
    return testcases

    
if __name__ == "__main__":
    output_path = 'native_pcell_test.gds.gz'
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"Old layout {output_path} has been deleted")
    
    test_library_registered()

    layout = pya.Layout()
    layout.technology_name = TECH_NAME
    
    drc_testcases = create_testcases(layout)

    layout.write(output_path)
    print(f"IHP native KLayout pcell layout written to: {output_path}")
    
    passed_tests = []
    failed_tests = []
    
    for testcase in drc_testcases:
        print(f"\n[{testcase.name}] Running DRC checks …")
        
        result = run_drc_testcase(output_path, testcase)
        
        if result.passed():
            passed_tests.append(result)
        else:
            failed_tests.append(result)
        print(f"\n")
    
    if len(failed_tests) == 0:
        print(f"PASS: {len(passed_tests)} of {len(drc_testcases)} testcases passed")
        sys.exit(0)
    else:
        print(f"FAIL: {len(failed_tests)} of {len(drc_testcases)} testcases failed:")
        for result in failed_tests:
            failed_rules = result.violated_rule_names()
            print(f"\t❌ {result.testcase.name} ({', '.join(failed_rules)})")
        sys.exit(1)
    