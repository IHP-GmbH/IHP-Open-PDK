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
from abc import ABC, abstractmethod
from cni.ulist import *
from cni.namemapper import NameMapper
from cni.transform import Transform

import pya

class PhysicalComponent(ABC):

    @abstractmethod
    def addToRegion(self, region: pya.Region):
        pass

    @abstractmethod
    def clone(self, nameMap : NameMapper = NameMapper(), netMap : NameMapper = NameMapper()):
        pass

    def fgOr(self, component: PhysicalComponent, resultLayer: Layer) -> Grouping:
        """
        Performs a logical or operation for this physical component and another physical component,
        by selecting those polygon areas which are in either physical component. The resulting
        merged polygon shapes are generated on the resultLayer layer. In addition, these polygon
        shapes are used to create a Grouping object, which is the return value for this method.

        :param component: physical component derived object
        :type component: PhysicalCompent
        :param resultLayer: layer where resulting shapes will be generated on
        :type resultLayer: Layer
        :return: grouping object
        :rtype: Grouping

        """
        components1 = ulist[PhysicalComponent]()
        components1.append(self)

        components2 = ulist[PhysicalComponent]()
        components2.append(component)

        import cni.geo
        return cni.geo.fgOr(components1, components2, resultLayer)

    def fgXor(self, component: PhysicalComponent, resultLayer: Layer) -> Grouping:
        """
        Performs a logical xor operation for this physical component and another physical component,
        by selecting those polygon areas which are in either physical component, but not in both
        lists of physical components. The resulting merged polygon shapes are generated on the
        resultLayer layer. In addition, these polygon shapes are used to create a Grouping object,
        which is the return value for this method.

        :param component: physical component derived object
        :type component: PhysicalCompent
        :param resultLayer: layer where resulting shapes will be generated on
        :type resultLayer: Layer
        :return: grouping object
        :rtype: Grouping

        """
        components1 = ulist[PhysicalComponent]()
        components1.append(self)

        components2 = ulist[PhysicalComponent]()
        components2.append(component)

        import cni.geo
        return cni.geo.fgXor(components1, components2, resultLayer)

    def fgAnd(self, component: PhysicalComponent, resultLayer: Layer) -> Grouping:
        """
        Performs a logical and operation for this physical component and the component physical
        component, by selecting those polygon areas which are in both physical components. The
        resulting polygon shapes are generated on the resultLayer layer. In addition, these polygon
        shapes are used to create a Grouping object, which is the return value for this method. If
        there are no polygon shapes, then this Grouping object is empty.

        :param component: physical component derived object
        :type component: PhysicalCompent
        :param resultLayer: layer where resulting shapes will be generated on
        :type resultLayer: Layer
        :return: grouping object
        :rtype: Grouping

        """
        components1 = ulist[PhysicalComponent]()
        components1.append(self)

        components2 = ulist[PhysicalComponent]()
        components2.append(component)

        import cni.geo
        return cni.geo.fgAnd(components1, components2, resultLayer)

    def fgNot(self, component: PhysicalComponent, resultLayer: Layer) -> Grouping:
        """
        Performs a logical not operation for this physical component and another physical component,
        by selecting those polygon areas contained in this physical component which are not
        contained in the component physical component. The resulting polygon shapes are generated on
        the resultLayer layer. In addition, these polygon shapes are used to create a Grouping
        object, which is the return value for this method. If there are no polygon shapes generated,
        then this Grouping object will be empty.

        :param component: physical component derived object
        :type component: PhysicalCompent
        :param resultLayer: layer where resulting shapes will be generated on
        :type resultLayer: Layer
        :return: grouping object
        :rtype: Grouping

        """
        components1 = ulist[PhysicalComponent]()
        components1.append(self)

        components2 = ulist[PhysicalComponent]()
        components2.append(component)

        import cni.geo
        return cni.geo.fgNot(components1, components2, resultLayer)

    def fgSize(self, filter: ShapeFilter, sizeValue: float, resultLayer: Layer, grid: float = None) -> Grouping:
        """
        Expands or shrinks all polygon areas contained in this physical component, according to the
        sizeValue parameter value. If this sizeValue parameter is positive, then the polygon edges
        are expanded outward by that amount. If this sizeValue parameter is negative, then the
        polygon edges are shrunk inward by that amount. The resulting polygon shapes are generated
        on the resultLayer layer. In addition, these polygon shapes are used to create a Grouping
        object, which is the return value for this method. If the grid parameter is specified, then
        the points of the physical components are snapped with grid value to the nearest grid point.

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

        components = ulist[PhysicalComponent]()
        components.append(self)

        import cni.geo
        return cni.geo.fgSize(components, filter, sizeValue, resultLayer, grid)

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def moveBy(self, dx: float, dy: float) -> None:
        pass

    @abstractmethod
    def transform(self, transform: Transform) -> None:
        pass
