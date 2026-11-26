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
Unit tests for the schema-2 exact-value exceptions (`models_verifier/waivers/`).

A synthetic curve (no simulation) goes through the real RangeChecker, the verifier's
`_apply_waivers` and the generator (`update_exceptions`, and `waive_run` through the real report
files):
  - an exact reproduction is waived ("Failed (waived, auto, pending review)" / "... approved");
  - one changed simulated value, one extra failing point, another judged-point count, another
    toolchain or a rejected entry give "Failed (new)";
  - a change far below the stored precision (5e-11 relative, the largest difference seen between
    machines) is still an exact reproduction (for that value; a value next to a rounding step can flip);
  - a curve without simulated values is "Failed (not simulated)", never waived;
  - the generator keeps existing entries and other toolchains, keeps an approval when nothing
    changed, withdraws it when values changed or a toolchain is added (the reviewer's reason is
    kept), never touches a rejected entry, carries old schema-1 dates, and refuses runs with
    simulation errors;
  - an exception whose curve is missing from the run makes the run exit 1;
  - unknown entry statuses and schemas stop the load;
  - the summary counts waived curves as failures, and only new failures set exit code 1.

Run: `python -m pytest models_verifier/tests/test_waivers.py` (from the framework root), or
standalone `python models_verifier/tests/test_waivers.py`.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance  # noqa: E402
from models_verifier.error_analyzer.range_checker import RangeChecker  # noqa: E402
from models_verifier.models_verifier import MdmVerifier  # noqa: E402
from models_verifier.run_record import exception_toolchain, toolchain_mismatch, write_toolchain_txt  # noqa: E402
from models_verifier.waivers.generate import update_exceptions, waive_run  # noqa: E402
from models_verifier.waivers.waiver import (  # noqa: E402
    APPROVED,
    AUTO_WAIVED,
    FAILED_NEW,
    NOT_SIMULATED,
    PASSED,
    REJECTED,
    WAIVED_APPROVED,
    WAIVED_AUTO,
    ExceptionStore,
    curve_key,
    round_sig,
)
import pytest  # noqa: E402

DEVICE = "npn13g2"
KEY = curve_key("fo_ib_RF.mdm", 3, "ic", "meas")


class _Verifier(MdmVerifier):
    """Just enough of MdmVerifier for _apply_waivers / gen_summary_stats (no config, no run)."""

    def __init__(self, exception_key: str = "ng47"):
        self.device_name = DEVICE
        self.toolchain = exception_key
        self.exception_key = exception_key
        self.clip_curr = 1e-12
        self.stale_exceptions = []
        self.absent_exceptions = []
        self.simulation_errors = []


def _curve(shift_point: int = -1, factor: float = 1.0, extra_fail: bool = False) -> pd.DataFrame:
    """
    One curve of 10 points: measured ic is 20 % above tt on points 7..9 (band = +-5 %), so the
    meas target fails with 3 out-of-band points. `shift_point`/`factor` change one simulated
    value; `extra_fail` pushes point 6 out of the band as well.
    """
    vb = np.round(np.linspace(0.70, 0.88, 10), 3)
    tt = 1e-6 * np.exp((vb - 0.7) / 0.026)
    if shift_point >= 0:
        tt[shift_point] *= factor
    meas = tt.copy()
    meas[7:] *= 1.2
    if extra_fail:
        meas[6] *= 1.2
    return pd.DataFrame({
        "block_id": "uuid-of-this-run", "input_data": "fo_ib_RF.mdm", "block_index": 3,
        "output_vars": "ic", "vb": vb, "vc": 0.5, "ve": 0.0, "vs": 0.0,
        "ic_meas": meas, "ic_sim_hbt_typ": tt, "ic_sim_hbt_bcs": tt * 0.95, "ic_sim_hbt_Wcs": tt * 1.05,
    })


def _judge(curve: pd.DataFrame, store: ExceptionStore, exception_key: str = "ng47"):
    """Range-check one curve and apply the exceptions; return (verifier, rows, failing points)."""
    checker = RangeChecker(
        metrics=[MetricSpec(name="ic", meas="ic_meas", tt="ic_sim_hbt_typ", ss="ic_sim_hbt_bcs",
                            ff="ic_sim_hbt_Wcs", tolerance=Tolerance(abs=0.0, rel=0.27))],
        default_threshold=Threshold(max_out_of_range_percent=0.5),
    )
    report, failures = checker.analyze(curve)
    verifier = _Verifier(exception_key)
    return verifier, verifier._apply_waivers(report, failures, store), failures


