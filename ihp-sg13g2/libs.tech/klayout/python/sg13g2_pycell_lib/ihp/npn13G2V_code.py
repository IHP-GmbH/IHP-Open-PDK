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
from .geometry import *
from .thermal import *
from .utility_functions import *

import math

class npn13G2V(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        model      = techparams['npn13G2V_model']

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')

        specs('Nx', 2, 'x-Multiplier', RangeConstraint(1, 8))
        specs('le', '1.0u', "Emitter Length")
        specs('we', '0.12u', "Emitter Width")

        specs('Icmax', '0.41m', 'Ic,max@Uce=2V (50%@0.5V)')
        specs('Iarea', '0.41m', 'Ic,max/squm@Uce=2V')
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

        emWindOrigin_x = 3.81
        emWindOrigin_y = 3.1
        Activ_enc_vert = 0.28
        Activ_enc_hori = 1.11
        Col_Metal1_distance = 0.79
        Col_Metal1_width = 0.32
        Bas_Metal1_distance = 0.295
        Bas_Metal1_width = 0.17
        Emi_Metal1_enc_vert = 0.28
        Emi_Metal1_enc_hori = 0.07

        Cell = self.__class__.__name__

        techparams = self.tech.getTechParams()
        self.techparams = techparams
        self.epsilon = techparams['epsilon1']

        #*************************************************************************
        #
        # Cell Properties
        #
        #*************************************************************************
        dbReplaceProp(self, 'ivCellType', 'graphic')
        dbReplaceProp(self, 'viewSubType', 'maskLayoutParamCell')
        dbReplaceProp(self, 'instNamePrefix', 'B')
        dbReplaceProp(self, 'function', 'transistor')
        dbReplaceProp(self, 'pcellVersion', '$Revision: 1.0 $')
        dbReplaceProp(self, 'pin#', 4)

        #*************************************************************************
        #
        # Pcell layers Definitions
        #
        #*************************************************************************
        l_EmWiHV  = Layer('EmWiHV', 'drawing')
        l_act     = Layer('Activ', 'drawing')
        l_actMask = Layer('Activ', 'mask')
        l_via1    = Layer('Via1', 'drawing')
        l_cont    = Layer('Cont', 'drawing')
        l_met1    = Layer('Metal1', 'drawing')
        l_met2    = Layer('Metal2', 'drawing')
        l_trans   = Layer('TRANS', 'drawing')
        l_pSD     = Layer('pSD', 'drawing')
        l_text    = Layer('TEXT', 'drawing')

        #*************************************************************************
        #
        # Generic Design Rule Definitions
        #
        #*************************************************************************
        Via1Width = techparams['V1_a']
        Via1Space = techparams['V1_b']
        m1EncVia1 = techparams['V1_c']

        #*************************************************************************
        #
        # Main body of code
        #
        #*************************************************************************
        le = Numeric(le)*1e6
        Nx = Numeric(Nx)
        we = Numeric(we)*1e6

        id = dbCreateRect(self, l_EmWiHV, Box(emWindOrigin_x, emWindOrigin_y, emWindOrigin_x + we, emWindOrigin_y + le))

        groupId = list()
        groupId.append(id)

        id =  ihpAddThermalBjtLayer(self, Box(emWindOrigin_x - 0.05, emWindOrigin_y - 0.05, emWindOrigin_x + we + 0.05, emWindOrigin_y + le + 0.05), True, Cell)
        groupId.append(id)

        outer = dbCreateRect(self, l_act, Box(emWindOrigin_x - Activ_enc_hori, emWindOrigin_y - Activ_enc_vert, emWindOrigin_x + we + Activ_enc_hori, emWindOrigin_y + le + Activ_enc_vert))
        inner = dbCreateRect(self, l_actMask, Box(emWindOrigin_x - 0.705, emWindOrigin_y - Activ_enc_vert, emWindOrigin_x - Emi_Metal1_enc_hori, emWindOrigin_y + le + Activ_enc_vert))
        inner1 = dbCreateRect(self, l_actMask, Box(emWindOrigin_x + we + 0.705, emWindOrigin_y - Activ_enc_vert, emWindOrigin_x +we + Emi_Metal1_enc_hori, emWindOrigin_y + le + Activ_enc_vert))

        id = dbLayerXorList(l_act, [outer], [inner, inner1])

        for item in id :
            groupId.append(item)

        dbDeleteObject(outer)
        groupId.append(inner)
        groupId.append(inner1)

        # Metals
        # Metal Path upwards
        # Collector
        id = dbCreateRect(self, l_met1, Box(emWindOrigin_x-Col_Metal1_distance, 2.82, emWindOrigin_x-Col_Metal1_distance-Col_Metal1_width, 4.1+le))
        groupId.append(id)
        id = dbCreateRect(self, l_met1, Box(emWindOrigin_x+we+Col_Metal1_distance, 2.82, emWindOrigin_x+we+Col_Metal1_distance+Col_Metal1_width, 4.1+le))
        groupId.append(id)
        id = dbCreateRect(self, l_met1, Box(emWindOrigin_x - Col_Metal1_distance - Col_Metal1_width, 4.1 + le, emWindOrigin_x + we + Col_Metal1_distance + Col_Metal1_width, 4.1 + le + 0.65))
        id.col = True
        groupId.append(id)

        # Basis
        id = dbCreateRect(self, l_met1, Box(emWindOrigin_x-Bas_Metal1_distance, 2.1, emWindOrigin_x-Bas_Metal1_distance-Bas_Metal1_width, 3.38+le))
        groupId.append(id)
        id = dbCreateRect(self, l_met1, Box(emWindOrigin_x+we+Bas_Metal1_distance, 2.1, emWindOrigin_x+we+Bas_Metal1_distance+Bas_Metal1_width, 3.38+le))
        groupId.append(id)
        id = dbCreateRect(self, l_met1, Box(emWindOrigin_x-Bas_Metal1_distance-Bas_Metal1_width, 1.45, emWindOrigin_x+we+Bas_Metal1_distance+Bas_Metal1_width, 2.1))
        id.base = True
        groupId.append(id)

        # Emitter
        emMet1 = dbCreateRect(self, l_met1, Box(emWindOrigin_x - Emi_Metal1_enc_hori, emWindOrigin_y - Emi_Metal1_enc_vert, emWindOrigin_x + we + Emi_Metal1_enc_hori, emWindOrigin_y + le + Emi_Metal1_enc_vert))
        groupId.append(emMet1)
        id = dbCreateRect(self, l_met2, Box(emWindOrigin_x-Col_Metal1_distance-Col_Metal1_width, 2.82, emWindOrigin_x+Col_Metal1_distance+Col_Metal1_width+we, 3.38+le))
        id.emi = True
        groupId.append(id)

        #; Draw contacts & Via
        via_cnt = int((le+0.46)/(0.19+0.22))
        id = dbCreateRect(self, l_via1, Box(3.775, 2.87, 3.965, 3.06))

        bbx= emMet1.bbox
        # 0.5 is Y offset on bottom
        viaColumn = via_cnt*Via1Width+(via_cnt-1)*Via1Space+(Via1Width+Via1Space)+0.05+m1EncVia1
        if bbx.getHeight() < viaColumn :
            via_cnt -= 1

        groupId.append(id)

        for cnt in range(via_cnt) :
            id = dbCopyShape(id, Point(0, 0.41), 'R0')
            groupId.append(id)

        id = dbCreateRect(self, l_cont, Box(3.79, 3.04, 3.95, 3.16+le))
        groupId.append(id)

        cont_cnt = fix((le+0.21)/(0.16+0.18))

        id = dbCreateRect(self, l_cont, Box(2.8, 2.89, 2.96, 3.05))
        groupId.append(id)

        for cnt in range(cont_cnt) :
            id = dbCopyShape(id, Point(0, 0.34), 'R0')
            groupId.append(id)

        id = dbCreateRect(self, l_cont, Box(3.35, 2.89, 3.51, 3.05))
        groupId.append(id)
        for cnt in range(cont_cnt) :
            id = dbCopyShape(id, Point(0, 0.34), 'R0')
            groupId.append(id)

        id = dbCreateRect(self, l_cont, Box(4.23, 2.89, 4.39, 3.05))
        groupId.append(id)
        for cnt in range(cont_cnt) :
            id = dbCopyShape(id, Point(0, 0.34), 'R0')
            groupId.append(id)

        id = dbCreateRect(self, l_cont, Box(4.78, 2.89, 4.94, 3.05))
        groupId.append(id)
        for cnt in range(cont_cnt) :
            id = dbCopyShape(id, Point(0, 0.34), 'R0')
            groupId.append(id)

        # Draw Guardring

        dbCreateRect(self, l_trans, Box(0.9, 0.9, 6.84+((Nx-1)*2.34), 5.3+le))
        outer = dbCreateRect(self, l_pSD, Box(0, 0, 7.74+((Nx-1)*2.34), 6.2+le))
        inner = dbCreateRect(self, l_pSD, Box(0.9, 0.9, (7.74-0.9)+((Nx-1)*2.34), 6.2-0.9+le))
        dbLayerXor(l_pSD, outer, inner)
        dbDeleteObject(outer)
        dbDeleteObject(inner)

        outer = dbCreateRect(self, l_act, Box(0.2, 0.2, 7.54+((Nx-1)*2.34), 6.0+le))
        inner = dbCreateRect(self, l_act, Box(0.7, 0.7, (7.54-0.5)+((Nx-1)*2.34), 6.0-0.5+le))
        dbLayerXor(l_act, outer, inner)
        dbDeleteObject(outer)
        dbDeleteObject(inner)

        pcLabelText = 'Ae={0:d}*{1:.2f}*{2:.2f}'.format(int(Nx), le, we)
        pcLabelHeight = 0.35
        pcInst = dbCreateLabel(self, l_text, Point(1.5, 1.0), pcLabelText, 'lowerLeft', 'R90', Font.EURO_STYLE, pcLabelHeight)
        pcInst.setDrafting(True)

        pcLabelText = Cell
        pcLabelHeight = 0.35
        pcInst = dbCreateLabel(self, l_text, Point(1.75, 1.0), pcLabelText, 'lowerLeft', 'R0', Font.EURO_STYLE, pcLabelHeight)
        pcInst.setDrafting(True)

        if self.Nx > 1 :
            id = dbCreateRect(self, l_met1, Box(4.395, 1.45, 5.685, 2.1))
            for cnt in range(1, self.Nx) :
                groupId = ihpCopyFig(groupId, Point(2.34, 0), 'R0')
                if cnt != self.Nx-1 :
                    id = dbCopyShape(id, Point(2.34, 0), 'R0')

        groupCol = Grouping();
        [groupCol.add(id) for id in self.getShapes() if id.col]

        groupBase = Grouping();
        [groupBase.add(id) for id in self.getShapes() if id.base]

        groupEmi = Grouping();
        [groupEmi.add(id) for id in self.getShapes() if id.emi]

        MkPin(self, 'C', 1, groupCol.getBBox(), 'Metal1')
        MkPin(self, 'B', 2, groupBase.getBBox(), 'Metal1')
        MkPin(self, 'E', 3, groupEmi.getBBox(), 'Metal2')

