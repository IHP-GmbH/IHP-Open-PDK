# =========================================================================================
# Copyright 2025 IHP PDK Authors
#
# Licensed under the the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
# =========================================================================================

import argparse
import logging
import sys
import uuid
from pathlib import Path
from typing import Literal, Optional, List, Dict, Set

import pandas as pd

from models_verifier.mdm_processing.utils import (
    get_dut_params,
    extract_data_blocks,
    extract_section,
    parse_data_block,
    parse_design_parameters,
    parse_header_inputs,
    infer_step,
    derive_master_setup_type_from_filename,
    derive_sweep_var,
    setup_global_logging,
)


# =========================================================================================
# Exceptions
# =========================================================================================

class MdmParseError(Exception):
    """Raised when parsing an MDM file fails."""


# =========================================================================================
# Parser
# =========================================================================================

class MdmParser:
    """Parser for IC-CAP `.mdm` files producing long-format and compact CSV exports."""

    def __init__(self, filepath: Path, device_type: Literal["mos", "pnpmpa", "hbt"] = "mos"):
        """
        Args:
            filepath (Path): Path to the MDM file.
            device_type (str): Device type, influences parsing rules.
        """
        self.filepath = Path(filepath)
        self.device_type = device_type

        self.dataframe: pd.DataFrame = pd.DataFrame()
        self.input_columns: List[str] = []
        self.output_columns: List[str] = []
        self.compact_rows: List[Dict[str, object]] = []
        self.block_metadata: Dict[int, Dict] = {}

        if self.device_type not in {"mos", "pnpmpa", "hbt"}:
            raise ValueError(f"Unsupported device type: {device_type}")

        self._validate_input()

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def _validate_input(self) -> None:
        """Ensure input file exists and is readable."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Input file not found: {self.filepath}")
        if not self.filepath.is_file():
            raise ValueError(f"Path is not a file: {self.filepath}")

    # -------------------------------------------------------------------------
    # Parsing
    # -------------------------------------------------------------------------

    def _generate_block_id(self) -> str:
        """Return a unique block identifier."""
        return str(uuid.uuid4())

    def parse(self) -> pd.DataFrame:
        """
        Parse the MDM file.

        Returns:
            pd.DataFrame: Long-format data (point-by-point).
        """
        try:
            logging.info("Parsing MDM file: %s", self.filepath)

            # Load file
            content = self.filepath.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            # Extract header
            header_lines, header_end_idx = extract_section(lines, "BEGIN_HEADER", "END_HEADER")
            if not header_lines or header_end_idx == -1:
                raise MdmParseError("Header section missing or incomplete")

            body_lines = lines[header_end_idx:]

            # Parse header
            input_vars = parse_header_inputs(header_lines)
            design_params = parse_design_parameters(header_lines, self.device_type)

            if self.device_type != "mos":
                design_params["MASTER_SETUP_TYPE"] = derive_master_setup_type_from_filename(self.filepath)
            if self.device_type == "pnpmpa":
                design_params["A"], design_params["P"] = get_dut_params(self.filepath)

            self.input_columns = list(input_vars)

            # Process blocks
            block_dfs: List[pd.DataFrame] = []
            cumulative_outputs: Set[str] = set()
            self.compact_rows.clear()
            self.block_metadata.clear()

            for idx, block_lines in enumerate(extract_data_blocks(body_lines)):
                block_meta, block_df = parse_data_block(block_lines, input_vars)
                if block_df.empty:
                    continue

                block_id = self._generate_block_id()
                self.block_metadata[idx] = {**block_meta, **design_params,
                                            "block_id": block_id, "block_index": idx}

                # Track outputs
                outputs = [c for c in block_df.columns if c not in input_vars]
                cumulative_outputs.update(outputs)

                # Augment block data
                block_df = block_df.assign(block_id=block_id, block_index=idx, **block_meta)
                block_dfs.append(block_df)

                # Build compact representation
                try:
                    self._build_compact_row(idx, block_id, block_df, input_vars,
                                            design_params, cumulative_outputs)
                except Exception as e:
                    logging.error("Compact row build failed for block %d: %s", idx, e)

            if not block_dfs:
                raise MdmParseError("No valid data blocks found")

            full_df = pd.concat(block_dfs, ignore_index=True).assign(**design_params)
            self.output_columns = sorted(cumulative_outputs)
            full_df["input_vars"] = ",".join(self.input_columns)
            full_df["output_vars"] = ",".join(self.output_columns)

            self.dataframe = full_df
            logging.info("Parsed %d blocks successfully", len(block_dfs))
            return self.dataframe

        except Exception as e:
            raise MdmParseError(f"Failed to parse {self.filepath}: {e}") from e

    def _build_compact_row(
        self,
        idx: int,
        block_id: str,
        block_df: pd.DataFrame,
        input_vars: List[str],
        design_params: Dict,
        outputs: Set[str],
    ) -> None:
        """Construct a compact row summarizing a block sweep."""
        sweep_var = block_df.columns[0]
        sweep_vals = pd.to_numeric(block_df.iloc[:, 0], errors="coerce").dropna()

        start = float(sweep_vals.iloc[0]) if not sweep_vals.empty else None
        stop = float(sweep_vals.iloc[-1]) if not sweep_vals.empty else None
        step = infer_step(sweep_vals.values) if len(sweep_vals) > 1 else 0.0

        row = {"block_id": block_id, "block_index": idx, **design_params}
        sweep_str = "" if start is None or stop is None else f"{start:.16g} {stop:.16g} {step:.16g}"

        for name in input_vars:
            if name == sweep_var:
                row[name] = sweep_str
            else:
                val = self.block_metadata[idx].get(name, None)
                if val is None or str(val).lower() == sweep_var.lower():
                    row[name] = sweep_str
                    sweep_var = derive_sweep_var(sweep_var, name)
                else:
                    row[name] = val

        row["sweep_var"] = sweep_var
        row["input_vars"] = ",".join(input_vars)
        row["output_vars"] = ",".join(sorted(outputs))
        self.compact_rows.append(row)

    # -------------------------------------------------------------------------
    # Export
    # -------------------------------------------------------------------------

    def to_csv(self, output_dir: Optional[Path]) -> Path:
        """Export parsed data (long format) to CSV."""
        if self.dataframe.empty:
            self.parse()

        output_dir = output_dir or self.filepath.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{self.filepath.stem}.csv"

        self.dataframe.to_csv(output_path, index=False, float_format="%.16g")
        logging.info("Exported %d rows → %s", len(self.dataframe), output_path)
        return output_path

    def to_compact_csv(self, output_dir: Optional[Path]) -> Path:
        """Export block-wise compact summary to CSV."""
        if not self.compact_rows:
            self.parse()

        dfc = pd.DataFrame(self.compact_rows)

        # Column ordering
        design_pref = ["W", "L", "NF", "M", "AD", "AS", "PD", "PS", "TEMP", "MASTER_SETUP_TYPE"]
        design_cols = [c for c in design_pref if c in dfc.columns]
        input_cols = [c for c in self.input_columns if c in dfc.columns]
        trailing = ["sweep_var"] if "sweep_var" in dfc.columns else []
        other = [c for c in dfc.columns if c not in {"block_id", *design_cols, *input_cols, *trailing}]
        ordered = ["block_id"] + design_cols + input_cols + other + trailing
        dfc = dfc.reindex(columns=ordered)

        output_dir = output_dir or self.filepath.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{self.filepath.stem}.compact.csv"

        dfc.to_csv(output_path, index=False, float_format="%.16g")
        logging.info("Exported compact sweep CSV (%d rows) → %s", len(dfc), output_path)
        return output_path


# =========================================================================================
# CLI
# =========================================================================================

def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Parse IC-CAP MDM files into CSV (long and compact formats)."
    )
    parser.add_argument("-i", "--input", type=Path, required=True, help="Input MDM file path")
    parser.add_argument("-od", "--output-dir", type=Path, help="Directory for CSV/log outputs")
    parser.add_argument("-d", "--device-type", choices=["mos", "pnpmpa", "hbt"],
                        default="mos", help="Device type (affects parsing rules)")
    args = parser.parse_args()

    # Setup logging
    output_dir = args.output_dir or Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = output_dir / "mdm_parser.log"
    setup_global_logging(log_file)

    try:
        parser = MdmParser(args.input, args.device_type)
        long_csv = parser.to_csv(output_dir)
        compact_csv = parser.to_compact_csv(output_dir)
        print("Successfully converted:")
        print(f"  Long CSV    → {long_csv}")
        print(f"  Compact CSV → {compact_csv}")
        return 0
    except (FileNotFoundError, ValueError, MdmParseError) as e:
        logging.error("%s", e)
        return 1
    except KeyboardInterrupt:
        logging.warning("Operation cancelled by user")
        return 1
    except Exception:
        logging.exception("Unexpected error")
        return 1


if __name__ == "__main__":
    sys.exit(main())
