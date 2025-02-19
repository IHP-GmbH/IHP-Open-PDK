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

class rfcmim(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        techparams = specs.tech.getTechParams()

        model      = techparams['rfcmim_model']
        minLW      = techparams['rfcmim_minLW']
        maxLW      = techparams['rfcmim_maxLW']
        defLW      = techparams['rfcmim_defLW']
        caspec     = techparams['rfcmim_caspec']
        cmax       = eng_string(CbCapCalc('C', 0, Numeric(maxLW), Numeric(maxLW), 'rfcmim'))
        
        C = CbCapCalc('C', 0, Numeric(defLW), Numeric(defLW), 'rfcmim')
        
#ifdef KLAYOUT
        specs('Calculate', 'C', 'Calculate', ChoiceConstraint(['C', 'w', 'l', 'w&l']))
        specs('model', model, 'Model name')
              
        specs('C', eng_string(C), 'C')
        
        specs('w', defLW, 'Width')
        specs('l', defLW, 'Length')
        
        specs('wfeed', '3u', 'Feed width')
        specs('Cspec', caspec, 'Cspec [F/sqm]')
        specs('Wmin', minLW, 'Wmin')
        specs('Lmin', minLW, 'Lmin')
        specs('Cmax', cmax, 'Cmax')
#else
        CDFVersion = techparams['CDFVersion']
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('Calculate', 'C', 'Calculate', ChoiceConstraint(['C', 'w', 'l', 'w&l']))
        specs('model', model, 'Model name')
              
        specs('C', eng_string(C), 'C')
        
        specs('l', defLW, 'Length')
        specs('w', defLW, 'Width')
        
        specs('wfeed', '3u', 'Feed width')
        specs('Cspec', caspec, 'Cspec [F/sqm]')
        specs('Wmin', minLW, 'Wmin')
        specs('Lmin', minLW, 'Lmin')
        specs('Cmax', cmax, 'Cmax')
        
        specs('ic', '', 'Initial condition')
        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')
#endif

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.w = Numeric(self.params['w'])
        self.l = Numeric(self.params['l'])
        self.wfeed = Numeric(self.params['wfeed'])
        self.C = eng_string(CbCapCalc('C', 0, self.l, self.w, 'rfcmim'))

    def genLayout(self):
        self.grid = self.tech.getGridResolution()
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']
        
        w = self.w
        l = self.l
        wfeed = self.wfeed
            
        lu = GridFix(l*1e6)
        wu = GridFix(w*1e6)
        wf = GridFix(wfeed*1e6)
        
        #########################################################
        #
        # Layer Definitions
        #
        #########################################################
        
        textlayer = Layer('TEXT', 'drawing')     # TEXT
        gndlayer = Layer('Metal1')    # Metal1 used for ground ring
        tmlayer = Layer('TopMetal1')  # Top Metal above MIM is TopMetal1
        bmlayer = Layer('Metal5')     # Bottom metal below MIM is Metal5
        caplayer = Layer('MIM')
        vialayer = Layer('Vmim')
        pwellblock = Layer('PWell', 'block')
        cont = Layer('Cont')
        activ = Layer('Activ')
        psd = Layer('pSD')
        
        nolayer = 0
            
        #########################################################
        #
        # Generic Design Rule Definitions
        #
        #########################################################
        
        via_size = self.techparams['TV1_a']
        via_dist = self.techparams['TV1_b']
        cont_size = self.techparams['Cnt_a']
        cont_dist = self.techparams['Cnt_b']
        tm_over = self.techparams['TV1_d']
        
        #########################################################
        #
        # Device Specific Design Rule Definitions
        #
        #########################################################
        
        mim_over = self.techparams['Mim_c']
        via_over = self.techparams['Mim_d']
        
        #########################################################
        #
        # Main body of code
        #
        #########################################################
        
        #########################################################
        # Special dimensions for rfcmim
        #########################################################
        gnd_width = 2                # um, ground frame width
        gnd_over_bm = 3+gnd_width/2  # um, distance from ground frame to bottom plate
        feedox = GridFix((lu-wf)/2)
        feedoy = GridFix((wu-wf)/2)
        
        contactArray(self, nolayer, vialayer, 0, 0, lu, wu, via_over+tm_over, via_over+tm_over, via_size, via_dist)
        dbCreateRect(self, caplayer, Box(0, 0, lu, wu))
        dbCreateRect(self, tmlayer, Box(via_over, via_over, lu-via_over, wu-via_over))
        dbCreateRect(self, bmlayer, Box(-mim_over, -mim_over, lu+mim_over, wu+mim_over))
        dbCreateRect(self, bmlayer, Box(-mim_over, -mim_over, lu+mim_over, wu+mim_over))
        dbCreateRect(self, pwellblock, Box(-3, -3, lu+3, wu+3))
        dbCreateRect(self, tmlayer, Box(-5.6, feedoy, via_over, feedoy+wf))
        id1 = dbCreateRect(self, Layer('TopMetal1', 'pin'), Box(-5.6, feedoy, -3.6, feedoy+wf))
        MkPin(self, 'PLUS', 0, id1.bbox, id1.layer)
        dbCreateLabel(self, textlayer, Point(-4.6, feedoy+wf/2), 'PLUS', 'centerCenter', 'R90', Font.EURO_STYLE, 0.8)
        
        # no QRC up to Metal3 in entire device area
        dbCreateRect(self, Layer('Activ', 'noqrc'), Box(-5.6, -5.6, lu+5.6, wu+5.6))
        dbCreateRect(self, Layer('Metal1', 'noqrc'), Box(-5.6, -5.6, lu+5.6, wu+5.6))
        dbCreateRect(self, Layer('Metal2', 'noqrc'), Box(-5.6, -5.6, lu+5.6, wu+5.6))
        dbCreateRect(self, Layer('Metal3', 'noqrc'), Box(-5.6, -5.6, lu+5.6, wu+5.6))

        dbCreateRect(self, Layer('Metal4', 'noqrc'), Box(-5.6, -5.6, lu+5.6, wu+5.6))
        dbCreateRect(self, Layer('Metal5', 'noqrc'), Box(-5.6, -5.6, lu+5.6, wu+5.6))
        dbCreateRect(self, Layer('TopMetal1', 'noqrc'), Box(-5.6, -5.6, lu+5.6, wu+5.6))
         
        # the ring   
        id1 = dbCreateRect(self, activ, Box(-3.6, -3.6, lu+3.6, wu+3.6))
        id2 = dbCreateRect(self, activ, Box(-5.6, -5.6, lu+5.6, wu+5.6))
        idlist = dbLayerXor(activ, id1, id2)
        dbDeleteObject(id1)
        dbDeleteObject(id2)
        
        id1 = idlist.getComp(0)
        
        dbCreateRect(self, bmlayer, Box(lu+5.6, feedoy, lu+0.6, feedoy+wf))
        id2 = dbCreateRect(self, Layer('Metal5', 'pin'), Box(lu+5.6, feedoy, lu+3.6, feedoy+wf))
            
        idlist = dbLayerXor(activ, id1, id2)
        dbDeleteObject(id1)
        MkPin(self, 'MINUS', 0, id2.bbox, id2.layer)
        x = (nth(0, id2.bbox) + nth(2, id2.bbox)) / 2
        y = (nth(1, id2.bbox) + nth(3, id2.bbox)) / 2
                
        dbCreateLabel(self, textlayer, Point(x, y), 'MINUS', 'centerCenter', 'R90', Font.EURO_STYLE, 0.8)
        
        # pSD ring
        ps_cutarea = dbCreateRect(self, psd, Box(-3.57, -3.57, lu+3.57, wu+3.57))
        ps_guardarea = dbCreateRect(self, psd, Box(-5.63, -5.63, lu+5.63, wu+5.63))
        psd_guardring = dbLayerXor(psd, ps_cutarea, ps_guardarea)
        dbDeleteObject(ps_cutarea)
        dbDeleteObject(ps_guardarea)
        
        # Metal1 ring
        id1 = dbCreateRect(self, gndlayer, Box(-3.6, -3.6, lu+3.6, wu+3.6))
        id3 = dbCreateRect(self, gndlayer, Box(-5.6, -5.6, lu+5.6, wu+5.6))
        id4 = dbLayerXor(gndlayer, id1, id3)
        dbLayerXor(gndlayer, id4, id2)
        dbDeleteObject(id1)
        dbDeleteObject(id3)
        dbDeleteObject(id4)
        
        # ring contacts
        contactArray(self, nolayer, cont, lu+3.6, -3.6, lu+5.6, feedoy, 0.36, 0.36, cont_size, cont_dist)
        contactArray(self, nolayer, cont, lu+3.6, feedoy+wf, lu+5.6, wu+3.6, 0.36, 0.36, cont_size, cont_dist)
        
        contactArray(self, nolayer, cont, -5.6, -3.6, -3.6, wu+3.6, 0.36, 0.36, cont_size, cont_dist)
        contactArray(self, nolayer, cont, -5.6, wu+3.6, lu+5.6, wu+5.6, 0.36, 0.36, cont_size, cont_dist)
        contactArray(self, nolayer, cont, -5.6, -5.6, lu+5.6, -3.6, 0.36, 0.36, cont_size, cont_dist)
            
        id1 = dbCreateRect(self, Layer('Metal1', 'pin'), Box(-5.6, -5.6, lu+5.6, -3.6))
        y = -4.6
            
        MkPin(self, 'TIE', 0, id1.bbox, id1.layer)
        dbCreateLabel(self, textlayer, Point(lu/2, y), 'TIE', 'centerCenter', 'R0', Font.EURO_STYLE, 1)
        dbCreateLabel(self, textlayer, Point(lu/2, wu+2), 'rfcmim', 'centerCenter', 'R0', Font.EURO_STYLE, 0.8)
        dbCreateLabel(self, textlayer, Point(lu/2, -2), 'C='+self.C, 'centerCenter', 'R0', Font.EURO_STYLE, 0.8)
