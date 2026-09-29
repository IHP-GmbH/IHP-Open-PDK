#!/bin/bash
# ==============================================================
# Run LVS for SRAM support testcase
# ==============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_LVS="${SCRIPT_DIR}/../../../../run_lvs.py"
RUN_DIR="${TMPDIR:-/tmp}/sg13cmos5l_sram_support_$(date +%Y_%m_%d_%H_%M_%S)"

python3 "${RUN_LVS}" \
  --layout="${SCRIPT_DIR}/SP01.oas" \
  --netlist="${SCRIPT_DIR}/SP01.spi" \
  --topcell=SP01 \
  --run_mode=deep \
  --run_dir="${RUN_DIR}" \
  --ignore_top_ports_mismatch

echo "LVS logs and reports: ${RUN_DIR}"
