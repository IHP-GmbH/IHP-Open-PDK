#!/usr/bin/env python3
#==========================================================================
# Copyright 2026 IHP PDK Authors
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
# SPDX-License-Identifier: Apache-2.0
#==========================================================================
"""Expand the single-row RESOVER tables of a `write_rcx_model` output.

The field solver flow measures resistance once per metal, so each
`Metal N RESOVER 0` table has one row. The extractor
(`extDistRCTable::getComputeRC_res`) however indexes the second row of
that table unconditionally and segfaults on a one-row table. Extraction
rules files from other sources carry a grid of neighbour spacing pairs
(s1 <= s2) with the resistance for each; this script writes the same
grid, using the spacings of the metal's OVER table and the measured
resistance for every pair.

Usage: expand_resover.py <model file>   (rewritten in place)
"""

import re
import sys


def main():
    path = sys.argv[1]
    lines = open(path).read().split("\n")

    # spacings per metal from the "Metal N OVER 0" tables
    spacings = {}
    i = 0
    while i < len(lines):
        m = re.match(r"Metal (\d+) OVER 0$", lines[i])
        if m and lines[i + 1].startswith("DIST count"):
            j = i + 2
            s = []
            while not lines[j].startswith("END DIST"):
                s.append(lines[j].split()[0])
                j += 1
            spacings[int(m.group(1))] = s
        i += 1

    out = []
    i = 0
    while i < len(lines):
        m = re.match(r"Metal (\d+) RESOVER 0$", lines[i])
        if m and lines[i + 1].startswith("DIST count 1 "):
            met = int(m.group(1))
            width = lines[i + 1].split()[4]
            res = lines[i + 2].split()[3]
            s = ["0"] + spacings[met]
            rows = [f"{a} {b} 0 {res}" for k, a in enumerate(s) for b in s[k:]]
            rows.append(f"{s[-1]} 0 {s[-1]} {res}")
            out.append(lines[i])
            out.append(f"DIST count {len(rows)} width {width}")
            out.extend(rows)
            i += 3  # skip DIST, row; END DIST is copied below
        else:
            out.append(lines[i])
            i += 1

    open(path, "w").write("\n".join(out))


if __name__ == "__main__":
    main()
