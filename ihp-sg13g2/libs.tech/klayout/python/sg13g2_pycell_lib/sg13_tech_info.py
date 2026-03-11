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
import os
from typing import *

from .ihp.geometry import *


NX = int
NY = int
LayerName = str
ViaName = str
SpaceLambda = Callable[[NX, NY], Tuple[float, float]]


@dataclass(frozen=True)
class LayerInfo:
    gds_layer: int
    gds_datatype: int
    name: str


@dataclass
class ViaInfo:
    name: str
    description: str
    bottom: LayerInfo 
    cut: LayerInfo
    top: LayerInfo
    bottom_grid: float
    top_grid: float
    wbmin: float
    hbmin: float
    wtmin: float
    htmin: float
    enc_bottom: float
    enc_endcap_bottom: float
    enc_top: float
    enc_endcap_top: float
    width: float
    space_lambda: SpaceLambda
    
    def enc_bottom_for_nx_ny(self, nx: int, ny: int) -> (float, float):
        if nx < ny:
            return (self.enc_bottom, self.enc_endcap_bottom)
        else:
            return (self.enc_endcap_bottom, self.enc_bottom)

    def enc_top_for_nx_ny(self, nx: int, ny: int) -> (float, float):
        if nx < ny:
            return (self.enc_top, self.enc_endcap_top)
        else:
            return (self.enc_endcap_top, self.enc_top)


@dataclass
class ViaArrayInfo:
    via: ViaInfo
    nx: int
    ny: int
    
    @cached_property
    def enc_bottom(self) -> (float, float):
        if self.nx < self.ny:
            return (self.via.enc_bottom, self.via.enc_endcap_bottom)
        else:
            return (self.via.enc_endcap_bottom, self.via.enc_bottom)

    @cached_property
    def enc_top(self) -> (float, float):
        if self.nx < self.ny:
            return (self.via.enc_top, self.via.enc_endcap_top)
        else:
            return (self.via.enc_endcap_top, self.via.enc_top)

    @cached_property
    def space(self) -> (float, float):    
        return self.via.space_lambda(self.nx, self.ny)

    @cached_property
    def size(self) -> (float, float):   
        """
        Size of the array without enclosure
        """
        space_x, space_y = self.space
        array_w = (self.nx * self.via.width + (self.nx - 1) * space_x)
        array_h = (self.ny * self.via.width + (self.ny - 1) * space_y)
        return array_w, array_h
    
    def each_via_box(self) -> Iterator[Box]:
        space_x, space_y = self.space
        array_w, array_h = self.size
        for i in range(self.nx):
            x0 = i * space_x + i * self.via.width - array_w/2
            for j in range(self.ny):
                y0 = j * space_y + j * self.via.width - array_h/2
                yield Box(x0, y0, x0 + self.via.width, y0 + self.via.width)

    @staticmethod
    def ensure_min_size_rules(box: Box, min_width: float, min_height: float) -> Box:
        w = box.right - box.left
        h = box.top - box.bottom

        center_x = box.left + w/2
        center_y = box.bottom + h/2

        if w < min_width:
            w = min_width
        if h < min_height:
            h = min_height
            
        return Box(center_x - w/2,
                   center_y - h/2,
                   center_x + w/2,
                   center_y + h/2)
    
    def bottom_metal_box(self, via_array_below: Optional[ViaArrayInfo]) -> Box:
        enc_bot_x, enc_bot_y = self.enc_bottom
        
        via_arr_w, via_arr_h = self.size
        met_bot_w = via_arr_w + enc_bot_x*2
        met_bot_h = via_arr_h + enc_bot_y*2
        
        bottom_layer_box = Box(-met_bot_w/2,
                               -met_bot_h/2,
                               met_bot_w/2,
                               met_bot_h/2)
                               
        if via_array_below is not None:
            previous_top_metal_box = via_array_below.top_metal_box()
            bottom_layer_box = Box(min(bottom_layer_box.left, previous_top_metal_box.left),
                                   min(bottom_layer_box.bottom, previous_top_metal_box.bottom),
                                   max(bottom_layer_box.right, previous_top_metal_box.right),
                                   max(bottom_layer_box.top, previous_top_metal_box.top))
        bottom_layer_box = self.ensure_min_size_rules(bottom_layer_box, self.via.wbmin, self.via.hbmin)
        return bottom_layer_box

    def top_metal_box(self) -> Box:
        enc_top_x, enc_top_y = self.enc_top
        via_arr_w, via_arr_h = self.size
        met_bot_w = via_arr_w + enc_top_x*2
        met_bot_h = via_arr_h + enc_top_y*2
        top_layer_box = Box(-met_bot_w/2,
                            -met_bot_h/2,
                            met_bot_w/2,
                            met_bot_h/2)
        top_layer_box = self.ensure_min_size_rules(top_layer_box, self.via.wtmin, self.via.htmin)
        return top_layer_box


