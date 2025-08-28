import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import subprocess

import pandas as pd

CORNERS_MOS = ("mos_tt", "mos_ss", "mos_ff")
CORNERS_BJT = ("hbt_typ", "hbt_bcs", "hbt_Wcs")
# sweep_var -> (voltage source name in netlist, node letter)
MOS_SWEEP_MAP: Dict[str, Tuple[str, str]] = {
    "vd": ("Vd", "d"),
    "vg": ("Vg", "g"),
    "vs": ("Vs", "s"),
    "vb": ("Vb", "b"),
}

BJT_SWEEP_MAP = {
    "vb": ("Vb", "b"),
    "vc": ("Vc", "c"),
    "ve": ("Ve", "e"),
    "vcb": ("Vcb", "c"),
    "vce": ("Vce", "c"),
    "vbe": ("Vbe", "b"),
}

SIM_TYPE_MAP: dict[str, str] = {
    "cbc": "cap",
    "cbe": "cap",
    "c_bd_perim": "cap",
    "c_g_ds": "cap",
    "di_bs_area": "current",
    "c_bs_perim": "cap",
    "c_d_g": "cap",
    "di_bs_perim": "current",
    "dc_idvd": "current",
    "c_oxide": "cap",
    "di_bd_area": "current",
    "di_bd_perim": "current",
    "c_bd_area": "cap",
    "c_bs_area": "cap",
    "c_g_dsb": "cap",
    "dc_idvg": "current",
}
DEVICE_SWEEP_MAPS = {
    "mos": MOS_SWEEP_MAP,
    "pnpmpa": BJT_SWEEP_MAP,
    "hbt": BJT_SWEEP_MAP,
}


def run_ngspice(netlist_path: Path, log_path: Path) -> int:
    env = os.environ.copy()
    env.setdefault("OMP_NUM_THREADS", "1")  # avoid oversubscription
    proc = subprocess.run(
        ["ngspice", "-b", "-o", str(log_path), str(netlist_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )
    return proc.returncode


def read_wrdata_df(out_path: Path) -> Optional[pd.DataFrame]:
    if not out_path.exists():
        return None
    df = pd.read_csv(out_path, sep=r"\s+", comment="*", engine="python")
    if df.empty:
        return None
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def parse_float(val, default: float = 0.0) -> float:
    try:
        if pd.isna(val):
            return float(default)
        return float(val)
    except Exception:
        return float(default)


def parse_int(val, default: int = 0) -> int:
    try:
        if pd.isna(val):
            return int(default)
        return int(val)
    except Exception:
        return int(default)


def parse_sweep_triple(triple_str: Any) -> Tuple[float, float, float]:
    """
    Expect a string like "start stop step". Tolerant to multiple spaces/commas.
    """
    if pd.isna(triple_str):
        raise ValueError("missing sweep triple")
    s = str(triple_str).strip().replace(",", " ")
    parts = [p for p in s.split() if p]
    if len(parts) != 3:
        raise ValueError(f"invalid sweep triple: {triple_str!r}")
    start, stop, step = map(float, parts)
    return start, stop, step


def expand_env(obj):
    """Expand ${VAR}, $VAR, and ~ in any str within nested lists/dicts."""
    if isinstance(obj, str):
        return os.path.expandvars(os.path.expanduser(obj))
    if isinstance(obj, list):
        return [expand_env(x) for x in obj]
    if isinstance(obj, dict):
        return {k: expand_env(v) for k, v in obj.items()}
    return obj


def get_topology_params(row: pd.Series, sweep_var: str) -> Dict[str, float]:
    """Return voltage parameters based on sweep variable and  topology."""

    def get_bias_value(field: str) -> float:
        return parse_float(row.get(field, 0.0), 0.0)

    sweep_map = {
        "vcb": ("VCB", "VE", "ve"),
        "vbe": ("VBE", "VC", "vc"),
        "vce": ("VCE", "VB", "vb"),
    }

    if sweep_var in sweep_map:
        swept_param_key, companion_param_key, source_field = sweep_map[sweep_var]
        return {swept_param_key: 0.0, companion_param_key: get_bias_value(source_field)}

    return {
        "VB": get_bias_value("vb"),
        "VC": get_bias_value("vc"),
        "VE": get_bias_value("ve"),
    }
