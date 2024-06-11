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

from cni.signaltype import SignalType

class Net(object):
    """
    Creates a Net object in the current design, using the netName parameter to name this newly
    created Net object. If this netName string parameter is empty, or is the name of anexisting net
    in the design, then an exception is raised. In addition, the sigType parameter is used to
    specify the signal type for this net, and the isGlobal Boolean flag parameter should be set to
    True, when this net is a global net for the current design.

    :param netName: name of the new net
    :type netName: string
    :param sigType: optional signal type of the new net
    :type sigType: SignalType

    """

    def __init__(self, netName: str, sigType: SignalType = SignalType.SIGNAL, isGlobal: bool = False):
        import cni.dlo
        impl = cni.dlo.PyCellContext.getCurrentPyCellContext().impl

        if netName == "":
            raise Exception("Empty net name given")

        if impl.hasNet(netName):
            raise Exception(f"Net {netName} already defined")


        self._name = netName
        self._type = sigType
        self._terminal = None
        self._isGlobal = isGlobal

    def addTerm(self, term: Term) -> None:
        self._terminal = term

    def getName(self) -> str:
        """
        Returns the name for this Net.

        :return: The name of the Net
        :rtype: string

        """
        return self._name

    def getPins(self) -> list[Pin]:
        """
        Returns a list of pins which are connected to any terminal associated with this Net object.
        All Pin objects associated with this terminal are returned in this list.

        :return: List of Pin
        :rtype: list[Pin]
        """
        if self._terminal is not None:
            return self._terminal.getPins()
        else:
            pins = []
            return pins

    def setName(self, name: str) -> None:
        """
        Sets the name for this Net object. Note that the name of any associated terminal for this
        Net will also be changed to use this new name. This is done in order to ensure that any
        terminal connected to a net will always have the same name as the net. If this name string
        parameter is empty, or is the name of an existing net or terminal in the current design,
        then an exception is raised.

        :param name: The name of the net
        :type name: string

        """

        import cni.dlo
        impl = cni.dlo.PyCellContext.getCurrentPyCellContext().impl

        if name == "" or impl.hasNet(name):
            raise Exception(f"Net {name} already defined")
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


