import numpy as np
from scipy.interpolate import interp1d

def pointwise_rel_err(
        bm_arr: np.ndarray,
        arr: np.ndarray,
        atol: float = 1e-16,
        rtol: float = 1e-6,
) -> np.ndarray:
    denom = np.maximum(np.abs(bm_arr), np.ones_like(bm_arr) * atol)
    rel_err = np.abs(arr - bm_arr) / denom
    zero_threshold = rtol * (np.max(bm_arr) - np.min(bm_arr))
    rel_err[np.abs(bm_arr) <= zero_threshold] = np.nan
    return rel_err

def align_time_series(
        t_arr: np.ndarray,
        v_arr: np.ndarray,
        t_ref_arr: np.ndarray,
        kind: str = 'linear',
) -> np.ndarray:

    assert t_arr.min() <= t_ref_arr.min(), "Reference time range exceeds original time range (min)."
    assert t_arr.max() >= t_ref_arr.max(), "Reference time range exceeds original time range (max)."

    # Interpolate the values at the reference time points
    v_interp_arr = interp1d(t_arr, v_arr, kind=kind)(t_ref_arr)

    return v_interp_arr

def round_significant(values: np.ndarray, digits: int) -> np.ndarray:

    rounded = values.copy()
    nonzero = rounded != 0
    scale = 10 ** np.floor(np.log10(np.abs(rounded[nonzero])))
    rounded[nonzero] = np.round(rounded[nonzero] / scale, digits - 1) * scale
    return rounded
