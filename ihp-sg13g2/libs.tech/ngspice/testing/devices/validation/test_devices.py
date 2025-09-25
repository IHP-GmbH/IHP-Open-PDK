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
Device-Level Model Validation Tests for IHP SG13G2 PDK
=======================================================

This test suite validates the consistency and correctness of device model
implementations using the `models_verifier` framework.

Each device is associated with a YAML configuration file that defines:
    - The model under test
    - Simulation setup (stimuli, sweeps, corners)
    - Expected behavior and tolerances

The tests perform the following checks for every device:
    1. Ensure the configuration file exists.
    2. Use MdmVerifier to generate merged simulation DataFrames.
    3. Validate that merged data is non-empty and properly structured.
    4. Run the RangeChecker to analyze results against reference targets.
    5. Assert that all range checks pass for key targets ("meas", "tt").

Usage
-----
Run all device tests using pytest:

    python3 -m pytest validation/test_devices.py --tb=short -p no:capture

Run tests for a specific device only:

    python3 -m pytest validation/test_devices.py -k "nmos_lv" --tb=short -p no:capture

Run with verbose output:

    python3 -m pytest -v validation/test_devices.py --tb=short -p no:capture
"""

from pathlib import Path
import pandas as pd
import pytest

from models_verifier.models_verifier import MdmVerifier
from models_verifier.constants import CASES

@pytest.mark.parametrize("label, rel_yaml", CASES, ids=[c[0] for c in CASES])
def test_devices(label: str, rel_yaml: str) -> None:
    """
    Parametrized test for device model validation.

    Parameters
    ----------
    label : str
        Short identifier for the device under test (e.g., "nmos_lv").
    rel_yaml : str
        Relative path to the YAML configuration file defining the test.

    Test Flow
    ---------
    1. Locate and validate the device configuration file.
    2. Initialize MdmVerifier with the configuration.
    3. Build merged simulation DataFrames from the test cases.
    4. Assert that the DataFrames are non-empty and valid.
    5. Run the RangeChecker to evaluate parameter ranges.
    6. Ensure all required checks ("meas", "tt") pass.

    Assertions
    ----------
    - Configuration file must exist.
    - Merged DataFrames must be created and non-empty.
    - RangeChecker analysis must pass without violations.
    """
    # ----------------------------------------------------------------------
    # Locate the YAML configuration file for the current test case
    # ----------------------------------------------------------------------
    test_dir = Path(__file__).parent
    cfg_path = test_dir.parent / rel_yaml

    assert cfg_path.exists(), (
        f"❌ Config YAML not found for {label.upper()}.\n"
        f"Expected at: {cfg_path}\n"
        f"Current working directory: {Path.cwd()}"
    )

    # ----------------------------------------------------------------------
    # Initialize verifier for the device under test
    # ----------------------------------------------------------------------
    verifier = MdmVerifier(cfg_path)

    # ----------------------------------------------------------------------
    # Step 1: Build merged simulation DataFrames
    # ----------------------------------------------------------------------
    dfs = verifier._build_merged_dataframes(create_csvs=False)
    assert dfs, f"❌ No merged DataFrames returned for {label.upper()}"

    merged_df = pd.concat(dfs, ignore_index=True)
    assert not merged_df.empty, f"❌ Merged DataFrame is empty for {label.upper()}"

    # ----------------------------------------------------------------------
    # Step 2: Run RangeChecker analysis
    # ----------------------------------------------------------------------
    rc = verifier._build_range_checker()
    report_df, _ = rc.analyze(merged_df)

    # ----------------------------------------------------------------------
    # Step 3: Assert that all checks pass for "meas" and "tt" targets
    # ----------------------------------------------------------------------
    rc.assert_all_pass(
        report_df,
        targets=("meas", "tt"),
    )
