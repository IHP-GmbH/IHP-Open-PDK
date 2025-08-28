from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from models_verifier.dc_runner.helper import (
    CORNERS_BJT,
    CORNERS_MOS,
    DEVICE_SWEEP_MAPS,
    get_topology_params,
    parse_float,
    parse_int,
    parse_sweep_triple,
    read_wrdata_df,
    run_ngspice,
)


@dataclass
class DcSweepRunner:

    template_path: Path
    device_name: str
    corner_lib_path: Path
    osdi_path: Optional[Path] = None
    device_type: str = "mos"
    corners: Sequence[str] = None
    max_workers: int = max(1, os.cpu_count() or 4)
    netlists_dir: Optional[Path] = None

    def __post_init__(self):
        paths = [
            self.template_path,
            self.corner_lib_path,
            self.osdi_path,
        ]
        for p in paths:
            if isinstance(p, Path) and not p.exists():
                raise FileNotFoundError(f"Path not found: {p}")

        if self.device_type not in DEVICE_SWEEP_MAPS:
            raise ValueError(
                f"Unsupported device_type: {self.device_type}. "
                f"Supported types: {list(DEVICE_SWEEP_MAPS.keys())}"
            )
        self.corners = CORNERS_MOS if self.device_type == "mos" else CORNERS_BJT

        if self.netlists_dir:
            shutil.rmtree(self.netlists_dir, ignore_errors=True)
            self.netlists_dir.mkdir(parents=True, exist_ok=True)

    def _save_netlist(
        self, netlist_text: str, corner: str, block_id: str, source_file: str
    ) -> None:
        """
        Save the generated netlist to the netlists directory if specified.

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
        dump_path = self.netlists_dir / dump_name
        dump_path.write_text(netlist_text)

    @staticmethod
    def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    def run(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Tuple[int, str]]]:
        """
        Execute all sweeps in df in parallel. Returns (sim_df, errors).
        """
        df = self._normalize_cols(df).reset_index(drop=True)
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        workdir = Path(tempfile.mkdtemp(prefix="ngspice_sim_"))

        results: List[pd.DataFrame] = []
        errors: List[Tuple[int, str]] = []

        tasks: List[Dict[str, Any]] = []
        for idx, row in df.iterrows():
            tasks.append(
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
            )

        with ProcessPoolExecutor(max_workers=max(1, self.max_workers)) as ex:
            futs = [ex.submit(self._process_one_worker, t) for t in tasks]

            completed = 0
            for f in as_completed(futs):
                completed += 1
                rid, out_df, err = f.result()
                if err is not None or out_df is None:
                    errors.append((rid, err or "unknown error"))
                else:
                    results.append(out_df)

                if completed % 10 == 0 or completed == len(futs):
                    print(f"Processed {completed}/{len(futs)} ...")

        if not results:
            shutil.rmtree(workdir, ignore_errors=True)
            print(errors)
            raise RuntimeError("All simulations failed.")

        sim_df = pd.concat(results, ignore_index=True)
        sim_df = sim_df.sort_values(by=["block_id", "sweep_value"]).reset_index(
            drop=True
        )

        shutil.rmtree(workdir, ignore_errors=True)

        return sim_df, errors

    def _link_sim_to_clean(
        self,
        sim_results_df: pd.DataFrame,
        clean_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Merge sim results with clean data by block_id and sweep values.
        """
        if (
            "block_id" not in sim_results_df.columns
            or "block_id" not in clean_df.columns
        ):
            raise ValueError("Both DataFrames must contain a 'block_id' column.")

        out_blocks: List[pd.DataFrame] = []
        clean_groups = {bid: g for bid, g in clean_df.groupby("block_id")}

        for bid, sim_block in sim_results_df.groupby("block_id"):
            if bid not in clean_groups:
                print(f"Warning: block_id '{bid}' in sim, not in clean. Skipping.")
                continue
            cblock = clean_groups[bid].copy()
            if sim_block.empty or cblock.empty:
                continue

            sweep_var = sim_block["sweep_var"].iloc[0]
            if sweep_var not in cblock.columns:
                print(
                    f"Warning: sweep var '{sweep_var}' missing in clean for block '{bid}'. Skipping."
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
                print(
                    f"Warning: No matching sweep values for block '{bid}' after merge."
                )
                continue

            if "sweep_var" not in merged.columns:
                merged["sweep_var"] = sweep_var

            output_vars_str = merged["output_vars"].iloc[0]
            measured_vars = [v.strip() for v in output_vars_str.split(",")]

            base_cols = [col for col in cblock.columns] + ["sweep_var"]
            sim_cols = []

            for var in measured_vars:
                for corner in self.corners:
                    sim_col_name = f"{var}_sim_{corner}"
                    if sim_col_name in merged.columns:
                        sim_cols.append(sim_col_name)

            cols_to_keep = base_cols + sim_cols
            cols_to_keep = [c for c in cols_to_keep if c in merged.columns]

            merged = merged.sort_values(sweep_var).reset_index(drop=True)
            out_blocks.append(merged[cols_to_keep])

        if not out_blocks:
            print("Error: No matching block_ids to link. Returning empty DataFrame.")
            return pd.DataFrame()

        final_df = pd.concat(out_blocks, ignore_index=True)
        return final_df.sort_values("block_id").reset_index(drop=True)

    def merge_with_clean(
        self, sim_results: pd.DataFrame, clean: pd.DataFrame | str | Path
    ) -> pd.DataFrame:
        """
        Merge sim results with measured/clean data. Accepts DataFrame or CSV path.
        Requires 'block_id' in the clean data.
        """
        if isinstance(clean, (str, Path)):
            clean_df = pd.read_csv(clean)
        else:
            clean_df = clean

        if clean_df.empty:
            print("Warning: clean data is empty. Returning sim only.")
            return sim_results

        clean_df = self._normalize_cols(clean_df).copy()

        sim_cols = [
            col
            for col in sim_results.columns
            if col.endswith("_sim_" + self.corners[0])
        ]
        actual_output_vars = [
            col.replace(f"_sim_{self.corners[0]}", "") for col in sim_cols
        ]

        rename_map = {}
        for var in actual_output_vars:
            if var in clean_df.columns:
                rename_map[var] = f"{var}_meas"

        if rename_map:
            clean_df = clean_df.rename(columns=rename_map)

        if self.device_type != "mos":
            sim_results["sweep_var"] = sim_results["sweep_var"].str[:2]

        return self._link_sim_to_clean(sim_results, clean_df)

    def _process_one_worker(
        self,
        args: Dict[str, Any],
    ) -> Tuple[int, Optional[pd.DataFrame], Optional[str]]:
        """
        One row -> sweep across corners -> merged DataFrame for that row.
        Returns (row_idx, df_results, error_msg).
        """
        (
            idx,
            row_dict,
            template_path,
            workdir,
            corner_lib_path,
            device_name,
            device_type,
            corners,
            netlists_dir,
        ) = (
            args["idx"],
            args["row_dict"],
            Path(args["template_path"]),
            Path(args["workdir"]),
            Path(args["corner_lib_path"]),
            args["device_name"],
            args["device_type"],
            tuple(args["corners"]),
            Path(args["netlists_dir"]) if args["netlists_dir"] else None,  # NEW
        )
        if self.device_type == "mos":
            osdi_path = Path(args["osdi_path"])

        def fixed_or_zero(name: str) -> float:
            if name == sweep_var:
                return float(sweep_start)
            return parse_float(row.get(name, 0.0), 0.0)

        row = pd.Series(row_dict)
        sweep_config = DEVICE_SWEEP_MAPS[device_type]

        block_id = row.get("block_id", f"blk_{idx}")
        if pd.isna(block_id):
            block_id = f"blk_{idx}"

        temp = parse_float(row.get("temp", 27.0), 27.0)
        tnom = parse_float(row.get("tnom", 27.0), 27.0)

        output_vars_str = row.get("output_vars", "ib,ic,ie")
        output_vars = [v.strip().lower() for v in str(output_vars_str).split(",")]

        params = {}
        if device_type == "mos":
            params.update(
                {
                    "W": parse_float(row.get("w", 1e-6), 1e-6),
                    "L": parse_float(row.get("l", 1e-6), 1e-6),
                    "AD": parse_float(row.get("ad", 0.0), 0.0),
                    "AS": parse_float(row.get("as", 0.0), 0.0),
                    "PD": parse_float(row.get("pd", 0.0), 0.0),
                    "PS": parse_float(row.get("ps", 0.0), 0.0),
                    "NF": parse_int(row.get("nf", 1), 1),
                    "M": parse_int(row.get("m", 1), 1),
                }
            )
        elif device_type == "pnpmpa":
            params.update(
                {
                    "A": parse_float(row.get("a", 2e-5), 2e-5),
                    "P": parse_float(row.get("p", 2.4e-5), 2.4e-5),
                }
            )
        elif device_type == "hbt":
            params.update(
                {
                    "M": parse_int(row.get("m", 1), 1),
                    "W": parse_float(row.get("w", 1e-6), 1e-6),
                    "L": parse_float(row.get("l", 1e-6), 1e-6),
                    "Nx": parse_int(row.get("nx", 1), 1),
                }
            )
        sweep_var = str(row.get("sweep_var", "")).strip().lower()
        if sweep_var not in sweep_config:
            return (
                idx,
                None,
                f"unsupported or missing sweep_var '{sweep_var}' for device type '{device_type}'",
            )

        try:
            sweep_start, sweep_stop, sweep_step = parse_sweep_triple(
                row.get(sweep_var[:2])
            )
        except Exception as e:
            return (
                idx,
                None,
                f"cannot parse sweep triple from column '{sweep_var}': {e}",
            )

        sweep_src, sweep_node = sweep_config[sweep_var]
        bias_conditions = {}
        if device_type == "mos":
            for volt_name in ("vd", "vg", "vs", "vb"):
                bias_conditions[volt_name.upper()] = fixed_or_zero(volt_name)
        else:
            bias_conditions = get_topology_params(row, sweep_var)

            input_vars_str = row.get("input_vars", "")

            if input_vars_str and pd.notna(input_vars_str):
                inputs = [v.strip().lower() for v in str(input_vars_str).split(",")]
                for var in inputs:
                    if len(var) == 2 and var.startswith("i"):
                        bias_conditions[var] = parse_float(row[var], 0.0)

            bias_conditions["output_vars"] = output_vars

        sig = f"{idx}-dc-{block_id}-{device_type}"
        hsh = hashlib.sha1(sig.encode()).hexdigest()[:10]
        row_dir = workdir / f"job_{idx:06d}_{hsh}"
        row_dir.mkdir(parents=True, exist_ok=True)

        log_base = row_dir / "ngspice"
        netlist_base = row_dir / "test_dc"

        template_dir = template_path.parent
        template_name = template_path.name
        jenv = Environment(
            loader=FileSystemLoader(str(template_dir)),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        merged_df: Optional[pd.DataFrame] = None
        vcol = f"v({sweep_node[:2]})"

        for corner in corners:
            out_path = row_dir / f"wr_outputs_{corner}.txt"
            log_path = Path(f"{log_base}_{corner}.log")
            netlist_path = Path(f"{netlist_base}_{corner}.cir")

            ctx = {
                "model_corner_lib": str(corner_lib_path),
                "corner": corner,
                "TEMP": f"{temp}",
                "TNOM": f"{tnom}",
                "device_subckt": device_name,
                "out_path": str(out_path),
                "sweep_src": sweep_src,
                "sweep_node": sweep_node,
                "sweep_start": f"{sweep_start:.16g}",
                "sweep_stop": f"{sweep_stop:.16g}",
                "sweep_step": f"{sweep_step:.16g}",
            }
            for param, value in params.items():
                if isinstance(value, float):
                    ctx[param] = f"{value:.16g}"
                else:
                    ctx[param] = str(value)

            ctx.update(bias_conditions)
            if self.device_type == "mos":
                ctx["osdi_path"] = str(osdi_path)

            try:
                netlist_text = jenv.get_template(template_name).render(**ctx)
                netlist_path.write_text(netlist_text)

                if netlists_dir:
                    src = str(row.get("source_file", ""))
                    self._save_netlist(netlist_text, corner, block_id, src)

            except Exception as e:
                shutil.rmtree(row_dir, ignore_errors=True)
                return idx, None, f"[{corner}] template rendering failed: {e}"

            rc = run_ngspice(netlist_path, log_path)
            if rc != 0:
                shutil.rmtree(row_dir, ignore_errors=True)
                return idx, None, f"[{corner}] ngspice failed (rc={rc})"

            df = read_wrdata_df(out_path)
            if df is None or df.empty:
                shutil.rmtree(row_dir, ignore_errors=True)
                return idx, None, f"[{corner}] empty or missing wrdata output"

            try:
                part_data = {"sweep_value": pd.to_numeric(df[vcol], errors="coerce")}

                for var in output_vars:
                    if var in df.columns:
                        part_data[f"{var}_sim_{corner}"] = pd.to_numeric(
                            df[var], errors="coerce"
                        )
                    elif f"v({var[1:]})" in df.columns and var.startswith("v"):
                        part_data[f"{var}_sim_{corner}"] = pd.to_numeric(
                            df[f"v({var[1:]})"], errors="coerce"
                        )
                    else:
                        part_data[f"{var}_sim_{corner}"] = pd.Series(
                            [float("nan")] * len(df)
                        )
                part = pd.DataFrame(part_data)

            except Exception as e:
                shutil.rmtree(row_dir, ignore_errors=True)
                return idx, None, f"[{corner}] error building corner DataFrame: {e}"

            merged_df = (
                part
                if merged_df is None
                else pd.merge(merged_df, part, on="sweep_value", how="outer")
            )

        assert merged_df is not None
        merged_df = merged_df.sort_values(by=["sweep_value"]).reset_index(drop=True)
        merged_df["block_id"] = block_id
        merged_df["sweep_var"] = sweep_var

        col_order = ["block_id", "sweep_var", "sweep_value"]
        for var in output_vars:
            col_order.extend([f"{var}_sim_{c}" for c in corners])

        col_order = [c for c in col_order if c in merged_df.columns]
        out = merged_df[col_order].copy()

        shutil.rmtree(row_dir, ignore_errors=True)
        return idx, out, None


def _cli():
    ap = argparse.ArgumentParser(
        description=(
            "Run ngspice DC sweeps for each row in a COMPACT CSV "
            "across corners and optionally merge with measured data."
        )
    )
    ap.add_argument("-i", "--input", required=True, help="Input COMPACT sweep CSV.")
    ap.add_argument("-o", "--output", required=True, help="Output CSV (merged).")
    ap.add_argument(
        "--clean-csv",
        required=True,
        help="Optional measured CSV to merge with (must contain block_id).",
    )

    ap.add_argument(
        "--dc-template",
        required=True,
        help="Full path to DC sweep Jinja2 template file.",
    )

    ap.add_argument("--corner-lib", required=True, help="Path to corner lib (.lib).")
    ap.add_argument(
        "--osdi", required=False, help="Path to PSP/OSDI file for pre_osdi."
    )
    ap.add_argument(
        "--max-workers", type=int, default=os.cpu_count() or 4, help="Parallel workers."
    )
    ap.add_argument("--device", default="sg13_lv_nmos", help="Device subckt name.")
    ap.add_argument(
        "--device-type",
        choices=list(DEVICE_SWEEP_MAPS.keys()),
        default="mos",
        help="Device type: mos, pnpmpa, or hbt",
    )
    ap.add_argument(
        "--netlists-dir", help="Directory to save generated netlists (optional)."
    )

    args = ap.parse_args()

    in_csv = Path(args.input)
    if not in_csv.exists():
        print(f"Input CSV not found: {in_csv}", file=sys.stderr)
        sys.exit(2)

    template_path = Path(args.dc_template)
    if not template_path.exists():
        print(f"Template file not found: {template_path}", file=sys.stderr)
        sys.exit(2)

    osdi_path = None
    if args.device_type == "mos":
        if not args.osdi:
            print("--osdi is required for MOS devices", file=sys.stderr)
            sys.exit(2)
        osdi_path = Path(args.osdi)
        if not osdi_path.exists():
            print(" OSDI path not found", file=sys.stderr)
            sys.exit(2)
    corner_lib_path = Path(args.corner_lib)

    try:
        df = pd.read_csv(in_csv)
    except Exception as e:
        print(f"Error reading input CSV: {e}", file=sys.stderr)
        sys.exit(2)
    if df.empty:
        print("Input CSV is empty", file=sys.stderr)
        sys.exit(2)
    netlists_dir = Path(args.netlists_dir) if args.netlists_dir else None

    runner = DcSweepRunner(
        template_path=template_path,
        osdi_path=osdi_path,
        corner_lib_path=corner_lib_path,
        max_workers=args.max_workers,
        device_name=args.device,
        device_type=args.device_type,
        netlists_dir=netlists_dir,
    )

    print(
        f"Processing {df.shape} sweep rows for {args.device_type} device with up to {args.max_workers} workers..."
    )
    sim_df, errors = runner.run(df)

    if args.clean_csv:
        final_df = runner.merge_with_clean(sim_df, args.clean_csv)
    else:
        final_df = sim_df

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(args.output, index=False)

    if errors:
        print(f"\nErrors occurred in {len(errors)} :", file=sys.stderr)
        for rid, err in sorted(errors):
            sys.stderr.write(f"[row {rid}] {err}\n")

    print(f"\nCompleted! Wrote {args.output} with {len(final_df)} rows.")
    print(f"Successful simulations: {len(sim_df.groupby('block_id'))} blocks")
    if errors:
        print(f"Failed rows: {len(errors)}")


if __name__ == "__main__":
    _cli()
