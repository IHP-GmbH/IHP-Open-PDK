
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
import math

class isolbox(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):   
        techparams = specs.tech.getTechParams()
        
        CDFVersion = techparams['CDFVersion']
        
        minL       = techparams['isolbox_defLW']
        minW       = techparams['isolbox_defLW']
        defA       = '12.96p'
        defP       = '14.4u'
        
        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', 'isolbox', 'Model name')
             
        specs('l', minL, 'Length')
        specs('w', minW, 'Width')
        specs('wellwidth', '1.05u', 'Well width', ChoiceConstraint(['1.05u', '1.5u']))
        specs('diode_layer', 't', 'Add the DIODE layer', ChoiceConstraint(['t', 'nil']))
        specs('cont_ring', 'nil', 'Add the ring of contacts', ChoiceConstraint(['O', 'U', 'nil']))
        specs('calculate', 'Bv', 'Calculate', ChoiceConstraint(['Bv', 'PWell width']))
        
        specs('pwell_w', '0', 'PWellBlock width')
        specs('Bv', '10.8', 'Break voltage')
        specs('a', defA, 'Area')
        specs('p', defP, 'Perimeter')
        specs('aw', defA, 'Inner Area')
        specs('pw', defP, 'Inner Perimeter')
        specs('Wmin', minW, 'Wmin')
        specs('Lmin', minL, 'Lmin')
        specs('bn', '[@sub:%:sub!]', 'Bulk node connection')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.l = params['l']
        self.w = params['w']
        self.wellwidth = params['wellwidth']
        self.diode_layer = params['diode_layer']
        self.pwell_w = params['pwell_w']
        self.cont_ring = params['cont_ring']

    def genLayout(self):
        l = self.l
        w = self.w
        wellwidth = self.wellwidth
        diode_layer = self.diode_layer
        pwell_w = self.pwell_w
        cont_ring = self.cont_ring

        l = Numeric(l)*1e6
        w = Numeric(w)*1e6
        nw_a = Numeric(wellwidth)*1e6
        pw_width = Numeric(pwell_w)*1e6
        
        dwell = Layer('nBuLay', 'drawing')
        well = Layer('NWell', 'drawing')
        activ = Layer('Activ', 'drawing')
        diode = Layer('Recog', 'diode')
        metal1 = Layer('Metal1', 'drawing')
        contact = Layer('Cont', 'drawing')
        pwbl = Layer('PWell', 'block')
        contW = 0.16
        contS = 0.18
        nbl_nw = 0.62
        nwOact = 0.24
        if wellwidth == '0.85u':
            nwOact2 = 0.32
        else :
            nwOact2 = nwOact
                
        if  wellwidth == '1.05u' :
            dd = 0.4
        else :
            dd = nw_a-nbl_nw
                        
        dbCreateRect(self, dwell, Box(-nw_a+dd, -nw_a+dd, (l-nw_a-dd), (w-nw_a-dd)))
        
        dbCreatePolygon(self, well, PointList([Point(0, 0), Point(l-2*nw_a, 0), Point(l-2*nw_a, w-2*nw_a), Point(0, w-2*nw_a),
                                               Point(0, 0), Point(-nw_a, 0), Point(-nw_a, w-nw_a), Point(l-nw_a, w-nw_a),
                                               Point(l-nw_a, -nw_a), Point(-nw_a, -nw_a), Point(-nw_a, 0)]))
        
        if diode_layer :
            dbCreatePolygon(self, diode, PointList([Point(0, 0), Point(l-2*nw_a, 0), 
                                                    Point(l-2*nw_a, w-2*nw_a), Point(0, w-2*nw_a), 
                                                    Point(0, 0), Point(-nw_a, 0), 
                                                    Point(-nw_a, w-nw_a), Point(l-nw_a, w-nw_a), 
                                                    Point(l-nw_a, -nw_a), Point(-nw_a, -nw_a), 
                                                    Point(-nw_a, 0)]))
            
        if pw_width >  0 :
            dbCreatePolygon(self, pwbl, PointList([Point(-nw_a-pw_width, -nw_a), Point(l-nw_a, -nw_a), 
                                                   Point(l-nw_a, w-nw_a), Point(-nw_a, w-nw_a), 
                                                   Point(-nw_a, -nw_a), Point(-nw_a-pw_width, -nw_a), 
                                                   Point(-nw_a-pw_width, w-nw_a+pw_width), Point(l-nw_a+pw_width, w-nw_a+pw_width), 
                                                   Point(l-nw_a+pw_width, -nw_a-pw_width), Point(-nw_a-pw_width, -nw_a-pw_width)]))
            
        dbCreatePolygon(self, activ, PointList([Point(-(nw_a-nwOact2), -(nw_a-nwOact2)), Point(l-nw_a-nwOact2, -(nw_a-nwOact2)), 
                                                Point(l-nw_a-nwOact2, w-nw_a-nwOact2), Point(-(nw_a-nwOact2), w-nw_a-nwOact2), 
                                                Point(-(nw_a-nwOact2), -nwOact), Point(-nwOact, -nwOact), 
                                                Point(-nwOact, w-2*nw_a+nwOact), Point(l-2*nw_a+nwOact, w-2*nw_a+nwOact), 
                                                Point(l-2*nw_a+nwOact, -nwOact), Point(-(nw_a-nwOact2), -nwOact)]))
                                                
        MkPin(self, 'I', 2, Box(-(nw_a-nwOact2), -(nw_a-nwOact2), -nwOact, w-nw_a-nwOact2), Layer('Activ', 'pin'))
        labelpos = Point(0, -nw_a/2)
        dbCreateLabel(self, Layer('TEXT', 'drawing'), labelpos, 'isolbox', 'centerCenter', 'R0', Font.EURO_STYLE, nw_a/4)
        
        if cont_ring != 'nil':
            venc = 0.06
            xm = nw_a/2+0.015
            wm = contW+venc*2
            off = 0.06
            if wellwidth == '0.85u' :
                xm = xm-0.05
                wm = wm-0.02
                off = 0.05
                
            if cont_ring == 'O' :
                MetalCont(self, -xm+wm/2, w-nw_a*2+xm, l-nw_a*2+xm-wm/2, w-nw_a*2+xm, metal1, contact, wm, contW, contW, contS-off, contS)
                
            MetalCont(self, -xm+wm/2, -xm, l-nw_a*2+xm-wm/2, -xm, metal1, contact, wm, contW, contW, contS-off, contS)
            MetalCont(self, -xm, -xm-wm/2, -xm, w-nw_a*2+xm+wm/2, metal1, contact, wm, contW, contW, off, contS)
            MetalCont(self, l-nw_a*2+xm, -xm-wm/2, l-nw_a*2+xm, w-nw_a*2+xm+wm/2, metal1, contact, wm, contW, contW, off, contS)
