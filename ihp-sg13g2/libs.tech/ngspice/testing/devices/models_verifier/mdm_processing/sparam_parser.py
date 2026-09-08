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
Milestone M4 -- frequency-domain S-parameter MDM parser (HBT device caps + fT).

The DC pipeline (`mdm_processing/parser.py` / `aggregator.py`) intentionally SKIPS
`spar_*` files (see `MdmDirectoryAggregator.find_mdm_files`). This module is a SEPARATE
ingestion path that reads the S-parameter `.mdm` files directly, so the DC path is left
byte-for-byte unchanged.

S-param MDM layout (IC-CAP), e.g. `libs.doc/meas/HBT/npn13g2_T03/spar_vb.mdm`::

    BEGIN_HEADER
     ICCAP_INPUTS
      vbe        V  B GROUND SMU_B ...      <- the 3rd token (B/C/E/S) is the NODE
      vc         V  C GROUND SMU_C ...
      ve         V  E GROUND SMU_E ...
      vs         V  S GROUND SMU_S ...
      freq       F  LIST  1 74 100000000 ... 65000000000
     ICCAP_OUTPUTS
      S          S  B C GROUND NWA M        <- raw measured 2-port
      ib         I  B GROUND SMU_B M
      S_deemb    S B C GROUND n/a B         <- already open/short deembedded 2-port
     ICCAP_VALUES
      TEMP "27"  DEV_GEOM_L "0.9"  DEV_GEOM_W "0.07"  NUM_OF_TRANS_RF "1"
      REMARKS "Nx=8; ..."
    END_HEADER
    BEGIN_DB
     ICCAP_VAR vbe 0.6
     ICCAP_VAR vc  0
     ICCAP_VAR ve  0
     ICCAP_VAR vs  0
     #freq R:S(1,1) I:S(1,1) ... ib R:S_deemb(1,1) I:S_deemb(1,1) ... I:S_deemb(2,2)
      <one row per frequency>
    END_DB
    ... (one BEGIN_DB per bias point)

CRITICAL: the ICCAP_VAR *names* are misleading -- e.g. in `spar_vc.mdm` the swept var is
called ``vce`` but its ICCAP_INPUTS declaration puts it on node **C** (collector). We map
every input variable to its physical node letter (B/C/E/S) from ICCAP_INPUTS and record
the true node voltages V(B), V(C), V(E), V(S) per bias point, so downstream code derives
VBE = V(B)-V(E), VCB = V(C)-V(B), VCE = V(C)-V(E) consistently across all spar files.

Port convention (from ICCAP_OUTPUTS ``S ... B C ...``): port 1 = base, port 2 = collector,
common emitter. The parsed ``s_deemb`` array is ordered (S11, S12, S21, S22) with
S(i,j) -> ``s_deemb[:, i-1, j-1]``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from models_verifier.mdm_processing.utils import (
    extract_section,
    parse_design_parameters,
)

logger = logging.getLogger(__name__)

# Physical node letters used by the HBT S-param setups.
_NODES = ("B", "C", "E", "S")

# Which 2-port S set to consume. Primary path uses the already open/short deembedded
# columns; fall back to the raw measured S if deembedded columns are absent (documented).
_PREFERRED_S = "S_deemb"
_FALLBACK_S = "S"


class SparamParseError(Exception):
    """Raised when parsing an S-parameter MDM file fails."""


@dataclass
class BiasPoint:
    """One BEGIN_DB block: a fixed bias with an S-parameter sweep over frequency."""

    node_voltages: Dict[str, float]          # {"B": .., "C": .., "E": .., "S": ..}
    freq: np.ndarray                         # (nf,) Hz
    s: np.ndarray                            # (nf, 2, 2) complex 2-port S
    s_source: str = _PREFERRED_S             # which column set was consumed
    raw_vars: Dict[str, float] = field(default_factory=dict)  # ICCAP_VAR name->value

    @property
    def vb(self) -> float:
        return self.node_voltages.get("B", 0.0)

    @property
    def vc(self) -> float:
        return self.node_voltages.get("C", 0.0)

    @property
    def ve(self) -> float:
        return self.node_voltages.get("E", 0.0)

    @property
    def vs(self) -> float:
        return self.node_voltages.get("S", 0.0)

    @property
    def vbe(self) -> float:
        return self.vb - self.ve

    @property
    def vcb(self) -> float:
        return self.vc - self.vb

    @property
    def vce(self) -> float:
        return self.vc - self.ve


@dataclass
class SparamData:
    """Parsed contents of one S-parameter MDM file."""

    filepath: Path
    node_map: Dict[str, str]                 # input var name -> node letter (B/C/E/S)
    design_params: Dict[str, object]         # W, L, M, Nx, TEMP, ...
    bias_points: List[BiasPoint]

    @property
    def temp(self) -> float:
        try:
            return float(self.design_params.get("TEMP", 27.0))
        except (TypeError, ValueError):
            return 27.0


