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


def default_guard_ring_active_w(techparams: dict) -> float:
    """
    Default guard-ring Activ/Metal1 width, in micrometers: a single contact
    row/column plus the minimum Activ enclosure on both sides.
    """
    cont_size = techparams['Cnt_a']
    cont_min_act_encl = techparams['Cnt_c']
    return GridFix(cont_size + 2 * cont_min_act_encl)


def cont_array_num_and_remainder(available_span: float,
                                 cont_size: float,
                                 space: float,
                                 epsilon: float) -> Tuple[int, float]:
    """
    Number of Cont and the surplus space for an array of Cont with the given
    spacing that fits into `available_span`: n cuts, (n - 2) gaps of `space`
    and one gap of the surplus span the available space exactly. Callers
    either use the surplus as one wider gap or spread it evenly over all
    gaps of the array.
    """
    # NOTE: epsilon keeps floating point noise from dropping a contact
    #       when the span fits exactly (e.g. at the minimum guard ring size)
    min_contacts = math.floor(available_span / (cont_size + space) + epsilon)
    min_span = min_contacts * cont_size + (min_contacts - 2) * space
    max_span = min_span + cont_size + space
    if available_span - max_span >= space - epsilon:
        return min_contacts + 1, available_span - max_span
    return min_contacts, available_span - min_span


def guard_ring_fill_space(techparams: dict, active_w: float) -> float:
    """
    Cont spacing for the Cont fill of the Metal1 guard ring: Cnt_b, or Cnt_b1
    once the fill becomes an array of more than Cnt_b1_nr rows and more than
    Cnt_b1_nr columns.

    The number of contact rows across the ring band decides this: the number
    of columns along the ring sides is always at least as large, so more than
    Cnt_b1_nr rows implies more than Cnt_b1_nr columns.
    """
    cont_size = techparams['Cnt_a']
    cont_space = techparams['Cnt_b']
    cont_space_array = techparams['Cnt_b1']
    cont_b1_nr = techparams['Cnt_b1_nr']
    cont_min_act_encl = techparams['Cnt_c']
    epsilon = techparams['epsilon1']

    band_span = active_w - 2 * cont_min_act_encl
    rows_across, _ = cont_array_num_and_remainder(band_span, cont_size, cont_space, epsilon)
    if rows_across > cont_b1_nr:
        return cont_space_array
    return cont_space


def min_guard_ring_span(techparams: dict, active_w: Optional[float] = None) -> float:
    """
    Single source of truth for the minimum guard-ring width/height, in micrometers,
    so that each of the four sides of the ring still gets at least one contact.

    The standalone `guard_ring` PCell declares it as a RangeConstraint, but
    KLayout does not enforce min/max values on string parameters. The
    CbGuardRingSize callback (guard_ring_cb.tcl) normally corrects too small
    values, the fallback check happens in `generate_guard_ring()` (which is
    also called directly by DeviceBase.genLayout() with computed w/h).

    The minimum span grows with the Activ/Metal1 ring width `active_w`
    (defaults to `default_guard_ring_active_w()`), taking into account the
    Cont fill spacing (`guard_ring_fill_space()`).
    """
    cont_size = techparams['Cnt_a']
    cont_min_act_encl = techparams['Cnt_c']
    if active_w is None:
        active_w = default_guard_ring_active_w(techparams)
    fill_space = guard_ring_fill_space(techparams, active_w)

    # the left/right contacts keep fill_space to the bottom/top contacts,
    # which end cont_min_act_encl before the inner edge of the ring
    return GridFix(2 * (active_w - cont_min_act_encl + fill_space) + cont_size)


