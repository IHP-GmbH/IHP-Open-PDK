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
import logging
import os
import re
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, Union

import pandas as pd

from models_verifier.mdm_processing.parser import MdmParser, MdmParseError
from models_verifier.mdm_processing.utils import (
    setup_global_logging,
    normalize_master_setup_type,
    safe_name,
)

# -----------------------------------------------------------------------------------------
# Global logger
# -----------------------------------------------------------------------------------------
logger = logging.getLogger(__name__)


# =========================================================================================
# Helper
# =========================================================================================
def clean_group_item(
    item: Tuple[Optional[str], pd.DataFrame],
    device_type: Literal["mos", "pnpmpa", "hbt"] = "mos",
) -> Tuple[Optional[str], pd.DataFrame]:
    """
    Post-process a grouped DataFrame: remove empty columns and reorder.

    Args:
        item: (master_setup_type, DataFrame)
        device_type: Device type ("mos", "pnpmpa", "hbt")

    Returns:
        Tuple of (master_setup_type, cleaned DataFrame)
    """
    mtype, df = item
    out = MdmDirectoryAggregator._drop_all_empty_columns(df)
    out = MdmDirectoryAggregator.reorder_columns(out, device_type)
    return mtype, out


# =========================================================================================
# Aggregator
# =========================================================================================
class MdmDirectoryAggregator:
    """
    Aggregate many `.mdm` files into structured DataFrames grouped by master_setup_type.

    Features:
    - Supports recursive directory scanning
    - Produces both full (long) and compact representations
    - Optional CSV output (per master_setup_type)
    - Handles MOS, PNPMPA, and HBT device types

    Typical usage:
    --------------
        aggregator = MdmDirectoryAggregator("/path/to/mdm/files")
        full_by_type, compact_by_type = aggregator.aggregate()

        # With CSV output
        aggregator = MdmDirectoryAggregator(
            "/path/to/mdm/files",
            output_dir="/path/to/output",
            create_csvs=True
        )
        full_by_type, compact_by_type = aggregator.aggregate()
    """

    def __init__(
        self,
        input_dir: Union[str, Path],
        recursive: bool = True,
        *,
        output_dir: Optional[Union[str, Path]] = None,
        create_csvs: bool = False,
        device_type: Literal["mos", "pnpmpa", "hbt"] = "mos",
    ):
        self.input_dir = Path(input_dir)
        self.recursive = recursive
        self.output_dir = Path(output_dir) if output_dir is not None else None
        self.create_csvs = create_csvs
        self.device_type = device_type

        if not self.input_dir.exists() or not self.input_dir.is_dir():
            raise NotADirectoryError(f"Input path must be a directory: {self.input_dir}")

        if self.create_csvs and self.output_dir is None:
            raise ValueError("output_dir must be provided when create_csvs=True")

        if self.output_dir and self.create_csvs:
            self.output_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------------------
    # Column handling
    # -------------------------------------------------------------------------------------
    @staticmethod
    def reorder_columns(df: pd.DataFrame, device_type: str) -> pd.DataFrame:
        """
        Reorder columns into a canonical order:
          1. Identifiers
          2. Device-specific parameters
          3. Input variables
          4. Output variables
          5. Remaining metadata/debug columns
        """
        if df is None or df.empty:
            return df

        primary = [
            "block_id", "block_index", "source_file",
            "input_vars", "output_vars",
            "master_setup_type", "TNOM", "TEMP",
        ]
        design_params_map = {
            "mos": ["W", "L", "AD", "AS", "PD", "PS", "NF", "M"],
            "pnpmpa": ["A", "P"],
            "hbt": ["W", "L", "M", "Nx"],
        }
        design_params = design_params_map.get(device_type.lower(), [])

        input_vars, output_vars = [], []
        for _, row in df.iterrows():
            if pd.notna(row.get("input_vars")):
                input_vars = [v.strip() for v in str(row["input_vars"]).split(",")]
                break
        for _, row in df.iterrows():
            if pd.notna(row.get("output_vars")):
                output_vars = [v.strip() for v in str(row["output_vars"]).split(",")]
                break

        cols = list(df.columns)
        planned, seen = [], set()

        def add(seq):
            for c in seq:
                if c in df.columns and c not in seen:
                    planned.append(c)
                    seen.add(c)

        add(primary)
        add(design_params)
        add(input_vars + output_vars)
        add([c for c in cols if c not in seen])

        return df.reindex(columns=planned)

    @staticmethod
    def _drop_all_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Drop columns that are fully empty (NaN or stripped empty strings).
        """
        if df is None or df.empty:
            return df

        for col in df.select_dtypes(include=["object"]).columns:
            s = df[col]
            is_str = s.notna() & s.map(lambda x: isinstance(x, str))
            if is_str.any():
                try:
                    trimmed = s.where(~is_str, s[is_str].str.strip())
                    trimmed = trimmed.mask(is_str & (trimmed == ""), pd.NA)
                    df[col] = trimmed
                except Exception as e:
                    logger.warning(f"Could not clean column {col}: {e}")

        return df.dropna(axis=1, how="all")

    # -------------------------------------------------------------------------------------
    # File parsing
    # -------------------------------------------------------------------------------------
    def _process_one(
        self, path: Path
    ) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        Parse one .mdm file into (full_df, compact_df).
        """
        try:
            parser = MdmParser(path, device_type=self.device_type)
            full_df = parser.parse()
            compact_df = pd.DataFrame(parser.compact_rows) if parser.compact_rows else None

            results: List[Optional[pd.DataFrame]] = []
            for df in (full_df, compact_df):
                if df is None or df.empty:
                    results.append(None)
                    continue

                df["source_file"] = path.name
                if "MASTER_SETUP_TYPE" in df.columns:
                    df["master_setup_type"] = df.pop("MASTER_SETUP_TYPE").map(normalize_master_setup_type)
                else:
                    df["master_setup_type"] = None
                results.append(df)

            return tuple(results)

        except (FileNotFoundError, ValueError, MdmParseError) as e:
            logger.warning(f"Skip {path}: {e}")
            return None, None
        except Exception as e:
            logger.exception(f"Unexpected error parsing {path}: {e}")
            return None, None

    # -------------------------------------------------------------------------------------
    # File I/O
    # -------------------------------------------------------------------------------------
    def _write_by_type(self, by_type, suffix: str, label: str) -> int:
        """Write grouped DataFrames to CSV."""
        if not by_type:
            return 0

        total_rows = 0

        def _write_one(item):
            mtype, df = item
            out = df.drop(columns=["master_setup_type"], errors="ignore")
            if out.empty or out.shape[1] == 0:
                return 0
            fpath = self.output_dir / f"{safe_name(mtype)}_{suffix}.csv"
            out.to_csv(fpath, index=False)
            logger.info(f"Wrote {len(out):6d} {label} rows → {fpath.name}")
            return len(out)

        with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as ex:
            for n in ex.map(_write_one, by_type.items()):
                total_rows += n

        logger.info(f"Wrote {total_rows} {label} rows to {self.output_dir}")
        return total_rows

    # -------------------------------------------------------------------------------------
    # Discovery
    # -------------------------------------------------------------------------------------
    def find_mdm_files(self) -> List[Path]:
        """
        Find all `.mdm` files under input_dir, applying device-specific filters.
        """
        iterator = self.input_dir.rglob("*.mdm") if self.recursive else self.input_dir.glob("*.mdm")
        is_pnp = self.device_type.lower() == "pnpmpa"
        skip_duts = {3, 5, 9, 13, 14, 15}
        dut_re = re.compile(r"(?i)dut(\d+)")

        return sorted(
            p for p in iterator
            if p.is_file()
            and not p.name.lower().startswith(("dummy", "spar", "contact", "ftfmax", "h21gu"))
            and not (is_pnp and (m := dut_re.search(p.name)) and int(m.group(1)) in skip_duts)
        )

    # -------------------------------------------------------------------------------------
    # Main aggregation
    # -------------------------------------------------------------------------------------
    def aggregate(self) -> Tuple[Dict[Optional[str], pd.DataFrame], Dict[Optional[str], pd.DataFrame]]:
        """Aggregate all found `.mdm` files into grouped DataFrames."""
        files = self.find_mdm_files()
        if not files:
            raise FileNotFoundError("No .mdm files found.")

        logger.info(f"Found {len(files)} MDM files...")

        frames_full, frames_compact = [], []
        with ProcessPoolExecutor(max_workers=max(1, os.cpu_count() or 4)) as ex:
            for full_df, compact_df in ex.map(self._process_one, files):
                if full_df is not None and not full_df.empty:
                    frames_full.append(full_df)
                if compact_df is not None and not compact_df.empty:
                    frames_compact.append(compact_df)

        def build_by_type(frames):
            if not frames:
                return {}
            df = pd.concat(frames, ignore_index=True, sort=False)
            if "master_setup_type" not in df.columns:
                df["master_setup_type"] = None
            df["master_setup_type"] = pd.Categorical(df["master_setup_type"])
            return {mtype: g.copy() for mtype, g in df.groupby("master_setup_type", dropna=False, observed=False)}

        full_by_type = build_by_type(frames_full)
        compact_by_type = build_by_type(frames_compact)

        # Clean
        cleaner = partial(clean_group_item, device_type=self.device_type)
        with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as ex:
            full_by_type = dict(ex.map(cleaner, full_by_type.items()))
            compact_by_type = dict(ex.map(cleaner, compact_by_type.items()))

        # Write CSVs if requested
        if self.create_csvs:
            n_full = self._write_by_type(full_by_type, "clean", "full")
            n_compact = self._write_by_type(compact_by_type, "sweep", "compact")
            if not (n_full or n_compact):
                logger.warning("No CSV files were written.")
            else:
                logger.info(f"Done. Output directory: {self.output_dir}")

        return full_by_type, compact_by_type

    # -------------------------------------------------------------------------------------
    def get_summary(self) -> Dict[str, Union[int, str, bool]]:
        """Quick summary of input files without full parsing."""
        return {
            "total_files": len(self.find_mdm_files()),
            "input_directory": str(self.input_dir),
            "recursive_search": self.recursive,
        }


