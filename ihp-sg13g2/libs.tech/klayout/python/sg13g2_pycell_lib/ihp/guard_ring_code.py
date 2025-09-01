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

from __future__ import annotations
import sys
from typing import List, Tuple

__version__ = '$Revision: #3 $'

from cni.dlo import *

from .geometry import *
from .utility_functions import *

import math


if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum
    class StrEnum(str, Enum):
        def __str__(self) -> str:
            return str(self.value)


class GuardRingType(StrEnum):
    NONE = 'none'
    NWELL = 'nwell'
    # DNWELL = 'dnwell'
    PSUB = 'psub'

    @classmethod
    def cases(cls) -> List[GuardRingType]:
        return [c for c in cls]

    @classmethod
    def case_values(cls) -> List[str]:
        return [c.value for c in cls]


def generate_guard_ring(dlo_gen: DloGen,
                        guard_ring_type: str,
                        w: float,
                        h: float,
                        x_center: float,
                        y_center: float):
    dlo_gen.grid = dlo_gen.tech.getGridResolution()
    techparams = dlo_gen.tech.getTechParams()

    #*************************************************************************
    #*
    #* Layer Definitions
    #*
    #*************************************************************************

    sub = Layer('Substrate', 'drawing')
    nwell = Layer('NWell', 'drawing')
    nbulay = Layer('nBuLay', 'drawing')
    activ = Layer('Activ', 'drawing')
    psd = Layer('pSD', 'drawing')
    cont = Layer('Cont', 'drawing')
    met1 = Layer('Metal1', 'drawing')
    met1_pin = Layer('Metal1','pin')
    text = Layer('TEXT', 'drawing')

    #*************************************************************************
    #*
    #* Generic Design Rule Definitions
    #*
    #*************************************************************************

    cont_size = techparams['Cnt_a']          # Cont width
    cont_space = techparams['Cnt_b']         # Min. Cont space
    cont_min_act_encl = techparams['Cnt_c']  # Min. Activ enclosure of Cont
    ndiff_over = techparams['NW_e']     # Minimum NWell enclosure of NWell tie
                                        # surrounded entirely by NWell in N+Activ1
    pdiffx_over = techparams['pSD_c1']  # pSD enc. of p+Activ in pWell
    nbulay_min_w = techparams['NBL_a']  # Min nBulLay width
    min_metal1_width = techparams['M1_a']  # Min Metal1 Width
    min_metal1_cont_encl = techparams['M1_c1']  # Min. Metal1 endcap enclosure of Cont

    #*************************************************************************
    #*
    #* Main body of code
    #*
    #*************************************************************************

    wguard_active = cont_size + 2 * cont_min_act_encl

    wguard_met1 = wguard_active
    # wguard_met1 = max(cont_size, min_metal1_width) + 2 * min_metal1_cont_encl  # metal1 guardring width

    nbulay_over = (nbulay_min_w - wguard_active) / 2.0

    # guardring
    xl = -w / 2.0 + x_center
    yb = -h / 2.0 + y_center
    xr =  w / 2.0 + x_center
    yt =  h / 2.0 + y_center

    def draw_contacted_ring(xl: float, yb: float, xr: float, yt: float, width: float):
        # NOTE: xl / yb / xr / yt defines the outer bounds of the guard ring

        bottom_box = Box(xl,         yb,          xr,          yb + width)
        top_box    = Box(xl,         yt - width,  xr,          yt)
        left_box   = Box(xl,         yb + width,  xl + width,  yt - width)
        right_box  = Box(xr - width, yb + width,  xr,          yt - width)
        dbCreateRect(dlo_gen, met1, bottom_box)
        dbCreateRect(dlo_gen, met1, top_box)
        dbCreateRect(dlo_gen, met1, left_box)
        dbCreateRect(dlo_gen, met1, right_box)

        # NOTE: in case of leftover space, we adjust the offset to ensure the spacing
        #       we want to create the gap in the middle

        def num_contacts_and_remainder(available_span: float) -> Tuple[int, float]:
            min_contacts = math.floor(available_span / (cont_size + cont_space))
            min_span = min_contacts * cont_size + (min_contacts - 2) * cont_space
            max_span = min_span + cont_size + cont_space
            num_contacts: int
            remainder: float
            if available_span - max_span >= cont_space:
                remainder = available_span - max_span
                num_contacts = min_contacts + 1
            else:
                remainder = available_span - min_span
                num_contacts = min_contacts
            return num_contacts, remainder

        h_available_span = bottom_box.right - bottom_box.left - 2 * cont_min_act_encl
        v_available_span =  left_box.top - left_box.bottom + 2 * cont_min_act_encl - 2 * cont_space
        h_num_contacts, h_remainder = num_contacts_and_remainder(h_available_span)
        v_num_contacts, v_remainder = num_contacts_and_remainder(v_available_span)

        for box in (bottom_box, top_box):
            x1 = box.left + cont_min_act_encl
            y_bot = box.bottom + cont_min_act_encl
            y_top = y_bot + cont_size
            for i in range(0, h_num_contacts):
                x2 = x1 + cont_size
                contact_box = Box(x1, y_bot, x2, y_top)
                dbCreateRect(dlo_gen, cont, contact_box)
                if i + 1 == floor(h_num_contacts / 2.0):
                    x1 = x2 + h_remainder
                else:
                    x1 = x2 + cont_space

        for box in (left_box, right_box):
            y1 = box.bottom - cont_min_act_encl + cont_space
            x_left = box.left + cont_min_act_encl
            x_right = x_left + cont_size
            for i in range(0, v_num_contacts):
                y2 = y1 + cont_size
                contact_box = Box(x_left, y1, x_right, y2)
                dbCreateRect(dlo_gen, cont, contact_box)
                if i + 1 == floor(v_num_contacts / 2.0):
                    y1 = y2 + v_remainder
                else:
                    y1 = y2 + cont_space

    def draw_ring(lyr: Layer,
                  xl: float, yb: float, xr: float, yt: float,
                  width: float,
                  over: float,
                  label: Optional[Tuple[Layer, str]] = None):
        box_bottom = Box(xl - over,         yb - over,         xr + over,         yb + width + over)
        box_top    = Box(xl - over,         yt + over,         xr + over,         yt - width - over)
        box_left   = Box(xl - over,         yb + width + over, xl + width + over, yt - width - over)
        box_right  = Box(xr - width - over, yb + width + over, xr + over,         yt - width - over)

        if label is not None:
            label_lyr, label_txt = label
            label_point = box_bottom.getCenter()
            dbCreateLabel(dlo_gen, label_lyr, label_point, label_txt, 'centerCenter',
                          'R0', Font.EURO_STYLE, cont_size)

        mlist = ulist[Rect]()
        mlist += [
            dbCreateRect(dlo_gen, lyr, box_bottom),
            dbCreateRect(dlo_gen, lyr, box_top),
            dbCreateRect(dlo_gen, lyr, box_left),
            dbCreateRect(dlo_gen, lyr, box_right),
        ]
        dbLayerOrList(lyr, mlist)

    def draw_well_box(lyr: Layer, xl: float, yb: float, xr: float, yt: float,over: float):
        box = Box(xl - over, yb - over, xr + over, yt + over)
        dbCreateRect(dlo_gen, lyr, box)

    draw_contacted_ring(xl, yb, xr, yt, wguard_met1)

    if guard_ring_type == 'nwell':
        draw_well_box(nwell, xl, yb, xr, yt, ndiff_over)
        draw_ring(activ, xl, yb, xr, yt, wguard_active, 0.0, label=(text, 'well'))
        draw_ring(nbulay, xl, yb, xr, yt, wguard_active, nbulay_over)
    # elif guard_ring_type == 'dnwell':
    #     draw_well_box(nwell, xl, yb, xr, yt, wguard, nbulay_over)
    #     draw_well_box(nbulay, xl, yb, xr, yt, wguard, nbulay_over)
    elif guard_ring_type == 'psub':
        draw_ring(sub, xl, yb, xr, yt, wguard_active, pdiffx_over)
        draw_ring(psd, xl, yb, xr, yt, wguard_active, pdiffx_over)
        draw_ring(activ, xl, yb, xr, yt, wguard_active, 0.0, label=(text, 'sub!'))


class guard_ring(DloGen):
    @classmethod
    def defineParamSpecs(cls, specs):
        specs('type', 'ntap', 'Guard Ring Type', ChoiceConstraint(['nwell', 'psub']))  # 'dnwell'
        specs('w', '3.05u', 'Width')
        specs('h', '3.05u', 'Height')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.type = params['type']
        self.w = Numeric(params['w'])*1e6
        self.h = Numeric(params['h'])*1e6

    def genLayout(self):
        generate_guard_ring(dlo_gen=self,
                            guard_ring_type=self.type,
                            w=self.w,
                            h=self.h,
                            x_center=0.0,
                            y_center=0.0)