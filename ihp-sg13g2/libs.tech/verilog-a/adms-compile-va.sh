#!/bin/bash

# Copyright 2023 The ngspice team
# Authors: Holger Vogt, Dietmar Warning
# License: New BSD


DIRECTORY="../xyce/plugins"

if [ ! -d "$DIRECTORY" ]; then
  # Directory does not exist, so create it
  mkdir -p "$DIRECTORY"
fi

cd ./psp103/
buildxyceplugin psp103.va ../../xyce/plugins
rm *.la *.log
rm -rfd .libs/
cd ..

cd ./r3_cmc/
buildxyceplugin r3_cmc.va ../../xyce/plugins
rm *.la *.log
rm -rfd .libs/
cd ..

echo Compilation finished! \
Plugins can be found in $PDK_ROOT/$PDK/libs.tech/xyce/plugins

