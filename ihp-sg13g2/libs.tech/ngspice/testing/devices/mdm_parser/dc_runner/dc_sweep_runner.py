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
from mdm_parser.dc_runner.helper import (
    CORNERS,
    SWEEP_MAP,
    parse_float,
    parse_int,
    parse_sweep_triple,
    read_wrdata_df,
    run_ngspice,
)


@dataclass
class DcSweepRunner:

    template_path: Path
    model_lib_path: Path
    corner_lib_path: Path
    osdi_path: Path
    device_name: str
    corners: Sequence[str] = CORNERS
    max_workers: int = max(1, os.cpu_count() or 4)

    def __post_init__(self):
        for p in [
            self.template_path,
            self.model_lib_path,
            self.corner_lib_path,
            self.osdi_path,
        ]:
            if isinstance(p, Path) and not p.exists():
                raise FileNotFoundError(f"Path not found: {p}")

    @staticmethod
    def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    def run(
        self, df: pd.DataFrame, workdir: Optional[Path] = None
    ) -> Tuple[pd.DataFrame, List[Tuple[int, str]]]:
        """
        Execute all sweeps in df in parallel. Returns (sim_df, errors).
        """
        df = self._normalize_cols(df).reset_index(drop=True)
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        # Working directory
        owns_workdir = False
        if workdir is None:
            workdir = Path(tempfile.mkdtemp(prefix="ngspice_sim_"))
            owns_workdir = True
        else:
            workdir = Path(workdir)
            workdir.mkdir(parents=True, exist_ok=True)

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
                    model_lib_path=str(self.model_lib_path),
                    corner_lib_path=str(self.corner_lib_path),
                    osdi_path=str(self.osdi_path),
                    device_name=self.device_name,
                    corners=tuple(self.corners),
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
                    print(f"Processed {completed}/{len(futs)} jobs...")

        if not results:
            if owns_workdir:
                shutil.rmtree(workdir, ignore_errors=True)
            raise RuntimeError("All simulations failed.")

        sim_df = pd.concat(results, ignore_index=True)
        sim_df = sim_df.sort_values(by=["block_id", "sweep_value"]).reset_index(
            drop=True
        )

        if owns_workdir:
            shutil.rmtree(workdir, ignore_errors=True)

        return sim_df, errors

    @staticmethod
    def _link_sim_to_clean(
        sim_results_df: pd.DataFrame, clean_df: pd.DataFrame
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

            output_vars_str = (
                merged["output_vars"].iloc[0]
                if "output_vars" in merged.columns
                else "ib,id,ig,is"
            )
            measured_vars = [v.strip() for v in output_vars_str.split(",")]

            base_cols = [col for col in cblock.columns] + ["sweep_var"]
            sim_cols = []

            for var in measured_vars:
                for corner in CORNERS:
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
        # rename measured currents (if present) to *_meas
        rename_map = {}
        for col in ("ib", "id", "ig", "is"):
            if col in clean_df.columns:
                rename_map[col] = f"{col}_meas"

        if rename_map:
            clean_df = clean_df.rename(columns=rename_map)
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
            model_lib_path,
            corner_lib_path,
            osdi_path,
            device_name,
            corners,
        ) = (
            args["idx"],
            args["row_dict"],
            Path(args["template_path"]),
            Path(args["workdir"]),
            Path(args["model_lib_path"]),
            Path(args["corner_lib_path"]),
            Path(args["osdi_path"]),
            args["device_name"],
            tuple(args["corners"]),
        )

        row = pd.Series(row_dict)

        block_id = row.get("block_id", f"blk_{idx}")
        if pd.isna(block_id):
            block_id = f"blk_{idx}"

        tempC = parse_float(row.get("temp", 27.0), 27.0)
        W = parse_float(row.get("w", 1e-6), 1e-6)
        L = parse_float(row.get("l", 1e-6), 1e-6)
        AD = parse_float(row.get("ad", 0.0), 0.0)
        AS = parse_float(row.get("as", 0.0), 0.0)
        PD = parse_float(row.get("pd", 0.0), 0.0)
        PS = parse_float(row.get("ps", 0.0), 0.0)
        NF = parse_int(row.get("nf", 1), 1)
        M = parse_int(row.get("m", 1), 1)

        sweep_var = str(row.get("sweep_var", "")).strip().lower()
        if sweep_var not in SWEEP_MAP:
            return idx, None, f"unsupported or missing sweep_var '{sweep_var}'"

        try:
            sweep_start, sweep_stop, sweep_step = parse_sweep_triple(row.get(sweep_var))
        except Exception as e:
            return (
                idx,
                None,
                f"cannot parse sweep triple from column '{sweep_var}': {e}",
            )

        sweep_src, sweep_node = SWEEP_MAP[sweep_var]

        def fixed_or_zero(name: str) -> float:
            if name == sweep_var:
                return float(sweep_start)
            return parse_float(row.get(name, 0.0), 0.0)

        vd = fixed_or_zero("vd")
        vg = fixed_or_zero("vg")
        vs = fixed_or_zero("vs")
        vb = fixed_or_zero("vb")

        sig = f"{idx}-dc-{block_id}"
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
        vcol = f"v({sweep_node})"

        for corner in corners:
            out_path = row_dir / f"wr_outputs_{corner}.txt"
            log_path = Path(f"{log_base}_{corner}.log")
            netlist_path = Path(f"{netlist_base}_{corner}.cir")

            ctx = {
                "model_lib_path": str(model_lib_path),
                "model_corner_lib": str(corner_lib_path),
                "corner": corner,
                "osdi_path": str(osdi_path),
                "TEMP": f"{tempC}",
                "W": f"{W:.16g}",
                "L": f"{L:.16g}",
                "AD": f"{AD:.16g}",
                "AS": f"{AS:.16g}",
                "PD": f"{PD:.16g}",
                "PS": f"{PS:.16g}",
                "NF": f"{NF}",
                "M": f"{M}",
                "VD": f"{vd:.16g}",
                "VS": f"{vs:.16g}",
                "VG": f"{vg:.16g}",
                "VB": f"{vb:.16g}",
                "device_subckt": device_name,
                "out_path": str(out_path),
                "sweep_src": sweep_src,
                "sweep_node": sweep_node,
                "sweep_start": f"{sweep_start:.16g}",
                "sweep_stop": f"{sweep_stop:.16g}",
                "sweep_step": f"{sweep_step:.16g}",
            }

            try:
                netlist_text = jenv.get_template(template_name).render(**ctx)
                netlist_path.write_text(netlist_text)
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
                part = pd.DataFrame(
                    {
                        "sweep_value": pd.to_numeric(df[vcol], errors="coerce"),
                        f"ib_sim_{corner}": pd.to_numeric(
                            df.get("ib", pd.Series([float("nan")] * len(df))),
                            errors="coerce",
                        ),
                        f"id_sim_{corner}": pd.to_numeric(
                            df.get("id", pd.Series([float("nan")] * len(df))),
                            errors="coerce",
                        ),
                        f"ig_sim_{corner}": pd.to_numeric(
                            df.get("ig", pd.Series([float("nan")] * len(df))),
                            errors="coerce",
                        ),
                        f"is_sim_{corner}": pd.to_numeric(
                            df.get("is", pd.Series([float("nan")] * len(df))),
                            errors="coerce",
                        ),
                    }
                )
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

        col_order = (
            ["block_id", "sweep_var", "sweep_value"]
            + [f"ib_sim_{c}" for c in corners]
            + [f"id_sim_{c}" for c in corners]
            + [f"ig_sim_{c}" for c in corners]
            + [f"is_sim_{c}" for c in corners]
        )
        col_order = [c for c in col_order if c in merged_df.columns]
        out = merged_df[col_order].copy()

        shutil.rmtree(row_dir, ignore_errors=True)
        return idx, out, None


