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
__version__ = "$Revision: #3 $"

from cni.dlo import *
from .thermal import *
from .geometry import *
from .utility_functions import *

import math

class npn13G2_base(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        specs('STI', '0.44u')
        specs('baspolyx', '0.3u')
        specs('bipwinx', '0.07u')
        specs('bipwiny', '0.1u')
        specs('empolyx', '0.15u')
        specs('empolyy', '0.18u')
        specs('le', '0.9u')
        specs('we', '0.07u')
        specs('Nx', 1)
        specs('Text', 'npn13G2')
        specs('CMetY1', '0.0')
        specs('CMetY2', '0.0')

    def setupParams(self, params):
        # process parameter values entered by user
        self.STI = Numeric(params['STI'])
        self.baspolyx = Numeric(params['baspolyx'])
        self.bipwinx = Numeric(params['bipwinx'])
        self.bipwiny = Numeric(params['bipwiny'])
        self.empolyx = Numeric(params['empolyx'])
        self.empolyy = Numeric(params['empolyy'])
        self.le = Numeric(params['le'])
        self.we = Numeric(params['we'])
        self.Nx = Numeric(params['Nx'])
        self.Text = params['Text']
        self.CMetY1 = Numeric(params['CMetY1'])
        self.CMetY2 = Numeric(params['CMetY2'])

    def genLayout(self):
        STI = self.STI
        baspolyx = self.baspolyx
        bipwinx = self.bipwinx
        bipwiny = self.bipwiny
        empolyx = self.empolyx
        empolyy = self.empolyy
        le = self.le
        we = self.we
        Nx = self.Nx
        Text = self.Text
        CMetY1 = self.CMetY1
        CMetY2 = self.CMetY2

        STI = Numeric(STI)*1e6
        baspolyx = Numeric(baspolyx)*1e6
        bipwinx = Numeric(bipwinx)*1e6
        bipwiny = Numeric(bipwiny)*1e6
        empolyx = Numeric(empolyx)*1e6
        empolyy = Numeric(empolyy)*1e6
        le = Numeric(le)*1e6
        we = Numeric(we)*1e6;

        Cell = 'npn13G2_base'

        stepX = 1.85
        stretchX = stepX*(Nx-1)
        
        bipwinxoffset = ((2 * (bipwinx - 0.04)) / 2)
        empolyxoffset = ((2 * (empolyx - 0.15)) / 2)
        baspolyxoffset = ((2 * (baspolyx - 0.3)) / 2)
        STIoffset = ((2 * (STI - 0.44)) / 2)
        bipwinyoffset = ((2 * (bipwiny - 0.1)) / 2)
        empolyyoffset = ((2 * (empolyy - 0.18)) / 2)
        
        nSDBlockShift = 0.43 - le # 23.07.09: needed to draw nSDBlock shorter in small pCell
        
        # 28.02.07: In the moment only le=48 and le=84 is possible. So use an if to get the right values
        leoffset = 0 # ((le - 0.07) / 2)  # 03.04.08: moved here
        
        pcStepY = 0.41
        yOffset = 0.20

        pcRepeatY = 4

        if Nx >  1 :
            CMetY1 = -1.01 - we/2 - leoffset - bipwinyoffset - empolyyoffset
            CMetY2 = -0.57 - we/2 - leoffset - bipwinyoffset - empolyyoffset
        else :
            CMetY1 = -0.8 - we/2 - leoffset - bipwinyoffset - empolyyoffset
            CMetY2 = -0.56 - we/2 - leoffset - bipwinyoffset - empolyyoffset

        pcPurpose = 'drawing'
        for pcIndexX in range(int(math.floor(Nx))) :
            # loop for generate the given number of vias in variable pcRepeatY
            # two vias are generated per loop
            for pcIndexY in range(int((math.floor(pcRepeatY)))) :
                # via on left side 
                pcInst = dbCreateRect(self, Layer('Via1', pcPurpose),
                                      Box((stepX*pcIndexX)-0.3,  (( -0.3-yOffset-leoffset-bipwinyoffset-empolyyoffset)+(pcIndexY*pcStepY))-0.2,
                                          (stepX*pcIndexX)-0.11, ((-0.11-yOffset-leoffset-bipwinyoffset-empolyyoffset)+(pcIndexY*pcStepY))-0.2))
                # via on right side
                pcInst = dbCreateRect(self, Layer('Via1', pcPurpose),
                                      Box((stepX*pcIndexX)+0.11, ((-0.3-yOffset-leoffset-bipwinyoffset-empolyyoffset)+(pcIndexY*pcStepY))-0.2,
                                          (stepX*pcIndexX)+0.3, ((-0.11-yOffset-leoffset-bipwinyoffset-empolyyoffset)+(pcIndexY*pcStepY))-0.2))

            pcLayer = 'Metal1'
            pcInst = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(stepX*pcIndexX-0.35, (-0.32-we/2-leoffset-bipwinyoffset-empolyyoffset), stepX*pcIndexX+0.35, (0.335+we/2+leoffset+bipwinyoffset+empolyyoffset)))
            
            pcLayer = 'Cont'
            pcInst = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(stepX*pcIndexX-0.79-le/2, (-0.76-we/2-leoffset-bipwinyoffset-empolyyoffset), stepX*pcIndexX+0.79+le/2, (-0.6-we/2-leoffset-bipwinyoffset-empolyyoffset)))
            pcInst = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(stepX*pcIndexX-0.76, (0.77+we/2-leoffset-bipwinyoffset-empolyyoffset), stepX*pcIndexX+0.76, (0.61+we/2-leoffset-bipwinyoffset-empolyyoffset)))
            
            pcLayer = 'EmWind'
            pcInst = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(stepX*pcIndexX-le/2, (-we/2-leoffset), stepX*pcIndexX+le/2, (we/2+leoffset)))

            #ihpAddThermalBjtLayer(pcCellView, Box((stepX*pcIndexX-le/2)-0.05, , -we/2 - leoffset, -0.05, (stepX*pcIndexX+le/2)+0.05, , we/2 + leoffset, +0.05), t, Cell)
            
            pcLayer = 'Activ'
            xl = stepX*pcIndexX-0.06
            xh = xl+0.12
            yl = -0.24-leoffset
            yh = -yl
            pcInst = dbCreatePolygon(self, Layer(pcLayer, 'mask'), PointList([Point(xh+0.865, yl-0.74), Point(xl-0.865, yl-0.74), Point(xl-0.865, yh+0.38), Point(xl-0.385, yh+0.38), Point(xl-0.175, yh+0.59), Point(xh+0.175, yh+0.59), Point(xh+0.385, yh+0.38), Point(xh+0.865, yh+0.38)]))
            
            pcInst = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box((stepX*pcIndexX-0.89-le/2-empolyxoffset-baspolyxoffset-STIoffset), (-0.83-we/2-leoffset-bipwinyoffset-empolyyoffset), (stepX*pcIndexX+0.89+le/2+empolyxoffset+baspolyxoffset+STIoffset), (-0.89-we/2+0.36-leoffset-bipwinyoffset-empolyyoffset)))
            
            pcLayer ='nSD'
            pcInst = dbCreatePolygon(self, Layer(pcLayer, 'block'),
                     PointList([Point((stepX * pcIndexX + 0.94 + le/2 + empolyxoffset + baspolyxoffset + STIoffset), (1.98 + we/2 + leoffset + bipwinyoffset + empolyyoffset)),
                                Point((stepX * pcIndexX + 0.94 + le/2 + empolyxoffset + baspolyxoffset + STIoffset), (0.45 + we/2 + leoffset + bipwinyoffset + empolyyoffset)),
                                Point((stepX * pcIndexX + 0.52 + le/2 + empolyxoffset + baspolyxoffset + STIoffset), (0.03 + we/2 + leoffset + bipwinyoffset + empolyyoffset)),
                                Point((stepX * pcIndexX + 0.52 + le/2 + empolyxoffset + baspolyxoffset + STIoffset), (-0.6 - we/2 + leoffset + bipwinyoffset + empolyyoffset + nSDBlockShift)),
                                Point((stepX * pcIndexX + 0.27 + le/2 + empolyxoffset + baspolyxoffset + STIoffset), (-0.85 - we/2 + leoffset + bipwinyoffset + empolyyoffset + nSDBlockShift)),
                                Point((stepX * pcIndexX - 0.27 - le/2 - empolyxoffset - baspolyxoffset - STIoffset), (-0.85 - we/2 + leoffset + bipwinyoffset + empolyyoffset + nSDBlockShift)),
                                Point((stepX * pcIndexX - 0.52 - le/2 - empolyxoffset - baspolyxoffset - STIoffset), (-0.6 - we/2 + leoffset + bipwinyoffset + empolyyoffset + nSDBlockShift)),
                                Point((stepX * pcIndexX - 0.52 - le/2 - empolyxoffset - baspolyxoffset - STIoffset), (0.03 + we/2 + leoffset + bipwinyoffset + empolyyoffset) ),
                                Point((stepX * pcIndexX - 0.94 - le/2 - empolyxoffset - baspolyxoffset - STIoffset), (0.45 + we/2 + leoffset + bipwinyoffset + empolyyoffset)),
                                Point((stepX * pcIndexX - 0.94 - le/2 - empolyxoffset - baspolyxoffset - STIoffset), (1.98 + we/2 + leoffset + bipwinyoffset + empolyyoffset))]))

        pcLayer = 'Metal1'
        pcInst = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(-0.89-le/2, CMetY1, stretchX+0.89+le/2, CMetY2))
        pcInst = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(-0.94-le/2, (0.57+we/2+leoffset+bipwinyoffset+empolyyoffset), stretchX+0.94+le/2, (0.81+we/2+leoffset+bipwinyoffset+empolyyoffset)))
        
        pcLayer = 'Metal2'
        pcInst = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(-0.89-le/2, (-0.32-we/2-leoffset-bipwinyoffset-empolyyoffset), stretchX+0.89+le/2, (0.335+we/2+leoffset+bipwinyoffset+empolyyoffset)))
        
        pcLayer = 'TEXT'
        pcLabelText = self.Text
        pcLabelHeight = 0.35
        pcInst = dbCreateLabel(self, Layer(pcLayer, pcPurpose), Point(0.015, (-1.86 - we/2 - leoffset - bipwinyoffset - empolyyoffset)), pcLabelText, 'centerCenter', 'R0', Font.EURO_STYLE, pcLabelHeight)
        pcInst.setDrafting(True)
