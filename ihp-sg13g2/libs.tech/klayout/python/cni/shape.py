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
from cni.box import *
from cni.physicalComponent import *

class Shape(PhysicalComponent):

    cell = None

    def __init__(self, bbox = None):
        self._shape = None
        self._bbox = bbox

    def set_shape(self, shape: Shape):
        self._shape = shape

    def getShape(self):
        if self._shape is None:
            raise Exception(f"Shape.getShape no shape set {hex(id(self))}: {hex(id(self._shape))}")
        return self._shape

    def getBBox(self):
        return Box(self._bbox.box.left, self._bbox.box.bottom, self._bbox.box.right, self._bbox.box.top)
