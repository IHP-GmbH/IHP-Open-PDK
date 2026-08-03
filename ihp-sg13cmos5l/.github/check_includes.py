#!/usr/bin/env python3
# =========================================================================
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
# =========================================================================

"""Check that every rule deck the top decks include actually exists.

Most of this PDK's rule decks are symlinks into a sibling ihp-sg13g2
checkout. When SG13G2 adds a deck and includes it unconditionally from
a deck we symlink, we need a symlink for the new file too. Until someone
adds one, KLayout aborts on the very first include with

    Unable to open file: .../rule_decks//custom_mom_extractor.lvs
    in MacroInterpreter::include_expansion

which says nothing about the actual cause. That is issue #64.

Looking for dangling symlinks does not catch this: the new deck has no
symlink at all, so there is no broken link to find. What catches it is
walking the includes, which is what this does.

KLayout's `# %include` is a preprocessor directive, not a comment, and a
relative include resolves against the directory of the including file as
reached, i.e. through the symlink, not through its target. Paths here are
resolved the same way.

Usage:
    python3 .github/check_includes.py [ROOT]
"""

import os
import re
import sys

INCLUDE = re.compile(r"^\s*#\s*%include\s+(\S+)\s*$")

TOP_DECKS = [
    "libs.tech/klayout/tech/lvs/sg13cmos5l.lvs",
    "libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc",
]


def walk(path, seen, missing, chain):
    """Follow every %include reachable from path."""
    if path in seen:
        return
    seen.add(path)

    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = handle.readlines()
    except OSError as exc:
        missing.append((path, chain, str(exc)))
        return

    base = os.path.dirname(path)
    for number, line in enumerate(lines, 1):
        match = INCLUDE.match(line)
        if not match:
            continue
        target = os.path.normpath(os.path.join(base, match.group(1)))
        where = "{}:{}".format(path, number)
        if not os.path.exists(target):
            missing.append((target, chain + [where], "not found"))
            continue
        walk(target, seen, missing, chain + [where])


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    seen = set()
    missing = []

    for deck in TOP_DECKS:
        path = os.path.join(root, deck)
        if not os.path.exists(path):
            missing.append((path, [], "top deck not found"))
            continue
        walk(path, seen, missing, [])

    print("Resolved {} rule decks from {} top decks.".format(
        len(seen), len(TOP_DECKS)))

    if not missing:
        return 0

    for target, chain, reason in missing:
        print("", file=sys.stderr)
        print("MISSING: {} ({})".format(target, reason), file=sys.stderr)
        for step in chain:
            print("  included from {}".format(step), file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "If SG13G2 added these decks, this PDK needs symlinks for them, and\n"
        "possibly an include in its own top deck. See issue #64.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
