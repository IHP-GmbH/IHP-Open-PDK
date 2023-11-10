
from cni.box import *

class Shape(object):

    cell = None

    def __init__(self, bbox = None):
        self.shape = None
        self.bbox = bbox

    def set_shape(self, sh):
        self.shape = sh

    def getBBox(self):
        return Box(self.bbox.box.left, self.bbox.box.bottom, self.bbox.box.right, self.bbox.box.top)

