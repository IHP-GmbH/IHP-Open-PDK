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
Milestone M4 -- simulated-side S-parameter runner.

For each measured bias point we run an ngspice AC small-signal analysis of the HBT subckt
(via `configs/hbt/hbt_sp.spice.j2`) at the *same* node voltages, recover the 2-port Y
matrix over frequency (two AC excitations), and extract CjE/CjC/fT with the SAME
`sp_runner.extract` functions used on the measured side -- guaranteeing an apples-to-apples
meas-vs-sim comparison.

Sim-side method: **AC 2-port Y extraction** (not ngspice `SP`). AC is used because it
directly and reliably yields Y for the built-in VBIC HBT model in ngspice v46 and matches
the measured cold-cap / fT values within a few percent (validated during M4 development).
"""

from __future__ import annotations

import logging
import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from tqdm import tqdm

from models_verifier.dc_runner.helper import (
    CORNERS_BJT,
    read_wrdata_df,
    sim_netlist_ngspice,
)
from models_verifier.sp_runner.extract import extract_metric

logger = logging.getLogger(__name__)


def _read_y(col1: Path, col2: Path) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Read the two wrdata files written by the AC template and assemble the Y(f) array.

    col1 -> real/imag of y11, y21 ; col2 -> real/imag of y12, y22. Returns (freq, Y)
    with Y shape (nf, 2, 2) complex, or None on failure.
    """
    df1 = read_wrdata_df(col1)
    df2 = read_wrdata_df(col2)
    if df1 is None or df2 is None or df1.empty or df2.empty:
        return None

    def cplx(df: pd.DataFrame, name: str) -> np.ndarray:
        return (
            pd.to_numeric(df[f"real({name})"], errors="coerce").to_numpy()
            + 1j * pd.to_numeric(df[f"imag({name})"], errors="coerce").to_numpy()
        )

    try:
        freq = pd.to_numeric(df1.iloc[:, 0], errors="coerce").to_numpy()
        y = np.zeros((len(freq), 2, 2), dtype=complex)
        y[:, 0, 0] = cplx(df1, "y11")
        y[:, 1, 0] = cplx(df1, "y21")
        y[:, 0, 1] = cplx(df2, "y12")
        y[:, 1, 1] = cplx(df2, "y22")
    except KeyError as e:
        logger.debug("Missing Y column in wrdata output: %s", e)
        return None
    return freq, y


def _run_one_bias(task: Dict) -> Tuple[int, Dict[str, float], Dict[str, float], Optional[str]]:
    """
    Worker: run all corners for a single bias point and extract `metric` per corner.

    Returns (idx, node_voltages, {corner: scalar}, error_or_None).
    """
    idx = task["idx"]
    metric = task["metric"]
    corners = tuple(task["corners"])
    work_dir = Path(task["work_dir"])
    template_path = Path(task["template_path"])

    jenv = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = jenv.get_template(template_path.name)

    per_corner: Dict[str, float] = {}
    for corner in corners:
        base = work_dir / f"sp_{metric}_{idx}_{corner}"
        col1 = Path(f"{base}_c1.csv")
        col2 = Path(f"{base}_c2.csv")
        netlist = Path(f"{base}.cir")
        log = Path(f"{base}.log")

        ctx = {
            "vb": task["vb"], "vc": task["vc"], "ve": task["ve"],
            "W": task["W"], "L": task["L"], "Nx": task["Nx"], "M": task["M"],
            "TEMP": task["TEMP"],
            "device_subckt": task["device_subckt"],
            "model_corner_lib": task["corner_lib_path"],
            "corner": corner,
            "out_col1": str(col1),
            "out_col2": str(col2),
            "ac_dec": task["ac_dec"],
            "f_start": task["f_start"],
            "f_stop": task["f_stop"],
        }
        try:
            netlist.write_text(template.render(**ctx))
        except Exception as e:  # pragma: no cover - template errors are fatal per row
            return idx, task["node_voltages"], per_corner, f"[{corner}] render failed: {e}"

        rc = sim_netlist_ngspice(netlist, log)
        if rc != 0:
            return idx, task["node_voltages"], per_corner, f"[{corner}] ngspice rc={rc} ({log})"

        y_pair = _read_y(col1, col2)
        if y_pair is None:
            return idx, task["node_voltages"], per_corner, f"[{corner}] no/invalid Y output"

        freq, y = y_pair
        try:
            per_corner[corner] = extract_metric(metric, freq, y)
        except Exception as e:  # pragma: no cover
            return idx, task["node_voltages"], per_corner, f"[{corner}] extract failed: {e}"

    return idx, task["node_voltages"], per_corner, None


