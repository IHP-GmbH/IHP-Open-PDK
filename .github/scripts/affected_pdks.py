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

"""Turn a set of changed files into the CI matrix of affected PDKs.

Reads .github/pdk-ci.yml (the single source of truth for PDKs, their
dependencies and their per-PDK CI parameters) and prints a GitHub Actions
matrix listing the PDKs whose CI must run for the given change.

Rules (see .github/pdk-ci.yml for the rationale):
  * A change under a PDK's own directory affects that PDK and every PDK that
    depends on it (the reverse of `depends_on`).
  * A change matching `shared_infra` affects every PDK.
  * A workflow_dispatch / merge_group / schedule run, or a run whose changed
    file set could not be determined (empty), affects every PDK.

The heavy lifting (deciding which files changed) is done by the caller, which
passes the changed file list in; this script only applies policy, so it is
pure and unit-testable offline (see test_affected_pdks.py).

Usage (in CI):
  EVENT=<github.event_name> CHANGED='<json or newline list>' \
      python3 .github/scripts/affected_pdks.py [path/to/pdk-ci.yml]
Writes `matrix=<json>` and `any=<true|false>` to $GITHUB_OUTPUT (or stdout).
"""

import fnmatch
import json
import os
import sys

import yaml

FORCE_ALL_EVENTS = ("workflow_dispatch", "merge_group", "schedule", "push")


def load_config(path):
    with open(path, encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)
    if not cfg or "pdks" not in cfg:
        raise ValueError("%s: missing 'pdks' section" % path)
    cfg.setdefault("shared_infra", [])
    return cfg


def parse_changed(raw):
    """Accept a JSON array (dorny list-files: json) or a whitespace/newline list."""
    raw = (raw or "").strip()
    if not raw:
        return []
    if raw[0] == "[":
        return [str(f) for f in json.loads(raw)]
    return [line.strip() for line in raw.replace("\n", " ").split() if line.strip()]


def matches_shared(path, shared_globs):
    return any(fnmatch.fnmatch(path, pattern) for pattern in shared_globs)


def matches_class(rel_path, globs):
    """rel_path is relative to the PDK dir; globs come from test_classes."""
    return any(fnmatch.fnmatch(rel_path, g) for g in globs)


def dependents(pdks):
    """Reverse of `depends_on`: dep -> set of PDKs that depend on it."""
    rev = {name: set() for name in pdks}
    for name, meta in pdks.items():
        for dep in (meta or {}).get("depends_on", []) or []:
            rev.setdefault(dep, set()).add(name)
    return rev


def closure(seed, rev):
    """seed PDKs plus everything that transitively depends on them."""
    affected, stack = set(), list(seed)
    while stack:
        name = stack.pop()
        if name in affected:
            continue
        affected.add(name)
        stack.extend(rev.get(name, ()))
    return affected


def compute(cfg, event, changed, test_class=None):
    """Return (matrix_dict, any_bool) for the given event and changed files.

    With test_class set, a PDK is "directly changed" only when one of its own
    changed files matches that class's globs in cfg['test_classes']; a
    shared_infra change still forces every PDK. With no test_class (or an
    unknown one) any file under a PDK dir counts.
    """
    pdks = cfg["pdks"]
    shared = cfg.get("shared_infra", [])
    class_globs = (cfg.get("test_classes") or {}).get(test_class) if test_class else None

    force_all = (
        event in FORCE_ALL_EVENTS
        or not changed
        or any(matches_shared(f, shared) for f in changed)
    )

    if force_all:
        affected = set(pdks)
    else:
        direct = set()
        for name in pdks:
            prefix = name + "/"
            for f in changed:
                if not f.startswith(prefix):
                    continue
                if class_globs is None or matches_class(f[len(prefix):], class_globs):
                    direct.add(name)
                    break
        affected = closure(direct, dependents(pdks))

    include = [{"pdk": name} for name in sorted(affected)]
    return {"include": include}, bool(include)


def main(argv):
    config_path = argv[1] if len(argv) > 1 else ".github/pdk-ci.yml"
    cfg = load_config(config_path)
    event = os.environ.get("EVENT", "")
    changed = parse_changed(os.environ.get("CHANGED", ""))
    test_class = os.environ.get("CLASS", "") or None

    matrix, any_affected = compute(cfg, event, changed, test_class)

    line_matrix = "matrix=" + json.dumps(matrix)
    line_any = "any=" + ("true" if any_affected else "false")

    out_path = os.environ.get("GITHUB_OUTPUT")
    if out_path:
        with open(out_path, "a", encoding="utf-8") as handle:
            handle.write(line_matrix + "\n")
            handle.write(line_any + "\n")

    # Always echo to the log so the decision is visible in the job output.
    print(line_matrix)
    print(line_any)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
