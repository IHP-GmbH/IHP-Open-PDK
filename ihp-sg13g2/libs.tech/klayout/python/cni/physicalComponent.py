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
from abc import ABC, abstractmethod
from cni.ulist import *
from cni.namemapper import NameMapper
from cni.transform import Transform

import pya

class PhysicalComponent(ABC):

    @abstractmethod
    def addToRegion(self, region: pya.Region):
        pass

    @abstractmethod
    def clone(self, nameMap : NameMapper = NameMapper(), netMap : NameMapper = NameMapper()):
        pass

    def fgOr(self, component: PhysicalComponent, resultLayer: Layer) -> Grouping:
        components1 = ulist[PhysicalComponent]()
        components1.append(self)

        components2 = ulist[PhysicalComponent]()
        components2.append(component)

        import cni.geo
        return cni.geo.fgOr(components1, components2, resultLayer)

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def moveBy(self, dx: float, dy: float) -> None:
        pass

    @abstractmethod
    def transform(self, transform: Transform) -> None:
        pass
