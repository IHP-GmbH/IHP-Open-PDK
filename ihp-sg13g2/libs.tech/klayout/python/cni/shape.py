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
from cni.box import *
from cni.physicalComponent import *
from cni.layer import *
from cni.shapefilter import *
from cni.constants import *

import pya

class Shape(PhysicalComponent):

    @classmethod
    def getCell(cls) -> pya.Cell:
        import cni.dlo
        return cni.dlo.PyCellContext.getCurrentPyCellContext().cell

    def __init__(self, layer: Layer, bbox: Box):
        self._shape = None
        self._layer = layer
        self._bbox = bbox
        self._net = None
        self._pin = None

    def set_shape(self, shape: Shape):
        self._shape = shape

    def getShape(self):
        if self._shape is None:
            raise Exception(f"Shape.getShape no shape set {hex(id(self))}: {hex(id(self._shape))}")
        return self._shape

    def getBBox(self, filter: ShapeFilter = ShapeFilter()) -> Box:
        if type(filter) is Layer and self._layer.getLayerName() == filter.getLayerName():
            return Box(self._bbox.box.left, self._bbox.box.bottom, self._bbox.box.right, self._bbox.box.top)

        if filter.isIncluded(self._layer):
            return Box(self._bbox.box.left, self._bbox.box.bottom, self._bbox.box.right, self._bbox.box.top)
        else:
            return Box(INT_MAX, INT_MAX, INT_MIN, INT_MIN)

    def getLayer(self) -> Layer:
        return self._layer

    def getNet(self) -> Net:
        return self._net

    def getPin(self) -> Pin:
        return self._pin

    def setPin(self, pin: Pin) -> None:
        if self._pin is not None:
            raise Exception("Shape already associated to a pin")

        self._pin = pin

    @property
    def bbox(self):
        """
        The bounding box for this Shape

        """
        return self.getBBox()

    @property
    def layer(self):
        """
        The Layer associated with this Shape

        """
        return self.getLayer()
