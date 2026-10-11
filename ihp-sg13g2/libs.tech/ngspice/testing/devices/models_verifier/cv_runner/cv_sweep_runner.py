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
C-V runner: simulates the capacitance-meter measurement of every measured C-V block.

A C-V file holds one block: a DC sweep of the meter's HIGH terminal(s) and one measured
capacitance column (cbd, cbs, cg_sd, cg_sdb, cd_g, cox, cbe, cbc). The terminal roles of each
measurement group come from the config (`cv_setups[<group>]`):

    high      pins driven by the sweep plus a small AC voltage (one or more)
    low       pins held at 0 V through sources whose AC currents are summed (the meter input)
    float     pins left open for AC but tied for DC (1e12 ohm) to the node of `float_to`
              (default: ground)
    sign      -1 when the file's sweep value is the negative of the HIGH-pin voltage (default 1)

Subckt pins in no role are AC ground (0 V). The template (`cv_template_path`) writes the device
instance from the block's design parameters. One single-frequency AC analysis per bias point:

    C = sum over the low pins of Im(I_low) / (2 pi f)

The rows "<frequency> <sweep value> <C>" of each corner are merged with the measured block on the sweep
value rounded to 9 decimals; every measured point is kept (a point the simulation did not give
has empty simulated columns and counts as n_missing).
"""

from __future__ import annotations

import logging
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import pandas as pd
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from tqdm import tqdm

from models_verifier.dc_runner.helper import sim_netlist_ngspice

# Design-parameter columns a C-V block may carry (MOS and pnpMPA); passed to the template by name.
DESIGN_COLUMNS = ("W", "L", "AD", "AS", "PD", "PS", "NF", "M", "A", "P", "AC", "PC")


def pin_nodes(setup: Mapping[str, Any], pins: Sequence[str]) -> Dict[str, str]:
    """
    Netlist node of every subckt pin for one `cv_setups` entry: "nh" for the HIGH pins,
    "nl_<pin>" for a LOW pin, "nf_<pin>" for a FLOAT pin, "0" (AC ground) for the others.
    Raises ValueError for an unknown pin, a pin in two roles, or a missing high / low.
    """
    roles = {role: [str(p) for p in (setup.get(role) or [])] for role in ("high", "low", "float")}
    if not roles["high"] or not roles["low"]:
        raise ValueError(f"cv_setups entry {dict(setup)} needs 'high' and 'low' pins")
    nodes: Dict[str, str] = {p: "0" for p in pins}
    seen: Dict[str, str] = {}
    for role, prefix in (("high", "nh"), ("low", "nl_"), ("float", "nf_")):
        for p in roles[role]:
            if p not in nodes:
                raise ValueError(f"cv_setups pin '{p}' is not a subckt pin {list(pins)}")
            if p in seen:
                raise ValueError(f"cv_setups pin '{p}' is both {seen[p]} and {role}")
            seen[p] = role
            nodes[p] = prefix if role == "high" else prefix + p
    return nodes


def read_cv_table(path: Path) -> Optional[pd.DataFrame]:
    """Read the rows "frequency sweep c" the template appends; None when missing or empty."""
    if not Path(path).exists():
        return None
    try:
        df = pd.read_csv(path, sep=r"\s+", engine="python", header=None, names=["freq", "sweep", "c"])
    except (pd.errors.EmptyDataError, ValueError):
        return None
    df = df.apply(pd.to_numeric, errors="coerce").dropna()
    return df[["sweep", "c"]] if not df.empty else None


def render_netlist(task: Dict[str, Any], corner: str, out_path: Path) -> str:
    """The netlist of one block and corner (the template decides the device instance)."""
    template_path = Path(task["template_path"])
    jenv = Environment(loader=FileSystemLoader(str(template_path.parent)), undefined=StrictUndefined,
                       trim_blocks=True, lstrip_blocks=True)
    return jenv.get_template(template_path.name).render(
        **task["params"], nodes=task["nodes"], low_pins=task["low_pins"], float_pins=task["float_pins"],
        float_to=task["float_to"], sweep_values=[f"{task['sign'] * v:.10g}" for v in task["sweep_values"]],
        freq=f"{task['freq']:.10g}", device_subckt=task["device_subckt"], TEMP=task["TEMP"],
        out_path=str(out_path), model_corner_lib=task["corner_lib_path"], corner=corner,
    )


def simulate_block(task: Dict[str, Any]) -> Tuple[int, Optional[pd.DataFrame], Optional[str]]:
    """
    Worker: render and simulate one measured C-V block for every corner. Returns (task index,
    frame [sweep, <metric>_sim_<corner>...], error message or None). The simulated bias is
    `sign` times the measured sweep value; the table is mapped back to the measured value.
    """
    merged: Optional[pd.DataFrame] = None
    for corner in task["corners"]:
        base = Path(f"{task['run_base']}_{corner}")
        netlist, log, out = base.with_suffix(".cir"), base.with_suffix(".log"), base.with_suffix(".txt")
        out.unlink(missing_ok=True)
        netlist.write_text(render_netlist(task, corner, out))
        rc = sim_netlist_ngspice(netlist, log)
        table = read_cv_table(out)
        if table is None:
            return task["idx"], None, f"[{log}] ngspice failed (rc={rc}), no C-V table"
        if rc != 0 or len(table) < len(task["sweep_values"]):
            logging.warning("ngspice %s for %s corner %s: %d of %d bias points simulated; see %s",
                            f"rc={rc}" if rc != 0 else "incomplete", task["input_data"], corner,
                            len(table), len(task["sweep_values"]), log)
        part = pd.DataFrame({"sweep": (task["sign"] * table["sweep"]).round(9) + 0.0,
                             f"{task['metric']}_sim_{corner}": table["c"]})
        merged = part if merged is None else pd.merge(merged, part, on="sweep", how="outer")
    return task["idx"], merged, None


@dataclass
class CvSweepRunner:
    """Render, simulate and merge every measured C-V block of one measurement group."""

    template_path: Path
    corner_lib_path: Path
    device_subckt: str
    subckt_pins: Sequence[str]
    cv_setups: Mapping[str, Mapping[str, Any]]
    output_dir: Path                     # <output_dir>/cv; run_data/ is created here
    corners: Sequence[str]
    freq: float = 1.0e6
    # {file-name substring: {design parameter: value}}: corrections of wrong header values
    file_overrides: Mapping[str, Mapping[str, float]] = field(default_factory=dict)
    max_workers: int = max(1, os.cpu_count() or 1)

    def __post_init__(self) -> None:
        for p in (self.template_path, self.corner_lib_path):
            if not Path(p).exists():
                raise FileNotFoundError(f"Path not found: {p}")
        self.used_overrides: set = set()     # file_overrides patterns that matched a file
        self.run_dir = Path(self.output_dir) / "run_data"
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def _params(self, row: Mapping[str, Any], input_data: str) -> Dict[str, Any]:
        """Design parameters of a block (header values, then the matching file overrides)."""
        lowered = {str(k).lower(): v for k, v in row.items()}
        params = {k: float(lowered[k.lower()]) for k in DESIGN_COLUMNS
                  if k.lower() in lowered and pd.notna(lowered[k.lower()])}
        for pattern, values in self.file_overrides.items():
            if pattern in input_data:
                self.used_overrides.add(pattern)
                logging.info("C-V %s: header values %s replaced by %s (cv_file_overrides)",
                             input_data, {k: params.get(k) for k in values}, dict(values))
                params.update({k: float(v) for k, v in values.items()})
        return params

    def run(self, group: str, compact_df: pd.DataFrame, full_df: pd.DataFrame
            ) -> Tuple[List[pd.DataFrame], List[Tuple[int, str]]]:
        """
        Simulate every block of `group`. Returns (merged frames, errors); each frame holds the
        measured block columns with `<metric>_meas` and the `<metric>_sim_<corner>` columns.
        """
        setup = self.cv_setups[group]
        nodes = pin_nodes(setup, self.subckt_pins)
        float_to = nodes[str(setup["float_to"])] if setup.get("float_to") else "0"
        compact = compact_df.rename(columns=str.lower).reset_index(drop=True)
        full = full_df.rename(columns=str.lower)

        tasks, errors = [], []
        for idx, row in compact.iterrows():
            input_data = str(row.get("input_data", ""))
            sweep_var = str(row.get("sweep_var", "")).strip().lower()
            metric = str(row.get("output_vars", "")).split(",")[0].strip().lower()
            block = full[full["block_id"].astype(str) == str(row["block_id"])]
            if sweep_var not in block.columns or metric not in block.columns:
                errors.append((int(idx), f"{input_data}: sweep '{sweep_var}' or output '{metric}' missing"))
                continue
            tasks.append({
                "idx": int(idx), "input_data": input_data, "metric": metric, "sweep_var": sweep_var,
                "block_id": str(row["block_id"]),
                "sweep_values": pd.to_numeric(block[sweep_var], errors="coerce").dropna().tolist(),
                "sign": float(setup.get("sign", 1)), "params": self._params(row.to_dict(), input_data),
                "nodes": [nodes[p] for p in self.subckt_pins], "low_pins": list(setup["low"]),
                "float_pins": list(setup.get("float") or []), "float_to": float_to,
                "freq": self.freq, "device_subckt": self.device_subckt,
                "TEMP": str(row.get("temp", 27.0)), "corners": list(self.corners),
                "template_path": str(self.template_path), "corner_lib_path": str(Path(self.corner_lib_path).resolve()),
                "run_base": str(self.run_dir / f"{group}_{row['block_id']}"),
            })

        frames = []
        with ProcessPoolExecutor(max_workers=max(1, self.max_workers)) as ex:
            futures = [ex.submit(simulate_block, t) for t in tasks]
            for f in tqdm(as_completed(futures), total=len(futures), desc=f"C-V {group}"):
                idx, sim, err = f.result()
                if err or sim is None:
                    errors.append((idx, err or "unknown error"))
                    continue
                task = next(t for t in tasks if t["idx"] == idx)
                block = full[full["block_id"].astype(str) == task["block_id"]].copy()
                block["sweep"] = pd.to_numeric(block[task["sweep_var"]], errors="coerce").round(9) + 0.0
                block = block.rename(columns={task["metric"]: f"{task['metric']}_meas"})
                # every measured point stays; one the simulation did not give counts as n_missing
                merged = block.merge(sim, on="sweep", how="left").drop(columns=["sweep"])
                merged["sweep_var"] = task["sweep_var"]      # for the figures (input_vars is sorted)
                if merged.empty:
                    errors.append((idx, f"{task['input_data']}: no common sweep values after the merge"))
                    continue
                frames.append(merged)
        return frames, errors
