import numpy as np
from scipy.interpolate import interp1d

def pointwise_rel_err(bm_arr: np.ndarray, arr: np.ndarray, atol: float = 1e-16) -> np.ndarray:
    denom = np.maximum(np.abs(bm_arr), np.ones_like(bm_arr) * atol)
    return np.abs(arr - bm_arr) / denom

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