class GuardRingMetalStack:
    """
    Metal/via stack of the guard ring, from Activ up to a selectable top metal
    (Metal1..Metal5).

    Per via level it bundles the cut layer name with the via rules (cut size,
    spacing, metal enclosures), taken from the tech parameters. Via1 has its
    own rules (V1_*), Via2..Via4 share the generic metal via rules (Vn_*)
    according to sg13_tech_info.py. The metal rings are drawn on every metal
    layer of the stack, so that the stacked vias make the ring an LVS-clean
    connected net from Activ/Metal1 up to the top metal.
    """

    TOP_LAYER_CHOICES = ['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5']

    def __init__(self, techparams: dict, top_layer: str = 'Metal1'):
        self.techparams = techparams
        if top_layer not in self.TOP_LAYER_CHOICES:
            raise ValueError(
                f"guard ring: unsupported top layer '{top_layer}' "
                f"(expected one of {self.TOP_LAYER_CHOICES})"
            )
        self.top_layer = top_layer

        # NOTE: in SG13G2_CMOS5L, this file is reused (symlinked) and that
        #       simplified process has no Metal5
        if self.num_metals() > 4 and techparams['techName'] != 'SG13G2':
            raise ValueError(
                "guard ring: top_layer 'Metal5' is only available in SG13G2"
            )

    def num_metals(self) -> int:
        """Number of metal layers of the stack (1..5)."""
        return self.TOP_LAYER_CHOICES.index(self.top_layer) + 1

    def metal_layer_name(self, level: int) -> str:
        """Layer name of the metal at the given stack level (1-based)."""
        return f'Metal{level}'

    def via_info(self, level: int) -> dict:
        """
        Via rules between Metal<level> and Metal<level+1> (level is 1-based):
        cut layer name, cut size, cut spacings and enclosures in the metals.
        """
        techparams = self.techparams
        if level == 1:
            # Via1 (Metal1 -> Metal2)
            return {'layer': 'Via1',
                    'size': techparams['V1_a'],
                    'space': techparams['V1_b'],
                    'space_array': techparams['V1_b1'],
                    'space_array_nr': techparams['V1_b1_nr'],
                    'enc_bottom': techparams['V1_c'],
                    'enc_bottom_endcap': techparams['V1_c1'],
                    'enc_top': techparams['Vn_c'],
                    'enc_top_endcap': techparams['Vn_c1']}
        # Via2..Via4 (Metal2 -> Metal3 .. Metal4 -> Metal5)
        return {'layer': f'Via{level}',
                'size': techparams['Vn_a'],
                'space': techparams['Vn_b'],
                'space_array': techparams['Vn_b1'],
                'space_array_nr': techparams['Vn_b1_nr'],
                'enc_bottom': techparams['Vn_c'],
                'enc_bottom_endcap': techparams['Vn_c1'],
                'enc_top': techparams['Vn_c'],
                'enc_top_endcap': techparams['Vn_c1']}


