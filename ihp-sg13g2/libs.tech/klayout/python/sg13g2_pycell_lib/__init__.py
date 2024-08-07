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

import pya
import os
import sys

from cni.dlo import Tech
from cni.dlo import PCellWrapper

# Creates the SG13_dev technology
from .sg13_tech import *

import pya

import os
import io
import sys
import inspect
import re
import importlib
import pathlib
import tempfile

moduleNames = [
        'nmos_code',
        'nmosHV_code',
        'pmos_code',
        'pmosHV_code',
        'cmim_code',
        'rsil_code',
        'rhigh_code',
        'rppd_code',
        'sealring_code',
        'npn13G2_base_code',
        'npn13G2_code',
        'npn13G2L_code',
        'npn13G2V_code',
        'inductor2_code',
        'inductor2_sc_code',
        'inductor2_sp_code',
        'inductor3_code',
        'inductor3_sc_code',
        'inductor3_sp_code',
        'dantenna_code',
        'dpantenna_code'

]


"""
Support for 'conditional compilation' in a C-style manner of PyCell code:

#ifdef name
    ...some_code...
#else
    ...some_other_code...
#endif

If an environment variable 'name' can be found the #ifdef-block will be executed, the #else-block
otherwise
"""

class PyCellLib(pya.Library):
    def __init__(self):
        self.description = "IHP SG13G2 Pcells"

        tech = Tech.get('SG13_dev')

        module = importlib.import_module(f"{__name__}.ihp.pypreprocessor")
        preProcessor = getattr(module, "preprocessor")

        for moduleName in moduleNames:
            defines = []
            definesSet = []

            modulePath = os.path.join(os.path.dirname(__file__), 'ihp', f"{moduleName}.py")
            moduleFile = io.open(modulePath, 'r', encoding=sys.stdin.encoding)

            try:
                for line in moduleFile:
                    match = re.match(r'^#ifdef\s+(\w+)', line)
                    if match:
                        define = match.group(1)
                        if define not in defines:
                            defines.append(define)

            finally:
                moduleFile.close()

            for define in defines:
                if os.getenv(define) is not None:
                    definesSet.append(define)

            modulePreProcPath = os.path.join(tempfile.gettempdir(), f"{moduleName}_pre.py")

            pyPreProcessor = preProcessor(modulePath, modulePreProcPath, definesSet, removeMeta=False, resume=True, run=True)
            pyPreProcessor.parse()

            spec = importlib.util.spec_from_file_location(f"{__name__}.ihp.{moduleName}", modulePreProcPath)
            module = importlib.util.module_from_spec(spec)
            sys.modules[moduleName] = module
            spec.loader.exec_module(module)

            match = re.fullmatch(r'^(\S+)_code$', moduleName)
            if match:
                func = getattr(module, f"{match.group(1)}")
                self.layout().register_pcell(match.group(1), PCellWrapper(func(), tech))

            os.remove(modulePreProcPath)

        self.register("SG13_dev")

# instantiate and register the library
PyCellLib()

