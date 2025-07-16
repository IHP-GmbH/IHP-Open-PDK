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
    
class pnpMPA(DloGen):

    Cell = 'pnpMPA'
    
    @classmethod
    def defineParamSpecs(self, specs):
        techparams = specs.tech.getTechParams()
        
        model      = techparams[self.Cell+'_model']
        defL       = techparams[self.Cell+'_defL']
        defW       = techparams[self.Cell+'_defW']
        minL       = techparams[self.Cell+'_minL']
        minW       = techparams[self.Cell+'_minW']
        
#ifdef KLAYOUT        
        specs('model', model, 'Model name')
        specs('Calculate', 'a', "Calculate", ChoiceConstraint(['a', 'w', 'l', 'w&l']))
        specs('w', defW, 'Width')
        specs('l', defL, 'Length')
        specs('a', eng_string(CbDiodeCalc('a', 0, Numeric(defL), Numeric(defW), 'pnpMPA'), 3), 'Area')
        specs('p', eng_string(CbDiodeCalc('p', 0, Numeric(defL), Numeric(defW), 'pnpMPA'), 3), 'Perimeter')
        specs('ac', '7.524p', 'Collector area')
        specs('pc', '11.16u', 'Collector perimeter')
        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')
        specs('region', ' ', 'Estimated operating region', ChoiceConstraint([' ', 'off', 'on']))
#else
        CDFVersion = techparams['CDFVersion']
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')
        
        specs('Calculate', 'a', "Calculate", ChoiceConstraint(['a', 'w', 'l', 'w&l']))
        specs('w', defW, 'Width')
        specs('l', defL, 'Length')
        specs('a', eng_string(CbDiodeCalc('a', 0, Numeric(defL), Numeric(defW), 'pnpMPA'), 3), 'Area')
        specs('p', eng_string(CbDiodeCalc('p', 0, Numeric(defL), Numeric(defW), 'pnpMPA'), 3), 'Perimeter')
        specs('ac', '7.524p', 'Collector area')
        specs('pc', '11.16u', 'Collector perimeter')
        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')
        specs('region', ' ', 'Estimated operating region', ChoiceConstraint([' ', 'off', 'on']))
