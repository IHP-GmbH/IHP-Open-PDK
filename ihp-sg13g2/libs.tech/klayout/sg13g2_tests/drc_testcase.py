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

from __future__ import annotations
from dataclasses import dataclass, field
import os
from pathlib import Path
import subprocess
from typing import *

import pya



def drc_script_path() -> str:
    directory_containing_this_script = os.path.realpath(os.path.dirname(__file__))
    parent_directory = os.path.dirname(directory_containing_this_script)
    script_path = os.path.join(parent_directory, 'tech', 'drc', 'run_drc.py')
    return script_path


@dataclass 
class DRCViolation:
    rule_name: str
    count: int
    description: str


@dataclass 
class DRCResult:
    testcase: DRCTestCase
    report_dbs: List[pya.RdbDatabase] = field(default_factory=list)
    violations: List[DRCViolation] = field(default_factory=list)
    
    def passed(self) -> bool:
        return len(self.violations) == 0

    def violated_rule_names(self) -> List[str]:
        return [v.rule_name for v in self.violations]


@dataclass
class DRCTestCase:
    name: str
    top_cell: pya.Cell
    density_checks: bool = True
    offgrid_checks: bool = True
    feol_checks: bool = True
    beol_checks: bool = True
    antenna_checks: bool = False
    blacklist_rules: List[str] = field(default_factory=list)   # like ['M3.b', ]

    def is_blacklisted(self, category: pya.RdbCategory) -> bool:
        if category.name() in self.blacklist_rules:
            return True
        return False

    def run(self,
            run_dir_base: str | Path, 
            layout_path: str | Path) -> DRCResult:
        fs_test_name = self.name.replace(' ', '_').replace('/', '-').lower()
        run_dir = Path(run_dir_base).resolve() / fs_test_name
        
        layout_path = Path(layout_path).resolve()
        
        args = [
            '--run_dir', str(run_dir),
            '--topcell', self.top_cell.name,
            '--path', str(layout_path),
        ]
        
        if not self.feol_checks:
            args += ['--no_feol']

        if not self.beol_checks:
            args += ['--no_beol']
        
        if not self.density_checks:
            args += ['--no_density']
        
        if not self.offgrid_checks:
            args += ['--no_offgrid']
        
        if self.antenna_checks:
            args += ['--antenna']
        
        cmd_args = ['python3', drc_script_path()] + args
        print(f"Calling subprocess with: {' '.join(cmd_args)}")
        
        result = subprocess.run(cmd_args)
        print(f"Script terminated with exit code {result.returncode}")
        
        result = DRCResult(self)
        
        for rdb_file in run_dir.glob('*.lyrdb'):
            print(rdb_file)
            
            rdb = pya.ReportDatabase()
            rdb.load(str(rdb_file))
            
            result.report_dbs.append(rdb)
            
            for cat in rdb.each_category():
                if cat.num_items() == 0:
                    continue
                
                if self.is_blacklisted(cat):
                    continue
                
                print(f"ERROR: [{self.name}] {cat.name()} ({cat.num_items()} violations) … {cat.description}")
                result.violations.append(DRCViolation(cat.name(), cat.num_items(), cat.description))

        return result
        