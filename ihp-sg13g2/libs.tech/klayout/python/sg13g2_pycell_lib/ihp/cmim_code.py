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
from .utility_functions import *
from .geometry import *

class cmim(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        # define parameters and default values
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        minLW      = techparams['cmim_minLW']
        defLW      = techparams['cmim_defLW']
        caspec     = techparams['cmim_caspec']
        cmax       = techparams['cmim_maxC']
        model      = techparams['cmim_model']

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('Calculate', 'w&l', 'Calculate', ChoiceConstraint(['C', 'w', 'l', 'w&l']))
        specs('model', model, 'Model name')

        C = CbCapCalc('C', 0, Numeric(defLW), Numeric(defLW), 'cmim')
        specs('C', eng_string(C), 'C')

        specs('w', defLW, 'Width')
        specs('l', defLW, 'Length')

        specs('Cspec', caspec, 'Cspec [F/sqm]')
        specs('Wmin', minLW, 'Wmin')
        specs('Lmin', minLW, 'Lmin')
        specs('Cmax', cmax, 'Cmax')

        specs('ic', '', 'Initial condition')
        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')

    def setupParams(self, params):
        # process parameter values entered by user
        self.w = eng_string_to_float(params['w'])*1e6
        self.l = eng_string_to_float(params['l'])*1e6

    def genLayout(self):
        self.grid = self.tech.getGridResolution()
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']

        self.generateVias()

        # generate rectangle layout
        x1 = self.techparams['Mim_d']-self.techparams['TV1_d']+self.xoffset
        x2 = self.xcont_cnt
        y1 = self.techparams['Mim_d']-self.techparams['TV1_d']+self.yoffset
        y2 = self.ycont_cnt
        caplayerBBox = Box(0, 0, self.w, self.l)
        topMetalBBox = Box(x1, y1, x2, y2)
        bottomMetalBBox = Box(-self.techparams['Mim_c'], -self.techparams['Mim_c'], self.w + self.techparams['Mim_c'], self.l + self.techparams['Mim_c'])

        Rect(Layer('MIM'), caplayerBBox)
        self.bottomMetal = Rect(Layer('Metal5'), bottomMetalBBox)
        self.topMetal= Rect(Layer('TopMetal1'), topMetalBBox)

        self.createPins()

    def createPins(self):
        self.addPin('PLUS', 'PLUS', self.topMetal.getBBox(), Layer('TopMetal1','pin'))
        self.addPin('MINUS', 'MINUS', self.bottomMetal.getBBox(), Layer('Metal5','pin'))

    def generateVias(self):
        cont_over = self.techparams['Mim_d']
        cont_dist = 0.84
        cont_size = self.techparams['TV1_a']

        xanz=((self.w-cont_over-cont_over+cont_dist)//(cont_size+cont_dist)+self.epsilon)
        w1 = xanz*(cont_size+cont_dist)-cont_dist+cont_over+cont_over
        self.xoffset=GridFix((self.w-w1)/2)

        yanz = ((self.l-cont_over-cont_over+cont_dist)//(cont_size+cont_dist)+self.epsilon)
        l1=yanz*(cont_size+cont_dist)-cont_dist+cont_over+cont_over
        self.yoffset=GridFix((self.l-l1)/2)

        ycont_cnt=cont_over+self.yoffset
        while ycont_cnt+cont_size+cont_over <= self.l+self.epsilon:
            xcont_cnt=cont_over+self.xoffset
            while xcont_cnt+cont_size+cont_over <= self.w+self.epsilon:
                via = Box(xcont_cnt, ycont_cnt, xcont_cnt+cont_size, ycont_cnt+cont_size)
                Rect(Layer('Vmim'), via)
                xcont_cnt=xcont_cnt+cont_size+cont_dist

            ycont_cnt=ycont_cnt+cont_size+cont_dist
        self.xcont_cnt=xcont_cnt+self.techparams['TV1_d']-cont_dist
        self.ycont_cnt=ycont_cnt+self.techparams['TV1_d']-cont_dist
