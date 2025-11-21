# Copyright 2024 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Original file changed by IHP PDK Authors 2025
# Adopting the Skywater PDK sky130_pcell_templates.py 
# file to the IHP SG13G2 technology
# 

import re

templates = [
    {
        "regex": re.compile(
            r"^.*sg13_lv_nmos(?=.*w=(?P<w>\d+(\.\d+)?u))(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*ng=(?P<ng>\d+))(?=.*m=(?P<m>\d+))(?!.*rfmode).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "nmos",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "ng",
                "type": "int",
            },
            {
                "name": "m",
                "type": "int",
            },
        ],
        "default_params": {"w": "0.13u", "l": "0.13u", "ng": 1, "m": 1},
    },  # Your updated template for sg13_lv_nmos
    {
        "regex": re.compile(
            r"^.*sg13_lv_pmos(?=.*w=(?P<w>\d+(\.\d+)?u))(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*ng=(?P<ng>\d+))(?=.*m=(?P<m>\d+))(?!.*rfmode).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "pmos",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "ng",
                "type": "int",
            },
            {
                "name": "m",
                "type": "int",
            },
        ],
        "default_params": {"w": "0.13u", "l": "0.13u", "ng": 1, "m": 1},
    },
    {
        "regex": re.compile(
            r"^.*sg13_hv_nmos(?=.*w=(?P<w>\d+(\.\d+)?u))(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*ng=(?P<ng>\d+))(?=.*m=(?P<m>\d+))(?!.*rfmode).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "nmosHV",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "ng",
                "type": "int",
            },
            {
                "name": "m",
                "type": "int",
            },
        ],
        "default_params": {"w": "0.3u", "l": "0.4u", "ng": 1, "m": 1},
    },
    {
        "regex": re.compile(
            r"^.*sg13_hv_pmos(?=.*w=(?P<w>\d+(\.\d+)?u))(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*ng=(?P<ng>\d+))(?=.*m=(?P<m>\d+))(?!.*rfmode).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "pmosHV",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "ng",
                "type": "int",
            },
            {
                "name": "m",
                "type": "int",
            },
        ],
        "default_params": {"w": "0.3u", "l": "0.45u", "ng": 1, "m": 1},
    },
    {
        "regex": re.compile(
            r"^.*sg13_lv_nmos(?=.*w=(?P<w>\d+(\.\d+)?u))(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*ng=(?P<ng>\d+))(?=.*m=(?P<m>\d+))(?=.*rfmode=(?P<rfmode>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "rfnmos",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "ng",
                "type": "int",
            },
            {
                "name": "m",
                "type": "int",
            },
            {
                "name": "rfmode",
                "type": "int",
            },
        ],
        "default_params": {
            "w": "1.0u",
            "l": "0.72u",
            "ng": 1,
            "m": 1,
            "rfmode": 1,
        },
    },
    {
        "regex": re.compile(
            r"^.*sg13_lv_pmos(?=.*w=(?P<w>\d+(\.\d+)?u))(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*ng=(?P<ng>\d+))(?=.*m=(?P<m>\d+))(?=.*rfmode=(?P<rfmode>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "rfpmos",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "ng",
                "type": "int",
            },
            {
                "name": "m",
                "type": "int",
            },
            {
                "name": "rfmode",
                "type": "int",
            },
        ],
        "default_params": {
            "w": "1.0u",
            "l": "0.72u",
            "ng": 1,
            "m": 1,
            "rfmode": 1,
        },
    },
    {
        "regex": re.compile(
            r"^.*sg13_hv_nmos(?=.*w=(?P<w>\d+(\.\d+)?u))(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*ng=(?P<ng>\d+))(?=.*m=(?P<m>\d+))(?=.*rfmode=(?P<rfmode>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "rfnmosHV",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "ng",
                "type": "int",
            },
            {
                "name": "m",
                "type": "int",
            },
            {
                "name": "rfmode",
                "type": "int",
            },
        ],
        "default_params": {
            "w": "1.0u",
            "l": "0.72u",
            "ng": 1,
            "m": 1,
            "rfmode": 1,
        },
    },
    {
        "regex": re.compile(
            r"^.*sg13_hv_pmos(?=.*w=(?P<w>\d+(\.\d+)?u))(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*ng=(?P<ng>\d+))(?=.*m=(?P<m>\d+))(?=.*rfmode=(?P<rfmode>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "rfpmosHV",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "ng",
                "type": "int",
            },
            {
                "name": "m",
                "type": "int",
            },
            {
                "name": "rfmode",
                "type": "int",
            },
        ],
        "default_params": {
            "w": "1.0u",
            "l": "0.72u",
            "ng": 1,
            "m": 1,
            "rfmode": 1,
        },
    },
    {
        "regex": re.compile(r"^.*bondpad(?=.*size=(?P<size>\d+(\.\d+)?u)).*$"),
        "pcell_library": "SG13_dev",
        "pcell_name": "bondpad",
        "params": [
            {
                "name": "size",
                "type": "string",
            }
        ],
        "default_params": {"size": "80u"},
    },
    {
        "regex": re.compile(
            r"^.*cap_cmim(?=.*w=(?P<w>\d+(\.\d+)?e-?\d+))(?=.*l=(?P<l>\d+(\.\d+)?e-?\d+))(?=.*m=(?P<m>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "cmim",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "m",
                "type": "int",
            },
        ],
        "default_params": {"w": "7.0e-6", "l": "7.0e-6", "m": 1},
    },
    {
        "regex": re.compile(
            r"^.*cap_rfcmim(?=.*w=(?P<w>\d+(\.\d+)?e-?\d+))(?=.*l=(?P<l>\d+(\.\d+)?e-?\d+))(?=.*wfeed=(?P<wfeed>\d+(\.\d+)?e-?\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "rfcmim",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "wfeed",
                "type": "string",
            },
        ],
        "default_params": {"w": "10.0e-6", "l": "10.0e-6", "wfeed": "5.0e-6"},
    },
    {
        "regex": re.compile(
            r"^.*dantenna(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*w=(?P<w>\d+(\.\d+)?u)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "dantenna",
        "params": [
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "w",
                "type": "string",
            },
        ],
        "default_params": {"l": "0.78u", "w": "0.78u"},
    },
    {
        "regex": re.compile(
            r"^.*dpantenna(?=.*l=(?P<l>\d+(\.\d+)?u))(?=.*w=(?P<w>\d+(\.\d+)?u)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "dpantenna",
        "params": [
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "w",
                "type": "string",
            },
        ],
        "default_params": {"l": "0.78u", "w": "0.78u"},
    },
    {
        "regex": re.compile(
            r"^.*npn13G2(?=.*\bNx=(?P<Nx>\d+)\b)(?!.*\bEl=).*"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "npn13G2",
        "params": [
            {
                "name": "Nx",
                "type": "int",
            }
        ],
        "default_params": {"Nx": 1},
    },
    {
        "regex": re.compile(
            r"^.*npn13G2l(?=.*\bNx=(?P<Nx>\d+)\b)(?=.*\bEl=(?P<El>\d+(\.\d+)?)).*"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "npn13G2L",
        "params": [
            {
                "name": "Nx",
                "type": "int",
            },
            {
                "name": "El",
                "type": "float",
            },
        ],
        "default_params": {"Nx": 1, "El": 1.0},
    },
    {
        "regex": re.compile(
            r"^.*npn13G2v(?=.*\bNx=(?P<Nx>\d+)\b)(?=.*\bEl=(?P<El>\d+)).*"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "npn13G2V",
        "params": [
            {
                "name": "Nx",
                "type": "int",
            },
            {
                "name": "El",
                "type": "int",
            },
        ],
        "default_params": {"Nx": 1, "El": 1},
    },
    {
        "regex": re.compile(
            r"^.*ntap1(?=.*R=(?P<R>\d+(\.\d+)?))(?=.*w=(?P<w>\d+(\.\d+)?e-?\d+))(?=.*l=(?P<l>\d+(\.\d+)?e-?\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "ntap1",
        "params": [
            {
                "name": "R",
                "type": "float",
            },
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
        ],
        "default_params": {"R": 262.8, "w": "0.78e-6", "l": "0.78e-6"},
    },
    {
        "regex": re.compile(
            r"^.*ptap1(?=.*R=(?P<R>\d+(\.\d+)?))(?=.*w=(?P<w>\d+(\.\d+)?e-?\d+))(?=.*l=(?P<l>\d+(\.\d+)?e-?\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "ptap1",
        "params": [
            {
                "name": "R",
                "type": "float",
            },
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
        ],
        "default_params": {"R": 262.8, "w": "0.78e-6", "l": "0.78e-6"},
    },
    {
        "regex": re.compile(
            r"^.*rhigh(?=.*w=(?P<w>\d+(\.\d+)?e-?\d+))(?=.*l=(?P<l>\d+(\.\d+)?e-?\d+))(?=.*m=(?P<m>\d+))(?=.*b=(?P<b>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "rhigh",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "m",
                "type": "int",
            },
            {
                "name": "b",
                "type": "int",
            },
        ],
        "default_params": {"w": "0.5e-6", "l": "0.5e-6", "m": 1, "b": 0},
    },
    {
        "regex": re.compile(
            r"^.*rppd(?=.*w=(?P<w>\d+(\.\d+)?e-?\d+))(?=.*l=(?P<l>\d+(\.\d+)?e-?\d+))(?=.*m=(?P<m>\d+))(?=.*b=(?P<b>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "rppd",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "m",
                "type": "int",
            },
            {
                "name": "b",
                "type": "int",
            },
        ],
        "default_params": {"w": "0.5e-6", "l": "0.5e-6", "m": 1, "b": 0},
    },
    {
        "regex": re.compile(
            r"^.*rsil(?=.*w=(?P<w>\d+(\.\d+)?e-?\d+))(?=.*l=(?P<l>\d+(\.\d+)?e-?\d+))(?=.*m=(?P<m>\d+))(?=.*b=(?P<b>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "rsil",
        "params": [
            {
                "name": "w",
                "type": "string",
            },
            {
                "name": "l",
                "type": "string",
            },
            {
                "name": "m",
                "type": "int",
            },
            {
                "name": "b",
                "type": "int",
            },
        ],
        "default_params": {"w": "0.5e-6", "l": "0.5e-6", "m": 1, "b": 0},
    },
    {
        "regex": re.compile(
            r"^.*sg13_hv_svaricap(?=.*W=(?P<W>\d+(\.\d+)?e-?\d+))(?=.*L=(?P<L>\d+(\.\d+)?e-?\d+))(?=.*Nx=(?P<Nx>\d+)).*$"
        ),
        "pcell_library": "SG13_dev",
        "pcell_name": "SVaricap",
        "params": [
            {
                "name": "W",
                "type": "string",
            },
            {
                "name": "L",
                "type": "string",
            },
            {
                "name": "Nx",
                "type": "int",
            },
        ],
        "default_params": {"W": "3.74e-6", "L": "0.3e-6", "Nx": 1},
    },
    ###################################################################
    {
        "regex": re.compile(r"^.*diodevdd_2kv(?=.*m=(?P<m>\d+)).*$"),
        "pcell_library": "SG13_dev",
        "pcell_name": "esd",
        "params": [
            {
                "name": "m",
                "type": "int",
            }
        ],
        "default_params": {"model": "diodevdd_2kv", "m": 1},
    },
    {
        "regex": re.compile(r"^.*diodevdd_4kv(?=.*m=(?P<m>\d+)).*$"),
        "pcell_library": "SG13_dev",
        "pcell_name": "esd",
        "params": [
            {
                "name": "m",
                "type": "int",
            }
        ],
        "default_params": {"model": "diodevdd_4kv", "m": 1},
    },
    {
        "regex": re.compile(r"^.*diodevss_2kv(?=.*m=(?P<m>\d+)).*$"),
        "pcell_library": "SG13_dev",
        "pcell_name": "esd",
        "params": [
            {
                "name": "m",
                "type": "int",
            }
        ],
        "default_params": {"model": "diodevss_2kv", "m": 1},
    },
    {
        "regex": re.compile(r"^.*diodevss_4kv(?=.*m=(?P<m>\d+)).*$"),
        "pcell_library": "SG13_dev",
        "pcell_name": "esd",
        "params": [
            {
                "name": "m",
                "type": "int",
            }
        ],
        "default_params": {"model": "diodevss_4kv", "m": 1},
    },
    {
        "regex": re.compile(r"^.*nmoscl_2(?=.*m=(?P<m>\d+)).*$"),
        "pcell_library": "SG13_dev",
        "pcell_name": "esd",
        "params": [
            {
                "name": "m",
                "type": "int",
            }
        ],
        "default_params": {"model": "nmoscl_2", "m": 1},
    },
    {
        "regex": re.compile(r"^.*nmoscl_4(?=.*m=(?P<m>\d+)).*$"),
        "pcell_library": "SG13_dev",
        "pcell_name": "esd",
        "params": [
            {
                "name": "m",
                "type": "int",
            }
        ],
        "default_params": {"model": "nmoscl_4", "m": 1},
    },
]
