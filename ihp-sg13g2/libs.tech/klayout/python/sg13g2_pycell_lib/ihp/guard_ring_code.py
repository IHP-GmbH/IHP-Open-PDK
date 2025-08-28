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
from typing import List

__version__ = '$Revision: #3 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *


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
    DNWELL = 'dnwell'
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

    cont_size = techparams['Cnt_a']
    cont_space = techparams['Cnt_b']
    ndiff_over = techparams['NW_e']  # Minimum NWell enclosure of NWell tie
                                          # surrounded entirely by NWell in N+Activ1
    pdiffx_over = techparams['pSD_c1']  # pSD enc. of p+Activ in pWell
    nbulay_min_w = techparams['NBL_a']  # Min nBulLay width

    #*************************************************************************
    #*
    #* Main body of code
    #*
    #*************************************************************************

    wguard = cont_size * 2  # metal1 guardring width
    met1_w1 = wguard

    h_cont_offset = cont_size / 2.0
    v_cont_offset = cont_space - h_cont_offset

    # guardring
    xl = -w / 2.0 + x_center
    yb = -h / 2.0 + y_center
    xr =  w / 2.0 + x_center
    yt =  h / 2.0 + y_center

    def add_metal_cont(xl: float, yb: float, xr: float, yt: float, offset: float):
        MetalCont(dlo_gen, xl, yb, xr, yt, met1, cont, met1_w1, cont_size, cont_size, offset, cont_space)

    def draw_contacted_ring(xl: float, yb: float, xr: float, yt: float, width: float):
        add_metal_cont(xl,             yb + width/2.0, xr,             yb + width/2.0, h_cont_offset)  # bottom
        add_metal_cont(xl,             yt - width/2.0, xr,             yt - width/2.0, h_cont_offset)  # top
        add_metal_cont(xl + width/2.0, yb + width,     xl + width/2.0, yt - width,     v_cont_offset)  # right
        add_metal_cont(xr - width/2.0, yb + width,     xr - width/2.0, yt - width,     v_cont_offset)  # left

    def draw_ring(lyr: Layer, xl: float, yb: float, xr: float, yt: float, width: float, over: float):
        box_bottom = Box(xl - over,         yb - over,         xr + over,         yb + width + over)
        box_top    = Box(xl - over,         yt + over,         xr + over,         yt - width - over)
        box_left   = Box(xl - over,         yb + width - over, xl + width + over, yt - width - over)
        box_right  = Box(xr - width - over, yb + width - over, xr + over,         yt - width - over)
        mlist = ulist[Rect]()
        mlist += [
            dbCreateRect(dlo_gen, lyr, box_bottom),
            dbCreateRect(dlo_gen, lyr, box_top),
            dbCreateRect(dlo_gen, lyr, box_left),
            dbCreateRect(dlo_gen, lyr, box_right),
        ]
        dbLayerOrList(lyr, mlist)

    # draw pin
    pin_box = Box(xl, yb + cont_size/2.0, xr, yb + cont_size*1.5)
    id = dbCreateRect(dlo_gen, met1_pin, pin_box)
    MkPin(dlo_gen, 'TIE', 0, id.bbox, id.layer)
    tie_label_point = pin_box.getCenter()
    dbCreateLabel(dlo_gen, text, tie_label_point, 'TIE', 'centerCenter', 'R0', Font.EURO_STYLE, cont_size)

    draw_contacted_ring(xl, yb, xr, yt, wguard)

    draw_ring(activ, xl, yb, xr, yt, wguard, 0.0)

    if guard_ring_type == 'nwell':
        draw_ring(nwell, xl, yb, xr, yt, wguard, ndiff_over)
    elif guard_ring_type == 'dnwell':
        nbulay_over = (nbulay_min_w - wguard) / 2.0
        draw_ring(nwell, xl, yb, xr, yt, wguard, nbulay_over)
        draw_ring(nbulay, xl, yb, xr, yt, wguard, nbulay_over)
    elif guard_ring_type == 'psub':
        draw_ring(sub, xl, yb, xr, yt, wguard, pdiffx_over)
        draw_ring(psd, xl, yb, xr, yt, wguard, pdiffx_over)


class guard_ring(DloGen):
    @classmethod
    def defineParamSpecs(cls, specs):
        specs('type', 'ntap', 'Guard Ring Type', ChoiceConstraint(['nwell', 'dnwell', 'psub']))
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