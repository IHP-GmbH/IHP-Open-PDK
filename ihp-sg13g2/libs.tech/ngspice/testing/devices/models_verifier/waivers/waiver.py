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

"""
Curve exceptions ("waivers"), schema 2: exact-value exceptions per curve and toolchain.

How a run judges a curve
    A curve is one measured data block, identified by (input_data, block_index). The range
    checker judges it per metric (id, ib, ic, cgg, ft, ...) and per target ("meas" = the
    measurement, "tt" = the typical simulation) against the ss..ff band. A judged row fails
    when too many points lie outside the band.

What an exception stores
    For one failing (curve, metric, target) row and per toolchain (e.g. "ng47" or
    "ng47-ovr-b4517ad"): the number of judged points, the number of failing points, a
    fingerprint of ALL failing points and, for the reader, the worst failing point. The
    fingerprint is a hash of every failing point's bias coordinates and simulated tt / ss / ff
    values, rounded to `exact_sig_digits` significant digits (6 by default, see DEFAULT_SIG_DIGITS).

When a row is waived
    Only when the run reproduces that record exactly: the same number of judged points, the
    same number of failing points and the same fingerprint. Anything else (one point more or
    less, a changed simulated value, a toolchain without a record, an entry the reviewer
    rejected) is a NEW failure and makes the run exit 1. A row whose measured points have no
    simulated values at all ("Failed (not simulated)") is a framework error: it always makes
    the run exit 1 and is never waived.

A waiver means "reviewed", not "good"
    Waived rows stay failures in every report (status "Failed (waived, ...)"); only the exit
    code treats them differently.

File: <waivers_dir>/<device_name>.yaml

    schema: 2
    device: npn13g2
    exact_sig_digits: 6
    exceptions:
      - curve: {input_data: fo_ib_RF.mdm, block_index: 3, metric: ic, target: meas}
        status: auto-waived            # auto-waived | approved | rejected (reviewer sets the last two)
        reason: auto-waived from a run, pending review
        first_waived: '2026-09-09'
        documentation: final_reports/failed_results.csv of the run (all failing points)
        toolchains:
          ng47:
            n_points: 81
            n_out_of_bounds: 3
            points_sha256: 3f1c0e5a9b7d2e44
            worst_point: {bias: {vb: 0.81, vc: 0.5}, sim: {tt: ..., ss: ..., ff: ...},
                          meas: ..., lower: ..., upper: ...}

The generator `waivers/generate.py` writes these entries from a finished run.
"""

from __future__ import annotations

import hashlib
import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import yaml

from models_verifier.error_analyzer.range_checker import BIAS_COLUMNS

SCHEMA = 2
# Significant digits of the fingerprinted values. The same netlist on another machine (an ngspice built
# elsewhere) differs in the last digits: C-V values on the GitHub runner differed from this machine's by
# up to 5e-11 (relative), enough to change a 9th digit and so the fingerprint (CI run 38127836304).
# With 6 digits such a difference changes a fingerprint only for a value within 5e-11 of a rounding
# step (about 1e-4 of the values), while any change larger than 1e-5 (relative) always changes it.
DEFAULT_SIG_DIGITS = 6

# Row statuses in full_results.csv. Every "Failed ..." status is a failure in every report;
# the two UNWAIVED ones make the run exit 1.
PASSED = "Passed"
FAILED_NEW = "Failed (new)"
NOT_SIMULATED = "Failed (not simulated)"      # measured points without simulated values: framework error
WAIVED_AUTO = "Failed (waived, auto, pending review)"
WAIVED_APPROVED = "Failed (waived, approved)"
UNWAIVED_STATUSES = (FAILED_NEW, NOT_SIMULATED)
WAIVED_STATUSES = (WAIVED_AUTO, WAIVED_APPROVED)
NO_POINTS = "No points"      # no measured point inside the metric's bias window: not judged

# Entry statuses in the YAML file. The generator writes "auto-waived"; only the reviewer
# changes an entry to "approved" or "rejected".
AUTO_WAIVED = "auto-waived"
APPROVED = "approved"
REJECTED = "rejected"
ENTRY_STATUSES = (AUTO_WAIVED, APPROVED, REJECTED)


# (input_data, block_index, metric, target) as text.
CurveKey = Tuple[str, str, str, str]


def _text(value: object) -> str:
    """Stable text for a key part: None/NaN -> "", 3.0 -> "3"."""
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        if value.is_integer():
            return str(int(value))
    return str(value)


def curve_key(input_data: object, block_index: object, metric: object, target: object) -> CurveKey:
    """Key of one judged row. `block_id` (a new uuid every run) is deliberately not part of it."""
    return (_text(input_data), _text(block_index), _text(metric), _text(target))


def round_sig(value: object, digits: int = DEFAULT_SIG_DIGITS) -> Optional[float]:
    """Round to `digits` significant digits; None for missing / NaN values."""
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(x):
        return None
    if x == 0.0 or math.isinf(x):
        return x
    return float(f"{x:.{digits - 1}e}")


