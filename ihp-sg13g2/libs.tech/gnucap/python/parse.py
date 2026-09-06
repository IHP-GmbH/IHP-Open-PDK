from typing import List
from io import StringIO
import numpy as np

def filter_data(filepath: str, skip_prefixes) -> str:

    with open(filepath, "r") as f:
        filtered_data = "".join(line for line in f if not line.lstrip().startswith(skip_prefixes))

    return filtered_data

def split_nested_sweep(
    data_arr: np.ndarray,
    data_col_idx_list: List[int],
    inner_sweep_col_idx: int = 0,
    outer_sweep_col_idx: int = 1,
    ):

    inner_sweep_arr = data_arr[:, inner_sweep_col_idx]
    inner_sweep_arr, idx = np.unique(inner_sweep_arr, return_index=True)
    inner_sweep_arr = inner_sweep_arr[np.argsort(idx)]
    outer_sweep_arr, idx = np.unique(np.round(data_arr[:, outer_sweep_col_idx], 10), return_index=True)
    outer_sweep_arr = outer_sweep_arr[np.argsort(idx)]

    split_data_list = []

    for v in outer_sweep_arr:
        idx_arr = np.round(data_arr[:, outer_sweep_col_idx], 10) == v
        sweep_data_list = []
        for cold_idx in data_col_idx_list:
            sweep_data_list.append(data_arr[idx_arr, cold_idx])

        split_data_list.append(np.squeeze(np.array(sweep_data_list)))

    return split_data_list, inner_sweep_arr, outer_sweep_arr

def split_mc_trials(data_arr: np.ndarray, col_idx: int = 0) -> List[np.ndarray]:
    if data_arr.size == 0:
        return []

    idx_trial_start = np.flatnonzero(np.diff(data_arr[:, col_idx]) < 0) + 1
    return np.array(np.split(data_arr, idx_trial_start))


















