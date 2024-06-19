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
from cni.shapefilter import ShapeFilter

import pya

def fgOr(components1: ulist[PhysicalComponent], components2: ulist[PhysicalComponent], resultLayer: Layer) -> Grouping:
    """
    Performs a logical OR operation for lists of physical components components1 and components2, by
    selecting those polygon areas which are in either list of physical components. The resulting
    merged polygon shapes are generated on the resultLayer layer. In addition, these polygon shapes
    are used to create a Grouping object, which is the return value for this method.

    :param components1: first list of physical component derived objects
    :type components1: list of PhysicalCompent
    :param components2: second list of physical component derived objects
    :type components2: list of PhysicalCompent
    :param resultLayer: layer where resulting shapes will be generated on
    :type resultLayer: Layer
    :return: grouping object
    :rtype: Grouping

    """

    return __fgOperation(components1, components2, resultLayer, 'fgOr')


def fgAnd(components1: ulist[PhysicalComponent], components2: ulist[PhysicalComponent], resultLayer: Layer) -> Grouping:
    """
    Performs a logical AND operation for lists of physical components components1 and components2,
    by selecting those polygon areas which are in both physical components. The resulting polygon
    shapes are generated on the resultLayer layer. In addition,these polygon shapes are used to
    create a Grouping object, which is the return value for this method. If there are no polygon
    shapes, then this Grouping object is empty.

    :param components1: first list of physical component derived objects
    :type components1: list of PhysicalCompent
    :param components2: second list of physical component derived objects
    :type components2: list of PhysicalCompent
    :param resultLayer: layer where resulting shapes will be generated on
    :type resultLayer: Layer
    :return: grouping object
    :rtype: Grouping

    """

    return __fgOperation(components1, components2, resultLayer, 'fgAnd')


def fgXor(components1: ulist[PhysicalComponent], components2: ulist[PhysicalComponent], resultLayer: Layer) -> Grouping:
    """
    Performs a logical XOR operation for lists of physical components components1 and components2,
    by selecting those polygon areas which are in either list of physical components, but not in
    both lists of physical components. The resulting merged polygon shapes are generated on the
    resultLayer layer. In addition, these polygon shapes are used to create a Grouping object, which
    is the return value for this method.

    :param components1: first list of physical component derived objects
    :type components1: list of PhysicalCompent
    :param components2: second list of physical component derived objects
    :type components2: list of PhysicalCompent
    :param resultLayer: layer where resulting shapes will be generated on
    :type resultLayer: Layer
    :return: grouping object
    :rtype: Grouping

    """

    return __fgOperation(components1, components2, resultLayer, 'fgXor')


def fgNot(components1: ulist[PhysicalComponent], components2: ulist[PhysicalComponent], resultLayer: Layer) -> Grouping:
    """
    Performs a logical NOT operation for lists of physical components components1 and components2,
    by selecting those polygon areas contained in the components1 physical component which are not
    contained in the components2 physical component. The resulting polygon shapes are generated on
    the resultLayer layer. In addition, these polygon shapes are used to create a Grouping object,
    which is the return value for this method. If there are no polygon shapes generated, then this
    Grouping object will be empty.

    :param components1: first list of physical component derived objects
    :type components1: list of PhysicalCompent
    :param components2: second list of physical component derived objects
    :type components2: list of PhysicalCompent
    :param resultLayer: layer where resulting shapes will be generated on
    :type resultLayer: Layer
    :return: grouping object
    :rtype: Grouping

    """

    return __fgOperation(components1, components2, resultLayer, 'fgNot')


def __fgOperation(
        components1: ulist[PhysicalComponent],
        components2: ulist[PhysicalComponent],
        resultLayer: Layer,
        operation: str,
        filter1: ShapeFilter = ShapeFilter(),
        filter2: ShapeFilter = ShapeFilter()) -> Grouping:
    region1 = pya.Region()
    region2 = pya.Region()

    [component.addToRegion(region1, filter1) for component in components1]
    [component.addToRegion(region2, filter2) for component in components2]

    if operation == 'fgXor':
        region = region1.xor(region2)
    elif operation == 'fgAnd':
        region = region1.and_(region2)
    elif operation == 'fgOr':
        region = region1.or_(region2)
    elif operation == 'fgNot':
        region = region1.not_(region2)
    else:
        raise Exception(f"Operation '{operation}' not supported")

    grouping = Grouping()

    for poly in region.each():
        pointList = PointList()
        for point in poly.to_simple_polygon().to_dtype(Tech.get(Tech.techInUse).dataBaseUnits).each_point():
            pointList.append(Point(point.x, point.y))

        polygon = Polygon(resultLayer, pointList)
        grouping.add(polygon)

    return grouping


def fgSize(components: ulist[PhysicalComponent], filter: ShapeFilter, sizeValue: float, resultLayer: Layer, grid: float = None) -> Grouping:
    """
    Expands or shrinks all polygon areas contained in this list of physical components, according to
    the sizeValue parameter value. If this sizeValue parameter is positive, then the polygon edges
    are expanded outward by that amount. If this sizeValue parameter is negative, then the polygon
    edges are shrunk inward by that amount. The resulting polygon shapes are generated on the
    resultLayer layer. In addition, these polygon shapes are used to create a Grouping object, which
    is the return value for this method. Note that filter shape filter is first used to merge all
    shapes from the comps list, and then the SIZE geometrical operation is performed on these merged
    geometries. If the grid parameter is specified, then the points of the physical components are
    snapped with grid value to the nearest grid point.

    :param components: list of physical component derived objects
    :type components: list of PhysicalCompent
    :param filter: layer filter to use
    :type filter: ShapeFilter
    :param sizeValue: value for sizing (bias)
    :type sizeValue: float
    :param resultLayer: layer where resulting shapes will be generated on
    :type resultLayer: Layer
    :param grid: optional value for snapping
    :type grid: float
    :return: grouping object
    :rtype: Grouping

    """

    region = pya.Region()

    [component.addToRegion(region, filter) for component in components]

    grouping = Grouping()

    sizedRegion = region.sized(sizeValue / Tech.get(Tech.techInUse).dataBaseUnits)

    if grid is not None:
        decimalGrid = int(grid / Tech.get(Tech.techInUse).dataBaseUnits)
        sizedRegion.snap(decimalGrid, decimalGrid)

    for poly in sizedRegion.each():
        pointList = PointList()
        for point in poly.to_simple_polygon().to_dtype(Tech.get(Tech.techInUse).dataBaseUnits).each_point():
            pointList.append(Point(point.x, point.y))

        polygon = Polygon(resultLayer, pointList)
        grouping.add(polygon)

    return grouping