@dataclass
class TechInfo:
    layers: List[LayerInfo]
    vias: List[ViaInfo]

    @classmethod
    def instance(cls) -> TechInfo:
        if not hasattr(cls, '_instance'):
            tech_file_path = os.path.join(os.path.dirname(__file__), 'sg13g2_tech.json')
            js_data: Dict
            with open(tech_file_path, "r") as tech_file:
                js_data = json.load(tech_file)
            tp = js_data['techParams']
        
            layers = [
                LayerInfo(1, 0, 'Activ'),
                LayerInfo(5, 0, 'GatPoly'),
                LayerInfo(6, 0, 'Cont'),
                LayerInfo(8, 0, 'Metal1'),
                LayerInfo(19, 0, 'Via1'),
                LayerInfo(10, 0, 'Metal2'),
                LayerInfo(29, 0, 'Via2'),
                LayerInfo(30, 0, 'Metal3'),
                LayerInfo(49, 0, 'Via3'),
                LayerInfo(50, 0, 'Metal4'),
                LayerInfo(66, 0, 'Via4'),
                LayerInfo(67, 0, 'Metal5'),
                LayerInfo(125, 0, 'TopVia1'),
                LayerInfo(126, 0, 'TopMetal1'),
                LayerInfo(133, 0, 'TopVia2'),
                LayerInfo(134, 0, 'TopMetal2'),
            ]
            ld: Dict[str, LayerInfo] = {l.name: l for l in layers}
            
            grid = 0.005
            
            vias = [
                ViaInfo(name='SG13G2_CONT_GATPOLY_M1', description='Cont (GatPoly→Metal1)', 
                        bottom=ld['GatPoly'], cut=ld['Cont'], top=ld['Metal1'], bottom_grid=grid, top_grid=grid, 
                        wbmin=tp['Cnt_a'], hbmin=tp['Cnt_a'], wtmin=tp['M1_a'], htmin=tp['M1_a'],
                        enc_bottom=tp['Cnt_d'], enc_endcap_bottom=tp['Cnt_d'],
                        enc_top=tp['M1_c'], enc_endcap_top=tp['M1_c1'],
                        width=tp['Cnt_a'],
                        space_lambda=lambda nx, ny: (tp['Cnt_b1'], tp['Cnt_b']) \
                                                    if nx > tp['Cnt_b1_nr'] and ny > tp['Cnt_b1_nr'] \
                                                    else (tp['Cnt_b'], tp['Cnt_b'])
                        ),
                ViaInfo(name='SG13G2_CONT_ACTIV_M1', description='Cont (Activ→Metal1)', 
                        bottom=ld['Activ'], cut=ld['Cont'], top=ld['Metal1'], bottom_grid=grid, top_grid=grid, 
                        wbmin=tp['Cnt_a'], hbmin=tp['Cnt_a'], wtmin=tp['M1_a'], htmin=tp['M1_a'],
                        enc_bottom=tp['Cnt_d'], enc_endcap_bottom=tp['Cnt_d'],
                        enc_top=tp['M1_c'], enc_endcap_top=tp['M1_c1'],
                        width=tp['Cnt_a'], 
                        space_lambda=lambda nx, ny: (tp['Cnt_b1'], tp['Cnt_b']) \
                                                    if nx > tp['Cnt_b1_nr'] and ny > tp['Cnt_b1_nr'] \
                                                    else (tp['Cnt_b'], tp['Cnt_b'])
                        ),
                ViaInfo(name='SG13G2_VIA_M1_M2', description='Via1 (Metal1→Metal2)', 
                        bottom=ld['Metal1'], cut=ld['Via1'], top=ld['Metal2'], bottom_grid=grid, top_grid=grid, 
                        wbmin=tp['M1_a'], hbmin=tp['M1_a'], wtmin=tp['Mn_a'], htmin=tp['Mn_a'],
                        enc_bottom=tp['V1_c'], enc_endcap_bottom=tp['V1_c1'],
                        enc_top=tp['Mn_c'], enc_endcap_top=tp['Mn_c1'],
                        width=tp['V1_a'], 
                        space_lambda=lambda nx, ny: (tp['V1_b1'], tp['V1_b']) \
                                                    if nx > tp['V1_b1_nr'] and ny > tp['V1_b1_nr'] \
                                                    else (tp['V1_b'], tp['V1_b'])
                        ),
                ViaInfo(name='SG13G2_VIA_M2_M3', description='Via2 (Metal2→Metal3)', 
                        bottom=ld['Metal2'], cut=ld['Via2'], top=ld['Metal3'], bottom_grid=grid, top_grid=grid, 
                        wbmin=tp['Mn_a'], hbmin=tp['Mn_a'], wtmin=tp['Mn_a'], htmin=tp['Mn_a'],
                        enc_bottom=tp['Vn_c'], enc_endcap_bottom=tp['Vn_c1'],
                        enc_top=tp['Mn_c'], enc_endcap_top=tp['Mn_c1'],
                        width=tp['Vn_a'], 
                        space_lambda=lambda nx, ny: (tp['Vn_b1'], tp['Vn_b']) \
                                                    if nx > tp['Vn_b1_nr'] and ny > tp['Vn_b1_nr'] \
                                                    else (tp['Vn_b'], tp['Vn_b'])
                        ),
                ViaInfo(name='SG13G2_VIA_M3_M4', description='Via3 (Metal3→Metal4)', 
                        bottom=ld['Metal3'], cut=ld['Via3'], top=ld['Metal4'], bottom_grid=grid, top_grid=grid, 
                        wbmin=tp['Mn_a'], hbmin=tp['Mn_a'], wtmin=tp['Mn_a'], htmin=tp['Mn_a'],
                        enc_bottom=tp['Vn_c'], enc_endcap_bottom=tp['Vn_c1'],
                        enc_top=tp['Mn_c'], enc_endcap_top=tp['Mn_c1'],
                        width=tp['Vn_a'], 
                        space_lambda=lambda nx, ny: (tp['Vn_b1'], tp['Vn_b']) \
                                                    if nx > tp['Vn_b1_nr'] and ny > tp['Vn_b1_nr'] \
                                                    else (tp['Vn_b'], tp['Vn_b'])
                        ),
                ViaInfo(name='SG13G2_VIA_M4_M5', description='Via4 (Metal4→Metal5)', 
                        bottom=ld['Metal4'], cut=ld['Via4'], top=ld['Metal5'], bottom_grid=grid, top_grid=grid, 
                        wbmin=tp['Mn_a'], hbmin=tp['Mn_a'], wtmin=tp['Mn_a'], htmin=tp['Mn_a'],
                        enc_bottom=tp['Vn_c'], enc_endcap_bottom=tp['Vn_c1'],
                        enc_top=tp['Mn_c'], enc_endcap_top=tp['Mn_c1'],
                        width=tp['Vn_a'], 
                        space_lambda=lambda nx, ny: (tp['Vn_b1'], tp['Vn_b']) \
                                                    if nx > tp['Vn_b1_nr'] and ny > tp['Vn_b1_nr'] \
                                                    else (tp['Vn_b'], tp['Vn_b'])
                    ),
                ViaInfo(name='SG13G2_VIA_M5_TM1', description='TopVia1 (Metal5→TopMetal1)', 
                        bottom=ld['Metal5'], cut=ld['TopVia1'], top=ld['TopMetal1'], bottom_grid=grid, top_grid=grid, 
                        wbmin=tp['Mn_a'], hbmin=tp['Mn_a'], wtmin=tp['TM1_a'], htmin=tp['TM1_a'],
                        enc_bottom=tp['TV1_c'], enc_endcap_bottom=tp['TV1_c'],
                        enc_top=tp['TV1_d'], enc_endcap_top=tp['TV1_d'],
                        width=tp['TV1_a'], 
                        space_lambda=lambda nx, ny: (tp['TV1_b'], tp['TV1_b'])
                        ),
                ViaInfo(name='SG13G2_VIA_TM1_TM2', description='TopVia2 (TopMetal1→TopMetal2)', 
                        bottom=ld['TopMetal1'], cut=ld['TopVia2'], top=ld['TopMetal2'], bottom_grid=grid, top_grid=grid, 
                        wbmin=tp['TM1_a'], hbmin=tp['TM1_a'], wtmin=tp['TM2_a'], htmin=tp['TM2_a'],
                        enc_bottom=tp['TV2_c'], enc_endcap_bottom=tp['TV2_c'],
                        enc_top=tp['TV2_d'], enc_endcap_top=tp['TV2_d'],
                        width=tp['TV2_a'], 
                        space_lambda=lambda nx, ny: (tp['TV2_b'], tp['TV2_b'])
                        ),
            ]
            
            cls._instance = TechInfo(layers=layers, vias=vias)
        return cls._instance
    
    @cached_property
    def activ(self) -> LayerInfo:
        return self.layers[0]
        
    @cached_property
    def gat_poly(self) -> LayerInfo:
        return self.layers[1]
    
    @cached_property
    def metal1(self) -> LayerInfo:
        return self.layers[3]
    
    @cached_property
    def device_layer_names(self) -> List[LayerName]:
        return [self.activ.name, self.gat_poly.name]
    
    @cached_property
    def first_metal_layer_name(self) -> LayerName:
        return self.metal1.name
    
    #----------------------------------------------- helper methods -------------------------------------------------   
    
    @cached_property
    def via_and_top_layer_by_bottom_layer(self) -> Dict[LayerName, Tuple[ViaName, LayerName]]:
        return {v.bottom.name: (v.name, v.top.name) for v in self.vias}
    
    def layer_by_name(self, name: str) -> LayerInfo:
        try:
            return [l for l in self.layers if l.name == name][0]
        except IndexError:
            raise Exception(f"no layer found named '{name}'")

    def via_by_name(self, name: str) -> ViaInfo:
        try:
            return [v for v in self.vias if v.name == name][0]
        except IndexError:
            raise Exception(f"no via found named '{name}'")

    @cached_property
    def via_layers(self) -> Set[LayerInfo]:
        return {v.cut for v in self.vias}

    @cached_property
    def non_via_layers(self) -> List[LayerInfo]:
        return [l for l in self.layers if not l in self.via_layers]
    
    @cached_property
    def layer_choices(self) -> List[Tuple[str, LayerInfo]]:
        return [(l.name, l) for l in self.non_via_layers]
    
    @cached_property
    def via_choices(self) -> List[Tuple[str, str]]:
        return [(v.description, v.name) for v in self.vias]
    
    def num_stack_steps(self, bot: LayerInfo, top: LayerInfo) -> int:
        bi = self.layers.index(bot)
        ti = self.layers.index(top)
        return ti - bi

    def get_vias(self, bottom: LayerInfo, top: LayerInfo) -> List[Via]:
        bottom_via_found = False
        already_added_cut_layers: Set[LayerInfo] = set()
        vias = []
        for via in self.vias:
            if not bottom_via_found:
                if via.bottom == bottom:
                    vias.append(via)
                    already_added_cut_layers.add(via.cut)
                    bottom_via_found = True
                    
            if bottom_via_found:
                if via.cut not in already_added_cut_layers:
                    vias.append(via)
                
                if via.top == top:
                    break

        return vias

