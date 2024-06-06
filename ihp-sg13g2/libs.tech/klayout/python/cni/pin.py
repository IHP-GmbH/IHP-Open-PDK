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

from cni.shape import Shape
from cni.term import Term
from cni.box import Box
from cni.layer import Layer
from cni.ulist import ulist

import pya

class Pin(object):
    """
    Creates a Pin object for the specified terminal in the current design, using the pinName
    parameter to name this newly created Pin object. If there is already a terminal in the
    current design having the same name as the termName parameter, then this terminal will be
    used to create this Pin object. Otherwise, a new terminal will be created, using this
    termName string to name this newly created terminal. If there is already a pin in the
    current design having the same name as the pinName string parameter, then an exception is
    raised. In addition, the shape parameter can optionally be used to associate a shape object
    with this pin.

    :param pinName: Name of the pin.
    :type pinName: string
    :param termName: second point.
    :type termName: string
    :param shape: optional shape to associate
    :type shape: Shape

    """

    def __init__(self, pinName: str, termName: str, shape: Shape = None):
        self._name = pinName
        self._term = None
        self._bbox = None
        self._shapes = []

        import cni.dlo
        impl = cni.dlo.PyCellContext.getCurrentPyCellContext().impl

        if impl.hasPin(pinName):
            raise Exception(f"Pin {pinName} already defined")

        if impl.hasTerm(termName):
            self._term = impl.findTerm(termName)
        else:
            self._term = Term(termName)

        self._term.addPin(self)

        if shape is not None:
            self._shapes.append(shape)

    @singledispatchmethod
    def addShape(self, arg):
        pass

    @addShape.register
    def _(self, arg: Shape) -> None:
        shapes = ulist[Shape]()
        shapes.append(arg)
        self.addShape(shapes)

    @addShape.register
    def _(self, arg: list) -> None:
        for shape in arg:
            shape.setPin(self)
            self._shapes.append(shape)

    def getName(self) -> str:
        """
        Returns the name for this Pin object.

        :return: pin name
        :rtype: string
        """
        return self._name

    def setBBox(self, box: Box, layer: Layer) -> None:
        self._bbox = box
        text = pya.DText(self._name, pya.DTrans(box.left, box.bottom + (box.top-box.bottom) * 0.05), (box.top-box.bottom) * 0.8, 2)
        Shape.getCell().shapes(layer.number).insert(text)

    def getBBox(self) -> Box:
        return self._bbox

    def setName(self, name: str) -> None:
        """
        Sets the name for this Pin object. If there is already a pin in the current design with the
        same name as the name parameter, an exception is raised.

        :param name: Name to set
        :type name: string
        """

        import cni.dlo
        impl = cni.dlo.PyCellContext.getCurrentPyCellContext().impl

        if impl.hasPin(name):
            raise Exception(f"Pin {name} already defined")
        self._name = name

    def setTerm(self, term: Term) -> None:
        """
        Associates the term terminal with this Pin object. Note that multiple Pin objects may be
        associated with a single terminal.

        :param Term: Terminal to associate
        :type name: Term
        """

        self._term = term

    def getTerm(self) -> Term:
        if self._term is None:
            raise Exception("Pin '{self._name}' has no terminal")
        else:
            return self._term

    @property
    def name(self):
        """
        Returns the name of this pin

        """
        return self.getName()

    @name.setter
    def name(self, value):
        """
        Sets the name of this pin

        """
        self.setName(value)


