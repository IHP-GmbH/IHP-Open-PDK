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

import argparse
import logging
import uuid
from pathlib import Path
from typing import Literal, Optional, List, Dict, Set
import pandas as pd

from models_verifier.mdm_processing.utils import (
    get_dut_params,
    setup_global_logging,
    extract_data_blocks,
    extract_section,
    parse_data_block,
    parse_design_parameters,
    parse_header_inputs,
    infer_step,
    derive_master_setup_type_from_filename,
    derive_sweep_var,
)

setup_global_logging()


class MdmParseError(Exception):
    """Custom exception for MDM parsing errors."""

    pass


class MdmParser:
    """
    MDM file parser
    """

    def __init__(
        self, filepath: Path, device_type: Literal["mos", "pnpmpa", "hbt"] = "mos"
    ):
        self.filepath = Path(filepath)
        self.dataframe = pd.DataFrame()
        self.input_columns: List[str] = []
        self.output_columns: List[str] = []
        self.compact_rows: List[Dict[str, object]] = []
        self.block_metadata: Dict[int, Dict] = {}
        self.device_type = device_type
        if self.device_type not in ("mos", "pnpmpa", "hbt"):
            raise ValueError(f"Unsupported device type: {device_type}")
        self._validate_input()

    def _validate_input(self) -> None:
        """Validate input file exists and is readable."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Input file not found: {self.filepath}")

        if not self.filepath.is_file():
            raise ValueError(f"Path is not a file: {self.filepath}")

    def _generate_block_id(self) -> str:
        """Generate a unique block ID using UUID for guaranteed uniqueness."""
        return str(uuid.uuid4())

    def parse(self) -> pd.DataFrame:
        """
        Parse the MDM file and return combined DataFrame (point-by-point).
        Also builds self.compact_rows (one per DB block) for compact mode.
        """
        try:
            logging.info(f"Parsing MDM file: {self.filepath}")

            content = self.filepath.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()

            # Extract header section
            header_lines, header_end_idx = extract_section(
                lines, "BEGIN_HEADER", "END_HEADER"
            )
            if not header_lines:
                raise MdmParseError("No header section found")

            if header_end_idx == -1:
                raise MdmParseError("END_HEADER not found")

            body_lines = lines[header_end_idx:]

            # Parse header information
            input_variables = parse_header_inputs(header_lines)
            design_parameters = parse_design_parameters(header_lines, self.device_type)

            logging.info(
                f"Found {len(input_variables)} input variables and {len(design_parameters)} design parameters"
            )
            if self.device_type != "mos":
                design_parameters["MASTER_SETUP_TYPE"] = (
                    derive_master_setup_type_from_filename(self.filepath)
                )
            if self.device_type == "pnpmpa":
                design_parameters["A"], design_parameters["P"] = get_dut_params(
                    self.filepath
                )

            input_names = list(input_variables)
            self.input_columns = input_names

            block_dataframes: List[pd.DataFrame] = []
            cumulative_output_names: Set[str] = set()
            self.compact_rows.clear()
            self.block_metadata.clear()

            block_index = 0
            for block_lines in extract_data_blocks(body_lines):
                block_metadata, block_df = parse_data_block(
                    block_lines, input_variables
                )

                if block_df.empty:
                    logging.debug("Skipping empty block")
                    continue

                block_id = self._generate_block_id()

                self.block_metadata[block_index] = {
                    "block_id": block_id,
                    "block_index": block_index,
                    **block_metadata,
                    **design_parameters,
                }

                block_output_names = [
                    c for c in block_df.columns if c not in input_names
                ]
                cumulative_output_names.update(block_output_names)

                block_df = block_df.assign(
                    block_id=block_id, block_index=block_index, **block_metadata
                )
                block_dataframes.append(block_df)

                try:
                    sweep_var = block_df.columns[0]  # first column after '#'
                    sweep_vals = pd.to_numeric(
                        block_df.iloc[:, 0], errors="coerce"
                    ).dropna()
                    start = float(sweep_vals.iloc[0]) if not sweep_vals.empty else None
                    stop = float(sweep_vals.iloc[-1]) if not sweep_vals.empty else None
                    step = infer_step(sweep_vals.values) if len(sweep_vals) > 1 else 0.0

                    row_compact: Dict[str, object] = {}

                    row_compact["block_id"] = block_id
                    row_compact["block_index"] = block_index

                    for k, v in design_parameters.items():
                        row_compact[k] = v

                    if start is None or stop is None:
                        sweep_triple = ""
                    else:
                        sweep_triple = f"{start:.16g} {stop:.16g} {step:.16g}"

                    for in_name in input_names:
                        if in_name == sweep_var:
                            row_compact[in_name] = sweep_triple

                        else:
                            val = block_metadata.get(in_name, None)
                            if val is None or str(val).lower() == sweep_var.lower():
                                row_compact[in_name] = sweep_triple
                                sweep_var = derive_sweep_var(sweep_var, in_name)
                            else:
                                row_compact[in_name] = val
                    row_compact["sweep_var"] = sweep_var
                    row_compact["input_vars"] = ",".join(input_names)
                    row_compact["output_vars"] = ",".join(
                        sorted(cumulative_output_names)
                    )
                    self.compact_rows.append(row_compact)
                except Exception as e:
                    logging.error(
                        f"Could not build compact row for block {block_index}: {e}"
                    )

                block_index += 1

            if not block_dataframes:
                raise MdmParseError("No data blocks with valid data found")

            logging.info(f"Successfully parsed {len(block_dataframes)} data blocks")

            full_df = pd.concat(block_dataframes, ignore_index=True)

            full_df = full_df.assign(**design_parameters)
            self.output_columns = sorted(cumulative_output_names)
            full_df["input_vars"] = ",".join(input_names)
            full_df["output_vars"] = ",".join(self.output_columns)

            self.dataframe = full_df
            return self.dataframe

        except Exception as e:
            raise MdmParseError(f"Failed to parse MDM file: {e}") from e

    def to_csv(self, output_dir: Optional[Path] = None) -> Path:
        """
        Export parsed data to CSV file (point-by-point, long).
        """
        if self.dataframe.empty:
            logging.info("parsing file first")
            self.parse()

        if output_dir is None:
            output_path = self.filepath.with_suffix(".csv")
        else:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{self.filepath.stem}.csv"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.dataframe.to_csv(output_path, index=False, float_format="%.16g")
        logging.info(f"Exported {len(self.dataframe)} rows to: {output_path}")
        return output_path

    def to_compact_csv(self, output_dir: Optional[Path] = None) -> Path:
        """
        Export one-row-per-DB-block compact CSV.
        Columns:
          - block_id, block_index (for linking)
          - design params (W,L,NF,M,AD,AS,PD,PS,TEMP,MASTER_SETUP_TYPE) if present
          - all input variables (swept one as 'start stop step', others as scalars)
          - sweep_var
        """
        if not self.compact_rows:
            self.parse()

        dfc = pd.DataFrame(self.compact_rows)

        design_cols_pref = [
            "W",
            "L",
            "NF",
            "M",
            "AD",
            "AS",
            "PD",
            "PS",
            "TEMP",
            "MASTER_SETUP_TYPE",
        ]
        design_cols = [c for c in design_cols_pref if c in dfc.columns]
        input_cols = [c for c in self.input_columns if c in dfc.columns]
        trailing = ["sweep_var"] if "sweep_var" in dfc.columns else []
        other_cols = [
            c
            for c in dfc.columns
            if c not in set(["block_id"] + design_cols + input_cols + trailing)
        ]

        ordered = ["block_id"] + design_cols + input_cols + other_cols + trailing
        dfc = dfc.reindex(columns=ordered)

        if output_dir is None:
            output_path = self.filepath.with_suffix(".compact.csv")
        else:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{self.filepath.stem}.compact.csv"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        dfc.to_csv(output_path, index=False, float_format="%.16g")
        logging.info(
            f"Exported compact sweep CSV with {len(dfc)} rows to: {output_path}"
        )
        return output_path


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Parse IC-CAP MDM files to CSV format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-i", "--input", type=Path, required=True, help="Input MDM file path"
    )
    parser.add_argument(
        "-od", "--output-dir", type=Path, help="Directory for all output CSV files"
    )
    parser.add_argument(
        "-d",
        "--device-type",
        choices=["mos", "pnpmpa", "hbt"],
        default="mos",
        help="Device type: guides which ICCAP_VALUES to prefer and how to order compact columns",
    )

    args = parser.parse_args()

    try:
        mdm_parser = MdmParser(args.input, device_type=args.device_type)

        long_path = mdm_parser.to_csv(args.output_dir)
        compact_path = mdm_parser.to_compact_csv(args.output_dir)
        print("Successfully converted to:")
        print(f"  Long format: {long_path}")
        print(f"  Compact format: {compact_path}")

    except (FileNotFoundError, ValueError, MdmParseError) as e:
        logging.error(e)
        return 1
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
