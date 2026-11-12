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
C-V verification of one device config (MOS junction / gate / oxide capacitances, pnpMPA
CBC / CBE).

    python -m models_verifier.cv_runner.verifier --config configs/mos/nmos_lv/sg13_lv_nmos.yaml

Subclasses `MdmVerifier` for the range checker, exceptions, reports and summaries; the
measurement groups listed in `cv_setups` are simulated by `CvSweepRunner`. Everything goes to
`<output_dir>/cv/`, so the DC results stay untouched. The acceptance check is the normal one:
the ss..ff band widened by `corner_tolerance_percent`, at most `threshold_percent_oob` of the
points outside.

Config keys: `cv_template_path`, `cv_subckt_pins` (pin order of the subckt), `cv_setups`
(terminal roles per group, see cv_sweep_runner.py), `cv_metrics`, `cv_freq_hz` (meter
frequency, not recorded in the files: 1 MHz assumed), `cv_file_overrides`, `cv_mqa_ranges`
(optional), `cv_waivers_dir` (default waivers/cv).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

from models_verifier.cv_runner.cv_sweep_runner import CvSweepRunner
from models_verifier.dc_runner.helper import CORNERS_BJT, CORNERS_MOS, SIM_TYPE_MAP
from models_verifier.error_analyzer.config import MetricSpec, Threshold, Tolerance
from models_verifier.error_analyzer.range_checker import RangeChecker
from models_verifier.mdm_processing.aggregator import MdmDirectoryAggregator
from models_verifier.models_verifier import MdmVerifier, VerificationError


class CvVerifier(MdmVerifier):
    """Simulate and range-check the capacitance groups of one device config."""

    def __init__(self, config_path: Path):
        super().__init__(config_path)
        cfg = self.config
        self.cv_setups: Dict[str, Dict] = cfg.get("cv_setups") or {}
        self.cv_metrics_cfg: List[Dict] = cfg.get("cv_metrics") or []
        if not self.cv_setups or not self.cv_metrics_cfg or not cfg.get("cv_template_path"):
            raise VerificationError("C-V verification needs cv_template_path, cv_setups and cv_metrics.")
        self.cv_waivers_dir = Path(cfg.get("cv_waivers_dir", "waivers/cv"))
        self.output_dir = self.output_dir / "cv"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _build_frames(self) -> List[pd.DataFrame]:
        """Simulate every C-V group of the config; one merged frame per group."""
        cfg = self.config
        aggregator = MdmDirectoryAggregator(
            input_dir=Path(cfg["mdm_dir"]), recursive=True,
            output_dir=self._clean_mkdir(self.output_dir / "clean_measured_data"), create_csvs=True,
            device_type=self.device_type, exclude_patterns=cfg.get("exclude_patterns") or [],
        )
        full_by_type, compact_by_type = aggregator.aggregate()
        runner = CvSweepRunner(
            template_path=Path(cfg["cv_template_path"]),
            corner_lib_path=Path(cfg["corner_lib_path"]),
            device_subckt=self.device_name,
            subckt_pins=list(cfg["cv_subckt_pins"]),
            cv_setups=self.cv_setups,
            output_dir=self.output_dir,
            corners=CORNERS_MOS if self.device_type == "mos" else CORNERS_BJT,
            freq=float(cfg.get("cv_freq_hz", 1.0e6)),
            file_overrides=cfg.get("cv_file_overrides") or {},
            max_workers=int(cfg.get("max_workers", 8)),
        )
        logging.info("C-V meter frequency assumed %.4g Hz (not recorded in the MDM headers)", runner.freq)

        frames: List[pd.DataFrame] = []
        for group, compact_df in compact_by_type.items():
            if group not in self.cv_setups:
                if SIM_TYPE_MAP.get(group) == "cap":
                    logging.warning("C-V group '%s' (%d blocks) has no cv_setups entry: not judged.",
                                    group, len(compact_df))
                continue
            logging.info("Processing C-V group: %s (%d blocks)", group, len(compact_df))
            parts, errors = runner.run(group, compact_df, full_by_type[group])
            if errors:
                logging.error("C-V errors for %s: %s", group, errors)
                self.simulation_errors += [(str(group), int(i), str(m)) for i, m in errors]
            if parts:
                frames.append(pd.concat(parts, ignore_index=True).assign(master_setup_type=group))
        missing = sorted(set(self.cv_setups) - set(compact_by_type))
        if missing:     # a typo would leave the intended group unjudged
            raise VerificationError(f"cv_setups groups without measurement files: {missing}")
        unused = sorted(set(runner.file_overrides) - runner.used_overrides)
        if unused:
            raise VerificationError(f"cv_file_overrides patterns that match no measured file: {unused}")
        if not frames:
            raise VerificationError("No merged C-V rows produced.")
        return frames

    def _build_cv_range_checker(self) -> RangeChecker:
        """The normal check on the C-V metrics: ss..ff band + corner tolerance, 0.5 % rule."""
        tolerance = Tolerance(abs=float(self.config.get("tolerance_abs", 0.0)),
                              rel=float(self.config.get("corner_tolerance_percent", 0.0)))
        metrics = [MetricSpec(name=m["name"], meas=m["meas"], tt=m["tt"], ss=m["ss"], ff=m["ff"],
                              tolerance=tolerance, valid_range=m.get("valid_range"))
                   for m in self.cv_metrics_cfg]
        threshold = Threshold(max_out_of_range_percent=float(self.config.get("threshold_percent_oob", 0)))
        return RangeChecker(metrics=metrics, default_threshold=threshold, mqa_ranges=self.config.get("cv_mqa_ranges"))

    def _run_cv_pipeline(self, waivers_dir: Optional[Path] = None
                         ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, float]]:
        """Simulate -> range-check -> exceptions -> reports (mirrors `MdmVerifier._run_pipeline`)."""
        logging.info("Starting C-V verification of device: %s", self.device_name)
        self._start_run()
        frames = self._build_frames()
        full_res, detailed_failures, stats = self._check_and_report(
            frames, self._build_cv_range_checker(), waivers_dir or self.cv_waivers_dir,
            threshold=self.config.get("threshold_percent_oob", 0),
            tolerance_rel=self.config.get("corner_tolerance_percent", 0.0),
        )
        return full_res, detailed_failures, stats

    def run_verification(self) -> int:
        _full, _det, stats = self._run_cv_pipeline()
        return self._exit_code(stats)


def main() -> int:
    parser = argparse.ArgumentParser(prog="cv_verifier", description="C-V (capacitance) meas-vs-sim verification.")
    parser.add_argument("--config", "-c", type=Path, required=True, help="Device YAML config (with cv_setups).")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    try:
        if not args.config.exists():
            logging.error("Configuration file not found: %s", args.config)
            return 2
        return CvVerifier(args.config).run_verification()
    except VerificationError as e:
        logging.error("C-V verification failed: %s", e)
        return 2
    except Exception as e:  # pragma: no cover
        logging.exception("Unexpected error during C-V verification: %s", e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
