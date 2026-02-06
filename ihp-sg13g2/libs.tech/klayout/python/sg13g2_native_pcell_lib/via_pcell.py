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
import json
import math
from typing import *

import pya
from .sg13_klayout_tech_info import (
    KTechInfo, 
    KViaInfo, 
    KLayerInfo,
)


class ViaPCell(pya.PCellDeclarationHelper):
    def __init__(self):
        super().__init__()

        self.tech_info = KTechInfo.instance()

        # Endpoints
        self.param("via", self.TypeList, "Via", choices=self.tech_info.via_choices, default='SG13G2_VIA_M1_M2')
        
	 # Optional array override
        self.param("nx", self.TypeInt, "nx", default=1)
        self.param("ny", self.TypeInt, "ny", default=1)

        # Optional plane sizes
        self.param("w_bottom", self.TypeDouble, "Bottom width [µm]",  default=0.0)
        self.param("h_bottom", self.TypeDouble, "Bottom height [µm]", default=0.0)
        self.param("w_top",    self.TypeDouble, "Top width [µm]",     default=0.0)
        self.param("h_top",    self.TypeDouble, "Top height [µm]",    default=0.0)

    def dump_params(self):
        params = []
        for p in self.get_parameters():
            params += [f"{p.name}={getattr(self, p.name, None)}"]
        msg = ', '.join(params)
        print(f"ViaPCell.dump_params: {msg}")

    def callback_impl(self, name: str):
        # print(f"ViaPCell.callback_impl: name={name}. Params: ", end='')
        # self.dump_params()
        pass
    
    # Wire tool support
    def via_types(self): 
        return self.tech_info.klayout_via_types
        
    def display_text_impl(self):
        ## FIXME: for now, KLayout does not support via stacks yet, when using the Path tool with 'o'
        return f"{self.via}"

    def coerce_parameters_impl(self):
        ## FIXME: for now, KLayout does not support via stacks yet, when using the Path tool with 'o'
        return
    
    def can_create_from_shape_impl(self):
        return False
        
    def parameters_from_shape_impl(self): 
        pass
        
    def transformation_from_shape_impl(self): 
        return pya.Trans()

    # Helpers
    def _insert_dbox_centered(self, shapes: pya.Shapes, w: float, h: float):
        shapes.insert(pya.DBox(-0.5*w, -0.5*h, 0.5*w, 0.5*h))
    
    def produce_impl(self):
        vias = [self.tech_info.via_by_name(self.via)]

        nx, ny = self.nx, self.ny
        
        for idx, via in enumerate(vias):
            bottom_ly = self.layout.layer(KLayerInfo(via.bottom).klayout_layer_info)
            top_ly    = self.layout.layer(KLayerInfo(via.top).klayout_layer_info)
            cut_ly    = self.layout.layer(KLayerInfo(via.cut).klayout_layer_info)
            
            v = via.width
            sx, sy = via.space_lambda(nx, ny)
            enc_bot_x, enc_bot_y = via.enc_bottom_for_nx_ny(nx, ny)
            enc_top_x, enc_top_y = via.enc_top_for_nx_ny(nx, ny)
            wcut = nx * v + (nx - 1) * sx
            hcut = ny * v + (ny - 1) * sy
            
            wbot = max(via.wbmin, self.w_bottom if idx == 0 else 0.0,           2.0*enc_bot_x + wcut)
            hbot = max(via.hbmin, self.h_bottom if idx == 0 else 0.0,           2.0*enc_bot_y + hcut)
            wtop = max(via.wtmin, self.w_top    if idx == len(vias)-1 else 0.0, 2.0*enc_top_x + wcut)
            htop = max(via.htmin, self.h_top    if idx == len(vias)-1 else 0.0, 2.0*enc_top_y + hcut)

            self._insert_dbox_centered(self.cell.shapes(bottom_ly), wbot, hbot)
            self._insert_dbox_centered(self.cell.shapes(top_ly),    wtop, htop)

            scut = self.cell.shapes(cut_ly)
            x0 = -0.5 * (nx - 1) * (v + sx)
            y0 = -0.5 * (ny - 1) * (v + sy)
            for ix in range(nx):
                cx = x0 + ix * (v + sx)
                for iy in range(ny):
                    cy = y0 + iy * (v + sy)
                    scut.insert(pya.DBox(cx - 0.5*v, cy - 0.5*v, cx + 0.5*v, cy + 0.5*v))
