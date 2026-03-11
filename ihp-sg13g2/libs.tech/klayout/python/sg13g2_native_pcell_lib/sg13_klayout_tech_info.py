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
from dataclasses import dataclass
from functools import cached_property
from typing import *

import pya

from sg13g2_pycell_lib.sg13_tech_info import (
    TechInfo, 
    ViaInfo, 
    LayerInfo,
)


class KLayerInfo:
    def __init__(self, layer_info: LayerInfo):
        self.layer_info = layer_info

    @cached_property
    def klayout_layer_info(self) -> pya.LayerInfo:
        return pya.LayerInfo(self.layer_info.gds_layer, 
                             self.layer_info.gds_datatype,
                             self.layer_info.name)


class KViaInfo:
    def __init__(self, via_info: ViaInfo):
        self.via_info = via_info
        
    @cached_property
    def klayout_via_type(self) -> pya.ViaType:
        vt = pya.ViaType(self.via_info.name, self.via_info.description)
        vt.bottom = KLayerInfo(self.via_info.bottom).klayout_layer_info
        vt.cut = KLayerInfo(self.via_info.cut).klayout_layer_info
        vt.top = KLayerInfo(self.via_info.top).klayout_layer_info
        vt.bottom_grid = self.via_info.bottom_grid
        vt.top_grid = self.via_info.top_grid
        vt.wbmin = self.via_info.wbmin
        vt.hbmin = self.via_info.hbmin
        vt.wtmin = self.via_info.wtmin
        vt.htmin = self.via_info.htmin
        return vt
        

class KTechInfo:
    def __init__(self, tech_info: TechInfo):
        self.tech_info = tech_info
    
    @classmethod
    def instance(cls) -> KTechInfo:
        if not hasattr(cls, '_instance'):
            cls._instance = KTechInfo(tech_info=TechInfo.instance())
        return cls._instance
    
    @cached_property
    def klayout_via_types(self) -> List[pya.ViaType]:
        kvias = [KViaInfo(via) for via in self.tech_info.vias]
        return [via.klayout_via_type for via in kvias]
    
    @cached_property
    def via_choices(self) -> List[Tuple[str, str]]:
        return [(v.description, v.name) for v in self.tech_info.vias]
    
    def via_by_name(self, name: str) -> ViaInfo:
        return self.tech_info.via_by_name(name)
        
