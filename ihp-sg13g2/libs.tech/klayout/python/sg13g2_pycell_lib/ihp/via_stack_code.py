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

        specs('b_layer', 'Metal1', 'Bottom layer', ChoiceConstraint(['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']))
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

        b_layer = self.b_layer
        t_layer = self.t_layer

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

        v1_size = techparams['V1_a']
        v1_sep1 = techparams['V1_b']
        v1_sep2 = techparams['V1_b1']
        v1_enc = techparams['V1_c1']

        vn_size = techparams['Vn_a']
        vn_sep1 = techparams['Vn_b']
        vn_sep2 = techparams['Vn_b1']
        vn_enc = techparams['Vn_c1']

        Topvia1_size = techparams['TV1_a']
        TopVia1_sep = techparams['TV1_b']
        Topvia1_enc_met5 = techparams['TV1_c']
        Topvia1_enc_top1 = techparams['TV1_d']

        Topvia2_size = techparams['TV2_a']
        TopVia2_sep = techparams['TV2_b']
        Topvia2_enc_top1 = techparams['TV2_c']
        Topvia2_enc_top2 = techparams['TV2_d']

        TopMetal1_min = techparams['TM1_a']
        TopMetal2_min = techparams['TM2_a']
        #*************************************************************************
        #*
        #* Device Specific Design Rule Definitions
        #*
        #************************************************************************

        vn_columns = self.vn_columns
        vn_rows = self.vn_rows
        vt1_columns = self.vt1_columns
        vt1_rows = self.vt1_rows
        vt2_columns = self.vt2_columns
        vt2_rows = self.vt2_rows

        metal_layers = ['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']
        via_layers = ['Via1', 'Via2', 'Via3', 'Via4', 'TopVia1', 'TopVia2']
        
        #*************************************************************************
        #*
        #* Main body of code
        #*
        #************************************************************************

        idx_b = metal_layers.index(b_layer)
        idx_t = metal_layers.index(t_layer)
        if idx_b > idx_t:
            idx_b, idx_t = idx_t, idx_b
        stack_layers = metal_layers[idx_b:idx_t+1]
        
        for layer in stack_layers:

            #pre-procesing
            if layer == 'Metal1':
                columns = vn_columns
                rows = vn_rows
                via_size = v1_size
                via_sep = v1_sep1 if (columns<4 and rows<4) else v1_sep2
                via_enc = v1_enc
                w_x = (columns * via_size + (columns - 1) * via_sep)
                w_y = (rows * via_size + (rows - 1) * via_sep)

            elif layer == 'TopMetal1':
                via_size = Topvia1_size
                via_sep = TopVia1_sep
                via_enc = Topvia1_enc_met5
                columns = vt1_columns
                rows = vt1_rows
                w_x = (columns * via_size + (columns - 1) * via_sep)
                w_y = (rows * via_size + (rows - 1) * via_sep)
                if "Metal5" in stack_layers:
                    dbCreateRect(self, 'Metal5', Box(-via_enc-w_x/2, -via_enc-w_y/2, w_x/2 + via_enc, w_y/2 + via_enc))
                via_enc = Topvia1_enc_top1

            elif layer == 'TopMetal2':
                via_size = Topvia2_size
                via_sep = TopVia2_sep
                via_enc = Topvia2_enc_top1
                columns = vt2_columns
                rows = vt2_rows
                w_x = (columns * via_size + (columns - 1) * via_sep)
                w_y = (rows * via_size + (rows - 1) * via_sep)
                dbCreateRect(self, 'TopMetal1', Box(-via_enc-w_x/2, -via_enc-w_y/2, w_x/2+via_enc, w_y/2+via_enc))
                via_enc = Topvia2_enc_top2

            else:
                columns = vn_columns
                rows = vn_rows
                via_size = vn_size
                via_sep = vn_sep1 if (columns<4 and rows<4) else vn_sep2
                via_enc = vn_enc
                w_x = (columns * via_size + (columns - 1) * via_sep)
                w_y = (rows * via_size + (rows - 1) * via_sep)

            #metal draw
            if layer == 'TopMetal1':
                if columns * via_size + (columns - 1) * 2 * via_sep < TopMetal1_min:
                    via_enc = (TopMetal1_min - Topvia1_size)/2
            elif layer == 'TopMetal2':
                if columns * via_size + (columns - 1) * 2 * via_sep < TopMetal2_min:
                    via_enc = (TopMetal2_min - Topvia2_size) / 2

            dbCreateRect(self, layer, Box(-via_enc-w_x/2, -via_enc-w_y/2, w_x/2 + via_enc, w_y/2 + via_enc))

            #via draw
            if layer != b_layer:
                via_layer = via_layers[metal_layers.index(layer)-1]
                for i in range(columns):
                    x0 = i * via_sep + i * via_size - w_x/2
                    for j in range(rows):
                        y0 = j * via_sep + j * via_size - w_y/2
                        dbCreateRect(self, via_layer, Box(x0, y0, x0 + via_size, y0 + via_size))
