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

class rhigh(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        # define parameters and default values 
        techparams = specs.tech.getTechParams()

        #SG13_TECHNOLOGY = techparams["techName"]
        suffix = "G2"
        #if 'SG13G2' in SG13_TECHNOLOGY :
        #    suffix = 'G2' 
        #if 'SG13G3' in SG13_TECHNOLOGY :
        #    suffix = 'G3'
        
        CDFVersion = techparams['CDFVersion']
        model      = techparams['rhigh_model']
        rspec      = techparams['rhigh_rspec']
        rkspec     = techparams['rhigh_rkspec']
        rzspec     = techparams['rhigh_rzspec']
        defL       = techparams['rhigh_defL']
        defW       = techparams['rhigh_defW']
        defB       = techparams['rhigh_defB']
        defPS      = techparams['rhigh_defPS']
        minL       = techparams['rhigh_minL']
        minW       = techparams['rhigh_minW']
        minPS      = techparams['rhigh_minPS']
        eps        = techparams['epsilon2']
        
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('Calculate', 'l', 'Calculate', ChoiceConstraint(['R', 'w', 'l']))
        specs('Recommendation', 'No', 'Recommendation', ChoiceConstraint(['Yes', 'No']))
        specs('model', model, 'Model name')
        
        resistance = CbResCalc('R', 0, defL, defW, defB, defPS, 'rhigh')
        specs('R', eng_string(resistance), 'R')
        
        specs('w',  defW, 'Width')
        specs('l',  defL, 'Length')
        specs('b',  defB, 'Bends')
        specs('ps', defPS, 'Poly Space')
        
        imax = CbResCurrent(Numeric(defW), eps, 'rhigh'+suffix)
        specs('Imax', imax, 'Imax')
        specs('bn', 'sub!', 'Bulk node connection')
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('PSmin', minPS, 'PSmin')
        specs('Rspec', rspec, 'Rspec [Ohm/sq]')
        specs('Rkspec', rkspec, 'Rkspec [Ohm/cont]')
        specs('Rzspec', rzspec, 'Rzspec [Ohm*m]')
        specs('tc1', '-2300e-6', 'Temperature coefficient 1')
        specs('tc2', '2.1e-6', 'Temperature coefficient 2')
        specs('PWB', 'No', 'PWell Blockage', ChoiceConstraint(['Yes', 'No']))
        specs('m', '1', 'Multiplier')
        specs('trise', '0.0', 'Temp rise from ambient')
        
    def setupParams(self, params):
        # process parameter values entered by user
        self.l = Numeric(params['l'])
        self.w = Numeric(params['w'])
        self.b = int(params['b'])
        self.ps = Numeric(params['ps'])
        #self.resistance = Numeric(params['R'])
        
        self.grid = self.tech.getGridResolution()
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']  

    def genLayout(self):  
        #*************************************************************************
        #*
        #* Cell Properties
        #*
        #*************************************************************************     
        dbReplaceProp(self, 'ivCellType', 'graphic')
        dbReplaceProp(self, 'viewSubType', 'maskLayoutParamCell')
        dbReplaceProp(self, 'instNamePrefix', 'R')
        dbReplaceProp(self, 'function', 'resistor')
        dbReplaceProp(self, 'pcellVersion', '$Revision: 1.0 $')
        dbReplaceProp(self, 'pin#', 3)
        
        #*************************************************************************
        #*
        #* Layer Definitions
        #*
        #*************************************************************************
        contpolylayer = 'GatPoly'
        bodypolylayer = 'PolyRes'
        sallayer = 'SalBlock'
        locintlayer = 'Cont'
        extBlocklayer = 'EXTBlock'
        metlayer = 'Metal1'
        textlayer = Layer('TEXT', 'drawing')
        nsdlayer = 'nSD'
        psdlayer = 'pSD'
        
        #*************************************************************************
        #*
        #* Generic Design Rule Definitions
        #*
        #*************************************************************************
        metover = self.techparams['M1_c']
        salover = self.techparams['Sal_c']
        salover1 = self.techparams['Sal_c']
        salspace = self.techparams['Sal_d']
        psdover1 = self.techparams['Rppd_b']
        consize = self.techparams['Cnt_a']
        conspace = self.techparams['Cnt_b']
        endcap = self.techparams['M1_c1']
        endcap2 = self.techparams['M1_c1']
        polyover = self.techparams['Cnt_d']
        grid = self.techparams['grid']
        contbar_min_len = self.techparams['CntB_a1']
        contbar_poly_over = self.techparams['CntB_d']
        
        #*************************************************************************
        #*
        #* Device Specific Design Rule Definitions
        #*
        #*************************************************************************
        psdover = self.techparams['Rhi_c']
        nsdover = self.techparams['Rhi_c']
        li_salblock = self.techparams['Rhi_d']
        poly_cont_len = consize+polyover # self.techparams['rhigh_poly_cont_len']   # 0.57
        
        # **************** Internal / External *********************************
        # use internalCode True for internal PCell
        internalCode = True
        # **************** Internal / External *********************************
        salblock_nsd_enc = 0.0
        li_poly_over = 0.0
        contactpush = 0.0
        resshort = 0.0
        gridnumber = 0.0
        contoverlay = 0.0
        lcor = 0.0
        psmin = Numeric(self.techparams['rhigh_minPS'])*1e6 
        
        #*************************************************************************
        #*
        #* Instances For Mosaic Fills
        #*
        #*************************************************************************
        Cell = self.__class__.__name__
        #*************************************************************************
        #*
        #* Main body of code
        #*
        #*************************************************************************
       
        l = Numeric(self.l)*1e6;
        w = Numeric(self.w)*1e6;
        b = fix(self.b + self.epsilon)
        ps = Numeric(self.ps)*1e6;
        
        # GGa Attention: Poly must be 2*Cnt_a + Cnt_b + 2*Cnt_d Min Size of Cont + 2* GatPolyEnclosure. Might be dogbone
        wcontact = w
        
        # 10.12.07 GGa added block for internal code
        drawbar = False
        
        if internalCode :
            if wcontact-2*contbar_poly_over + self.epsilon >= contbar_min_len :
                drawbar = True
                
        if psdover1 > psdover :
            psdover = psdover1
            
        if salover1 > salover :
            salover = salover1
            
        nsdover = psdover
        # GGa dogbone has to be on grid, so make difference in gridsteps
        contoverlay = wcontact - w
        if contoverlay > 0 :
            # is dogbone: keep on checking for lay on grid
            # Distance per side
            contoverlay = contoverlay/2
            # gridpoints per side?
            gridnumber = contoverlay/grid
            # make to fixnumber
            gridnumber = round(gridnumber + self.epsilon)
            # need more gridpoints to lay on grip?
            if (gridnumber*grid*100) < contoverlay :
                gridnumber += 1
                
            contoverlay = gridnumber*grid
            wcontact = w+2*contoverlay
        # if
        
        # Insertionpoint for contact is at (0-contoverlay:0)    
        xpos1 = 0-contoverlay
        ypos1 = 0
        xpos2 = xpos1+wcontact
        ypos2 = 0
        dir = -1
        stripes = b+1
        endcap = max(endcap, endcap2)
        metover = max(endcap2, metover)
        
        # set contacts out of resistor-square?
        # GridFix because 0.40000 < (0.20000+0.2000). Works with GridFix
        lsumold = 0.0
        lsumnew = 0.0
        lcor = 0.0
        if GridFix(ps) < GridFix((salover+salspace)) and stripes > 2 :
            contactpush = contactpush+w+salover
            resshort = GridFix((2*contactpush)/stripes)+grid
            lsumold = l*stripes
            l = l-resshort
            lsumnew = l*stripes+contactpush*2
            # need to push out contact2?
            lcor = lsumold-lsumnew
        
        # 05.05.06 GGa Check, if contacts have to be asymmetric
        # Some cases need to have asym contacts:
        # 2 stripes and low ps and are not pushed out of resistor    
        if zerop(contactpush) and (ps-2*contoverlay <= psmin) and onep(b) :
            asymcont = True
        else :
            asymcont = False
        
        # set all parts up to get 0:0 at beginning of resistorbody:    
        ypos1 = ypos1-contactpush*dir
        ypos2 = ypos2-contactpush*dir
        
        # *********************************************************
        # draw res contact #1 -> realise Overlap by dogbone to keep burdens, when needed
        # BOT Contact area
        # *********************************************************
        # set xpos1/xpos2 to left for contacts when Stripes>1 and ps<
        if asymcont :
            xpos1 = xpos1-contoverlay
            xpos2 = xpos2-contoverlay
        
        # *********************************************************
        # gatpolyarea between salBlock and contact    
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos1+contactpush*dir, xpos2, ypos2+(contactpush+poly_cont_len+li_salblock)*dir))
        
        # *********************************************************
        # nSD/pSD EXTBlock
        dbCreateRect(self, psdlayer,      Box(xpos1-psdover, ypos1+(contactpush-psdover)*dir, xpos2+psdover, ypos2+(contactpush+poly_cont_len+li_salblock+psdover)*dir))
        dbCreateRect(self, nsdlayer,      Box(xpos1-psdover, ypos1+(contactpush-psdover)*dir, xpos2+psdover, ypos2+(contactpush+poly_cont_len+li_salblock+psdover)*dir))
        dbCreateRect(self, extBlocklayer, Box(xpos1-psdover, ypos1+(contactpush-psdover)*dir, xpos2+psdover, ypos2+(contactpush+poly_cont_len+li_salblock+psdover)*dir))
        
        # contact area
        # number parallel contacts ncont, distance distc:
        wcon = wcontact-2.0*polyover
        distc = consize+conspace
        ncont = floor((wcon+conspace)/distc + self.epsilon)
        if ncont < 1 :
            ncont = 1
        distr = GridFix((wcon-ncont*distc+conspace)*0.5)
        
        # *********************************************************
        # draw contact
        if drawbar :
            # can only be in internal version
            dbCreateRect(self, locintlayer, Box(xpos1+contbar_poly_over, ypos2+(contactpush+li_salblock+li_poly_over)*dir, xpos2-contbar_poly_over, ypos2+(contactpush+consize+li_salblock+li_poly_over)*dir))
        else :
            for i in range(ncont) :
                dbCreateRect(self, locintlayer, Box(xpos1+polyover+distr+i*distc, ypos2+(contactpush+li_salblock+li_poly_over)*dir, xpos1+polyover+distr+i*distc+consize, ypos2+(contactpush+consize+li_salblock+li_poly_over)*dir))
                
        # 26.6.08 GG: new metal block   
        dbCreateRect(self, metlayer, Box(xpos1+contbar_poly_over-endcap, ypos2+(contactpush+li_salblock+li_poly_over-metover)*dir, xpos2-contbar_poly_over+endcap, ypos2+(contactpush+consize+li_salblock+li_poly_over+metover)*dir))
        MkPin(self, 'PLUS', 1, Box(xpos1+contbar_poly_over-endcap, ypos2+(contactpush+li_salblock+li_poly_over-metover)*dir, xpos2-contbar_poly_over+endcap, ypos2+(contactpush+consize+li_salblock+li_poly_over+metover)*dir), metlayer)
        
        # set xpos1/xpos2 back to right for resistorbody
        if asymcont :
            xpos1 = xpos1+contoverlay
            xpos2 = xpos2+contoverlay
        
        # *********************************************************
        # resistorbody:
        # *********************************************************    
        dir = 1
        xpos1 = xpos1+contoverlay
        xpos2 = xpos1+w-contoverlay
        ypos2 = ypos1+(l-resshort)*dir
        
        # *********************************************************
        # normal contatcs or outlying contacts?
        if contactpush >  0 :
            # *********************************************************
            # draw salblock and pSD over resistor and bends
            # Sal Block over stripes and bends
            dbCreateRect(self, sallayer, Box(xpos1-salover, ypos1-contactpush*dir, xpos1+stripes*(w+ps)-ps+salover, ypos1+l+w+salover))
            # 09.02.07 GGa added EXTBlock
            dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos1-contactpush*dir, xpos1+stripes*(w+ps)-ps+salover, ypos1+l+w+salover))
            # pSD over Stripes and bend
            dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos1-(contactpush-salblock_nsd_enc)*dir, xpos1+stripes*(w+ps)-ps+psdover, ypos1+(l+w+psdover)*dir))
            # nsdBlock over Stripes and Bends
            dbCreateRect(self, nsdlayer, Box(xpos1-nsdover, ypos1-(contactpush-salblock_nsd_enc)*dir, xpos1+stripes*(w+ps)-ps+nsdover, ypos1+(l+w+nsdover)*dir))
            
            # *********************************************************
            # maybe draw extra salblock for longer last stripe
            if lcor > 0 :
                if oddp(stripes) :
                    # draw new rect topright
                    # SalBlock
                    dbCreateRect(self, sallayer, Box(xpos1+stripes*(w+ps)-ps-w-salover, ypos1+l+w+salover, xpos1+stripes*(w+ps)-ps+salover, ypos1+l+w+salover+lcor))
                    # 09.02.07 GGa added EXTBlock
                    dbCreateRect(self, extBlocklayer, Box(xpos1+stripes*(w+ps)-ps-w-salover, ypos1+l+w+salover, xpos1+stripes*(w+ps)-ps+salover, ypos1+l+w+salover+lcor))
                    # pSD
                    dbCreateRect(self, psdlayer, Box(xpos1+stripes*(w+ps)-ps-w-psdover, ypos1+l+w+salover-salblock_nsd_enc, xpos1+stripes*(w+ps)-ps+psdover, ypos1+l+w+salover+lcor-salblock_nsd_enc))
                    # nSD
                    dbCreateRect(self, nsdlayer, Box(xpos1+stripes*(w+ps)-ps-w-nsdover, ypos1+l+w+salover-salblock_nsd_enc, xpos1+stripes*(w+ps)-ps+nsdover, ypos1+l+w+salover+lcor-salblock_nsd_enc))
                else :   # draw new rect bottom right
                    dbCreateRect(self, sallayer, Box(xpos1+stripes*(w+ps)-ps-w-salover, ypos1-contactpush-lcor, xpos1+stripes*(w+ps)-ps+salover, ypos1-contactpush))
                    # 09.02.07 GGa added EXTBlock
                    dbCreateRect(self, extBlocklayer, Box(xpos1+stripes*(w+ps)-ps-w-salover, ypos1-contactpush-lcor, xpos1+stripes*(w+ps)-ps+salover, ypos1-contactpush))
                    dbCreateRect(self, psdlayer, Box(xpos1+stripes*(w+ps)-ps-w-psdover, ypos1-contactpush-lcor+salblock_nsd_enc, xpos1+stripes*(w+ps)-ps+psdover, ypos1-contactpush+salblock_nsd_enc))
                    dbCreateRect(self, nsdlayer, Box(xpos1+stripes*(w+ps)-ps-w-nsdover, ypos1-contactpush-lcor+salblock_nsd_enc, xpos1+stripes*(w+ps)-ps+nsdover, ypos1-contactpush+salblock_nsd_enc))
                # if oddp(stripes)  
            # if lcor>0  
        # *********************************************************               
        else :   # normal SalBlock
        # *********************************************************
            if onep(stripes) :   # only one Stripe->other nSD/pSD
        # *********************************************************
                # one Stripe, only one SalBlock and shorter nSD/pSD
                # draw salblock and pSD over resistor
                dbCreateRect(self, sallayer, Box(xpos1-salover, ypos1, xpos1+stripes*(w+ps)-ps+salover, ypos2))
                # 09.02.07 GGa added EXTBlock
                dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos1, xpos1+stripes*(w+ps)-ps+salover, ypos2))
                dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos1+salblock_nsd_enc*dir, xpos1+stripes*(w+ps)-ps+psdover, ypos2-salblock_nsd_enc))
                dbCreateRect(self, nsdlayer, Box(xpos1-nsdover, ypos1+dir*salblock_nsd_enc, xpos1+stripes*(w+ps)-ps+nsdover, ypos2-salblock_nsd_enc))
            else :   # other nSD/pSD Blockcover Bends
                # draw salblock and pSD over resistor
                dbCreateRect(self, sallayer, Box(xpos1-salover, ypos1, xpos1+stripes*(w+ps)-ps+salover, ypos2))
                # 09.02.07 GGa added EXTBlock
                dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos1, xpos1+stripes*(w+ps)-ps+salover, ypos2))
                dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos1+salblock_nsd_enc*dir, xpos1+stripes*(w+ps)-ps+psdover, ypos2))
                dbCreateRect(self, nsdlayer, Box(xpos1-nsdover, ypos1+dir*salblock_nsd_enc, xpos1+stripes*(w+ps)-ps+nsdover, ypos2))
                if oddp(stripes) :    # draw salblock and pSD over resistor
                    # odd stripesnumber
                    dbCreateRect(self, sallayer, Box(xpos1+w+ps-salover, ypos1, xpos1+stripes*(w+ps)-ps+salover, ypos1-w-salover))
                    # 09.02.07 GGa added EXTBlock
                    dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos2, xpos1+(stripes-1)*(w+ps)-ps+salover, ypos2+w+salover))
                    dbCreateRect(self, sallayer, Box(xpos1+w+ps-salover, ypos1, xpos1+stripes*(w+ps)-ps+salover, ypos1-w-salover))
                    # 09.02.07 GGa added EXTBlock
                    dbCreateRect(self, extBlocklayer, Box(xpos1+w+ps-salover, ypos1, xpos1+stripes*(w+ps)-ps+salover, ypos1-w-salover))
                    dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos2, xpos1+(stripes-1)*(w+ps)-ps+psdover, ypos2+w+psdover))
                    dbCreateRect(self, psdlayer, Box(xpos1+w+ps-psdover, ypos1+salblock_nsd_enc, xpos1+stripes*(w+ps)-ps+psdover, ypos1-w-psdover))
                    dbCreateRect(self, nsdlayer, Box(xpos1-nsdover, ypos2, xpos1+(stripes-1)*(w+ps)-ps+nsdover, ypos2+w+nsdover))
                    dbCreateRect(self, nsdlayer, Box(xpos1+w+ps-nsdover, ypos1+salblock_nsd_enc, xpos1+stripes*(w+ps)-ps+nsdover, ypos1-w-nsdover))
                else :   # unodd stripesnumber
                    dbCreateRect(self, sallayer, Box(xpos1-salover, ypos2, xpos1+stripes*(w+ps)-ps+salover, ypos2+w+salover))
                    # 09.02.07 GGa added EXTBlock
                    dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos2, xpos1+stripes*(w+ps)-ps+salover, ypos2+w+salover))
                    dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos2, xpos1+stripes*(w+ps)-ps+psdover, ypos2+w+psdover))
                    dbCreateRect(self, nsdlayer, Box(xpos1-nsdover, ypos2, xpos1+stripes*(w+ps)-ps+nsdover, ypos2+w+nsdover))
                    if stripes > 2 :
                        dbCreateRect(self, sallayer, Box(xpos1+w+ps-salover, ypos1, xpos1+(stripes-1)*(w+ps)-ps+salover, ypos1-w-salover))
                        # 09.02.07 GGa added EXTBlock
                        dbCreateRect(self, extBlocklayer, Box(xpos1+w+ps-salover, ypos1, xpos1+(stripes-1)*(w+ps)-ps+salover, ypos1-w-salover))
                        dbCreateRect(self, psdlayer, Box(xpos1+w+ps-psdover, ypos1+salblock_nsd_enc, xpos1+(stripes-1)*(w+ps)-ps+psdover, ypos1-w-psdover))
                        dbCreateRect(self, nsdlayer, Box(xpos1+w+ps-nsdover, ypos1+salblock_nsd_enc, xpos1+(stripes-1)*(w+ps)-ps+nsdover, ypos1-w-nsdover))
                    # if stripes > 2
                # if odd(stripes)
            # if onep(stripes)
        # if contactspush > 0
                        
        # *********************************************************
        # GatPoly parts
    
        for i in range(1, int(stripes)+1) :
            xpos2 = xpos1+w
            ypos2 = ypos1+l*dir
            # -----------------
            # draw long res line
            if i ==  1 :
                dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1-contactpush*dir, xpos2, ypos2))
                ihpAddThermalResLayer(self, Box(xpos1, ypos1-contactpush*dir, xpos2, ypos2), True, Cell)
                dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos1-contactpush*dir, xpos2+psdover, ypos2))
                dbCreateRect(self, nsdlayer, Box(xpos1-psdover, ypos1-contactpush*dir, xpos2+psdover, ypos2))
            else :
                # Last Stripe has to be longer
                if i == stripes :
                    dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2+(contactpush+lcor)*dir))
                    ihpAddThermalResLayer(self, Box(xpos1, ypos1, xpos2, ypos2+(contactpush+lcor)*dir), True, Cell)
                    dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos1, xpos2+psdover, ypos2+(contactpush+lcor)*dir))
                    dbCreateRect(self, nsdlayer, Box(xpos1-psdover, ypos1, xpos2+psdover, ypos2+(contactpush+lcor)*dir))
                else : 
                    # all other stripes
                    dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2))
                    ihpAddThermalResLayer(self, Box(xpos1, ypos1, xpos2, ypos2), True, Cell)
                    
                
            if i < stripes : # connectionparts
                ypos1 = ypos2+w*dir
                xpos2 = xpos1+2*w+ps
                ypos2 = ypos1-w*dir
                dir *= -1
                dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2))
                ihpAddThermalResLayer(self, Box(xpos1, ypos1, xpos2, ypos2), True, Cell)
                xpos1 = xpos1+w+ps
                ypos1 = ypos2
        # for
                
        # x1,y1,x2,y2,dir are updated, so the code of first contact can be used
        # (Except Pin Informations)

        # *********************************************************
        # TOP Contact Area
        #draw res contact -> realise Overlap with dogbone, to keep burdens
        # set x1 x2 to dogbone,:
        #contact has to be out of symetric
           
        if asymcont :
            xpos1 = xpos1
            xpos2 = xpos2+contoverlay+contoverlay
        else :   # leave, where ist is
            xpos1 = xpos1-contoverlay
            xpos2 = xpos2+contoverlay
        
        # *********************************************************
        # pSD and SalBlock
        # between res and cont    
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos2+(lcor+contactpush)*dir, xpos2, ypos2+(lcor+contactpush+poly_cont_len+li_salblock)*dir))
        # *********************************************************
        # 26.6.08 GG: nSD/pSD added
        dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos2+(lcor+contactpush-psdover)*dir, xpos2+psdover, ypos2+(lcor+contactpush+poly_cont_len+li_salblock+psdover)*dir))
        dbCreateRect(self, nsdlayer, Box(xpos1-psdover, ypos2+(lcor+contactpush-psdover)*dir, xpos2+psdover, ypos2+(lcor+contactpush+poly_cont_len+li_salblock+psdover)*dir))
        # 11.02.09 GGa added EXTBlockLayer
        dbCreateRect(self, extBlocklayer, Box(xpos1-psdover, ypos2+(lcor+contactpush-psdover)*dir, xpos2+psdover, ypos2+(lcor+contactpush+poly_cont_len+li_salblock+psdover)*dir))
        
        # *********************************************************
        # contacts
        # 10.12.07 GGa added internal code block
        if drawbar :
            # can only be in internal version
            lastCont = dbCreateRect(self, locintlayer, Box(xpos1+contbar_poly_over, ypos2+(lcor+contactpush+li_salblock+li_poly_over)*dir, xpos2-contbar_poly_over, ypos2+(lcor+contactpush+consize+li_salblock+li_poly_over)*dir))
        else :
            for i in range(ncont) :
                lastCont = dbCreateRect(self, locintlayer, Box(xpos1+polyover+distr+i*distc, ypos2+(lcor+contactpush+li_salblock+li_poly_over)*dir, xpos1+polyover+distr+i*distc+consize, ypos2+(lcor+contactpush+consize+li_salblock+li_poly_over)*dir))
                
        # 26.6.08 GG: new metal block
        # *********************************************************
        # Metal and pin
        bBox = lastCont.getBBox()
        dbCreateRect(self, metlayer, Box(bBox.left-endcap, bBox.bottom-endcap, bBox.right+endcap, bBox.top+endcap))
    
        MkPin(self, 'MINUS', 2, Box(bBox.left-endcap, bBox.bottom-endcap, bBox.right+endcap, bBox.top+endcap), metlayer)
        
        # *********************************************************
        # draw the label
        # GGa 08.05.06 added lcalc
        # create virtuel l for CbResCalc
        lcalc = (l*stripes+contactpush*2+lcor)/stripes
        resistance = CbResCalc('R', 0, lcalc*1e-6, w*1e-6, b, ps*1e-6, Cell)
        labeltext = 'rpnd r={0:.3f}'.format(resistance)
        labelpos = Point(w/2, l/2)
        labelheight = 0.1
        if w > l :
            rot = 'R0'
        else :
            rot = 'R90'
            
        lbl = dbCreateLabel(self, textlayer, labelpos, labeltext, 'centerCenter', rot, Font.EURO_STYLE, labelheight)
        #lsizex = lbl.bbox.getWidth()
        #lsizey = lbl.bbox.getHeight()
        #scale = min(w/lsizex, (l+2*poly_cont_len)/lsizey)
        #SetSGq(lbl scale height)