@dataclass
class SparamSweepRunner:
    """Run ngspice AC S-param (Y) sims across corners for a set of bias points."""

    template_path: Path
    corner_lib_path: Path
    device_subckt: str
    work_dir: Path
    corners: Sequence[str] = field(default_factory=lambda: list(CORNERS_BJT))
    max_workers: int = max(1, os.cpu_count())
    ac_dec: int = 20
    f_start: float = 1e8
    f_stop: float = 65e9

    def __post_init__(self) -> None:
        for p in (self.template_path, self.corner_lib_path):
            if not Path(p).exists():
                raise FileNotFoundError(f"Path not found: {p}")
        shutil.rmtree(self.work_dir, ignore_errors=True)
        Path(self.work_dir).mkdir(parents=True, exist_ok=True)

    def run(
        self,
        metric: str,
        bias_points: List[Dict],
        geom: Dict[str, float],
        temp: float = 27.0,
    ) -> pd.DataFrame:
        """
        Simulate `metric` for every bias point and return a DataFrame with one row per
        bias point: node voltages (vb, vc, ve, vs) plus `<metric>_sim_<corner>` columns.

        `bias_points` items: {"vb","vc","ve","vs"} node voltages.
        `geom`: {"W","L","Nx","M"} device geometry (W/L in metres or um as read from MDM).
        """
        tasks = []
        for idx, bp in enumerate(bias_points):
            node_voltages = {k: float(bp.get(k, 0.0)) for k in ("vb", "vc", "ve", "vs")}
            tasks.append({
                "idx": idx,
                "metric": metric,
                "vb": node_voltages["vb"],
                "vc": node_voltages["vc"],
                "ve": node_voltages["ve"],
                "node_voltages": node_voltages,
                "W": geom.get("W", 0.12),
                "L": geom.get("L", 0.96),
                "Nx": geom.get("Nx", 1),
                "M": geom.get("M", 1),
                "TEMP": temp,
                "device_subckt": self.device_subckt,
                "corner_lib_path": str(self.corner_lib_path),
                "template_path": str(self.template_path),
                "corners": tuple(self.corners),
                "work_dir": str(self.work_dir),
                "ac_dec": self.ac_dec,
                "f_start": f"{self.f_start:.16g}",
                "f_stop": f"{self.f_stop:.16g}",
            })

        rows: List[Dict] = [None] * len(tasks)
        errors: List[str] = []
        with ProcessPoolExecutor(max_workers=max(1, self.max_workers)) as ex:
            futs = {ex.submit(_run_one_bias, t): t["idx"] for t in tasks}
            for fut in tqdm(as_completed(futs), total=len(futs), desc=f"AC sim {metric}"):
                idx, node_voltages, per_corner, err = fut.result()
                row = dict(node_voltages)
                for corner in self.corners:
                    row[f"{metric}_sim_{corner}"] = per_corner.get(corner, float("nan"))
                rows[idx] = row
                if err:
                    errors.append(f"bias#{idx}: {err}")

        if errors:
            logger.warning("S-param AC sim: %d bias/corner issue(s): %s",
                           len(errors), "; ".join(errors[:5]) + (" ..." if len(errors) > 5 else ""))

        return pd.DataFrame([r for r in rows if r is not None])
