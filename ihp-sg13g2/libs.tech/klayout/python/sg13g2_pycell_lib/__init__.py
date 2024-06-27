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
import sys
import inspect
import re
import importlib

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
        'dpantenna_code',
        'via_stack_code'

]

class PyCellLib(pya.Library):
    def __init__(self):
        self.description = "IHP SG13G2 Pcells"

        tech = Tech.get('SG13_dev')

        for moduleName in moduleNames:
            module = importlib.import_module(f"{__name__}.ihp." + moduleName)

            match = re.fullmatch(r'^(\S+)_code$', moduleName)
            if match:
                func = getattr(module, f"{match.group(1)}")
                self.layout().register_pcell(match.group(1), PCellWrapper(func(), tech))

        self.register("SG13_dev")

# instantiate and register the library
PyCellLib()

