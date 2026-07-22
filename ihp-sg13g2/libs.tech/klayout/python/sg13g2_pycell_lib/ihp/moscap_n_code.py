########################################################################
#
# Copyright 2026 IHP PDK Authors
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

__version__ = '$Revision: #1 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *
from .thermal import *

import math

class moscap_n(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        model = techparams['moscap_n_model']
        defL = techparams['moscap_n_defL']
        defW = techparams['moscap_n_defW']
        minL = techparams['moscap_n_minL']
        minW = techparams['moscap_n_minW']
        maxL = techparams['moscap_n_maxL']
        maxW = techparams['moscap_n_maxW']

#ifdef KLAYOUT
        specs('model', model, 'Model name')
        # Input w, l with range visible
        specs('w', defW, 'Width', RangeConstraint(Numeric(minW), Numeric(maxW)))
        specs('l', defL, 'Length', RangeConstraint(Numeric(minL), Numeric(maxL)))
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('m', '1', 'Multiplier')
#else
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')
        # Input w, l with range visible
        specs('w', defW, 'Width', RangeConstraint(Numeric(minW), Numeric(maxW)))
        specs('l', defL, 'Length', RangeConstraint(Numeric(minL), Numeric(maxL)))
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')
#endif

    def setupParams(self, params):
        # Get tech params
        techparams = self.tech.getTechParams()
        minW = Numeric(techparams['moscap_n_minW'])
        minL = Numeric(techparams['moscap_n_minL'])
        maxW = Numeric(techparams['moscap_n_maxW'])
        maxL = Numeric(techparams['moscap_n_maxL'])

        # Get user input params
        w_in = Numeric(params['w'])
        l_in = Numeric(params['l'])

        self.w = w_in * 1e6
        self.l = l_in * 1e6
        self.m = int(params['m'])

    def genLayout(self):
        cap_w = GridFix(self.w)
        cap_l = GridFix(self.l)

        techparams = self.tech.getTechParams()
        self.techparams = techparams

        #**************************************************************************
        #*
        #* Cell Properties
        #*
        #**************************************************************************
        dbReplaceProp(self, 'ivCellType', 'graphic')
        dbReplaceProp(self, 'viewSubType', 'maskLayoutParamCell')
        dbReplaceProp(self, 'instNamePrefix', 'C')
        dbReplaceProp(self, 'function', 'capacitor')
        dbReplaceProp(self, 'pcellVersion', '$Revision: 1.0 $')
        dbReplaceProp(self, 'pin#', 2)

        #**************************************************************************
        #*
        #* Layer Definitions
        #*
        #**************************************************************************
        metall_layer = Layer('Metal1')
        metall_layer_pin = Layer('Metal1', 'pin')
        active_layer = Layer('Activ')
        poly_layer = Layer('GatPoly')
        locint_layer = Layer('Cont')
        text_layer = Layer('TEXT', 'drawing')
        psd_layer = Layer('pSD')

        #**************************************************************************
        #*
        #* Generic Design Rule Definitions
        #*
        #**************************************************************************
        cont_size = techparams['Cnt_a']
        cont_space = techparams['Cnt_b']
        cont_space_a = techparams['Cnt_b1']
        cont_activ_enc = techparams['Cnt_c']
        cont_poly_enc = techparams['Cnt_d']
        cont_poly_to_activ = techparams['Cnt_e']
        cont_activ_to_poly = techparams['Cnt_f']
        cont_m1_endcap = techparams['M1_c1']
        m1_space = techparams['M1_e']
        m1_space_wide = techparams['M1_f']
        m1_long_threshold = techparams['M1_f_cr']
        gatpoly_activ_over = techparams['Gat_c']
        activ_gate_over = techparams['Act_c']
        active_space = techparams['Act_b']
        psd_activ_over = techparams['pSD_c1']
        psd_gate_space = techparams['pSD_j']
        psd_pactiv_pwell_space = techparams['pSD_d']
        model = techparams['moscap_n_model']
        m1_space_eff = m1_space_wide if cap_w >= m1_long_threshold else m1_space

        #**************************************************************************
        #*
        #* Main body of code
        #*
        #**************************************************************************
        core_left = 0
        core_bottom = 0
        core_right = cap_l
        core_top = cap_w

        #**************************************************************************
        #*
        #* Core Gate - Active(N+) Stack
        #*
        #**************************************************************************

        # Gate contacts : top and bottom
        gate_cont_left = cont_poly_enc
        gate_cont_right = core_right - cont_poly_enc
        top_gate_cont_bottom = core_top + cont_poly_to_activ
        top_gate_cont_top = top_gate_cont_bottom + cont_size
        contactArray(
            self, None, locint_layer, gate_cont_left, top_gate_cont_bottom,
            gate_cont_right, top_gate_cont_top, 0, 0, cont_size, cont_space
        )

        bottom_gate_cont_top_m1 = core_bottom - cont_poly_to_activ
        bottom_gate_cont_bottom = bottom_gate_cont_top_m1 - cont_size
        contactArray(
            self, None, locint_layer, gate_cont_left, bottom_gate_cont_bottom,
            gate_cont_right, bottom_gate_cont_top_m1, 0, 0, cont_size, cont_space
        )

        # Gate contacts metal overlay : top and bottom
        gate_m1_left = gate_cont_left - cont_m1_endcap
        gate_m1_right = gate_cont_right + cont_m1_endcap
        top_gate_m1_bottom = top_gate_cont_bottom - cont_m1_endcap
        top_gate_m1_top = top_gate_cont_top + cont_m1_endcap
        dbCreateRect(self, metall_layer, Box(
            gate_m1_left, top_gate_m1_bottom,
            gate_m1_right, top_gate_m1_top
        ))
        bottom_gate_cont_m1_bottom = bottom_gate_cont_bottom - cont_m1_endcap
        bottom_gate_cont_top_m1 = bottom_gate_cont_top_m1 + cont_m1_endcap
        dbCreateRect(self, metall_layer, Box(
            gate_m1_left, bottom_gate_cont_m1_bottom,
            gate_m1_right, bottom_gate_cont_top_m1
        ))

        # Create pin G
        MkPin(self, 'G', 0, Box(
            gate_m1_left, top_gate_m1_bottom,
            gate_m1_right, top_gate_m1_top
        ), metall_layer_pin)

        # Draw gate poly
        gate_ext = max(cont_poly_to_activ + cont_size + cont_poly_enc, gatpoly_activ_over)
        gate_top = core_top + gate_ext
        gate_bottom = core_bottom - gate_ext
        dbCreateRect(self, poly_layer, Box(
            core_left, gate_bottom,
            core_right, gate_top
        ))

        # N+ contacts: right and left
        v_offset_gate_bottom_act_bottom_m1 = max(
            m1_space_eff - (core_bottom - bottom_gate_cont_top_m1) + cont_m1_endcap,
            cont_activ_enc
        )

        act_cont_bottom = core_bottom + v_offset_gate_bottom_act_bottom_m1

        act_cont_top = core_top - v_offset_gate_bottom_act_bottom_m1
        right_act_cont_left = core_right + cont_activ_to_poly
        right_act_cont_right = right_act_cont_left + cont_size
        contactArray(
            self, None, locint_layer, right_act_cont_left, act_cont_bottom,
            right_act_cont_right, act_cont_top, 0, 0, cont_size, cont_space
        )

        left_act_cont_right = core_left - cont_activ_to_poly
        left_act_cont_left = left_act_cont_right - cont_size
        contactArray(
            self, None, locint_layer, left_act_cont_left, act_cont_bottom,
            left_act_cont_right, act_cont_top, 0, 0, cont_size, cont_space
        )

        # N+ contacts m1 overaly: right and left
        act_m1_top = act_cont_top + cont_m1_endcap
        act_m1_bottom = act_cont_bottom - cont_m1_endcap
        right_act_m1_left = right_act_cont_left - cont_m1_endcap
        right_act_m1_right = right_act_cont_right + cont_m1_endcap
        left_act_m1_left = left_act_cont_left - cont_m1_endcap
        left_act_m1_right = left_act_cont_right + cont_m1_endcap

        # core active
        active_ext = max(cont_activ_to_poly + cont_size + cont_activ_enc, activ_gate_over)
        active_left = core_left - active_ext
        active_right = core_right + active_ext
        dbCreateRect(self, active_layer, Box(
            active_left, core_bottom,
            active_right, core_top
        ))

        #**************************************************************************
        #*
        #* Sub taps
        #*
        #**************************************************************************

        side_act_offset_for_gate = (psd_gate_space + psd_activ_over) - (active_right - core_right)
        side_act_offset_for_psd = psd_activ_over + psd_pactiv_pwell_space
        side_act_offset_for_m1 = (
            m1_space_eff
            - (active_right - right_act_m1_right)
            - abs(cont_activ_enc - cont_m1_endcap)
        )

        side_act_offset = max(
            active_space - (active_right - core_right),
            side_act_offset_for_gate,
            side_act_offset_for_psd,
            side_act_offset_for_m1
        )

        bottom_act_offset_for_gate = psd_gate_space + psd_activ_over
        bottom_act_offset_for_m1 = (
            m1_space_eff
            - abs(gate_bottom - right_act_m1_right)
            - abs(cont_activ_enc - cont_m1_endcap)
        )

        bottom_act_offset = max(
            bottom_act_offset_for_gate,
            bottom_act_offset_for_m1
        )

        # draw left and right tap
        bottom_tap_top = gate_bottom - bottom_act_offset
        bottom_tap_bottom = bottom_tap_top - (2 * cont_activ_enc) - cont_size

        right_tap_left = active_right + side_act_offset
        right_tap_right = right_tap_left + (2 * cont_activ_enc) + cont_size
        dbCreateRect(self, active_layer, Box(
            right_tap_left, bottom_tap_bottom,
            right_tap_right, core_top
        ))
        dbCreateRect(self, psd_layer, Box(
            right_tap_left - psd_activ_over, bottom_tap_bottom - psd_activ_over,
            right_tap_right + psd_activ_over, core_top + psd_activ_over
        ))

        left_tap_right = active_left - side_act_offset
        left_tap_left = left_tap_right - (2 * cont_activ_enc) - cont_size
        dbCreateRect(self, active_layer, Box(
            left_tap_left, bottom_tap_bottom,
            left_tap_right, core_top
        ))
        dbCreateRect(self, psd_layer, Box(
            left_tap_left - psd_activ_over, bottom_tap_bottom - psd_activ_over,
            left_tap_right + psd_activ_over, core_top + psd_activ_over
        ))

        # draw botoom tap
        dbCreateRect(self, active_layer, Box(
            left_tap_left, bottom_tap_bottom,
            right_tap_right, bottom_tap_top
        ))
        dbCreateRect(self, psd_layer, Box(
            left_tap_left - psd_activ_over, bottom_tap_bottom - psd_activ_over,
            right_tap_right + psd_activ_over, bottom_tap_top + psd_activ_over
        ))

        bottom_tap_cont_left = left_tap_left + cont_activ_enc
        bottom_tap_cont_right = right_tap_right - cont_activ_enc
        bottom_tap_cont_top = bottom_tap_top - cont_activ_enc
        bottom_tap_cont_bottom = bottom_tap_cont_top - cont_size

        contactArray(
            self, None, locint_layer, bottom_tap_cont_left, bottom_tap_cont_bottom,
            bottom_tap_cont_right, bottom_tap_cont_top, 0, 0, cont_size, cont_space
        )

        dbCreateRect(self, metall_layer, Box(
            bottom_tap_cont_left - cont_m1_endcap, bottom_tap_cont_bottom - cont_m1_endcap,
            bottom_tap_cont_right + cont_m1_endcap, bottom_tap_cont_top + cont_m1_endcap
        ))

        # Create pin SUB
        MkPin(self, 'SUB', 1, Box(
            bottom_tap_cont_left - cont_m1_endcap, bottom_tap_cont_bottom - cont_m1_endcap,
            bottom_tap_cont_right + cont_m1_endcap, bottom_tap_cont_top + cont_m1_endcap
        ), metall_layer_pin)

        left_tap_cont_bottom = bottom_tap_cont_top + cont_space_a
        left_tap_cont_right = left_tap_right - cont_activ_enc
        contactArray(
            self, None, locint_layer, bottom_tap_cont_left, left_tap_cont_bottom,
            left_tap_cont_right, act_cont_top, 0, 0, cont_size, cont_space
        )

        right_tap_cont_left = right_tap_left + cont_activ_enc

        contactArray(
            self, None, locint_layer, right_tap_cont_left, left_tap_cont_bottom,
            bottom_tap_cont_right, act_cont_top, 0, 0, cont_size, cont_space
        )

        dbCreateRect(self, metall_layer, Box(
            bottom_tap_cont_left - cont_m1_endcap, bottom_tap_cont_bottom - cont_m1_endcap,
            left_tap_cont_right + cont_m1_endcap, act_cont_top + cont_m1_endcap
        ))

        dbCreateRect(self, metall_layer, Box(
            right_tap_cont_left - cont_m1_endcap, bottom_tap_cont_bottom - cont_m1_endcap,
            bottom_tap_cont_right + cont_m1_endcap, act_cont_top + cont_m1_endcap
        ))

        #**************************************************************************
        #*
        #* Connects sub taps to N+
        #*
        #**************************************************************************

        dbCreateRect(self, metall_layer, Box(
            bottom_tap_cont_left - cont_m1_endcap, act_m1_bottom,
            left_act_m1_right, act_m1_top
        ))

        dbCreateRect(self, metall_layer, Box(
            right_act_m1_left, act_m1_bottom,
            bottom_tap_cont_right + cont_m1_endcap, act_m1_top
        ))

        # Label at the middle of the device
        dbCreateLabel(
            self, text_layer,
            Point((core_left + core_right) / 2, (core_top + core_bottom) / 2),
            'moscap_n', 'centerCenter', 'R0', Font.EURO_STYLE, 0.1
        )
