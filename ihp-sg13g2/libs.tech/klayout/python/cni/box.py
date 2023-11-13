########################################################################
#
# Copyright 2023 IHP PDK Authors
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

import pya

class Box(object):

    def __init__(self, l = INT_MAX, b = INT_MAX, r = INT_MIN, t = INT_MIN):
        self.box = pya.DBox(l, b, r, t)

    def abut(dir, refBox, align = True):
        raise Exception("Not implemented yet!")

    def alignEdge(dir, refBox, refDir=None, offset=None):
        raise Exception("Not implemented yet!")

    def alignEdgeToCoord(dir, coord):
        raise Exception("Not implemented yet!")

    def alignEdgeToPoint(dir, point):
        raise Exception("Not implemented yet!")

    def alignLocation(loc, refBox, refLoc=None, offset=None):
        raise Exception("Not implemented yet!")

    def alignLocationToPoint(loc, pt):
        raise Exception("Not implemented yet!")

    def centerCenter():
        raise Exception("Not implemented yet!")

    def centerLeft():
        raise Exception("Not implemented yet!")

    def centerRight():
        raise Exception("Not implemented yet!")

    def contains(box, incEdges = True):
        raise Exception("Not implemented yet!")

    def containsPoint(p, incEdges = True):
        raise Exception("Not implemented yet!")

    def expand(coord):
        raise Exception("Not implemented yet!")

    def expandDir(dir, coord):
        raise Exception("Not implemented yet!")

    def expandForMinArea(dir, minArea, grid = None):
        raise Exception("Not implemented yet!")

    def expandForMinWidth(dir, minWidth, grid = None):
        raise Exception("Not implemented yet!")

    def expandToGrid(grid, dir = None):
        raise Exception("Not implemented yet!")

    def fix(self):
        # is that function supposed for normalize the order?
        return self

    def getArea():
        raise Exception("Not implemented yet!")

    def getCenter():
        raise Exception("Not implemented yet!")

    def getCenterX():
        raise Exception("Not implemented yet!")

    def getCenterY():
        raise Exception("Not implemented yet!")

    def getCoord(dir):
        raise Exception("Not implemented yet!")

    def getDimension(dir):
        raise Exception("Not implemented yet!")

    def getHeight(self):
        return self.box.top - self.box.bottom

    def getLeft():
        raise Exception("Not implemented yet!")

    def getLocationPoint(loc):
        raise Exception("Not implemented yet!")

    def getLocationPoint(dir):
        raise Exception("Not implemented yet!")

    def getPoints():
        raise Exception("Not implemented yet!")

    def getRange(dir):
        raise Exception("Not implemented yet!")

    def getRangeX():
        raise Exception("Not implemented yet!")

    def getRangeY():
        raise Exception("Not implemented yet!")

    def getRight():
        raise Exception("Not implemented yet!")

    def getSpacing(dir, refBox):
        raise Exception("Not implemented yet!")

    def getTop():
        raise Exception("Not implemented yet!")

    def getWidth(self):
        return self.box.right - self.box.left

    def hasNoArea():
        raise Exception("Not implemented yet!")

    def init():
        raise Exception("Not implemented yet!")

    def intersect(box):
        raise Exception("Not implemented yet!")

    def intersect(box, dir):
        raise Exception("Not implemented yet!")

    def isInverted():
        raise Exception("Not implemented yet!")

    def isNormal():
        raise Exception("Not implemented yet!")

    def limit(point):
        raise Exception("Not implemented yet!")

    def lowerCenter():
        raise Exception("Not implemented yet!")

    def lowerLeft(self):
        return Point(self.box.left, self.box.bottom)

    def lowerRight():
        raise Exception("Not implemented yet!")

    def merge(box, dir):
        raise Exception("Not implemented yet!")

    def mergePoint(p):
        raise Exception("Not implemented yet!")

    def mirrorX(yCoord = 0):
        raise Exception("Not implemented yet!")

    def mirrorY(xCoord = 0):
        raise Exception("Not implemented yet!")

    def moveBy(dx, dy):
        raise Exception("Not implemented yet!")

    def moveTo(destination, loc = Location.CENTER_CENTER):
        raise Exception("Not implemented yet!")

    def moveTowards(dir, d):
        raise Exception("Not implemented yet!")

    def overlaps(box, incEdges = True):
        raise Exception("Not implemented yet!")

    def place(dir, refBox, distance, align = True):
        raise Exception("Not implemented yet!")

    def removeRegion(box):
        raise Exception("Not implemented yet!")

    def rotate90(origin = None):
        raise Exception("Not implemented yet!")

    def rotate180(origin = None):
        raise Exception("Not implemented yet!")

    def rotate270(origin = None):
        raise Exception("Not implemented yet!")

    def set(b):
        raise Exception("Not implemented yet!")

    def set(b, dir = None):
        raise Exception("Not implemented yet!")

    def set(lowerLeft, upperRight):
        raise Exception("Not implemented yet!")

    def set(left, bottom, right, top):
        raise Exception("Not implemented yet!")

    def setBottom(v):
        raise Exception("Not implemented yet!")

    def setCenter(point):
        raise Exception("Not implemented yet!")

    def setCenterY(v):
        raise Exception("Not implemented yet!")

    def setCoord(dir, coord):
        raise Exception("Not implemented yet!")

    def setDimension(coord, dir):
        raise Exception("Not implemented yet!")

    def setBottom(v):
        raise Exception("Not implemented yet!")

    def setHeight(height):
        raise Exception("Not implemented yet!")

    def setLocationPoint(loc, pt):
        raise Exception("Not implemented yet!")

    def setRange(dir, range):
        raise Exception("Not implemented yet!")

    def setRangeX(range):
        raise Exception("Not implemented yet!")

    def setRangeY(range):
        raise Exception("Not implemented yet!")

    def setRight(v):
        raise Exception("Not implemented yet!")

    def setTop(v):
        raise Exception("Not implemented yet!")

    def setWidth(width):
        raise Exception("Not implemented yet!")

    def snap(grid, snapType = None):
        raise Exception("Not implemented yet!")

    def snapX(grid, snapType = None):
        raise Exception("Not implemented yet!")

    def snapY(grid, snapType = None):
        raise Exception("Not implemented yet!")

    def snapTowards(grid, dir):
        raise Exception("Not implemented yet!")

    def transform(trans):
        raise Exception("Not implemented yet!")

    def upperCenter():
        raise Exception("Not implemented yet!")

    def upperLeft():
        raise Exception("Not implemented yet!")

    def upperRight(self):
        return Point(self.box.right, self.box.top)

    @property
    def bottom(self):
        raise Exception("Not implemented yet!")

    @property
    def left(self):
        raise Exception("Not implemented yet!")

    @property
    def right(self):
        raise Exception("Not implemented yet!")

    @property
    def top(self):
        raise Exception("Not implemented yet!")

