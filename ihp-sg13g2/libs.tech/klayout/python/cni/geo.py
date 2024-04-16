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
from cni.grouping import *
from cni.pointlist import PointList
from cni.point import Point
from cni.polygon import Polygon
from cni.dlo import Tech

import pya

def fgOr(components1: ulist[PhysicalComponent], components2: ulist[PhysicalComponent], resultLayer: Layer) -> Grouping:
    region1 = pya.Region()
    region2 = pya.Region()

    [component.addToRegion(region1) for component in components1]
    [component.addToRegion(region2) for component in components2]

    orRegion = region1.or_(region2).merge()

    grouping = Grouping()

    for poly in orRegion.each():
        pointList = PointList()
        for point in poly.to_simple_polygon().to_dtype(Tech.get(Tech.techInUse).dataBaseUnits).each_point():
            pointList.append(Point(point.x, point.y))

        polygon = Polygon(resultLayer, pointList)
        grouping.add(polygon)

    return grouping


def fgAnd():
  # TODO: implement
  pass


def fgXor():
  # TODO: implement
  pass


def fgNot():
  # TODO: implement
  pass


def fgMerge():
  # TODO: implement
  pass