def _store_from(curve: pd.DataFrame, tmp: Path, toolchain: str = "ng47") -> ExceptionStore:
    """Exception file written by the generator from a first run of `curve`."""
    store = ExceptionStore(device=DEVICE, path=tmp / f"{DEVICE}.yaml")
    _v, rows, failures = _judge(curve, store, toolchain)
    update_exceptions(store, rows, failures, toolchain, "2026-10-11")
    store.save()
    return ExceptionStore.load(DEVICE, tmp)


def _meas_status(rows: pd.DataFrame) -> str:
    return rows[rows["target"] == "meas"]["status"].iloc[0]


def test_exact_reproduction_is_waived():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        _v, rows, _f = _judge(_curve(), store)
    assert _meas_status(rows) == WAIVED_AUTO
    assert rows[rows["target"] == "tt"]["status"].iloc[0] == PASSED   # tt lies inside its band
    assert not rows[rows["target"] == "meas"]["passed"].iloc[0]        # still a failure


def test_approved_entry_gives_approved_status():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        store.entries[KEY]["status"] = APPROVED
        _v, rows, _f = _judge(_curve(), store)
    assert _meas_status(rows) == WAIVED_APPROVED


def test_changed_simulated_value_is_new():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        _v, rows, _f = _judge(_curve(shift_point=8, factor=1.0001), store)   # 1e-4 change on a failing point
    assert _meas_status(rows) == FAILED_NEW


def test_change_below_stored_precision_is_still_waived():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        # 5e-11: the largest machine-to-machine difference seen between this machine and the CI runner
        _v, rows, _f = _judge(_curve(shift_point=8, factor=1 + 5e-11), store)
    assert _meas_status(rows) == WAIVED_AUTO


def test_difference_names_what_changed():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        _v, rows, _f = _judge(_curve(shift_point=8, factor=1.01), store)
    meas = rows[rows["target"] == "meas"].iloc[0]
    why = store.difference(KEY, "ng47", meas["n_points"], meas["n_out_of_bounds"], meas["points_sha256"])
    assert why.startswith("points_sha256 ") and "n_points" not in why
    assert store.difference(KEY, "ng46", 10, 3, "x") is None          # no record for that toolchain


def test_extra_failing_point_is_new():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        _v, rows, _f = _judge(_curve(extra_fail=True), store)
    assert _meas_status(rows) == FAILED_NEW


def test_different_judged_point_count_is_new():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        _v, rows, _f = _judge(_curve().iloc[1:], store)     # same failing points, one point less judged
    assert _meas_status(rows) == FAILED_NEW


def test_other_toolchain_is_new():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td), toolchain="ng47")
        _v, rows, _f = _judge(_curve(), store, exception_key="ng46")
    assert _meas_status(rows) == FAILED_NEW


def test_rejected_entry_is_new():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        store.entries[KEY]["status"] = REJECTED
        _v, rows, _f = _judge(_curve(), store)
    assert _meas_status(rows) == FAILED_NEW


def test_file_records_counts_fingerprint_and_worst_point():
    with tempfile.TemporaryDirectory() as td:
        _store_from(_curve(), Path(td))
        doc = yaml.safe_load((Path(td) / f"{DEVICE}.yaml").read_text())
    assert doc["schema"] == 2 and doc["exact_sig_digits"] == 6
    entry = doc["exceptions"][0]
    assert entry["curve"] == {"input_data": "fo_ib_RF.mdm", "block_index": 3, "metric": "ic", "target": "meas"}
    assert entry["status"] == AUTO_WAIVED
    record = entry["toolchains"]["ng47"]
    assert record["n_points"] == 10 and record["n_out_of_bounds"] == 3
    assert len(record["points_sha256"]) == 16
    assert record["worst_point"]["bias"]["vb"] == 0.88          # the last point is furthest out
    tt = 1e-6 * np.exp((0.88 - 0.7) / 0.026)
    assert record["worst_point"]["sim"]["tt"] == round_sig(tt)


