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

from pathlib import Path
import pandas as pd
import pytest

from models_verifier.models_verifier import MdmVerifier
from models_verifier.constants import CASES


@pytest.mark.parametrize("label, rel_yaml", CASES, ids=[c[0] for c in CASES])
def test_devices(label, rel_yaml):
    test_dir = Path(__file__).parent
    cfg_path = test_dir.parent / rel_yaml

    assert cfg_path.exists(), f"Config YAML not found: {cfg_path,Path.cwd()}"

    verifier = MdmVerifier(cfg_path)

    dfs = verifier._build_merged_dataframes()
    assert dfs, f"No merged {label.upper()} DataFrames returned"
    merged_df = pd.concat(dfs, ignore_index=True)
    assert not merged_df.empty, f"Merged {label.upper()} DataFrame is empty"

    rc = verifier._build_range_checker()
    report_df, _ = rc.analyze(merged_df)

    rc.assert_all_pass(report_df, targets=("meas", "tt"))
