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

from ...cni.dlogen import Dlo


class via_stack(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        # define parameters and default values
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Bottom_layer', 'b_layer', 'Bottom layer', ChoiceConstraint(['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5']))
        specs('Top_layer', 't_layer', 'Top layer', ChoiceConstraint(['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5']))

        specs('Calculate', 'bottom_num', 'Calculate', ChoiceConstraint(['top_size', 'bottom_num', 'top_num', 'bottom_num']))

        #resistance = CbResCalc('R', 0, defL, defW, defB, defPS, 'rsil')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.b_layer = Numeric(params['b_layer'])
        self.t_layer = Numeric(params['t_layer'])

    def genLayout(self):

        b_layer = self.b_layer
        t_layer = self.t_layer

        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']
        self.grid = self.tech.getGridResolution()         # needed for Dogbone

        Cell = self.__class__.__name__

        metal1_layer = 'Metal1'
        metal2_layer = 'Metal2'
        metal3_layer = 'Metal3'
        metal4_layer = 'Metal4'

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

        v2_size = techparams['V2_a']
        v2_sep1 = techparams['V2_b']
        v2_sep2 = techparams['V2_b1']
        v2_enc = techparams['V2_c1']

        v3_size = techparams['V3_a']
        v3_sep1 = techparams['V3_b']
        v3_sep2 = techparams['V3_b1']
        v3_enc = techparams['V3_c1']

        v4_size = techparams['V4_a']
        v4_sep1 = techparams['V4_b']
        v4_sep2 = techparams['V4_b1']
        v4_enc = techparams['V4_c1']

        grid = techparams['grid']
        
        #*************************************************************************
        #*
        #* Device Specific Design Rule Definitions
        #*
        #************************************************************************

        
        #*************************************************************************
        #*
        #* Main body of code
        #*
        #************************************************************************
        internalCode = True
        gridnumber = 0.0
        contoverlay = 0.0

        columns = 2
        rows = 2

        if (b_layer == 'Metal1'):

            via_size = v1_size
            via_sep = v1_sep1
            dbCreateRect(self, b_layer, Box(-50, -50, columns * (via_size) + (columns - 1) * via_sep + 50, rows * (via_size) + (rows - 1) * via_sep + 50))


