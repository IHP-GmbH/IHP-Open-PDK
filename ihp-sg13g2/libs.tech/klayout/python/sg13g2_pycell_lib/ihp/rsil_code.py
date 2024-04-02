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

class rsil(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        # define parameters and default values
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        model      = techparams['rsil_model']
        rspec      = techparams['rsilG2_rspec']
        rkspec     = techparams['rsil_rkspec']
        rzspec     = techparams['rsil_rzspec']
        defL       = techparams['rsil_defL']
        defW       = techparams['rsil_defW']
        defB       = techparams['rsil_defB']
        defPS      = techparams['rsil_defPS']
        minL       = techparams['rsil_minL']
        minW       = techparams['rsil_minW']
        minPS      = techparams['rsil_minPS']
        eps        = techparams['epsilon2']
        
        defR   = '17.248'
        
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('Calculate', 'l', 'Calculate', ChoiceConstraint(['R', 'w', 'l']))
        #specs('Recommendation', 'No', 'Recommendation', ChoiceConstraint(['Yes', 'No'])) -> display = nil
        specs('model', model, 'Model name')

        resistance = CbResCalc('R', 0, defL, defW, defB, defPS, 'rsil')
        specs('R', eng_string(resistance), 'R')

        specs('w',  defW, 'Width')
        specs('l',  defL, 'Length')
        specs('b',  defB, 'Bends')
        specs('ps', defPS, 'Poly Space')

        imax = CbResCurrent(Numeric(defW), Numeric(eps), 'rsilG2')
        specs('Imax', imax, 'Imax')
        specs('bn', 'sub!', 'Bulk node connection')
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('PSmin', minPS, 'PSmin')
        specs('Rspec', rspec, 'Rspec [Ohm/sq]')
        specs('Rkspec', rkspec, 'Rkspec [Ohm/cont]')
        specs('Rzspec', rzspec, 'Rzspec [Ohm*m]')
        specs('tc1', '3100e-6', 'Temperature coefficient 1')
        specs('tc2', '0.30e-6', 'Temperature coefficient 2')
        # GenPWB TBD
        #specs('PWB', 'No', 'PWell Blockage', ChoiceConstraint(['Yes', 'No']))
        specs('m', '1', 'Multiplier')
        specs('trise', '0.0', 'Temp rise from ambient')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.l = Numeric(params['l'])
        self.w = Numeric(params['w'])
        self.b = int(params['b'])
        self.ps = Numeric(params['ps'])
        self.resistance = Numeric(params['R'])

    def genLayout(self):
        l = self.l
        w = self.w
        b = self.b
        ps = self.ps

        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']
        self.grid = self.tech.getGridResolution()         # needed for Dogbone

        Cell = self.__class__.__name__
        
        contpolylayer = 'GatPoly'
        bodypolylayer = 'PolyRes'
        reslayer = 'RES'
        extBlocklayer = 'EXTBlock'
        locintlayer = 'Cont'
        metlayer = 'Metal1'
        textlayer = 'TEXT'

        #*************************************************************************
        #*
        #* Generic Design Rule Definitions
        #*
        #************************************************************************
        epsilon = techparams['epsilon1']
        consize = techparams['Cnt_a']
        conspace = techparams['Cnt_b']
        polyover = techparams['Cnt_d']
        endcap = techparams['M1_c1']
        contbar_poly_over = techparams['CntB_d']
        contbar_min_len = techparams['CntB_a1']
        grid = techparams['grid']
        
        #*************************************************************************
        #*
        #* Device Specific Design Rule Definitions
        #*
        #************************************************************************
        metover = techparams[Cell+'_met_over_cont']
        li_poly_over = techparams['Rsil_b']
        ext_over = techparams['Rsil_e']
        poly_cont_len = li_poly_over+consize+polyover                
        
        #*************************************************************************
        #*
        #* Main body of code
        #*
        #************************************************************************
        internalCode = True
        gridnumber = 0.0
        contoverlay = 0.0
        l = Numeric(l)*1e6
        w = Numeric(w)*1e6
        b = fix(b + epsilon)
        ps = Numeric(ps)*1e6
        
        wcontact = w
        drawbar = False
        if internalCode :
            if wcontact-2*contbar_poly_over + epsilon >= contbar_min_len :
                drawbar = True
                
        # check of met enc of cont    
        if metover < endcap :
            metover = endcap
            
        # dogbone has to be on grid, so make difference in gridsteps
        contoverlay = wcontact - w
        if contoverlay > 0 :
            contoverlay = contoverlay/2
            gridnumber = contoverlay/grid
            gridnumber = round(gridnumber + epsilon)
            if (gridnumber*grid*100) < contoverlay :
                gridnumber += 1
            # set contoverlay to new length    
            contoverlay = gridnumber*grid
            wcontact = w+2*contoverlay
        
        # insertion point is at (0,0) - contoverlay    
        xpos1 = 0-contoverlay
        ypos1 = 0
        xpos2 = xpos1+wcontact
        ypos2 = 0
        dir = -1
        stripes = b+1
        
        # set xpos1/xpos2 to left for contacts
        xpos1 = xpos1-contoverlay
        xpos2 = xpos2-contoverlay
        
        # Gat PolyPart of bottom ContactArea
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos1, xpos2, ypos2+poly_cont_len*dir))
        
        wcon = wcontact-2.0*polyover
        distc = consize+conspace
        ncont = fix((wcon+conspace)/distc +epsilon)
        if ncont < 1 :
            ncont = 1
            
        distr = GridFix((wcon-ncont*distc+conspace)*0.5)
        
        # draw ExtBlock for bottom Cont Area
        dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1, xpos2+ext_over, ypos2-ext_over+poly_cont_len*dir))
        
        # **************************************************************
        # draw Cont squares or bars of bottom ContactArea
        # LI and Metal
        # always dot contacts, autogenerated LI
        if drawbar :
            # can only be in internal PCell
            dbCreateRect(self, locintlayer, Box(xpos1+contbar_poly_over, ypos2+li_poly_over*dir, xpos2-contbar_poly_over, ypos2+(consize+li_poly_over)*dir))
        else :
            for i in range(ncont) :
                dbCreateRect(self, locintlayer, Box(xpos1+polyover+distr+i*distc, ypos2+li_poly_over*dir, xpos1+polyover+distr+i*distc+consize, ypos2+(consize+li_poly_over)*dir))
                
        # **************************************************************
        # draw MetalRect and Pin of bottom Contact Area    
        ypos1 = ypos2+(li_poly_over-metover)*dir
        ypos2 = ypos2+(consize+li_poly_over+metover)*dir
        dbCreateRect(self, metlayer, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2))
        MkPin(self, 'PLUS', 1, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2), metlayer)
        
        # **************************************************************
        # Resistorbody
        # **************************************************************
        dir = 1
        xpos1 = xpos1+contoverlay
        ypos1 = 0
        xpos2 = xpos1+w-contoverlay
        ypos2 = ypos1+l*dir
        
        # **************************************************************
        # GatPoly and PolyRes
        # major structures ahead -> here: not applicable
        for i in range(1, stripes+1) :
            xpos2 = xpos1+w
            ypos2 = ypos1+l*dir
            # draw long res line
            # when dogbone and bends>0 shift long res line to inner contactline
            if stripes > 1 :
                if i == 1 :
                    xpos1 = xpos1+contoverlay
                    xpos2 = xpos2+contoverlay
                    
            # all vertical ResPoly and GatPoly Parts   
            dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2))
            dbCreateRect(self, reslayer, Box(xpos1, ypos1, xpos2, ypos2))
            
            ihpAddThermalResLayer(self, Box(xpos1, ypos1, xpos2, ypos2), True, Cell)
            
            if i == 1 :
                dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1, xpos2+ext_over, ypos2))
            else :
                dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1, xpos2+ext_over, ypos2))
                
            # hor connection parts
            if i < stripes : # Connections parts
                ypos1 = ypos2+w*dir
                xpos2 = xpos1+2*w+ps
                ypos2 = ypos1-w*dir
                dir = dir*-1
                # draw res bend
                dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2))
                dbCreateRect(self, reslayer, Box(xpos1, ypos1, xpos2, ypos2))
                if oddp(i) :
                    dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1+ext_over, xpos2+ext_over, ypos2-ext_over))
                else :
                    dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1-ext_over, xpos2+ext_over, ypos2+ext_over))
                    
                xpos1 = xpos1+w+ps
                ypos1 = ypos2
                
        # draw res contact (Top)    
        if stripes >  1 :
            xpos1 = xpos1
            xpos2 = xpos2+contoverlay+contoverlay
        else :
            xpos1 = xpos1-contoverlay
            xpos2 = xpos2+contoverlay
           
        #  GatPoly Part
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos2, xpos2, ypos2+poly_cont_len*dir))
        
        # draw ExtBlock for bottom Cont Area
        dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1, xpos2+ext_over, ypos2+ext_over*dir+poly_cont_len*dir))
        
        #  ExtBlock Part
        # added internal code
        if drawbar :
            dbCreateRect(self, locintlayer, Box(xpos1+contbar_poly_over, ypos2+li_poly_over*dir, xpos2-contbar_poly_over, ypos2+(consize+li_poly_over)*dir))
        else :
            for i in range(ncont) :
                dbCreateRect(self, locintlayer, Box(xpos1+polyover+distr+i*distc, ypos2+li_poly_over*dir, xpos1+polyover+distr+i*distc+consize, ypos2+(consize+li_poly_over)*dir))
                
        # **************************************************************
        #  Metal and Pin Part
        # new metal block   
        ypos1 = ypos2+(li_poly_over-metover)*dir
        ypos2 = ypos2+(consize+li_poly_over+metover)*dir
        dbCreateRect(self, metlayer, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2))
        MkPin(self, 'MINUS', 2, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2), metlayer)
        
        # now draw the label
        resistance = CbResCalc('R', 0, l*1e-6, w*1e-6, b, ps*1e-6, Cell)
        labeltext = Cell + ' r=' + eng_string(resistance)
        labelpos = Point(w/2, l/2)
        labelheight = 0.1
        if w > l :
            rot = 'R0'
        else :
            rot = 'R90'
            
        lbl = dbCreateLabel(self, Layer(textlayer, 'drawing'), labelpos, labeltext, 'centerCenter', rot, Font.EURO_STYLE, labelheight)
        #lsizex = lbl.bbox.getWidth()
        #lsizey = lbl.bbox.getHeight()
        #scale = min(w/lsizex, (l+2*poly_cont_len)/lsizey)
        #SetSGq(lbl scale height)
