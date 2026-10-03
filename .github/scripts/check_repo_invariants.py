#!/usr/bin/env python3
# ==========================================================================
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
# ==========================================================================

"""Assert the repo-level invariants the per-PDK CI routing relies on.

The routing in affected_pdks.py trusts .github/pdk-ci.yml to describe reality.
If the map drifts from the tree, CI fails open (an unlisted PDK routes to
nothing, all gates pass having tested nothing; a wrong-direction symlink breaks
the dependency model). This script makes that drift fail loudly. Run from the
repo root; exits non-zero listing every violation.

  1. pdks <-> directories: every top-level ihp-* directory that carries a
     libs.tech is declared under `pdks`, and every declared PDK exists.
  2. symlink direction: every symlink that points from one PDK into another has
     a matching depends_on edge (source depends on target). This catches a link
     added in the wrong direction (e.g. ihp-sg13g2 -> ihp-sg13cmos5l), which
     would silently invalidate the closure.
"""

import os
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG = os.path.join(ROOT, ".github", "pdk-ci.yml")
SKIP_DIRS = {".git", "actions_venv", "node_modules"}


def pdk_dirs():
    """Top-level ihp-* directories that carry a libs.tech (i.e. real PDKs)."""
    out = set()
    for name in os.listdir(ROOT):
        if name.startswith("ihp-") and os.path.isdir(os.path.join(ROOT, name, "libs.tech")):
            out.add(name)
    return out


def pdk_of(rel_path):
    """Which PDK a repo-relative path belongs to, or None."""
    top = rel_path.split(os.sep, 1)[0]
    return top if top in PDKS else None


def closure(name, deps):
    seen, stack = set(), [name]
    while stack:
        n = stack.pop()
        for d in deps.get(n, []):
            if d not in seen:
                seen.add(d)
                stack.append(d)
    return seen


def main():
    cfg = yaml.safe_load(open(CONFIG, encoding="utf-8"))
    declared = set(cfg.get("pdks", {}))
    deps = {n: list((m or {}).get("depends_on", []) or []) for n, m in cfg["pdks"].items()}

    global PDKS
    PDKS = pdk_dirs()

    errors = []

    # 1. map <-> directories
    for missing in sorted(PDKS - declared):
        errors.append("PDK directory '%s' has libs.tech but is not in pdk-ci.yml `pdks` "
                      "(its CI would never run)." % missing)
    for extra in sorted(declared - PDKS):
        errors.append("pdk-ci.yml declares PDK '%s' but no such directory with libs.tech exists." % extra)

    # 2. symlink direction
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for entry in dirnames + filenames:
            abspath = os.path.join(dirpath, entry)
            if not os.path.islink(abspath):
                continue
            rel = os.path.relpath(abspath, ROOT)
            src = pdk_of(rel)
            if src is None:
                continue
            target = os.readlink(abspath)
            resolved = os.path.normpath(os.path.join(os.path.dirname(rel), target))
            tgt = pdk_of(resolved)
            if tgt and tgt != src and tgt not in closure(src, deps):
                errors.append("symlink %s -> %s crosses %s -> %s, but pdk-ci.yml has no "
                              "matching depends_on edge." % (rel, target, src, tgt))

    if errors:
        print("Repo invariant violations:", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        return 1
    print("Repo invariants OK: pdks=%s, cross-PDK symlinks all match depends_on."
          % ", ".join(sorted(PDKS)))
    return 0


PDKS = set()

if __name__ == "__main__":
    sys.exit(main())
