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

from functools import singledispatchmethod
from cni.shape import *
from cni.layer import *
from cni.pointlist import *
from cni.pathstyle import *
from cni.tech import Tech

import pya

class Path(Shape):
    """
    Creates a path object, using the points list of points to define the path. The width
    parameter is used to specify the width of this path. The layer parameter is a Layer object,
    the width parameter is an integer value, and the points parameter is a Python list of Point
    objects.

    :param layer: Layer to place the path
    :type layer: Layer
    :param width: width of the path
    :type width: float
    :param points: pointlist to define the path
    :type points: PointList

    """

    @singledispatchmethod
    def __init__(self, arg1, arg2, arg3, arg4 = None):
        pass

    @__init__.register
    def _(self, arg1: Layer, arg2: float, arg3: PointList, arg4 = PathStyle.TRUNCATE) -> None:
        pyaPoints = []
        [pyaPoints.append(point.point) for point in arg3]

        self._path = pya.DPath(pyaPoints, arg2)
        super().__init__(arg1, self._path.bbox())
        self.set_shape(Shape.getCell().shapes(arg1.number).insert(self._path))

    @__init__.register
    def _(self, arg1: pya.DPath, arg2: int, arg3: Layer) -> None:
        self._path = arg1
        super().__init__(arg3, self._path.bbox())
        self.set_shape(Shape.getCell().shapes(arg2).insert(self._path))

    def addToRegion(self, region: pya.Region):
        region.insert(self._path.to_itype(Tech.get(Tech.techInUse).dataBaseUnits))

    def clone(self, nameMap : NameMapper = NameMapper(), netMap : NameMapper = NameMapper()):
        dup = self._path.dup();
        path = Path(dup, self.getShape().layer, self.layer)
        return path

    def destroy(self):
        if not self._path._destroyed():
            Shape.getCell().shapes(self.getShape().layer).erase(self.getShape())
            self._path._destroy()
        else:
            pya.Logger.warn(f"Path.destroy: already destroyed!")

    def getPoints(self) -> PointList:
        pointList = PointList()
        [pointList.append(Point(point.x, point.y)) for point in self._path.each_point()]
        return pointList

    def moveBy(self, dx: float, dy: float) -> None:
        movedPath = (pya.DTrans(float(dx), float(dy)) * self._path).to_itype(Tech.get(Tech.techInUse).
            dataBaseUnits).to_simple_polygon().to_dtype(Tech.get(Tech.techInUse).dataBaseUnits)
        shape = Shape.getCell().shapes(self._shape.layer).insert(movedPath)
        self.destroy()
        self._path = movedPath
        self.set_shape(shape)

    def toString(self) -> str:
        return "Path: {}".format(self._path.to_s())

    def transform(self, transform: Transform) -> None:
        transformedPath = self._path.transformed(transform.transform)
        shape = Shape.getCell().shapes(self.getShape().layer).insert(transformedPath)
        self.destroy()
        self._path = transformedPath
        self.set_shape(shape)

