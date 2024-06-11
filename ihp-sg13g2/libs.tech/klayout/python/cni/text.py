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
from cni.location import Location
from cni.transform import Transform

import pya

class Text(Shape):

    def __init__(self, layer: Layer, text: str, origin: Point, height: float):
        text = pya.DText(text, pya.DTrans(origin.getX(), origin.getY()), height, 2)

        self._text = text
        self._layer = layer
        self._height = height

        super().__init__(layer, Box(text.bbox().left, text.bbox().bottom, text.bbox().right, text.bbox().top))
        self.set_shape(Shape.getCell().shapes(layer.number).insert(text))

    def addToRegion(self, region: pya.Region):
        region.insert(self._text)

    def clone(self, nameMap : NameMapper = NameMapper(), netMap : NameMapper = NameMapper()):
        return Text(self._layer, self._text.dup())

    def destroy(self):
        if not self._text._destroyed():
            Shape.getCell().shapes(self.getShape().layer).erase(self.getShape())
            self._text._destroy()
        else:
            pya.Logger.warn(f"Text.destroy: already destroyed!")

    def moveBy(self, dx: float, dy: float) -> None:
        movedText = (pya.DTrans(float(dx), float(dy)) * self._text)
        shape = Shape.getCell().shapes(self._shape.layer).insert(movedText)
        self.destroy()
        self._text = movedText
        self.set_shape(shape)

    def setAlignment(self, location: Location) -> None:
        width = len(self._text.string) * self._height

        match location:
            case Location.LOWER_LEFT:
                self._text.halign = pya.HAlign.HAlignLeft
                self._text.valign = pya.VAlign.VAlignBottom
            case Location.CENTER_LEFT:
                self._text.halign = pya.HAlign.HAlignLeft
                self._text.valign = pya.VAlign.VAlignCenter
            case Location.UPPER_LEFT:
                self._text.halign = pya.HAlign.HAlignLeft
                self._text.valign = pya.VAlign.VAlignTop
            case Location.LOWER_CENTER:
                self._text.halign = pya.HAlign.HAlignCenter
                self._text.valign = pya.VAlign.VAlignBottom
            case Location.CENTER_CENTER:
                self._text.halign = pya.HAlign.HAlignCenter
                self._text.valign = pya.VAlign.VAlignCenter
            case Location.UPPER_CENTER:
                self._text.halign = pya.HAlign.HAlignCenter
                self._text.valign = pya.VAlign.VAlignTop
            case Location.LOWER_RIGHT:
                self._text.halign = pya.HAlign.HAlignRight
                self._text.valign = pya.VAlign.VAlignBottom
            case Location.CENTER_RIGHT:
                self._text.halign = pya.HAlign.HAlignRight
                self._text.valign = pya.VAlign.VAlignCenter
            case Location.UPPER_RIGHT:
                self._text.halign = pya.HAlign.HAlignRight
                self._text.valign = pya.VAlign.VAlignTop

        layer = self.getShape().layer

        Shape.getCell().shapes(layer).erase(self.getShape())
        self.set_shape(Shape.getCell().shapes(layer).insert(self._text))

    def setOrientation(self, orient):
        x = self._text.x
        y = self._text.y
        self.moveBy(-x, -y)
        self.transform(Transform(0.0, 0.0, orient))
        self.moveBy(x, y)

    def setDrafting(self, drafting):
        # TODO
        pass

    def transform(self, transform: Transform) -> None:
        transformedText = self._text.transformed(transform.transform)
        shape = Shape.getCell().shapes(self.getShape().layer).insert(transformedText)
        self.destroy()
        self._text = transformedText
        self.set_shape(shape)

