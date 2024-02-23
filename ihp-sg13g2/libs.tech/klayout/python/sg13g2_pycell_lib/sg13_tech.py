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

from cni.dlo import TechImpl
from cni.dlo import Tech

import os
import json

class SG13_Tech(TechImpl):

    def __init__(self):
        self._techParams = {}

        # TODO: more generic acquisition of tech file name
        techFilePath = os.path.join(os.path.dirname(__file__), "sg13g2_tech.json")

        with open(techFilePath, "r") as tech_file:
            jsData = json.load(tech_file)
            self._techParams = jsData["Parameters"]

            layers = jsData["Layers"]
            self._layers = {}
            for key, value in layers.items():
                layer, dataType = value.split(',')
                self._layers[key] = (int(layer.strip()), int(dataType.strip()))

    def name(self):
        return "SG13_dev"

    def getGridResolution(self):
        return 0.0

    def getTechParams(self):
        return self._techParams

    def stream_layers(self):
        return self._layers


# Make this class known to the system
Tech.register(SG13_Tech())

