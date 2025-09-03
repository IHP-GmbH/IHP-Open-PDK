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
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import logging
import os
from pathlib import Path
import re
from typing import Dict, List, Literal, Optional, Tuple, Union

import pandas as pd

from models_verifier.mdm_processing.parser import MdmParser, MdmParseError
from models_verifier.mdm_processing.utils import (
    setup_global_logging,
    normalize_master_setup_type,
    safe_name,
)

setup_global_logging()
logger = logging.getLogger(__name__)


def clean_group_item(
    item: Tuple[Optional[str], pd.DataFrame],
) -> Tuple[Optional[str], pd.DataFrame]:

    mtype, df = item
    out = MdmDirectoryAggregator._drop_all_empty_columns(df)
    return mtype, out


class MdmDirectoryAggregator:
    """
    Aggregate many MDM files into DataFrames grouped by master_setup_type.

    Can optionally write CSV files
    Usage:
        aggregator = MdmDirectoryAggregator("/path/to/mdm/files")
        full_by_type, compact_by_type = aggregator.aggregate()

        # Or with CSV output:
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
        """
        Initialize the aggregator.

        Args:
            input_dir: Directory containing .mdm files
            recursive: Whether to search subdirectories
            output_dir: Directory for CSV output (required if create_csvs=True)
            create_csvs: Whether to write CSV files
        """
        self.input_dir = Path(input_dir)
        self.recursive = recursive
        self.output_dir = Path(output_dir) if output_dir is not None else None
        self.create_csvs = create_csvs
        self.device_type = device_type
        if not self.input_dir.exists() or not self.input_dir.is_dir():
            raise NotADirectoryError(
                f"Input path must be a directory: {self.input_dir}"
            )

        if self.create_csvs and self.output_dir is None:
            raise ValueError("output_dir must be provided when create_csvs=True")

        if self.output_dir is not None and self.create_csvs:
            self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _drop_all_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            return df

        obj_cols = df.select_dtypes(include=["object"]).columns
        for col in obj_cols:
            s = df[col]
            is_str = s.notna() & s.map(lambda x: isinstance(x, str))
            if is_str.any():
                try:
                    trimmed = s.where(~is_str, s[is_str].str.strip())
                    trimmed = trimmed.mask(is_str & (trimmed == ""), pd.NA)
                    df[col] = trimmed
                except (TypeError, AttributeError) as e:
                    logger.warning(f"Could not process column {col}: {e}")
                    continue

        return df.dropna(axis=1, how="all")

    def _process_one(
        self, path: Path
    ) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        Parse one .mdm file and return (full_df, compact_df).

        Returns:
            Tuple of (full DataFrame, compact DataFrame), either may be None
        """
        try:
            parser = MdmParser(path, device_type=self.device_type)
            full_df = parser.parse()
            compact_df = (
                pd.DataFrame(parser.compact_rows)
                if getattr(parser, "compact_rows", None)
                else None
            )

            results: List[Optional[pd.DataFrame]] = []
            for df in (full_df, compact_df):
                if df is None or df.empty:
                    results.append(None)
                    continue

                df["source_file"] = path.name

                df["master_setup_type"] = (
                    df.pop("MASTER_SETUP_TYPE").map(normalize_master_setup_type)
                    if "MASTER_SETUP_TYPE" in df.columns
                    else None
                )
                results.append(df)

            return tuple(results)

        except (FileNotFoundError, ValueError, MdmParseError) as e:
            logger.warning(f"Skip {path}: {e}")
            return None, None
        except Exception as e:
            logger.exception(f"Unexpected error parsing {path}: {e}")
            return None, None

    def _write_by_type(self, by_type, suffix, label):
        if not by_type:
            return 0
        total_rows = 0

        def _write_one(item):
            mtype, df = item
            out = df.copy()
            out = out.drop(columns=["master_setup_type"], errors="ignore")
            if out.empty or out.shape[1] == 0:
                return 0
            fpath = self.output_dir / f"{safe_name(mtype)}_{suffix}.csv"
            with open(fpath, "w", buffering=1024 * 1024) as fh:
                out.to_csv(fh, index=False)
            logger.info(f"  wrote {len(out):6d} {label} rows -> {fpath.name}")
            return len(out)

        max_workers = min(8, os.cpu_count() or 4)
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            for n in ex.map(_write_one, by_type.items()):
                total_rows += n
        logger.info(f"Wrote {total_rows} {label} rows under: {self.output_dir}")
        return total_rows

    def find_mdm_files(self) -> List[Path]:
        iterator = (
            self.input_dir.rglob("*.mdm")
            if self.recursive
            else self.input_dir.glob("*.mdm")
        )

        is_pnp = str(self.device_type).lower() == "pnpmpa"
        skip_duts = {3, 5, 9, 13, 14, 15}
        dut_re = re.compile(r"(?i)dut(\d+)")

        return sorted(
            p
            for p in iterator
            if p.is_file()
            and not p.name.lower().startswith(
                ("dummy", "spar", "contact", "ftfmax", "h21gu")
            )
            and not (
                is_pnp and (m := dut_re.search(p.name)) and int(m.group(1)) in skip_duts
            )
        )

    def aggregate(
        self,
    ) -> Tuple[Dict[Optional[str], pd.DataFrame], Dict[Optional[str], pd.DataFrame]]:
        files = self.find_mdm_files()
        if not files:
            raise FileNotFoundError("No .mdm files found.")

        logger.info(f"Found {len(files)} MDM files...")

        frames_full: List[pd.DataFrame] = []
        frames_compact: List[pd.DataFrame] = []

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
            by_type = {
                mtype: g.copy()
                for mtype, g in df.groupby(
                    "master_setup_type", sort=False, observed=True, dropna=False
                )
            }
            return by_type

        full_by_type = build_by_type(frames_full)
        compact_by_type = build_by_type(frames_compact)
        max_workers = min(8, os.cpu_count() or 4)
        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            full_by_type = dict(ex.map(clean_group_item, full_by_type.items()))
        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            compact_by_type = dict(ex.map(clean_group_item, compact_by_type.items()))

        if self.create_csvs:
            n_full = self._write_by_type(full_by_type, "clean", "full")
            n_compact = self._write_by_type(compact_by_type, "sweep", "compact")
            if n_full == 0 and n_compact == 0:
                logger.warning("No CSV files were written.")
            else:
                logger.info(f"Done. Output directory: {self.output_dir}")
        return full_by_type, compact_by_type

    def get_summary(self) -> Dict[str, int]:
        """Get a summary of files and potential data without full processing."""
        files = self.find_mdm_files()
        return {
            "total_files": len(files),
            "input_directory": str(self.input_dir),
            "recursive_search": self.recursive,
        }


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Aggregate .mdm files under a directory into per-type CSVs (full and compact)"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Directory to scan (recursively) for .mdm files",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("all_measurements"),
        help="Output directory for per-type CSVs (default: ./all_measurements)",
    )
    parser.add_argument(
        "--no-recursive", action="store_true", help="Do not scan subdirectories"
    )
    parser.add_argument("--show-csvs", action="store_true", help="Write per-type CSVs")
    parser.add_argument(
        "-d",
        "--device-type",
        choices=["mos", "pnpmpa", "hbt"],
        default="mos",
        help="Device type: guides which ICCAP_VALUES to prefer and how to order compact columns",
    )
    args = parser.parse_args()

    try:
        output_dir = args.output
        aggregator = MdmDirectoryAggregator(
            input_dir=args.input,
            recursive=not args.no_recursive,
            output_dir=output_dir,
            device_type=args.device_type,
            create_csvs=args.show_csvs,
        )

        summary = aggregator.get_summary()
        logger.info(
            f"Processing {summary['total_files']} files from {summary['input_directory']}"
        )

        full_by_type, compact_by_type = aggregator.aggregate()

        total_types = len(set(full_by_type.keys()) | set(compact_by_type.keys()))
        total_full_rows = sum(len(df) for df in full_by_type.values())
        total_compact_rows = sum(len(df) for df in compact_by_type.values())

        print("\nSummary:")
        print(f"  Found {total_types} distinct master_setup_types")
        print(f"  Total full rows: {total_full_rows}")
        print(f"  Total compact rows: {total_compact_rows}")
        if args.show_csvs:
            print(f"  Output directory: {output_dir}")
        else:
            print("use --show-csvs to save the output as csv ")

        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
