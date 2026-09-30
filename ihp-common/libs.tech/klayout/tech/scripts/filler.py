# =========================================================================================
# Copyright 2025 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================================

"""Module to automatically apply filler cells to a GDS file and store the result to a
parametrizable output file. This module is required because .lym files cannot alter and save
a GDS file in batch mode.

Every PDK reaches it through its own
<pdk>/libs.tech/klayout/tech/scripts/filler.py, which is a symlink to this file.
The technology is taken from KLayout itself, so run it with KLAYOUT_PATH scoped
to the PDK you want to fill for:

KLAYOUT_PATH=$PDK_ROOT/$PDK/libs.tech/klayout \
klayout -n <tech> -zz -r $PDK_ROOT/$PDK/libs.tech/klayout/tech/scripts/filler.py \
        -rd output_file=filled-design.gds.gz \
        input-file.gds.gz

This script has optional arguments to disable fill for some areas:

* no_activ - Disable Activ and GatPoly fill
* no_metal - Disable Metal fill
* no_topmetal - Disable TopMetal fill

Which areas a PDK offers depends on the macros it ships, so a technology without
a TopMetal filler macro simply has no TopMetal stage. These arguments don't take
a value. See the following example.

KLAYOUT_PATH=$PDK_ROOT/$PDK/libs.tech/klayout \
klayout -n <tech> -zz -r $PDK_ROOT/$PDK/libs.tech/klayout/tech/scripts/filler.py \
        -rd output_file=filled-design.gds.gz \
        -rd no_activ \
        -rd no_metal \
        input-file.gds.gz
"""
# pylint: disable=import-error

import os
import pathlib
import sys
import pya

LIB = 'SG13_dev'

# Fill areas in the order they must run, mapped to the '-rd' flag disabling each.
AREA_FLAGS = {
    'ActGatP': 'no_activ',
    'Metal': 'no_metal',
    'TopMetal': 'no_topmetal',
}

# Unlike the other scripts this one runs .lym macros rather than PCells, so it
# needs no loaded technology at all -- only the name, to build the macro file
# names. A PDK value is therefore taken at face value and an unregistered
# technology is not an error; the registry is just a fallback when PDK is unset.
def detect_tech():
    """Name of the technology to fill for, or exit if it cannot be pinned down."""
    pdk = os.environ.get('PDK', '').strip()
    if pdk:
        return pdk.removeprefix('ihp-')

    registered = [t for t in pya.Technology.technology_names() if t]
    if len(registered) == 1:
        return registered[0]

    if registered:
        print(f"Cannot tell which of {len(registered)} registered technologies to fill for: "
              f"{', '.join(registered)}.")
    else:
        print("PDK is not set and no KLayout technology is registered.")
    print("Set PDK, or scope KLAYOUT_PATH to exactly one PDK, for example:")
    print("  PDK=ihp-<tech> klayout -zz -r $PDK_ROOT/$PDK/libs.tech/klayout/tech/scripts/filler.py \\")
    print("          -rd output_file=<path-to-output-file> <input-file>")
    sys.exit(1)


TECH = detect_tech()

# The macros sit beside the scripts directory this was invoked from. The path is
# not resolved, so a PDK entry point finds its own macros whether it is a symlink
# to this file or a copy a PDK builder dereferenced into place.
MACROS = pathlib.Path(__file__).absolute().parents[1] / 'macros'

# A PDK offers exactly the areas it ships a filler macro for.
FILL_AREAS = [area for area in AREA_FLAGS
              if (MACROS / f"{TECH}_filler_{area}.lym").is_file()]

if not FILL_AREAS:
    print(f"No filler macros found for '{TECH}' in {MACROS}.")
    sys.exit(1)

try:
    output_file
except NameError:
    print("Missing output_file argument. Please define '-rd output_file=<path-to-output-file>'")
    sys.exit(1)

for area in FILL_AREAS:
    if AREA_FLAGS[area] in globals():
        print(f"Skip {area} fill because disabled by argument")
        continue

    print(f"Start filling {area}")
    pya.Macro(str(MACROS / f"{TECH}_filler_{area}.lym")).run()

layout = pya.CellView.active().layout()
layout.write(output_file)  # pylint: disable=undefined-variable
