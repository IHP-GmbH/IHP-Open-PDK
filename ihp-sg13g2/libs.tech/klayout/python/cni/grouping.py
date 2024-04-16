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
import pya
import sys

class Grouping(PhysicalComponent):

    def __init__(self, name: str = "", components: PhysicalComponent = None):
        self._name = name
        self._components = []

        if components is not None:
            self._components.add(components)

    def add(self, components: PhysicalComponent) -> None:
        if type(components) is not list:
            self._components.append(components)
        else:
            self._components.extend(components)

    def addToRegion(self, region: pya.Region):
        [component.addToRegion(region) for component in self._components]

    def clone(self, nameMap : NameMapper = NameMapper(), netMap : NameMapper = NameMapper()):
        components = []
        [components.append(component.clone()) for component in self._components]
        return Grouping(self._name, components)

    def destroy(self):
        [component.destroy() for component in self._components]
        self._components.clear()

    def getComps(self) -> list:
        return self._components

    def getComp(self, index: int) -> PhysicalComponent:
        return self._components[index]

    def moveBy(self, dx: float, dy: float) -> None:
        [component.moveBy(dx, dy) for component in self._components]

    def toString(self):
        [component.toString() for component in self._components]

    def transform(self, transform: Transform) -> None:
        [component.transform(transform) for component in self._components]
