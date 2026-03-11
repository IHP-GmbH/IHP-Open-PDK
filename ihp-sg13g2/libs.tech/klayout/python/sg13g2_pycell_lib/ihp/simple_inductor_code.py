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

class simple_inductor(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']

        defS = '2.1u'
        defW = '2u'
        minS = defS
        minW = defW
        defNr_t  = 1
        minNr_t  = 1
        defL     = '33.303pH'
        defR     = '577.7m'
        model    = 'simple_inductor'
        grid  = techparams['grid']
        minDf = inductor_minD(2, 2.1, defNr_t, grid)
        minD  = str(minDf)+'u'
        defD  = minD

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')

        specs('w', defW, 'Width')
        specs('s', defS, 'Space')
        specs('d', defD, 'The distance in the center of the inductor')
        specs('r', '1m', 'Resistance')
        specs('l', '1p', 'Inductance')
        specs('nr_r', defNr_t, 'The number of turns')
        specs('blockqrc', True, 'Block QRC layer')
        specs('subE', False, 'Substrate Etching')

        specs('lEstim', defL, 'Inductance (estim.)')
        specs('rEstim', defR, 'Resistance (estim.)')

        specs('Wmin', minW, 'Wmin')
        specs('Smin', minS, 'Smin')
        specs('Dmin', defD, 'Dmin')
        specs('minNr_t', minNr_t, 'Minimum number of turns')
        specs('mergeStat', 16, 'Layer mask')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.w = params['w']
        self.s = params['s']
        self.d = params['d']
        self.r = params['r']
        self.l = params['l']
        self.model = params['model']
        self.nr_r = params['nr_r']
        self.blockqrc = params['blockqrc']
        self.subE = params['subE']

    def genLayout(self):
        w = self.w
        s = self.s
        d = self.d
        r = self.r
        l = self.l
        model = self.model
        nr_r = self.nr_r
        blockqrc = self.blockqrc
        subE = self.subE

        cellName = self.__class__.__name__

        w = GridFix(Numeric(w)*5e5)*2
        s = GridFix(Numeric(s)*1e6)
        d = GridFix(Numeric(d)*5e5)*2
        d1 = d

        # layers
        TM2 = Layer('TopMetal2', 'drawing')
        TM1 = Layer('TopMetal1', 'drawing')
        TM2p = Layer('TopMetal2', 'pin')
        TM1p = Layer('TopMetal1', 'pin')
        TV2 = Layer('TopVia2', 'drawing')
        IND = Layer('IND', 'drawing')
        PWellBlock = Layer('PWell', 'block')
        NoActFiller = Layer('Activ', 'nofill')
        NoGatFiller = Layer('GatPoly', 'nofill')
        NoMet1Filler = Layer('Metal1', 'nofill')
        NoMet2Filler = Layer('Metal2', 'nofill')
        NoMet3Filler = Layer('Metal3', 'nofill')
        NoTMet1Filler = Layer('TopMetal1', 'nofill')
        NoTMet2Filler = Layer('TopMetal2', 'nofill')
        NoRCX = Layer('NoRCX', 'drawing')
        substrateE = Layer('LBE', 'drawing')

        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']

        nr_vias = round((w+0.06)/1.96-0.5)

        var = 1+sqrt(2)
        grid = 0.01
        d = max(d, inductor_minD(w, s, nr_r, grid))

        lat_sm = GridFix(d/(2*var))*2
        lat_big = GridFix((d+2*w)/var)
        cateta_sm = (d-lat_sm)/2
        cateta_big = GridFix((d+2*w)/(var*sqrt(2)))

        x1 = GridFix(lat_sm/2)-w
        y1 = 30-w/2
        x2 = GridFix(lat_big/2)
        x = x1+(x2-x1)/2
        y2 = nr_r*w+(nr_r-1)*s+30-w
        x_cross = GridFix(w/sqrt(2)+s/2)
        d_via_cross = GridFix(s*0.4143)+grid
        d1_via_cross = GridFix(w*0.4143)+grid
        x_via = x_cross+d_via_cross+grid

        for pcIndexX in range(nr_r) :
            # Draw side lines
            if nr_r == 1 :
                polyPoints1 = PointList([
                    Point(s/2, y2),                                         Point(s/2, y2+w),
                    Point(lat_sm/2, y2+w),                                  Point(d/2, y2+w+cateta_sm),
                    Point(d/2, y2+w+cateta_sm+lat_sm),                      Point(lat_sm/2, y2+w+d),
                    Point(-lat_sm/2, y2+w+d),                               Point(-d/2, y2+w+cateta_sm+lat_sm),
                    Point(-d/2, y2+w+cateta_sm),                            Point(-lat_sm/2, y2+w),
                    Point(-s/2, y2+w),                                      Point(-s/2, y2),
                    Point(-lat_sm/2-d1_via_cross, y2),                      Point(-(d+2*w)/2, y2+w+cateta_sm-d1_via_cross),
                    Point(-(d+2*w)/2, y2+w+cateta_sm+lat_sm+d1_via_cross),  Point(-lat_sm/2-d1_via_cross, y2+2*w+d),
                    Point(-x_via, y2+2*w+d),                                Point(x_via, y2+w*2+d),
                    Point(lat_sm/2+d1_via_cross, y2+d+2*w),                 Point((d+2*w)/2, y2+w+cateta_sm+lat_sm+d1_via_cross),
                    Point((d+2*w)/2, y2+w+cateta_sm-d1_via_cross),          Point(lat_sm/2+d1_via_cross, y2)
                ])
            else :
                prev_y2 = y2+w+s
                prev_d = d-2*(s+w+grid)
                prev_lat_sm = GridFix(prev_d/(2*var))*2
                delta_2turns = ((x_via+s+w)-s/2) if (nr_r == 2) else 0.0
                delta_first = s/2 if pcIndexX == nr_r-1 else 0.0
                delta_last  = s/2 if pcIndexX == 0 else 0.0

                prev_cateta_sm = (prev_d-prev_lat_sm)/2
                polyPoints1 = PointList([
                    Point(0-delta_first, y2),                               Point(-lat_sm/2-d1_via_cross, y2),
                    Point(-(d+2*w)/2, y2+w+cateta_sm-d1_via_cross),         Point(-(d+2*w)/2, y2+w+cateta_sm+lat_sm+d1_via_cross),
                    Point(-lat_sm/2-d1_via_cross, y2+d+2*w),                Point(lat_sm/2+d1_via_cross, y2+d+2*w),
                    Point((d+2*w)/2, y2+w+cateta_sm+lat_sm+d1_via_cross),   Point((d+2*w)/2, prev_y2+w+prev_cateta_sm-d1_via_cross),
                    Point((d+2*w)/2-w-prev_cateta_sm+d1_via_cross, prev_y2),Point(0+delta_last, prev_y2),
                    Point(0+delta_last, prev_y2+w),                         Point(d/2-prev_cateta_sm, prev_y2+w),
                    Point(d/2, prev_y2+w+prev_cateta_sm),                   Point(d/2, y2+w+cateta_sm+lat_sm),
                    Point(lat_sm/2, y2+w+d),                                Point(-lat_sm/2, y2+w+d),
                    Point(-d/2, y2+w+cateta_sm+lat_sm),                     Point(-d/2, y2+w+cateta_sm),
                    Point(-lat_sm/2, y2+w),                                 Point(0-delta_first, y2+w)         
                ])
                                            
            dbCreatePolygon(self, TM2, polyPoints1)

            # ID TAG
            if pcIndexX == nr_r-1 :
                dbCreateRect(self, IND, Box(-w/2-grid, y2+w*2+d+grid, w/2+grid, y2+w+d-grid))
                dbCreateLabel(self, Layer('TEXT', 'drawing'), Point(0, y2+w+w/2+d), 'L2_TM2', 'centerCenter', 'R0', Font.EURO_STYLE, w/6)
                dbCreateLabel(self, Layer('TEXT', 'drawing'), Point(0, y2+w+w/2+d+w/3), 'l='+l, 'centerCenter', 'R0', Font.EURO_STYLE, w/6)
                dbCreateLabel(self, Layer('TEXT', 'drawing'), Point(0, y2+w+w/2+d-w/3), 'r='+r, 'centerCenter', 'R0', Font.EURO_STYLE, w/6)

            y2 = y2-w-s
            x1 = x_via
            d = d+2*(s+w+grid)
            lat_sm = GridFix(d/(2*var))*2
            lat_big = GridFix((d+2*w)/var)
            cateta_sm = (d-lat_sm)/2
            cateta_big = GridFix((d+2*w)/(var*sqrt(2)))
        # end for;


        # Draw vias
        x1 = (w+s)/2
        x1_via = s/2+0.5+(w-nr_vias*0.9-(nr_vias-1)*1.06-1)/2
        y1_via_l = y2+w+s+0.5+(w-nr_vias*0.9-(nr_vias-1)*1.06-1)/2
        y1_via_r = y2+w+s+0.5+(w-nr_vias*0.9-(nr_vias-1)*1.06-1)/2+(nr_r)*w+(nr_r)*s

        if nr_r >=  2 :
            for pcIndex1 in range(int(nr_vias)) :
                for pcIndex2 in range(int(nr_vias)) :
                    dbCreateRect(self, TV2, Box(-x1_via, y1_via_l, -(x1_via+0.9), y1_via_l+0.9))
                    dbCreateRect(self, TV2, Box(x1_via, y1_via_r, x1_via+0.9, y1_via_r+0.9))
                    x1_via = x1_via+1.96

                x1_via = s/2+0.5+(w-nr_vias*0.9-(nr_vias-1)*1.06-1)/2
                y1_via_l += 1.96
                y1_via_r += 1.96
        

        pinPathPoints1 = PointList([Point(-x1, -1), Point(-x1, w+30)])
        if nr_r == 1 :
            pinPathPoints2 = PointList([Point( x1, -1), Point( x1, (nr_r)*w+(nr_r-1)*s+30)])
        else:
            pinPathPoints2 = PointList([Point( x1, -1), Point( x1, (nr_r+1)*w+(nr_r)*s+30)])

        if nr_r == 1 :
            dbCreatePath(self, TM2, pinPathPoints1, w);
            dbCreatePath(self, TM2, pinPathPoints2, w);
            pcInst1 = dbCreateRect(self, TM2p, Box(x1-w/2, -1, x1+w/2, 1))
            pcInst2 = dbCreateRect(self, TM2p, Box(-x1-w/2, -1, -x1+w/2, 1))
        else :
            dbCreatePath(self, TM1, pinPathPoints1, w);
            dbCreatePath(self, TM1, pinPathPoints2, w);
            pcInst1 = dbCreateRect(self, TM1p, Box(x1-w/2, -1, x1+w/2, 1))
            pcInst2 = dbCreateRect(self, TM1p, Box(-x1-w/2, -1, -x1+w/2, 1))

        pcPin = dbCreatePin(self, 'LB', pcInst1)
        dbCreateLabel(self, Layer('TEXT', 'drawing'), Point(x1, 0), 'LB', 'centerCenter', 'R0', Font.EURO_STYLE, w/2)
        pcPin = dbCreatePin(self, 'LA', pcInst2)
        dbCreateLabel(self, Layer('TEXT', 'drawing'), Point(-x1, 0), 'LA', 'centerCenter', 'R0', Font.EURO_STYLE, w/2)

        dbCreateLabel(self, Layer('TEXT', 'drawing'), Point(0, y2+cateta_sm/2+lat_sm), cellName, 'centerCenter', 'R0', Font.EURO_STYLE, w)

        y2 = 0
        d = d-2*s+2*30
        lat_sm = GridFix(d/(2*var))*2
        lat_big = GridFix((d+2*w)/var)
        cateta_sm = (d-lat_sm)/2
        cateta_big = GridFix((d+2*w)/(var*sqrt(2)))

        polyPoints1 = PointList([Point(lat_sm/2, y2), Point(d/2, y2+cateta_sm), Point(d/2, y2+cateta_sm+lat_sm), Point(lat_sm/2, y2+d), Point(-lat_sm/2, y2+d),
                                 Point(-d/2, y2+cateta_sm+lat_sm), Point(-d/2, y2+cateta_sm), Point(-lat_sm/2, y2)])
        dbCreatePolygon(self, PWellBlock, polyPoints1)
        dbCreatePolygon(self, NoActFiller, polyPoints1)
        dbCreatePolygon(self, NoGatFiller, polyPoints1)
        dbCreatePolygon(self, NoMet1Filler, polyPoints1)
        dbCreatePolygon(self, NoMet2Filler, polyPoints1)
        dbCreatePolygon(self, NoMet3Filler, polyPoints1)

        dbCreatePolygon(self, NoTMet1Filler, polyPoints1)
        dbCreatePolygon(self, NoTMet2Filler, polyPoints1)

        if blockqrc :
            dbCreatePolygon(self, NoRCX, polyPoints1)

        if subE :
            dbCreatePolygon(self, substrateE, polyPoints1)

        y2 = 2*nr_r*w+2*(nr_r-1)*s
        d = d1

