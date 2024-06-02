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
from .utility_functions import *

import math

class sealring(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        defL       = techparams['sealring_complete_defL']
        minL       = techparams['sealring_complete_minL']
        defW       = techparams['sealring_complete_defW']
        minW       = techparams['sealring_complete_minW']
        edgeBox    = techparams['sealring_complete_edgeBox']

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))

        specs('l', defL, 'Length(X-Axis)')
        specs('w', defW, 'Width(Y-Axis)')
        specs('addLabel', 'nil', 'Add sub! label', ChoiceConstraint(['nil', 't']))
        specs('addSlit', 'nil' , 'Add Slit', ChoiceConstraint(['nil', 't']))

        specs('Lmin', minL, 'Lmin')
        specs('Wmin', minW, 'Wmin')

        specs('edgeBox', edgeBox, 'EdgeSeal.boundary box away from the outer EdgeSeal.drawing')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.l = params['l']
        self.w = params['w']
        self.addLabel = params['addLabel']
        self.addSlit = params['addSlit']
        self.edgeBox = params['edgeBox']

    def genLayout(self):
        techparams = self.tech.getTechParams()
        self.techparams = techparams
        self.epsilon = techparams['epsilon1']

        addLabel = self.addLabel
        addSlit = self.addSlit

        corneroffset = self.techparams['Seal_k']
        cont_size = self.techparams['Cnt_a']
        vian_size = self.techparams['Vn_a']
        TV1_size = self.techparams['TV1_a']
        TV2_size = self.techparams['TV2_a']

        # PCell Code

        edgeBox = Numeric(self.edgeBox) * 1e6
        w = Numeric(self.w) * 1e6 + edgeBox * 2;
        l = Numeric(self.l) * 1e6 + edgeBox * 2;

        maxMetalWidth = 4.2
        maxMetalLength = maxMetalWidth * 2
        corner_width = 4.2
        metalOffset = 3 + corner_width + edgeBox
        viaOffset = 5.1 + corner_width + edgeBox
        corner_length = corner_width * 2
        corner_steps = 4
        corner_end = 28.2 + edgeBox   # end of the bottom right and top left
        corner_startx = 0 + corner_end - (corner_end - corner_width * (corner_steps + 1))
        corner_starty = 0   # start at the bottom right
        metal_startx = corner_end - (corner_end - maxMetalWidth * (corner_steps + 1)) + metalOffset
        edgeBox_startx = 0
        edgeBox_starty = 0

        # Sealring Corner
        layers = ['Activ', 'pSD', 'EdgeSeal', 'Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']
        vias = ['Cont', 'Via1', 'Via2', 'Via3', 'Via4', 'TopVia1', 'TopVia2']

        item_list = list()
        groupId   = list()

        # Passiv
        layerobj = dbCreateRect(self, Layer('Passiv', 'drawing'), Box(corner_startx + edgeBox, corner_starty + edgeBox, corner_end + edgeBox, corner_width + edgeBox))
        item_list.append(layerobj)
        layerobj = generateCorner(self, corner_startx + edgeBox, corner_starty + edgeBox, corner_width, corner_length, corner_steps, corner_end, 0, 'Passiv')
        item_list += layerobj
        groupId = combineLayerAndDelete(self, item_list, groupId, 'Passiv')

        item_list = []

        # Metals
        for layer in layers:
            layerobj = generateCorner(self, metal_startx, corner_starty, maxMetalWidth, maxMetalLength, corner_steps, corner_end, metalOffset, layer)
            groupId = combineLayerAndDelete(self, layerobj, groupId, layer)

        # Vias
        for layer in vias :
            if layer == 'TopVia1' :
                viaWidth = TV1_size
                viaLength = 4.2
            elif layer == 'TopVia2' :
                viaWidth = TV2_size
                viaLength = 4.2
            elif layer == 'Cont' :
                viaWidth = cont_size
                viaLength = 4.2
            else :
                viaWidth = vian_size
                viaLength = 4.2

            via_startx = corner_end - (corner_end - maxMetalWidth * (corner_steps + 1)) + metalOffset - maxMetalWidth/2-0.1
            layerobj = dbCreateRect(self, layer, Box(via_startx, viaOffset, via_startx+viaWidth, viaOffset+viaLength))
            cons(item_list, layerobj)

            viaGroupId = layerobj

            for cnt in range(1, corner_steps+1) :
                layerobj = dbCopyShape(viaGroupId, Point(2 * viaOffset + viaLength * cnt + viaWidth-0.1, -viaLength*(cnt-1)), 'R90')
                cons(item_list, layerobj)
                layerobj = dbCopyShape(viaGroupId, Point(-maxMetalWidth*(cnt-1), maxMetalWidth*(cnt-1)-0.1), 'R0')
                cons(item_list, layerobj)

            layerobj = dbCreateRect(self, layer, Box(via_startx, viaOffset-0.1, corner_end, viaOffset-0.1+viaWidth))
            cons(item_list, layerobj)
            layerobj = dbCreateRect(self, layer, Box(viaOffset-0.1, corner_end -  maxMetalWidth/2-0.1, viaOffset-0.1+viaWidth, corner_end))
            cons(item_list, layerobj)
            groupId = combineLayerAndDelete(self, item_list, groupId, layer)

            item_list = []

        # Copy Corners
        ihpCopyFig(groupId, Point(l, w), 'R180')
        ihpCopyFig(groupId, Point(l, 0), 'R90')
        ihpCopyFig(groupId, Point(0, w), 'R270')

        # end PCell Code

        # Straight Lines
        dbCreateRect(self, Layer('Passiv', 'drawing'), Box(edgeBox, corner_end, corner_width + edgeBox, w - corner_end))
        dbCreateRect(self, Layer('Passiv', 'drawing'), Box(corner_end, edgeBox, l - corner_end, corner_width + edgeBox))
        dbCreateRect(self, Layer('Passiv', 'drawing'), Box(l - edgeBox, corner_end, l - corner_width - edgeBox, w - corner_end))
        dbCreateRect(self, Layer('Passiv', 'drawing'), Box(corner_end, w - edgeBox, l - corner_end, w - corner_width - edgeBox))

        for layer in layers :
            dbCreateRect(self, Layer(layer, 'drawing'), Box(metalOffset, corner_end, metalOffset + corner_width, w - corner_end))
            dbCreateRect(self, Layer(layer, 'drawing'), Box(corner_end, metalOffset, l - corner_end, metalOffset + corner_width))
            dbCreateRect(self, Layer(layer, 'drawing'), Box(l - metalOffset, corner_end, l - corner_width - metalOffset, w - corner_end))
            dbCreateRect(self, Layer(layer, 'drawing'), Box(corner_end, w - metalOffset, l - corner_end, w - corner_width - metalOffset))

        for layer in vias :
            if layer == 'TopVia1' :
                viaWidth = TV1_size
                viaLength = 4.2
            elif layer == 'TopVia2' :
                viaWidth = TV2_size
                viaLength = 4.2
            elif layer == 'Cont' :
                viaWidth = cont_size
                viaLength = 4.2
            else :
                viaWidth = vian_size
                viaLength = 4.2

            dbCreateRect(self, Layer(layer, 'drawing'), Box(viaOffset-0.1, corner_end, viaOffset + viaWidth - 0.1, w - corner_end))
            dbCreateRect(self, Layer(layer, 'drawing'), Box(corner_end, viaOffset-0.1, l - corner_end, viaOffset + viaWidth - 0.1))
            dbCreateRect(self, Layer(layer, 'drawing'), Box(l - viaOffset+0.1, corner_end, l - viaWidth - viaOffset + 0.1, w - corner_end))
            dbCreateRect(self, Layer(layer, 'drawing'), Box(corner_end, w - viaOffset+0.1, l - corner_end, w - viaWidth - viaOffset + 0.1))

        # EdgeSeal box around sealring
        dbCreateRect(self, Layer('EdgeSeal', 'boundary'),
            Box(edgeBox_startx, edgeBox_starty, w, l))