def test_generator_keeps_entries_and_other_toolchains():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        store = _store_from(_curve(), tmp, toolchain="ng47")
        other = curve_key("other.mdm", 0, "ib", "meas")
        store.entries[other] = {"curve": {"input_data": "other.mdm", "block_index": 0, "metric": "ib",
                                          "target": "meas"}, "status": AUTO_WAIVED, "toolchains": {}}
        _v, rows, failures = _judge(_curve(), store, exception_key="ng46")   # new on ng46
        counts = update_exceptions(store, rows, failures, "ng46", "2026-10-12")
    assert counts == {"updated": 1}
    assert other in store.entries                                   # an entry not in this run is kept
    assert sorted(store.entries[KEY]["toolchains"]) == ["ng46", "ng47"]
    assert store.entries[KEY]["first_waived"] == "2026-10-11"


def test_generator_withdraws_approval_when_values_change_and_skips_rejected():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        store.entries[KEY]["status"] = APPROVED
        _v, rows, failures = _judge(_curve(shift_point=8, factor=1.01), store)
        update_exceptions(store, rows, failures, "ng47", "2026-10-12")
        assert store.entries[KEY]["status"] == AUTO_WAIVED
        assert "approval needs renewal" in store.entries[KEY]["withdrawn"]
        assert store.entries[KEY]["reason"] == "auto-waived from a run, pending review"   # kept

        store.entries[KEY]["status"] = REJECTED
        before = dict(store.entries[KEY]["toolchains"]["ng47"])
        _v, rows, failures = _judge(_curve(shift_point=8, factor=1.02), store)
        counts = update_exceptions(store, rows, failures, "ng47", "2026-10-13")
    assert counts == {"rejected, left failing": 1}
    assert store.entries[KEY]["toolchains"]["ng47"] == before


def test_schema1_file_waives_nothing_but_gives_first_waived():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        (tmp / f"{DEVICE}.yaml").write_text(yaml.safe_dump({"device": DEVICE, "waivers": [
            {"input_data": "fo_ib_RF.mdm", "block_index": 3, "metric": "ic", "target": "meas",
             "snapshot_percentage_oob": 30.0, "margin": 1.0, "date": "2026-09-09"}]}))
        store = ExceptionStore.load(DEVICE, tmp)
        _v, rows, failures = _judge(_curve(), store)
        assert _meas_status(rows) == FAILED_NEW
        update_exceptions(store, rows, failures, "ng47", "2026-10-11")
    assert store.entries[KEY]["first_waived"] == "2026-09-09"


def test_stale_exception_is_listed():  # the curve passes now
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        passing = _curve()
        passing["ic_meas"] = passing["ic_sim_hbt_typ"]
        verifier, _rows, _f = _judge(passing, store)
    assert verifier.stale_exceptions == [KEY]


def test_summary_counts_waived_as_failed_and_exit_code_only_on_new():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        verifier, rows, failures = _judge(_curve(), store)
        stats = verifier.gen_summary_stats(rows, failures, final_summary_path=Path(td) / "final_summary.md")
        summary = (Path(td) / "final_summary.md").read_text()
        new_verifier, new_rows, new_failures = _judge(_curve(), ExceptionStore(device=DEVICE))
        new_stats = new_verifier.gen_summary_stats(new_rows, new_failures)
    assert stats["n_failed"] == 1 and stats["n_waived"] == 1 and stats["n_failed_new"] == 0
    assert verifier._exit_code(stats) == 0
    assert "| Measured | 1 | 0 | 1 | 1 | 0 | 0 |" in summary
    assert new_stats["n_failed_new"] == 1 and new_verifier._exit_code(new_stats) == 1
    verifier.simulation_errors = [("fo_ib", 3, "ngspice failed")]
    assert verifier._exit_code(stats) == 1             # a block that could not be simulated


def test_curve_without_simulated_values_is_an_error_not_a_pass():
    curve = _curve()
    curve["ic_sim_hbt_bcs"] = np.nan                  # one corner did not simulate at all
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        verifier, rows, failures = _judge(curve, store)
        stats = verifier.gen_summary_stats(rows, failures)
    assert set(rows["status"]) == {NOT_SIMULATED}
    assert stats["n_failed_new"] == 2 and verifier._exit_code(stats) == 1


