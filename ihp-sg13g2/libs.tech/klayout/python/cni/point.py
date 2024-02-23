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

import pya

import math

class Point(object):
    def __init__(self, x, y):
        self.point = pya.DPoint(x, y)

    @classmethod
    def areColinearPoints(cls, p1, p2, p3):
        """
        Returns True if these three points are colinear or coincident, and returns False otherwise.

        :param p1: first point.
        :type p1: Point
        :param p2: second point.
        :type p2: Point
        :param p3: third point.
        :type p3: Point
        :return: whether all three points are collinear or coincident
        :rtype: boolean

        """
        triangleArea = 0.5 * abs(
                (p1.point.x * (p2.point.y - p3.point.y)) +
                (p2.point.x * (p3.point.y - p1.point.y)) +
                (p3.point.x * (p1.point.y - p2.point.y)))
        return math.isclose(0.0, triangleArea) or (p1 == p2 and p2 == p3)

    def copy(self):
        raise Exception("Not implemented yet!")

    def getCoord(self, dir):
        raise Exception("Not implemented yet!")

    def getSpacing(self, dir, refPoint):
        raise Exception("Not implemented yet!")

    def getX(self):
        return self.point.x

    def getY(self):
        return self.point.y

    def invalid(self):
        raise Exception("Not implemented yet!")

    def isBetween(self, a, b):
        raise Exception("Not implemented yet!")

    def isValid(self, ):
        raise Exception("Not implemented yet!")

    def place(self, dir, refPoint, distance, align = True):
        raise Exception("Not implemented yet!")

    def set(self, p):
        raise Exception("Not implemented yet!")

    def set(self, _x, _y):
        raise Exception("Not implemented yet!")

    def setCoord(self, dir, coord):
        raise Exception("Not implemented yet!")

    def setX(self, x):
        self.point.x = x

    def setY(self, y):
        self.point.y = y

    def snap(self, grid, snapType=None):
        raise Exception("Not implemented yet!")

    def snapX(self, grid, snapType=None):
        raise Exception("Not implemented yet!")

    def snapY(self, grid, snapType=None):
        raise Exception("Not implemented yet!")

    def snapTowards(self, grid, dir):
        raise Exception("Not implemented yet!")

    def toDiagAxes(self):
        raise Exception("Not implemented yet!")

    def toOrthogAxes(self):
        raise Exception("Not implemented yet!")

    def transform(self, trans):
        raise Exception("Not implemented yet!")

    def __eq__(self, other):
        return self.point == other.point

    @property
    def x(self):
        """
        Returns the value of the x-coordinate for this point

        """
        return self.point.x

    @x.setter
    def x(self, value):
        """
        Sets the value of the x-coordinate for this point

        """
        self.point.x = value

    @property
    def y(self):
        """
        Returns the value of the y-coordinate for this point

        """
        return self.point.y

    @y.setter
    def y(self, value):
        """
        Sets the value of the y-coordinate for this point

        """
        self.point.y = value
