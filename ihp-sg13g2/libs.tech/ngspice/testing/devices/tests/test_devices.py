from pathlib import Path
import pandas as pd
import pytest

from mdm_parser.mdm_verifier import MdmVerifier

CASES = [
    ("nmos_lv", "mos/nmos_lv/sg13_lv_nmos.yaml"),
    ("pmos_lv", "mos/pmos_lv/sg13_lv_pmos.yaml"),
    ("nmos_hv", "mos/nmos_hv/sg13_hv_nmos.yaml"),
    ("pmos_hv", "mos/pmos_hv/sg13_hv_pmos.yaml"),
    ("pnp_mpa", "pnp_mpa/pnpmpa.yaml"),
    ("npn13g2", "hbt/npn13g2/npn13g2.yaml"),
    ("npn13g2l", "hbt/npn13g2l/npn13g2l.yaml"),
    ("npn13g2v", "hbt/npn13g2v/npn13g2v.yaml"),
]


@pytest.mark.parametrize("label, rel_yaml", CASES, ids=[c[0] for c in CASES])
def test_devices(label, rel_yaml):
    test_dir = Path(__file__).parent    
    cfg_path = test_dir.parent / rel_yaml
    assert cfg_path.exists(), f"Config YAML not found: {cfg_path}"

    verifier = MdmVerifier(cfg_path)

    dfs = verifier._build_merged_dataframes()
    assert dfs, f"No merged {label.upper()} DataFrames returned"
    merged_df = pd.concat(dfs, ignore_index=True)
    assert not merged_df.empty, f"Merged {label.upper()} DataFrame is empty"

    rc = verifier._build_range_checker()
    report_df, _ = rc.analyze(merged_df)

    rc.assert_all_pass(report_df, targets=("meas", "tt"))