class SparamMdmParser:
    """Parser for a single frequency-domain S-parameter `.mdm` file."""

    def __init__(self, filepath: Path):
        self.filepath = Path(filepath)
        if not self.filepath.is_file():
            raise FileNotFoundError(f"S-param MDM not found: {self.filepath}")

    # ---------------------------------------------------------------------
    # Header
    # ---------------------------------------------------------------------
    @staticmethod
    def _parse_input_node_map(header_lines: List[str]) -> Dict[str, str]:
        """
        Map each ICCAP_INPUTS variable name to its physical node letter (B/C/E/S).

        Format: ``<name>  <UNIT> <NODE> <ref> ...`` where UNIT is ``V`` for a voltage
        input and NODE is one of B/C/E/S. Non-voltage inputs (e.g. ``freq F LIST ...``)
        are ignored.
        """
        input_lines, _ = extract_section(header_lines, "ICCAP_INPUTS", "ICCAP_OUTPUTS")
        node_map: Dict[str, str] = {}
        for line in input_lines:
            s = line.strip()
            if not s or s.startswith("!"):
                continue
            toks = s.split()
            if len(toks) >= 3 and toks[1].upper() == "V" and toks[2].upper() in _NODES:
                node_map[toks[0]] = toks[2].upper()
        return node_map

    # ---------------------------------------------------------------------
    # Blocks
    # ---------------------------------------------------------------------
    @staticmethod
    def _s_column_indices(columns: List[str], prefix: str) -> Optional[Dict[tuple, tuple]]:
        """
        Locate the R:/I: column indices for the 2x2 S set named `prefix`
        (e.g. "S_deemb" or "S"). Returns {(i,j): (r_idx, i_idx)} for i,j in 1..2, or
        None if the full set is not present.
        """
        idx: Dict[tuple, tuple] = {}
        for i in (1, 2):
            for j in (1, 2):
                r_name = f"R:{prefix}({i},{j})"
                i_name = f"I:{prefix}({i},{j})"
                if r_name not in columns or i_name not in columns:
                    return None
                idx[(i, j)] = (columns.index(r_name), columns.index(i_name))
        return idx

    def _parse_block(self, block_lines: List[str], node_map: Dict[str, str]) -> Optional[BiasPoint]:
        raw_vars: Dict[str, float] = {}
        columns: Optional[List[str]] = None
        rows: List[List[float]] = []

        for line in block_lines:
            s = line.strip()
            if not s:
                continue
            if s.startswith("ICCAP_VAR"):
                parts = s.split(None, 2)
                if len(parts) == 3:
                    try:
                        raw_vars[parts[1]] = float(parts[2])
                    except ValueError:
                        pass
                continue
            if s.startswith("#"):
                columns = s.lstrip("#").split()
                continue
            if columns is not None:
                parts = s.split()
                if len(parts) == len(columns):
                    try:
                        rows.append([float(x) for x in parts])
                    except ValueError:
                        continue

        if not columns or not rows:
            return None

        arr = np.asarray(rows, dtype=float)
        if "freq" not in columns:
            return None
        freq = arr[:, columns.index("freq")]

        # Prefer the deembedded S set; fall back to raw S if not present.
        s_source = _PREFERRED_S
        s_idx = self._s_column_indices(columns, _PREFERRED_S)
        if s_idx is None:
            s_idx = self._s_column_indices(columns, _FALLBACK_S)
            s_source = _FALLBACK_S
        if s_idx is None:
            return None

        nf = arr.shape[0]
        s = np.zeros((nf, 2, 2), dtype=complex)
        for (i, j), (r_i, im_i) in s_idx.items():
            s[:, i - 1, j - 1] = arr[:, r_i] + 1j * arr[:, im_i]

        node_voltages = {n: 0.0 for n in _NODES}
        for name, val in raw_vars.items():
            node = node_map.get(name)
            if node in node_voltages:
                node_voltages[node] = val

        return BiasPoint(
            node_voltages=node_voltages,
            freq=freq,
            s=s,
            s_source=s_source,
            raw_vars=raw_vars,
        )

    # ---------------------------------------------------------------------
    # Public
    # ---------------------------------------------------------------------
    def parse(self) -> SparamData:
        content = self.filepath.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()

        header_lines, header_end = extract_section(lines, "BEGIN_HEADER", "END_HEADER")
        if not header_lines or header_end == -1:
            raise SparamParseError(f"Header missing in {self.filepath}")

        node_map = self._parse_input_node_map(header_lines)
        if not node_map:
            raise SparamParseError(f"No voltage node map parsed from {self.filepath}")
        design_params = parse_design_parameters(header_lines, "hbt")

        body = lines[header_end:]
        bias_points: List[BiasPoint] = []
        current: Optional[List[str]] = None
        for line in body:
            stripped = line.strip()
            if stripped == "BEGIN_DB":
                current = []
            elif stripped == "END_DB" and current is not None:
                bp = self._parse_block(current, node_map)
                if bp is not None:
                    bias_points.append(bp)
                current = None
            elif current is not None:
                current.append(line)

        if not bias_points:
            raise SparamParseError(f"No bias blocks parsed from {self.filepath}")

        sources = {bp.s_source for bp in bias_points}
        if _FALLBACK_S in sources and _PREFERRED_S not in sources:
            logger.warning(
                "%s: consumed RAW '%s' columns (no '%s' present) -- results are NOT "
                "deembedded.", self.filepath.name, _FALLBACK_S, _PREFERRED_S,
            )

        return SparamData(
            filepath=self.filepath,
            node_map=node_map,
            design_params=design_params,
            bias_points=bias_points,
        )


def parse_sparam_mdm(filepath: Path) -> SparamData:
    """Convenience wrapper: parse one S-parameter MDM file."""
    return SparamMdmParser(filepath).parse()
