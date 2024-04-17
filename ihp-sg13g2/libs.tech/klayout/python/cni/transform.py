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

from __future__ import annotations
from functools import singledispatchmethod
from cni.orientation import *
from cni.point import *
from cni.orientation import *

import pya

class Transform(object):

    @singledispatchmethod
    def __init__(self, arg1, arg2, arg3, arg4 = None):
        pass

    @__init__.register
    def _(self, arg1: float, arg2: float, arg3: Orientation = Orientation.R0, arg4: float = 1.0):
        self._internalInit(arg1, arg2, arg3, arg4)

    @__init__.register
    def _(self, arg1: int, arg2: float, arg3: Orientation = Orientation.R0, arg4: float = 1.0):
        self._internalInit(arg1, arg2, arg3, arg4)

    @__init__.register
    def _(self, arg1: Point, arg2: Orientation = Orientation.R0, arg3 : float = 1.0):
        self._internalInit(arg1.x, arg1.y, arg2, arg3)

    def _internalInit(self, x: float, y: float, orientation: Orientation, magnification: float) -> None:
        self._x = x
        self._y = y
        self._orientation = orientation
        self._mag = magnification

        match orientation:
            case Orientation.R0:
                self._transform = pya.DCplxTrans(magnification, 0, False, x, y)
            case Orientation.R90:
                self._transform = pya.DCplxTrans(magnification, 90, False, x, y)
            case Orientation.R180:
                self._transform = pya.DCplxTrans(magnification, 180, False, x, y)
            case Orientation.R270:
                self._transform = pya.DCplxTrans(magnification, 270, False, x, y)
            case Orientation.MYR90:
                self._transform = pya.DCplxTrans(magnification, 90, False, x, y) * pya.DCplxTrans.M90
            case Orientation.MXR90:
                self._transform = pya.DCplxTrans(magnification, 90, True, x, y)
            case Orientation.MY:
                self._transform = pya.DCplxTrans(magnification, 0, False, x, y) * pya.DCplxTrans.M90
            case Orientation.MX:
                self._transform = pya.DCplxTrans(magnification, 0, True, x, y)
            case _:
                raise Exception(f"Unknown orientation '{orientation}'")
    @property
    def transform(self):
        """
        returns the internal transform representation

        """
        return self._transform

    @property
    def xOffset(self):
        """
        returns the x-coordinate value of the offset for this Transform

        """
        return self._x

    @property
    def yOffset(self):
        """
        returns the y-coordinate value of the offset for this Transform

        """
        return self._y

    @property
    def mag(self):
        """
        returns the magnification value for this Transform

        """
        return self._mag

    @property
    def orientation(self):
        """
        returns the orientation value for this Transform

        """
        return self._orientation

