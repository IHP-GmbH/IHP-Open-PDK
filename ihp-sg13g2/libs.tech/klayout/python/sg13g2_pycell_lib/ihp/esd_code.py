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
        
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name', ChoiceConstraint(['diodevdd_2kv', 'diodevss_2kv', 'diodevdd_4kv', 'diodevss_4kv', 'nmoscl_2', 'nmoscl_4']) )
        specs('isolated', False, 'Make dovice isolated')

    def setupParams(self, params):
        self.model = params['model']
        self.isolated = params['isolated']
        pass

    def genLayout(self):
        
        self.techparams = self.tech.getTechParams()
        epsilon = self.techparams['epsilon1']

        isolated = self.isolated
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
        textlayer = Layer('TEXT', 'drawing')
        nbul_layer = Layer('nBuLay', 'drawing')
        # DRC rules
        cont_size = self.techparams['Cnt_a']
        cont_dist = self.techparams['Cnt_b']
        cont_diff_over = self.techparams['Cnt_c']
        pdiffx_over = self.techparams['pSD_c']
        via1_size = self.techparams['Vn_a']
        via1_sep = self.techparams['Vn_b1']
        
        # custom definitions
        cont_sep = 0.2


        if self.model == 'diodevss_2kv':
            pass
            #  well layer

        if self.model == 'diodevdd_2kv':
            pass
        
        if self.model == 'diodevss_2kv':
            pass

        if self.model == 'diodevdd_2kv' or self.model == 'diodevdd_2kv': 
            outer_box = Box(0, 0, 9.72, 37.05)
            dbCreateRect(self, diodeesd_recog_layer, outer_box)  
            if self.isolated : 
                dbCreateRect(self, nbul_layer, outer_box)  
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
            dbCreateRectArray(self, via1_layer, origin=(1.99,  3.74), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(1.99, 12.74), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(1.99, 21.74), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(1.99, 30.74), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.55,  3.74), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.55, 12.74), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.55, 21.74), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.55, 30.74), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.305,  7.76), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.305, 16.76), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.305, 25.76), n=8, m=3, x1=0.19, off1=via1_sep)
        
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
            
            if self.isolated: 
                dbCreateRect(self, nbul_layer, outer_box)  

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
            dbCreateRectArray(self, via1_layer, origin=(2.03,  3.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.03, 12.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.03, 21.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.03, 30.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.59,  3.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.59, 12.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.59, 21.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.59, 30.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285,  7.745), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 16.745), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 25.745), n=8, m=3, x1=0.19, off1=via1_sep)

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
            
            if self.isolated: 
                dbCreateRect(self, nbul_layer, outer_box)  

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
            dbCreateRectArray(self, via1_layer, origin=(2.01,  3.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 12.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 21.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 30.73), n=6, m=3, x1=0.19, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(6.57,  3.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 12.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 21.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 30.73), n=6, m=3, x1=0.19, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(11.13,  3.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 12.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 21.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 30.73), n=6, m=3, x1=0.19, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(4.285,  7.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 16.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 25.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815,  7.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815, 16.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815, 25.665), n=8, m=3, x1=0.19, off1=via1_sep)
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
            
            if self.isolated: 
                dbCreateRect(self, nbul_layer, outer_box)  

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
            dbCreateRectArray(self, via1_layer, origin=(2.01,  3.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 12.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 21.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(2.01, 30.73), n=6, m=3, x1=0.19, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(6.57,  3.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 12.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 21.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(6.57, 30.73), n=6, m=3, x1=0.19, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(11.13,  3.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 12.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 21.73), n=6, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(11.13, 30.73), n=6, m=3, x1=0.19, off1=via1_sep)
            
            dbCreateRectArray(self, via1_layer, origin=(4.285,  7.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 16.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(4.285, 25.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815,  7.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815, 16.665), n=8, m=3, x1=0.19, off1=via1_sep)
            dbCreateRectArray(self, via1_layer, origin=(8.815, 25.665), n=8, m=3, x1=0.19, off1=via1_sep)

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
            
            dbCreateRectArray(self, cont_layer, origin=(-0.71,  -1.315), n=1, m=96, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(0.45,  16.945), n=1, m=90, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(-0.71,  18.785), n=1, m=96, x1=cont_size, off1=cont_sep)
            
            dbCreateRectArray(self, cont_layer, origin=(-1.59,  -1.35), n=57, m=1, x1=cont_size, off1=cont_sep)
            dbCreateRectArray(self, cont_layer, origin=(34.17,  -1.35), n=57, m=1, x1=cont_size, off1=cont_sep)
            
            for i in range(1, 14):
                dbCreateRectArray(self, cont_layer, origin=(0.065+(i-1)*2.66,  1.28), n=39, m=1, x1=cont_size, off1=cont_sep)
                dbCreateRectArray(self, cont_layer, origin=(0.425+(i-1)*2.66,  1.28), n=39, m=1, x1=cont_size, off1=cont_sep)
                dbCreateRectArray(self, via1_layer, origin=(-0.02+(i-1)*2.66,  1.125), n=30, m=2, x1=0.19, off1=via1_sep)
                dbCreateRectArray(self, via2_layer, origin=(-0.02+(i-1)*2.66,  1.125), n=30, m=2, x1=0.19, off1=via1_sep)




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
            SalBlock_layer_polygon_list_0 = PointList([Point(-0.51500, 0.86000), Point(-0.51500, 15.84500), Point(33.09500, 15.84500), Point(33.09500, 0.86000)])
            dbCreatePolygon(self, SalBlock_layer, SalBlock_layer_polygon_list_0)

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
            nbullay_layer_polygon_list_0 = PointList([Point(-1.89000, -1.59000), Point(-1.89000, 19.26000), Point(34.60000, 19.26000), Point(34.60000, -1.59000)])
            dbCreatePolygon(self, nbul_layer, nbullay_layer_polygon_list_0)