def test_summary_csv_counts_not_simulated_rows_as_new():
    curve = _curve()
    curve["ic_sim_hbt_bcs"] = np.nan
    checker = RangeChecker(
        metrics=[MetricSpec(name="ic", meas="ic_meas", tt="ic_sim_hbt_typ", ss="ic_sim_hbt_bcs",
                            ff="ic_sim_hbt_Wcs", tolerance=Tolerance(abs=0.0, rel=0.27))],
        default_threshold=Threshold(max_out_of_range_percent=0.5),
    )
    report, failures = checker.analyze(curve)
    rows = _Verifier()._apply_waivers(report, failures, ExceptionStore(device=DEVICE))
    with tempfile.TemporaryDirectory() as td:
        checker.summarize_to_csv(rows, failures, Path(td) / "s.csv", Path(td) / "f.csv")
        summary = pd.read_csv(Path(td) / "s.csv")
    assert list(summary["n_failed_new"]) == [1, 1] and list(summary["n_failed"]) == [1, 1]


def test_partly_simulated_curve_fails_and_its_exception_records_the_missing_point():
    partial = _curve()
    partial.loc[2, "ic_sim_hbt_bcs"] = np.nan         # one corner did not converge at one point
    _v, rows, failures = _judge(partial, ExceptionStore(device=DEVICE))
    meas = rows[rows["target"] == "meas"].iloc[0]
    assert meas["status"] == FAILED_NEW and meas["n_missing"] == 1 and meas["n_out_of_bounds"] == 3
    failing_vb = sorted(failures.loc[failures["target"] == "meas", "vb"].round(3))
    assert failing_vb == sorted(partial["vb"].iloc[[2, 7, 8, 9]].round(3))
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(partial, Path(td))
        assert _meas_status(_judge(partial, store)[1]) == WAIVED_AUTO
        # the point simulates again: another result, so the exception no longer applies
        assert _meas_status(_judge(_curve(), store)[1]) == FAILED_NEW


def test_fingerprint_tells_which_point_of_a_cv_sweep_is_missing():
    """A junction C-V file sweeps vbc (not a terminal voltage): it must be part of the fingerprint."""
    def judged(missing: int) -> str:
        vbc = np.round(np.linspace(-1.0, 0.4, 8), 3)
        c = 1e-13 * (1 + 0.3 * vbc)
        curve = pd.DataFrame({"block_id": "b", "input_data": "CBC_pnpMPA_DUT1.mdm", "block_index": 0,
                              "output_vars": "cbc", "vbc": vbc, "ve": 0.0, "cbc_meas": c, "cbc_sim_typ": c,
                              "cbc_sim_bcs": c * 0.99, "cbc_sim_Wcs": c * 1.01})
        curve.loc[missing, "cbc_sim_bcs"] = np.nan
        checker = RangeChecker(
            metrics=[MetricSpec(name="cbc", meas="cbc_meas", tt="cbc_sim_typ", ss="cbc_sim_bcs",
                                ff="cbc_sim_Wcs", tolerance=Tolerance(abs=0.0, rel=0.27))],
            default_threshold=Threshold(max_out_of_range_percent=0.5),
        )
        report, failures = checker.analyze(curve)
        rows = _Verifier()._apply_waivers(report, failures, ExceptionStore(device=DEVICE))
        return rows[rows["target"] == "meas"]["points_sha256"].iloc[0]
    assert judged(2) != judged(5)


def test_two_rows_with_one_curve_key_stop_the_run():
    report = pd.DataFrame({"input_data": ["a.mdm", "a.mdm"], "block_index": [0, 0], "metric": ["ic", "ic"],
                           "target": ["meas", "meas"], "n_points": [3, 3], "n_out_of_bounds": [0, 0],
                           "passed": [True, True]})
    with pytest.raises(Exception, match="share a curve key"):
        _Verifier()._apply_waivers(report, pd.DataFrame(), ExceptionStore(device=DEVICE))


