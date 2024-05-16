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
    """
    The Transform class provides the ability to implement two-dimensional
    transformations, consisting of orientation changes (rotations and mirroring about the
    coordinate axes), translation (offsets in the X and Y directions), and magnification of the
    X and Y coordinates, with the operations performed in the following order:
        1. Rotation/Mirroring
        2. Translation
        3. Magnification
    When rotation operations are performed on an object in the layout design, it is important
    to note that it may be necessary to first translate the object to the origin of the DLO
    coordinate system, apply the rotation operation, and then translate the object back to its
    original location. This would be necessary, because the center of rotation is the origin of
    the coordinate system, not the center of the object. With this approach, the object will be
    rotated about the center of the object. Otherwise, the resulting rotation may not produce
    the expected results. In order to more easily handle this situation, the rotate() methods
    are provided by this Transform class.

    Creation:\n
    The Transform object can be directly created using the desired x and y coordinate values
    for the translation operation, the desired orientation value, and the desired magnification
    value. The individual x and y coordinate values can be specified, or the corresponding
    Point object can be used instead. Thus, this Transform object can be created using either
    of the following forms:

    Transform(Coord x, Coord y, Orientation o=R0, double mag=1.0)\n
    Transform(Point offset, Orientation o=R0, double mag=1.0)

    If these values are not specified, then default values will be generated and used.

    """
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

