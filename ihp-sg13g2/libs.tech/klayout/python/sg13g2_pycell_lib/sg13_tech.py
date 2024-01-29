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


class SG13_Tech(TechImpl):

    def name(self):
        return "SG13_dev"

    def getGridResolution(self):
        return 0.0

    def getTechParams(self):
        return {
            "techName": "SG13G2",
            "CDFVersion": 0,
            "epsilon1": 0.001,
            "epsilon2": 1e-09,
            "Mim_d": 0.36,
            "Mim_c": 0.6,

            "nmos_defL": 0.130e-6,
            "nmos_defW": 0.5e-6,
            "nmos_defNG": 1,
            "nmos_minL": 0.130,
            "nmos_minW": 0.250,

            "pmos_model": "pmos",
            "pmos_defW": "0.15u",
            "pmos_defL": "0.13u",
            "pmos_defNG": "1",
            "pmos_maxNG": "100",
            "pmos_maxW": "10u",
            "pmos_maxL": "10u",
            "pmos_minW": "0.15u",
            "pmos_minL": "0.13u",

            "cmim_model": "cap_cmim",
            "cmim_caspec": "1.5m",
            "cmim_cpspec": "40p",
            "cmim_lwd": "0.01u",
            "cmim_defLW": "6.99u",
            "cmim_minLW": "1.14u",
            "cmim_maxLW": "1m",
            "cmim_minC": "1f",
            "cmim_maxC": "8p",

            "Rsil_a": 0.5,
            "Rsil_b": 0.12,
            "Rsil_c": 0.0,
            "Rsil_d": 0.18,
            "Rsil_e": 0.18,
            "Rsil_f":0.5,
            "rsil_model": "res_rsil",
            "rsil_rspec": "7.0",
            "rsilG2_model": "res_rsil",
            "rsilG2_rspec": "7.0",
            "rsil_rkspec": "0.0",
            "rsil_rzspec": "4.5e-6",
            "rsil_ipspec": "2e3",
            "rsil_lwd": "0.04u",
            "rsilG2_lwd": "0.01u",
            "rsilG2_ikspec": "0.11m",
            "rsilG2_ipspec": "2e3",
            "rsilG2C_ikspec": "0.11m",
            "rsilG2C_ipspec": "2e3",
            "rsilG2C_lwd": "0.01u",
            "rsilG3_lwd": "0.016u",
            "rsil_tc1": "3100e-6",
            "rsil_tc2": "0.3e-6",
            "rsil_rztc1": "1300e-6",
            "rsil_defL": "0.50u",
            "rsil_defW": "0.50u",
            "rsil_defB": "0",
            "rsil_defPS": "0.18u",
            "rsil_minL": "0.50u",
            "rsil_minW": "0.50u",
            "rsil_minB": "0",
            "rsil_minPS": "0.18u",
            "rsil_maxL": "1m",
            "rsil_maxW": "1m",
            "rsil_maxB": "100",
            "rsil_maxPS": "9.99u",
            "rsil_kappa": "1.85",
            "rsil_met_over_cont": 0.03,
            "rsil_cont_to_body": 0.12,

            "grid": 0.005,

            "Cnt_a": 0.16,
            "Cnt_b": 0.18,
            "Cnt_c": 0.07,
            "Cnt_d": 0.07,
            "Cnt_f": 0.11,
            "CntB_a1": 0.34,
            "CntB_d": 0.07,
            "M1_c": 0.0,
            "M1_c1": 0.05,
            "NW_c": 0.31,
            "NW_NBL": 1.0,

            "Gat_a": 0.13,
            "Gat_a1": 0.13,
            "Gat_a2": 0.13,
            "Gat_a3": 0.45,
            "Gat_a4": 0.4,
            "Gat_b": 0.18,
            "Gat_b1": 0.25,
            "Gat_c": 0.18,
            "Gat_d": 0.07,
            "Gat_e": 0.09,
            "Gat_g": 0.16,
            "Gat_g_min": 0.39,

            "pSD_c": 0.18,
            "pSD_i": 0.3,
            "TGO_a": 0.27,
            "TGO_c": 0.34,
            "TV1_a": 0.42,
            "TV1_b": 0.42,
            "TV1_c": 0.1,
            "TV1_d": 0.42,
        }

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

