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
from .utility_functions import *
from .rfmosfet_base_code import rfmosfet_base

class rfpmos(rfmosfet_base):
    Cell = 'rfpmos'
    
    @classmethod
    def defineParamSpecs(self, specs):
        techparams = specs.tech.getTechParams()
        
        model      = techparams[self.Cell+'_model']
        defL       = techparams[self.Cell+'_defL']
        defW       = techparams[self.Cell+'_defW']
        defNG      = techparams[self.Cell+'_defNG']
        minL       = techparams[self.Cell+'_minL']
        minW       = techparams[self.Cell+'_minW']
        
#ifdef KLAYOUT
        specs('rfmode', 1, 'rfmode')
        specs('model', model, 'Model name')
        
        specs('w' ,   defW, 'Width')
        specs('ws',   eng_string(Numeric(defW)/Numeric(defNG)), 'SingleWidth')
        specs('l' ,   defL, 'Length')
        specs('ng',   defNG, 'Number of Gates')
        specs('calculate',   True, 'Calculate as,ad,ps,pd')
        specs('cnt_rows', 1, 'Contact rows')
        specs('Met2Cont', 'Yes', 'Metal2 contact', ChoiceConstraint(['Yes', 'No']))
        specs('gat_ring', 'Yes', 'Gate ring', ChoiceConstraint(['Yes', 'No']))
        specs('guard_ring', 'Yes', 'Guard ring', ChoiceConstraint(['Yes', 'No', 'U', 'Top+Bottom']))
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
#else        
        CDFVersion = techparams['CDFVersion']
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('rfmode', 1, 'rfmode')
        specs('model', model, 'Model name')
        
        specs('w' ,   defW, 'Width')
        specs('ws',   eng_string(Numeric(defW)/Numeric(defNG)), 'SingleWidth')
        specs('l' ,   defL, 'Length')
        specs('ng',   defNG, 'Number of Gates')
        specs('calculate',   True, 'Calculate as,ad,ps,pd')
        specs('cnt_rows', 1, 'Contact rows')
        specs('Met2Cont', 'Yes', 'Metal2 contact', ChoiceConstraint(['Yes', 'No']))
        specs('gat_ring', 'Yes', 'Gate ring', ChoiceConstraint(['Yes', 'No']))
        specs('guard_ring', 'Yes', 'Guard ring', ChoiceConstraint(['Yes', 'No', 'U', 'Top+Bottom']))
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')
#endif
    
    def genLayout(self):
        super(rfpmos, self).genLayout()
