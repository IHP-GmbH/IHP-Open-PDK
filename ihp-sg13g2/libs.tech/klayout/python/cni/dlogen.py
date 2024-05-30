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

from cni.rect import *
from cni.dlo import *
from cni.grouping import *
from cni.pin import *
from cni.term import *

import pya

class Dlo(object):

    def __init__(self, libName, cellName, viewName='layout', viewType=None):
        self._pins = {}
        self._terms = {}

    @classmethod
    def exists(cls, dloName : str) -> bool:
        """
        Returns True if the dloName Dlo design object exists, and False
        otherwise. The dloName is a string of the form “<libName>/<cellName>/<viewName>”.
        If <viewName> is not specified, then the default value “layout” will be used.

        :param dloName: name of dlo object
        :type dloName: str
        :return: wether cell exists
        :rtype: bool

        """
        libName = ''
        cellName = ''
        viewName = 'layout'

        strings = dloName.split('/')

        if len(strings) >= 1:
            libName = strings[0]
        if len(strings) >= 2:
            cellName = strings[1]
        if len(strings) >= 3:
            viewName = strings[2]

        if libName == '':
            pya.Logger.warn(f"Dlo.exists: no libName given!")
            return False

        if cellName == '':
            pya.Logger.warn(f"Dlo.exists: no cellName given!")
            return False

        if viewName == '':
            pya.Logger.warn(f"Dlo.exists: no viewName given!")
            return False

        lib = pya.Library.library_by_name(libName)
        if lib is None:
            pya.Logger.warn(f"Dlo.exists: library '{libName}' don't exists!")
            return False

        if viewName != 'layout':
            pya.Logger.warn(f"Dlo.exists: view '{viewName}' not exists in library {libName}!")
            return False

        if not lib.layout().has_cell(cellName):
            pya.Logger.warn(f"Dlo.exists: cell '{cellName}' don't exists in library '{libName}'!")
            return False

        return True

    def findPin(self, name: str) -> Pin:
        if name == "":
            if len(self._pins) != 0:
                return next(iter(self._pins))
            else:
                raise Exception(f"No pins defined")
        else:
            if name in self._pins:
                return self._pins[name]
            else:
                raise Exception(f"Pin '{name}' don't exists")


    def hasPin(self, name: str) -> bool:
        return name in self._pins

    def hasTerm(self, name: str) -> bool:
        return name in self._terms

    def findTerm(self, name: str) -> Term:
        if name == "":
            if len(self._terms) != 0:
                return next(iter(self._terms))
            else:
                raise Exception(f"No terminals defined")
        else:
            if name in self._terms:
                return self._terms[name]
            else:
                raise Exception(f"Terminal '{name}' don't exists")


class DloGen(Dlo):

    _libName = ''

    def __init__(self):
        super(DloGen, self).__init__('', '')
        self.tech = None
        self.props = {}

    @classmethod
    def setLibName(cls, libName: str) -> None:
        cls._libName = libName

    @classmethod
    def getLibName(cls) -> str:
        if cls._libName == '':
            raise Exception("Library name not set!")
        return cls._libName

    def setTech(self, tech):
        self.tech = tech

    def addPin(self, pinName : str, termName: str, box : Box, layer: Layer) -> Pin:
        pin = Pin(pinName, termName)
        self._pins[pinName] = pin

        if not self.hasTerm(termName):
            self._terms[termName] = pin.getTerm()

        pin.setBBox(box, layer)

        return pin


