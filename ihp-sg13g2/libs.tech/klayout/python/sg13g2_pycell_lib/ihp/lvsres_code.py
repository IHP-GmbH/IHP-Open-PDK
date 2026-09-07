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

__version__ = '$Revision: #3 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *

import math

class lvsres(DloGen):

    @classmethod
    def defineParamSpecs(self, specs): 
        # define parameters and default values   
        specs('layer', 'Metal1', 'Layer', ChoiceConstraint(['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']))
        specs('width', '5u', 'Width')
        specs('length', '1u', 'Length')
        specs('r', '1u', 'Resistance')
        
    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.length = self.params['length']
        self.width  = self.params['width']
        self.layer  = self.params['layer']

    def genLayout(self):
        #*************************************************************************
        #
        # Get parameter values
        #
        #*************************************************************************
        metLay = self.layer
        l = Numeric(self.length)*1e6
        w = Numeric(self.width)*1e6
        
        #*************************************************************************
        #
        # Cell Properties
        #
        #*************************************************************************
        dbReplaceProp(self, 'ivCellType', 'graphic')
        dbReplaceProp(self, 'viewSubType', 'maskLayoutParamCell')
        dbReplaceProp(self, 'instNamePrefix', 'R')
        dbReplaceProp(self, 'function', 'resistor')
        dbReplaceProp(self, 'pcellVersion', '$Revision: 1.0 $')
        
        #*************************************************************************
        #
        # Layer Definitions
        #
        #*************************************************************************
        MLayer = Layer(metLay, 'drawing')
        PinLayer = Layer(metLay, 'pin')
        RecLay = Layer(metLay, 'res')
        
        #*************************************************************************
        #
        # Device Specific Design Rule Definitions
        #
        #*************************************************************************
        # for legacy support will not calculte pin width take old fixed value
        pinWid = 0.2
        
        #*************************************************************************
        #
        # Main body of code
        #
        #*************************************************************************
        # do not broke old pcell set origin as was.
        body = dbCreateRect(self, MLayer, Box(0-l*0.5, 0, 0+l*0.5, w))
        # recognition layer
        body = dbCreateRect(self, RecLay, Box(0-l*0.5, 0, 0+l*0.5, w))
        resBbx = body.bbox
        dbCreateRect(self, MLayer, Box(resBbx.left-pinWid, resBbx.top, resBbx.right+pinWid, resBbx.bottom))
        
        # plus term
        MkPin(self, 'PLUS', 1, Box(resBbx.left, resBbx.bottom, resBbx.left-pinWid, resBbx.top), metLay)
	      # minus terminal
        MkPin(self, 'MINUS', 2, Box(resBbx.right, resBbx.top, resBbx.right+pinWid, resBbx.bottom), metLay)
