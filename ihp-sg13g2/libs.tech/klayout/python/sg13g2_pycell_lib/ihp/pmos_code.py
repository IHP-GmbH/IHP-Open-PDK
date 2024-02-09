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
from .geometry import *
from .thermal import *
from .utility_functions import *

import math

class pmos(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        model      = 'sg13_lv_pmos'
        defL       = techparams['pmos_defL']
        defW       = techparams['pmos_defW']
        defNG      = techparams['pmos_defNG']
        minL       = techparams['pmos_minL']
        minW       = techparams['pmos_minW']

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')

        specs('w' ,   defW, 'Width')

        test = Numeric(defW)
        specs('ws',   eng_string(Numeric(defW)/Numeric(defNG)), 'SingleWidth')
        specs('l' ,   defL, 'Length')
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('ng',   defNG, 'Number of Gates')

        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.w = Numeric(params['w'])
        self.l = Numeric(params['l'])
        self.ng = Numeric(params['ng'])

    def genLayout(self):
        self.grid = self.tech.getGridResolution()
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']

        w = self.w
        ng = self.ng
        l = self.l

        typ = 'P'
        hv = False

        ndiff_layer = Layer('Activ', 'drawing')     # 1
        pdiff_layer = Layer('Activ', 'drawing')     # 1
        poly_layer = Layer('GatPoly', 'drawing')    # 5
        locint_layer = Layer('Cont', 'drawing')     # 6
        metall_layer = Layer('Metal1', 'drawing')   # 8
        pdiffx_layer = Layer('pSD', 'drawing')      # 14
        well_layer = Layer('NWell', 'drawing')      # 31
        tgo_layer = Layer('ThickGateOx', 'drawing') # 44
        textlayer = Layer('TEXT', 'drawing')        # 63

        endcap = self.techparams['M1_c1']
        cont_size = self.techparams['Cnt_a']
        cont_dist = self.techparams['Cnt_b']
        cont_Activ_overRec = self.techparams['Cnt_c']
        cont_metall_over = self.techparams['M1_c']
        psd_pActiv_over = self.techparams['pSD_c']
        nwell_pActiv_over = self.techparams['NW_c']
        gatpoly_Activ_over = self.techparams['Gat_c']
        gatpoly_cont_dist = self.techparams['Cnt_f']
        smallw_gatpoly_cont_dist = cont_Activ_overRec+self.techparams['Gat_d']
        psd_PFET_over = self.techparams['pSD_i']
        pdiffx_poly_over_orth = 0.48
        wmin = Numeric(self.techparams['pmos_minW'])
        lmin = Numeric(self.techparams['pmos_minL'])
        contActMin = 2*cont_Activ_overRec+cont_size
        thGateOxGat = self.techparams['TGO_c']
        thGateOxAct = self.techparams['TGO_a']

        dbReplaceProp(self, 'pin#', 5)

        w = w*1e6;
        l = l*1e6;
        ng = math.floor(Numeric(ng)+self.epsilon)
        w = w/ng
        w = GridFix(w)
        l = GridFix(l)

        # additional Text for label
        if hv :
            labelhv = 'HV'
        else :
            labelhv = ''

        if w < contActMin-self.epsilon :
            gatpoly_cont_dist = smallw_gatpoly_cont_dist

        xdiff_beg = 0
        ydiff_beg = 0
        ydiff_end = w

        if w < wmin-self.epsilon :
            hiGetAttention()
            print('Width < '+str(wmin))
            w = wmin

        if l < lmin-self.epsilon :
            hiGetAttention()
            print('Length < '+str(lmin))
            l = lmin

        if ng < 1 :
            hiGetAttention()
            print('Minimum one finger')
            ng = 1

        xanz = math.floor((w-2*cont_Activ_overRec+cont_dist)/(cont_size+cont_dist)+self.epsilon)
        w1 = xanz*(cont_size+cont_dist)-cont_dist+cont_Activ_overRec+cont_Activ_overRec
        xoffset = (w-w1)/2
        xoffset = GridFix(xoffset)
        diffoffset = 0
        if w < contActMin :
            xoffset = 0
            diffoffset = (contActMin-w)/2
            diffoffset = Snap(diffoffset)

        # get the number of contacts
        lcon = w-2*cont_Activ_overRec
        distc = cont_size+cont_dist
        ncont = math.floor((lcon+cont_dist-2*endcap)/distc + self.epsilon)
        if zerop(ncont) :
            ncont = 1

        diff_cont_offset = GridFix((w-2*cont_Activ_overRec-ncont*cont_size-(ncont-1)*cont_dist)/2)

        # draw the cont row
        xcont_beg = xdiff_beg+cont_Activ_overRec
        ycont_beg = ydiff_beg+cont_Activ_overRec
        ycont_cnt = ycont_beg+diffoffset+diff_cont_offset
        xcont_end = xcont_beg+cont_size

        # draw contacts
        # LI and Metall
        contactArray(self, 0, locint_layer, xcont_beg, ydiff_beg, xcont_end, ydiff_end+diffoffset*2, 0, cont_Activ_overRec, cont_size, cont_dist)

        # 30.01.08 GGa added block
        # draw Metal rect
        # calculate bot and top cont position
        yMet1 = ycont_cnt-endcap
        yMet2 = ycont_cnt+cont_size+(ncont-1)*distc +endcap
        # is metal1 overlapping Activ?
        yMet1 = min(yMet1, ydiff_beg+diffoffset)
        yMet2 = max(yMet2, ydiff_end+diffoffset)

        dbCreateRect(self, metall_layer, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2))

        if w > contActMin :
            MkPin(self, 'S', 3, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2), metall_layer)
        else :
            MkPin(self, 'S', 3, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2), metall_layer)

        if typ == 'N' :
            dbCreateRect(self, ndiff_layer, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec))
        else :  # typ == 'P'
            dbCreateRect(self, pdiff_layer, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec))

        for i in range(1, int(ng)+1) :
            # draw the poly line
            xpoly_beg = xcont_end+gatpoly_cont_dist
            ypoly_beg = ydiff_beg-gatpoly_Activ_over
            xpoly_end = xpoly_beg+l
            ypoly_end = ydiff_end+gatpoly_Activ_over

            dbCreateRect(self, poly_layer, Box(xpoly_beg, ypoly_beg+diffoffset, xpoly_end, ypoly_end+diffoffset))

            ihpAddThermalMosLayer(self, Box(xpoly_beg, ypoly_beg+diffoffset, xpoly_end, ypoly_end+diffoffset), True, 'pmos')

            if i == 1 :
                dbCreateLabel(self, textlayer, Point((xpoly_beg+xpoly_end)/2, (ypoly_beg+ypoly_end)/2+diffoffset), 'pmos'+labelhv, 'centerCenter', 'R90', Font.EURO_STYLE, 0.1)

            if onep(i) :
                MkPin(self, 'G', 2, Box(xpoly_beg, ypoly_beg+diffoffset, xpoly_end, ypoly_end+diffoffset), poly_layer)

            # draw the second cont row
            xcont_beg = xpoly_end+gatpoly_cont_dist
            ycont_beg = ydiff_beg+cont_Activ_overRec
            ycont_cnt = ycont_beg+diffoffset+diff_cont_offset
            xcont_end = xcont_beg+cont_size

            dbCreateRect(self, metall_layer, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2))
            # draw contacts
            # LI and Metall
            contactArray(self, 0, locint_layer, xcont_beg, ydiff_beg, xcont_end, ydiff_end+diffoffset*2, 0, cont_Activ_overRec, cont_size, cont_dist)

            if onep(i) :
                if w > contActMin :
                    MkPin(self, 'D', 1, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2), metall_layer)
                else :
                    MkPin(self, 'D', 1, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2), metall_layer)


            if typ == 'N' :
                dbCreateRect(self, ndiff_layer, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec))
            else :
                dbCreateRect(self, pdiff_layer, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec))
        # for i 1 ng

        # now finish drawing the diffusion
        xdiff_end = xcont_end+cont_Activ_overRec
        if typ == 'N' :
            dbCreateRect(self, ndiff_layer, Box(xdiff_beg, ydiff_beg+diffoffset, xdiff_end, ydiff_end+diffoffset))
        else :
            dbCreateRect(self, pdiff_layer,  Box(xdiff_beg, ydiff_beg+diffoffset, xdiff_end, ydiff_end+diffoffset))
            dbCreateRect(self, pdiffx_layer, Box(xdiff_beg-psd_pActiv_over, ypoly_beg-psd_PFET_over+gatpoly_Activ_over+diffoffset, xdiff_end+psd_pActiv_over, ypoly_end+psd_PFET_over-gatpoly_Activ_over+diffoffset))
            # draw minimum nWell
            nwell_offset = max(0, GridFix((contActMin-w)/2+0.5*self.grid))
            dbCreateRect(self, well_layer, Box(xdiff_beg-nwell_pActiv_over, ydiff_beg-nwell_pActiv_over+diffoffset-nwell_offset, xdiff_end+nwell_pActiv_over, ydiff_end+nwell_pActiv_over+diffoffset+nwell_offset))

        # B-Pin
        MkPin(self, 'B', 4, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec), Layer('Substrate', 'drawing'))

        # draw Thick Gate Oxide
        if hv :
            dbCreateRect(self, Layer('ThickGateOx', 'drawing'), Box(xdiff_beg-thGateOxAct, ydiff_beg-gatpoly_Activ_over-thGateOxGat, xdiff_end+thGateOxAct, ydiff_end+gatpoly_Activ_over+thGateOxGat))

