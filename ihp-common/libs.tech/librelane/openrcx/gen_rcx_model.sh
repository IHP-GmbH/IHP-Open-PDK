#!/usr/bin/env bash
#==========================================================================
# Copyright 2026 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# SPDX-License-Identifier: Apache-2.0
#==========================================================================
#
# Generate an OpenRCX model file from a process stack description using
# FasterCap as the reference field solver.
#
# Usage:
#   gen_rcx_model.sh <name>.<CORNER>.process [stage ...]
#   stages: patterns fastercap parse model (default: all)
#
# Each PDK keeps one process file per RC corner (TYP, MIN, MAX) in
# <pdk>/libs.tech/librelane/openrcx/ and symlinks this script next to
# them. The model is written next to the process file as
# <name>.<CORNER>.rcx.model.
#
# Follows OpenROAD's src/rcx/test/rcx_v2/FasterCapModel flow, with our own
# geometry step (see solve_pattern.py for why):
#   1. gen_solver_patterns  (openroad)  -> 3D wire patterns + resistance table
#   2. solve_pattern.py + FasterCap     -> capacitance matrix per pattern
#   3. fasterCapParse.py  (openroad)    -> one table file per pattern set
#   4. init_rcx_model / read_rcx_tables / write_rcx_model (openroad)
#
# Requirements: openroad (OpenRCX v2), FasterCap, python3 with xlsxwriter,
# pandas, matplotlib and numpy (imported by the OpenROAD parser), curl
# (unless OPENROAD_SRC points to an OpenROAD checkout with the parser).
#
# Environment:
#   OPENROAD, FASTERCAP   executables (default: from PATH)
#   OPENROAD_SRC          OpenROAD source tree for the helper scripts;
#                         without it they are fetched from GitHub
#   CORNER                corner name written into the model (default: the
#                         suffix of the process file name, else TYP)
#   WORK                  scratch directory (default <dir of process>/work)
#   OUT                   model file path
#   EPS                   relative permittivity of the uniform dielectric
#   EXT, ACCURACY, JOBS   FasterCap ground plane extension (um), relative
#                         accuracy, parallel solver jobs
#   TIMEOUT               seconds per FasterCap run; a run that does not
#                         converge in time is killed and its last completed
#                         capacitance matrix is used
#
# Stage 3 is incremental: rerunning skips patterns with a usable wires.log.
set -euo pipefail

