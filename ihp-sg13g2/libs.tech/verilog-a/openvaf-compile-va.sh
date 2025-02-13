#!/bin/bash

# Copyright 2023 The ngspice team
# Authors: Holger Vogt, Dietmar Warning
# License: New BSD

DIRECTORY="../ngspice/osdi"

if [ ! -d "$DIRECTORY" ]; then
  # Directory does not exist, so create it
  mkdir -p "$DIRECTORY"
fi

openvaf -D__NGSPICE__ -o $DIRECTORY/psp103.osdi psp103/psp103.va
openvaf -D__NGSPICE__ -o $DIRECTORY/psp103_nqs.osdi psp103/psp103_nqs.va
openvaf -D__NGSPICE__ -o $DIRECTORY/r3_cmc.osdi r3_cmc/r3_cmc.va

echo done

