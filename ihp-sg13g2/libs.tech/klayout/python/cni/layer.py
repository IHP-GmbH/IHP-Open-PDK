########################################################################
#
# Copyright 2023 IHP PDK Authors
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

class Layer(object):

    tech = None
    layout = None

    def __init__(self, name, purpose = None):
        namePurpose = name if purpose is None else name + "." + purpose
        layer, datatype = Layer.tech.stream_layers()[namePurpose]

        self._name = namePurpose
        self._number = Layer.layout.layer(layer, datatype, namePurpose)
        self._purposeName = "" if purpose is None else purpose

    def getAttrs(self):
        raise Exception("Not implemented yet!")

    def getGridResolution(self):
        raise Exception("Not implemented yet!")

    def getLayerAbove(self):
        raise Exception("Not implemented yet!")

    def getLayerAbove(self, layerMaterial):
        raise Exception("Not implemented yet!")

    def getLayerBelow(self):
        raise Exception("Not implemented yet!")

    def getLayerBelow(self, layerMaterial):
        raise Exception("Not implemented yet!")

    def getLayerName(self):
        return self._name

    def getLayerNumber(self):
        return self._number

    def getMaterial(self):
        raise Exception("Not implemented yet!")

    def getPurposeName(self):
        raise Exception("Not implemented yet!")

    def getPurposeNumber(self):
        raise Exception("Not implemented yet!")

    def getRoutingDir(self):
        raise Exception("Not implemented yet!")

    def isAbove(self, layer):
        raise Exception("Not implemented yet!")

    def isMaskLayer(self):
        raise Exception("Not implemented yet!")

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @property
    def purposeName(self):
        return self._purposeName

    @property
    def purposeNumber(self):
        raise Exception("Not implemented yet!")



