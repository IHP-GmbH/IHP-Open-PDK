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

        SG13_TECHNOLOGY = techparams["techName"]
        suffix = ""
        if 'SG13G2' in SG13_TECHNOLOGY :
            suffix = 'G2'
        if 'SG13G3' in SG13_TECHNOLOGY :
            suffix = 'G3'

        CDFVersion = techparams['CDFVersion']
        model      = techparams['rsil_model']
        rspec      = techparams['rsil'+suffix+'_rspec']
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
        if 'SG13G2' in SG13_TECHNOLOGY :
            defR   = '17.248'
        else :
            defR   = '16.923'

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('Calculate', 'l', 'Calculate', ChoiceConstraint(['R', 'w', 'l']))
        specs('Recommendation', 'No', 'Recommendation', ChoiceConstraint(['Yes', 'No']))
        specs('model', model, 'Model name')

        resistance = CbResCalc('R', 0, defL, defW, defB, defPS, 'rsil')
        specs('R', eng_string(resistance), 'R')

        specs('w',  defW, 'Width')
        specs('l',  defL, 'Length')
        specs('b',  defB, 'Bends')
        specs('ps', defPS, 'Poly Space')

        imax = CbResCurrent(Numeric(defW), eps, 'rsil'+suffix)
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
        specs('PWB', 'No', 'PWell Blockage', ChoiceConstraint(['Yes', 'No']))
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

        contpolylayer = 'GatPoly'
        bodypolylayer = 'PolyRes'
        reslayer = 'RES'
        extBlocklayer = 'EXTBlock'
        locintlayer = 'Cont'
        metlayer = 'Metal1'
        textlayer = 'TEXT'

        internalCode = True
        Cell = self.__class__.__name__

        metover = self.techparams[Cell+'_met_over_cont']
        consize = self.techparams['Cnt_a']          # min and max size of Cont
        conspace = self.techparams['Cnt_b']         # min ContSpace
        polyover = self.techparams['Cnt_d']         # min GatPoly enclosure of Cont
        li_poly_over = self.techparams['Rsil_b']    # min RES Spacing to Cont
        ext_over = self.techparams['Rsil_e']        # min EXTBlock enclosure of RES
        endcap = self.techparams['M1_c1']
        poly_cont_len = li_poly_over+consize+polyover   # end of RES to end of poly
        contbar_poly_over = self.techparams['CntB_d']   # min length of LI-Bar
        contbar_min_len = self.techparams['CntB_a1']    # min length of LI-Bar

        wmin = eng_string_to_float(self.techparams[Cell+'_minW'])*1e6       # min Width
        lmin = eng_string_to_float(self.techparams[Cell+'_minL'])*1e6       # Min Length
        psmin = eng_string_to_float(self.techparams[Cell+'_minPS'])*1e6     # min PolySpace

        gridnumber = 0.0
        contoverlay = 0.0

        #dbReplaceProp(pcCV, 'pin#', 'int', 3)
        l = Numeric(l)*1e6
        w = Numeric(w)*1e6
        b = fix(b + self.epsilon)
        ps = Numeric(ps)*1e6
        wcontact = w
        drawbar = False

        if internalCode == True :
            if wcontact-2*contbar_poly_over + self.epsilon >= contbar_min_len :
                drawbar = True

        if metover < endcap :
            metover = endcap

        contoverlay = wcontact - w
        if contoverlay > 0 :
            contoverlay = contoverlay/2
            gridnumber = contoverlay/grid
            gridnumber = round(gridnumber + self.epsilon)
            if (gridnumber*grid*100) < contoverlay :
                gridnumber += 1

            contoverlay = gridnumber*grid
            wcontact = w+2*contoverlay

        # insertion point is at (0,0) - contoverlay
        xpos1 = 0-contoverlay
        ypos1 = 0
        xpos2 = xpos1+wcontact
        ypos2 = 0
        Dir = -1
        stripes = b+1
        if w < wmin-self.epsilon :
            w = wmin
            hiGetAttention()
            print('Width < '+str(wmin))

        if l < lmin-self.epsilon :
            l = lmin
            hiGetAttention()
            print('Length < '+str(lmin))

        if ps < psmin-self.epsilon :
            ps = psmin
            hiGetAttention()
            print('poly space < '+str(psmin))

        # **************************************************************
        # draw res contact  #1 (bottom)
        # **************************************************************

        # set xpos1/xpos2 to left for contacts
        xpos1 = xpos1-contoverlay
        xpos2 = xpos2-contoverlay
        # Gat PolyPart of bottom ContactArea
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos1, xpos2, ypos2+poly_cont_len*Dir))

        # number parallel conts: ncont, distance: distc:
        wcon = wcontact-2.0*polyover
        distc = consize+conspace
        ncont = fix((wcon+conspace)/distc + self.epsilon)
        if ncont < 1 :
            ncont = 1

        distr = GridFix((wcon-ncont*distc+conspace)*0.5)

        # **************************************************************
        # draw Cont squares or bars of bottom ContactArea
        # LI and Metal
        # always dot contacts, autogenerated LI
        if drawbar == True :
            dbCreateRect(self, locintlayer, Box(xpos1+contbar_poly_over, ypos2+li_poly_over*Dir, xpos2-contbar_poly_over, ypos2+(consize+li_poly_over)*Dir))
        else :
            for i in range(ncont) :
                dbCreateRect(self, locintlayer, Box(xpos1+polyover+distr+i*distc, ypos2+li_poly_over*Dir, xpos1+polyover+distr+i*distc+consize, ypos2+(consize+li_poly_over)*Dir))


        # **************************************************************
        # draw MetalRect and Pin of bottom Contact Area
        ypos1 = ypos2+(li_poly_over-metover)*Dir
        ypos2 = ypos2+(consize+li_poly_over+metover)*Dir
        dbCreateRect(self, metlayer, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2))
        MkPin(self, 'PLUS', 1, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2), metlayer)

        # **************************************************************
        # Resistorbody
        # **************************************************************
        Dir = 1
        # set xpos1 & xpos2 correct with contoverlay
        xpos1 = xpos1+contoverlay
        ypos1 = 0
        xpos2 = xpos1+w-contoverlay
        ypos2 = ypos1+l*Dir

        # **************************************************************
        # GatPoly and PolyRes
        # major structures ahead -> here: not applicable
        for i in range(1, int(stripes)+1) :
            xpos2 = xpos1+w
            ypos2 = ypos1+l*Dir
            # draw long res line
            # when dogbone and bends>0 shift long res line to inner contactline
            if stripes > 1 :
                if i == 1 :
                    # fist stripe move to right
                    xpos1 = xpos1+contoverlay
                    xpos2 = xpos2+contoverlay

            # all vertical ResPoly and GatPoly Parts
            dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2))
            dbCreateRect(self, reslayer, Box(xpos1, ypos1, xpos2, ypos2))

            ihpAddThermalResLayer(self, Box(xpos1, ypos1, xpos2, ypos2), True, Cell)

            # **************************************************************
            # EXTBlock
            if i ==  1 :
                dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1, xpos2+ext_over, ypos2))
            else :
                dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1, xpos2+ext_over, ypos2))

            # **************************************************************
            # hor connection parts
            if i < stripes : # Connections parts
                ypos1 = ypos2+w*Dir
                xpos2 = xpos1+2*w+ps
                ypos2 = ypos1-w*Dir
                Dir *= -1
                # draw res bend
                dbCreateRect(self, bodypolylayer, Box(xpos1, ypos1, xpos2, ypos2))
                dbCreateRect(self, reslayer, Box(xpos1, ypos1, xpos2, ypos2))
                # decide in which direction the part is drawn
                if oddp(i) :
                    dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1+ext_over, xpos2+ext_over, ypos2-ext_over))
                else :
                    dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1-ext_over, xpos2+ext_over, ypos2+ext_over))

                xpos1 = xpos1+w+ps
                ypos1 = ypos2


        # x1,y1,x2,y2,dir are updated, use code from first contact, only pin is different
        # **************************************************************
        # draw res contact (Top)
        # **************************************************************
        # set x1 x2 to dogbone,:
        if stripes >  1 :
            xpos1 = xpos1
            xpos2 = xpos2+contoverlay+contoverlay
        else :
            xpos1 = xpos1-contoverlay
            xpos2 = xpos2+contoverlay

        # **************************************************************
        #  GatPoly Part
        dbCreateRect(self, contpolylayer, Box(xpos1, ypos2, xpos2, ypos2+poly_cont_len*Dir))

        # draw contacts
        # LI and Metal
        # always dot contacts with auto-generated LI

        # **************************************************************
        # EXTBlock
        # draw ExtBlock for bottom Cont Area
        dbCreateRect(self, extBlocklayer, Box(xpos1-ext_over, ypos1, xpos2+ext_over, ypos2+ext_over*Dir+poly_cont_len*Dir))

        # **************************************************************
        #  ExtBlock Part
        # added internal code
        if drawbar == True :
            # can only be in internal PCell
            dbCreateRect(self, locintlayer, Box(xpos1+contbar_poly_over, ypos2+li_poly_over*Dir, xpos2-contbar_poly_over, ypos2+(consize+li_poly_over)*Dir))
        else :
            for i in range(ncont) :
                dbCreateRect(self, locintlayer, Box(xpos1+polyover+distr+i*distc, ypos2+li_poly_over*Dir, xpos1+polyover+distr+i*distc+consize, ypos2+(consize+li_poly_over)*Dir))

        # **************************************************************
        #  Metal ans Pin Part
        # new metal block
        ypos1 = ypos2+(li_poly_over-metover)*Dir
        ypos2 = ypos2+(consize+li_poly_over+metover)*Dir
        dbCreateRect(self, metlayer, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2))
        MkPin(self, 'MINUS', 2, Box(xpos1+contbar_poly_over-endcap, ypos1, xpos2-contbar_poly_over+endcap, ypos2), metlayer)

        # **************************************************************
        # now draw the label
        resistance = CbResCalc('R', 0, l*1e-6, w*1e-6, b, ps*1e-6, Cell)
        labeltext = '{0} r={1:.3f}'.format(Cell, resistance)
        labelpos = Point(w/2, l/2)
        print(f"w={w}, l={l}, text='{labeltext}'")

        # label scaling. Should always fit into bBox of device
        labelheight = 0.1    # use 1.0 to avoid later multiplication
        if w > l :
            rot = 'R0'
        else :
            rot = 'R90'

        # lbl
        lbl = dbCreateLabel(self, Layer(textlayer, 'drawing'), labelpos, labeltext, 'centerCenter', rot, Font.EURO_STYLE, labelheight)
        lsizex = lbl.bbox.getWidth()
        lsizey = lbl.bbox.getHeight()
        print(f"lsizex={lsizex}, lsizey={lsizey}")
        scale = min(w/lsizex, (l+2*poly_cont_len)/lsizey)
        #SetSGq(lbl scale height)
