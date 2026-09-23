#!/bin/bash
# ==============================================================
# Run LVS for SP6TCClockGenerator
# ==============================================================
# This script runs the LVS check with specified layout, netlist,
# and implicit nets.
# ==============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 "${SCRIPT_DIR}/../../../../run_lvs.py" \
  --layout="${SCRIPT_DIR}/SP6TCClockGenerator.gds" \
  --netlist="${SCRIPT_DIR}/SP6TCClockGenerator.cdl" \
  --implicit_nets=vdd \
  --ignore_top_ports_mismatch