def test_exception_of_a_curve_missing_from_the_run_is_stale():
    with tempfile.TemporaryDirectory() as td:
        store = _store_from(_curve(), Path(td))
        other = _curve()
        other["input_data"] = "another_file.mdm"
        verifier, rows, failures = _judge(other, store)
        stats = verifier.gen_summary_stats(rows, failures)
    assert verifier.stale_exceptions == [KEY] and verifier.absent_exceptions == [KEY]
    assert verifier._exit_code(stats) == 1            # lost coverage fails the run


def test_rerun_of_the_generator_keeps_an_unchanged_approval():
    with tempfile.TemporaryDirectory() as td:
        store = ExceptionStore(device=DEVICE, path=Path(td) / f"{DEVICE}.yaml")
        _v, rows, failures = _judge(_curve(), store)
        update_exceptions(store, rows, failures, "ng47", "2026-10-11")
        store.entries[KEY]["status"] = APPROVED
        counts = update_exceptions(store, rows, failures, "ng47", "2026-10-12")   # the same finished run
        assert counts == {"already recorded": 1} and store.entries[KEY]["status"] == APPROVED
        _v, rows46, failures46 = _judge(_curve(), store, exception_key="ng46")
        update_exceptions(store, rows46, failures46, "ng46", "2026-10-12")
    assert store.entries[KEY]["status"] == AUTO_WAIVED
    assert store.entries[KEY]["withdrawn"].startswith("new toolchain ng46")


def test_waive_run_from_report_files_then_exact_match():
    """The generator reads the run's CSV files; the next run matches the written record exactly."""
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        results, waivers = tmp / "results", tmp / "waivers"
        config = tmp / "config.yaml"
        config.write_text(yaml.safe_dump({"device_name": DEVICE, "output_dir": str(results),
                                          "waivers_dir": str(waivers)}))
        verifier, rows, failures = _judge(_curve(), ExceptionStore(device=DEVICE))
        reports = results / "final_reports"
        reports.mkdir(parents=True)
        rows.to_csv(reports / "full_results.csv", index=False)
        failures.to_csv(reports / "failed_results.csv", index=False)
        verifier._write_new_failures(rows, reports / "new_failures.csv")
        write_toolchain_txt(results, DEVICE, "ng47-ovr-b4517ad", "ng47", "ngspice", "ngspice-47 : x")
        waive_run(config)
        _v, rows2, _f = _judge(_curve(), ExceptionStore.load(DEVICE, waivers))
        assert _meas_status(rows2) == WAIVED_AUTO

        verifier.simulation_errors = [("fo_ib", 3, "ngspice failed")]
        verifier._write_new_failures(rows, reports / "new_failures.csv")
        with pytest.raises(SystemExit, match="simulation errors"):
            waive_run(config)


def test_unknown_status_or_schema_stops_the_load():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        _store_from(_curve(), tmp)
        doc = yaml.safe_load((tmp / f"{DEVICE}.yaml").read_text())
        doc["exceptions"][0]["status"] = "Rejected"
        (tmp / f"{DEVICE}.yaml").write_text(yaml.safe_dump(doc))
        with pytest.raises(ValueError, match="status"):
            ExceptionStore.load(DEVICE, tmp)
        doc["exceptions"][0]["status"] = REJECTED
        doc["schema"] = "2"
        (tmp / f"{DEVICE}.yaml").write_text(yaml.safe_dump(doc))
        with pytest.raises(ValueError, match="schema"):
            ExceptionStore.load(DEVICE, tmp)


def test_toolchain_keys_and_binary_checks():
    assert exception_toolchain("ng47-ovr-b4517ad", uses_osdi=True) == "ng47-ovr-b4517ad"
    assert exception_toolchain("ng47-ovr-b4517ad", uses_osdi=False) == "ng47"
    assert toolchain_mismatch("ng47-ovr-b4517ad", "ngspice-47 : Circuit level", "/x/ovr-b4517ad/psp103.osdi") is None
    assert "ngspice binary" in toolchain_mismatch("ng47-ovr-b4517ad", "ngspice-46 : Circuit level", None)
    assert "OSDI" in toolchain_mismatch("ng47-ovr-b4517ad", "ngspice-47 : x", "/x/ovr-fdf2522/psp103.osdi")


def _run_all() -> None:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS: {t.__name__}")
    print(f"\nAll {len(tests)} exception tests passed.")


if __name__ == "__main__":
    _run_all()
