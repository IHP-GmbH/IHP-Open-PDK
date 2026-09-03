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

"""Offline unit tests for affected_pdks.compute.

Runs the real .github/pdk-ci.yml through every change scenario the CI must get
right, plus an in-memory third-PDK case proving the map scales by one entry.
No GitHub, no network, no Docker: `python3 test_affected_pdks.py` (also works
under pytest).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import affected_pdks as ap  # noqa: E402

CONFIG = os.path.join(REPO, ".github", "pdk-ci.yml")


def affected(cfg, event, changed):
    matrix, any_affected = ap.compute(cfg, event, changed)
    names = sorted(entry["pdk"] for entry in matrix["include"])
    return names, any_affected


def load():
    return ap.load_config(CONFIG)


# --- scenarios against the real map -------------------------------------

def test_g2_change_pulls_in_cmos5l():
    cfg = load()
    names, any_a = affected(cfg, "pull_request",
                            ["ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/beol/5_16_metal1.drc"])
    assert names == ["ihp-sg13cmos5l", "ihp-sg13g2"], names
    assert any_a is True


def test_cmos5l_own_file_stays_cmos5l():
    cfg = load()
    # A real, non-symlink file that only cmos5l carries.
    names, any_a = affected(cfg, "pull_request",
                            ["ihp-sg13cmos5l/libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc"])
    assert names == ["ihp-sg13cmos5l"], names
    assert any_a is True


def test_both_pdks_changed():
    cfg = load()
    names, _ = affected(cfg, "pull_request", [
        "ihp-sg13g2/libs.tech/klayout/tech/lvs/rule_decks/x.lvs",
        "ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/foo.lvs",
    ])
    assert names == ["ihp-sg13cmos5l", "ihp-sg13g2"], names


def test_shared_infra_makefile_runs_all():
    cfg = load()
    names, any_a = affected(cfg, "pull_request", ["ihp-common/pdk.mk"])
    assert names == ["ihp-sg13cmos5l", "ihp-sg13g2"], names
    assert any_a is True


def test_shared_infra_versions_runs_all():
    cfg = load()
    names, _ = affected(cfg, "pull_request", ["versions.txt"])
    assert names == ["ihp-sg13cmos5l", "ihp-sg13g2"], names


def test_shared_infra_root_makefile_and_glob():
    cfg = load()
    for f in ("Makefile", "Makefile.sg13cmos5l", ".github/workflows/pdk-run.yml"):
        names, _ = affected(cfg, "pull_request", [f])
        assert names == ["ihp-sg13cmos5l", "ihp-sg13g2"], (f, names)


def test_workflow_dispatch_runs_all():
    cfg = load()
    names, any_a = affected(cfg, "workflow_dispatch", [])
    assert names == ["ihp-sg13cmos5l", "ihp-sg13g2"], names
    assert any_a is True


def test_merge_group_runs_all():
    cfg = load()
    names, _ = affected(cfg, "merge_group",
                        ["ihp-sg13cmos5l/libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc"])
    assert names == ["ihp-sg13cmos5l", "ihp-sg13g2"], names


def test_empty_changeset_falls_back_to_all():
    cfg = load()
    names, any_a = affected(cfg, "pull_request", [])
    assert names == ["ihp-sg13cmos5l", "ihp-sg13g2"], names
    assert any_a is True


def test_non_pdk_non_shared_change_runs_nothing():
    cfg = load()
    names, any_a = affected(cfg, "pull_request", ["README.md", "CHANGELOG.md"])
    assert names == [], names
    assert any_a is False


def test_third_pdk_scales_by_one_entry():
    # In-memory map extension: a new PDK depending on g2 must be pulled in by a
    # g2 change, proving the closure scales without touching the workflows.
    cfg = load()
    cfg["pdks"]["ihp-sg13foo"] = {"depends_on": ["ihp-sg13g2"]}
    names, _ = affected(cfg, "pull_request",
                        ["ihp-sg13g2/libs.tech/klayout/tech/drc/rule_decks/beol/5_16_metal1.drc"])
    assert names == ["ihp-sg13cmos5l", "ihp-sg13foo", "ihp-sg13g2"], names
    # A change to the new PDK alone stays contained.
    names, _ = affected(cfg, "pull_request", ["ihp-sg13foo/libs.tech/x"])
    assert names == ["ihp-sg13foo"], names


def _all_tests():
    return sorted(name for name in globals()
                  if name.startswith("test_") and callable(globals()[name]))


def main():
    failures = 0
    for name in _all_tests():
        try:
            globals()[name]()
            print("PASS %s" % name)
        except AssertionError as exc:
            failures += 1
            print("FAIL %s: %s" % (name, exc))
    print("\n%d passed, %d failed" % (len(_all_tests()) - failures, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
