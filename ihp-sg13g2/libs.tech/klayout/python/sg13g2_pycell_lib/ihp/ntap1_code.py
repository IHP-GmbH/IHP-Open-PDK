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

__version__ = '$Revision: #3 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *

import math

class ntap1(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        # define parameters and default values
        techparams = specs.tech.getTechParams()
        
        minL       = techparams['ntap1_minLW' ]
        minW       = techparams['ntap1_minLW' ]
        defL       = techparams['ntap1_defL' ]
        defW       = techparams['ntap1_defW']
        defA       = Numeric(defL)*Numeric(defW)
        defP       = 2*Numeric(defL)+2*Numeric(defW)
        
        r = eng_string(CbTapCalc('R', 0.0, Numeric(defL), Numeric(defW), 'ntap1'), 3)
                
#ifdef KLAYOUT
        specs('Calculate', 'R,A', 'Calculate', ChoiceConstraint(['R,A', 'w,A', 'l,A', 'w,l,A', 'w,l,R', 'w,R', 'l,R']))
        specs('R', r, 'R')
        specs('w', defW, 'Width')
        specs('l', defL, 'Length')
        specs('A', str(defA), 'Area')
        specs('Perim', str(defP), 'Perimeter')
        specs('Rspec', '0.980n', 'Rspec [R*m^2]')
#else
        CDFVersion = techparams['CDFVersion' ]
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('Calculate', 'R,A', 'Calculate', ChoiceConstraint(['R,A', 'w,A', 'l,A', 'w,l,A', 'w,l,R', 'w,R', 'l,R']))
        specs('R', r, 'R')
        specs('w', defW, 'Width')
        specs('l', defL, 'Length')
        specs('A', str(defA), 'Area')
        specs('Perim', str(defP), 'Perimeter')
        specs('Rspec', '0.980n', 'Rspec [R*m^2]')
        specs('Wmin', minL, 'Wmin')
        specs('Lmin', minW, 'Lmin')
        specs('m', '1', 'Multiplier')
#endif

    def setupParams(self, params):
        # process parameter values entered by user
        self.w = Numeric(params['w'])
        self.l = Numeric(params['l'])

    def genLayout(self):
        self.grid = self.tech.getGridResolution()
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']      # for rounding purposes
        
        #*************************************************************************
        #*
        #* Layer Definitions
        #*
        #*************************************************************************
        metal1_layer = Layer('Metal1')
        metal1_layer_pin = Layer('Metal1','pin')
        ndiff_layer = Layer('Activ')
        cont_layer = Layer('Cont')
        well_layer = Layer('NWell')
        well_layer_pin = Layer('NWell', 'pin')
        bulay_layer = Layer('nBuLay')
        textlayer = Layer('TEXT', 'drawing')
        
        #*************************************************************************
        #*
        #* Generic Design Rule Definitions
        #*
        #*************************************************************************
        cont_size = self.techparams['Cnt_a']
        cont_dist = self.techparams['Cnt_b']
        cont_diff_over = self.techparams['Cnt_c']
        cont_metal_over = self.techparams['M1_c']
        cont_metal_endcap = self.techparams['M1_c1']
        ndiff_over = self.techparams['NW_e']          # Minimum NWell enclosure of NWell tie surrounded entirely by NWell in N+Activ1
        wmin = Numeric(self.techparams['ntap1_minLW'])
        lmin = Numeric(self.techparams['ntap1_minLW'])
        
        # ntap1 gets 2 Pins -> value must be 3
        dbReplaceProp(self, 'pin#', 3)
        
        #*************************************************************************
        #*
        #* Main body of code
        #*
        #*************************************************************************    
        w = self.w*1e6;
        l = self.l*1e6;
        
        # cheking for min w/l -> should be defined elsewhere
        ########################################
        if w < wmin-self.epsilon :
            w = wmin
            hiGetAttention()
            print('Width < '+str(wmin))
            
        if l < lmin-self.epsilon :
            l = lmin
            hiGetAttention()
            print('Length < '+str(lmin))
        ########################################
        
        bBox = DrawContArray(self, cont_layer, Box(0, 0, w, l), cont_size, cont_dist, cont_diff_over)
        
        # change bBox to size of Metal1 drawing
        bBox = ResizeBBox(bBox, cont_metal_over)
        dbCreateRect(self, metal1_layer,     Box(bBox.left, bBox.bottom - cont_metal_endcap, bBox.right, bBox.top + cont_metal_endcap)) 
        dbCreateRect(self, metal1_layer_pin, Box(bBox.left, bBox.bottom - cont_metal_endcap, bBox.right, bBox.top + cont_metal_endcap)) 
        
        # create Pin
        MkPin(self, 'TIE', 1, Box(bBox.left, bBox.bottom, bBox.right, bBox.top), metal1_layer_pin)
        
        dbCreateRect(self, ndiff_layer, Box(0, 0, w, l))
        dbCreateRect(self, well_layer_pin, Box(0, 0, w, l))
        dbCreateRect(self, well_layer, Box(-ndiff_over, -ndiff_over, w+ndiff_over, l+ndiff_over))
        dbCreateRect(self, bulay_layer, Box(-ndiff_over, -ndiff_over, w+ndiff_over, l+ndiff_over))

        MkPin(self, 'WELL', 2, Box(0, 0, w, l), well_layer)
        dbCreateLabel(self, textlayer, Point(w/2, 0.01), 'well', 'centerCenter', 'R0', Font.EURO_STYLE, 0.15)
        dbCreateLabel(self, well_layer, Point(w/2, 0.01), 'well', 'centerCenter', 'R0', Font.EURO_STYLE, 0.15)    