PROCESS=${1:?usage: $0 <stack.process> [patterns|fastercap|parse|model ...]}
shift
PROCESS=$(readlink -f "$PROCESS")
pdir=$(dirname "$PROCESS")
pname=$(basename "$PROCESS" .process)
case $pname in
    *.*) CORNER=${CORNER:-${pname##*.}}; pname=${pname%.*} ;;
esac

OPENROAD=${OPENROAD:-openroad}
FASTERCAP=${FASTERCAP:-FasterCap}
CORNER=${CORNER:-TYP}
WORK=${WORK:-$pdir/work}
OUT=${OUT:-$pdir/$pname.$CORNER.rcx.model}
EPS=${EPS:-4.1}
EXT=${EXT:-20}
ACCURACY=${ACCURACY:-0.01}
JOBS=${JOBS:-$(nproc)}
TIMEOUT=${TIMEOUT:-600}
MET_CNT=$(grep -c '^CONDUCTOR' "$PROCESS")

# OpenROAD parser script, pinned to a known commit
or_commit=e304dc6304a5ef637bb69388935af37fdbddb112
or_scripts=src/rcx/test/rcx_v2/FasterCapModel/scripts
if [ -n "${OPENROAD_SRC:-}" ]; then
    scripts=$OPENROAD_SRC/$or_scripts
else
    scripts=$WORK/scripts
    mkdir -p "$scripts"
    f=fasterCapParse.py
    [ -s "$scripts/$f" ] || curl -sfo "$scripts/$f" \
        "https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD/$or_commit/$or_scripts/$f"
fi
fcparse=$scripts/fasterCapParse.py
solve=$(dirname "$(readlink -f "$0")")/solve_pattern.py

# pattern sets: <name>:<wire_cnt>:<version>:<target wire index>
# 1 wire  -> ground cap of open-ended wires (v1: resistance tables)
# 3 wires -> total and coupling caps of the middle wire
sets="1v1:1:1:1 1v2:1:2:1 3v2:3:2:2"

patterns() {
    for s in $sets; do
        IFS=: read -r name cnt ver _ <<<"$s"
        d=$WORK/$name
        rm -rf "$d"; mkdir -p "$d"
        echo "gen_solver_patterns -process_file $PROCESS -process_name $CORNER \
            -wire_cnt $cnt -version $ver" > "$d/gen_patterns.tcl"
        (cd "$d" && $OPENROAD -exit gen_patterns.tcl > OUT)
        find "$d" -name wires | sort > "$d/wires_file_list"
        echo "$name: $(wc -l < "$d/wires_file_list") patterns"
    done
}

# The converter must run from $WORK with a relative pattern path: it writes
# the shared Wires/ and Dielectrics/ panel files into the cwd and references
# them from <pattern>/wires.lst by a fixed ../../../../../../ prefix.
# Conversion is sequential (shared files), the solver runs in parallel.
# solve_pattern.py builds the FasterCap geometry itself (uniform
# dielectric, two wire lengths to cancel end effects) and writes a
# FasterCap-style wires.log for the OpenROAD parser.
solve_one() {
    cd "$WORK"
    python3 "$solve" "$1" --process "$PROCESS" --fastercap "$FASTERCAP" \
        --eps "$EPS" --ext "$EXT" --accuracy "$ACCURACY" --timeout "$TIMEOUT" \
        > "$1/solve.log" 2>&1 ||
        echo "FAILED $1" >> "$1/solve.log"
    echo "$(date +%T) $(tail -1 "$1/solve.log")"
}

fastercap() {
    cd "$WORK"
    export solve PROCESS FASTERCAP EPS EXT ACCURACY TIMEOUT
    export -f solve_one
    todo=$WORK/todo_list
    : > "$todo"
    for s in $sets; do
        IFS=: read -r name cnt ver _ <<<"$s"
        [ "$ver" = 2 ] || continue
        while read -r w; do
            p=${w%/wires}; p=${p#"$WORK"/}
            [ -s "$p/wires.log" ] && grep -q "^Dimension" "$p/wires.log" && continue
            echo "$p" >> "$todo"
        done < "$WORK/$name/wires_file_list"
    done
    echo "$(wc -l < "$todo") patterns to solve"
    xargs -P "$JOBS" -I{} bash -c 'solve_one "$1"' _ {} < "$todo"
}

parse() {
    for s in $sets; do
        IFS=: read -r name cnt ver wire <<<"$s"
        [ "$ver" = 2 ] || continue
        d=$WORK/$name
        (cd "$d" && find "$d" -name wires.log | sort > sorted.input.list &&
            python3 "$fcparse" -in_list_file sorted.input.list -wire "$wire" \
                -out_file "$name.caps" > parse.log)
        echo "$name: $(wc -l < "$d/$name.caps") table lines"
    done
}

model() {
    # read_rcx_tables normalizes by LEN * width with LEN in width multiples
    # (as in the capacitance tables), but gen_solver_patterns writes LEN in
    # um into the resistance table; convert it
    awk '$11 == "LEN" { $12 = sprintf("%d", $12 / $10 + 0.5) } 1' \
        "$WORK/1v1/resistance.$CORNER" > "$WORK/1v1/resistance.$CORNER.widths"
    tcl=$WORK/gen_model.tcl
    {
        echo "init_rcx_model -corner_names \"$CORNER\" -met_cnt $MET_CNT"
        for s in $sets; do
            IFS=: read -r name cnt ver _ <<<"$s"
            [ "$ver" = 2 ] || continue
            echo "read_rcx_tables -corner $CORNER -file $WORK/$name/$name.caps"
        done
        echo "read_rcx_tables -corner $CORNER -file $WORK/1v1/resistance.$CORNER.widths"
        echo "write_rcx_model -file $OUT"
    } > "$tcl"
    $OPENROAD -exit "$tcl" > "$WORK/gen_model.log"
    python3 "$(dirname "$solve")/expand_resover.py" "$OUT"
    echo "wrote $OUT"
}

stages=${*:-patterns fastercap parse model}
for st in $stages; do $st; done