def _cli():
    ap = argparse.ArgumentParser(
        description=(
            "Run ngspice DC sweeps for each row in a COMPACT CSV "
            f"across corners {','.join(CORNERS)} and optionally merge with measured data."
        )
    )
    ap.add_argument("-i", "--input", required=True, help="Input COMPACT sweep CSV.")
    ap.add_argument(
        "-o", "--output", required=True, help="Output CSV (merged or sims-only)."
    )
    ap.add_argument(
        "--clean-csv",
        help="Optional measured CSV to merge with (must contain block_id).",
    )

    ap.add_argument(
        "--dc-template",
        required=True,
        help="Full path to DC sweep Jinja2 template file.",
    )

    ap.add_argument("--model-lib", required=True, help="Path to model lib (.include).")
    ap.add_argument("--corner-lib", required=True, help="Path to corner lib (.lib).")
    ap.add_argument("--osdi", required=True, help="Path to PSP/OSDI file for pre_osdi.")
    ap.add_argument(
        "--max-workers", type=int, default=os.cpu_count() or 4, help="Parallel workers."
    )
    ap.add_argument("--workdir", help="Working dir (default: temp).")
    ap.add_argument("--device", default="sg13_lv_nmos", help="Device subckt name.")

    args = ap.parse_args()

    in_csv = Path(args.input)
    if not in_csv.exists():
        print(f"Input CSV not found: {in_csv}", file=sys.stderr)
        sys.exit(2)

    template_path = Path(args.dc_template)
    if not template_path.exists():
        print(f"Template file not found: {template_path}", file=sys.stderr)
        sys.exit(2)

    model_lib_path = Path(args.model_lib)
    corner_lib_path = Path(args.corner_lib)
    osdi_path = Path(args.osdi)

    for p in (model_lib_path, corner_lib_path, osdi_path):
        if not p.exists():
            print(f"Path not found: {p}", file=sys.stderr)
            sys.exit(2)

    try:
        df = pd.read_csv(in_csv)
    except Exception as e:
        print(f"Error reading input CSV: {e}", file=sys.stderr)
        sys.exit(2)
    if df.empty:
        print("Input CSV is empty", file=sys.stderr)
        sys.exit(2)

    runner = DcSweepRunner(
        template_path=template_path,
        model_lib_path=model_lib_path,
        corner_lib_path=corner_lib_path,
        osdi_path=osdi_path,
        max_workers=args.max_workers,
        device_name=args.device,
    )

    print(f"Processing {df.shape} sweep rows with up to {args.max_workers} workers...")
    sim_df, errors = runner.run(
        df, workdir=Path(args.workdir) if args.workdir else None
    )

    if args.clean_csv:
        final_df = runner.merge_with_clean(sim_df, args.clean_csv)
    else:
        final_df = sim_df

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(args.output, index=False)

    if errors:
        print(f"\nErrors occurred in {len(errors)} jobs:", file=sys.stderr)
        for rid, err in sorted(errors):
            sys.stderr.write(f"[row {rid}] {err}\n")

    print(f"\nCompleted! Wrote {args.output} with {len(final_df)} rows.")
    print(f"Successful simulations: {len(sim_df.groupby('block_id'))} blocks")
    if errors:
        print(f"Failed rows: {len(errors)}")


if __name__ == "__main__":
    _cli()
