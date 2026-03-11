#!/bin/bash

# Copyright 2023-2026 The ngspice team
# Authors: Holger Vogt, Dietmar Warning, Harald Pretl
# License: New BSD

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

$COMPILER -D__NGSPICE__ $TARGET_CPU_FLAG -o $DIRECTORY/psp103.osdi psp103/psp103.va
$COMPILER -D__NGSPICE__ $TARGET_CPU_FLAG -o $DIRECTORY/psp103_nqs.osdi psp103/psp103_nqs.va
$COMPILER -D__NGSPICE__ $TARGET_CPU_FLAG -o $DIRECTORY/r3_cmc.osdi r3_cmc/r3_cmc.va
$COMPILER -D__NGSPICE__ $TARGET_CPU_FLAG -o $DIRECTORY/mosvar.osdi mosvar/mosvar.va

echo done
