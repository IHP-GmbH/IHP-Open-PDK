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

__version__ = "$Revision: #3 $"

from cni.dlo import *
from .geometry import *
from .utility_functions import *

import math

def dbCreateRectArray(self, layerId, origin, n, m, x1, off1):
    """
    Creates an n x m array of rectangles.

    Parameters:
    - layerId: The layer on which to create the rectangles.
    - origin: Tuple (x, y) specifying the lower-left corner of the first rectangle.
    - n: Number of rows.
    - m: Number of columns.
    - x1: Size of each rectangle (square: x1 x x1).
    - off1: Offset between rectangles in both X and Y directions.

    Returns:
    - List of created rectangle instances.
    """
    if type(layerId) == str:
        layerId = Layer(layerId)

    x0, y0 = origin  # Lower-left corner of the first rectangle
    rect_list = []

    for i in range(n):  # Loop over rows
        for j in range(m):  # Loop over columns
            x = x0 + j * (x1 + off1)  # Compute X position
            y = y0 + i * (x1 + off1)  # Compute Y position
            rect = dbCreateRect(self, layerId, Box(x, y, x + x1, y + x1))  # Create rectangle
            rect_list.append(rect)

    return rect_list

class esd(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        techparams = specs.tech.getTechParams()

        model = 'diodevdd_2kv'
        
        specs('model', model, 'Model name', ChoiceConstraint(['diodevdd_2kv', 'diodevss_2kv', 'diodevdd_4kv', 'diodevss_4kv', 'nmoscl_2', 'nmoscl_4']) )

    def setupParams(self, params):
        self.model = params['model']
        pass

    def genLayout(self):
        
        self.techparams = self.tech.getTechParams()
        epsilon = self.techparams['epsilon1']

        # layers
        metal1_layer = Layer('Metal1')
        metal1_layer_pin = Layer('Metal1','pin')
        via1_layer = Layer('Via1')
        metal2_layer = Layer('Metal2')
        metal2_layer_pin = Layer('Metal2','pin')
        via2_layer = Layer('Via2')
        metal3_layer = Layer('Metal3')
        metal3_layer_pin = Layer('Metal3','pin')
        activ_layer = Layer('Activ')
        gatpoly_layer = Layer('GatPoly')
        SalBlock_layer = Layer('SalBlock')
        ThickGateOx_layer = Layer('ThickGateOx')
        pSD_layer = Layer('pSD')
        well_layer = Layer('NWell')
        cont_layer = Layer('Cont')
        diodeesd_recog_layer = Layer('Recog', 'esd')
        recog_layer = Layer('Recog')
        textlayer = Layer('TEXT', 'drawing')
        substratelayer = Layer('Substrate', 'drawing')
        nbul_layer = Layer('nBuLay', 'drawing')
        PWell_layer_block = Layer('PWell', 'block')
        # DRC rules
        cont_size = self.techparams['Cnt_a']
        cont_dist = self.techparams['Cnt_b']
        cont_diff_over = self.techparams['Cnt_c']
        pdiffx_over = self.techparams['pSD_c']
        via1_size = self.techparams['Vn_a']
        via1_sep = self.techparams['Vn_b1']
        
        # custom definitions
        cont_sep = 0.2


        if self.model == 'diodevdd_2kv':  
            outer_box = Box(0, 0, 9.72, 37.05)
            dbCreateRect(self, diodeesd_recog_layer, outer_box)  
            
            #label 
            dbCreateLabel(self, textlayer, Point(-0.32, 18.535), 'PAD', 'centerCenter', 'R0', Font.SCRIPT, 0.2)
            dbCreateLabel(self, textlayer, Point(9.15, 18.99), 'VDD', 'centerCenter', 'R0', Font.MATH, 0.2)
            dbCreateLabel(self, textlayer, Point(4.86, 0.675), 'VSS', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(8.33, 0.625), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            #  contact layer
            dbCreateRectArray(self, cont_layer, origin=(0.64,  0.61), n=1, m=24, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.64, 36.28), n=1, m=24, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.58,  1.145), n=97, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(8.98,  1.145), n=97, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(4.44,  4.89),  n=77, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.165,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(6.695,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.055,  2.19),  n=3, m=16, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.055,  34.02),  n=3, m=16, x1=cont_size, off1=cont_sep)
            #  via1 layer
            dbCreateRectArray(self, via1_layer, origin=(1.99,  3.74), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(1.99, 12.74), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(1.99, 21.74), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(1.99, 30.74), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.55,  3.74), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.55, 12.74), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.55, 21.74), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.55, 30.74), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.305,  7.76), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.305, 16.76), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.305, 25.76), n=8, m=3, x1=via1_size, off1=via1_sep)
        
