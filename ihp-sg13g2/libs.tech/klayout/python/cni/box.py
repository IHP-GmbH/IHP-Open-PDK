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

from cni.constants import *
from cni.location import *
from cni.point import *
from cni.namemapper import *
from cni.transform import *

import pya

class Box(object):

    def __init__(self, l = INT_MAX, b = INT_MAX, r = INT_MIN, t = INT_MIN):
        self.box = pya.DBox(l, b, r, t)

    def abut(self, dir, refBox, align = True):
        raise Exception("Not implemented yet!")

    def alignEdge(self, dir, refBox, refDir=None, offset=None):
        raise Exception("Not implemented yet!")

    def alignEdgeToCoord(self, dir, coord):
        raise Exception("Not implemented yet!")

    def alignEdgeToPoint(self, dir, point):
        raise Exception("Not implemented yet!")

    def alignLocation(self, loc, refBox, refLoc=None, offset=None):
        raise Exception("Not implemented yet!")

    def alignLocationToPoint(self, loc, pt):
        raise Exception("Not implemented yet!")

    def centerCenter(self):
        raise Exception("Not implemented yet!")

    def centerLeft(self):
        raise Exception("Not implemented yet!")

    def centerRight(self):
        raise Exception("Not implemented yet!")

    def clone(self, nameMap : NameMapper = NameMapper(), netMap : NameMapper = NameMapper()):
        return Box(self.box.left, self.box.bottom, self.box.right, self.box.top)

    def contains(self, box, incEdges = True):
        raise Exception("Not implemented yet!")

    def containsPoint(self, p, incEdges = True):
        raise Exception("Not implemented yet!")

    def destroy(self):
        if not self.box._destroyed():
            import cni.shape
            cni.shape.Shape.getCell().shapes(self.__rect.getShape().layer).erase(self.__rect.getShape())
            self.box._destroy()
        else:
            pya.Logger.warn(f"Box.destroy: already destroyed!")

    def expand(self, coord):
        raise Exception("Not implemented yet!")

    def expandDir(self, dir, coord):
        raise Exception("Not implemented yet!")

    def expandForMinArea(self, dir, minArea, grid = None):
        raise Exception("Not implemented yet!")

    def expandForMinWidth(self, dir, minWidth, grid = None):
        raise Exception("Not implemented yet!")

    def expandToGrid(self, grid, dir = None):
        raise Exception("Not implemented yet!")

    def fix(self):
        if self.box.left > self.box.right or self.box.bottom > self.box.top:
            fixedBox = pya.DBox(
                    min(self.box.left, self.box.right),
                    min(self.box.bottom, self.box.top),
                    max(self.box.left, self.box.right),
                    max(self.box.bottom, self.box.top))
            self.box.assign(fixedBox)
        return self

    def getArea(self):
        raise Exception("Not implemented yet!")

    def getCenter(self):
        center = self.box.center()
        return Point(center.x, center.y)

    def getCenterX(self):
        raise Exception("Not implemented yet!")

    def getCenterY(self):
        raise Exception("Not implemented yet!")

    def getCoord(self, dir):
        raise Exception("Not implemented yet!")

    def getDimension(self, dir):
        raise Exception("Not implemented yet!")

    def getHeight(self):
        return self.box.top - self.box.bottom

    def getLeft(self):
        raise Exception("Not implemented yet!")

    def getLocationPoint(self, loc):
        raise Exception("Not implemented yet!")

    def getLocationPoint(self, dir):
        raise Exception("Not implemented yet!")

    def getPoints(self):
        raise Exception("Not implemented yet!")

    def getRange(self, dir):
        raise Exception("Not implemented yet!")

    def getRangeX(self):
        raise Exception("Not implemented yet!")

    def getRangeY(self):
        raise Exception("Not implemented yet!")

    def getRight(self):
        raise Exception("Not implemented yet!")

    def getSpacing(self, dir, refBox):
        raise Exception("Not implemented yet!")

    def getTop(self):
        raise Exception("Not implemented yet!")

    def getWidth(self):
        return self.box.right - self.box.left

    def hasNoArea(self):
        raise Exception("Not implemented yet!")

    def init(self):
        raise Exception("Not implemented yet!")

    def intersect(self, box):
        raise Exception("Not implemented yet!")

    def intersect(self, box, dir):
        raise Exception("Not implemented yet!")

    def isInverted(self):
        raise Exception("Not implemented yet!")

    def isNormal(self):
        raise Exception("Not implemented yet!")

    def limit(self, point):
        raise Exception("Not implemented yet!")

    def lowerCenter(self):
        raise Exception("Not implemented yet!")

    def lowerLeft(self):
        return Point(self.box.left, self.box.bottom)

    def lowerRight(self):
        raise Exception("Not implemented yet!")

    def merge(self, box, dir):
        raise Exception("Not implemented yet!")

    def mergePoint(self, p):
        raise Exception("Not implemented yet!")

    def mirrorX(self, yCoord = 0):
        raise Exception("Not implemented yet!")

    def mirrorY(self, xCoord = 0):
        raise Exception("Not implemented yet!")

    def moveBy(self, dx: float, dy: float) -> None:
        movedBox = pya.DTrans(dx, dy) * self.box
        import cni.shape
        shape = cni.shape.Shape.getCell().shapes(self.__rect._shape.layer).insert(movedBox)
        self.destroy()
        self.__rect._shape = shape
        self.box = movedBox

    def moveTo(self, destination, loc = Location.CENTER_CENTER):
        raise Exception("Not implemented yet!")

    def moveTowards(self, dir, d):
        raise Exception("Not implemented yet!")

    def overlaps(self, box, incEdges = True):
        raise Exception("Not implemented yet!")

    def place(self, dir, refBox, distance, align = True):
        raise Exception("Not implemented yet!")

    def removeRegion(self, box):
        raise Exception("Not implemented yet!")

    def rotate90(self, origin = None):
        raise Exception("Not implemented yet!")

    def rotate180(self, origin = None):
        raise Exception("Not implemented yet!")

    def rotate270(self, origin = None):
        raise Exception("Not implemented yet!")

    def set(self, b):
        raise Exception("Not implemented yet!")

    def set(self, b, dir = None):
        raise Exception("Not implemented yet!")

    def set(self, lowerLeft, upperRight):
        raise Exception("Not implemented yet!")

    def set(self, left, bottom, right, top):
        raise Exception("Not implemented yet!")

    def setBottom(self, v):
        raise Exception("Not implemented yet!")

    def setCenter(self, point):
        raise Exception("Not implemented yet!")

    def setCenterY(self, v):
        raise Exception("Not implemented yet!")

    def setCoord(self, dir, coord):
        raise Exception("Not implemented yet!")

    def setDimension(self, coord, dir):
        raise Exception("Not implemented yet!")

    def setBottom(self, v):
        raise Exception("Not implemented yet!")

    def setHeight(self, height):
        raise Exception("Not implemented yet!")

    def setLocationPoint(self, loc, pt):
        raise Exception("Not implemented yet!")

    def setRange(self, dir, range):
        raise Exception("Not implemented yet!")

    def setRangeX(self, range):
        raise Exception("Not implemented yet!")

    def setRangeY(self, range):
        raise Exception("Not implemented yet!")

    def setRect(self, rect):
        self.__rect = rect

    def setRight(self, v):
        raise Exception("Not implemented yet!")

    def setTop(self, v):
        raise Exception("Not implemented yet!")

    def setWidth(self, width):
        raise Exception("Not implemented yet!")

    def snap(self, grid, snapType = None):
        raise Exception("Not implemented yet!")

    def snapX(self, grid, snapType = None):
        raise Exception("Not implemented yet!")

    def snapY(self, grid, snapType = None):
        raise Exception("Not implemented yet!")

    def snapTowards(self, grid, dir):
        raise Exception("Not implemented yet!")

    def transform(self, transform: Transform) -> None:
        if self.__rect is None:
            raise Exception("No rect set for box!")

        transformedBox = self.box.transformed(transform.transform)
        import cni.shape
        shape = cni.shape.Shape.getCell().shapes(self.__rect._shape.layer).insert(transformedBox)
        self.destroy()
        self.__rect._shape = shape
        self.box = transformedBox

    def upperCenter(self):
        raise Exception("Not implemented yet!")

    def upperLeft(self):
        raise Exception("Not implemented yet!")

    def upperRight(self):
        return Point(self.box.right, self.box.top)

    @property
    def bottom(self):
        return self.box.bottom

    @property
    def left(self):
        return self.box.left

    @property
    def right(self):
        return self.box.right

    @property
    def top(self):
        return self.box.top

