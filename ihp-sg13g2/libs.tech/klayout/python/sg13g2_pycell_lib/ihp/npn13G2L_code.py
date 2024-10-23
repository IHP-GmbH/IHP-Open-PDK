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
from .thermal import *
from .utility_functions import *

import math

class npn13G2L(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        model      = techparams['npn13G2L_model']

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')

        specs('Nx', 2, 'x-Multiplier', RangeConstraint(1, 4))
        specs('le', '1.0u', "Emitter Length")
        specs('we', '0.07u', "Emitter Width")

        specs('Icmax', '2.6m', 'Ic,max@Uce=2V (50%@0.5V)')
        specs('Iarea', '2.6m', 'Ic,max/squm@Uce=2V')
        specs('area', '1', 'Area Factor')
        specs('bn', 'sub!', 'Bulk node connection')
        specs('Vbe', '', 'Base-emitter voltage')
        specs('Vce', '', 'Collector-emitter voltage')
        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.le = params['le']
        self.Nx = params['Nx']
        self.we = params['we']

    def genLayout(self):
        le = self.le
        Nx = self.Nx
        we = self.we
        masterLib = 'SG13_dev'

        emPoly_enc_vert = 0.16
        emPoly_enc_hori = 0.13
        emWindOrigin_x = 3.865
        emWindOrigin_y = 3.1
        BiWind_enc_vert = 0.1
        BiWind_enc_hori = 0.07
        ColWind_enc_vert = 0.58
        ColWind_enc_hori = 1.515
        Activ_enc_vert = 0.28
        Activ_enc_hori = 1.365
        BasPoly_enc_vert = 0.45
        BasPoly_enc_hori = 0.58
        Col_Metal1_distance = 0.975
        Col_Metal1_width = 0.39
        Bas_Metal1_distance = 0.32
        Bas_Metal1_width = 0.16
        Emi_Metal1_enc_vert = 0.2
        Emi_Metal1_enc_hori = 0.095

        Cell = self.__class__.__name__

        le = Numeric(le)*1e6
        Nx = Numeric(Nx)
        we = Numeric(we)*1e6

        pcPurpose = 'drawing'

        id = dbCreateRect(self,Layer('EmWind', 'drawing'), Box(emWindOrigin_x, emWindOrigin_y, emWindOrigin_x + we, emWindOrigin_y + le))
        groupId = list()
        groupId.append(id)

        id = ihpAddThermalBjtLayer(self, Box((emWindOrigin_x - 0.05), (emWindOrigin_y - 0.05), (emWindOrigin_x + we + 0.05), (emWindOrigin_y + le + 0.05)), True, Cell)
        groupId.append(id)

        masks = Grouping()

        outer  = dbCreateRect(self, Layer('Activ', 'drawing'), Box(emWindOrigin_x - Activ_enc_hori, emWindOrigin_y - Activ_enc_vert, emWindOrigin_x + we + Activ_enc_hori, emWindOrigin_y + le + Activ_enc_vert))
        inner  = dbCreateRect(self, Layer('Activ', 'mask'),    Box(emWindOrigin_x - 0.705, emWindOrigin_y - Activ_enc_vert, emWindOrigin_x - Emi_Metal1_enc_hori, emWindOrigin_y + le + Activ_enc_vert))
        masks.add(inner)
        inner1 = dbCreateRect(self, Layer('Activ', 'mask'),    Box(emWindOrigin_x + we + 0.705, emWindOrigin_y - Activ_enc_vert, emWindOrigin_x +we + Emi_Metal1_enc_hori, emWindOrigin_y + le + Activ_enc_vert))
        masks.add(inner1)

        id = dbLayerXor(Layer('Activ', 'drawing'), outer, masks)
        for item in id :
            groupId.append(item)
        dbDeleteObject(outer)
        groupId.append(inner)
        groupId.append(inner1)

        # Draw contacts & Via
        id = dbCreateRect(self, Layer('Via1', 'drawing'), Box(3.805, 3, 3.995, 3.2+le))
        groupId.append(id)
        id = dbCreateRect(self, Layer('Cont', 'drawing'), Box(2.68, 2.95, 2.84, 3.25+le))
        groupId.append(id)
        id = dbCreateRect(self, Layer('Cont', 'drawing'), Box(3.82, 2.95, 3.98, 3.25+le))
        groupId.append(id)
        id = dbCreateRect(self, Layer('Cont', 'drawing'), Box(4.96, 2.95, 5.12, 3.25+le))
        groupId.append(id)

        cont_cnt = fix((le+0.21)/(0.16+0.18))

        id = dbCreateRect(self, Layer('Cont', 'drawing'), Box(3.385, 2.89, 3.545, 3.05))
        groupId.append(id)
        for cnt in range(cont_cnt) :
            id = dbCopyShape(id, Point(0, 0.34), 'R0')
            groupId.append(id)

        id = dbCreateRect(self, Layer('Cont', 'drawing'), Box(4.255, 2.89, 4.415, 3.05))
        groupId.append(id)
        for cnt in range(cont_cnt) :
            id = dbCopyShape(id, Point(0, 0.34), 'R0')
            groupId.append(id)

        # Metals
        # Metal Path upwards
        # Collector
        id = dbCreateRect(self, Layer('Metal1', 'drawing'), Box(emWindOrigin_x - Col_Metal1_distance, 2.82, emWindOrigin_x - Col_Metal1_distance - Col_Metal1_width, 4.1 + le))
        groupId.append(id)
        id = dbCreateRect(self, Layer('Metal1', 'drawing'), Box(emWindOrigin_x + we + Col_Metal1_distance, 2.82, emWindOrigin_x + we + Col_Metal1_distance + Col_Metal1_width, 4.1 + le))
        groupId.append(id)
        id = dbCreateRect(self, Layer('Metal1', 'drawing'), Box(emWindOrigin_x - Col_Metal1_distance - Col_Metal1_width, 4.1 + le, emWindOrigin_x + we + Col_Metal1_distance + Col_Metal1_width, 4.1 + le + 0.65))
        id.col = True
        groupId.append(id)

        # Basis
        id = dbCreateRect(self, Layer('Metal1', 'drawing'), Box(emWindOrigin_x - Bas_Metal1_distance, 2.1, emWindOrigin_x - Bas_Metal1_distance - Bas_Metal1_width, 3.38+le))
        groupId.append(id)
        id = dbCreateRect(self, Layer('Metal1', 'drawing'), Box(emWindOrigin_x + we + Bas_Metal1_distance, 2.1, emWindOrigin_x + we + Bas_Metal1_distance + Bas_Metal1_width, 3.38+le))
        groupId.append(id)
        id = dbCreateRect(self, Layer('Metal1', 'drawing'), Box(emWindOrigin_x - Bas_Metal1_distance - Bas_Metal1_width, 1.45, emWindOrigin_x + we + Bas_Metal1_distance + Bas_Metal1_width, 2.1))
        id.base = True
        groupId.append(id)

        # Emitter
        id = dbCreateRect(self, Layer('Metal1', 'drawing'), Box(emWindOrigin_x - Emi_Metal1_enc_hori, emWindOrigin_y - Emi_Metal1_enc_vert, emWindOrigin_x + we + Emi_Metal1_enc_hori, emWindOrigin_y + le + Emi_Metal1_enc_vert))
        groupId.append(id)
        id = dbCreateRect(self, Layer('Metal2', 'drawing'), Box(emWindOrigin_x - Col_Metal1_distance  - Col_Metal1_width, 2.9, emWindOrigin_x + Col_Metal1_distance + Col_Metal1_width + we, 3.3+le))
        id.emi = True
        groupId.append(id)

        # Draw Guardring
        pcLayer = 'TRANS'
        dbCreateRect(self, Layer('TRANS', 'drawing'), Box(0.9, 0.9, 6.9+((Nx-1)*2.8), 5.3+le))

        pcLayer = 'pSD'
        outer = dbCreateRect(self, Layer('pSD', 'drawing'), Box(0, 0, 7.8+((Nx-1)*2.8), 6.2+le))
        inner = dbCreateRect(self, Layer('pSD', 'drawing'), Box(0.9, 0.9, 7.8-0.9+((Nx-1)*2.8), 6.2-0.9+le))
        dbLayerXor(pcLayer, outer, inner)
        dbDeleteObject(outer)
        dbDeleteObject(inner)

        pcLayer = 'Activ'
        outer = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(0.2, 0.2, 7.6+((Nx-1)*2.8), 6.0+le))
        inner = dbCreateRect(self, Layer(pcLayer, pcPurpose), Box(0.7, 0.7, (7.6-0.5)+((Nx-1)*2.8), 6.0-0.5+le))
        dbLayerXor(pcLayer, outer, inner)
        dbDeleteObject(outer)
        dbDeleteObject(inner)

        pcLayer = 'TEXT'
        pcLabelText = 'Ae={0:d}*{1:d}*{2:.2f}*{3:.2f}'.format(int(Nx), 1, le, we)
        pcLabelHeight = 0.35
        pcInst = dbCreateLabel(self, Layer('TEXT', 'drawing'), Point(1.5, 1.0), pcLabelText, 'lowerLeft', 'R90', Font.EURO_STYLE, pcLabelHeight)
        pcInst.setDrafting(True)
        pcLabelText = 'npn13G2L'
        pcLabelHeight = 0.35
        pcInst = dbCreateLabel(self, Layer('TEXT', 'drawing'), Point(1.75, 1.0), pcLabelText, 'lowerLeft', 'R0', Font.EURO_STYLE, pcLabelHeight)
        pcInst.setDrafting(True)

        if self.Nx > 1 :
            id = dbCreateRect(self, Layer('Metal1', 'drawing'), Box(4.415, 1.45, 6.185, 2.1))
            id.base = True
            for cnt in range(1, self.Nx) :
                groupId = ihpCopyFig(groupId, Point(2.8, 0), 'R0')
                if cnt != self.Nx-1 :
                    id = dbCopyShape(id, Point(2.8, 0), 'R0')


        groupCol = Grouping();
        [groupCol.add(id) for id in self.getShapes() if id.col]

        groupBase = Grouping();
        [groupBase.add(id) for id in self.getShapes() if id.base]

        groupEmi = Grouping();
        [groupEmi.add(id) for id in self.getShapes() if id.emi]

        MkPin(self, 'C', 1, groupCol.getBBox(), 'Metal1')
        MkPin(self, 'B', 2, groupBase.getBBox(), 'Metal1')
        MkPin(self, 'E', 3, groupEmi.getBBox(), 'Metal2')
