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

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
import logging

import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import suppress
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from tqdm import tqdm
from models_verifier.dc_runner.helper import (
    CORNERS_BJT,
    CORNERS_MOS,
    DEVICE_SWEEP_MAPS,
    get_topology_params,
    parse_float,
    parse_int,
    parse_sweep_triple,
    read_wrdata_df,
    sim_netlist_ngspice,
)


@dataclass
class DcSweepRunner:
    """
    Runner for executing ngspice DC sweeps across corners for a given device type.
    """

    template_path: Path
    device_name: str
    corner_lib_path: Path
    osdi_path: Optional[Path] = None
    device_type: str = "mos"
    corners: Sequence[str] = field(default_factory=list)
    max_workers: int = max(1, os.cpu_count() or 4)
    netlists_dir: Optional[Path] = None

    def __post_init__(self) -> None:
        """Validate paths, set corners, and prepare netlists directory."""
        self._validate_paths()
        self._set_corners()
        self._prepare_netlists_dir()

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------
    def _validate_paths(self) -> None:
        """Ensure required paths exist."""
        for p in (self.template_path, self.corner_lib_path, self.osdi_path):
            if isinstance(p, Path) and p is not None and not p.exists():
                raise FileNotFoundError(f"Path not found: {p}")

        if self.device_type not in DEVICE_SWEEP_MAPS:
            raise ValueError(
                f"Unsupported device_type: {self.device_type}. "
                f"Supported: {list(DEVICE_SWEEP_MAPS.keys())}"
            )

    def _set_corners(self) -> None:
        """Set corner list depending on device type."""
        self.corners = CORNERS_MOS if self.device_type == "mos" else CORNERS_BJT

    def _prepare_netlists_dir(self) -> None:
        """Recreate netlists_dir if provided."""
        if self.netlists_dir:
            shutil.rmtree(self.netlists_dir, ignore_errors=True)
            self.netlists_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    @staticmethod
    def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to lowercase without surrounding spaces."""
        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    def _save_netlist(
        self, netlist_text: str, corner: str, block_id: str, source_file: str
    ) -> None:
        """
        Optionally dump rendered netlist into netlists_dir.

        Args:
            netlist_text: The rendered netlist content
            corner: The corner name
            block_id: The block identifier
            source_file: The source file name for naming
        """
        if not self.netlists_dir:
            return
        src_stem = Path(source_file).stem if source_file else "unknown"
        dump_name = f"{src_stem}_{corner}_block-{block_id}.cir"
        (self.netlists_dir / dump_name).write_text(netlist_text)

    # -------------------------------------------------------------------------
    # Main entry
    # -------------------------------------------------------------------------

    def run(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Tuple[int, str]]]:
        """
        Execute sweeps in parallel.
        Returns:
            sim_df: concatenated simulation results
            errors: list of (row_idx, error_message)
        """
        df = self._normalize_cols(df).reset_index(drop=True)
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        workdir = Path(tempfile.mkdtemp(prefix="ngspice_sim_"))
        results: List[pd.DataFrame] = []
        errors: List[Tuple[int, str]] = []

        # Prepare tasks
        tasks: List[Dict[str, Any]] = [
            dict(
                idx=int(idx),
                row_dict=row.to_dict(),
                template_path=str(self.template_path),
                workdir=str(workdir),
                corner_lib_path=str(self.corner_lib_path),
                osdi_path=str(self.osdi_path),
                device_name=self.device_name,
                device_type=self.device_type,
                corners=tuple(self.corners),
                netlists_dir=str(self.netlists_dir) if self.netlists_dir else None,
            )
            for idx, row in df.iterrows()
        ]

        # Parallel execution
        with ProcessPoolExecutor(max_workers=max(1, self.max_workers)) as ex:
            futs = [ex.submit(self._process_one_worker, t) for t in tasks]

            for f in tqdm(as_completed(futs), total=len(futs), desc="Processing tasks"):
                rid, out_df, err = f.result()
                if err or out_df is None:
                    errors.append((rid, err or "unknown error"))
                else:
                    results.append(out_df)

        # Aggregate results
        with suppress(Exception):
            shutil.rmtree(workdir, ignore_errors=True)

        if not results:
            logging.error(f"All tasks failed. Errors: {errors}")
            raise RuntimeError("All simulations failed.")

        sim_df = pd.concat(results, ignore_index=True)
        sim_df = sim_df.sort_values(by=["block_id", "sweep_value"]).reset_index(
            drop=True
        )

        return sim_df, errors

    def _link_sim_to_clean(
        self,
        sim_results_df: pd.DataFrame,
        clean_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Merge simulation results with measured clean data on block_id + sweep values.

        Args:
            sim_results_df: Simulation results DataFrame (block_id, sweep_var, sweep_value, ...).
            clean_df: Measured/clean DataFrame (block_id, sweep_var, measured values).

        Returns:
            A merged DataFrame containing block_id, sweep_var, sweep values,
            measured variables, and all simulated corner variables.
        """
        if (
            "block_id" not in sim_results_df.columns
            or "block_id" not in clean_df.columns
        ):
            raise ValueError("Both DataFrames must contain a 'block_id' column.")

        out_blocks: list[pd.DataFrame] = []
        clean_groups = {bid: g for bid, g in clean_df.groupby("block_id")}

        for bid, sim_block in sim_results_df.groupby("block_id"):
            if bid not in clean_groups:
                logging.warning(f"Block_id '{bid}' in sim, not in clean. Skipping.")
                continue
            cblock = clean_groups[bid].copy()
            if sim_block.empty or cblock.empty:
                continue

            sweep_var = sim_block["sweep_var"].iloc[0]
            if sweep_var not in cblock.columns:
                logging.warning(
                    f"Sweep var '{sweep_var}' missing in clean for block '{bid}'. Skipping."
                )
                continue

            sim_block = sim_block.rename(columns={"sweep_value": sweep_var})

            merged = pd.merge(
                cblock,
                sim_block,
                on=["block_id", sweep_var],
                how="inner",
                suffixes=("", "_sim_dup"),
            )
            if merged.empty:
                logging.warning(
                    f"No matching sweep values for block '{bid}' after merge."
                )
                continue

            if "sweep_var" not in merged.columns:
                merged["sweep_var"] = sweep_var

            output_vars_str = merged["output_vars"].iloc[0]
            measured_vars = [v.strip() for v in output_vars_str.split(",")]

            cols_to_keep = self._build_keep_columns(cblock, merged, measured_vars, sweep_var)

            merged = merged.sort_values(sweep_var).reset_index(drop=True)
            out_blocks.append(merged[cols_to_keep])

        if not out_blocks:
            logging.error("No matching block_ids to link. Returning empty DataFrame.")
            return pd.DataFrame()

        final_df = pd.concat(out_blocks, ignore_index=True)
        return final_df.sort_values("block_id").reset_index(drop=True)

    def _build_keep_columns(
        self,
        cblock: pd.DataFrame,
        merged: pd.DataFrame,
        measured_vars: list[str],
        sweep_var: str,
    ) -> list[str]:
        """Build the final list of columns to retain in merged output."""
        base_cols = [
            col
            for col in cblock.columns
            if not any(col.endswith(f"{var}_meas") for var in measured_vars)
        ] + ["sweep_var"]

        paired_cols: list[str] = []
        for var in measured_vars:
            meas_col = f"{var}_meas"
            if meas_col in merged.columns:
                paired_cols.append(meas_col)
            for corner in self.corners:
                sim_col = f"{var}_sim_{corner}"
                if sim_col in merged.columns:
                    paired_cols.append(sim_col)

        return [c for c in base_cols + paired_cols if c in merged.columns]

    def merge_with_clean(
        self, sim_results: pd.DataFrame, clean: pd.DataFrame | str | Path
    ) -> pd.DataFrame:
        """
        Merge sim results with measured clean data.

        Args:
            sim_results: DataFrame containing simulation results.
            clean: Either a DataFrame or path to CSV of measured data.

        Returns:
            DataFrame containing merged measured and simulated results.
        """
        clean_df = pd.read_csv(clean) if isinstance(clean, (str, Path)) else clean
        if clean_df.empty:
            logging.warning("Clean data is empty. Returning sim results only.")
            return sim_results

        clean_df = self._normalize_cols(clean_df).copy()

        # Map measured var names -> *_meas suffix
        sim_cols = [c for c in sim_results.columns if c.endswith("_sim_" + self.corners[0])]
        actual_output_vars = [c.replace(f"_sim_{self.corners[0]}", "") for c in sim_cols]

        rename_map = {var: f"{var}_meas" for var in actual_output_vars if var in clean_df.columns}
        if rename_map:
            clean_df = clean_df.rename(columns=rename_map)

        # Special case for BJT/PNP sweeps
        if self.device_type != "mos":
            sim_results["sweep_var"] = sim_results["sweep_var"].str[:2]

        return self._link_sim_to_clean(sim_results, clean_df)

    def _process_one_worker(
        self,
        args: Dict[str, Any],
    ) -> Tuple[int, Optional[pd.DataFrame], Optional[str]]:
        """
        Process a single row of sweep configuration by generating, simulating,
        and collecting results across all corners.

        Args:
            args (Dict[str, Any]): Worker input dictionary with required fields:
                - idx (int): Row index.
                - row_dict (dict): Row data with sweep and device parameters.
                - template_path (str | Path): Jinja2 template path.
                - workdir (str | Path): Temporary working directory.
                - corner_lib_path (str | Path): SPICE corner library path.
                - device_name (str): Subcircuit name.
                - device_type (str): Device family (mos, pnpmpa, hbt).
                - corners (list[str]): List of corners to simulate.
                - netlists_dir (str | Path, optional): Where to store rendered netlists.
                - osdi_path (str | Path, required for MOS): OSDI model file path.

        Returns:
            Tuple[int, Optional[pd.DataFrame], Optional[str]]:
                (row index, merged DataFrame of results, error message if any).
        """
        # -----------------
        # Argument unpacking
        # -----------------
        idx = args["idx"]
        row = pd.Series(args["row_dict"])
        template_path = Path(args["template_path"])
        workdir = Path(args["workdir"])
        corner_lib_path = Path(args["corner_lib_path"])
        device_name = args["device_name"]
        device_type = args["device_type"]
        corners = tuple(args["corners"])
        netlists_dir = Path(args["netlists_dir"]) if args.get("netlists_dir") else None
        osdi_path = Path(args["osdi_path"]) if device_type == "mos" else None

        # -----------------
        # Helpers
        # -----------------
        def fixed_or_zero(name: str) -> float:
            """Return sweep_start if this is sweep_var, otherwise parse numeric value."""
            return float(sweep_start) if name == sweep_var else parse_float(row.get(name, 0.0), 0.0)

        # -----------------
        # Sweep + block setup
        # -----------------
        sweep_config = DEVICE_SWEEP_MAPS[device_type]

        block_id = row.get("block_id", f"blk_{idx}")
        if pd.isna(block_id):
            block_id = f"blk_{idx}"

        temp = parse_float(row.get("temp", 27.0), 27.0)
        output_vars_str = row.get("output_vars")
        output_vars = [v.strip().lower() for v in str(output_vars_str).split(",")]

        # -----------------
        # Device parameters
        # -----------------
        params: Dict[str, Any] = {}
        if device_type == "mos":
            params.update({
                "W": parse_float(row.get("w", 1e-6), 1e-6),
                "L": parse_float(row.get("l", 1e-6), 1e-6),
                "AD": parse_float(row.get("ad", 0.0), 0.0),
                "AS": parse_float(row.get("as", 0.0), 0.0),
                "PD": parse_float(row.get("pd", 0.0), 0.0),
                "PS": parse_float(row.get("ps", 0.0), 0.0),
                "NF": parse_int(row.get("nf", 1), 1),
                "M": parse_int(row.get("m", 1), 1),
            })
        elif device_type == "pnpmpa":
            params.update({
                "A": parse_float(row.get("a", 2e-5), 2e-5),
                "P": parse_float(row.get("p", 2.4e-5), 2.4e-5),
            })
        elif device_type == "hbt":
            params.update({
                "M": parse_int(row.get("m", 1), 1),
                "W": parse_float(row.get("w", 1e-6), 1e-6),
                "L": parse_float(row.get("l", 1e-6), 1e-6),
                "Nx": parse_int(row.get("nx", 1), 1),
            })

        # -----------------
        # Sweep configuration
        # -----------------
        sweep_var = str(row.get("sweep_var", "")).strip().lower()
        if sweep_var not in sweep_config:
            return idx, None, f"Unsupported or missing sweep_var '{sweep_var}' for device '{device_type}'"

        try:
            sweep_start, sweep_stop, sweep_step = parse_sweep_triple(row.get(sweep_var[:2]))
        except Exception as e:
            return idx, None, f"Invalid sweep triple in '{sweep_var}': {e}"

        sweep_src, sweep_node = sweep_config[sweep_var]

        # -----------------
        # Bias conditions
        # -----------------
        if device_type == "mos":
            bias_conditions = {volt.upper(): fixed_or_zero(volt) for volt in ("vd", "vg", "vs", "vb")}
        else:
            bias_conditions = get_topology_params(row, sweep_var)
            input_vars_str = row.get("input_vars", "")
            if input_vars_str and pd.notna(input_vars_str):
                for var in [v.strip().lower() for v in str(input_vars_str).split(",")]:
                    if len(var) == 2 and var.startswith("i"):
                        bias_conditions[var] = parse_float(row[var], 0.0)
            bias_conditions["output_vars"] = output_vars

        # -----------------
        # Paths and template setup
        # -----------------
        sig = f"{idx}-dc-{block_id}-{device_type}"
        hsh = hashlib.sha1(sig.encode()).hexdigest()[:10]
        row_dir = workdir / f"job_{idx:06d}_{hsh}"
        row_dir.mkdir(parents=True, exist_ok=True)

        log_base = row_dir / "ngspice"
        netlist_base = row_dir / "test_dc"

        jenv = Environment(
            loader=FileSystemLoader(str(template_path.parent)),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        merged_df: Optional[pd.DataFrame] = None
        vcol = f"v({sweep_node[:2]})"

        # -----------------
        # Corner loop
        # -----------------
        for corner in corners:
            out_path = row_dir / f"wr_outputs_{corner}.csv"
            log_path = Path(f"{log_base}_{corner}.log")
            netlist_path = Path(f"{netlist_base}_{corner}.cir")

            ctx = {
                "model_corner_lib": str(corner_lib_path),
                "corner": corner,
                "TEMP": f"{temp}",
                "device_subckt": device_name,
                "out_path": str(out_path),
                "sweep_src": sweep_src,
                "sweep_node": sweep_node,
                "sweep_start": f"{sweep_start:.16g}",
                "sweep_stop": f"{sweep_stop:.16g}",
                "sweep_step": f"{sweep_step:.16g}",
                **{k: (f"{v:.16g}" if isinstance(v, float) else str(v)) for k, v in params.items()},
                **bias_conditions,
            }
            if osdi_path:
                ctx["osdi_path"] = str(osdi_path)

            # Render template and write netlist
            try:
                netlist_text = jenv.get_template(template_path.name).render(**ctx)
                netlist_path.write_text(netlist_text)
                if netlists_dir:
                    self._save_netlist(netlist_text, corner, block_id, str(row.get("source_file", "")))
            except Exception as e:
                shutil.rmtree(row_dir, ignore_errors=True)
                return idx, None, f"[{corner}] Template rendering failed: {e}"

            # Run simulation
            rc = sim_netlist_ngspice(netlist_path, log_path)
            if rc != 0:
                shutil.rmtree(row_dir, ignore_errors=True)
                return idx, None, f"[{corner}] ngspice failed (rc={rc})"

            df = read_wrdata_df(out_path)
            if df is None or df.empty:
                shutil.rmtree(row_dir, ignore_errors=True)
                return idx, None, f"[{corner}] Empty or missing wrdata output"

            # Extract outputs
            try:
                part_data = {"sweep_value": pd.to_numeric(df[vcol], errors="coerce")}
                for var in output_vars:
                    if var in df.columns:
                        part_data[f"{var}_sim_{corner}"] = pd.to_numeric(df[var], errors="coerce")
                    elif var.startswith("v") and f"v({var[1:]})" in df.columns:
                        part_data[f"{var}_sim_{corner}"] = pd.to_numeric(df[f"v({var[1:]})"], errors="coerce")
                    else:
                        part_data[f"{var}_sim_{corner}"] = pd.Series([float("nan")] * len(df))
                part = pd.DataFrame(part_data)
            except Exception as e:
                shutil.rmtree(row_dir, ignore_errors=True)
                return idx, None, f"[{corner}] Error building DataFrame: {e}"

            merged_df = part if merged_df is None else pd.merge(merged_df, part, on="sweep_value", how="outer")

        # -----------------
        # Final assembly
        # -----------------
        assert merged_df is not None
        merged_df = merged_df.sort_values("sweep_value").reset_index(drop=True)
        merged_df["block_id"] = block_id
        merged_df["sweep_var"] = sweep_var

        col_order = ["block_id", "sweep_var", "sweep_value"]
        for var in output_vars:
            col_order.extend([f"{var}_sim_{c}" for c in corners])

        out = merged_df[[c for c in col_order if c in merged_df.columns]].copy()
        shutil.rmtree(row_dir, ignore_errors=True)
        return idx, out, None


# -------------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------------

def _cli() -> None:
    """Command-line entry point for running ngspice DC sweeps across corners."""

    ap = argparse.ArgumentParser(
        description=(
            "Run ngspice DC sweeps for each row in a COMPACT-format CSV across "
            "corners, then optionally merge with measured data."
        )
    )
    ap.add_argument("-i", "--input", required=True, help="Path to input COMPACT CSV.")
    ap.add_argument("-o", "--output", required=True, help="Path to output merged CSV.")
    ap.add_argument(
        "--clean-csv",
        help="Optional measured CSV with block_id column for merging results.",
    )
    ap.add_argument(
        "--dc-template",
        required=True,
        help="Path to Jinja2 template file for DC sweep netlist generation.",
    )
    ap.add_argument(
        "--corner-lib",
        required=True,
        help="Path to corner library file (.lib).",
    )
    ap.add_argument(
        "--osdi",
        help="Path to PSP/OSDI model file (required for MOS devices).",
    )
    ap.add_argument(
        "--max-workers",
        type=int,
        default=os.cpu_count() or 4,
        help="Maximum number of parallel workers (default: CPU count).",
    )
    ap.add_argument(
        "--device",
        default="sg13_lv_nmos",
        help="Device subcircuit name in the netlist (default: sg13_lv_nmos).",
    )
    ap.add_argument(
        "--device-type",
        choices=list(DEVICE_SWEEP_MAPS.keys()),
        default="mos",
        help="Type of device to simulate (default: mos).",
    )
    ap.add_argument(
        "--netlists-dir",
        help="Optional directory to save generated netlists.",
    )

    args = ap.parse_args()

    # -------------------------------------------------------------------------
    # Validation helpers
    # -------------------------------------------------------------------------
    def require_path(path: Path, description: str) -> Path:
        if not path.exists():
            logging.error(f"{description} not found: {path}")
            sys.exit(2)
        return path

    # -------------------------------------------------------------------------
    # Input validation
    # -------------------------------------------------------------------------
    in_csv = require_path(Path(args.input), "Input CSV")
    template_path = require_path(Path(args.dc_template), "Template file")
    corner_lib_path = require_path(Path(args.corner_lib), "Corner library")

    osdi_path: Optional[Path] = None
    if args.device_type == "mos":
        if not args.osdi:
            logging.error("--osdi is required for MOS devices")
            sys.exit(2)
        osdi_path = require_path(Path(args.osdi), "OSDI file")

    # -------------------------------------------------------------------------
    # Load input CSV
    # -------------------------------------------------------------------------
    try:
        df = pd.read_csv(in_csv)
    except Exception as e:
        logging.error(f"Failed to read input CSV: {e}")
        sys.exit(2)

    if df.empty:
        logging.error("Input CSV is empty")
        sys.exit(2)

    netlists_dir = Path(args.netlists_dir) if args.netlists_dir else None

    # -------------------------------------------------------------------------
    # Run simulations
    # -------------------------------------------------------------------------
    runner = DcSweepRunner(
        template_path=template_path,
        osdi_path=osdi_path,
        corner_lib_path=corner_lib_path,
        max_workers=args.max_workers,
        device_name=args.device,
        device_type=args.device_type,
        netlists_dir=netlists_dir,
    )

    logging.info(
        f"Starting DC sweep: {df.shape[0]} rows x {len(df.columns)} columns "
        f"for device type '{args.device_type}' with up to {args.max_workers} workers."
    )

    sim_df, errors = runner.run(df)

    # -------------------------------------------------------------------------
    # Merge with measured data (optional)
    # -------------------------------------------------------------------------
    if args.clean_csv:
        final_df = runner.merge_with_clean(sim_df, args.clean_csv)
    else:
        final_df = sim_df

    # -------------------------------------------------------------------------
    # Save results
    # -------------------------------------------------------------------------
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path, index=False)

    # -------------------------------------------------------------------------
    # Reporting
    # -------------------------------------------------------------------------
    logging.info(f"Completed. Results written to: {output_path}")
    logging.info(f"  Total rows: {len(final_df)}")
    logging.info(f"  Successful simulations: {len(sim_df.groupby('block_id'))} blocks")

    if errors:
        logging.error(f"\nErrors occurred in {len(errors)} rows:")
        for rid, err in sorted(errors):
            sys.stderr.write(f"[row {rid}] {err}\n")
        logging.error(f"Failed rows: {len(errors)}")


if __name__ == "__main__":
    _cli()
