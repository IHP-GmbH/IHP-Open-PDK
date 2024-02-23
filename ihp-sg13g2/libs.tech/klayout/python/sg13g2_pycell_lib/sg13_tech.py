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
            self._techParams = json.load(tech_file)

    def name(self):
        return "SG13_dev"

    def getGridResolution(self):
        return 0.0

    def getTechParams(self):
        return self._techParams

    def stream_layers(self):
        # TODO: placeholder, plan is to use separate tech file
        return {
            "Activ":            (1, 0),
            "Activ.drawing":    (1, 1),
            "Activ.label":      (1, 2),
            "Activ.pin":        (1, 3),
            "Activ.net":        (1, 4),
            "Activ.boundary":   (1, 5),
            "Activ.lvs":        (1, 6),
            "Activ.mask":       (1, 7),
            "Activ.filler":     (1, 8),
            "Activ.nofill":     (1, 9),
            "Activ.OPC":        (1, 10),
            "Activ.iOPC":       (1, 11),
            "Activ.noqrc":      (1, 12),

            "NWell":            (31, 0),
            "NWell.drawing":    (31, 1),
            "NWell.label":      (31, 2),
            "NWell.pin":        (31, 3),
            "NWell.net":        (31, 4),
            "NWell.boundary":   (31, 5),

            "nBuLay":           (32, 0),
            "pSD":              (14, 0),
            "pSD.drawing":      (14, 0),
            "GatPoly":          (5, 0),
            "GatPoly.drawing":  (5, 1),
            "GatPoly.track":    (5, 2),
            "GatPoly.label":    (5, 3),
            "GatPoly.pin":      (5, 4),
            "GatPoly.net":      (5, 5),
            "GatPoly.boundary": (5, 6),
            "GatPoly.filler":   (5, 7),
            "GatPoly.nofill":   (5, 8),
            "GatPoly.OPC":      (5, 9),
            "GatPoly.iOPC":     (5, 10),
            "GatPoly.noqrc":    (5, 11),

            "ThickGateOx":      (44, 0),
            "ThickGateOx.drawing":  (44, 1),

            "Cont":             (6, 0),
            "Cont.drawing":     (6, 0),
            "Cont.grid":        (6, 2),
            "Cont.blockage":    (6, 3),
            "Cont.net":         (6, 4),
            "Cont.boundary":    (6, 5),
            "Cont.OPC":         (6, 6),

            "Metal1":           (8, 0),
            "Metal1.drawing":   (8, 0),
            "Metal1.label":     (8, 1),
            "Metal1.pin":       (8, 2),
            "Metal1.net":       (8, 3),

            "RES":              (24, 0),
            "MIM":              (36, 0),

            "Substrate":        (40, 0),
            "Substrate.drawing":  (40, 0),
            "Substrate.text":   (40, 25),

            "TEXT":             (63, 0),
            "TEXT.drawing":     (63, 0),
            "Metal5":           (67, 0),
            "Metal5.pin":       (67, 2),
            "HeatTrans":        (51, 0),
            "EXTBlock":         (111, 0),
            "TopMetal1":        (126, 0),
            "TopMetal1.pin":    (126, 2),
            "PolyRes":          (128, 0),
            "Vmim":             (129, 0),
        }


# Make this class known to the system
Tech.register(SG13_Tech())