def min_guard_ring_active_w(techparams: dict, top_layer: str = 'Metal1') -> float:
    """
    Minimum Activ/Metal1 guard-ring width, in micrometers, so that a Cont and
    the vias of the metal stack still fit with their enclosures into the ring
    on every layer.
    """
    cont_size = techparams['Cnt_a']
    cont_min_act_encl = techparams['Cnt_c']
    min_metal1_width = techparams['M1_a']          # Min Metal1 Width
    min_metal1_cont_encl = techparams['M1_c1']     # Min. Metal1 endcap enclosure of Cont

    stack = GuardRingMetalStack(techparams, top_layer)

    # width needed by the widest via of the stack plus its metal enclosures
    min_via_w = 0.0
    for level in range(1, stack.num_metals()):
        via = stack.via_info(level)
        enclosure = max(via['enc_bottom'], via['enc_bottom_endcap'],
                        via['enc_top'], via['enc_top_endcap'])
        min_via_w = max(min_via_w, via['size'] + 2 * enclosure)

    # upper metals follow the generic metal rules (Mn_a)
    min_metal_width = min_metal1_width
    if stack.num_metals() > 1:
        min_metal_width = max(min_metal_width, techparams['Mn_a'])

    return max(default_guard_ring_active_w(techparams),               # Activ enclosure of Cont
               cont_size + 2 * min_metal1_cont_encl,                  # Metal1 enclosure of Cont
               min_metal1_width,                                      # Min Metal1 width
               min_via_w,                                             # Via of the stack in the band
               min_metal_width)                                       # Min upper metal width


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
                        y_center: float,
                        active_w: Optional[float] = None,
                        top_layer: str = 'Metal1'):
    dlo_gen.grid = dlo_gen.tech.getGridResolution()
    techparams = dlo_gen.tech.getTechParams()

    if active_w is None:
        active_w = default_guard_ring_active_w(techparams)

    metal_stack = GuardRingMetalStack(techparams, top_layer)

    min_span = min_guard_ring_span(techparams, active_w)
    if w < min_span or h < min_span:
        raise ValueError(
            f"generate_guard_ring: width/height must be >= "
            f"{min_span}um (got w={w}um, h={h}um)"
        )

    #*************************************************************************
    #*
    #* Tech Layer Stack capabilities
    #*
    #*************************************************************************

    # NOTE: in SG13G2_CMOS5L, this file is reused (symlinked)
    #       that simplified process does not have nBuLay
    nbulay_available = techparams['techName'] == 'SG13G2' # and not 'SG13G2_CMOS5L'

    #*************************************************************************
    #*
    #* Layer Definitions
    #*
    #*************************************************************************

    sub = Layer('Substrate', 'drawing')
    nwell = Layer('NWell', 'drawing')
    
    if nbulay_available:
        nbulay = Layer('nBuLay', 'drawing')
      
    activ = Layer('Activ', 'drawing')
    psd = Layer('pSD', 'drawing')
    cont = Layer('Cont', 'drawing')
    met1 = Layer('Metal1', 'drawing')
    met1_pin = Layer('Metal1','pin')
    text = Layer('TEXT', 'drawing')

    # upper metals and vias of the stack (Metal2..Metal5, Via1..Via4)
    metal_layers = [met1]
    via_layers = []
    for level in range(2, metal_stack.num_metals() + 1):
        metal_layers.append(Layer(metal_stack.metal_layer_name(level), 'drawing'))
    for level in range(1, metal_stack.num_metals()):
        via_layers.append(Layer(metal_stack.via_info(level)['layer'], 'drawing'))
    
    #*************************************************************************
    #*
    #* Generic Design Rule Definitions
    #*
    #*************************************************************************

    epsilon = techparams['epsilon1']         # for rounding purposes
    cont_size = techparams['Cnt_a']          # Cont width
    cont_space = techparams['Cnt_b']         # Min. Cont space
    cont_space_array = techparams['Cnt_b1']         # Cont space for large arrays
    cont_space_array_nr = techparams['Cnt_b1_nr']   # rows/cols threshold for cont_space_array
    cont_min_act_encl = techparams['Cnt_c']  # Min. Activ enclosure of Cont
    ndiff_over = techparams['NW_e']     # Minimum NWell enclosure of NWell tie
                                        # surrounded entirely by NWell in N+Activ1
    pdiffx_over = techparams['pSD_c1']  # pSD enc. of p+Activ in pWell
    
    if nbulay_available:
        nbulay_min_w = techparams['NBL_a']  # Min nBulLay width

    min_metal1_width = techparams['M1_a']  # Min Metal1 Width
    min_metal1_cont_encl = techparams['M1_c1']  # Min. Metal1 endcap enclosure of Cont

    #*************************************************************************
    #*
    #* Main body of code
    #*
    #*************************************************************************

    # Activ and Metal1 guard ring width, parameterizable
    wguard_active = active_w
    wguard_met1 = wguard_active

    min_active_w = min_guard_ring_active_w(techparams, top_layer)
    if active_w < min_active_w - epsilon:
        raise ValueError(
            f"generate_guard_ring: active_w must be >= "
            f"{min_active_w}um for top_layer '{top_layer}' (got {active_w}um)"
        )

    if nbulay_available:
        # nBuLay ring width grows with the Activ width, keeping the enclosure
        # of the default ring (and never getting narrower than the minimum
        # nBuLay width, since active_w >= default_guard_ring_active_w)
        nbulay_over = max(0.0, (nbulay_min_w - default_guard_ring_active_w(techparams)) / 2.0)

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
        drawn_metal_levels = [1]

        #*********************************************************************
        #* The whole metal stack of the ring is filled with a lattice of cuts
        #* (Cont and Via1..Via4):
        #*   - cuts keep the minimum enclosure to every metal/Activ ring edge
        #*   - cut spacing is <space>, or <space_array> once the fill becomes
        #*     an array of more than <space_array_nr> rows and columns
        #*********************************************************************

        def draw_cut_fill(cut_lyr: Layer,
                          cut_size: float,
                          cut_space: float,
                          cut_space_array: float,
                          cut_space_array_nr: int,
                          enclosure: float):
            # NOTE: the enclosure is the same on all four ring edges; it is
            #       the maximum of the enclosure/endcap rules of the two
            #       layers connected by the cut
            fill_space = cut_space
            band_span = width - 2 * enclosure
            # NOTE: the epsilon lets an exactly-fitting cut through despite
            #       floating point noise (at the minimum ring width the band
            #       span equals the cut size, e.g. 0.3um - 2*0.07um evaluates
            #       to slightly less than 0.16um)
            if band_span < cut_size - epsilon:
                # cuts do not fit into the band cross-section
                return

            rows_across, _ = cont_array_num_and_remainder(band_span, cut_size,
                                                          cut_space, epsilon)
            if rows_across > cut_space_array_nr:
                fill_space = cut_space_array
            pitch = cut_size + fill_space

            # contacts across the band (rows of the bottom/top bands, columns
            # of the left/right bands), centered in the band cross-section
            def across_coords(band_lo: float) -> List[float]:
                n, _ = cont_array_num_and_remainder(band_span, cut_size, fill_space, epsilon)
                length = n * cut_size + (n - 1) * fill_space
                first = band_lo + enclosure + (band_span - length) / 2.0
                return [first + k * pitch for k in range(n)]

            # contacts along the ring, starting at the enclosure edge; the
            # surplus space is spread evenly over all gaps, keeping the row
            # uniform (instead of one wider gap in the middle)
            def along_coords(start: float, span_len: float) -> List[float]:
                n, remainder = cont_array_num_and_remainder(span_len, cut_size,
                                                            fill_space, epsilon)
                coords: List[float] = []
                if n < 1:
                    return coords
                # every gap keeps at least fill_space; the surplus on top of
                # it is shared equally, so the row ends exactly at
                # start + span_len with all gaps of equal width
                gap = fill_space
                if n > 1:
                    gap += (remainder - fill_space) / (n - 1)
                for k in range(n):
                    coords.append(start + k * (cut_size + gap))
                return coords

            # bottom/top bands: cut rows across the band, columns along the
            # full ring width (including the corners)
            bottom_rows = across_coords(yb)
            top_rows = across_coords(yt - width)
            x_coords = along_coords(xl + enclosure, xr - xl - 2 * enclosure)

            # left/right bands: cut columns across the band, rows along the
            # ring height, keeping fill_space to the bottom/top band cuts
            y_start = bottom_rows[-1] + cut_size + fill_space
            y_span = top_rows[0] - fill_space - y_start
            # NOTE: no fit check needed here; cont_array_num_and_remainder()
            #       yields no cuts for spans that are too small or negative,
            #       and its epsilon already tolerates an exactly-fitting cut
            y_coords = along_coords(y_start, y_span)

            left_cols = across_coords(xl)
            right_cols = across_coords(xr - width)

            for y in bottom_rows + top_rows:
                for x in x_coords:
                    cut_box = Box(x, y, x + cut_size, y + cut_size)
                    dbCreateRect(dlo_gen, cut_lyr, cut_box)

            for y in y_coords:
                for x in left_cols + right_cols:
                    cut_box = Box(x, y, x + cut_size, y + cut_size)
                    dbCreateRect(dlo_gen, cut_lyr, cut_box)

        # Cont fill of the Activ/Metal1 ring
        draw_cut_fill(cont, cont_size, cont_space, cont_space_array,
                      cont_space_array_nr, cont_min_act_encl)
        # upper metal rings and the via fills between adjacent metals
        for level in range(1, metal_stack.num_metals()):
            via = metal_stack.via_info(level)
            enclosure = max(via['enc_bottom'], via['enc_bottom_endcap'],
                            via['enc_top'], via['enc_top_endcap'])
            # the ring on the upper metal of this via, if not drawn yet
            if level + 1 > len(drawn_metal_levels):
                draw_ring(metal_layers[level], xl, yb, xr, yt, wguard_met1, 0.0)
                drawn_metal_levels.append(level + 1)
            draw_cut_fill(via_layers[level - 1], via['size'], via['space'],
                          via['space_array'], via['space_array_nr'], enclosure)

    def draw_label(label: Tuple[Layer, str],
                   label_point: Point):
        label_lyr, label_txt = label
        dbCreateLabel(dlo_gen, label_lyr, label_point, label_txt, 'centerCenter',
                     'R0', Font.EURO_STYLE, cont_size)

    def draw_ring(lyr: Layer,
                  xl: float, yb: float, xr: float, yt: float,
                  width: float,
                  over: float,
                  label: Optional[Tuple[Layer, str]] = None):
        box_bottom = Box(xl - over,         yb - over,         xr + over,         yb + width + over)
        box_top    = Box(xl - over,         yt - width - over, xr + over,         yt + over)
        box_left   = Box(xl - over,         yb + width + over, xl + width + over, yt - width - over)
        box_right  = Box(xr - width - over, yb + width + over, xr + over,         yt - width - over)

        if label is not None:
            label_point = box_bottom.getCenter()
            draw_label(label, label_point)

        mlist = ulist[Rect]()
        mlist += [
            dbCreateRect(dlo_gen, lyr, box_bottom),
            dbCreateRect(dlo_gen, lyr, box_top),
            dbCreateRect(dlo_gen, lyr, box_left),
            dbCreateRect(dlo_gen, lyr, box_right),
        ]
        dbLayerOrList(lyr, mlist)
        # NOTE: dbLayerOrList already destroys the first shape
        for shape in mlist[1:]:
            dbDeleteObject(shape)

    def draw_well_box(lyr: Layer,
                      xl: float, yb: float, xr: float, yt: float,
                      over: float,
                      label: Optional[Tuple[Layer, str]] = None):
        box = Box(xl - over, yb - over, xr + over, yt + over)
        dbCreateRect(dlo_gen, lyr, box)

        if label is not None:
            label_point = box.getCenter()
            draw_label(label, label_point)

    draw_contacted_ring(xl, yb, xr, yt, wguard_met1)
    
    if guard_ring_type == 'nwell':
        if nbulay_available:
            draw_well_box(nwell, xl, yb, xr, yt, max(nbulay_over, ndiff_over), label=(nwell, 'well'))
            draw_ring(activ, xl, yb, xr, yt, wguard_active, 0.0, label=(text, 'well'))
            draw_ring(nbulay, xl, yb, xr, yt, wguard_active, nbulay_over)
        else:
            draw_well_box(nwell, xl, yb, xr, yt, ndiff_over, label=(nwell, 'well'))
            draw_ring(activ, xl, yb, xr, yt, wguard_active, 0.0, label=(text, 'well'))

    # elif guard_ring_type == 'dnwell':
    #     draw_well_box(nwell, xl, yb, xr, yt, wguard, nbulay_over)
    #     draw_well_box(nbulay, xl, yb, xr, yt, wguard, nbulay_over)
    elif guard_ring_type == 'psub':
        draw_ring(sub, xl, yb, xr, yt, wguard_active, pdiffx_over, label=(sub, 'sub!'))
        draw_ring(psd, xl, yb, xr, yt, wguard_active, pdiffx_over)
        draw_ring(activ, xl, yb, xr, yt, wguard_active, 0.0, label=(text, 'sub!'))


