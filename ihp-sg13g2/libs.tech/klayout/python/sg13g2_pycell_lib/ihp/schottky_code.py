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

class schottky(DloGen):

    @classmethod
    #def __init__(self, cellName):
    #    self.Cell = cellName
    
    def defineParamSpecs(self, specs):        
        techparams = specs.tech.getTechParams()
        
        CDFVersion = techparams['CDFVersion']
        #model      = techparams[self.Cell+'_model']
        defL       = '0.3u'
        defW       = '1.0u'
        
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', 'schottky', 'Model name')
        
        specs('w', defW, 'Width')
        specs('l', defL, 'Length')
        specs('Nx', 1, 'Columns number Nx', RangeConstraint(1, 10))
        specs('Ny', 1, 'Rows number Ny'   , RangeConstraint(1, 10))
        specs('m', '1', 'Multiplier')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.Nx = params['Nx']
        self.Ny = params['Ny']
        self.l = params['l']
        self.w = params['w']

    def genLayout(self):
        Nx = self.Nx
        Ny = self.Ny
        l = self.l
        w = self.w

        l = Numeric(l)*1e6
        w = Numeric(w)*1e6
               
        activ = Layer('Activ', 'drawing')        # 1
        nsdblock = Layer('nSD', 'block')         # 4
        cont  = Layer('Cont', 'drawing')         # 6
        met1 = Layer('Metal1', 'drawing')        # 8
        met1_pin = Layer('Metal1', 'pin')        # 8
        met2 = Layer('Metal2', 'drawing')        # 10
        met2_pin = Layer('Metal2', 'pin')        # 10
        psd = Layer('pSD', 'drawing')            # 14 
        via1 = Layer('Via1', 'drawing')          # 19
        salblock = Layer('SalBlock', 'drawing')  # 28
        nwell = Layer('NWell', 'drawing')        # 31
        nbulay = Layer('nBuLay', 'drawing')      # 32
        pwellblock = Layer('PWell', 'block')     # 46
        gateOx = Layer('ThickGateOx', 'drawing') # 44
        text = Layer('TEXT', 'drawing')          # 63
        diode = Layer('Recog', 'diode')          # 99
        
        nsdbOcont = 0.45
        pcStepX = l + 2
        pcStepY = w + 1.7
        psdWidth = 0.5
        gateOxOpsd = 0.17
        nwellScont = 0.25
        activWidth = 0.3
        psdOactiv = 0.1
        contW = 0.16
        contS = 0.18
        metWidth = contW+0.14
        viaW = 0.19
        if w <  1.52 :
            viaS = 0.22
        else :
            viaS = 0.29
            
        Cell = self.__class__.__name__
            
        pcRepeatX = Nx
        pcRepeatY = Ny
        for pcIndexX in range(Nx) :
            for pcIndexY in range(Ny) :
                dbCreateRect(self, cont, Box(nsdbOcont+pcIndexX*pcStepX, nsdbOcont+pcIndexY*pcStepY, nsdbOcont+l+pcIndexX*pcStepX, nsdbOcont+w+pcIndexY*pcStepY))
                dbCreateRect(self, met1, Box(nsdbOcont-0.05+pcIndexX*pcStepX, nsdbOcont-0.07+pcIndexY*pcStepY, nsdbOcont+0.05+l+pcIndexX*pcStepX, nsdbOcont+0.07+w+pcIndexY*pcStepY))
                
                ihpBuildCont(self, met2, met1, via1, viaW+0.1, viaW, viaW, 
                             Box(nsdbOcont+GridFix(l/2-0.205)+pcIndexX*pcStepX, nsdbOcont-0.07+pcIndexY*pcStepY, nsdbOcont+GridFix(l/2-0.205)+pcIndexX*pcStepX, nsdbOcont+0.07+w+pcIndexY*pcStepY),
                             "", False, 0.04, 0.05, 0, viaS)
        
                ihpBuildCont(self, met2, met1, via1, viaW+0.1, viaW, viaW,
                             Box(nsdbOcont+GridFix(l/2+0.205)+pcIndexX*pcStepX, nsdbOcont-0.07+pcIndexY*pcStepY, nsdbOcont+GridFix(l/2+0.205)+pcIndexX*pcStepX, nsdbOcont+0.07+w+pcIndexY*pcStepY),
                             "", False, 0.04, 0.05, 0, viaS)
                
                dbCreateRect(self, nsdblock, Box(0.05+pcIndexX*pcStepX, 0.05+pcIndexY*pcStepY, 2*nsdbOcont-0.05+l+pcIndexX*pcStepX, 2*nsdbOcont-0.05+w+pcIndexY*pcStepY))
                dbCreateRect(self, salblock, Box(pcIndexX*pcStepX, pcIndexY*pcStepY, 2*nsdbOcont+l+pcIndexX*pcStepX, 2*nsdbOcont+w+pcIndexY*pcStepY))
                dbCreateRect(self, activ, Box(nsdbOcont-1+pcIndexX*pcStepX, nsdbOcont-0.85+pcIndexY*pcStepY, nsdbOcont+l+1+pcIndexX*pcStepX, nsdbOcont+w+0.85+pcIndexY*pcStepY))
                dbCreateRect(self, nwell, Box(-1+nsdbOcont-nwellScont+pcIndexX*pcStepX, nsdbOcont-nwellScont+pcIndexY*pcStepY, nsdbOcont-nwellScont+pcIndexX*pcStepX, nsdbOcont+nwellScont+w+pcIndexY*pcStepY))
                dbCreateRect(self, nwell, Box(nsdbOcont+l+nwellScont+pcIndexX*pcStepX, nsdbOcont-nwellScont+pcIndexY*pcStepY, nsdbOcont+l+nwellScont+1+pcIndexX*pcStepX, nsdbOcont+nwellScont+w+pcIndexY*pcStepY))
                dbCreateRect(self, nwell, Box(-1+nsdbOcont-nwellScont+pcIndexX*pcStepX, nsdbOcont+nwellScont+w+pcIndexY*pcStepY, nsdbOcont+l+nwellScont+1+pcIndexX*pcStepX, nsdbOcont+nwellScont+w+0.85+pcIndexY*pcStepY))
                dbCreateRect(self, nwell, Box(-1+nsdbOcont-nwellScont+pcIndexX*pcStepX, nsdbOcont-nwellScont+pcIndexY*pcStepY, nsdbOcont+l+nwellScont+1+pcIndexX*pcStepX, nsdbOcont-nwellScont-0.85+pcIndexY*pcStepY))
                dbCreateRect(self, pwellblock, Box(nsdbOcont-nwellScont+pcIndexX*pcStepX, nsdbOcont-nwellScont+pcIndexY*pcStepY, nsdbOcont+l+nwellScont+pcIndexX*pcStepX, nsdbOcont+nwellScont+w+pcIndexY*pcStepY))
                
            MetalCont(self, -0.37+pcIndexX*pcStepX, nsdbOcont-0.07-0.78, -0.37+pcIndexX*pcStepX, nsdbOcont+0.07+w+0.78+(Ny-1)*pcStepY, met1, cont, metWidth-0.02, contW, contW, 0.09, contS)
            MetalCont(self, 2*nsdbOcont+l+0.37+pcIndexX*pcStepX, nsdbOcont-0.07-0.78, 2*nsdbOcont+l+0.37+pcIndexX*pcStepX, nsdbOcont+0.07+w+0.78+(Ny-1)*pcStepY, met1, cont, metWidth-0.02, contW, contW, 0.09, contS)
            
            dbCreateRect(self, met2, Box(nsdbOcont+GridFix(l/2-0.305)+pcIndexX*pcStepX, nsdbOcont-1.145, nsdbOcont+GridFix(l/2+0.305)+pcIndexX*pcStepX, nsdbOcont + w + 0.555 + (Ny-1)*pcStepY))
            dbCreateRect(self, met1, Box(-0.55+pcIndexX*pcStepX, nsdbOcont-0.07-0.78, -0.51+pcIndexX*pcStepX, nsdbOcont+0.07+w+0.78+(Ny-1)*pcStepY))
            dbCreateRect(self, met1, Box(2*nsdbOcont+l+0.51+pcIndexX*pcStepX, nsdbOcont-0.07-0.78, 2*nsdbOcont+l+0.55+pcIndexX*pcStepX, nsdbOcont+0.07+w+0.78+(Ny-1)*pcStepY))
            
        dbCreateRect(self, diode, Box(-1+nsdbOcont-nwellScont, nsdbOcont-nwellScont-0.85, nsdbOcont+l+nwellScont+1+(Nx-1)*pcStepX, nsdbOcont+nwellScont+w+0.85+(Ny-1)*pcStepY))
            
        dbCreateRect(self, met1, Box(-0.55, nsdbOcont+0.07+w+0.78+(Ny-1)*pcStepY, 2*nsdbOcont+l+0.55+(Nx-1)*pcStepX, nsdbOcont+0.07+w+0.78+1.055+(Ny-1)*pcStepY))
        MkPin(self, 'MINUS', 0, Box(-0.55, nsdbOcont+0.07+w+0.78+(Ny-1)*pcStepY, 2*nsdbOcont+l+0.55+(Nx-1)*pcStepX, nsdbOcont+0.07+w+0.78+1.055+(Ny-1)*pcStepY), met1_pin)
        
        MetalCont(self, -1.9-GridFix(psdWidth/2), -1.98-psdOactiv, -1.9-GridFix(psdWidth/2), 1.62+psdOactiv+2*nsdbOcont+w+(Ny-1)*pcStepY, met1, cont, metWidth, contW, contW, 0.09, contS)
        MkPin(self, 'TIE1', 0, Box(-1.9-GridFix((psdWidth+metWidth)/2), -1.98-psdOactiv, -1.9-GridFix((psdWidth-metWidth)/2), 1.62+psdOactiv+2*nsdbOcont+w+(Ny-1)*pcStepY), met1_pin)
        MetalCont(self, l+2*nsdbOcont+1.9+GridFix(psdWidth/2)+(Nx-1)*pcStepX, -1.98-psdOactiv, l+2*nsdbOcont+1.9+GridFix(psdWidth/2)+(Nx-1)*pcStepX, 1.62+psdOactiv+2*nsdbOcont+w+(Ny-1)*pcStepY, met1, cont, metWidth, contW, contW, 0.09, contS)
        
        MkPin(self, 'TIE2', 0, Box(l+2*nsdbOcont+1.9+GridFix((psdWidth-metWidth)/2)+(Nx-1)*pcStepX, -1.98-psdOactiv, l+2*nsdbOcont+1.9+GridFix((psdWidth+metWidth)/2)+(Nx-1)*pcStepX, 1.62+psdOactiv+2*nsdbOcont+w+(Ny-1)*pcStepY), met1_pin)
        dbCreateRect(self, met2, Box(nsdbOcont-0.05-0.98, nsdbOcont-1.145-1.12, nsdbOcont+0.05+l+0.98+(Nx-1)*pcStepX, nsdbOcont-1.145))
        MkPin(self, 'PLUS', 0, Box(nsdbOcont-0.05-0.98, nsdbOcont-1.145-1.12, nsdbOcont+0.05+l+0.98+(Nx-1)*pcStepX, nsdbOcont-1.145), met2_pin)
        
        dbCreateRect(self, psd, Box(-1.9-psdWidth, -1.98, -1.9, 1.62+2*nsdbOcont+w+(Ny-1)*pcStepY))
        dbCreateRect(self, psd, Box(l+2*nsdbOcont+1.9+(Nx-1)*pcStepX, -1.98, l+2*nsdbOcont+psdWidth+1.9+(Nx-1)*pcStepX, 1.62+2*nsdbOcont+w+(Ny-1)*pcStepY))
        dbCreateRect(self, psd, Box(-1.9-psdWidth, 1.62+2*nsdbOcont+w+(Ny-1)*pcStepY, l+2*nsdbOcont+psdWidth+1.9+(Nx-1)*pcStepX, 1.62+2*nsdbOcont+psdWidth+w+(Ny-1)*pcStepY))
        dbCreateRect(self, psd, Box(-1.9-psdWidth, -1.98-psdWidth, l+2*nsdbOcont+psdWidth+1.9+(Nx-1)*pcStepX, -1.98))
        
        dbCreateRect(self, activ, Box(-1.9-psdOactiv-activWidth, -1.98-psdOactiv, -1.9-psdOactiv, 1.62+psdOactiv+2*nsdbOcont+w+(Ny-1)*pcStepY))
        dbCreateRect(self, activ, Box(l+2*nsdbOcont+1.9+psdOactiv+(Nx-1)*pcStepX, -1.98-psdOactiv, l+2*nsdbOcont+psdOactiv+activWidth+1.9+(Nx-1)*pcStepX, 1.62+psdOactiv+2*nsdbOcont+w+(Ny-1)*pcStepY))
        dbCreateRect(self, activ, Box(-1.9-psdOactiv-activWidth, 1.62+psdOactiv+2*nsdbOcont+w+(Ny-1)*pcStepY, l+2*nsdbOcont+psdOactiv+activWidth+1.9+(Nx-1)*pcStepX, 1.62+2*nsdbOcont+psdOactiv+activWidth+w+(Ny-1)*pcStepY))
        dbCreateRect(self, activ, Box(-1.9-psdOactiv-activWidth, -1.98-psdOactiv-activWidth, l+2*nsdbOcont+psdOactiv+activWidth+1.9+(Nx-1)*pcStepX, -1.98-psdOactiv))
        
        dbCreateRect(self, gateOx, Box(-1.9-psdWidth-gateOxOpsd, -1.98-psdWidth-gateOxOpsd, l+2*nsdbOcont+psdWidth+1.9+(Nx-1)*pcStepX+gateOxOpsd, 1.62+2*nsdbOcont+psdWidth+w+(Ny-1)*pcStepY+gateOxOpsd))
        dbCreateRect(self, nbulay, Box(nsdbOcont-1, nsdbOcont-0.85-0.02, nsdbOcont+l+1+(Nx-1)*pcStepX, nsdbOcont+w+0.85+(Ny-1)*pcStepY+0.02))
        dbCreateRect(self, pwellblock, Box(nsdbOcont-2.08, nsdbOcont-1.1, nsdbOcont-1.25, nsdbOcont+w+1.1+(Ny-1)*pcStepY))
        dbCreateRect(self, pwellblock, Box(nsdbOcont+l+1.25+(Nx-1)*pcStepX, nsdbOcont-1.1, nsdbOcont+l+2.08+(Nx-1)*pcStepX, nsdbOcont+w+1.1+(Ny-1)*pcStepY))
        dbCreateRect(self, pwellblock, Box(nsdbOcont-2.08, nsdbOcont-2.29, nsdbOcont+l+2.08+(Nx-1)*pcStepX, nsdbOcont-1.1))
        dbCreateRect(self, pwellblock, Box(nsdbOcont-2.08, nsdbOcont+w+1.1+(Ny-1)*pcStepY, nsdbOcont+l+2.08+(Nx-1)*pcStepX, nsdbOcont+w+1.93+(Ny-1)*pcStepY))
        
        pcInst = dbCreateLabel(self, text, Point(0.018, -0.59), Cell, 'centerCenter', 'R0', Font.EURO_STYLE, 0.28)
        pcInst.setDrafting(True)
         
##############################################
class schottky_nbl1(schottky):
    Cell = 'schottky_nbl1'
