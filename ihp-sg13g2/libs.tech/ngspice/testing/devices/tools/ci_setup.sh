#!/usr/bin/env bash
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
# System packages of the CI jobs (Ubuntu GitHub-hosted runners); called by the workflow only.
#   tools/ci_setup.sh ngspice   build and run ngspice (compiler, X11/readline/FFTW headers and libraries)
#   tools/ci_setup.sh llvm      LLVM 21 from apt.llvm.org (build and run OpenVAF-Reloaded, see toolchain.lock)
set -euo pipefail
case "${1:-}" in
  ngspice)
    sudo apt-get update
    sudo apt-get install -y build-essential bison flex libtool automake autoconf pkg-config \
      libx11-dev libxaw7-dev libxmu-dev libxpm-dev libxext-dev libreadline-dev libfftw3-dev libgomp1
    ;;
  llvm)
    wget -qO /tmp/llvm.sh https://apt.llvm.org/llvm.sh
    sudo bash /tmp/llvm.sh 21
    sudo apt-get install -y llvm-21-dev libclang-21-dev libpolly-21-dev zlib1g-dev libzstd-dev
    ;;
  *)
    echo "usage: $0 ngspice | llvm" >&2
    exit 2
    ;;
esac
