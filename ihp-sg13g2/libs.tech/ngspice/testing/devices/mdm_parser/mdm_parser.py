#!/usr/bin/env python3
"""
 IC-CAP MDM file parser with improved performance and cleaner structure.

Usage:
    python mdm_parser.py -i input.mdm -o output.csv
    python mdm_parser.py -i input.mdm  # outputs to input.csv
"""

import argparse
import logging
from pathlib import Path
from typing import Optional
import pandas as pd
from mdm_parser_utils import (
    setup_global_logging,
    extract_data_blocks,
    extract_section,
    parse_data_block,
    parse_design_parameters,
    parse_header_inputs,
)

setup_global_logging()


class MdmParseError(Exception):
    """Custom exception for MDM parsing errors."""

    pass


class MdmParser:
    """
    MDM file parser
    """

    def __init__(self, filepath: Path):
        self.filepath = Path(filepath)
        self.dataframe = pd.DataFrame()
        self._validate_input()

    def _validate_input(self) -> None:
        """Validate input file exists and is readable."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Input file not found: {self.filepath}")

        if not self.filepath.is_file():
            raise ValueError(f"Path is not a file: {self.filepath}")

    def parse(self) -> pd.DataFrame:
        """
        Parse the MDM file and return combined DataFrame.

        Returns:
            Combined DataFrame with all data blocks

        Raises:
            MdmParseError: If parsing fails
        """
        try:
            logging.info(f"Parsing MDM file: {self.filepath}")

            # Read file with error handling
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
            design_parameters = parse_design_parameters(header_lines)

            logging.info(
                f"Found {len(input_variables)} input variables and {len(design_parameters)} design parameters"
            )

            # Process data blocks
            block_dataframes = []

            for block_lines in extract_data_blocks(body_lines):
                block_metadata, block_df = parse_data_block(
                    block_lines, input_variables
                )

                if block_df.empty:
                    logging.debug(f"Skipping empty block ")
                    continue
                
                block_df = block_df.assign(**block_metadata)
                block_dataframes.append(block_df)

            if not block_dataframes:
                raise MdmParseError("No data blocks with valid data found")

            logging.info(f"Successfully parsed {len(block_dataframes)} data blocks")

            full_df = pd.concat(block_dataframes, ignore_index=True)

            # Now add the same design parameters to every row at once
            full_df = full_df.assign(**design_parameters)

            self.dataframe = full_df
            return self.dataframe

        except Exception as e:
            raise MdmParseError(f"Failed to parse MDM file: {e}") from e

    def to_csv(self, output_path: Optional[Path] = None) -> Path:
        """
        Export parsed data to CSV file.

        Args:
            output_path: Output CSV path (defaults to input filename with .csv extension)

        Returns:
            Path to the created CSV file
        """
        if self.dataframe.empty:
            logging.info("parsing file first")
            self.parse()

        if output_path is None:
            output_path = self.filepath.with_suffix(".csv")
        else:
            output_path = Path(output_path)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Export to CSV with  settings
        self.dataframe.to_csv(output_path, index=False, float_format="%.6g")

        logging.info(f"Exported {len(self.dataframe)} rows to: {output_path}")
        return output_path


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Parse IC-CAP MDM files to CSV format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python mdm_parser.py -i data.mdm -o output.csv
    python mdm_parser.py -i data.mdm  # outputs to data.csv
        """,
    )

    parser.add_argument(
        "-i", "--input", type=Path, required=True, help="Input MDM file path"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output CSV file path (default: input filename with .csv extension)",
    )

    args = parser.parse_args()

    try:
        mdm_parser = MdmParser(args.input)
        output_path = mdm_parser.to_csv(args.output)

        print(f"Successfully convertedto {output_path}")

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
