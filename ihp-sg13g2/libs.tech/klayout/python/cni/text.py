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

from cni.box import *
from cni.shape import *
from cni.rect import *

import pya

class Text(Shape):

    def __init__(self, layer, text, point, size):
        # TODO: size
        text = pya.DText(text, pya.DTrans(point.getX(), point.getY()), 1, 0)

        self._text = text
        self._layer = layer

        self.set_shape(Shape.cell.shapes(layer.number).insert(text))
        super().__init__(Box(text.bbox().left, text.bbox().bottom, text.bbox().right, text.bbox().top))

    def addToRegion(self, region: pya.Region):
        region.insert(self._text)

    def clone(self, nameMap : NameMapper = NameMapper(), netMap : NameMapper = NameMapper()):
        return Text(self._layer, self._text.dup())

    def destroy(self):
        if not self._text._destroyed():
            Shape.cell.shapes(self.getShape().layer).erase(self.getShape())
            self._text._destroy()
        else:
            pya.Logger.warn(f"Text.destroy: already destroyed!")

    def moveBy(self, dx: float, dy: float) -> None:
        movedText = (pya.DTrans(float(dx), float(dy)) * self._text)
        shape = Shape.cell.shapes(self._shape.layer).insert(movedText)
        self.destroy()
        self._polygon = movedPolygon
        self.set_shape(shape)

    def setAlignment(self, align):
        # TODO
        pass

    def setOrientation(self, orient):
        # TODO
        pass

    def setDrafting(self, drafting):
        # TODO
        pass

    def transform(self, transform: Transform) -> None:
        transformedText = self._text.transformed(transform.transform)
        shape = Shape.cell.shapes(self.getShape().layer).insert(transformedText)
        self.destroy()
        self._text = transformedText
        self.set_shape(shape)