# -------------------------------------------------------------------------------------------
# Failing points of a run
# -------------------------------------------------------------------------------------------

def index_failing_points(failures: pd.DataFrame) -> Dict[CurveKey, List[dict]]:
    """
    Group the point records of `RangeChecker.analyze()` (failed_results.csv) by curve key.

    Each point becomes {"bias": {...}, "sim": {"tt", "ss", "ff"}, "meas", "lower", "upper",
    "deviation"} with unrounded values.
    """
    index: Dict[CurveKey, List[dict]] = {}
    if failures is None or failures.empty:
        return index
    bias_cols = [c for c in BIAS_COLUMNS if c in failures.columns]
    for rec in failures.to_dict("records"):
        key = curve_key(rec.get("input_data"), rec.get("block_index"), rec.get("metric"), rec.get("target"))
        index.setdefault(key, []).append({
            "bias": {c: rec[c] for c in bias_cols if round_sig(rec.get(c)) is not None},
            "sim": {c: rec.get(f"{c}_value") for c in ("tt", "ss", "ff")},
            "meas": rec.get("meas_value"),
            "lower": rec.get("lower_bound"),
            "upper": rec.get("upper_bound"),
            "deviation": rec.get("deviation"),
        })
    return index


def points_fingerprint(points: List[dict], digits: int = DEFAULT_SIG_DIGITS) -> str:
    """
    Hash of the failing points: bias coordinates and simulated tt/ss/ff values, each rounded to
    `digits` significant digits. The order of the points does not matter.
    """
    def fmt(v: object) -> str:
        r = round_sig(v, digits)
        return "nan" if r is None else f"{r:.{digits - 1}e}"

    lines = sorted(
        ";".join(f"{k}={fmt(v)}" for k, v in sorted(p["bias"].items()))
        + "|" + ";".join(f"{k}={fmt(p['sim'].get(k))}" for k in ("tt", "ss", "ff"))
        for p in points
    )
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()[:16]


def worst_point(points: List[dict], digits: int = DEFAULT_SIG_DIGITS) -> Optional[dict]:
    """The failing point furthest outside its band, rounded for the YAML file (documentation only)."""
    if not points:
        return None
    # largest deviation; ties broken by the bias, so every toolchain records the same point
    p = max(points, key=lambda q: (abs(round_sig(q.get("deviation")) or 0.0),
                                   tuple(sorted((k, round_sig(v) or 0.0) for k, v in q["bias"].items()))))
    return {
        "bias": {k: round_sig(v, digits) for k, v in sorted(p["bias"].items())},
        "sim": {k: round_sig(p["sim"].get(k), digits) for k in ("tt", "ss", "ff")},
        "meas": round_sig(p.get("meas"), digits),
        "lower": round_sig(p.get("lower"), digits),
        "upper": round_sig(p.get("upper"), digits),
    }


def toolchain_record(n_points: int, n_out_of_bounds: int, fingerprint: str, points: List[dict],
                     digits: int = DEFAULT_SIG_DIGITS) -> dict:
    """What one toolchain must reproduce for the row to stay waived (`points` only for the worst point)."""
    return {
        "n_points": int(n_points),
        "n_out_of_bounds": int(n_out_of_bounds),
        "points_sha256": fingerprint,
        "worst_point": worst_point(points, digits),
    }


# -------------------------------------------------------------------------------------------
# The exception file of one device
# -------------------------------------------------------------------------------------------

