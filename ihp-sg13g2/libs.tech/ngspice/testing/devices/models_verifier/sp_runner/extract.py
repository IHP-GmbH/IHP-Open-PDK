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
Milestone M4 -- shared CjE / CjC / fT extraction from a 2-port network.

Both the MEASURED side (S_deemb columns from the MDM, converted S->Y with scikit-rf) and
the SIMULATED side (ngspice AC 2-port Y) reduce to the same Y(f) array, and are then fed
through the *identical* extraction functions here so the meas-vs-sim comparison is
apples-to-apples.

Port convention: port 1 = base, port 2 = collector, common emitter.

Equations (from GOAL_DEV_VER.md "Reference Data" / M4_RECON.md), Y in siemens, f in Hz::

    CjE = Im(Y11 + Y12) / (2*pi*f)                 averaged over ALL frequencies
    CjC = -0.5 * Im(Y21 + Y12) / (2*pi*f)          averaged over 0.5-5 GHz
    fT  = |H21| * f,  H21 = Y21 / Y11              averaged over ~30 GHz rolloff band

`fT` uses the ideal single-pole assumption |H21|*f ~ const in the -20 dB/dec rolloff
region; we average |H21|*f over a band centered on 30 GHz (robust "extrapolate at 30 GHz").
"""

from __future__ import annotations

from typing import Optional

import numpy as np

# Frequency bands (Hz).
_CJC_BAND = (0.5e9, 5.0e9)
_FT_BAND = (20.0e9, 40.0e9)   # centered on 30 GHz per the extrapolation recipe

METRICS = ("cje", "cjc", "ft")


def s_to_y(freq: np.ndarray, s: np.ndarray, z0: float = 50.0) -> np.ndarray:
    """
    Convert a 2-port S array (nf, 2, 2) to Y (siemens) using scikit-rf.

    scikit-rf is imported lazily so importing this module never hard-fails if the
    optional dep is missing on the sim-only path (sim already produces Y directly).
    """
    import skrf

    net = skrf.Network(f=np.asarray(freq, dtype=float), s=np.asarray(s, dtype=complex), z0=z0)
    return net.y


def _band_mask(freq: np.ndarray, lo: float, hi: float) -> np.ndarray:
    m = (freq >= lo) & (freq <= hi)
    if not m.any():  # degenerate: no points in band -> use all points
        m = np.ones_like(freq, dtype=bool)
    return m


def extract_cje(freq: np.ndarray, y: np.ndarray) -> float:
    """CjE (F) = mean over all f of Im(Y11 + Y12) / (2*pi*f)."""
    freq = np.asarray(freq, dtype=float)
    w = 2.0 * np.pi * freq
    cje_f = np.imag(y[:, 0, 0] + y[:, 0, 1]) / w
    return float(np.mean(cje_f))


def extract_cjc(freq: np.ndarray, y: np.ndarray) -> float:
    """CjC (F) = mean over 0.5-5 GHz of -0.5 * Im(Y21 + Y12) / (2*pi*f)."""
    freq = np.asarray(freq, dtype=float)
    w = 2.0 * np.pi * freq
    cjc_f = -0.5 * np.imag(y[:, 1, 0] + y[:, 0, 1]) / w
    mask = _band_mask(freq, *_CJC_BAND)
    return float(np.mean(cjc_f[mask]))


def extract_ft(freq: np.ndarray, y: np.ndarray) -> float:
    """fT (Hz) = mean over ~30 GHz band of |H21| * f, with H21 = Y21 / Y11."""
    freq = np.asarray(freq, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        h21 = y[:, 1, 0] / y[:, 0, 0]
    ft_f = np.abs(h21) * freq
    mask = _band_mask(freq, *_FT_BAND) & np.isfinite(ft_f)
    if not mask.any():
        return float("nan")
    return float(np.mean(ft_f[mask]))


_EXTRACTORS = {
    "cje": extract_cje,
    "cjc": extract_cjc,
    "ft": extract_ft,
}


def extract_metric(name: str, freq: np.ndarray, y: np.ndarray) -> float:
    """Dispatch to the extractor for `name` ("cje" / "cjc" / "ft")."""
    key = name.strip().lower()
    fn = _EXTRACTORS.get(key)
    if fn is None:
        raise ValueError(f"Unknown S-param metric '{name}'. Known: {sorted(_EXTRACTORS)}")
    return fn(freq, y)


def extract_from_s(name: str, freq: np.ndarray, s: np.ndarray, z0: float = 50.0) -> float:
    """Convenience: convert S->Y then extract `name` (used on the measured side)."""
    return extract_metric(name, freq, s_to_y(freq, s, z0=z0))
