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
from cni.grouping import *
from cni.pin import *
from cni.term import *

import pya

class Dlo(object):

    class _CellContext:
        def __init__(self):
            self.pins = {}
            self.terms = {}
            self.nets = {}


    def __init__(self, libName, cellName, viewName='layout', viewType=None):
        self._cellContexts = {}

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
        cellContext = self._getCurrentCellContext()

        if name == "":
            if len(cellContext.pins) != 0:
                return next(iter(cellContext.pins))
            else:
                raise Exception(f"No pins defined")
        else:
            if name in cellContext.pins:
                return cellContext.pins[name]
            else:
                raise Exception(f"Pin '{name}' don't exists")


    def hasPin(self, name: str) -> bool:
        cellContext = self._getCurrentCellContext()
        return name in cellContext.pins

    def hasTerm(self, name: str) -> bool:
        cellContext = self._getCurrentCellContext()
        return name in cellContext.terms

    def hasNet(self, name: str) -> bool:
        cellContext = self._getCurrentCellContext()
        return name in cellContext.nets

    def findTerm(self, name: str) -> Term:
        cellContext = self._getCurrentCellContext()

        if name == "":
            if len(cellContext.terms) != 0:
                return next(iter(cellContext.terms))
            else:
                raise Exception(f"No terminals defined")
        else:
            if name in cellContext.terms:
                return cellContext.terms[name]
            else:
                raise Exception(f"Terminal '{name}' don't exists")

    def _getCurrentCellContext(self):
        import cni.dlo
        cell = cni.dlo.PyCellContext.getCurrentPyCellContext().cell
        cellContext = self._cellContexts.get(cell)

        if cellContext is None:
            raise Exception("No current cell context")

        return cellContext

    def addCellContext(self, cell):
        if cell in self._cellContexts:
            self._cellContexts.pop(cell)

        self._cellContexts[cell] = Dlo._CellContext()


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

        cellContext = self._getCurrentCellContext()
        cellContext.pins[pinName] = pin

        term = pin.getTerm()
        if not self.hasTerm(termName):
            cellContext.terms[termName] = term

        # Note: The net associated with a terminal has the same name.
        net = term.getNet()
        if not self.hasNet(termName):
            cellContext.nets[termName] = net

        pin.setBBox(box, layer)

        return pin