@dataclass
class ExceptionStore:
    """All exception entries of one device (one YAML file), keyed by `curve_key`."""

    device: str
    path: Optional[Path] = None
    sig_digits: int = DEFAULT_SIG_DIGITS
    entries: Dict[CurveKey, dict] = field(default_factory=dict)
    # Dates of a schema-1 file (old tolerant waivers), kept only to fill `first_waived`.
    legacy_dates: Dict[CurveKey, str] = field(default_factory=dict)

    @classmethod
    def load(cls, device: str, waivers_dir: Path | str) -> "ExceptionStore":
        """
        Read `<waivers_dir>/<device>.yaml`. A missing file means no exceptions. A schema-1 file
        (the old snapshot/margin waivers: a `waivers:` list and no `schema:`) gives no exceptions
        either; its dates are kept so the generator can carry them over as `first_waived`.
        Any other schema or an unknown entry status stops the run (ValueError): a typo must not
        waive or drop anything.
        """
        path = Path(waivers_dir) / f"{device}.yaml"
        store = cls(device=device, path=path)
        if not path.exists():
            logging.info("No exception file for '%s' (%s): 0 exceptions.", device, path)
            return store

        # CSafeLoader is the fast (libyaml) version of the safe loader; plain data only.
        loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
        doc = yaml.load(path.read_text(), Loader=loader) or {}
        if "schema" not in doc and "waivers" in doc:
            for item in doc.get("waivers") or []:
                key = curve_key(item.get("input_data"), item.get("block_index"), item.get("metric"),
                                item.get("target"))
                store.legacy_dates[key] = str(item.get("date", ""))
            logging.warning("%s is a schema-1 waiver file (%d entries): it waives nothing until it is "
                            "regenerated as schema 2 (make waive-...).", path, len(store.legacy_dates))
            return store

        if doc and doc.get("schema") != SCHEMA:
            raise ValueError(f"{path}: schema {doc.get('schema')!r} is not supported (expected {SCHEMA})")
        store.sig_digits = int(doc.get("exact_sig_digits", DEFAULT_SIG_DIGITS))
        for entry in doc.get("exceptions") or []:
            c = entry["curve"]
            if entry.get("status") not in ENTRY_STATUSES:
                raise ValueError(f"{path}: entry {c} has status {entry.get('status')!r}; "
                                 f"expected one of {ENTRY_STATUSES}")
            store.entries[curve_key(c["input_data"], c["block_index"], c["metric"], c["target"])] = entry
        logging.info("Loaded %d exception(s) for '%s' from %s", len(store.entries), device, path)
        return store

    def status_of(self, key: CurveKey, toolchain: str, n_points: int, n_out_of_bounds: int,
                  fingerprint: str) -> str:
        """Status of one FAILING row: waived only on an exact reproduction of its record."""
        entry = self.entries.get(key)
        if entry is None or entry.get("status") == REJECTED:
            return FAILED_NEW
        record = (entry.get("toolchains") or {}).get(toolchain)
        if record is None:
            return FAILED_NEW
        same = (
            int(record.get("n_points", -1)) == int(n_points)
            and int(record.get("n_out_of_bounds", -1)) == int(n_out_of_bounds)
            and record.get("points_sha256") == fingerprint
        )
        if not same:
            return FAILED_NEW
        return WAIVED_APPROVED if entry.get("status") == APPROVED else WAIVED_AUTO

    def difference(self, key: CurveKey, toolchain: str, n_points: int, n_out_of_bounds: int,
                   fingerprint: str) -> Optional[str]:
        """Why a failing row does not match the record of its exception for this toolchain, e.g.
        "n_out_of_bounds 27 -> 28"; None when the curve has no record for the toolchain."""
        record = ((self.entries.get(key) or {}).get("toolchains") or {}).get(toolchain)
        if record is None:
            return None
        changes = [f"{name} {record.get(name)} -> {now}" for name, now in
                   (("n_points", int(n_points)), ("n_out_of_bounds", int(n_out_of_bounds)),
                    ("points_sha256", fingerprint)) if str(record.get(name)) != str(now)]
        return "; ".join(changes) or f"entry status {self.entries[key].get('status')}"

    def stale_keys(self, report: pd.DataFrame, toolchain: str) -> List[CurveKey]:
        """
        Entries with a record for `toolchain` that no failing row of the run used: the row now
        passes, is not judged, or is missing from the run. To be reviewed (and removed).
        """
        failing = {
            curve_key(getattr(row, "input_data", None), getattr(row, "block_index", None), row.metric, row.target)
            for row in report.itertuples(index=False) if str(getattr(row, "status", "")).startswith("Failed")
        }
        return sorted((key for key, entry in self.entries.items()
                       if toolchain in (entry.get("toolchains") or {}) and key not in failing), key=_sort_key)

    def absent_keys(self, report: pd.DataFrame, toolchain: str) -> List[CurveKey]:
        """Entries with a record for `toolchain` whose curve is not in the run at all (a file that
        disappeared, was excluded or could not be built): coverage was lost, the run fails."""
        present = {curve_key(getattr(row, "input_data", None), getattr(row, "block_index", None), row.metric, row.target)
                   for row in report.itertuples(index=False)}
        return sorted((key for key, entry in self.entries.items()
                       if toolchain in (entry.get("toolchains") or {}) and key not in present), key=_sort_key)

    def save(self) -> Path:
        """Write the file (entries sorted by curve key, so the file diffs cleanly)."""
        doc = {
            "schema": SCHEMA,
            "device": self.device,
            "exact_sig_digits": self.sig_digits,
            "exceptions": [self.entries[k] for k in sorted(self.entries, key=_sort_key)],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        dumper = getattr(yaml, "CSafeDumper", yaml.SafeDumper)
        self.path.write_text(yaml.dump(doc, Dumper=dumper, sort_keys=False, default_flow_style=None,
                                       width=200, allow_unicode=True))
        return self.path

    def __len__(self) -> int:
        return len(self.entries)


def _sort_key(key: CurveKey) -> tuple:
    """Sort by file, then numerically by block index, then metric and target."""
    input_data, block_index, metric, target = key
    return (input_data, int(block_index) if block_index.isdigit() else 0, block_index, metric, target)
