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

__version__ = '$Revision: #3 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *

import math
    
class rfmosfet_base(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        specs('l', '720n', 'Length')
        specs('w', '1u', 'Width')
        specs('ng', '1', 'Number of Gates')
        specs('cnt_rows', 1, 'Contact rows')
        specs('Met2Cont', 'Yes', 'Metal2 contact', ChoiceConstraint(['Yes', 'No']))
        specs('gat_ring', 'Yes', 'Gate ring', ChoiceConstraint(['Yes', 'No']))
        specs('guard_ring', 'Yes', 'Guard ring', ChoiceConstraint(['Yes', 'No', 'U', 'Top+Bottom']))

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.l = params['l']
        self.w = params['w']
        self.ng = params['ng']
        self.cnt_rows = params['cnt_rows']
        self.Met2Cont = params['Met2Cont']
        self.gat_ring = params['gat_ring']
        self.guard_ring = params['guard_ring']

    def genLayout(self):
        self.grid = self.tech.getGridResolution()
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']
        
        l = self.l
        w = self.w
        ng = int(self.ng)
        cnt_rows = int(self.cnt_rows)
        Met2Cont = self.Met2Cont
        gat_ring = self.gat_ring
        guard_ring = self.guard_ring
        
        cellname = self.__class__.__name__
            
        if cellname.find('HV') != -1 :
            hv = True
        else :
            hv = False
            
        if cellname.find('nmos') != -1 :
            rfnmos = True
        else :
            rfnmos = False
            
        met1_w1 = 0.32
        useMet2 = False
        if Met2Cont == 'Yes' :
            useMet2 = True
            
        ngi = ng;
        W = GridFix(Numeric(w)*1e6/ngi)
        L = Numeric(l)*1e6
        length = L-0.13
        nsdbOcont = 0.45
        psdWidth = 0.5
        gateOxOpsd = 0.17
        nwellScont = 0.25
        activWidth = 0.3
        psdOactiv = 0.1
        contW = 0.16
        contS = 0.18
        metWidth = contW+0.14
        viaW = 0.19
        if  W < 1.52 :
            viaS = 0.22
        else :
            viaS = 0.29
        shiftx = 0
        shiftl = shiftx-0.15
        shiftr = 2*shiftx-0.15
        shifta = shiftr-0.01
        shiftcl = 0.03
        shiftcr = shiftr-0.03
        
        # Used layers
        activ = Layer('Activ', 'drawing')
        nsdblock = Layer('nSD', 'block')
        gatpoly = Layer('GatPoly', 'drawing')
        cont = Layer('Cont', 'drawing')
        met1 = Layer('Metal1', 'drawing')
        met2 = Layer('Metal2', 'drawing')
        psd = Layer('pSD', 'drawing')
        via1 = Layer('Via1', 'drawing')
        salblock = Layer('SalBlock', 'drawing')
        nwell = Layer('NWell', 'drawing')
        nbulay = Layer('nBuLay', 'drawing')
        #pwellblock = Layer('PWellBlock', 'drawing')
        gateox = Layer('ThickGateOx', 'drawing')
        text = Layer('TEXT', 'drawing')
        smos = Layer('SMOS', 'drawing')
        
        # Channel distance, Active end pieces
        dc = (0.38+0.03)*cnt_rows-0.03
        ec = (0.345+0.065)*cnt_rows-0.065
        dce = 0.0
        if L < 0.14 and W >= 1 :
            dce = 0.005
            dc = dc+dce*2
            ec = ec + dce
        
        # gatpoly overhang    
        if ngi ==  1 :
            og = 0.27
        else :
            og = 0.395
        
        # source/drain metal width/height    
        wsd = 0.29
        hsd = 0.28
        # metal1 gatring, guardring width
        wgat = 0.3
        wguard = 0.32
        wpsd = 0.38
        # activ-gatring distance hor/vert
        dgatx = 0.13
        dgaty = 0.235
        if  cnt_rows > 2 :
            dgatx = 0.17
        else :
            dgatx = 0.13
        dgaty = 0.235
        # gatring-guardring distance hor/vert
        dguard = 0.36
        
        # Active
        hact = ec+ec+(ngi-1)*dc+ngi*L
        dbCreateRect(self, activ, Box(0, 0, W, hact))
        # Gates
        y = ec
        mlist = ulist[Rect]()
        for i in range(1, ngi+1) :
            mlist.append(dbCreateRect(self, gatpoly, Box(-dgatx, y, W+dgatx, y+L)))
            y = y+dc+L
            
        if cnt_rows ==  1 :
            u = 0.075
        else :
            u = 0.36
        
        # left/right vertical gatpoly stripe with contacts    
        mlist.append(dbCreateRect(self, gatpoly, Box(-dgatx-wgat, u, -dgatx, hact-u)))
        mlist.append(dbCreateRect(self, gatpoly, Box(W+dgatx, u, W+dgatx+wgat, hact-u)))
        dbLayerOrList(gatpoly, mlist)
        for shape in mlist :
            dbDeleteObject(shape)
        
        # drain/source metal with cont    
        if cnt_rows >  1 :
            id = dbCreateRect(self, met1, Box(0.05, 0.015, W-0.05, ec-0.05-dce))
            
        p1_x = 0.05
        p2_x = W-0.05
        p1_y = 0.015+metWidth*0.5-0.01
        p2_y = p1_y
        for i in range(1, cnt_rows+1) :
            MetalCont(self, p1_x, p1_y, p2_x, p2_y, met1, cont, metWidth-0.02, contW, contW, 0.05, contS)
            p1_y = p1_y+metWidth-0.02+0.13
            p2_y = p1_y
            
        if useMet2 :
            if cnt_rows > 1 :
                dbCreateRect(self, met2, Box(0.05, 0.015, W-0.05, ec-0.05-dce))
                
            p1_x = 0.05
            p2_x = W-0.05
            p1_y = 0.015+metWidth*0.5-0.01
            p2_y = p1_y
            for i in range(1, cnt_rows+1) :
                MetalCont(self, p1_x, p1_y, p2_x, p2_y, met2, via1, viaW+0.01, viaW, viaW, 0.05, viaS)
                p1_y = p1_y+metWidth-0.02+0.13
                p2_y = p1_y
                
        shapes = self.getShapes() or []  
        for id in shapes :
            if id.layer != gatpoly and id.layer != activ :
                y = dc+L
                for i in range(1, ngi+1) :
                    dbCopyShape(id, Point(0, y), 'R0')
                    y = y+dc+L
                    
        # Source pin
        id = dbCreateRect(self, Layer('Metal1', 'pin'), Box(0.05, 0.015, W-0.05, ec-0.05-dce))
        MkPin(self, 'S', 0, id.bbox, id.layer)
        dbCreateLabel(self, text, Point(W/2, ec/2), 'S', 'centerCenter', 'R0', Font.EURO_STYLE, wgat)
        id = dbCreateRect(self, Layer('Metal1', 'pin'), Box(0.05, 0.015+(dc+L)*1, W-0.05, ec-0.05+(dc+L)*1-dce))
        MkPin(self, 'D', 0, id.bbox, id.layer)
        dbCreateLabel(self, text, Point(W/2, ec/2+(dc+L)*1), 'D', 'centerCenter', 'R0', Font.EURO_STYLE, wgat)
        if gat_ring == 'Yes' :
            id = dbCreateRect(self, met1, Box(-dgatx-wgat, -dgaty-wgat, -dgatx, hact+dgaty+wgat))
            mlist = ulist[Rect]()
            mlist.append(id)
            id = dbCreateRect(self, met1, Box(W+dgatx, -dgaty-wgat, W+dgatx+wgat, hact+dgaty+wgat))
            mlist.append(id)
            id = dbCreateRect(self, met1, Box(-dgatx, -dgaty-wgat, W+dgatx, -dgaty))
            mlist.append(id)
            id = dbCreateRect(self, met1, Box(-dgatx, hact+dgaty, W+dgatx, hact+dgaty+wgat))
            mlist.append(id)
            dbLayerOrList(met1, mlist)
            for id in mlist :
                dbDeleteObject(id)
                
        # gatpoly-metal1 contact and pin    
        u = u+0.02
        p1_x = -dgatx-wgat*0.5
        p1_y = u
        p2_x = p1_x
        p2_y = hact-u
        MetalCont(self, p1_x, p1_y, p2_x, p2_y, met1, cont, viaW+0.01, contW, contW, 0.05, viaS)
        id = dbCreateRect(self, Layer('Metal1', 'pin'), Box(p1_x-0.1, p1_y, p2_x+0.1, p2_y))
        MkPin(self, 'G', 0, id.bbox, id.layer)
        dbCreateLabel(self, text, Point((p1_x+p2_x)/2, (p1_y+p2_y)/2), 'G', 'centerCenter', 'R0', Font.EURO_STYLE, wgat)
        p1_x = W+dgatx+wgat*0.5
        p2_x = p1_x
        MetalCont(self, p1_x, p1_y, p2_x, p2_y, met1, cont, viaW+0.01, contW, contW, 0.05, viaS)
        # guardring
        xl = -dgatx-wgat-dguard-wguard
        yb = -dgaty-wgat-dguard-wguard
        xr = -xl+W
        yt = -yb+hact
        
        if guard_ring != 'No' :
            p1_x = xl
            p1_y = yb+wguard*0.5
            p2_x = xr
            p2_y = p1_y
            MetalCont(self, p1_x, p1_y, p2_x, p2_y, met1, cont, met1_w1, contW, contW, 0.08, contS)
            id = dbCreateRect(self, Layer('Metal1', 'pin'), Box(p1_x, p1_y-wguard/4, p2_x, p2_y+wguard/4))
            MkPin(self, 'TIE', 0, id.bbox, id.layer)
            dbCreateLabel(self, text, Point((p1_x+p2_x)/2, (p1_y+p2_y)/2), 'TIE', 'centerCenter', 'R0', Font.EURO_STYLE, wguard/2)
            p1_y = yt-wguard*0.5
            p2_y = p1_y
            MetalCont(self, p1_x, p1_y, p2_x, p2_y, met1, cont, met1_w1, contW, contW, 0.08, contS)
            
        if guard_ring == 'Yes' :
            p1_x = xl+wguard*0.5
            p2_x = p1_x
            p1_y = yb+wguard
            p2_y = yt-wguard
            MetalCont(self, p1_x, p1_y, p2_x, p2_y, met1, cont, met1_w1, contW, contW, 0.11, contS)
            
        if guard_ring == 'Yes' or guard_ring == 'U' :
            p1_x = xr-wguard*0.5
            p2_x = p1_x
            p1_y = yb+wguard
            p2_y = yt-wguard
            MetalCont(self, p1_x, p1_y, p2_x, p2_y, met1, cont, met1_w1, contW, contW, 0.11, contS)
            
        #guard ring activ 
        mlist = ulist[Rect]()
        id = dbCreateRect(self, activ, Box(xl, yb, xr, yb+wguard))
        mlist.append(id)
        id = dbCreateRect(self, activ, Box(xl, yt, xr, yt-wguard))
        mlist.append(id)
        id = dbCreateRect(self, activ, Box(xl, yb+wguard, xl+wguard, yt-wguard))
        mlist.append(id)
        id = dbCreateRect(self, activ, Box(xr-wguard, yb+wguard, xr, yt-wguard))
        mlist.append(id)
        dbLayerOrList(activ, mlist)
        for id in mlist :
            dbDeleteObject(id)
        
        # Inscription    
        dbCreateLabel(self, text, Point((xl+xr)/2, yt-wguard/2), cellname, 'centerCenter', 'R0', Font.EURO_STYLE, 0.24)
        
        if rfnmos :
            d = (wpsd-wguard)/2
            xl = xl-d
            xr = xr+d
            yb = yb-d
            yt = yt+d
            id = dbCreateRect(self, psd, Box(xl, yb, xr, yb+wpsd))
            mlist = ulist[Rect]()
            mlist.append(id)
            id = dbCreateRect(self, psd, Box(xl, yt, xr, yt-wpsd))
            mlist.append(id)
            id = dbCreateRect(self, psd, Box(xl, yb+wpsd, xl+wpsd, yt-wpsd))
            mlist.append(id)
            id = dbCreateRect(self, psd, Box(xr-wpsd, yb+wpsd, xr, yt-wpsd))
            mlist.append(id)
            dbLayerOrList(psd, mlist)
            for id in mlist :
                dbDeleteObject(id)
                
        else :
            dbCreateRect(self, psd, Box(xl+0.5, yb+0.6, xr-0.5, yt-0.6))
         
        # Thick gate Oxide for HV Mos    
        if hv :
            if rfnmos :
                d = 0.35
            else :
                d = 0.31
            xl = xl-d
            xr = xr+d
            yb = yb-d
            yt = yt+d
            dbCreateRect(self, gateox, Box(xl, yb, xr, yt))
         
        # nwell for rfpmos
        if not rfnmos :
            if  hv :
                d = 0.35
            else :
                d = 0.31
            xl = xl-d
            xr = xr+d
            yb = yb-d
            yt = yt+d
            dbCreateRect(self, nwell, Box(xl, yb, xr, yt))
        
        # merge all

        # reset origin  
        shapes = self.getShapes() or []        
        for id in shapes :
            if id:
                dbMoveFig(id, Point(-xl, -yb), 'R0')

