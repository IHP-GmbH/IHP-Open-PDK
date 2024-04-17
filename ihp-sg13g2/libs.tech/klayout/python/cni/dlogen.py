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

class Dlo(object):

    def __init__(self, libName, cellName, viewName='layout', viewType=None):
        pass

    @classmethod
    def exists(cls, dloName) -> bool:
        return False


class DloGen(Dlo):

    def __init__(self):
        self.tech = None
        self.props = {}

    def set_tech(self, tech):
        self.tech = tech

    def addPin(self, name, label, box, layer):
        # simply creates a shape - needs to support other shape types?
        Rect(layer, box)


