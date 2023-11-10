
from cni.rect import *

class DloGen(object):

    def __init__(self):
        self.tech = None
        self.props = {}

    def set_tech(self, tech):
        self.tech = tech

    def addPin(self, name, label, box, layer):
        # simply creates a shape - needs to support other shape types?
        Rect(layer, box)


