__version__ = "$Revision: #3 $"

from cni.dlo import *
from .thermal import *
from .geometry import *
from .utility_functions import *

import math

class nmos(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        model      = 'sg13_lv_nmos'
        defL       = techparams['nmos_defL']
        defW       = techparams['nmos_defW']
        defNG      = techparams['nmos_defNG']
        minL       = techparams['nmos_minL']
        minW       = techparams['nmos_minW']

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')

        specs('w' ,   defW, 'Width')
        specs('ws',   eng_string(Numeric(defW)/Numeric(defNG)), 'SingleWidth')
        specs('l' ,   defL, 'Length')
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('ng',   defNG, 'Number of Gates')

        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')

    def setupParams(self, params):
        # process parameter values entered by user
        self.w = Numeric(params['w'])*1e6
        self.ng = Numeric(params['ng'])
        self.l = Numeric(params['l'])*1e6

    def genLayout(self):
        w = self.w
        ng = self.ng
        l = self.l

        techparams = self.tech.getTechParams()
        self.techparams = techparams
        self.epsilon = techparams['epsilon1']

        Cell = self.__class__.__name__
        typ = 'N'
        hv = False

        epsilon = techparams['epsilon1']
        #grid = techGetMfgGridResolution(tfId)
        grid = techparams['grid']
        metall_layer = Layer('Metal1')
        metall_layer_pin = Layer('Metal1', 'pin')
        ndiff_layer = Layer('Activ')
        pdiff_layer = Layer('Activ')
        pdiffx_layer = Layer('pSD')
        poly_layer = Layer('GatPoly')
        poly_layer_pin = Layer('GatPoly', 'pin')
        well_layer = Layer('NWell')
        well2_layer = Layer('nBuLay')
        textlayer = Layer('TEXT')
        locint_layer = Layer('Cont')
        tgo_layer = Layer('ThickGateOx')
        endcap = techparams['M1_c1']
        cont_size = techparams['Cnt_a']
        cont_dist = techparams['Cnt_b']
        cont_Activ_overRec = techparams['Cnt_c']
        cont_metall_over = techparams['M1_c']
        psd_pActiv_over = techparams['pSD_c']
        nwell_pActiv_over = techparams['NW_c']
        #minNwellForNBuLay = techparams['NW_g']
        well2_over = techparams['NW_NBL']
        gatpoly_Activ_over = techparams['Gat_c']
        gatpoly_cont_dist = techparams['Cnt_f']
        smallw_gatpoly_cont_dist = techparams['Cnt_c']
        psd_PFET_over = techparams['pSD_i']
        pdiffx_poly_over_orth = 0.48

        wmin = Numeric(techparams['nmos_minW'])
        lmin = Numeric(techparams['nmos_minL'])

        contActMin = 2*techparams['Cnt_c']+techparams['Cnt_a']
        thGateOxGat = techparams['TGO_c']
        thGateOxAct = techparams['TGO_a']

        dbReplaceProp(self, "pin#", 5)

        ng = math.floor(Numeric(ng)+epsilon)

        w = w/ng
        w = GridFix(w)
        l = GridFix(l)

        if endcap < cont_metall_over :
            endcap = cont_metall_over

        if hv :
            labelhv = 'HV'
        else :
            labelhv = ''

        smallMetAdd = cont_size + (2*cont_metall_over)
        if (w < contActMin-epsilon) :
            gatpoly_cont_dist = smallw_gatpoly_cont_dist

        xdiff_beg = 0
        ydiff_beg = 0
        ydiff_end = w
        if w < wmin-epsilon :
            hiGetAttention()
            print('Width < '+str(wmin))
            w = wmin

        if l < lmin-epsilon :
            hiGetAttention()
            print('Length < '+str(lmin))
            l = lmin

        if ng < 1 :
            hiGetAttention()
            print('Minimum one finger')
            ng = 1

        xanz = fix((w-2*cont_Activ_overRec+cont_dist)/(cont_size+cont_dist)+epsilon)
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
        ncont = fix((w-2*cont_Activ_overRec+cont_dist)/(cont_size+cont_dist)+epsilon)
        if zerop(ncont) :
            ncont = 1

        diff_cont_offset = GridFix((w-2*cont_Activ_overRec-ncont*cont_size-(ncont-1)*cont_dist)/2)

        # draw the cont row
        xcont_beg = xdiff_beg+cont_Activ_overRec
        ycont_beg = ydiff_beg+cont_Activ_overRec
        ycont_cnt = ycont_beg+diffoffset+diff_cont_offset
        xcont_end = xcont_beg+cont_size

        # draw Metal rect
        # calculate bot and top cont position
        yMet1 = ycont_cnt-endcap
        yMet2 = ycont_cnt+cont_size+( ncont-1)*distc +endcap
        # is metal1 overlapping Activ?
        yMet1 = min(yMet1, ydiff_beg+diffoffset)
        yMet2 = max(yMet2, ydiff_end+diffoffset)
        dbCreateRect(self, metall_layer, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2))

        # draw contacts
        # LI and Metall
        contactArray(self, 0, locint_layer, xcont_beg, ydiff_beg, xcont_end, ydiff_end+diffoffset*2, 0, cont_Activ_overRec, cont_size, cont_dist)

        if w > contActMin : # smallW
            MkPin(self, 'S', 3, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2), metall_layer_pin)
        else :
            MkPin(self, 'S', 3, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2), metall_layer_pin)

        if typ == 'N' :
            dbCreateRect(self, ndiff_layer, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec))
        else :
            dbCreateRect(self, pdiff_layer, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec))

        for i in range(int(ng)) :
            # draw the poly line
            xpoly_beg = xcont_end+gatpoly_cont_dist
            ypoly_beg = ydiff_beg-gatpoly_Activ_over
            xpoly_end = xpoly_beg+l
            ypoly_end = ydiff_end+gatpoly_Activ_over
            dbCreateRect(self, poly_layer, Box(xpoly_beg, ypoly_beg+diffoffset, xpoly_end, ypoly_end+diffoffset))

            ihpAddThermalMosLayer(self, Box(xpoly_beg, ypoly_beg+diffoffset, xpoly_end, ypoly_end+diffoffset), True, Cell)

            if i ==  0 :
                dbCreateLabel(self, Layer('TEXT', 'drawing'), Point((xpoly_beg+xpoly_end)/2, (ypoly_beg+ypoly_end)/2+diffoffset), 'nmos'+labelhv, 'centerCenter', 'R90', Font.EURO_STYLE, 0.09)

            if zerop(i) :
                MkPin(self, 'G', 2, Box(xpoly_beg, ypoly_beg+diffoffset, xpoly_end, ypoly_end+diffoffset), poly_layer_pin)

            # for every gate
            if typ == 'P' :
                dbCreateRect(self, pdiffx_layer, Box(xpoly_beg-pdiffx_poly_over_orth, ypoly_beg-psd_PFET_over+gatpoly_Activ_over+diffoffset, xpoly_end+pdiffx_poly_over_orth, ypoly_end+psd_PFET_over-gatpoly_Activ_over+diffoffset))

            # draw the second cont row
            xcont_beg = xpoly_end+gatpoly_cont_dist
            ycont_beg = ydiff_beg+cont_Activ_overRec
            ycont_cnt = ycont_beg+diffoffset+diff_cont_offset
            xcont_end = xcont_beg+cont_size

            dbCreateRect(self, metall_layer, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2))

            # draw contacts
            # LI and Metall
            contactArray(self, 0, locint_layer, xcont_beg, ydiff_beg, xcont_end, ydiff_end+diffoffset*2, 0, cont_Activ_overRec, cont_size, cont_dist)

            if zerop(i) :
                if (w > contActMin) :
                    MkPin(self, 'D', 1, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2), metall_layer)
                else :
                    MkPin(self, 'D', 1, Box(xcont_beg-cont_metall_over, yMet1, xcont_end+cont_metall_over, yMet2), metall_layer)


            if typ == 'N' :
                dbCreateRect(self, ndiff_layer, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec))
            else :
                dbCreateRect(self, pdiff_layer, Box(xcont_beg-cont_Activ_overRec, ycont_beg-cont_Activ_overRec, xcont_end+cont_Activ_overRec, ycont_beg+cont_size+cont_Activ_overRec))


        # now finish drawing the diffusion
        xdiff_end = xcont_end+cont_Activ_overRec
        if typ == 'N' :
            dbCreateRect(self, ndiff_layer, Box(xdiff_beg, ydiff_beg+diffoffset, xdiff_end, ydiff_end+diffoffset))
        else :
            dbCreateRect(self, pdiff_layer, Box(xdiff_beg, ydiff_beg+diffoffset, xdiff_end, ydiff_end+diffoffset))
            dbCreateRect(self, pdiffx_layer, Box(xdiff_beg-psd_pActiv_over, ydiff_beg-psd_pActiv_over+diffoffset, xdiff_end+psd_pActiv_over, ydiff_end+psd_pActiv_over+diffoffset))
            # draw minimum nWell
            nwell_offset = max(0, GridFix((contActMin-w)/2+0.5*grid))
            dbCreateRect(self, well_layer, Box(xdiff_beg-nwell_pActiv_over, ydiff_beg-nwell_pActiv_over+diffoffset-nwell_offset, xdiff_end+nwell_pActiv_over, ydiff_end+nwell_pActiv_over+diffoffset+nwell_offset))
            # draw nBuLay if nWell is large enough
            # wmin=2.88 -> only width musdt be checked
            if (ydiff_end+nwell_pActiv_over+diffoffset+nwell_offset)-(ydiff_beg-nwell_pActiv_over+diffoffset-nwell_offset) > minNwellForNBuLay :
                dbCreateRect(self, well2_layer, Box(xdiff_beg-nwell_pActiv_over+well2_over, ydiff_beg-nwell_pActiv_over+diffoffset-nwell_offset+well2_over, xdiff_end+nwell_pActiv_over-well2_over, ydiff_end+nwell_pActiv_over+diffoffset+nwell_offset-well2_over))

        if hv :
            dbCreateRect(self, Layer('ThickGateOx', 'drawing'), Box(xdiff_beg-thGateOxAct, ydiff_beg-gatpoly_Activ_over-thGateOxGat, xdiff_end+thGateOxAct, ydiff_end+gatpoly_Activ_over+thGateOxGat))

