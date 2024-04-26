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
from .thermal import *
from .geometry import *
from .utility_functions import *

import math

class rppd(DloGen):

    @classmethod
    def defineParamSpecs(cls, specs):
        # define parameters and default values
        techparams = specs.tech.getTechParams()
        
        SG13_TECHNOLOGY = techparams["techName"]
        suffix = ""
        if 'SG13G2' in SG13_TECHNOLOGY :
            suffix = 'G2' 
        if 'SG13G3' in SG13_TECHNOLOGY :
            suffix = 'G3'
        
        CDFVersion = techparams['CDFVersion']
        model      = techparams['rppd_model']
        rspec      = techparams['rppd'+suffix+'_rspec']
        rkspec     = techparams['rppd_rkspec']
        rzspec     = techparams['rppd_rzspec']
        defL       = techparams['rppd_defL']
        defW       = techparams['rppd_defW']
        defB       = techparams['rppd_defB']
        defPS      = techparams['rppd_defPS']
        minL       = techparams['rppd_minL']
        minW       = techparams['rppd_minW']
        minPS      = techparams['rppd_minPS']
        eps        = techparams['epsilon2']
        
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('Calculate', 'l', 'Calculate', ChoiceConstraint(['R', 'w', 'l']))
        specs('Recommendation', 'No', 'Recommendation', ChoiceConstraint(['Yes', 'No']))
        specs('model', model, 'Model name')
        
        resistance = CbResCalc('R', 0, defL, defW, defB, defPS, 'rppd')
        specs('R', eng_string(resistance), 'R')
        
        specs('w',  defW, 'Width')
        specs('l',  defL, 'Length')
        specs('b',  defB, 'Bends')
        specs('ps', defPS, 'Poly Space')
        
        imax = CbResCurrent(Numeric(defW), eps, 'rppd'+suffix)
        specs('Imax', imax, 'Imax')
        specs('bn', 'sub!', 'Bulk node connection')
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('PSmin', minPS, 'PSmin')
        specs('Rspec', rspec, 'Rspec [Ohm/sq]')
        specs('Rkspec', rkspec, 'Rkspec [Ohm/cont]')
        specs('Rzspec', rzspec, 'Rzspec [Ohm*m]')
        specs('tc1', '170e-6', 'Temperature coefficient 1')
        specs('tc2', '0.4e-6', 'Temperature coefficient 2')
        specs('PWB', 'No', 'PWell Blockage', ChoiceConstraint(['Yes', 'No']))
        specs('m', '1', 'Multiplier')
        specs('trise', '0.0', 'Temp rise from ambient')
     
    def setupParams(self, params):
        self.grid = self.tech.getGridResolution()
        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']      
        
        self.b = fix(int(params['b']) + self.epsilon)
        self.w = Numeric(params['w'])*1e6
        self.l = Numeric(params['l'])*1e6
        self.ps = Numeric(params['ps'])*1e6
        #self.resistance = Numeric(params['R'])
                
    def genLayout(self):
        psdlayer = Layer('pSD')
        textlayer = Layer('TEXT')
        metlayer = Layer('Metal1')
        locintlayer = Layer('Cont')
        sallayer = Layer('SalBlock')
        contpolylayer = Layer('GatPoly')
        bodypolylayer = Layer('PolyRes')
        extBlocklayer = Layer('EXTBlock')  
        metlayer_pin = Layer('Metal1', 'pin')
        
        lcor = 0.0        
        resshort = 0.0
        gridnumber = 0.0
        contoverlay = 0.0
        contactpush = 0.0
        li_poly_over = 0.0        
        
        internalCode = True
        Cell = self.__class__.__name__
        
        grid = self.techparams['grid']
        endcap = self.techparams['M1_c1']
        consize = self.techparams['Cnt_a']
        conspace = self.techparams['Cnt_b']
        polyover = self.techparams['Cnt_d']        
        psdover1 = self.techparams['pSD_n']
        psdNotch = self.techparams['pSD_b']
        psdover1 = self.techparams['Rppd_b']        
        li_salblock = self.techparams['Sal_e']        
        salover = self.techparams['Sal_c']
        salspace = self.techparams['Sal_d']
        psdover = self.techparams['Rppd_b']
        contbar_min_len = self.techparams['CntB_a1']
        contbar_poly_over = self.techparams['CntB_d']
        metover = self.techparams[Cell + '_met_over_cont']        
        poly_cont_len = consize + polyover # techParam('Cnt_a')+techParam('Cnt_d')            
        wmin = eng_string_to_float(self.techparams[Cell + '_minW'])*1e6
        lmin = eng_string_to_float(self.techparams[Cell + '_minL'])*1e6
        psmin = eng_string_to_float(self.techparams[Cell + '_minPS'])*1e6
        
        wcontact = self.w        
        drawbar = False
        
        # Resistor gets 2 Pins, procedure needs '3' to understand '2'
        dbReplaceProp(self, 'pin#', 3)
        
        if internalCode :
            if wcontact-2*contbar_poly_over + self.epsilon >= contbar_min_len:
                drawbar = True
  
        if psdover1 > psdover: 
            psdover = psdover1

        # dogbone has to be on grid, so make difference in gridsteps
        contoverlay = wcontact - self.w
        if contoverlay > 0:
            # is dogbone: keep on checking for lay on grid
            # Distance per side
            contoverlay = contoverlay/2
            # gridpoints per side?
            gridnumber = contoverlay/self.grid
            gridnumber = round(gridnumber + self.epsilon)
            # need more gridpoints to lay on grip?
            if (gridnumber*grid*100) < contoverlay:
                gridnumber += 1            
            
            # set contoverlay to new length
            contoverlay = gridnumber*grid
            wcontact = w+2*contoverlay
        
        # Insertionpoint for contact is at (0-contoverlay:0)
        xpos1 = 0-contoverlay
        ypos1 = 0
        xpos2 = xpos1+wcontact
        ypos2 = 0
        dir = -1
        stripes = self.b+1

        if self.w < wmin-self.epsilon:
            self.w = wmin
            hiGetAttention()
            print('Width < '+str(wmin))
    
        if self.l < lmin-self.epsilon:
            self.l = lmin
            hiGetAttention()
            print('Length < '+str(lmin))
        
        if self.ps < psmin-self.epsilon:
            ps = psmin
            hiGetAttention()
            print('poly space < '+str(psmin))
        
        # set contacts out of resitor-square?
        lcor = 0.0
        lsumnew = 0.0
        lsumold = 0.0
        
        if GridFix(self.ps) < GridFix((salover+salspace)) and stripes>2:
            contactpush = contactpush+self.w+salover
            resshort = GridFix((2*contactpush)/stripes)+grid
            lsumold = self.l*stripes
            self.l = self.l-resshort
            lsumnew = self.l*stripes+contactpush*2            
            lcor = lsumold-lsumnew
        
        # Check, if contacts have to be asymmetric
        # Some cases need to have asym contacts:
        # 2 stripes and low ps and are not pushed out of resistor
        if zerop(contactpush) is 1 and self.ps-2*contoverlay <= psmin and onep(self.b) is 1:
            asymcont = True
        else :
            asymcont = False

        # set all parts up to get 0:0 at beginning of resistorbody:
        ypos1 = ypos1-contactpush*dir
        ypos2 = ypos2-contactpush*dir
        
        # **************************************************************
        # draw res contact  #1 (bottom)
        # **************************************************************
        # draw res contact #1 -> realise Overlap by dogbone to keep burdens, when needed
        # set xpos1/xpos2 to left for contacts when Stripes>1 and ps<

        if asymcont :
            xpos1 = xpos1-contoverlay
            xpos2 = xpos2-contoverlay
        
        # **************************************************************
        # Gat PolyPart of bottom ContactArea
        # gatpolyarea between salBlock and contact
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos1+contactpush*dir, xpos2, 
                                              ypos2+(contactpush+li_salblock)*dir))
        # gatpolyarea right, left and under contact
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos1+(contactpush+li_salblock)*dir,
                                              xpos2, ypos2+(contactpush+poly_cont_len+li_salblock)*dir))
        # **************************************************************
        # pSD Part of bottom ContactArea
        if contactpush == 0.0:
            dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos2+contactpush*dir,
                                             xpos2+psdover, ypos2+(li_salblock+psdover+poly_cont_len+contactpush)*dir))
        else :
            dbCreateRect(self,  psdlayer, Box(xpos1-psdover, ypos2+(contactpush-salover+psdover)*dir,
                                             xpos2+psdover, ypos2+(li_salblock+psdover+poly_cont_len+contactpush)*dir))
        
        # **************************************************************
        # EXTBlock
        # draw ExtBlock for bottom Cont Area
        dbCreateRect(self, extBlocklayer, Box(xpos1-psdover, ypos2+contactpush*dir,
                                              xpos2+psdover, ypos2+(li_salblock+psdover+poly_cont_len+contactpush)*dir))

        # **************************************************************
        # contact area
        # number parallel contacts ncont, distance distc:
        wcon = wcontact-2.0*polyover
        distc = consize+conspace;        
        ncont = math.floor((wcon+conspace)/distc + self.epsilon)
        if ncont < 1: 
            ncont = 1
            
        distr = GridFix((wcon-ncont*distc+conspace)*0.5);
        
        # draw contact
        # block for internal PCell
        if drawbar :    
            dbCreateRect(self, locintlayer, Box(xpos1+contbar_poly_over, ypos2+(contactpush+li_salblock+li_poly_over)*dir,
                                                xpos2-contbar_poly_over, ypos2+(contactpush+consize+li_salblock+li_poly_over)*dir))
        else :
            for i in range(int(ncont)):
                dbCreateRect(self, locintlayer, Box(xpos1+polyover+distr+i*distc, ypos2+(contactpush+li_salblock+li_poly_over)*dir,
                                                    xpos1+polyover+distr+i*distc+consize, ypos2+(contactpush+consize+li_salblock+li_poly_over)*dir))

        # **************************************************************
        # Metal and pin
        ypos1 = ypos2+(contactpush+li_salblock+li_poly_over-metover)*dir
        ypos2 = ypos2+(contactpush+consize+li_salblock+li_poly_over+metover)*dir
        # new metal block
        dbCreateRect(self, metlayer, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2))
        
        MkPin(self, 'PLUS', 1, Box(xpos1+contbar_poly_over-endcap, ypos1, 
                                   xpos2-contbar_poly_over+endcap, ypos2), metlayer_pin)
        
        # set xpos1/xpos2 back to right for resistorbody
        if asymcont :
            xpos1=xpos1+contoverlay
            xpos2=xpos2+contoverlay        

        ypos1 = 0.0 - contactpush*dir

        # **************************************************************
        # resistorbody:
        # **************************************************************
        dir = 1;
        xpos1 = xpos1+contoverlay
        xpos2 = xpos1+self.w-contoverlay;
        ypos2 = ypos1+(self.l-resshort)*dir;
        # **************************************************************
        # normal contatcs or outlying contacts?
        if contactpush > 0 :   # Contacts are out of Resitorsquare->draw rectangle
            # **************************************************************
            # draw one salblock and pSD over resistor and bends
            # Sal Block over stripes and bends
            dbCreateRect(self, sallayer, Box(xpos1-salover, ypos1-contactpush,
                                             xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos1+self.l+self.w+salover))
        
            dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos1-contactpush,
                                                  xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos1+self.l+self.w+salover))
            # pSD over Stripes and bends
            # lower bends are salover obove 0.0, need to have psdover, so this psd has to be psdover-salover under 0.0
            dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos1-contactpush+salover-psdover,
                                             xpos1+stripes*(self.w+self.ps)-self.ps+psdover, ypos1+self.l+self.w+psdover))
            
            yyy = ypos1-contactpush+salover-psdover
            # maybe draw extra salblock for longer last stripe
            if lcor > 0:
                if oddp(stripes) :   
                    # draw new rect topright          
                    dbCreateRect(self, sallayer, Box(xpos1+stripes*(self.w+self.ps)-self.ps-self.w-salover, ypos1+self.l+self.w+salover,
                                                     xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos1+self.l+self.w+salover+lcor))
                    dbCreateRect(self, extBlocklayer, Box(xpos1+stripes*(self.w+self.ps)-self.ps-self.w-salover, ypos1+self.l+self.w+salover,
                                                          xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos1+self.l+self.w+salover+lcor))
                    dbCreateRect(self, psdlayer, Box(xpos1+stripes*(self.w+self.ps)-self.ps-self.w-psdover, ypos1+self.l+self.w+psdover,
                                                     xpos1+stripes*(self.w+self.ps)-self.ps+psdover, ypos1+self.l+self.w+salover+lcor))

                else :    # draw new rect bottom right
                    dbCreateRect(self, sallayer, Box(xpos1+stripes*(self.w+self.ps)-self.ps-self.w-salover, ypos1-contactpush-lcor,
                                                     xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos1-contactpush))
                    dbCreateRect(self, extBlocklayer, Box(xpos1+stripes*(self.w+self.ps)-self.ps-self.w-salover, ypos1-contactpush-lcor,
                                                          xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos1-contactpush))
                    dbCreateRect(self, psdlayer, Box(xpos1+stripes*(self.w+self.ps)-self.ps-self.w-psdover, ypos1-contactpush-lcor,
                                                     xpos1+stripes*(self.w+self.ps)-self.ps+psdover, yyy))
        else :    #  normal SalBlock, Conts in Resistorsquare
            # draw salblock and pSD over resistor
            dbCreateRect(self, sallayer, Box(xpos1-salover, ypos1, xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos2))      
            dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos1, xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos2))
            dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos1, xpos1+stripes*(self.w+self.ps)-self.ps+psdover, ypos2))
            
            if stripes > 1 :  # cover Bends
                if oddp(stripes) :   # odd stripesnumber
                    dbCreateRect(self, sallayer, Box(xpos1-salover, ypos2,
                                                     xpos1+(stripes-1)*(self.w+self.ps)-ps+salover, ypos2+self.w+salover))
                    dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos2,
                                                          xpos1+(stripes-1)*(self.w+self.ps)-self.ps+salover, ypos2+self.w+salover))
                    dbCreateRect(self, sallayer, Box(xpos1+self.w+self.ps-salover, ypos1,
                                                     xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos1-self.w-salover))
                    dbCreateRect(self, extBlocklayer, Box(xpos1+self.w+self.ps-salover, ypos1,
                                                          xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos1-self.w-salover))
                    dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos2-psdover,
                                                     xpos1+(stripes-1)*(self.w+self.ps)-self.ps+psdover, ypos2+self.w+psdover))
                    dbCreateRect(self, psdlayer, Box(xpos1+self.w+self.ps-psdover, ypos1,
                                                     xpos1+stripes*(self.w+self.ps)-self.ps+psdover, ypos1-self.w-psdover))
                else :  # unodd stripesnumber
                    dbCreateRect(self, sallayer, Box(xpos1-salover, ypos2, 
                                                     xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos2+self.w+salover))
                    dbCreateRect(self, extBlocklayer, Box(xpos1-salover, ypos2,
                                                          xpos1+stripes*(self.w+self.ps)-self.ps+salover, ypos2+self.w+salover))
                    dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos2, 
                                                     xpos1+stripes*(self.w+self.ps)-self.ps+psdover, ypos2+self.w+psdover))
                    
                    if stripes > 2:
                        dbCreateRect(self, sallayer, Box(xpos1+self.w+self.ps-salover, ypos1, 
                                                         xpos1+(stripes-1)*(self.w+self.ps)-self.ps+salover, ypos1-self.w-salover))
                        dbCreateRect(self, extBlocklayer, Box(xpos1+self.w+self.ps-salover, ypos1, 
                                                              xpos1+(stripes-1)*(self.w+self.ps)-self.ps+salover, ypos1-self.w-salover))
                        dbCreateRect(self, psdlayer, Box(xpos1+self.w+self.ps-psdover, ypos1, 
                                                             xpos1+(stripes-1)*(self.w+self.ps)-self.ps+psdover, ypos1-self.w-psdover))
                                                             
        # **************************************************************
        # Resistorbody GatPoly part
        for j in range(int(stripes)):
            i = j + 1
            xpos2=xpos1+self.w;
            ypos2=ypos1+self.l*dir;
            #-----------------
            # draw long res line
            if i == 1 :  # first part has to be longer
                dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1-contactpush*dir, xpos2, ypos2))
                ihpAddThermalResLayer(self, Box(xpos1, ypos1-contactpush*dir, xpos2, ypos2), True, Cell);
            else :
                if i == stripes :   # Last Stripe has to be longer
                    dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2+(contactpush+lcor)*dir))              
                    ihpAddThermalResLayer(self, Box(xpos1, ypos1, xpos2, ypos2+(contactpush+lcor)*dir), True, Cell);
                else :  # all other stripes
                    dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2))        
                    ihpAddThermalResLayer(self, Box(xpos1, ypos1, xpos2, ypos2), True, Cell);
      
            if i < stripes :  # connectionparts
                ypos1 = ypos2+self.w*dir
                xpos2 = xpos1+2*self.w+self.ps
                ypos2 = ypos1-self.w*dir
                dir = dir*-1;
                
                # draw res bend
                dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2))      
                ihpAddThermalResLayer(self, Box(xpos1, ypos1, xpos2, ypos2), True, Cell);
                
                xpos1 = xpos1+self.w+self.ps
                ypos1 = ypos2
    
        # **************************************************************
        # contact area (Top)
        # **************************************************************
        if asymcont :  # contact has to be out of symetric
            xpos1 = xpos1
            xpos2 = xpos2+contoverlay+contoverlay
        else :
            xpos1 = xpos1-contoverlay
            xpos2 = xpos2+contoverlay
        # **************************************************************
        # pSD and SalBlock
        # between res and cont
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos2+(lcor+contactpush)*dir,
                                              xpos2, ypos2+(lcor+contactpush+li_salblock)*dir))
        # cont
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos2+(lcor+contactpush+li_salblock)*dir,
                                              xpos2, ypos2+(lcor+contactpush+poly_cont_len+li_salblock)*dir))
        # psd
        dbCreateRect(self, psdlayer, Box(xpos1-psdover, ypos2+(lcor+contactpush)*dir,
                                         xpos2+psdover, ypos2+(lcor+contactpush+li_salblock+psdover+poly_cont_len)*dir))

        # **************************************************************
        # EXTBlock
        # draw ExtBlock for bottom Cont Area
        dbCreateRect(self, extBlocklayer, Box(xpos1-psdover, ypos2+(lcor+contactpush)*dir,
                                              xpos2+psdover, ypos2+(lcor+contactpush+li_salblock+psdover+poly_cont_len)*dir))

        # **************************************************************
        # contacts
        # codeblock for internal PCel
        if drawbar :  # can only be in internal code
            dbCreateRect(self, locintlayer, Box(xpos1+contbar_poly_over, ypos2+(contactpush+li_salblock+li_poly_over+lcor)*dir,
                                                xpos2-contbar_poly_over, ypos2+(contactpush+consize+li_salblock+li_poly_over+lcor)*dir))
        else :
            for i in range(ncont):
                dbCreateRect(self, locintlayer, Box(xpos1+polyover+distr+i*distc,
                                                    ypos2+(lcor+contactpush+li_salblock+li_poly_over)*dir,
                                                    xpos1+polyover+distr+i*distc+consize,
                                                    ypos2+(lcor+contactpush+consize+li_salblock+li_poly_over)*dir))
        # **************************************************************
        # Metal and Pin

        # metal block
        dbCreateRect(self, metlayer, Box(xpos1+contbar_poly_over-endcap, 
                                         ypos2+(contactpush+li_salblock+li_poly_over-metover+lcor)*dir,
                                         xpos2-contbar_poly_over+endcap, 
                                         ypos2+(contactpush+consize+li_salblock+li_poly_over+metover+lcor)*dir))
        
        MkPin(self, 'MINUS', 2, Box(xpos1+contbar_poly_over-endcap, ypos2+(contactpush+li_salblock+li_poly_over-metover+lcor)*dir, 
                                    xpos2-contbar_poly_over+endcap, ypos2+(contactpush+consize+li_salblock+li_poly_over+metover+lcor)*dir), metlayer_pin)

        # fill notches in pas layer
        if (self.ps-2.0*psdover < psdNotch) and (self.ps-2.0*psdover > 0.0):
            if stripes > 1:
                dbCreateRect(self, psdlayer, Box(self.w+psdover, 0, self.w+self.ps-psdover, -li_salblock-poly_cont_len-psdover))
    
            if stripes > 2:
                xpos1 = xpos1 - self.w - self.ps
                dbCreateRect(self, psdlayer, Box(xpos1+w+psdover, ypos2, xpos1+self.w+self.ps-psdover, ypos2+dir*(li_salblock+poly_cont_len+psdover)))
                
        # **************************************************************
        # now draw the label
        # lcalc
        # create virtuel l for CbResCalc
        lcalc = (self.l*stripes+contactpush*2+lcor)/stripes
        resistance = CbResCalc('R', 0, lcalc*1e-6, self.w*1e-6, self.b, self.ps*1e-6, Cell)
        labeltext = 'rpnd r={0:.3f}'.format(resistance)

        labelpos = Point(self.w/2, self.l/2)
            
        # label scaling. Should always fit into bBox of device
        labelheight = 0.1
        if self.w > self.l:
            rot = 'R0'
        else :
            rot = 'R90'
            
        lbl = dbCreateLabel(self, textlayer, labelpos, labeltext, 'centerCenter', rot, Font.EURO_STYLE, labelheight)
        #lsizex = lbl.bbox.getWidth()
        #lsizey = lbl.bbox.getHeight()
        #scale = min(self.w/lsizex, (self.l+2*poly_cont_len)/lsizey)  
        #SetSGq(lbl scale height) 