# =========================================================================================
# CLI
# =========================================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate `.mdm` files into grouped DataFrames and optional CSVs."
    )
    parser.add_argument("-i", "--input", type=Path, required=True, help="Directory containing .mdm files")
    parser.add_argument("-o", "--output", type=Path, default=Path("all_measurements"),
                        help="Output directory (default: ./all_measurements)")
    parser.add_argument("--no-recursive", action="store_true", help="Do not scan subdirectories")
    parser.add_argument("--show-csvs", action="store_true", help="Write grouped CSVs")
    parser.add_argument("-d", "--device-type", choices=["mos", "pnpmpa", "hbt"],
                        default="mos", help="Device type (affects parsing and column order)")
    args = parser.parse_args()

    # Setup logging
    log_file = args.output / "mdm_parser.log"
    setup_global_logging(log_file)

    try:
        aggregator = MdmDirectoryAggregator(
            input_dir=args.input,
            recursive=not args.no_recursive,
            output_dir=args.output,
            device_type=args.device_type,
            create_csvs=args.show_csvs,
        )
        summary = aggregator.get_summary()
        logger.info(f"Processing {summary['total_files']} files from {summary['input_directory']}")

        full_by_type, compact_by_type = aggregator.aggregate()

        total_types = len(set(full_by_type) | set(compact_by_type))
        total_full = sum(len(df) for df in full_by_type.values())
        total_compact = sum(len(df) for df in compact_by_type.values())

        print("\nSummary:")
        print(f"  Distinct master_setup_types: {total_types}")
        print(f"  Total full rows: {total_full}")
        print(f"  Total compact rows: {total_compact}")
        if args.show_csvs:
            print(f"  Output directory: {args.output}")
        else:
            print("  (use --show-csvs to save grouped CSVs)")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
