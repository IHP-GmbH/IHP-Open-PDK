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

class SVaricap(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs): 
        techparams = specs.tech.getTechParams()
        
        CDFVersion = techparams['CDFVersion']
        model      = 'sg13_hv_svaricap'
        defL       = '0.3u'
        defW       = '3.74u' 
#ifdef KLAYOUT
        specs('model', model, 'Model name')
        specs('w', defW, 'Width' , ChoiceConstraint(['3.74u', '9.74u']))
        specs('l', defL, 'Length', ChoiceConstraint(['0.3u' , '0.8u']))
        specs('Nx', 1, 'Choose the columns number', RangeConstraint(1, 10))
        specs('bn', 'sub!', 'Bulk node connection')
#else
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')
        
        specs('w', defW, 'Width' , ChoiceConstraint(['3.74u', '9.74u']))
        specs('l', defL, 'Length', ChoiceConstraint(['0.3u' , '0.8u']))
        specs('Nx', 1, 'Choose the columns number', RangeConstraint(1, 10))
        specs('bn', 'sub!', 'Bulk node connection')
#endif
    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.Nx = params['Nx']
        self.l = Numeric(params['l'])
        self.w = Numeric(params['w'])
        

    def genLayout(self):
        l = Numeric(self.l)*1e6
        w = Numeric(self.w)*1e6
        NX = self.Nx;

        activ = Layer('Activ', 'drawing')         # layer 1
        gate = Layer('GatPoly', 'drawing')        # layer 1
        cont = Layer('Cont', 'drawing')           # layer 6
        met1 = Layer('Metal1', 'drawing')         # layer 8
        met1_pin = Layer('Metal1', 'pin')         # layer 8
        psd = Layer('pSD', 'drawing')             # layer 14
        nwell = Layer('NWell', 'drawing')         # layer 31
        nbulay = Layer('nBuLay', 'drawing')       # layer 32
        gateOx = Layer('ThickGateOx', 'drawing')  # layer 44
        text = Layer('TEXT', 'drawing')           # layer 63

        nwellOgate = 0.57
        nbulayOgate = 0.33
        gateOactiv = 0.35
        contW = 0.16
        contS = 0.18
        metW = contW+2*0.05

        if w == 3.74 :
            gateOnwell  = 0.11
            gateOnbulay = 0.35
        else :
            gateOnwell  = -0.145
            gateOnbulay = 0.1
            
        x1 = 0.73
        gateS = 0.25
         

        psdStep = 10
        y1 = 0.39+gateS
        pcStepX = (gateS+l)*2
        nr_psd = round((2*NX*l+(2*NX-1)*gateS-0.24)/10+0.5)

        if nr_psd >  1 :
            x_psd = GridFix((2*NX*l+(2*NX-1)*gateS-(nr_psd-1)*10)/2+0.61)
            if x_psd < x1+GridFix((2*l+gateS-0.24)/2) :
                nr_psd = nr_psd-1
                x_psd = GridFix((2*NX*l+(2*NX-1)*gateS-(nr_psd-1)*10)/2+0.61)
        else :
            x_psd = x1+GridFix((2*NX*l+(2*NX-1)*gateS-0.24)/2)

        for pcIndexX in range(NX) :
            dbCreateRect(self, gate, Box(x1+pcIndexX*pcStepX, y1, x1+l+pcIndexX*pcStepX, y1+w))
            dbCreateRect(self, gate, Box(x1+l+gateS+pcIndexX*pcStepX, y1-gateS, x1-gateS+(pcIndexX+1)*pcStepX, y1-gateS+w))
            
            MetalCont(self, GridFix(x1+l/2)+pcIndexX*pcStepX, y1+0.08, GridFix(x1+l/2)+pcIndexX*pcStepX, y1+w-0.01, met1, cont, metW, contW, contW, 0.05, contS)
            MetalCont(self, x1-gateS-GridFix(l/2)+(pcIndexX+1)*pcStepX, y1-gateS+0.01, x1-gateS-GridFix(l/2)+(pcIndexX+1)*pcStepX, y1-gateS+w-0.08, met1, cont, metW, contW, contW, 0.05, contS)
            
            dbCreateRect(self, met1, Box(x1+GridFix((l-metW)/2)+pcIndexX*pcStepX, y1+w-0.01, x1+GridFix((l+metW)/2)+pcIndexX*pcStepX, y1+w+0.12))
            dbCreateRect(self, met1, Box(x1-gateS-GridFix((l+metW)/2)+(pcIndexX+1)*pcStepX, y1-gateS+0.01, x1-gateS-GridFix((l-metW)/2)+(pcIndexX+1)*pcStepX, y1-gateS-0.12))

        for pcIndexX in range(int(nr_psd)) :
            dbCreateRect(self, activ, Box(x_psd+pcIndexX*10, y1+w+0.5-gateOactiv, x_psd+0.24+pcIndexX*10, y1+w+0.5-gateOactiv+0.76))
            dbCreateRect(self, activ, Box(x_psd+pcIndexX*10, y1-gateS-0.5+gateOactiv, x_psd+0.24+pcIndexX*10, y1-gateS-0.5+gateOactiv-0.76))
            dbCreateRect(self, psd, Box(x_psd-0.1+pcIndexX*10, y1+w+0.6-gateOactiv, x_psd+0.34+pcIndexX*10, y1+w+0.6-gateOactiv+0.76))
            dbCreateRect(self, psd, Box(x_psd-0.1+pcIndexX*10, y1-gateS-0.6+gateOactiv, x_psd+0.34+pcIndexX*10, y1-gateS-0.6+gateOactiv-0.76))

        dbCreateRect(self, gate, Box(x1, y1+w, x1-gateS+NX*pcStepX, y1+w+0.5))
        dbCreateRect(self, gate, Box(x1, y1-gateS, x1-gateS+NX*pcStepX, y1-gateS-0.5))
        # metal1 and contacts from gate on top and bottom
        MetalCont(self, x1+0.02, y1-gateS-0.25, x1-gateS-0.02+NX*pcStepX, y1-gateS-0.25, met1, cont, metW, contW, contW, 0.05, contS)
        MetalCont(self, x1+0.02, y1+w+0.25, x1-gateS-0.02+NX*pcStepX, y1+w+0.25, met1, cont, metW, contW, contW, 0.05, contS)
        MetalCont(self, x1-0.34, y1+(w-gateS)/2-0.48, x1-0.34, y1+(w-gateS)/2+0.48, met1, cont, contW+2*0.02, contW, contW, 0.05, contS) #cont left side
        # the G1, G2 and W pins
        MkPin(self, 'G1', 0, Box(x1+0.02, y1-gateS-0.12, x1-gateS-0.02+NX*pcStepX, y1-gateS-0.38), 'Metal1')
        MkPin(self, 'G2', 0, Box(x1+0.02, y1+w+0.12, x1-gateS-0.02+NX*pcStepX, y1+w+0.38), 'Metal1')
        MkPin(self, 'W',  0, Box(x1-0.44, y1+GridFix((w-gateS)/2)-0.47, x1-0.24, y1+GridFix((w-gateS)/2)+0.47), 'Metal1')
        
        dbCreateRect(self, activ, Box(x1-0.49, y1-gateS-0.5+gateOactiv, x1-gateS+NX*pcStepX+0.33, y1+w+0.5-gateOactiv))
        dbCreateRect(self, nwell, Box(x1-0.73, y1-gateS-0.5+gateOnwell, x1-gateS+NX*pcStepX+0.57, y1+w+0.5-gateOnwell))
        dbCreateRect(self, nbulay, Box(x1-0.49, y1-gateS-0.5+gateOnbulay, x1-gateS+NX*pcStepX+0.33, y1+w+0.5-gateOnbulay))
        dbCreateLabel(self, text, Point(x1-0.49, y1-gateS-0.5+gateOnbulay+gateOactiv), 'SVaricap', 'centerLeft', 'R0', Font.EURO_STYLE, 0.25)
            