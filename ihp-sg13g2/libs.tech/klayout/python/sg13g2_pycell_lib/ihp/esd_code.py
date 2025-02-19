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
        specs('model', model, 'Model name', ChoiceConstraint(['diodevdd_2kv', 'diodevss_2kv', 'diodevdd_4kv', 'idiodevdd_2kv', 'idiodevdd_4kv', 'test']) )


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
        activ_layer = Layer('Activ')
        pSD_layer = Layer('pSD')
        well_layer = Layer('NWell')
        cont_layer = Layer('Cont')
        diodeesd_recog_layer = Layer('Recog', 'esd')
        textlayer = Layer('TEXT', 'drawing')
        # DRC rules
        cont_size = self.techparams['Cnt_a']
        cont_dist = self.techparams['Cnt_b']
        cont_diff_over = self.techparams['Cnt_c']
        pdiffx_over = self.techparams['pSD_c']
        
        # custom definitions
        cont_sep = 0.2
        via1_size = 0.19
        via1_sep = 0.29


        if self.model == 'diodevss_2kv':
            pass
            #  well layer

        if self.model == 'diodevdd_2kv':
            pass
        
        if self.model == 'diodevss_2kv':
            pass


        if self.model == 'diodevdd_2kv':
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
   
        #  text layer
        
        if self.model == 'diodevdd_2kv' :
            dbCreateLabel(self, textlayer, Point(-0.32, 18.535), 'PAD', 'centerCenter', 'R0', Font.SCRIPT, 0.2)
            dbCreateLabel(self, textlayer, Point(9.15, 18.99), 'VDD', 'centerCenter', 'R0', Font.MATH, 0.2)
            dbCreateLabel(self, textlayer, Point(4.86, 0.675), 'VSS', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(8.33, 0.625), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
        
        if self.model == 'diodevss_2kv' :
            dbCreateLabel(self, textlayer, Point(-0.2, 18.535), 'PAD', 'centerCenter', 'R0', Font.SCRIPT, 0.2)
            dbCreateLabel(self, textlayer, Point(9.15, 18.99), 'VSS', 'centerCenter', 'R0', Font.MATH, 0.2)
            dbCreateLabel(self, textlayer, Point(4.86, 36.375), 'VDD', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
            dbCreateLabel(self, textlayer, Point(2.285, 2.385), 'sub!', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)
        #MkPin(self, 'MINUS', 1, metal2_pin_box2, metal2_layer)



        if self.model == 'diodevdd_2kv':
            outer_box = Box(0, 0, 9.72, 37.05)
            dbCreateRect(self, diodeesd_recog_layer, outer_box)  
 
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
