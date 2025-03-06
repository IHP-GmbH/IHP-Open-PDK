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

__version__ = "$Revision: #3 $"

from cni.dlo import *
from .geometry import *
from .utility_functions import *

import math

class NoFillerStack(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):   
        techparams = specs.tech.getTechParams()
        
        minLW      = '10n'
        defLW      = '10u' 
        
#ifdef KLAYOUT
        specs('w', defLW, 'Width')
        specs('l', defLW, 'Length')
        specs('minLW', minLW, 'w/l min')
        
        specs('noAct', 'Yes', 'no Activ filler', ChoiceConstraint(['Yes', 'No']))
        specs('noGP',  'Yes', 'no GatPoly filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM1',  'Yes', 'no M1 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM2',  'Yes', 'no M2 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM3',  'Yes', 'no M3 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM4',  'Yes', 'no M4 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM5',  'Yes', 'no M5 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noTM1', 'Yes', 'no TM1 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noTM2', 'Yes', 'no TM2 filler', ChoiceConstraint(['Yes', 'No']))
#else
        CDFVersion = techparams['CDFVersion']
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        
        specs('w', defLW, 'Width')
        specs('l', defLW, 'Length')
        specs('minLW', minLW, 'w/l min')
        
        specs('noAct', 'Yes', 'no Activ filler', ChoiceConstraint(['Yes', 'No']))
        specs('noGP',  'Yes', 'no GatPoly filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM1',  'Yes', 'no M1 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM2',  'Yes', 'no M2 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM3',  'Yes', 'no M3 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM4',  'Yes', 'no M4 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noM5',  'Yes', 'no M5 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noTM1', 'Yes', 'no TM1 filler', ChoiceConstraint(['Yes', 'No']))
        specs('noTM2', 'Yes', 'no TM2 filler', ChoiceConstraint(['Yes', 'No']))
#endif

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.w = params['w']
        self.l = params['l']
        self.noAct = params['noAct']
        self.noGP = params['noGP']
        self.noM1 = params['noM1']
        self.noM2 = params['noM2']
        self.noM3 = params['noM3']
        self.noM4 = params['noM4']
        self.noM5 = params['noM5']
        self.noTM1 = params['noTM1']
        self.noTM2 = params['noTM2']

    def genLayout(self):
        w = self.w
        l = self.l
        noAct = self.noAct
        noGP  = self.noGP
        noM1  = self.noM1
        noM2  = self.noM2
        noM3  = self.noM3
        noM4  = self.noM4
        noM5  = self.noM5
        noTM1 = self.noTM1
        noTM2 = self.noTM2

        L = Numeric(l)*1e6;
        W = Numeric(w)*1e6;
        
        if noAct == 'Yes' :
            dbCreateRect(self, Layer('Activ', 'nofill'), Box(0, 0, W, L))
            
        if noGP == 'Yes' :
            dbCreateRect(self, Layer('GatPoly', 'nofill'), Box(0, 0, W, L))
            
        if noM1 == 'Yes' :
            dbCreateRect(self, Layer('Metal1', 'nofill'), Box(0, 0, W, L))
            
        if noM2 == 'Yes' :
            dbCreateRect(self, Layer('Metal2', 'nofill'), Box(0, 0, W, L))
            
        if noM3 == 'Yes' :
            dbCreateRect(self, Layer('Metal3', 'nofill'), Box(0, 0, W, L))
            
        if noM4 == 'Yes' :
            dbCreateRect(self, Layer('Metal4', 'nofill'), Box(0, 0, W, L))
            
        if noM5 == 'Yes' :
            dbCreateRect(self, Layer('Metal5', 'nofill'), Box(0, 0, W, L))
            
        if noTM1 == 'Yes' :
            dbCreateRect(self, Layer('TopMetal1', 'nofill'), Box(0, 0, W, L))
            
        if noTM2 == 'Yes' :
            dbCreateRect(self, Layer('TopMetal2', 'nofill'), Box(0, 0, W, L))
            
