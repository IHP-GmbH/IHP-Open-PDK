########################################################################
#
# Copyright 2026 IHP PDK Authors
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

__version__ = "$Revision: #4 $"

from cni.dlo import *
from .geometry import *
from .utility_functions import *

class chipText(DloGen):

    @classmethod
    def defineParamSpecs(self, specs): 
        # define parameters and default values   
        specs('Height', '50', 'Height')
        specs('letSpc', '2', 'letSpc')
        specs('Layers', 'TopMetal1', 'Layers')
        specs('Text', 'Text', 'Text')
        
    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.Height = self.params['Height']
        self.letSpc = self.params['letSpc']
        self.Layers = self.params['Layers']
        self.Text = self.params['Text']

    def genLayout(self):
        Size = round(Numeric(self.Height))
        # no lower-case letters
        Text = self.Text.upper()
        
        LayerList = self.Layers.split()
        
        Poly  = self.definePoints()
        poly  = PointList()
        poly2 = PointList()
        
        # 40 - because it is default character size
        mag = Size/40.0
        
        # write down text for every layer in the list
        for layer in LayerList :
            x = 0
            y = 0
            for ch in Text :
                if ch != ' ' and ch != '\n' :
                    
                    if ch in Poly :
                        poly = Poly[ch]
                    else :
                        poly = PointList([Point(0, 0), Point(25, 0), Point(25, 5), Point(0, 5)])
                    
                    poly2 = PointList()
                    
                    for xy in poly :
                        # Move origin
                        xneu = xy.x*mag+x
                        yneu = xy.y*mag+y
                        poly2.insert(0, Point(xneu, yneu))
                        
                    curChar = dbCreatePolygon(self, Layer(layer, 'drawing'), poly2)
                
                x_max = max(p.x for p in curChar.getPoints())
                x = x_max+Numeric(self.letSpc)*mag
                
    def definePoints(self):
        poly = dict()
        
        poly['0'] = PointList([Point(25, 34), Point(19, 40), Point(14, 40), Point(14, 35), Point(16, 35), Point(20, 31), Point(20, 28), Point(10, 18), Point(14, 14), Point(18, 18), Point(20, 18), Point(20, 9), Point(16, 5),
                               Point(9, 5), Point(5, 9), Point(5, 31), Point(9, 35), Point(11, 35), Point(11, 40), Point(6, 40), Point(0, 34), Point(0, 6), Point(6, 0), Point(19, 0), Point(25, 6)])

        poly['1'] = PointList([Point(8, 31), Point(5, 31), Point(2, 28), Point(-2, 32), Point(6, 40), Point(13, 40), Point(13, 5), Point(20, 5), Point(20, 0), Point(0, 0), Point(0, 5), Point(8, 5)])

        poly['2'] = PointList([Point(5, 27), Point(0, 27), Point(0, 34), Point(6, 40), Point(19, 40), Point(25, 34), Point(25, 25), Point(7, 7), Point(7, 5), Point(25, 5), Point(25, 0), Point(0, 0),
                               Point(0, 8), Point(20, 28), Point(20, 31), Point(16, 35), Point(9, 35), Point(5, 31)])

        poly['3'] = PointList([Point(25, 14), Point(19, 20), Point(25, 26), Point(25, 34), Point(19, 40), Point(6, 40), Point(0, 34), Point(4, 30), Point(9, 35), Point(16, 35), Point(20, 31), Point(20, 29), Point(14, 23),
                               Point(11, 23), Point(11, 17), Point(14, 17), Point(20, 11), Point(20, 9), Point(16, 5), Point(9, 5), Point(4, 10), Point(0, 6), Point(6, 0), Point(19, 0), Point(25, 6)])

        poly['4'] = PointList([Point(0, 30), Point(10, 40), Point(15, 40), Point(15, 35), Point(5, 25), Point(5, 15), Point(10, 15), Point(10, 22), Point(15, 22), Point(15, 15), Point(21, 15), Point(21, 10),
                               Point(15, 10), Point(15, 0), Point(10, 0), Point(10, 10), Point(0, 10)])

        poly['5'] = PointList([Point(25, 35), Point(5, 35), Point(5, 25), Point(19, 25), Point(25, 19), Point(25, 6), Point(19, 0), Point(6, 0), Point(0, 6), Point(4, 10), Point(9, 5), Point(16, 5), Point(20, 9),
                               Point(20, 16), Point(16, 20), Point(0, 20), Point(0, 40), Point(25, 40)])

        poly['6'] = PointList([Point(21, 30), Point(16, 35), Point(10, 35), Point(5, 30), Point(5, 9), Point(9, 5), Point(16, 5), Point(20, 9), Point(20, 16), Point(16, 20), Point(9, 20), Point(9, 25), Point(19, 25),
                               Point(25, 19), Point(25, 6), Point(19, 0), Point(6, 0), Point(0, 6), Point(0, 34), Point(6, 40), Point(19, 40), Point(25, 34)])

        poly['7'] = PointList([Point(0, 32), Point(0, 40), Point(22, 40), Point(22, 20), Point(25, 20), Point(25, 15), Point(22, 15), Point(22, 0), Point(16, 0), Point(16, 15), Point(9, 15), Point(9, 20), Point(16, 20), Point(16, 35), Point(5, 35), Point(5, 32)])

        poly['8'] = PointList([Point(11, 35), Point(8, 35), Point(5, 32), Point(5, 30), Point(10, 25), Point(11, 25), Point(11, 20), Point(9, 20), Point(5, 16), Point(5, 9), Point(9, 5), Point(16, 5), Point(20, 9), Point(20, 16),
                               Point(16, 20), Point(14, 20), Point(14, 25), Point(15, 25), Point(20, 30), Point(20, 32), Point(17, 35), Point(14, 35), Point(14, 40), Point(20, 40), Point(25, 35), Point(25, 27), Point(21, 23), Point(25, 19),
                               Point(25, 6), Point(19, 0), Point(6, 0), Point(0, 6), Point(0, 19), Point(4, 23), Point(0, 27), Point(0, 35), Point(5, 40), Point(11, 40)])

        poly['9'] = PointList([Point(17, 15), Point(6, 15), Point(0, 21), Point(0, 34), Point(6, 40), Point(19, 40), Point(25, 34), Point(25, 6), Point(19, 0), Point(6, 0), Point(0, 6), Point(4, 10), Point(9, 5), Point(16, 5), Point(20, 9),
                               Point(20, 31), Point(16, 35), Point(9, 35), Point(5, 31), Point(5, 24), Point(9, 20), Point(17, 20)])

        poly['A'] = PointList([Point(0, 0), Point(0, 34), Point(6, 40), Point(19, 40), Point(25, 34), Point(25, 0), Point(20, 0), Point(20, 13), Point(8, 13), Point(8, 18), Point(20, 18), Point(20, 31), Point(16, 35), Point(9, 35), Point(5, 31), Point(5, 0)])

        poly['B'] = PointList([Point(25, 18), Point(20, 23), Point(25, 28), Point(25, 34), Point(19, 40), Point(8, 40), Point(8, 35), Point(16, 35), Point(19, 32), Point(19, 30), Point(14, 25), Point(8, 25), Point(8, 20), Point(14, 20),
                               Point(20, 14), Point(20, 9), Point(16, 5), Point(5, 5), Point(5, 40), Point(0, 40), Point(0, 0), Point(19, 0), Point(25, 6)])

        poly['C'] = PointList([Point(20, 31), Point(16, 35), Point(9, 35), Point(5, 31), Point(5, 9), Point(9, 5), Point(16, 5), Point(20, 9), Point(20, 13), Point(25, 13), Point(25, 6), Point(19, 0), Point(6, 0),
                               Point(0, 6), Point(0, 34), Point(6, 40), Point(19, 40), Point(25, 34), Point(25, 27), Point(20, 27)])

        poly['D'] = PointList([Point(0, 40), Point(5, 40), Point(5, 5), Point(16, 5), Point(20, 9), Point(20, 31), Point(16, 35), Point(8, 35), Point(8, 40), Point(19, 40), Point(25, 34), Point(25, 5), Point(20, 0), Point(0, 0)])

        poly['E'] = PointList([Point(5, 23), Point(22, 23), Point(22, 18), Point(5, 18), Point(5, 5), Point(25, 5), Point(25, 0), Point(0, 0), Point(0, 40), Point(25, 40), Point(25, 35), Point(5, 35)])

        poly['F'] = PointList([Point(25, 35), Point(5, 35), Point(5, 23), Point(20, 23), Point(20, 18), Point(5, 18), Point(5, 0), Point(0, 0), Point(0, 40), Point(25, 40)])

        poly['G'] = PointList([Point(20, 31), Point(16, 35), Point(9, 35), Point(5, 31), Point(5, 9), Point(9, 5), Point(16, 5), Point(20, 9), Point(20, 15), Point(12, 15), Point(12, 20), Point(25, 20), Point(25, 6), Point(19, 0), Point(6, 0),
                               Point(0, 6), Point(0, 34), Point(6, 40), Point(19, 40), Point(25, 34), Point(25, 27), Point(20, 27)])

        poly['H'] = PointList([Point(5, 24), Point(20, 24), Point(20, 40), Point(25, 40), Point(25, 0), Point(20, 0), Point(20, 19), Point(5, 19), Point(5, 0), Point(0, 0), Point(0, 40), Point(5, 40)])

        poly['I'] = PointList([Point(15, 40), Point(15, 35), Point(10, 35), Point(10, 5), Point(15, 5), Point(15, 0), Point(0, 0), Point(0, 5), Point(5, 5), Point(5, 35), Point(0, 35), Point(0, 40)])

        poly['J'] = PointList([Point(0, 40), Point(25, 40), Point(25, 6), Point(19, 0), Point(6, 0), Point(0, 6), Point(0, 13), Point(5, 13), Point(5, 9), Point(9, 5), Point(16, 5), Point(20, 9), Point(20, 35), Point(0, 35)])

        poly['K'] = PointList([Point(5, 26), Point(7, 26), Point(21, 40), Point(25, 36), Point(10, 21), Point(25, 6), Point(25, 0), Point(20, 0), Point(20, 3), Point(7, 16), Point(5, 16), Point(5, 0), Point(0, 0), Point(0, 40), Point(5, 40)])

        poly['L'] = PointList([Point(5, 5), Point(25, 5), Point(25, 0), Point(0, 0), Point(0, 40), Point(5, 40)])

        poly['M'] = PointList([Point(25, 40), Point(20, 40), Point(13, 33), Point(12, 33), Point(5, 40), Point(0, 40), Point(0, 0), Point(5, 0), Point(5, 27), Point(8, 27), Point(12, 23), Point(13, 23), Point(17, 27), Point(20, 27), Point(20, 0), Point(25, 0)])

        poly['N'] = PointList([Point(0, 0), Point(0, 40), Point(6, 40), Point(18, 28), Point(20, 28), Point(20, 40), Point(25, 40), Point(25, 0), Point(20, 0), Point(20, 18), Point(7, 31), Point(5, 31), Point(5, 0)])

        poly['O'] = PointList([Point(11, 35), Point(9, 35), Point(5, 31), Point(5, 9), Point(9, 5), Point(16, 5), Point(20, 9), Point(20, 31), Point(16, 35), Point(14, 35), Point(14, 40), Point(19, 40), Point(25, 34), Point(25, 6), Point(19, 0), Point(6, 0),
                               Point(0, 6), Point(0, 34), Point(6, 40), Point(11, 40)])

        poly['P'] = PointList([Point(0, 0), Point(0, 40), Point(19, 40), Point(25, 34), Point(25, 21), Point(19, 15), Point(8, 15), Point(8, 20), Point(16, 20), Point(20, 24), Point(20, 31), Point(16, 35), Point(5, 35), Point(5, 0)])

        poly['Q'] = PointList([Point(11, 35), Point(9, 35), Point(5, 31), Point(5, 9), Point(9, 5), Point(10, 5), Point(20, 15), Point(20, 31), Point(16, 35), Point(14, 35), Point(14, 40), Point(19, 40), Point(25, 34), Point(25, 12), Point(20, 7),
                               Point(20, 5), Point(25, 5), Point(25, 0), Point(6, 0), Point(0, 6), Point(0, 34), Point(6, 40), Point(11, 40)])

        poly['R'] = PointList([Point(25, 0), Point(20, 0), Point(20, 4), Point(8, 16), Point(8, 21), Point(16, 21), Point(20, 25), Point(20, 31), Point(16, 35), Point(5, 35), Point(5, 0), Point(0, 0), Point(0, 40), Point(19, 40), Point(25, 34),
                               Point(25, 22), Point(18, 15), Point(18, 14), Point(25, 7)])

        poly['S'] = PointList([Point(20, 29), Point(20, 31), Point(16, 35), Point(9, 35), Point(5, 31), Point(5, 29), Point(9, 25), Point(19, 25), Point(25, 19), Point(25, 6), Point(19, 0), Point(6, 0), Point(0, 6), Point(0, 11), Point(5, 11), Point(5, 9),
                               Point(9, 5), Point(16, 5), Point(20, 9), Point(20, 16), Point(16, 20), Point(6, 20), Point(0, 26), Point(0, 34), Point(6, 40), Point(19, 40), Point(25, 34), Point(25, 29)])

        poly['T'] = PointList([Point(25, 35), Point(15, 35), Point(15, 0), Point(10, 0), Point(10, 35), Point(0, 35), Point(0, 40), Point(25, 40)])

        poly['U'] = PointList([Point(5, 9), Point(9, 5), Point(16, 5), Point(20, 9), Point(20, 40), Point(25, 40), Point(25, 6), Point(19, 0), Point(6, 0), Point(0, 6), Point(0, 40), Point(5, 40)])

        poly['V'] = PointList([Point(5, 40), Point(5, 25), Point(10, 20), Point(10, 5), Point(15, 5), Point(15, 20), Point(20, 25), Point(20, 40), Point(25, 40), Point(25, 22), Point(20, 17), Point(20, 0), Point(5, 0), Point(5, 17), Point(0, 22), Point(0, 40)])

        poly['W'] = PointList([Point(0, 40), Point(5, 40), Point(5, 11), Point(8, 11), Point(14, 17), Point(20, 11), Point(23, 11), Point(23, 40), Point(28, 40), Point(28, 0), Point(22, 0), Point(15, 7), Point(13, 7), Point(6, 0), Point(0, 0)])

        poly['X'] = PointList([Point(25, 0), Point(20, 0), Point(20, 11), Point(14, 17), Point(11, 17), Point(5, 11), Point(5, 0), Point(0, 0), Point(0, 14), Point(7, 21), Point(7, 24), Point(0, 31), Point(0, 40), Point(5, 40), Point(5, 34), Point(11, 28),
                               Point(14, 28), Point(20, 34), Point(20, 40), Point(25, 40), Point(25, 31), Point(18, 24), Point(18, 21), Point(25, 14)])

        poly['Y'] = PointList([Point(5, 40), Point(5, 27), Point(9, 23), Point(16, 23), Point(20, 27), Point(20, 40), Point(25, 40), Point(25, 24), Point(15, 14), Point(15, 0), Point(10, 0), Point(10, 14), Point(0, 24), Point(0, 40)])

        poly['Z'] = PointList([Point(25, 40), Point(25, 29), Point(5, 9), Point(5, 5), Point(25, 5), Point(25, 0), Point(0, 0), Point(0, 12), Point(20, 32), Point(20, 35), Point(0, 35), Point(0, 40)])

        poly[' '] = []

        poly['_'] = PointList([Point(0, 0), Point(25, 0), Point(25, 5), Point(0, 5)])

        poly['-'] = PointList([Point(0, 18), Point(25, 18), Point(25, 23), Point(0, 23)])
        
        return poly

