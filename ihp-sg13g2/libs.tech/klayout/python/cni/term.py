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
from typing import List

from cni.termtype import TermType
from cni.net import Net

class Term(object):
    """
    Creates a Term terminal object in the current design, using the termName parameter to name this
    newly created Term object. If there is already a net in the current design having the same name
    as this terminal, then this net will be connected to this terminal. Otherwise, a new net will be
    created, and connected to this terminal, using this termName string to name this newly created
    net. If the termName string parameter is empty, or is the name of an existing terminal in the
    design, then an exception is raised. In addition, the termType parameter is used to specify the
    terminal type for this terminal.

    :param termName: name of the new terminal
    :type termName: string
    :param termType: optional type of the new terminal
    :type termType: Termtype

    """

    def __init__(self, termName: str, termType: TermType = TermType.INPUT_OUTPUT):
        import cni.dlo
        impl = cni.dlo.PyCellContext.getCurrentPyCellContext().impl

        if termName == "":
            raise Exception("Empty terminal name given")

        if impl.hasTerm(termName):
            raise Exception(f"Term {termName} already defined")

        self._name = termName
        self._type = termType
        self._pins = []
        self._net = None

        if impl.hasNet(termName):
            self._net = impl.findNet(termName)
        else:
            self._net = Net(termName)

    def addPin(self, pin: Pin) -> None:
        self._pins.append(pin)

    def getName(self) -> str:
        """
        Returns the name for this terminal.

        :return: The name of the terminal
        :rtype: string

        """
        return self._name

    def getNet(self) -> Net:
        """
        Returns the net associated with this Term terminal object. If there is no associated net,
        then an exception is raised.

        :return: The associated net
        :rtype: Net

        """
        if self._net is None:
            raise Exception(f"No net associated for terminal {termName}")

        return self._net

    def getPins(self) -> list[Pin]:
        """
        Returns a uniform list of all of the Pin objects associated with this Term terminal object.

        :return: List of Pin
        :rtype: list[Pin]
        """
        return self._pins

    def setName(self, name: str) -> None:
        """
        Sets the name for this terminal. Note that the name of the associated net for this terminal
        is also changed to have the same name as this terminal. This is done in order to ensure that
        any net connected to this terminal will always have the same name as this terminal. If this
        name string parameter is empty, or is the name of an existing terminal or net in the design,
        then an exception is raised.

        :param name: The name of the terminal
        :type name: string

        """

        import cni.dlo
        impl = cni.dlo.PyCellContext.getCurrentPyCellContext().impl

        if name == "" or impl.hasTerm(name):
            raise Exception(f"Term {name} already defined")
        self._name = name

    @property
    def name(self):
        """
        Returns the name of this terminal

        """
        return self.getName()

    @name.setter
    def name(self, value):
        """
        Sets the name of this terminal

        """
        self.setName(value)


