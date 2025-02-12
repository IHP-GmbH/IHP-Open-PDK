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

class bondpad(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        techparams = specs.tech.getTechParams()
        
        model       = 'bondpad' 
        CDFVersion  = techparams['CDFVersion']
        topMetal    = techparams['bondpad_topMetal']
        bottomMetal = techparams['bondpad_bottomMetal']
        addFillerEx = techparams['bondpad_addFillerEx']
        
#ifdef KLAYOUT
#else
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
#endif
        specs('model', model, 'Model name')
        
        specs('shape', 'octagon', 'Shape', ChoiceConstraint(['octagon', 'square', 'circle']))
        specs('stack', 't', 'Stack Metals', ChoiceConstraint(['nil', 't']))
        specs('fill', 'nil', 'Fill Metals', ChoiceConstraint(['nil', 't']))
        specs('FlipChip', 'no', 'Flip Chip', ChoiceConstraint(['no', 'yes']))
        specs('diameter', techparams['bondpad_diameter'], 'Diameter')
        specs('hwquota', '1', 'Height-width quota')
        specs('topMetal', topMetal, 'TopMetal', ChoiceConstraint(['TM1', 'TM2']))
        specs('bottomMetal', bottomMetal, 'BottomMetal', ChoiceConstraint(['1', '2', '3', '4', '5', 'TM1']))
        specs('addFillerEx', addFillerEx, 'Metal Filler Exclusion', ChoiceConstraint(['nil', 't']))
        specs('passEncl', '2.1u', 'Passiv enclosure in TM2')

        specs('padType', techparams['bondpad_padType'], 'Pad type', ChoiceConstraint(['bondpad', 'probepad']))
        specs('padPin', 'PAD', 'padPin name:')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params      = params
        self.padType     = params['padType']
        self.diameter    = params['diameter']
        self.passEncl    = params['passEncl']
        self.hwquota     = params['hwquota']
        self.shape       = params['shape']
        self.topMetal    = params['topMetal']
        self.bottomMetal = params['bottomMetal']
        self.stack       = params['stack']
        self.fill        = params['fill']
        self.FlipChip    = params['FlipChip']
        self.addFillerEx = params['addFillerEx']

    def genLayout(self):
        techparams = self.tech.getTechParams()
        self.techparams = techparams
        self.epsilon = techparams['epsilon1']
        
        padType     = self.padType
        diameter    = self.diameter
        passEncl    = self.passEncl
        hwquota     = self.hwquota
        shape       = self.shape
        topMetal    = self.topMetal
        bottomMetal = self.bottomMetal
        
        if self.fill == 'nil' :
            fill = False
        else :
            fill = True
        if self.stack == 'nil' :
            stack = False
        else :
            stack = True
        if self.FlipChip == 'no' :
            FlipChip = False
        else :
            FlipChip = True
        if self.addFillerEx == 'nil' :
            addFillerEx = False
        else :
            addFillerEx = True

        grid = techparams['grid']
        Vn_size = techparams['Vn_a']
        Vn_dist = techparams['Vn_b']
        V1_size = techparams['V1_a']
        V1_dist = techparams['V1_b']
        TV1_size = techparams['TV1_a']
        TV1_dist = techparams['TV1_b']
        TV2_size = techparams['TV2_a']
        TV2_dist = techparams['TV2_b']
        met_over = techparams['TV1_d']
        met_over2 = techparams['Pad_gR']
        met_over_pass = techparams['Pas_c']
        metallization = techparams['metalName']
        
        noFillerEnc = 10.0
        sg13 = True
        pi = acos(0)*2
        maskLayer = 'Activ'
        
        # Pad has 0 pins -> value must be one for unknown reason
        dbReplaceProp(self, 'pin#', 1)
        dbReplaceProp(self, 'ignore', 'TRUE')
        
        if FlipChip and (shape == 'square') :
            print('Flip Chip requires octagon or circle shape')
            shape = octagon
            
        padLay = Layer('dfpad', 'drawing')
        if FlipChip :
            met_over_pass = 10.0
            padLay = Layer('dfpad', 'sbump')
            
        if padType == 'probepad' :
            met_over_pass = Numeric(passEncl);
            met_over_pass = tog(met_over_pass*1e6)
            
        # check which rule is harder
        if met_over2 > met_over :
            met_over = met_over2
            
        diameter = Numeric(diameter);
        hwq = Numeric(hwquota);
        rad = tog(diameter*5e5)
        diameter = rad*2
        if hwq == 1. :
            radx = rad
            rady = rad
            
        if hwq > 1. :
            if diameter/hwq < 10. :
                print('hwQuota too large for given diameter, 1.0 assumed')
                hwq = 1.
                
            rady = rad
            radx = tog(rad/hwq)
            
        if hwq < 1. :
            if diameter*hwq < 10. :
                print('hwQuota too small for given diameter, 1.0 assumed')
                hwq = 1.
                
            radx = rad
            rady = tog(rad*hwq)
            
        if topMetal == 'TM1' :
            if sg13 :
                topMetal = 6
            else :
                topMetal = 4
        else :
            if sg13 :
                topMetal = 7
            else :
                topMetal = 5
                    
        if bottomMetal == 'TM1' : # it can't be higher
            if sg13 :
                bottomMetal = 6
            else :
                bottomMetal = 4
        else :
            bottomMetal = int(bottomMetal);
                        
        if bottomMetal < 1 :
            bottomMetal = 1
            print('error: bottomMetal too low\n')
            
        if bottomMetal >= topMetal :
            bottomMetal = topMetal-1
            print('error: bottomMetal too high\n')
            
        # define stack of layers for filler exclusion
        # define Lists for Via and Metallayers depending to numbers
                        
        if topMetal == 4 :
            noFillerStack = ['Activ', 'GatPoly', 'Metal1', 'Metal2', 'Metal3', 'TopMetal1']
            drawMetalList = ['Metal1', 'Metal2', 'Metal3', 'TopMetal1']
            drawViaList   = ['Via1', 'Via2', 'TopVia1']
            tm1ind = 4
            tm2ind = 0
        elif topMetal == 5 :
            noFillerStack = ['Activ', 'GatPoly', 'Metal1', 'Metal2', 'Metal3', 'TopMetal1', 'TopMetal2']
            drawMetalList = ['Metal1', 'Metal2', 'Metal3', 'TopMetal1', 'TopMetal2']
            drawViaList   = ['Via1', 'Via2', 'TopVia1', 'TopVia2']
            tm1ind = 4
            tm2ind = 5
        elif topMetal == 6 :
            noFillerStack = ['Activ', 'GatPoly', 'Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1']
            drawMetalList = ['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1']
            drawViaList   = ['Via1', 'Via2', 'Via3', 'Via4', 'TopVia1']
            tm1ind = 6
            tm2ind = 0
        elif topMetal == 7 :
            noFillerStack = ['Activ', 'GatPoly', 'Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']
            drawMetalList = ['Metal1', 'Metal2', 'Metal3', 'Metal4', 'Metal5', 'TopMetal1', 'TopMetal2']
            drawViaList   = ['Via1', 'Via2', 'Via3', 'Via4', 'TopVia1', 'TopVia2']
            tm1ind = 6
            tm2ind = 7
        
    
        if tm2ind :
            stripeWidth = tog(met_over+sqrt(2)*TV2_size*0.5)*2;
        else :
            stripeWidth = tog(met_over+sqrt(2)*TV1_size*0.5)
                
        pcPurpose = 'drawing'
    
        if shape == 'octagon' :
            if addFillerEx :
                oradx = radx+noFillerEnc
                orady = rady+noFillerEnc
                ooff = tog(min(oradx, orady)*(1-1/(sqrt(2)+1)))
                poly = bondpadOctagonPoints(oradx, orady, ooff)
                for noFiller in noFillerStack :
                    dbCreatePolygon(self, Layer(noFiller, 'nofill'), poly)
                
            # draw all metallayer    
            metalNumber = topMetal
            # get layer from list
            pcLayer = drawMetalList[metalNumber-1]
            offset = tog(min(radx, rady)*(1-1/(sqrt(2)+1)))
            poly = bondpadOctagonPoints(radx, (rady+0.005), offset)
            dbCreatePolygon(self, pcLayer, poly)
            
            ####################################################################
            # draw HRACT over whole bondpad
            if padType == 'bondpad' :
                dbCreatePolygon(self, padLay, poly)
                
            oradx = radx-met_over_pass
            orady = rady-met_over_pass
            ooff = tog(min(oradx, orady)*(1-1/(sqrt(2)+1)))
            poly = bondpadOctagonPoints(oradx, orady, ooff)
            dbCreatePolygon(self, 'Passiv', poly)
            if stack :
                if fill :
                    ooff = stripeWidth
                    oradx = radx-ooff
                    orady = rady-ooff
                    ooff = tog((min(radx, rady)-ooff)*(1-1/(sqrt(2)+1)))
                    poly = bondpadOctagonPoints(oradx, orady, ooff)
                    idmask = dbCreatePolygon(self, maskLayer, poly)
                    
                poly = bondpadOctagonPoints(radx, rady+0.005, offset)
                ooff = tog(stripeWidth)
                oradx = radx-ooff
                orady = rady-ooff
                ooff = tog(min(oradx, orady)*(1-1/(sqrt(2)+1)))
                poly2 = bondpadOctagonRingPoints(radx, rady+0.005, offset, oradx, orady, ooff)
                
                for metal in range(int(bottomMetal), int(metalNumber)) :
                    pcLayer = nth(metal-1, drawMetalList)
                    if fill :
                        dbCreatePolygon(self, pcLayer, poly)
                    else :
                        dbCreatePolygon(self, pcLayer, poly2)
                    # determine if std. via or topvia rules apply
                    if metal == 1 :
                        vs = V1_size
                        vd = V1_dist
                        
                    if metal > 1 and metal < tm1ind-1 :
                        vs = Vn_size
                        vd = Vn_dist
                        
                    if metal == tm1ind-1 :
                        vs = TV1_size
                        vd = TV1_dist
                        
                    if metal == tm1ind :
                        vs = TV2_size
                        vd = TV2_dist
                        
                    pcLayer = nth(metal-1, drawViaList)
                    # draw via area
                    if fill :
                        if oddp(metal) :
                            viaofs = 0.0
                        else :
                            viaofs = 2.0*vd
                            
                        ooff = stripeWidth
                        oradx = radx-ooff
                        orady = rady-ooff
                        olist = contactArray(self, 0, maskLayer, -oradx, -orady, oradx, orady, viaofs, viaofs, vs, vd*4)
                        dbLayerInside(self, pcLayer, olist, idmask)
                        for item in olist :
                            dbDeleteObject(item)
                            
                        
                    # draw via ring
                    off = offset+vd
                    contactArray(self, 0, pcLayer, -radx, -rady+off, -radx+stripeWidth, rady-off, stripeWidth*0.5-vd, 0, vs, vd)
                    contactArray(self, 0, pcLayer, radx-stripeWidth, -rady+off, radx, rady-off, stripeWidth*0.5-vd, 0, vs, vd)
                    contactArray(self, 0, pcLayer, -radx+off, rady-stripeWidth, radx-off, rady, 0, stripeWidth*0.5-vd, vs, vd)
                    contactArray(self, 0, pcLayer, -radx+off, -rady, radx-off, -rady+stripeWidth, 0, stripeWidth*0.5-vd, vs, vd)
                    off = tog(stripeWidth/sqrt(2))
                    d = vs+tog(vd/sqrt(2)+grid)
                    x = -radx+off
                    y = rady-offset
                    while y < rady-stripeWidth*0.5-vs*1.5-vd :
                        item = dbCreateRect(self, pcLayer, Box(x, y, x+vs, y+vs))
                        dbCopyShape(item, Point(0, 0), 'MX')
                        dbCopyShape(item, Point(0, 0), 'MY')
                        dbCopyShape(item, Point(0, 0), 'R180')
                        x = x+d
                        y = y+d
                #  for metal
                
                if fill == 't' :
                    dbDeleteObject(car(idmask))
            # if stack
        else :
            if shape == 'square' :
                if addFillerEx :
                    oradx = radx+noFillerEnc
                    orady = rady+noFillerEnc
                    for noFiller in noFillerStack :
                        dbCreateRect(self, Layer(noFiller, 'nofill'), Box(-oradx, -orady, oradx, orady))
                        
                # draw all metallayer  
                metalNumber = topMetal
                # get layer from list
                pcLayer = nth(metalNumber-1, drawMetalList)
                dbCreateRect(self, pcLayer, Box(-radx, -rady, radx, rady))
                # draw HRACT over whole bondpad
                if padType == 'bondpad' :
                    dbCreateRect(self, padLay, Box(-radx, -rady, radx, rady))
                
                oradx = radx-met_over_pass
                orady = rady-met_over_pass
                dbCreateRect(self, 'Passiv', Box(-oradx, -orady, oradx, orady))
                
                if stack :
                    if not fill :
                        oradx = radx-stripeWidth
                        orady = rady-stripeWidth
                        poly = PointList([Point(-radx, -rady),   Point(-radx, rady),   Point(radx, rady),   Point(radx, -rady),   Point(-radx, -rady), 
                                          Point(-oradx, -orady), Point(oradx, -orady), Point(oradx, orady), Point(-oradx, orady), Point(-oradx, -orady)])
                    
                    for metal in range(bottomMetal, metalNumber) :
                        pcLayer = nth(metal-1, drawMetalList)
                        if fill :
                            dbCreateRect(self, pcLayer, Box(-radx, -rady, radx, rady))
                        else :
                            dbCreatePolygon(self, pcLayer, poly)
                            
                        if metal == 1 :
                            vs = V1_size
                            vd = V1_dist
                            
                        if metal > 1 and metal < tm1ind-1 :
                            vs = Vn_size
                            vd = Vn_dist
                            
                        if metal == tm1ind-1 :
                            vs = TV1_size
                            vd = TV1_dist
                            
                        if metal == tm1ind :
                            vs = TV2_size
                            vd = TV2_dist
                        
                        # draw via area    
                        pcLayer = nth(metal-1, drawViaList)
                        if fill :
                            if oddp(metal) :
                                viaofs = 0.0
                            else :
                                viaofs = 2.0*vd
                                
                            ooff = stripeWidth+4
                            oradx = radx-ooff
                            orady = rady-ooff
                            contactArray(self, False, pcLayer, -oradx, -orady, oradx, orady, viaofs, viaofs, vs, vd*4)
                            
                        oradx = tog(radx-stripeWidth*0.5)
                        viaofs = tog((stripeWidth-vs)/2)
                        contactArray(self, False, pcLayer, -radx, rady-stripeWidth, radx, rady, viaofs, viaofs, vs, vd)
                        contactArray(self, False, pcLayer, -radx, -rady, radx, -rady+stripeWidth, viaofs, viaofs, vs, vd)
                        contactArray(self, False, pcLayer, -radx, -rady, -radx+stripeWidth, rady, viaofs, viaofs+vs+vd+grid*2, vs, vd)
                        contactArray(self, False, pcLayer, radx-stripeWidth, -rady, radx, rady, viaofs, viaofs+vs+vd+grid*2, vs, vd)
                    # for
                # if stack
            else :      # circle
                if addFillerEx :
                    oradx = radx+noFillerEnc
                    orady = rady+noFillerEnc
                    id = bondpadStretchedCircle(self, Layer(noFillerStack[0], 'nofill'), oradx, orady, grid)
                    #id~>??
                    for noFiller in noFillerStack[1:] :
                        id1 = dbCopyShape(id, Point(0, 0), 'R0')
                        id1.layer = Layer(noFiller, 'nofill')
                
                # draw all metallayer    
                metalNumber = topMetal
                # get layer from list
                pcLayer = nth(metalNumber-1, drawMetalList)
                id = bondpadStretchedCircle(self, pcLayer, radx, rady, grid)
                
                # draw HRACT over whole bondpad
                if padType == 'bondpad' :
                    id1 = dbCopyShape(id, Point(0, 0), 'R0')
                    id1.layer = Layer('dfpad')
            
                oradx = radx-met_over_pass
                orady = rady-met_over_pass
                bondpadStretchedCircle(self, 'Passiv', oradx, orady, grid)
                if stack :
                    if fill :
                        ooff = stripeWidth
                        oradx = radx-ooff
                        orady = rady-ooff
                        idmask = bondpadStretchedCircle(self, maskLayer, oradx, orady, grid)
                        
                    for metal in range(bottomMetal, metalNumber) :
                        pcLayer = drawMetalList[metal-1]
                        if fill :
                            id1 = dbCopyShape(id, Point(0, 0), 'R0')
                            id1.layer = Layer(pcLayer)
                        else :
                            id1 = dbCopyShape(id, Point(0, 0), 'R0')
                            id1.layer = Layer(pcLayer)
                            oradx = radx-stripeWidth
                            orady = rady-stripeWidth
                            id2 = bondpadStretchedCircle(self, pcLayer, oradx, orady, grid)
                            dbLayerXor(pcLayer, id1, id2)
                            dbDeleteObject(id1)
                            dbDeleteObject(id2)
                            
                        if metal == 1 :
                            vs = V1_size
                            vd = V1_dist
                            
                        if metal > 1 and metal < tm1ind-1 :
                            vs = Vn_size
                            vd = Vn_dist
                            
                        if metal == tm1ind-1 :
                            vs = TV1_size
                            vd = TV1_dist
                            
                        if metal == tm1ind :
                            vs = TV2_size
                            vd = TV2_dist
                        
                        # draw via area    
                        pcLayer = nth(metal-1, drawViaList)
                        if fill :
                            if oddp(metal) :
                                viaofs = 0.0
                            else :
                                viaofs = 2.0*vd
                                
                            ooff = stripeWidth
                            oradx = radx-ooff
                            orady = rady-ooff
                            olist = contactArray(self, 0, maskLayer, -oradx, -orady, oradx, orady, viaofs, viaofs, vs, vd*4)
                            dbLayerInside(self, pcLayer, olist, idmask)
                            for item in olist :
                                dbDeleteObject(item)
                                
                        # draw via ring
                        rad = min(radx, rady)
                        u = pi*(rad*2-stripeWidth)
                        rad = rad-stripeWidth/2
                        n = floor(u/((vs+vd)*1.25))
                        n = (n/4)*4
                        w = pi*2/n
                        if radx == rady :
                            for i in range(int(n)) :
                                x = tog(rad*cos(w/2+i*w)-vs/2)
                                y = tog(rad*sin(w/2+i*w)-vs/2)
                                dbCreateRect(self, pcLayer, Box(x, y, x+vs, y+vs))
                                
                        if radx > rady :
                            ooff = tog((stripeWidth-vs)/2)-grid
                            contactArray(self, 0, pcLayer, rady-radx, -rady+ooff, radx-rady, -rady+stripeWidth-ooff, vd/2, 0, vs, vd)
                            contactArray(self, 0, pcLayer, rady-radx, rady-stripeWidth+ooff, radx-rady, rady-ooff, vd/2, 0, vs, vd)
                            for i in range(int(n/4)) :
                                x = tog(rad*cos(w/2+i*w)-vs/2)+radx-rady 
                                y = tog(rad*sin(w/2+i*w)-vs/2)
                                item = dbCreateRect(self, pcLayer, Box(x, y, x+vs, y+vs))
                                dbCopyShape(item, Point(0, 0), 'MX')
                                dbCopyShape(item, Point(0, 0), 'MY')
                                dbCopyShape(item, Point(0, 0), 'R180')
                                
                        if rady > radx :
                            ooff = tog((stripeWidth-vs)/2)-grid
                            contactArray(self, 0, pcLayer, -radx+ooff, radx-rady, -radx+stripeWidth-ooff, rady-radx, 0, vd/2, vs, vd)
                            contactArray(self, 0, pcLayer, radx-stripeWidth+ooff, radx-rady, radx-ooff, rady-radx, 0, vd/2, vs, vd)
                            for i in range(int(n/4)) :
                                x = tog(rad*cos(w/2+i*w)-vs/2)
                                y = tog(rad*sin(w/2+i*w)-vs/2)+rady-radx
                                item = dbCreateRect(self, pcLayer, Box(x, y, x+vs, y+vs))
                                dbCopyShape(item, Point(0, 0), 'MX')
                                dbCopyShape(item, Point(0, 0), 'MY')
                                dbCopyShape(item, Point(0, 0), 'R180')
                    # for
                        
                    if fill :
                        dbDeleteObject(idmask)
                # if stack
            # if square
        # if octagon
