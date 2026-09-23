#!/bin/bash
# ==============================================================
# Run LVS for esd_ptap
# ==============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 "${SCRIPT_DIR}/../../../../run_lvs.py" \
  --layout="${SCRIPT_DIR}/esd_ptap.gds" \
  --netlist="${SCRIPT_DIR}/esd_ptap.cdl" \
  --ignore_top_ports_mismatch