### Extracted Polygons ###
            activ_layer_polygon_list_0 = PointList([Point(4.23000, 4.73000), Point(4.23000, 32.51000), Point(5.49000, 32.51000), Point(5.49000, 4.73000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_0)
            activ_layer_polygon_list_1 = PointList([Point(1.98000, 1.98000), Point(1.98000, 3.24000), Point(6.51000, 3.24000), Point(6.51000, 33.81000), Point(3.24000, 33.81000), Point(3.24000, 3.24000), Point(1.98000, 3.24000), Point(1.98000, 35.07000), Point(7.77000, 35.07000), Point(7.77000, 1.98000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_1)
            activ_layer_polygon_list_2 = PointList([Point(0.42000, 0.45000), Point(0.42000, 0.93000), Point(8.82000, 0.93000), Point(8.82000, 36.12000), Point(0.90000, 36.12000), Point(0.90000, 0.93000), Point(0.42000, 0.93000), Point(0.42000, 36.60000), Point(9.30000, 36.60000), Point(9.30000, 0.45000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_2)

### Extracted Polygons ###
            pSD_layer_polygon_list_0 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(8.40000, 1.35000), Point(8.40000, 35.70000), Point(1.35000, 35.70000), Point(1.35000, 1.35000), Point(0.00000, 1.35000), Point(0.00000, 37.05000), Point(9.72000, 37.05000), Point(9.72000, 0.00000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_0)
            pSD_layer_polygon_list_1 = PointList([Point(3.81000, 4.07000), Point(3.81000, 33.14000), Point(5.91000, 33.14000), Point(5.91000, 4.07000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_1)

### Extracted Polygons ###
            well_layer_polygon_list_0 = PointList([Point(1.56000, 1.56000), Point(1.56000, 35.49000), Point(8.19000, 35.49000), Point(8.19000, 1.56000)])
            dbCreatePolygon(self, well_layer, well_layer_polygon_list_0)

### Extracted Polygons ###
            metal1_layer_polygon_list_0 = PointList([Point(1.83000, 1.89000), Point(1.83000, 3.30000), Point(6.36000, 3.30000), Point(6.36000, 33.75000), Point(3.36000, 33.75000), Point(3.36000, 3.30000), Point(1.83000, 3.30000), Point(1.83000, 35.16000), Point(7.92000, 35.16000), Point(7.92000, 1.89000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_0)
            metal1_layer_polygon_list_1 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(8.40000, 1.35000), Point(8.40000, 35.70000), Point(1.35000, 35.70000), Point(1.35000, 1.35000), Point(0.00000, 1.35000), Point(0.00000, 37.05000), Point(9.72000, 37.05000), Point(9.72000, 0.00000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_1)
            metal1_layer_polygon_list_2 = PointList([Point(3.96000, 4.43000), Point(3.96000, 32.78000), Point(5.76000, 32.78000), Point(5.76000, 4.43000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_2)

### Extracted Polygons ###
            metal1_layer_pin_polygon_list_0 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(9.72000, 1.35000), Point(9.72000, 0.00000)])
            dbCreatePolygon(self, metal1_layer_pin, metal1_layer_pin_polygon_list_0)

### Extracted Polygons ###
            metal2_layer_pin_polygon_list_0 = PointList([Point(-2.12000, 7.75500), Point(-2.12000, 29.31500), Point(1.48000, 29.31500), Point(1.48000, 7.75500)])
            dbCreatePolygon(self, metal2_layer_pin, metal2_layer_pin_polygon_list_0)
            metal2_layer_pin_polygon_list_1 = PointList([Point(7.34000, 3.73500), Point(7.34000, 33.33500), Point(10.94000, 33.33500), Point(10.94000, 3.73500)])
            dbCreatePolygon(self, metal2_layer_pin, metal2_layer_pin_polygon_list_1)

### Extracted Polygons ###
            metal2_layer_polygon_list_0 = PointList([Point(1.94000, 3.73500), Point(1.94000, 6.33500), Point(7.34000, 6.33500), Point(7.34000, 12.73500), Point(1.94000, 12.73500), Point(1.94000, 15.33500), Point(7.34000, 15.33500), Point(7.34000, 21.73500), Point(1.94000, 21.73500), Point(1.94000, 24.33500), Point(7.34000, 24.33500), Point(7.34000, 30.73500), Point(1.94000, 30.73500), Point(1.94000, 33.33500), Point(10.94000, 33.33500), Point(10.94000, 3.73500)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_0)
            metal2_layer_polygon_list_1 = PointList([Point(-2.12000, 7.75500), Point(-2.12000, 29.31500), Point(5.50500, 29.31500), Point(5.50500, 25.75500), Point(1.48000, 25.75500), Point(1.48000, 20.31500), Point(5.50500, 20.31500), Point(5.50500, 16.75500), Point(1.48000, 16.75500), Point(1.48000, 11.31500), Point(5.50500, 11.31500), Point(5.50500, 7.75500)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_1)
        

        if self.model == 'diodevss_2kv':
            outer_box = Box(0, 0, 9.72, 37.05)
            dbCreateRect(self, diodeesd_recog_layer, outer_box)  
            
            # labels
            dbCreateLabel(self, textlayer, Point(-0.2, 18.535), 'PAD', 'centerCenter', 'R0', Font.SCRIPT, 0.2)
            dbCreateLabel(self, textlayer, Point(9.15, 18.99), 'VSS', 'centerCenter', 'R0', Font.MATH, 0.2)
            dbCreateLabel(self, textlayer, Point(4.86, 36.375), 'VDD', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(2.285, 2.385), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            #  contact layer
            dbCreateRectArray(self, cont_layer, origin=(0.64,  0.61), n=1, m=24, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.64, 36.28), n=1, m=24, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.58,  1.145), n=97, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(8.98,  1.145), n=97, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(4.44,  4.89),  n=77, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.165,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(6.695,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.055,  2.19),  n=3, m=16, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.055,  34.02),  n=3, m=16, x1=cont_size, off1=cont_sep)
            #  via1 layer
            dbCreateRectArray(self, via1_layer, origin=(2.03,  3.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.03, 12.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.03, 21.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.03, 30.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.59,  3.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.59, 12.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.59, 21.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.59, 30.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285,  7.745), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 16.745), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 25.745), n=8, m=3, x1=via1_size, off1=via1_sep)

### Extracted Polygons ###
            activ_layer_polygon_list_0 = PointList([Point(4.23000, 4.73000), Point(4.23000, 32.51000), Point(5.49000, 32.51000), Point(5.49000, 4.73000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_0)
            activ_layer_polygon_list_1 = PointList([Point(1.98000, 1.98000), Point(1.98000, 3.24000), Point(6.51000, 3.24000), Point(6.51000, 33.81000), Point(3.24000, 33.81000), Point(3.24000, 3.24000), Point(1.98000, 3.24000), Point(1.98000, 35.07000), Point(7.77000, 35.07000), Point(7.77000, 1.98000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_1)
            activ_layer_polygon_list_2 = PointList([Point(0.42000, 0.45000), Point(0.42000, 0.93000), Point(8.82000, 0.93000), Point(8.82000, 36.12000), Point(0.90000, 36.12000), Point(0.90000, 0.93000), Point(0.42000, 0.93000), Point(0.42000, 36.60000), Point(9.30000, 36.60000), Point(9.30000, 0.45000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_2)

### Extracted Polygons ###
            pSD_layer_polygon_list_0 = PointList([Point(1.56000, 1.56000), Point(1.56000, 3.66000), Point(6.09000, 3.66000), Point(6.09000, 33.39000), Point(3.66000, 33.39000), Point(3.66000, 3.66000), Point(1.56000, 3.66000), Point(1.56000, 35.49000), Point(8.19000, 35.49000), Point(8.19000, 1.56000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_0)

### Extracted Polygons ###
            well_layer_polygon_list_0 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(8.40000, 1.35000), Point(8.40000, 35.70000), Point(1.35000, 35.70000), Point(1.35000, 1.35000), Point(0.00000, 1.35000), Point(0.00000, 37.05000), Point(9.72000, 37.05000), Point(9.72000, 0.00000)])
            dbCreatePolygon(self, well_layer, well_layer_polygon_list_0)

### Extracted Polygons ###
            metal2_layer_pin_polygon_list_0 = PointList([Point(-2.08000, 7.74500), Point(-2.08000, 29.30500), Point(1.52000, 29.30500), Point(1.52000, 7.74500)])
            dbCreatePolygon(self, metal2_layer_pin, metal2_layer_pin_polygon_list_0)
            metal2_layer_pin_polygon_list_1 = PointList([Point(7.38000, 3.72500), Point(7.38000, 33.32500), Point(10.98000, 33.32500), Point(10.98000, 3.72500)])
            dbCreatePolygon(self, metal2_layer_pin, metal2_layer_pin_polygon_list_1)

### Extracted Polygons ###
            metal1_layer_pin_polygon_list_0 = PointList([Point(0.00000, 35.70000), Point(0.00000, 37.05000), Point(9.72000, 37.05000), Point(9.72000, 35.70000)])
            dbCreatePolygon(self, metal1_layer_pin, metal1_layer_pin_polygon_list_0)

### Extracted Polygons ###
            metal1_layer_polygon_list_0 = PointList([Point(1.83000, 1.89000), Point(1.83000, 3.30000), Point(6.36000, 3.30000), Point(6.36000, 33.75000), Point(3.36000, 33.75000), Point(3.36000, 3.30000), Point(1.83000, 3.30000), Point(1.83000, 35.16000), Point(7.92000, 35.16000), Point(7.92000, 1.89000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_0)
            metal1_layer_polygon_list_1 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(8.40000, 1.35000), Point(8.40000, 35.70000), Point(1.35000, 35.70000), Point(1.35000, 1.35000), Point(0.00000, 1.35000), Point(0.00000, 37.05000), Point(9.72000, 37.05000), Point(9.72000, 0.00000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_1)
            metal1_layer_polygon_list_2 = PointList([Point(4.11000, 4.43000), Point(4.11000, 32.78000), Point(5.64000, 32.78000), Point(5.64000, 4.43000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_2)

### Extracted Polygons ###
            metal2_layer_polygon_list_0 = PointList([Point(4.23500, 7.74000), Point(4.23500, 7.74500), Point(-2.08000, 7.74500), Point(-2.08000, 29.30500), Point(5.30000, 29.30500), Point(5.30000, 29.30000), Point(5.48500, 29.30000), Point(5.48500, 25.74000), Point(4.23500, 25.74000), Point(4.23500, 25.74500), Point(1.52000, 25.74500), Point(1.52000, 20.30500), Point(5.30000, 20.30500), Point(5.30000, 20.30000), Point(5.48500, 20.30000), Point(5.48500, 16.74000), Point(4.23500, 16.74000), Point(4.23500, 16.74500), Point(1.52000, 16.74500), Point(1.52000, 11.30500), Point(5.30000, 11.30500), Point(5.30000, 11.30000), Point(5.48500, 11.30000), Point(5.48500, 7.74000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_0)
            metal2_layer_polygon_list_1 = PointList([Point(1.98000, 3.72500), Point(1.98000, 6.32500), Point(7.38000, 6.32500), Point(7.38000, 12.72500), Point(1.98000, 12.72500), Point(1.98000, 15.32500), Point(7.38000, 15.32500), Point(7.38000, 21.72500), Point(1.98000, 21.72500), Point(1.98000, 24.32500), Point(7.38000, 24.32500), Point(7.38000, 30.72500), Point(1.98000, 30.72500), Point(1.98000, 33.32500), Point(10.98000, 33.32500), Point(10.98000, 3.72500)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_1)
        

        if self.model == 'diodevss_4kv':
            outer_box = Box(0, 0, 14.32, 37.05)
            dbCreateRect(self, diodeesd_recog_layer, outer_box)  
            
            # labels
            dbCreateLabel(self, textlayer, Point(-0.51, 18.442), 'PAD', 'centerCenter', 'R0', Font.SCRIPT, 0.2)
            dbCreateLabel(self, textlayer, Point(13.64, 18.525), 'VSS', 'centerCenter', 'R0', Font.MATH, 0.2)
            dbCreateLabel(self, textlayer, Point(7.16, 36.375), 'VDD', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(3.445, 2.495), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            # contact 
            dbCreateRectArray(self, cont_layer, origin=(0.62,  0.61), n=1, m=37, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.62, 36.28), n=1, m=37, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.58,  1.105), n=97, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(13.54,  1.105), n=97, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(4.44,  4.81),  n=77, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(8.97,  4.81),  n=77, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.165,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(6.725,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(11.285,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.235,  2.19),  n=3, m=28, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.235,  34.02),  n=3, m=28, x1=cont_size, off1=cont_sep)
            #  via1 layer
            dbCreateRectArray(self, via1_layer, origin=(2.01,  3.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 12.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 21.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 30.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(6.57,  3.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 12.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 21.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 30.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(11.13,  3.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 12.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 21.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 30.73), n=6, m=3, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(4.285,  7.665), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 16.665), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 25.665), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815,  7.665), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815, 16.665), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815, 25.665), n=8, m=3, x1=via1_size, off1=via1_sep)
### Extracted Polygons ###
### Extracted Polygons ###
            activ_layer_polygon_list_0 = PointList([Point(4.23000, 4.65000), Point(4.23000, 32.43000), Point(5.49000, 32.43000), Point(5.49000, 4.65000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_0)
            activ_layer_polygon_list_1 = PointList([Point(1.98000, 1.98000), Point(1.98000, 3.24000), Point(11.05000, 3.24000), Point(11.05000, 33.81000), Point(7.77000, 33.81000), Point(7.77000, 3.24000), Point(6.51000, 3.24000), Point(6.51000, 33.81000), Point(3.24000, 33.81000), Point(3.24000, 3.24000), Point(1.98000, 3.24000), Point(1.98000, 35.07000), Point(12.31000, 35.07000), Point(12.31000, 1.98000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_1)
            activ_layer_polygon_list_2 = PointList([Point(0.42000, 0.45000), Point(0.42000, 0.93000), Point(13.42000, 0.93000), Point(13.42000, 36.12000), Point(0.90000, 36.12000), Point(0.90000, 0.93000), Point(0.42000, 0.93000), Point(0.42000, 36.60000), Point(13.90000, 36.60000), Point(13.90000, 0.45000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_2)
            activ_layer_polygon_list_3 = PointList([Point(8.76000, 4.65000), Point(8.76000, 32.43000), Point(10.02000, 32.43000), Point(10.02000, 4.65000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_3)

### Extracted Polygons ###
            well_layer_polygon_list_0 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(13.00000, 1.35000), Point(13.00000, 35.70000), Point(1.35000, 35.70000), Point(1.35000, 1.35000), Point(0.00000, 1.35000), Point(0.00000, 37.05000), Point(14.32000, 37.05000), Point(14.32000, 0.00000)])
            dbCreatePolygon(self, well_layer, well_layer_polygon_list_0)

### Extracted Polygons ###
            pSD_layer_polygon_list_0 = PointList([Point(1.56000, 1.56000), Point(1.56000, 3.66000), Point(10.63000, 3.66000), Point(10.63000, 33.39000), Point(8.19000, 33.39000), Point(8.19000, 3.66000), Point(6.09000, 3.66000), Point(6.09000, 33.39000), Point(3.66000, 33.39000), Point(3.66000, 3.66000), Point(1.56000, 3.66000), Point(1.56000, 35.49000), Point(12.73000, 35.49000), Point(12.73000, 1.56000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_0)

### Extracted Polygons ###
            metal1_layer_polygon_list_0 = PointList([Point(4.11000, 4.35000), Point(4.11000, 32.70000), Point(5.64000, 32.70000), Point(5.64000, 4.35000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_0)
            metal1_layer_polygon_list_1 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(13.00000, 1.35000), Point(13.00000, 35.70000), Point(1.35000, 35.70000), Point(1.35000, 1.35000), Point(0.00000, 1.35000), Point(0.00000, 37.05000), Point(14.32000, 37.05000), Point(14.32000, 0.00000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_1)
            metal1_layer_polygon_list_2 = PointList([Point(8.64000, 4.35000), Point(8.64000, 32.70000), Point(10.17000, 32.70000), Point(10.17000, 4.35000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_2)
            metal1_layer_polygon_list_3 = PointList([Point(1.83000, 1.89000), Point(1.83000, 3.30000), Point(10.90000, 3.30000), Point(10.90000, 33.75000), Point(7.92000, 33.75000), Point(7.92000, 3.30000), Point(6.36000, 3.30000), Point(6.36000, 33.75000), Point(3.36000, 33.75000), Point(3.36000, 3.30000), Point(1.83000, 3.30000), Point(1.83000, 35.16000), Point(12.46000, 35.16000), Point(12.46000, 1.89000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_3)

### Extracted Polygons ###
            metal2_layer_polygon_list_0 = PointList([Point(2.46000, 3.72000), Point(2.46000, 3.72500), Point(1.96000, 3.72500), Point(1.96000, 6.32500), Point(2.46000, 6.32500), Point(2.46000, 6.33000), Point(11.82000, 6.33000), Point(11.82000, 12.72000), Point(2.46000, 12.72000), Point(2.46000, 12.72500), Point(1.96000, 12.72500), Point(1.96000, 15.32500), Point(2.46000, 15.32500), Point(2.46000, 15.33000), Point(11.82000, 15.33000), Point(11.82000, 21.72000), Point(2.46000, 21.72000), Point(2.46000, 21.72500), Point(1.96000, 21.72500), Point(1.96000, 24.32500), Point(2.46000, 24.32500), Point(2.46000, 24.33000), Point(11.82000, 24.33000), Point(11.82000, 30.72000), Point(2.46000, 30.72000), Point(2.46000, 30.72500), Point(1.96000, 30.72500), Point(1.96000, 33.32500), Point(2.46000, 33.32500), Point(2.46000, 33.33000), Point(15.46000, 33.33000), Point(15.46000, 3.72000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_0)
            metal2_layer_polygon_list_1 = PointList([Point(-2.31000, 7.66000), Point(-2.31000, 29.22000), Point(10.01500, 29.22000), Point(10.01500, 25.66000), Point(1.29500, 25.66000), Point(1.29500, 20.22000), Point(10.01500, 20.22000), Point(10.01500, 16.66000), Point(1.29500, 16.66000), Point(1.29500, 11.22000), Point(10.01500, 11.22000), Point(10.01500, 7.66000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_1)

### Extracted Polygons ###
            metal1_layer_pin_polygon_list_0 = PointList([Point(0.00000, 35.70000), Point(0.00000, 37.05000), Point(14.32000, 37.05000), Point(14.32000, 35.70000)])
            dbCreatePolygon(self, metal1_layer_pin, metal1_layer_pin_polygon_list_0)

### Extracted Polygons ###
            metal2_layer_pin_polygon_list_0 = PointList([Point(-2.31000, 7.66000), Point(-2.31000, 29.22000), Point(1.29500, 29.22000), Point(1.29500, 7.66000)])
            dbCreatePolygon(self, metal2_layer_pin, metal2_layer_pin_polygon_list_0)
            metal2_layer_pin_polygon_list_1 = PointList([Point(11.82000, 3.72000), Point(11.82000, 33.33000), Point(15.46000, 33.33000), Point(15.46000, 3.72000)])
            dbCreatePolygon(self, metal2_layer_pin, metal2_layer_pin_polygon_list_1)
        
        if self.model == 'diodevdd_4kv':
            outer_box = Box(0, 0, 14.32, 37.05)
            dbCreateRect(self, diodeesd_recog_layer, outer_box)  
            
            # labels
            dbCreateLabel(self, textlayer, Point(-0.51, 18.442), 'PAD', 'centerCenter', 'R0', Font.SCRIPT, 0.2)
            dbCreateLabel(self, textlayer, Point(13.64, 18.525), 'VDD', 'centerCenter', 'R0', Font.MATH, 0.2)
            dbCreateLabel(self, textlayer, Point(7.16, 36.375), 'VSS', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(3.445, 0.495), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            # contact 
            dbCreateRectArray(self, cont_layer, origin=(0.62,  0.61), n=1, m=37, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.62, 36.28), n=1, m=37, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.58,  1.105), n=97, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(13.54,  1.105), n=97, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(4.44,  4.81),  n=77, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(8.97,  4.81),  n=77, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.165,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(6.725,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(11.285,  3.405),  n=85, m=3, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.235,  2.19),  n=3, m=28, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(2.235,  34.02),  n=3, m=28, x1=cont_size, off1=cont_sep)
            #  via1 layer
            dbCreateRectArray(self, via1_layer, origin=(2.005,  3.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.005, 12.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.005, 21.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.005, 30.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(6.565,  3.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.565, 12.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.565, 21.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.565, 30.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(11.125,  3.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.125, 12.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.125, 21.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.125, 30.72), n=6, m=3, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(4.305,  7.68), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.305, 16.68), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.305, 25.68), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.835,  7.68), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.835, 16.68), n=8, m=3, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.835, 25.68), n=8, m=3, x1=via1_size, off1=via1_sep)

### Extracted Polygons ###
            activ_layer_polygon_list_0 = PointList([Point(4.23000, 4.65000), Point(4.23000, 32.43000), Point(5.49000, 32.43000), Point(5.49000, 4.65000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_0)
            activ_layer_polygon_list_1 = PointList([Point(1.98000, 1.98000), Point(1.98000, 3.24000), Point(11.05000, 3.24000), Point(11.05000, 33.81000), Point(7.77000, 33.81000), Point(7.77000, 3.24000), Point(6.51000, 3.24000), Point(6.51000, 33.81000), Point(3.24000, 33.81000), Point(3.24000, 3.24000), Point(1.98000, 3.24000), Point(1.98000, 35.07000), Point(12.31000, 35.07000), Point(12.31000, 1.98000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_1)
            activ_layer_polygon_list_2 = PointList([Point(0.42000, 0.45000), Point(0.42000, 0.93000), Point(13.42000, 0.93000), Point(13.42000, 36.12000), Point(0.90000, 36.12000), Point(0.90000, 0.93000), Point(0.42000, 0.93000), Point(0.42000, 36.60000), Point(13.90000, 36.60000), Point(13.90000, 0.45000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_2)
            activ_layer_polygon_list_3 = PointList([Point(8.76000, 4.65000), Point(8.76000, 32.43000), Point(10.02000, 32.43000), Point(10.02000, 4.65000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_3)

### Extracted Polygons ###
            well_layer_polygon_list_0 = PointList([Point(1.56000, 1.56000), Point(1.56000, 35.49000), Point(12.79000, 35.49000), Point(12.79000, 1.56000)])
            dbCreatePolygon(self, well_layer, well_layer_polygon_list_0)
### Extracted Polygons ###
            pSD_layer_polygon_list_0 = PointList([Point(3.81000, 3.99000), Point(3.81000, 33.06000), Point(5.91000, 33.06000), Point(5.91000, 3.99000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_0)
            pSD_layer_polygon_list_1 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(13.00000, 1.35000), Point(13.00000, 35.70000), Point(1.35000, 35.70000), Point(1.35000, 1.35000), Point(0.00000, 1.35000), Point(0.00000, 37.05000), Point(14.32000, 37.05000), Point(14.32000, 0.00000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_1)
            pSD_layer_polygon_list_2 = PointList([Point(8.34000, 3.99000), Point(8.34000, 33.06000), Point(10.44000, 33.06000), Point(10.44000, 3.99000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_2)

### Extracted Polygons ###
            metal1_layer_polygon_list_0 = PointList([Point(3.96000, 4.35000), Point(3.96000, 32.70000), Point(5.76000, 32.70000), Point(5.76000, 4.35000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_0)
            metal1_layer_polygon_list_1 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(13.00000, 1.35000), Point(13.00000, 35.70000), Point(1.35000, 35.70000), Point(1.35000, 1.35000), Point(0.00000, 1.35000), Point(0.00000, 37.05000), Point(14.32000, 37.05000), Point(14.32000, 0.00000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_1)
            metal1_layer_polygon_list_2 = PointList([Point(8.49000, 4.35000), Point(8.49000, 32.70000), Point(10.29000, 32.70000), Point(10.29000, 4.35000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_2)
            metal1_layer_polygon_list_3 = PointList([Point(1.83000, 1.89000), Point(1.83000, 3.30000), Point(10.90000, 3.30000), Point(10.90000, 33.75000), Point(7.92000, 33.75000), Point(7.92000, 3.30000), Point(6.36000, 3.30000), Point(6.36000, 33.75000), Point(3.36000, 33.75000), Point(3.36000, 3.30000), Point(1.83000, 3.30000), Point(1.83000, 35.16000), Point(12.46000, 35.16000), Point(12.46000, 1.89000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_3)

### Extracted Polygons ###
            metal1_layer_pin_polygon_list_0 = PointList([Point(0.00000, 0.00000), Point(0.00000, 1.35000), Point(14.32000, 1.35000), Point(14.32000, 0.00000)])
            dbCreatePolygon(self, metal1_layer_pin, metal1_layer_pin_polygon_list_0)

### Extracted Polygons ###
            metal2_layer_polygon_list_0 = PointList([Point(4.25500, 7.67500), Point(4.25500, 7.73500), Point(-2.30000, 7.73500), Point(-2.30000, 29.29500), Point(9.54000, 29.29500), Point(9.54000, 29.23500), Point(10.03500, 29.23500), Point(10.03500, 25.67500), Point(8.78500, 25.67500), Point(8.78500, 25.73500), Point(5.50500, 25.73500), Point(5.50500, 25.67500), Point(4.25500, 25.67500), Point(4.25500, 25.73500), Point(1.30500, 25.73500), Point(1.30500, 20.29500), Point(9.54000, 20.29500), Point(9.54000, 20.23500), Point(10.03500, 20.23500), Point(10.03500, 16.67500), Point(8.78500, 16.67500), Point(8.78500, 16.73500), Point(5.50500, 16.73500), Point(5.50500, 16.67500), Point(4.25500, 16.67500), Point(4.25500, 16.73500), Point(1.30500, 16.73500), Point(1.30500, 11.29500), Point(9.54000, 11.29500), Point(9.54000, 11.23500), Point(10.03500, 11.23500), Point(10.03500, 7.67500), Point(8.78500, 7.67500), Point(8.78500, 7.73500), Point(5.50500, 7.73500), Point(5.50500, 7.67500)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_0)
            metal2_layer_polygon_list_1 = PointList([Point(1.95500, 3.71500), Point(1.95500, 6.31500), Point(11.86000, 6.31500), Point(11.86000, 12.71500), Point(1.95500, 12.71500), Point(1.95500, 15.31500), Point(11.86000, 15.31500), Point(11.86000, 21.71500), Point(1.95500, 21.71500), Point(1.95500, 24.31500), Point(11.86000, 24.31500), Point(11.86000, 30.71500), Point(1.95500, 30.71500), Point(1.95500, 33.31500), Point(15.50500, 33.31500), Point(15.50500, 3.71500)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_1)
### Extracted Polygons ###
            metal2_layer_pin_polygon_list_0 = PointList([Point(11.86000, 3.71500), Point(11.86000, 33.31500), Point(15.50500, 33.31500), Point(15.50500, 3.71500)])
            dbCreatePolygon(self, metal2_layer_pin, metal2_layer_pin_polygon_list_0)
            metal2_layer_pin_polygon_list_1 = PointList([Point(-2.30000, 7.73500), Point(-2.30000, 29.29500), Point(1.30500, 29.29500), Point(1.30500, 7.73500)])
            dbCreatePolygon(self, metal2_layer_pin, metal2_layer_pin_polygon_list_1)

        if self.model == 'nmoscl_2':
            outer_box = Box(-2.25, -1.95, 34.96, 19.62)
            dbCreateRect(self, diodeesd_recog_layer, outer_box)  
            dbCreateRect(self, recog_layer, outer_box)  
            # labels
            dbCreateLabel(self, textlayer, Point(1.811, -1.245), 'VSS', 'centerCenter', 'R0', Font.MATH, 0.2)
            dbCreateLabel(self, textlayer, Point(1.592, 19.26), 'VDD', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(1.45, 17.01), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(20.45, 10.01), 'nmoscl_2', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, substratelayer, Point(1.45, 17.01), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            # contact
            dbCreateRectArray(self, cont_layer, origin=(-0.71,  -1.315), n=1, m=91, x1=cont_size, off1=0.22)
            dbCreateRectArray(self, cont_layer, origin=(0.47,  16.945), n=1, m=89, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(-0.71,  18.785), n=1, m=91, x1=cont_size, off1=0.22)
            dbCreateRectArray(self, cont_layer, origin=(-1.59,  -1.35), n=57, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(34.17,  -1.35), n=57, m=1, x1=cont_size, off1=cont_sep)
            # Via1 
            dbCreateRectArray(self, via1_layer, origin=(-1.175,  -1.325), n=1, m=73, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(-1.175,  18.775), n=1, m=73, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(-1.605,  -1.045), n=42, m=1, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(34.155,  -1.045), n=42, m=1, x1=via1_size, off1=via1_sep)
            
            for i in range(1, 14):
                dbCreateRectArray(self, cont_layer, origin=(0.065+(i-1)*2.66,  1.28), n=39, m=1, x1=cont_size, off1=cont_sep)
                dbCreateRectArray(self, cont_layer, origin=(0.425+(i-1)*2.66,  1.28), n=39, m=1, x1=cont_size, off1=cont_sep)
                dbCreateRectArray(self, via1_layer, origin=(-0.02+(i-1)*2.66,  1.125), n=30, m=2, x1=via1_size, off1=via1_sep)
                dbCreateRectArray(self, via2_layer, origin=(-0.02+(i-1)*2.66,  1.125), n=30, m=2, x1=via1_size, off1=via1_sep)
            
            dbCreateRect(self, cont_layer, Box(1.47000, 0.11500, 1.63000, 0.27500))
            dbCreateRect(self, cont_layer, Box(1.13000, 0.11500, 1.29000, 0.27500))
            dbCreateRect(self, cont_layer, Box(6.45000, 0.11500, 6.61000, 0.27500))
            dbCreateRect(self, cont_layer, Box(6.79000, 0.11500, 6.95000, 0.27500))
            dbCreateRect(self, cont_layer, Box(4.68000, 0.11500, 4.84000, 0.27500))
            dbCreateRect(self, cont_layer, Box(4.34000, 0.11500, 4.50000, 0.27500))
            dbCreateRect(self, cont_layer, Box(12.11000, 0.11500, 12.27000, 0.27500))
            dbCreateRect(self, cont_layer, Box(11.77000, 0.11500, 11.93000, 0.27500))
            dbCreateRect(self, cont_layer, Box(15.32000, 0.11500, 15.48000, 0.27500))
            dbCreateRect(self, cont_layer, Box(14.98000, 0.11500, 15.14000, 0.27500))
            dbCreateRect(self, cont_layer, Box(10.00000, 0.11500, 10.16000, 0.27500))
            dbCreateRect(self, cont_layer, Box(9.66000, 0.11500, 9.82000, 0.27500))
            dbCreateRect(self, cont_layer, Box(20.64000, 0.11500, 20.80000, 0.27500))
            dbCreateRect(self, cont_layer, Box(20.30000, 0.11500, 20.46000, 0.27500))
            dbCreateRect(self, cont_layer, Box(22.75000, 0.11500, 22.91000, 0.27500))
            dbCreateRect(self, cont_layer, Box(22.41000, 0.11500, 22.57000, 0.27500))
            dbCreateRect(self, cont_layer, Box(17.43000, 0.11500, 17.59000, 0.27500))
            dbCreateRect(self, cont_layer, Box(17.09000, 0.11500, 17.25000, 0.27500))
            dbCreateRect(self, cont_layer, Box(28.07000, 0.11500, 28.23000, 0.27500))
            dbCreateRect(self, cont_layer, Box(27.73000, 0.11500, 27.89000, 0.27500))
            dbCreateRect(self, cont_layer, Box(31.28000, 0.11500, 31.44000, 0.27500))
            dbCreateRect(self, cont_layer, Box(30.94000, 0.11500, 31.10000, 0.27500))
            dbCreateRect(self, cont_layer, Box(25.96000, 0.11500, 26.12000, 0.27500))
            dbCreateRect(self, cont_layer, Box(25.62000, 0.11500, 25.78000, 0.27500))

### Extracted Polygons ###
            activ_layer_polygon_list_0 = PointList([Point(-1.83000, -1.53000), Point(-1.83000, -0.90000), Point(33.91000, -0.90000), Point(33.91000, 18.57000), Point(-1.20000, 18.57000), Point(-1.20000, -0.90000), Point(-1.83000, -0.90000), Point(-1.83000, 19.20000), Point(34.54000, 19.20000), Point(34.54000, -1.53000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_0)
            activ_layer_polygon_list_1 = PointList([Point(0.00000, 1.20000), Point(0.00000, 1.21000), Point(-0.00500, 1.21000), Point(-0.00500, 15.19000), Point(0.00000, 15.19000), Point(0.00000, 15.21000), Point(32.57000, 15.21000), Point(32.57000, 15.19000), Point(32.57500, 15.19000), Point(32.57500, 1.21000), Point(32.57000, 1.21000), Point(32.57000, 1.20000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_1)
            activ_layer_polygon_list_2 = PointList([Point(0.00000, 16.71000), Point(0.00000, 17.34000), Point(32.71000, 17.34000), Point(32.71000, 16.71000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_2)

### Extracted Polygons ###
            pSD_layer_polygon_list_0 = PointList([Point(-0.33000, 16.35000), Point(-0.33000, 17.67000), Point(33.04000, 17.67000), Point(33.04000, 16.35000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_0)

### Extracted Polygons ###
            gatpoly_layer_polygon_list_0 = PointList([Point(0.96000, -0.12000), Point(0.96000, 0.59000), Point(1.20000, 0.59000), Point(1.20000, 15.84000), Point(1.56000, 15.84000), Point(1.56000, 0.59000), Point(4.41000, 0.59000), Point(4.41000, 15.84000), Point(4.77000, 15.84000), Point(4.77000, 0.59000), Point(6.52000, 0.59000), Point(6.52000, 15.84000), Point(6.88000, 15.84000), Point(6.88000, 0.59000), Point(9.73000, 0.59000), Point(9.73000, 15.84000), Point(10.09000, 15.84000), Point(10.09000, 0.59000), Point(11.84000, 0.59000), Point(11.84000, 15.84000), Point(12.20000, 15.84000), Point(12.20000, 0.59000), Point(15.05000, 0.59000), Point(15.05000, 15.84000), Point(15.41000, 15.84000), Point(15.41000, 0.59000), Point(17.16000, 0.59000), Point(17.16000, 15.84000), Point(17.52000, 15.84000), Point(17.52000, 0.59000), Point(20.37000, 0.59000), Point(20.37000, 15.84000), Point(20.73000, 15.84000), Point(20.73000, 0.59000), Point(22.48000, 0.59000), Point(22.48000, 15.84000), Point(22.84000, 15.84000), Point(22.84000, 0.59000), Point(25.69000, 0.59000), Point(25.69000, 15.84000), Point(26.05000, 15.84000), Point(26.05000, 0.59000), Point(27.80000, 0.59000), Point(27.80000, 15.84000), Point(28.16000, 15.84000), Point(28.16000, 0.59000), Point(31.01000, 0.59000), Point(31.01000, 15.84000), Point(31.37000, 15.84000), Point(31.37000, 0.59000), Point(32.14000, 0.59000), Point(32.14000, -0.12000)])
            dbCreatePolygon(self, gatpoly_layer, gatpoly_layer_polygon_list_0)

### Extracted Polygons ###
            ThickGateOx_layer_polygon_list_0 = PointList([Point(-0.51500, 0.86000), Point(-0.51500, 15.84500), Point(33.09500, 15.84500), Point(33.09500, 0.86000)])
            dbCreatePolygon(self, ThickGateOx_layer, ThickGateOx_layer_polygon_list_0)

### Extracted Polygons ###
            metal1_layer_polygon_list_0 = PointList([Point(23.74000, 0.81000), Point(23.74000, 15.21000), Point(23.87000, 15.21000), Point(23.87000, 15.24500), Point(24.64000, 15.24500), Point(24.64000, 15.21000), Point(24.79000, 15.21000), Point(24.79000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_0)
            metal1_layer_polygon_list_1 = PointList([Point(29.06000, 0.81000), Point(29.06000, 15.21000), Point(29.19000, 15.21000), Point(29.19000, 15.24500), Point(29.96000, 15.24500), Point(29.96000, 15.21000), Point(30.11000, 15.21000), Point(30.11000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_1)
            metal1_layer_polygon_list_2 = PointList([Point(18.42000, 0.81000), Point(18.42000, 15.21000), Point(18.55000, 15.21000), Point(18.55000, 15.24500), Point(19.32000, 15.24500), Point(19.32000, 15.21000), Point(19.47000, 15.21000), Point(19.47000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_2)
            metal1_layer_polygon_list_3 = PointList([Point(-2.25000, -1.95000), Point(-2.25000, -0.54000), Point(33.58000, -0.54000), Point(33.58000, 17.88000), Point(-0.87000, 17.88000), Point(-0.87000, -0.54000), Point(-2.25000, -0.54000), Point(-2.25000, 19.29000), Point(34.96000, 19.29000), Point(34.96000, -1.95000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_3)
            metal1_layer_polygon_list_4 = PointList([Point(2.46000, 0.81000), Point(2.46000, 15.21000), Point(2.59000, 15.21000), Point(2.59000, 15.24500), Point(3.36000, 15.24500), Point(3.36000, 15.21000), Point(3.51000, 15.21000), Point(3.51000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_4)
            metal1_layer_polygon_list_5 = PointList([Point(13.10000, 0.81000), Point(13.10000, 15.21000), Point(13.23000, 15.21000), Point(13.23000, 15.24500), Point(14.00000, 15.24500), Point(14.00000, 15.21000), Point(14.15000, 15.21000), Point(14.15000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_5)
            metal1_layer_polygon_list_6 = PointList([Point(-0.21000, -0.12000), Point(-0.21000, 0.51000), Point(31.73000, 0.51000), Point(31.73000, 16.71000), Point(27.46000, 16.71000), Point(27.46000, 0.51000), Point(26.39000, 0.51000), Point(26.39000, 16.71000), Point(22.14000, 16.71000), Point(22.14000, 0.51000), Point(21.07000, 0.51000), Point(21.07000, 16.71000), Point(16.82000, 16.71000), Point(16.82000, 0.51000), Point(15.75000, 0.51000), Point(15.75000, 16.71000), Point(11.50000, 16.71000), Point(11.50000, 0.51000), Point(10.43000, 0.51000), Point(10.43000, 16.71000), Point(6.18000, 16.71000), Point(6.18000, 0.51000), Point(5.11000, 0.51000), Point(5.11000, 16.71000), Point(0.84000, 16.71000), Point(0.84000, 0.51000), Point(-0.21000, 0.51000), Point(-0.21000, 17.40000), Point(32.77000, 17.40000), Point(32.77000, 17.37000), Point(32.78000, 17.37000), Point(32.78000, -0.12000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_6)
            metal1_layer_polygon_list_7 = PointList([Point(7.78000, 0.81000), Point(7.78000, 15.21000), Point(7.91000, 15.21000), Point(7.91000, 15.24500), Point(8.68000, 15.24500), Point(8.68000, 15.21000), Point(8.83000, 15.21000), Point(8.83000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_7)

### Extracted Polygons ###
            metal2_layer_polygon_list_0 = PointList([Point(26.41000, 0.84000), Point(26.41000, 15.21000), Point(26.53000, 15.21000), Point(26.53000, 15.24000), Point(27.30000, 15.24000), Point(27.30000, 15.21000), Point(27.44000, 15.21000), Point(27.44000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_0)
            metal2_layer_polygon_list_1 = PointList([Point(-0.12000, 0.84000), Point(-0.12000, 15.21000), Point(-0.07000, 15.21000), Point(-0.07000, 15.24000), Point(0.70000, 15.24000), Point(0.70000, 15.21000), Point(0.84000, 15.21000), Point(0.84000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_1)
            metal2_layer_polygon_list_2 = PointList([Point(10.45000, 0.84000), Point(10.45000, 15.21000), Point(10.57000, 15.21000), Point(10.57000, 15.24000), Point(11.34000, 15.24000), Point(11.34000, 15.21000), Point(11.48000, 15.21000), Point(11.48000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_2)
            metal2_layer_polygon_list_3 = PointList([Point(31.73000, 0.84000), Point(31.73000, 15.21000), Point(31.85000, 15.21000), Point(31.85000, 15.24000), Point(32.62000, 15.24000), Point(32.62000, 15.21000), Point(32.69000, 15.21000), Point(32.69000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_3)
            metal2_layer_polygon_list_4 = PointList([Point(15.77000, 0.84000), Point(15.77000, 15.21000), Point(15.89000, 15.21000), Point(15.89000, 15.24000), Point(16.66000, 15.24000), Point(16.66000, 15.21000), Point(16.80000, 15.21000), Point(16.80000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_4)
            metal2_layer_polygon_list_5 = PointList([Point(5.13000, 0.84000), Point(5.13000, 15.21000), Point(5.25000, 15.21000), Point(5.25000, 15.24000), Point(6.02000, 15.24000), Point(6.02000, 15.21000), Point(6.16000, 15.21000), Point(6.16000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_5)
            metal2_layer_polygon_list_6 = PointList([Point(21.09000, 0.84000), Point(21.09000, 15.21000), Point(21.21000, 15.21000), Point(21.21000, 15.24000), Point(21.98000, 15.24000), Point(21.98000, 15.21000), Point(22.12000, 15.21000), Point(22.12000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_6)
            metal2_layer_polygon_list_7 = PointList([Point(-2.25000, -1.95000), Point(-2.25000, -0.54000), Point(33.58000, -0.54000), Point(33.58000, 17.88000), Point(30.11000, 17.88000), Point(30.11000, -0.54000), Point(29.06000, -0.54000), Point(29.06000, 17.88000), Point(24.79000, 17.88000), Point(24.79000, -0.54000), Point(23.74000, -0.54000), Point(23.74000, 17.88000), Point(19.47000, 17.88000), Point(19.47000, -0.54000), Point(18.42000, -0.54000), Point(18.42000, 17.88000), Point(14.15000, 17.88000), Point(14.15000, -0.54000), Point(13.10000, -0.54000), Point(13.10000, 17.88000), Point(8.83000, 17.88000), Point(8.83000, -0.54000), Point(7.78000, -0.54000), Point(7.78000, 17.88000), Point(3.51000, 17.88000), Point(3.51000, -0.54000), Point(2.46000, -0.54000), Point(2.46000, 17.88000), Point(-0.87000, 17.88000), Point(-0.87000, -0.54000), Point(-2.25000, -0.54000), Point(-2.25000, 19.29000), Point(34.96000, 19.29000), Point(34.96000, -1.95000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_7)

### Extracted Polygons ###
            metal3_layer_polygon_list_0 = PointList([Point(2.46000, 0.84000), Point(2.46000, 7.98000), Point(2.09500, 7.98000), Point(2.09500, 9.24000), Point(1.77000, 9.24000), Point(1.77000, 16.17000), Point(-0.63000, 16.17000), Point(-0.63000, 20.68000), Point(33.20000, 20.68000), Point(33.20000, 16.17000), Point(30.80000, 16.17000), Point(30.80000, 9.24000), Point(30.49500, 9.24000), Point(30.49500, 7.98000), Point(30.11000, 7.98000), Point(30.11000, 0.84000), Point(29.06000, 0.84000), Point(29.06000, 7.98000), Point(28.69500, 7.98000), Point(28.69500, 9.24000), Point(28.37000, 9.24000), Point(28.37000, 16.17000), Point(25.48000, 16.17000), Point(25.48000, 9.24000), Point(25.17500, 9.24000), Point(25.17500, 7.98000), Point(24.79000, 7.98000), Point(24.79000, 0.84000), Point(23.74000, 0.84000), Point(23.74000, 7.98000), Point(23.37500, 7.98000), Point(23.37500, 9.24000), Point(23.05000, 9.24000), Point(23.05000, 16.17000), Point(20.16000, 16.17000), Point(20.16000, 9.24000), Point(19.85500, 9.24000), Point(19.85500, 7.98000), Point(19.47000, 7.98000), Point(19.47000, 0.84000), Point(18.42000, 0.84000), Point(18.42000, 7.98000), Point(18.05500, 7.98000), Point(18.05500, 9.24000), Point(17.73000, 9.24000), Point(17.73000, 16.17000), Point(14.84000, 16.17000), Point(14.84000, 9.24000), Point(14.53500, 9.24000), Point(14.53500, 7.98000), Point(14.15000, 7.98000), Point(14.15000, 0.84000), Point(13.10000, 0.84000), Point(13.10000, 7.98000), Point(12.73500, 7.98000), Point(12.73500, 9.24000), Point(12.41000, 9.24000), Point(12.41000, 16.17000), Point(9.52000, 16.17000), Point(9.52000, 9.24000), Point(9.21500, 9.24000), Point(9.21500, 7.98000), Point(8.83000, 7.98000), Point(8.83000, 0.84000), Point(7.78000, 0.84000), Point(7.78000, 7.98000), Point(7.41500, 7.98000), Point(7.41500, 9.24000), Point(7.09000, 9.24000), Point(7.09000, 16.17000), Point(4.20000, 16.17000), Point(4.20000, 9.24000), Point(3.89500, 9.24000), Point(3.89500, 7.98000), Point(3.51000, 7.98000), Point(3.51000, 0.84000)])
            dbCreatePolygon(self, metal3_layer, metal3_layer_polygon_list_0)
            metal3_layer_polygon_list_1 = PointList([Point(-0.21000, -3.02000), Point(-0.21000, 15.54000), Point(0.84000, 15.54000), Point(0.84000, 7.08000), Point(1.56000, 7.08000), Point(1.56000, -0.12000), Point(4.41000, -0.12000), Point(4.41000, 7.08000), Point(5.11000, 7.08000), Point(5.11000, 15.54000), Point(6.18000, 15.54000), Point(6.18000, 7.08000), Point(6.88000, 7.08000), Point(6.88000, -0.12000), Point(9.73000, -0.12000), Point(9.73000, 7.08000), Point(10.43000, 7.08000), Point(10.43000, 15.54000), Point(11.50000, 15.54000), Point(11.50000, 7.08000), Point(12.20000, 7.08000), Point(12.20000, -0.12000), Point(15.05000, -0.12000), Point(15.05000, 7.08000), Point(15.75000, 7.08000), Point(15.75000, 15.54000), Point(16.82000, 15.54000), Point(16.82000, 7.08000), Point(17.52000, 7.08000), Point(17.52000, -0.12000), Point(20.37000, -0.12000), Point(20.37000, 7.08000), Point(21.07000, 7.08000), Point(21.07000, 15.54000), Point(22.14000, 15.54000), Point(22.14000, 7.08000), Point(22.84000, 7.08000), Point(22.84000, -0.12000), Point(25.69000, -0.12000), Point(25.69000, 7.08000), Point(26.39000, 7.08000), Point(26.39000, 15.54000), Point(27.46000, 15.54000), Point(27.46000, 7.08000), Point(28.16000, 7.08000), Point(28.16000, -0.12000), Point(31.01000, -0.12000), Point(31.01000, 7.08000), Point(31.73000, 7.08000), Point(31.73000, 15.54000), Point(32.78000, 15.54000), Point(32.78000, -3.02000)])
            dbCreatePolygon(self, metal3_layer, metal3_layer_polygon_list_1)

### Extracted Polygons ###
            metal3_layer_pin_polygon_list_0 = PointList([Point(-0.21000, -3.02000), Point(-0.21000, -0.12000), Point(32.78000, -0.12000), Point(32.78000, -3.02000)])
            dbCreatePolygon(self, metal3_layer_pin, metal3_layer_pin_polygon_list_0)
            metal3_layer_pin_polygon_list_1 = PointList([Point(-0.61000, 16.17000), Point(-0.61000, 20.68000), Point(33.20000, 20.68000), Point(33.20000, 16.17000)])
            dbCreatePolygon(self, metal3_layer_pin, metal3_layer_pin_polygon_list_1)

### Extracted Polygons ###
            well_layer_polygon_list_0 = PointList([Point(-2.25000, -1.95000), Point(-2.25000, -0.54000), Point(33.58000, -0.54000), Point(33.58000, 18.21000), Point(-0.87000, 18.21000), Point(-0.87000, -0.54000), Point(-2.25000, -0.54000), Point(-2.25000, 19.62000), Point(34.96000, 19.62000), Point(34.96000, -1.95000)])
            dbCreatePolygon(self, well_layer, well_layer_polygon_list_0)

### Extracted Polygons ###
            SalBlock_layer_polygon_list_0 = PointList([Point(30.11000, 0.84000), Point(30.11000, 15.54000), Point(31.73000, 15.54000), Point(31.73000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_0)
            SalBlock_layer_polygon_list_1 = PointList([Point(27.44000, 0.84000), Point(27.44000, 15.54000), Point(29.06000, 15.54000), Point(29.06000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_1)
            SalBlock_layer_polygon_list_2 = PointList([Point(24.79000, 0.84000), Point(24.79000, 15.54000), Point(26.41000, 15.54000), Point(26.41000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_2)
            SalBlock_layer_polygon_list_3 = PointList([Point(22.12000, 0.84000), Point(22.12000, 15.54000), Point(23.74000, 15.54000), Point(23.74000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_3)
            SalBlock_layer_polygon_list_4 = PointList([Point(19.47000, 0.84000), Point(19.47000, 15.54000), Point(21.09000, 15.54000), Point(21.09000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_4)
            SalBlock_layer_polygon_list_5 = PointList([Point(16.80000, 0.84000), Point(16.80000, 15.54000), Point(18.42000, 15.54000), Point(18.42000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_5)
            SalBlock_layer_polygon_list_6 = PointList([Point(14.15000, 0.84000), Point(14.15000, 15.54000), Point(15.77000, 15.54000), Point(15.77000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_6)
            SalBlock_layer_polygon_list_7 = PointList([Point(11.48000, 0.84000), Point(11.48000, 15.54000), Point(13.10000, 15.54000), Point(13.10000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_7)
            SalBlock_layer_polygon_list_8 = PointList([Point(8.83000, 0.84000), Point(8.83000, 15.54000), Point(10.45000, 15.54000), Point(10.45000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_8)
            SalBlock_layer_polygon_list_9 = PointList([Point(6.16000, 0.84000), Point(6.16000, 15.54000), Point(7.78000, 15.54000), Point(7.78000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_9)
            SalBlock_layer_polygon_list_10 = PointList([Point(3.51000, 0.84000), Point(3.51000, 15.54000), Point(5.13000, 15.54000), Point(5.13000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_10)
            SalBlock_layer_polygon_list_11 = PointList([Point(0.84000, 0.84000), Point(0.84000, 15.54000), Point(2.46000, 15.54000), Point(2.46000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_11)

### Extracted Polygons ###
            nbul_layer_polygon_list_0 = PointList([Point(-1.89000, -1.59000), Point(-1.89000, 19.26000), Point(34.60000, 19.26000), Point(34.60000, -1.59000)])
            dbCreatePolygon(self, nbul_layer, nbul_layer_polygon_list_0)
        

        if self.model == 'nmoscl_4':
            outer_box = Box(-2.25, -1.95, 66.88, 19.62)
            dbCreateRect(self, diodeesd_recog_layer, outer_box)  
            dbCreateRect(self, recog_layer, outer_box)  
            # labels
            dbCreateLabel(self, textlayer, Point(1.295, -0.751), 'VSS', 'centerCenter', 'R0', Font.MATH, 0.2)
            dbCreateLabel(self, textlayer, Point(0.96, 19.11), 'VDD', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(1.45, 17.01), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, substratelayer, Point(1.45, 17.01), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(20.45, 10.01), 'nmoscl_4', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            # contact
            dbCreateRectArray(self, cont_layer, origin=(-0.755,  -1.51), n=1, m=172, x1=cont_size, off1=0.22)
            dbCreateRectArray(self, cont_layer, origin=(-0.755,  -1.13), n=1, m=172, x1=cont_size, off1=0.22)
            
            dbCreateRectArray(self, cont_layer, origin=(-0.065,  16.765), n=1, m=180, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(-0.065,  17.125), n=1, m=180, x1=cont_size, off1=cont_sep)
            
            dbCreateRectArray(self, cont_layer, origin=(-0.755,  18.64), n=1, m=172, x1=cont_size, off1=0.22)
            dbCreateRectArray(self, cont_layer, origin=(-0.755,  19.02), n=1, m=172, x1=cont_size, off1=0.22)
            
            dbCreateRectArray(self, cont_layer, origin=(-1.77,  -1.35), n=57, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(-1.41,  -1.35), n=57, m=1, x1=cont_size, off1=cont_sep)
            
            dbCreateRectArray(self, cont_layer, origin=(65.91,  -1.35), n=57, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(66.27,  -1.35), n=57, m=1, x1=cont_size, off1=cont_sep)
            # Via1 
            dbCreateRectArray(self, via1_layer, origin=(-0.545,  -1.565), n=1, m=138, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(-0.545,  -1.085), n=1, m=138, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(-0.545,  18.535), n=1, m=138, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(-0.545,  19.015), n=1, m=138, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(-1.845,  -1.045), n=42, m=1, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(-1.365,  -1.045), n=42, m=1, x1=via1_size, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(65.835,  -1.045), n=42, m=1, x1=via1_size, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(66.315,  -1.045), n=42, m=1, x1=via1_size, off1=via1_sep)
            
            for i in range(1, 26):
                dbCreateRectArray(self, cont_layer, origin=(0.065+(i-1)*2.66,  1.28), n=39, m=1, x1=cont_size, off1=cont_sep)
                dbCreateRectArray(self, cont_layer, origin=(0.425+(i-1)*2.66,  1.28), n=39, m=1, x1=cont_size, off1=cont_sep)
                dbCreateRectArray(self, via1_layer, origin=(-0.02+(i-1)*2.66,  1.125), n=30, m=2, x1=via1_size, off1=via1_sep)
                dbCreateRectArray(self, via2_layer, origin=(-0.02+(i-1)*2.66,  1.125), n=30, m=2, x1=via1_size, off1=via1_sep)
            
            dbCreateRect(self, cont_layer, Box(1.47000, 0.11500, 1.63000, 0.27500))
            dbCreateRect(self, cont_layer, Box(1.13000, 0.11500, 1.29000, 0.27500))
            dbCreateRect(self, cont_layer, Box(4.34000, 0.11500, 4.50000, 0.27500))
            dbCreateRect(self, cont_layer, Box(6.45000, 0.11500, 6.61000, 0.27500))
            dbCreateRect(self, cont_layer, Box(4.68000, 0.11500, 4.84000, 0.27500))
            dbCreateRect(self, cont_layer, Box(9.66000, 0.11500, 9.82000, 0.27500))
            dbCreateRect(self, cont_layer, Box(12.11000, 0.11500, 12.27000, 0.27500))
            dbCreateRect(self, cont_layer, Box(6.79000, 0.11500, 6.95000, 0.27500))
            dbCreateRect(self, cont_layer, Box(11.77000, 0.11500, 11.93000, 0.27500))
            dbCreateRect(self, cont_layer, Box(14.98000, 0.11500, 15.14000, 0.27500))
            dbCreateRect(self, cont_layer, Box(10.00000, 0.11500, 10.16000, 0.27500))
            dbCreateRect(self, cont_layer, Box(22.75000, 0.11500, 22.91000, 0.27500))
            dbCreateRect(self, cont_layer, Box(22.41000, 0.11500, 22.57000, 0.27500))
            dbCreateRect(self, cont_layer, Box(15.32000, 0.11500, 15.48000, 0.27500))
            dbCreateRect(self, cont_layer, Box(20.64000, 0.11500, 20.80000, 0.27500))
            dbCreateRect(self, cont_layer, Box(20.30000, 0.11500, 20.46000, 0.27500))
            dbCreateRect(self, cont_layer, Box(17.43000, 0.11500, 17.59000, 0.27500))
            dbCreateRect(self, cont_layer, Box(17.09000, 0.11500, 17.25000, 0.27500))
            dbCreateRect(self, cont_layer, Box(25.62000, 0.11500, 25.78000, 0.27500))
            dbCreateRect(self, cont_layer, Box(27.73000, 0.11500, 27.89000, 0.27500))
            dbCreateRect(self, cont_layer, Box(31.28000, 0.11500, 31.44000, 0.27500))
            dbCreateRect(self, cont_layer, Box(30.94000, 0.11500, 31.10000, 0.27500))
            dbCreateRect(self, cont_layer, Box(28.07000, 0.11500, 28.23000, 0.27500))
            dbCreateRect(self, cont_layer, Box(25.96000, 0.11500, 26.12000, 0.27500))
            dbCreateRect(self, cont_layer, Box(49.35000, 0.11500, 49.51000, 0.27500))
            dbCreateRect(self, cont_layer, Box(38.37000, 0.11500, 38.53000, 0.27500))
            dbCreateRect(self, cont_layer, Box(36.60000, 0.11500, 36.76000, 0.27500))
            dbCreateRect(self, cont_layer, Box(36.26000, 0.11500, 36.42000, 0.27500))
            dbCreateRect(self, cont_layer, Box(33.39000, 0.11500, 33.55000, 0.27500))
            dbCreateRect(self, cont_layer, Box(33.05000, 0.11500, 33.21000, 0.27500))
            dbCreateRect(self, cont_layer, Box(38.71000, 0.11500, 38.87000, 0.27500))
            dbCreateRect(self, cont_layer, Box(49.01000, 0.11500, 49.17000, 0.27500))
            dbCreateRect(self, cont_layer, Box(47.24000, 0.11500, 47.40000, 0.27500))
            dbCreateRect(self, cont_layer, Box(46.90000, 0.11500, 47.06000, 0.27500))
            dbCreateRect(self, cont_layer, Box(44.03000, 0.11500, 44.19000, 0.27500))
            dbCreateRect(self, cont_layer, Box(41.92000, 0.11500, 42.08000, 0.27500))
            dbCreateRect(self, cont_layer, Box(41.58000, 0.11500, 41.74000, 0.27500))
            dbCreateRect(self, cont_layer, Box(43.69000, 0.11500, 43.85000, 0.27500))
            dbCreateRect(self, cont_layer, Box(57.88000, 0.11500, 58.04000, 0.27500))
            dbCreateRect(self, cont_layer, Box(54.67000, 0.11500, 54.83000, 0.27500))
            dbCreateRect(self, cont_layer, Box(57.54000, 0.11500, 57.70000, 0.27500))
            dbCreateRect(self, cont_layer, Box(54.33000, 0.11500, 54.49000, 0.27500))
            dbCreateRect(self, cont_layer, Box(52.56000, 0.11500, 52.72000, 0.27500))
            dbCreateRect(self, cont_layer, Box(52.22000, 0.11500, 52.38000, 0.27500))
            dbCreateRect(self, cont_layer, Box(59.65000, 0.11500, 59.81000, 0.27500))
            dbCreateRect(self, cont_layer, Box(63.20000, 0.11500, 63.36000, 0.27500))
            dbCreateRect(self, cont_layer, Box(62.86000, 0.11500, 63.02000, 0.27500))
            dbCreateRect(self, cont_layer, Box(59.99000, 0.11500, 60.15000, 0.27500))

# Extracted activ_layer
            activ_layer_polygon_list_0 = PointList([Point(0.00000, 1.20000), Point(0.00000, 1.21000), Point(-0.00500, 1.21000), Point(-0.00500, 15.19000), Point(0.00000, 15.19000), Point(0.00000, 15.21000), Point(64.49000, 15.21000), Point(64.49000, 15.19000), Point(64.49500, 15.19000), Point(64.49500, 1.21000), Point(64.49000, 1.21000), Point(64.49000, 1.20000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_0)
            activ_layer_polygon_list_1 = PointList([Point(-0.13500, 16.69500), Point(-0.13500, 17.35500), Point(64.60500, 17.35500), Point(64.60500, 17.34000), Point(64.63000, 17.34000), Point(64.63000, 16.71000), Point(64.60500, 16.71000), Point(64.60500, 16.69500)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_1)
            activ_layer_polygon_list_2 = PointList([Point(-0.82500, -1.58000), Point(-0.82500, -1.53000), Point(-1.83000, -1.53000), Point(-1.83000, -1.42000), Point(-1.84000, -1.42000), Point(-1.84000, -0.90000), Point(65.83000, -0.90000), Point(65.83000, 18.57000), Point(-1.18000, 18.57000), Point(-1.18000, -0.90000), Point(-1.84000, -0.90000), Point(-1.84000, 19.04000), Point(-1.83000, 19.04000), Point(-1.83000, 19.20000), Point(-0.82500, 19.20000), Point(-0.82500, 19.25000), Point(64.45500, 19.25000), Point(64.45500, 19.20000), Point(66.46000, 19.20000), Point(66.46000, 19.04000), Point(66.50000, 19.04000), Point(66.50000, -1.42000), Point(66.46000, -1.42000), Point(66.46000, -1.53000), Point(64.45500, -1.53000), Point(64.45500, -1.58000)])
            dbCreatePolygon(self, activ_layer, activ_layer_polygon_list_2)
# Extracted pSD_layer
            pSD_layer_polygon_list_0 = PointList([Point(-0.33000, 16.35000), Point(-0.33000, 17.67000), Point(64.96000, 17.67000), Point(64.96000, 16.35000)])
            dbCreatePolygon(self, pSD_layer, pSD_layer_polygon_list_0)
# Extracted gatpoly_layer
            gatpoly_layer_polygon_list_0 = PointList([Point(0.96000, -0.12000), Point(0.96000, 0.59000), Point(1.20000, 0.59000), Point(1.20000, 15.84000), Point(1.56000, 15.84000), Point(1.56000, 0.59000), Point(4.41000, 0.59000), Point(4.41000, 15.84000), Point(4.77000, 15.84000), Point(4.77000, 0.59000), Point(6.52000, 0.59000), Point(6.52000, 15.84000), Point(6.88000, 15.84000), Point(6.88000, 0.59000), Point(9.73000, 0.59000), Point(9.73000, 15.84000), Point(10.09000, 15.84000), Point(10.09000, 0.59000), Point(11.84000, 0.59000), Point(11.84000, 15.84000), Point(12.20000, 15.84000), Point(12.20000, 0.59000), Point(15.05000, 0.59000), Point(15.05000, 15.84000), Point(15.41000, 15.84000), Point(15.41000, 0.59000), Point(17.16000, 0.59000), Point(17.16000, 15.84000), Point(17.52000, 15.84000), Point(17.52000, 0.59000), Point(20.37000, 0.59000), Point(20.37000, 15.84000), Point(20.73000, 15.84000), Point(20.73000, 0.59000), Point(22.48000, 0.59000), Point(22.48000, 15.84000), Point(22.84000, 15.84000), Point(22.84000, 0.59000), Point(25.69000, 0.59000), Point(25.69000, 15.84000), Point(26.05000, 15.84000), Point(26.05000, 0.59000), Point(27.80000, 0.59000), Point(27.80000, 15.84000), Point(28.16000, 15.84000), Point(28.16000, 0.59000), Point(31.01000, 0.59000), Point(31.01000, 15.84000), Point(31.37000, 15.84000), Point(31.37000, 0.59000), Point(33.12000, 0.59000), Point(33.12000, 15.84000), Point(33.48000, 15.84000), Point(33.48000, 0.59000), Point(36.33000, 0.59000), Point(36.33000, 15.84000), Point(36.69000, 15.84000), Point(36.69000, 0.59000), Point(38.44000, 0.59000), Point(38.44000, 15.84000), Point(38.80000, 15.84000), Point(38.80000, 0.59000), Point(41.65000, 0.59000), Point(41.65000, 15.84000), Point(42.01000, 15.84000), Point(42.01000, 0.59000), Point(43.76000, 0.59000), Point(43.76000, 15.84000), Point(44.12000, 15.84000), Point(44.12000, 0.59000), Point(46.97000, 0.59000), Point(46.97000, 15.84000), Point(47.33000, 15.84000), Point(47.33000, 0.59000), Point(49.08000, 0.59000), Point(49.08000, 15.84000), Point(49.44000, 15.84000), Point(49.44000, 0.59000), Point(52.29000, 0.59000), Point(52.29000, 15.84000), Point(52.65000, 15.84000), Point(52.65000, 0.59000), Point(54.40000, 0.59000), Point(54.40000, 15.84000), Point(54.76000, 15.84000), Point(54.76000, 0.59000), Point(57.61000, 0.59000), Point(57.61000, 15.84000), Point(57.97000, 15.84000), Point(57.97000, 0.59000), Point(59.72000, 0.59000), Point(59.72000, 15.84000), Point(60.08000, 15.84000), Point(60.08000, 0.59000), Point(62.93000, 0.59000), Point(62.93000, 15.84000), Point(63.29000, 15.84000), Point(63.29000, 0.59000), Point(64.06000, 0.59000), Point(64.06000, -0.12000)])
            dbCreatePolygon(self, gatpoly_layer, gatpoly_layer_polygon_list_0)
# Extracted ThickGateOx_layer
            ThickGateOx_layer_polygon_list_0 = PointList([Point(-0.42000, 0.86000), Point(-0.42000, 15.84500), Point(64.98000, 15.84500), Point(64.98000, 0.86000)])
            dbCreatePolygon(self, ThickGateOx_layer, ThickGateOx_layer_polygon_list_0)
# Extracted metal1_layer
            metal1_layer_polygon_list_0 = PointList([Point(60.98000, 0.81000), Point(60.98000, 15.21000), Point(61.11000, 15.21000), Point(61.11000, 15.24500), Point(61.88000, 15.24500), Point(61.88000, 15.21000), Point(62.03000, 15.21000), Point(62.03000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_0)
            metal1_layer_polygon_list_1 = PointList([Point(55.66000, 0.81000), Point(55.66000, 15.21000), Point(55.79000, 15.21000), Point(55.79000, 15.24500), Point(56.56000, 15.24500), Point(56.56000, 15.21000), Point(56.71000, 15.21000), Point(56.71000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_1)
            metal1_layer_polygon_list_2 = PointList([Point(50.34000, 0.81000), Point(50.34000, 15.21000), Point(50.47000, 15.21000), Point(50.47000, 15.24500), Point(51.24000, 15.24500), Point(51.24000, 15.21000), Point(51.39000, 15.21000), Point(51.39000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_2)
            metal1_layer_polygon_list_3 = PointList([Point(45.02000, 0.81000), Point(45.02000, 15.21000), Point(45.15000, 15.21000), Point(45.15000, 15.24500), Point(45.92000, 15.24500), Point(45.92000, 15.21000), Point(46.07000, 15.21000), Point(46.07000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_3)
            metal1_layer_polygon_list_4 = PointList([Point(39.70000, 0.81000), Point(39.70000, 15.21000), Point(39.83000, 15.21000), Point(39.83000, 15.24500), Point(40.60000, 15.24500), Point(40.60000, 15.21000), Point(40.75000, 15.21000), Point(40.75000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_4)
            metal1_layer_polygon_list_5 = PointList([Point(34.38000, 0.81000), Point(34.38000, 15.21000), Point(34.51000, 15.21000), Point(34.51000, 15.24500), Point(35.28000, 15.24500), Point(35.28000, 15.21000), Point(35.43000, 15.21000), Point(35.43000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_5)
            metal1_layer_polygon_list_6 = PointList([Point(29.06000, 0.81000), Point(29.06000, 15.21000), Point(29.19000, 15.21000), Point(29.19000, 15.24500), Point(29.96000, 15.24500), Point(29.96000, 15.21000), Point(30.11000, 15.21000), Point(30.11000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_6)
            metal1_layer_polygon_list_7 = PointList([Point(23.74000, 0.81000), Point(23.74000, 15.21000), Point(23.87000, 15.21000), Point(23.87000, 15.24500), Point(24.64000, 15.24500), Point(24.64000, 15.21000), Point(24.79000, 15.21000), Point(24.79000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_7)
            metal1_layer_polygon_list_8 = PointList([Point(18.42000, 0.81000), Point(18.42000, 15.21000), Point(18.55000, 15.21000), Point(18.55000, 15.24500), Point(19.32000, 15.24500), Point(19.32000, 15.21000), Point(19.47000, 15.21000), Point(19.47000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_8)
            metal1_layer_polygon_list_9 = PointList([Point(13.10000, 0.81000), Point(13.10000, 15.21000), Point(13.23000, 15.21000), Point(13.23000, 15.24500), Point(14.00000, 15.24500), Point(14.00000, 15.21000), Point(14.15000, 15.21000), Point(14.15000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_9)
            metal1_layer_polygon_list_10 = PointList([Point(7.78000, 0.81000), Point(7.78000, 15.21000), Point(7.91000, 15.21000), Point(7.91000, 15.24500), Point(8.68000, 15.24500), Point(8.68000, 15.21000), Point(8.83000, 15.21000), Point(8.83000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_10)
            metal1_layer_polygon_list_11 = PointList([Point(2.46000, 0.81000), Point(2.46000, 15.21000), Point(2.59000, 15.21000), Point(2.59000, 15.24500), Point(3.36000, 15.24500), Point(3.36000, 15.21000), Point(3.51000, 15.21000), Point(3.51000, 0.81000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_11)
            metal1_layer_polygon_list_12 = PointList([Point(-0.21000, -0.12000), Point(-0.21000, 0.51000), Point(63.65000, 0.51000), Point(63.65000, 16.71000), Point(59.38000, 16.71000), Point(59.38000, 0.51000), Point(58.31000, 0.51000), Point(58.31000, 16.71000), Point(54.06000, 16.71000), Point(54.06000, 0.51000), Point(52.99000, 0.51000), Point(52.99000, 16.71000), Point(48.74000, 16.71000), Point(48.74000, 0.51000), Point(47.67000, 0.51000), Point(47.67000, 16.71000), Point(43.42000, 16.71000), Point(43.42000, 0.51000), Point(42.35000, 0.51000), Point(42.35000, 16.71000), Point(38.10000, 16.71000), Point(38.10000, 0.51000), Point(37.03000, 0.51000), Point(37.03000, 16.71000), Point(32.78000, 16.71000), Point(32.78000, 0.51000), Point(31.71000, 0.51000), Point(31.71000, 16.71000), Point(27.46000, 16.71000), Point(27.46000, 0.51000), Point(26.39000, 0.51000), Point(26.39000, 16.71000), Point(22.14000, 16.71000), Point(22.14000, 0.51000), Point(21.07000, 0.51000), Point(21.07000, 16.71000), Point(16.82000, 16.71000), Point(16.82000, 0.51000), Point(15.75000, 0.51000), Point(15.75000, 16.71000), Point(11.50000, 16.71000), Point(11.50000, 0.51000), Point(10.43000, 0.51000), Point(10.43000, 16.71000), Point(6.18000, 16.71000), Point(6.18000, 0.51000), Point(5.11000, 0.51000), Point(5.11000, 16.71000), Point(0.84000, 16.71000), Point(0.84000, 0.51000), Point(-0.21000, 0.51000), Point(-0.21000, 17.40000), Point(64.69000, 17.40000), Point(64.69000, 17.37000), Point(64.70000, 17.37000), Point(64.70000, -0.12000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_12)
            metal1_layer_polygon_list_13 = PointList([Point(-2.25000, -1.95000), Point(-2.25000, -0.54000), Point(65.50000, -0.54000), Point(65.50000, 17.88000), Point(-0.87000, 17.88000), Point(-0.87000, -0.54000), Point(-2.25000, -0.54000), Point(-2.25000, 19.29000), Point(66.88000, 19.29000), Point(66.88000, -1.95000)])
            dbCreatePolygon(self, metal1_layer, metal1_layer_polygon_list_13)
# Extracted metal2_layer
            metal2_layer_polygon_list_0 = PointList([Point(63.65000, 0.84000), Point(63.65000, 15.21000), Point(63.77000, 15.21000), Point(63.77000, 15.24000), Point(64.54000, 15.24000), Point(64.54000, 15.21000), Point(64.61000, 15.21000), Point(64.61000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_0)
            metal2_layer_polygon_list_1 = PointList([Point(58.33000, 0.84000), Point(58.33000, 15.21000), Point(58.45000, 15.21000), Point(58.45000, 15.24000), Point(59.22000, 15.24000), Point(59.22000, 15.21000), Point(59.36000, 15.21000), Point(59.36000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_1)
            metal2_layer_polygon_list_2 = PointList([Point(53.01000, 0.84000), Point(53.01000, 15.21000), Point(53.13000, 15.21000), Point(53.13000, 15.24000), Point(53.90000, 15.24000), Point(53.90000, 15.21000), Point(54.04000, 15.21000), Point(54.04000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_2)
            metal2_layer_polygon_list_3 = PointList([Point(47.69000, 0.84000), Point(47.69000, 15.21000), Point(47.81000, 15.21000), Point(47.81000, 15.24000), Point(48.58000, 15.24000), Point(48.58000, 15.21000), Point(48.72000, 15.21000), Point(48.72000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_3)
            metal2_layer_polygon_list_4 = PointList([Point(42.37000, 0.84000), Point(42.37000, 15.21000), Point(42.49000, 15.21000), Point(42.49000, 15.24000), Point(43.26000, 15.24000), Point(43.26000, 15.21000), Point(43.40000, 15.21000), Point(43.40000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_4)
            metal2_layer_polygon_list_5 = PointList([Point(37.05000, 0.84000), Point(37.05000, 15.21000), Point(37.17000, 15.21000), Point(37.17000, 15.24000), Point(37.94000, 15.24000), Point(37.94000, 15.21000), Point(38.08000, 15.21000), Point(38.08000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_5)
            metal2_layer_polygon_list_6 = PointList([Point(31.73000, 0.84000), Point(31.73000, 15.21000), Point(31.85000, 15.21000), Point(31.85000, 15.24000), Point(32.62000, 15.24000), Point(32.62000, 15.21000), Point(32.76000, 15.21000), Point(32.76000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_6)
            metal2_layer_polygon_list_7 = PointList([Point(26.41000, 0.84000), Point(26.41000, 15.21000), Point(26.53000, 15.21000), Point(26.53000, 15.24000), Point(27.30000, 15.24000), Point(27.30000, 15.21000), Point(27.44000, 15.21000), Point(27.44000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_7)
            metal2_layer_polygon_list_8 = PointList([Point(21.09000, 0.84000), Point(21.09000, 15.21000), Point(21.21000, 15.21000), Point(21.21000, 15.24000), Point(21.98000, 15.24000), Point(21.98000, 15.21000), Point(22.12000, 15.21000), Point(22.12000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_8)
            metal2_layer_polygon_list_9 = PointList([Point(15.77000, 0.84000), Point(15.77000, 15.21000), Point(15.89000, 15.21000), Point(15.89000, 15.24000), Point(16.66000, 15.24000), Point(16.66000, 15.21000), Point(16.80000, 15.21000), Point(16.80000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_9)
            metal2_layer_polygon_list_10 = PointList([Point(10.45000, 0.84000), Point(10.45000, 15.21000), Point(10.57000, 15.21000), Point(10.57000, 15.24000), Point(11.34000, 15.24000), Point(11.34000, 15.21000), Point(11.48000, 15.21000), Point(11.48000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_10)
            metal2_layer_polygon_list_11 = PointList([Point(5.13000, 0.84000), Point(5.13000, 15.21000), Point(5.25000, 15.21000), Point(5.25000, 15.24000), Point(6.02000, 15.24000), Point(6.02000, 15.21000), Point(6.16000, 15.21000), Point(6.16000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_11)
            metal2_layer_polygon_list_12 = PointList([Point(-0.12000, 0.84000), Point(-0.12000, 15.21000), Point(-0.07000, 15.21000), Point(-0.07000, 15.24000), Point(0.70000, 15.24000), Point(0.70000, 15.21000), Point(0.84000, 15.21000), Point(0.84000, 0.84000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_12)
            metal2_layer_polygon_list_13 = PointList([Point(-2.25000, -1.95000), Point(-2.25000, -0.54000), Point(65.50000, -0.54000), Point(65.50000, 17.88000), Point(62.03000, 17.88000), Point(62.03000, -0.54000), Point(60.98000, -0.54000), Point(60.98000, 17.88000), Point(56.71000, 17.88000), Point(56.71000, -0.54000), Point(55.66000, -0.54000), Point(55.66000, 17.88000), Point(51.39000, 17.88000), Point(51.39000, -0.54000), Point(50.34000, -0.54000), Point(50.34000, 17.88000), Point(46.07000, 17.88000), Point(46.07000, -0.54000), Point(45.02000, -0.54000), Point(45.02000, 17.88000), Point(40.75000, 17.88000), Point(40.75000, -0.54000), Point(39.70000, -0.54000), Point(39.70000, 17.88000), Point(35.43000, 17.88000), Point(35.43000, -0.54000), Point(34.38000, -0.54000), Point(34.38000, 17.88000), Point(30.11000, 17.88000), Point(30.11000, -0.54000), Point(29.06000, -0.54000), Point(29.06000, 17.88000), Point(24.79000, 17.88000), Point(24.79000, -0.54000), Point(23.74000, -0.54000), Point(23.74000, 17.88000), Point(19.47000, 17.88000), Point(19.47000, -0.54000), Point(18.42000, -0.54000), Point(18.42000, 17.88000), Point(14.15000, 17.88000), Point(14.15000, -0.54000), Point(13.10000, -0.54000), Point(13.10000, 17.88000), Point(8.83000, 17.88000), Point(8.83000, -0.54000), Point(7.78000, -0.54000), Point(7.78000, 17.88000), Point(3.51000, 17.88000), Point(3.51000, -0.54000), Point(2.46000, -0.54000), Point(2.46000, 17.88000), Point(-0.87000, 17.88000), Point(-0.87000, -0.54000), Point(-2.25000, -0.54000), Point(-2.25000, 19.29000), Point(66.88000, 19.29000), Point(66.88000, -1.95000)])
            dbCreatePolygon(self, metal2_layer, metal2_layer_polygon_list_13)
# Extracted metal3_layer
            metal3_layer_polygon_list_0 = PointList([Point(-0.21000, -3.02000), Point(-0.21000, 15.54000), Point(0.84000, 15.54000), Point(0.84000, 7.08000), Point(1.56000, 7.08000), Point(1.56000, -0.12000), Point(4.41000, -0.12000), Point(4.41000, 7.08000), Point(5.11000, 7.08000), Point(5.11000, 15.54000), Point(6.18000, 15.54000), Point(6.18000, 7.08000), Point(6.88000, 7.08000), Point(6.88000, -0.12000), Point(9.73000, -0.12000), Point(9.73000, 7.08000), Point(10.43000, 7.08000), Point(10.43000, 15.54000), Point(11.50000, 15.54000), Point(11.50000, 7.08000), Point(12.20000, 7.08000), Point(12.20000, -0.12000), Point(15.05000, -0.12000), Point(15.05000, 7.08000), Point(15.75000, 7.08000), Point(15.75000, 15.54000), Point(16.82000, 15.54000), Point(16.82000, 7.08000), Point(17.52000, 7.08000), Point(17.52000, -0.12000), Point(20.37000, -0.12000), Point(20.37000, 7.08000), Point(21.07000, 7.08000), Point(21.07000, 15.54000), Point(22.14000, 15.54000), Point(22.14000, 7.08000), Point(22.84000, 7.08000), Point(22.84000, -0.12000), Point(25.69000, -0.12000), Point(25.69000, 7.08000), Point(26.39000, 7.08000), Point(26.39000, 15.54000), Point(27.46000, 15.54000), Point(27.46000, 7.08000), Point(28.16000, 7.08000), Point(28.16000, -0.12000), Point(31.01000, -0.12000), Point(31.01000, 7.08000), Point(31.71000, 7.08000), Point(31.71000, 15.54000), Point(32.78000, 15.54000), Point(32.78000, 7.08000), Point(33.48000, 7.08000), Point(33.48000, -0.12000), Point(36.33000, -0.12000), Point(36.33000, 7.08000), Point(37.03000, 7.08000), Point(37.03000, 15.54000), Point(38.10000, 15.54000), Point(38.10000, 7.08000), Point(38.80000, 7.08000), Point(38.80000, -0.12000), Point(41.65000, -0.12000), Point(41.65000, 7.08000), Point(42.35000, 7.08000), Point(42.35000, 15.54000), Point(43.42000, 15.54000), Point(43.42000, 7.08000), Point(44.12000, 7.08000), Point(44.12000, -0.12000), Point(46.97000, -0.12000), Point(46.97000, 7.08000), Point(47.67000, 7.08000), Point(47.67000, 15.54000), Point(48.74000, 15.54000), Point(48.74000, 7.08000), Point(49.44000, 7.08000), Point(49.44000, -0.12000), Point(52.29000, -0.12000), Point(52.29000, 7.08000), Point(52.99000, 7.08000), Point(52.99000, 15.54000), Point(54.06000, 15.54000), Point(54.06000, 7.08000), Point(54.76000, 7.08000), Point(54.76000, -0.12000), Point(57.61000, -0.12000), Point(57.61000, 7.08000), Point(58.31000, 7.08000), Point(58.31000, 15.54000), Point(59.38000, 15.54000), Point(59.38000, 7.08000), Point(60.08000, 7.08000), Point(60.08000, -0.12000), Point(62.93000, -0.12000), Point(62.93000, 7.08000), Point(63.65000, 7.08000), Point(63.65000, 15.54000), Point(64.70000, 15.54000), Point(64.70000, -3.02000)])
            dbCreatePolygon(self, metal3_layer, metal3_layer_polygon_list_0)
            metal3_layer_polygon_list_1 = PointList([Point(2.46000, 0.84000), Point(2.46000, 7.98000), Point(2.09500, 7.98000), Point(2.09500, 9.24000), Point(1.77000, 9.24000), Point(1.77000, 16.17000), Point(-0.63000, 16.17000), Point(-0.63000, 20.68000), Point(65.12000, 20.68000), Point(65.12000, 16.17000), Point(62.72000, 16.17000), Point(62.72000, 9.24000), Point(62.41500, 9.24000), Point(62.41500, 7.98000), Point(62.03000, 7.98000), Point(62.03000, 0.84000), Point(60.98000, 0.84000), Point(60.98000, 7.98000), Point(60.61500, 7.98000), Point(60.61500, 9.24000), Point(60.29000, 9.24000), Point(60.29000, 16.17000), Point(57.40000, 16.17000), Point(57.40000, 9.24000), Point(57.09500, 9.24000), Point(57.09500, 7.98000), Point(56.71000, 7.98000), Point(56.71000, 0.84000), Point(55.66000, 0.84000), Point(55.66000, 7.98000), Point(55.29500, 7.98000), Point(55.29500, 9.24000), Point(54.97000, 9.24000), Point(54.97000, 16.17000), Point(52.08000, 16.17000), Point(52.08000, 9.24000), Point(51.77500, 9.24000), Point(51.77500, 7.98000), Point(51.39000, 7.98000), Point(51.39000, 0.84000), Point(50.34000, 0.84000), Point(50.34000, 7.98000), Point(49.97500, 7.98000), Point(49.97500, 9.24000), Point(49.65000, 9.24000), Point(49.65000, 16.17000), Point(46.76000, 16.17000), Point(46.76000, 9.24000), Point(46.45500, 9.24000), Point(46.45500, 7.98000), Point(46.07000, 7.98000), Point(46.07000, 0.84000), Point(45.02000, 0.84000), Point(45.02000, 7.98000), Point(44.65500, 7.98000), Point(44.65500, 9.24000), Point(44.33000, 9.24000), Point(44.33000, 16.17000), Point(41.44000, 16.17000), Point(41.44000, 9.24000), Point(41.13500, 9.24000), Point(41.13500, 7.98000), Point(40.75000, 7.98000), Point(40.75000, 0.84000), Point(39.70000, 0.84000), Point(39.70000, 7.98000), Point(39.33500, 7.98000), Point(39.33500, 9.24000), Point(39.01000, 9.24000), Point(39.01000, 16.17000), Point(36.12000, 16.17000), Point(36.12000, 9.24000), Point(35.81500, 9.24000), Point(35.81500, 7.98000), Point(35.43000, 7.98000), Point(35.43000, 0.84000), Point(34.38000, 0.84000), Point(34.38000, 7.98000), Point(34.01500, 7.98000), Point(34.01500, 9.24000), Point(33.69000, 9.24000), Point(33.69000, 16.17000), Point(30.80000, 16.17000), Point(30.80000, 9.24000), Point(30.49500, 9.24000), Point(30.49500, 7.98000), Point(30.11000, 7.98000), Point(30.11000, 0.84000), Point(29.06000, 0.84000), Point(29.06000, 7.98000), Point(28.69500, 7.98000), Point(28.69500, 9.24000), Point(28.37000, 9.24000), Point(28.37000, 16.17000), Point(25.48000, 16.17000), Point(25.48000, 9.24000), Point(25.17500, 9.24000), Point(25.17500, 7.98000), Point(24.79000, 7.98000), Point(24.79000, 0.84000), Point(23.74000, 0.84000), Point(23.74000, 7.98000), Point(23.37500, 7.98000), Point(23.37500, 9.24000), Point(23.05000, 9.24000), Point(23.05000, 16.17000), Point(20.16000, 16.17000), Point(20.16000, 9.24000), Point(19.85500, 9.24000), Point(19.85500, 7.98000), Point(19.47000, 7.98000), Point(19.47000, 0.84000), Point(18.42000, 0.84000), Point(18.42000, 7.98000), Point(18.05500, 7.98000), Point(18.05500, 9.24000), Point(17.73000, 9.24000), Point(17.73000, 16.17000), Point(14.84000, 16.17000), Point(14.84000, 9.24000), Point(14.53500, 9.24000), Point(14.53500, 7.98000), Point(14.15000, 7.98000), Point(14.15000, 0.84000), Point(13.10000, 0.84000), Point(13.10000, 7.98000), Point(12.73500, 7.98000), Point(12.73500, 9.24000), Point(12.41000, 9.24000), Point(12.41000, 16.17000), Point(9.52000, 16.17000), Point(9.52000, 9.24000), Point(9.21500, 9.24000), Point(9.21500, 7.98000), Point(8.83000, 7.98000), Point(8.83000, 0.84000), Point(7.78000, 0.84000), Point(7.78000, 7.98000), Point(7.41500, 7.98000), Point(7.41500, 9.24000), Point(7.09000, 9.24000), Point(7.09000, 16.17000), Point(4.20000, 16.17000), Point(4.20000, 9.24000), Point(3.89500, 9.24000), Point(3.89500, 7.98000), Point(3.51000, 7.98000), Point(3.51000, 0.84000)])
            dbCreatePolygon(self, metal3_layer, metal3_layer_polygon_list_1)
# Extracted metal3_layer_pin
            metal3_layer_pin_polygon_list_0 = PointList([Point(-0.21000, -3.02000), Point(-0.21000, -0.12000), Point(64.70000, -0.12000), Point(64.70000, -3.02000)])
            dbCreatePolygon(self, metal3_layer_pin, metal3_layer_pin_polygon_list_0)
            metal3_layer_pin_polygon_list_1 = PointList([Point(-0.63000, 16.17000), Point(-0.63000, 20.68000), Point(65.12000, 20.68000), Point(65.12000, 16.17000)])
            dbCreatePolygon(self, metal3_layer_pin, metal3_layer_pin_polygon_list_1)
# Extracted well_layer
            well_layer_polygon_list_0 = PointList([Point(-2.25000, -1.95000), Point(-2.25000, -0.54000), Point(65.50000, -0.54000), Point(65.50000, 18.21000), Point(-0.87000, 18.21000), Point(-0.87000, -0.54000), Point(-2.25000, -0.54000), Point(-2.25000, 19.62000), Point(66.88000, 19.62000), Point(66.88000, -1.95000)])
            dbCreatePolygon(self, well_layer, well_layer_polygon_list_0)
# Extracted SalBlock_layer
            SalBlock_layer_polygon_list_0 = PointList([Point(62.03000, 0.84000), Point(62.03000, 15.54000), Point(63.65000, 15.54000), Point(63.65000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_0)
            SalBlock_layer_polygon_list_1 = PointList([Point(59.36000, 0.84000), Point(59.36000, 15.54000), Point(60.98000, 15.54000), Point(60.98000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_1)
            SalBlock_layer_polygon_list_2 = PointList([Point(56.71000, 0.84000), Point(56.71000, 15.54000), Point(58.33000, 15.54000), Point(58.33000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_2)
            SalBlock_layer_polygon_list_3 = PointList([Point(54.04000, 0.84000), Point(54.04000, 15.54000), Point(55.66000, 15.54000), Point(55.66000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_3)
            SalBlock_layer_polygon_list_4 = PointList([Point(51.39000, 0.84000), Point(51.39000, 15.54000), Point(53.01000, 15.54000), Point(53.01000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_4)
            SalBlock_layer_polygon_list_5 = PointList([Point(48.72000, 0.84000), Point(48.72000, 15.54000), Point(50.34000, 15.54000), Point(50.34000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_5)
            SalBlock_layer_polygon_list_6 = PointList([Point(46.07000, 0.84000), Point(46.07000, 15.54000), Point(47.69000, 15.54000), Point(47.69000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_6)
            SalBlock_layer_polygon_list_7 = PointList([Point(43.40000, 0.84000), Point(43.40000, 15.54000), Point(45.02000, 15.54000), Point(45.02000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_7)
            SalBlock_layer_polygon_list_8 = PointList([Point(40.75000, 0.84000), Point(40.75000, 15.54000), Point(42.37000, 15.54000), Point(42.37000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_8)
            SalBlock_layer_polygon_list_9 = PointList([Point(38.08000, 0.84000), Point(38.08000, 15.54000), Point(39.70000, 15.54000), Point(39.70000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_9)
            SalBlock_layer_polygon_list_10 = PointList([Point(35.43000, 0.84000), Point(35.43000, 15.54000), Point(37.05000, 15.54000), Point(37.05000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_10)
            SalBlock_layer_polygon_list_11 = PointList([Point(32.76000, 0.84000), Point(32.76000, 15.54000), Point(34.38000, 15.54000), Point(34.38000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_11)
            SalBlock_layer_polygon_list_12 = PointList([Point(30.11000, 0.84000), Point(30.11000, 15.54000), Point(31.73000, 15.54000), Point(31.73000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_12)
            SalBlock_layer_polygon_list_13 = PointList([Point(27.44000, 0.84000), Point(27.44000, 15.54000), Point(29.06000, 15.54000), Point(29.06000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_13)
            SalBlock_layer_polygon_list_14 = PointList([Point(24.79000, 0.84000), Point(24.79000, 15.54000), Point(26.41000, 15.54000), Point(26.41000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_14)
            SalBlock_layer_polygon_list_15 = PointList([Point(22.12000, 0.84000), Point(22.12000, 15.54000), Point(23.74000, 15.54000), Point(23.74000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_15)
            SalBlock_layer_polygon_list_16 = PointList([Point(19.47000, 0.84000), Point(19.47000, 15.54000), Point(21.09000, 15.54000), Point(21.09000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_16)
            SalBlock_layer_polygon_list_17 = PointList([Point(16.80000, 0.84000), Point(16.80000, 15.54000), Point(18.42000, 15.54000), Point(18.42000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_17)
            SalBlock_layer_polygon_list_18 = PointList([Point(14.15000, 0.84000), Point(14.15000, 15.54000), Point(15.77000, 15.54000), Point(15.77000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_18)
            SalBlock_layer_polygon_list_19 = PointList([Point(11.48000, 0.84000), Point(11.48000, 15.54000), Point(13.10000, 15.54000), Point(13.10000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_19)
            SalBlock_layer_polygon_list_20 = PointList([Point(8.83000, 0.84000), Point(8.83000, 15.54000), Point(10.45000, 15.54000), Point(10.45000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_20)
            SalBlock_layer_polygon_list_21 = PointList([Point(6.16000, 0.84000), Point(6.16000, 15.54000), Point(7.78000, 15.54000), Point(7.78000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_21)
            SalBlock_layer_polygon_list_22 = PointList([Point(3.51000, 0.84000), Point(3.51000, 15.54000), Point(5.13000, 15.54000), Point(5.13000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_22)
            SalBlock_layer_polygon_list_23 = PointList([Point(0.84000, 0.84000), Point(0.84000, 15.54000), Point(2.46000, 15.54000), Point(2.46000, 0.84000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_23)
# Extracted nbul_layer
            nbul_layer_polygon_list_0 = PointList([Point(-1.89000, -1.59000), Point(-1.89000, 19.26000), Point(66.52000, 19.26000), Point(66.52000, -1.59000)])
            dbCreatePolygon(self, nbul_layer, nbul_layer_polygon_list_0)

