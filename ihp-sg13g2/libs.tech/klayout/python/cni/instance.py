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
from cni.physicalComponent import *
from cni.paramarray import *
from cni.shape import *
from cni.orientation import *
import pya
import sys

class Instance():
    """
    Creates an Instance object, where the dloName parameter specifies the Klayout name to be
    used for this Instance object. The dloName parameter is a string of the form
    “libName/cellName/viewName”, where the libName and the viewName are optional. If the libName
    is not specified, then the library name associated with the current DloGen is used; if the
    viewName is not specified, then the default viewName is used (currently “layout”).

    :param dloName: name of dlo object
    :type dloName: str

    """

    def __init__(self, dloName: str):
        self._instance = None

        libName = ''
        cellName = ''
        viewName = ''

        strings = dloName.split('/')

        if len(strings) >= 1:
            libName = strings[0]
        if len(strings) >= 2:
            cellName = strings[1]
        if len(strings) >= 3:
            viewName = strings[2]

        if libName == '':
            libName = dloGen.getLibName()

        if cellName == '':
            raise Exception("No cellName given!")

        if viewName == '':
            viewName = 'layout'

        lib = pya.Library.library_by_name(libName)
        if lib is None:
            raise Exception(f"Library '{libName}' don't exists!")

        if viewName != 'layout':
            raise Exception(f"View '{viewName}' not exists in library {libName}!")

        cell = lib.layout().cell(cellName)
        if cell is None:
            raise Exception(f"Cell '{cellName}' don't exists in library '{libName}'!")

        self._instance = Shape.getCell().insert(pya.DCellInstArray(cell, pya.DTrans()))

    def getParams(self) -> ParamArray:
        """
        Returns the ParamArray which provides the explicit parameters and values which were used
        when this Instance object was created.

        :return: array of parameters
        :rtype: ParamArray

        """
        return Shape.getCell().pcell_parameters_by_name(self._instance)

    def setParams(self, params: ParamArray) -> None:
        """
        Uses the passed ParamArray params to set the parameter values for this Instance.

        :param params: parameters to set
        :type params: ParamArray

        """
        return Shape.getCell().change_pcell_parameters(self._instance, params)

    def setOrientation(self, orientation: Orientation) -> None:
        """
        Sets the orientation for this Instance.

        :param orientation: orientation to set
        :type orientation: Orientation

        """
        match orientation:
            case Orientation.R0:
                transform = pya.DTrans(0, False)
            case Orientation.R90:
                transform = pya.DTrans(90, False)
            case Orientation.R180:
                transform = pya.DTrans(180, False)
            case Orientation.R270:
                transform = pya.DTrans(270, False)
            case Orientation.MYR90:
                transform = pya.DTrans(90, False) * pya.DTrans.M90
            case Orientation.MXR90:
                transform = pya.DTrans(90, True)
            case Orientation.MY:
                transform = pya.DTrans(0, False) * pya.DTrans.M90
            case Orientation.MX:
                transform = pya.DTrans(0, True)
            case _:
                raise Exception(f"Unknown orientation '{orientation}'")

        Shape.getCell().transform(self._instance, transform)

    def setOrigin(self, point: Point) -> None:
        """
        Sets the Point point parameter to be the origin for this Instance.

        :param point: origin to set
        :type point: Point

        """
        Shape.getCell().transform(self._instance, pya.DTrans(point.x, point.y))

