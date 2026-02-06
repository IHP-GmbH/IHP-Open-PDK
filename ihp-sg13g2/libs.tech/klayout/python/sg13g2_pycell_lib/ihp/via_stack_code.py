########################################################################
#
# Copyright 2023 IHP PDK Authors
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

__version__ = '$Revision: #3 $'

from cni.dlo import *
from .geometry import *
from .thermal import *
from .utility_functions import *

import math

from ..sg13_tech_info import *


class via_stack(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        # define parameters and default values
        techparams = specs.tech.getTechParams()
        
#ifdef KLAYOUT
#else
        CDFVersion = techparams['CDFVersion']
        specs('cdf_version', CDFVersion, 'CDF Version')
#endif

        specs('b_layer', 'Metal1', 'Bottom layer', ChoiceConstraint(['Activ', 'GatPoly', 'Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']))
        specs('t_layer', 'Metal2', 'Top layer', ChoiceConstraint(['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']))
        specs('vn_columns', 2, 'Via_n Columns')
        specs('vn_rows', 2, 'Via_n Rows')
        specs('vt1_columns', 1, 'Via_t1 Columns')
        specs('vt1_rows', 1, 'Via_t1 Rows')
        specs('vt2_columns', 1, 'Via_t2 Columns')
        specs('vt2_rows', 1, 'Via_t2 Rows')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.b_layer = params['b_layer']
        self.t_layer = params['t_layer']
        self.vn_columns = params['vn_columns']
        self.vn_rows = params['vn_rows']
        self.vt1_columns = params['vt1_columns']
        self.vt1_rows = params['vt1_rows']
        self.vt2_columns = params['vt2_columns']
        self.vt2_rows = params['vt2_rows']

    def genLayout(self):
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']
        self.grid = self.tech.getGridResolution()         # needed for Dogbone
        
        Cell = self.__class__.__name__

        textlayer = 'TEXT'

        #*************************************************************************
        #*
        #* Generic Design Rule Definitions
        #*
        #************************************************************************

        epsilon = techparams['epsilon1']

        self.tech_info = TechInfo.instance()
        
        #*************************************************************************
        #*
        #* Device Specific Design Rule Definitions
        #*
        #************************************************************************

        b_layer_name = self.b_layer
        t_layer_name = self.t_layer

        vn_columns = self.vn_columns
        vn_rows = self.vn_rows
        vt1_columns = self.vt1_columns
        vt1_rows = self.vt1_rows
        vt2_columns = self.vt2_columns
        vt2_rows = self.vt2_rows

        #*************************************************************************
        #*
        #* Main body of code
        #*
        #************************************************************************

        # NOTE: device_layers are mutual exclusive
        if b_layer_name in self.tech_info.device_layer_names:
            if t_layer_name in self.tech_info.device_layer_names:
                # this is not allowed, coerce top layer to Metal1
                t_layer_name = self.tech_info.first_metal_layer_name
        
        b_layer = self.tech_info.layer_by_name(b_layer_name)
        t_layer = self.tech_info.layer_by_name(t_layer_name)

        def nx_ny_for_via(via: ViaInfo) -> Tuple[int, int]:
            if via.cut.name == 'TopVia1':
                return self.vt1_columns, self.vt1_rows
            elif via.cut.name == 'TopVia2':
                return self.vt2_columns, self.vt2_rows
            else:
                return self.vn_columns, self.vn_rows
        
        vias = self.tech_info.get_vias(b_layer, t_layer)
        prev_via_array: Optional[ViaArrayInfo] = None
        
        for i, via in enumerate(vias):
            nx, ny = nx_ny_for_via(via)
            via_array = ViaArrayInfo(via, nx, ny)
            
            for box in via_array.each_via_box():
                dbCreateRect(self, via.cut.name, box)
            
            dbCreateRect(self, via.bottom.name, via_array.bottom_metal_box(prev_via_array))
            
            prev_via_array = via_array
        
        dbCreateRect(self, prev_via_array.via.top.name, prev_via_array.top_metal_box())