#endif

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.l = params['l']
        self.w = params['w']

    def genLayout(self):
        self.grid = self.tech.getGridResolution()
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']
        
        l = self.l
        w = self.w

        hact = GridFix(Numeric(l)*5e5)
        wact = GridFix(Numeric(w)*5e5)
        Cnt_a = self.techparams['Cnt_a']
        Cnt_b = self.techparams['Cnt_b']
        Cnt_b1 = self.techparams['Cnt_b1']
        M1_c1 = self.techparams['M1_c1']
        pSD_c = self.techparams['pSD_c']
        
        w1m1 = wact-0.02
        h1m1 = hact-0.02
        wpsd = wact+0.21
        hpsd = hact+0.18
        w2act = wpsd+pSD_c
        h2act = hpsd+pSD_c
        dw2act = max(wact, 0.3)
        dh2act = 0.29
        w2m1 = w2act+0.02
        h2m1 = h2act+0.02
        dw2m1 = dw2act-0.04
        dh2m1 = dh2act-0.04
        wbulay = w2act+dw2act+0.05
        hbulay = h2act+dh2act+0.05
        wnwell = wbulay+0.26
        hnwell = hbulay+0.26
        w2psd = wnwell+0.5
        h2psd = hnwell+0.5
        d2psd = 0.75
        w3act = w2psd+0.2
        h3act = h2psd+0.2
        d3act = 0.35
        
        activLayer = Layer('Activ', 'drawing')        # 1
        contLayer  = Layer('Cont', 'drawing')         # 6
        metal1Layer = Layer('Metal1', 'drawing')      # 8
        pSdLayer = Layer('pSD', 'drawing')            # 14 
        nwellLayer = Layer('NWell', 'drawing')        # 31
        nBuLayer = Layer('nBuLay', 'drawing')         # 32
        textLayer = Layer('TEXT', 'drawing')          # 63
        
        dbCreateRect(self, activLayer, Box(-wact, -hact, wact, hact))
        dbCreateLabel(self, textLayer, Point(0, 0), 'PLUS', 'centerCenter', 'R90', Font.EURO_STYLE, min(wact, d3act*2))
        dbCreateLabel(self, textLayer, Point(-w2m1-dw2m1/2, 0), 'MINUS', 'centerCenter', 'R90', Font.EURO_STYLE, min(wact, d3act*2))
        dbCreateLabel(self, textLayer, Point(0, -(hnwell+h2psd)/2), 'pnpMPA', 'centerCenter', 'R0', Font.EURO_STYLE, h2psd-hnwell)
        dbCreateRect(self, pSdLayer, Box(-wpsd, -hpsd, wpsd, hpsd))
        _xl = -w1m1
        _xh = w1m1
        _yl = -h1m1
        _yh = h1m1
        _ox = M1_c1
        _oy = M1_c1
        _ws = Cnt_a
        _ds = Cnt_b
        vg4 = (Cnt_a+Cnt_b)*4+Cnt_a+_ox*2
        if _xh-_xl >= vg4 and _yh-_yl >= vg4 :
            _ds = Cnt_b1
            
        contactArray(self, metal1Layer, contLayer, _xl, _yl, _xh, _yh, _ox, _oy, _ws, _ds)
        id1 = dbCreateRect(self, activLayer, Box(-w2act, -h2act, w2act, h2act))
        id2 = dbCreateRect(self, activLayer, Box(-w2act-dw2act, -h2act-dh2act, w2act+dw2act, h2act+dh2act))
        dbLayerXor(activLayer, id1, id2)
        id1.destroy()
        id2.destroy()
        id1 = dbCreateRect(self, metal1Layer, Box(-w2m1, -h2m1, w2m1, h2m1))
        id2 = dbCreateRect(self, metal1Layer, Box(-w2m1-dw2m1, -h2m1-dh2m1, w2m1+dw2m1, h2m1+dh2m1))
        dbLayerXor(metal1Layer, id1, id2)
        id1.destroy()
        id2.destroy()
        
        _xl = -w2m1-dw2m1
        _xh = -w2m1
        _yl = -h2m1
        _yh = h2m1
        if _xh-_xl >= vg4 and _yh-_yl >= vg4 :
            _ds = Cnt_b1
            
        contactArray(self, metal1Layer, contLayer, _xl, _yl, _xh, _yh, _ox, _oy, _ws, _ds)
        _xl = w2m1
        _xh = w2m1+dw2m1
        contactArray(self, metal1Layer, contLayer, _xl, _yl, _xh, _yh, _ox, _oy, _ws, _ds)
        dbCreateRect(self, nBuLayer, Box(-wbulay, -hbulay, wbulay, hbulay))
        dbCreateRect(self, nwellLayer, Box(-wnwell, -hnwell, wnwell, hnwell))
        
        # Ring
        id1 = dbCreateRect(self, pSdLayer, Box(-w2psd, -h2psd, w2psd, h2psd))
        id2 = dbCreateRect(self, pSdLayer, Box(-w2psd-d2psd, -h2psd-d2psd, w2psd+d2psd, h2psd+d2psd))
        dbLayerXor(pSdLayer, id1, id2)
        id1.destroy()
        id2.destroy()
        id1 = dbCreateRect(self, activLayer, Box(-w3act, -h3act, w3act, h3act))
        id2 = dbCreateRect(self, activLayer, Box(-w3act-d3act, -h3act-d3act, w3act+d3act, h3act+d3act))
        dbLayerXor(activLayer, id1, id2)
        id1.destroy()
        id2.destroy()
        
        # Ring Metal
        MetT = True
        MetB = True
        MetL = True
        MetR = True
        _ds = Cnt_b
        _ox = 0.095
        idtie = 0
        
        if MetT :
            contactArray(self, metal1Layer, contLayer, -w3act-d3act, h3act, w3act+d3act, h3act+d3act, _ox, _oy, _ws, _ds)
            if idtie == 0 :
                idtie = dbCreateRect(self, Layer('Metal1', 'pin'), Box(-w3act-d3act, h3act, w3act+d3act, h3act+d3act))
                dbCreateLabel(self, textLayer, Point(0, h3act+d3act/2), 'TIE', 'centerCenter', 'R0', Font.EURO_STYLE, d3act*2)
                
            
        if MetB :
            contactArray(self, metal1Layer, contLayer, -w3act-d3act, -h3act-d3act, w3act+d3act, -h3act, _ox, _oy, _ws, _ds)
            if idtie == 0 :
                idtie = dbCreateRect(self, Layer('Metal1', 'pin'), Box(-w3act-d3act, -h3act-d3act, w3act+d3act, -h3act))
                dbCreateLabel(self, textLayer, Point(0, -h3act-d3act/2), 'TIE', 'centerCenter', 'R0', Font.EURO_STYLE, d3act*2)
                
            
        _oy = 0.085
        if MetL :
            contactArray(self, metal1Layer, contLayer, -w3act-d3act, -h3act, -w3act, h3act, _ox, _oy, _ws, _ds)
            if idtie == 0 :
                idtie = dbCreateRect(self, Layer('Metal1', 'pin'), Box(-w3act-d3act, -h3act, -w3act, h3act))
                dbCreateLabel(self, textLayer, Point(-w3act-d3act/2, 0), 'TIE', 'centerCenter', 'R90', Font.EURO_STYLE, d3act*2)
                
            
        if MetR :
            contactArray(self, metal1Layer, contLayer, w3act, -h3act, w3act+d3act, h3act, _ox, _oy, _ws, _ds)
            if idtie == 0 :
                idtie = dbCreateRect(self, Layer('Metal1', 'pin'), Box(w3act, -h3act, w3act+d3act, h3act))
                dbCreateLabel(self, textLayer, Point(w3act+d3act/2, 0), 'TIE', 'centerCenter', 'R90', Font.EURO_STYLE, d3act*2)
                
            
        if idtie != 0 :
            dbCreatePin(self, 'TIE', idtie)
            
        id1 = dbCreateRect(self, Layer('Metal1', 'pin'), Box(-w1m1, -h1m1, w1m1, h1m1))
        dbCreatePin(self, 'PLUS', id1)
        id1 = dbCreateRect(self, Layer('Metal1', 'pin'), Box(-w2m1-dw2m1, -h2m1, -w2m1, h2m1))
        dbCreatePin(self, 'MINUS', id1)
