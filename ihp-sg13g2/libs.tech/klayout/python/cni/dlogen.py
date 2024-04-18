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

import pya

class Dlo(object):

    def __init__(self, libName, cellName, viewName='layout', viewType=None):
        pass

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


class DloGen(Dlo):

    _libName = ''

    def __init__(self):
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

    def addPin(self, name, label, box, layer):
        # simply creates a shape - needs to support other shape types?
        Rect(layer, box)


