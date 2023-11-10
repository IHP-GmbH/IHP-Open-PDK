
from cni.shape import *

class Rect(Shape):

    def __init__(self, layer, box):
        super().__init__(box)
        self.set_shape(Shape.cell.shapes(layer.number).insert(box.box))

