
from cni.location import *
from cni.orientation import *

class Font(object):
    EURO_STYLE = 1
    FIXED = 2
    GOTHIC = 3
    MATH = 4
    MIL_SPEC = 5
    ROMAN = 6
    SCRIPT = 7
    STICK = 8
    SWEDISH = 9

    @classmethod
    def getMembers(cls):
        return [cls.EURO_STYLE, cls.FIXED, cls.GOTHIC, cls.MATH, cls.MIL_SPEC, cls.ROMAN, cls.SCRIPT, cls.STICK, sls.SWEDISH]

    def calcBBox(self, text, origin, height, location=Location.UPPER_LEFT, orient=Orientation.R0, overbar=False):
        raise Exception("Not implemented yet!")

