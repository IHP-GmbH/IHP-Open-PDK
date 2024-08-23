#!/bin/bash

# Copyright 2023 The ngspice team
# Authors: Holger Vogt, Dietmar Warning
# License: New BSD


cd ./adms/psp103/
buildxyceplugin psp103_nqs.va ../../plugins
rm *.la *.log
rm -rfd .libs/
cd ..

echo Compilation finished! \
Plugins can be found in $PDK_ROOT/$PDK/libs.tech/xyce/plugins