class guard_ring(DloGen):
    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()
        default_active_w = default_guard_ring_active_w(techparams)
        min_active_w = min_guard_ring_active_w(techparams)
        min_span = min_guard_ring_span(techparams) * 1e-6

        specs('type', 'nwell', 'Guard Ring Type', ChoiceConstraint(['nwell', 'psub']))  # 'dnwell'
        specs('w', '3.05u', 'Width', RangeConstraint(min_span, None))
        specs('h', '3.05u', 'Height', RangeConstraint(min_span, None))
        specs('active_w', f'{default_active_w}u', 'Activ/Metal1 Width',
              RangeConstraint(min_active_w * 1e-6, None))
        specs('top_layer', 'Metal1', 'Top Layer',
              ChoiceConstraint(GuardRingMetalStack.TOP_LAYER_CHOICES))

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.type = params['type']
        self.w = Numeric(params['w'])*1e6
        self.h = Numeric(params['h'])*1e6
        self.active_w = Numeric(params['active_w'])*1e6
        self.top_layer = params['top_layer']

    def genLayout(self):
        generate_guard_ring(dlo_gen=self,
                            guard_ring_type=self.type,
                            w=self.w,
                            h=self.h,
                            x_center=0.0,
                            y_center=0.0,
                            active_w=self.active_w,
                            top_layer=self.top_layer)
