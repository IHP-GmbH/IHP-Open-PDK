from cni.box import *
from cni.shape import *
from cni.rect import *

import pya

class Text(Shape):

    def __init__(self, layer, text, point, size):
        # TODO: size
        text = pya.DText(text, pya.DTrans(point.getX(), point.getY()), 1, 0)
        self.set_shape(Shape.cell.shapes(layer.number).insert(text))
        super().__init__(Box(text.bbox().left, text.bbox().bottom, text.bbox().right, text.bbox().top))

    def setAlignment(self, align):
        # TODO
        pass

    def setOrientation(self, orient):
        # TODO
        pass

