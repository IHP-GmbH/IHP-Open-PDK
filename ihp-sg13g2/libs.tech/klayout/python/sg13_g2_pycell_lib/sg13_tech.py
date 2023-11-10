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

            "M1_c1": 0.02,
            "Cnt_a": 0.14,
            "Cnt_b": 0.14,
            "Cnt_c": 0.05,
            "Cnt_d": 0.07,
            "M1_c": 0.05,
            "pSD_c": 0.2,
            "NW_c": 0.4,
            "NW_NBL": 0.6,
            "Gat_c": 0.1,
            "Cnt_f": 0.05,
            "Cnt_c": 0.03,
            "CntB_a1": 0.34,
            "CntB_d": 0.07,
            "pSD_i": 0.2,
            "TGO_c": 0.03,
            "TGO_a": 0.3,
            "TV1_a": 0.42,
            "TV1_b": 0.42,
            "TV1_c": 0.1,
            "TV1_d": 0.42,
        }

    def stream_layers(self):
        # TODO: placeholder, plan is to use separate tech file
        return {
            "Activ":            (1, 0),
            "NWell":            (31, 0),
            "nBuLay":           (32, 0),
            "pSD":              (14, 0),
            "GatPoly":          (5, 0),
            "GatPoly.pin":      (5, 2),
            "ThickGateOx":      (44, 0),
            "Cont":             (6, 0),
            "Metal1":           (8, 0),
            "Metal1.pin":       (8, 2),
            "RES":              (24, 0),
            "MIM":              (36, 0),
            "TEXT":             (40, 0),
            "TEXT.drawing":     (63, 0),
            "Metal5":           (67, 0),
            "Metal5.pin":       (67, 2),
            "HeatTrans":        (51, 0),
            "EXTBlock":         (111, 0),
            "TopMetal1":        (126, 0),
            "TopMetal1.pin":    (126, 2),
            "PolyRes":          (128, 0),
        }


# Make this class known to the system
Tech.register(SG13_Tech())

