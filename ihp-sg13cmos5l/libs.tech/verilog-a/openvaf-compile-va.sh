#!/bin/bash

# Copyright 2023-2026 The ngspice team
# Authors: Holger Vogt, Dietmar Warning, Harald Pretl
# License: New BSD

# Compile the ihp-sg13cmos5l Verilog-A compact models to OSDI for ngspice.
# NOTE: cmos5l ships the cap_cmomi and cap_cmomf Verilog-A sources here; the
# other OSDI objects in ../ngspice/osdi (psp103, psp103_nqs, r3_cmc, mosvar) are
# supplied pre-built (their Verilog-A sources live in the sibling ihp-sg13g2).
# Run this from libs.tech/verilog-a/ .

# Parse command line arguments
TARGET_CPU_FLAG=""
for arg in "$@"; do
  case $arg in
    --compile-model-generic)
      TARGET_CPU_FLAG="--target_cpu generic"
      shift
      ;;
  esac
done

DIRECTORY="../ngspice/osdi"

if [ ! -d "$DIRECTORY" ]; then
  # Directory does not exist, so create it
  mkdir -p "$DIRECTORY"
fi

# Find and set VerilogA compiler
if command -v openvaf-r &> /dev/null; then
  # Use OpenVAF-Reloaded
  COMPILER="openvaf-r"
elif command -v openvaf &> /dev/null; then
  # Use OpenVAF
  COMPILER="openvaf"
else
  echo "VerilogA compiler not found - install 'openvaf-r' or 'openvaf' to compile models"
  exit 1
fi

echo "======================================================================"
echo "             Compiling VerilogA models using: '$COMPILER'             "
echo "======================================================================"

$COMPILER -D__NGSPICE__ $TARGET_CPU_FLAG -o $DIRECTORY/cap_cmomi.osdi cap_cmomi/cap_cmomi.va
$COMPILER -D__NGSPICE__ $TARGET_CPU_FLAG -o $DIRECTORY/cap_cmomf.osdi cap_cmomf/cap_cmomf.va

echo done
