#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2020 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# SPDX-License-Identifier: Apache-2.0

#
# check_density.py ---
#
#    Run density checks on a design (from GDS, after running fill generation).
#

import sys
import os
import re
import select
import subprocess

def usage():
    print("Usage:")
    print("check_density.py [<gds_file_name>] [-keep]")
    print("")
    print("where:")
    print("   <gds_file_name> is the path to the .gds file to be checked.")
    print("")
    print("  If '-keep' is specified, then keep the check script.")
    return 0


if __name__ == '__main__':

    optionlist = []
    arguments = []

    debugmode = False
    keepmode = False

    for option in sys.argv[1:]:
        if option.find('-', 0) == 0:
            optionlist.append(option)
        else:
            arguments.append(option)

    if len(arguments) != 1:
        print("Wrong number of arguments given to check_density.py.")
        usage()
        sys.exit(0)
        
    relative_path=arguments[0]

    gdspath = os.getcwd()+'/'+os.path.split(relative_path)[0]+'/'
    if gdspath == '':
        gdspath = os.getcwd()

    gds_filepath = os.path.split(relative_path)[1]
    
    if os.path.splitext(gds_filepath)[1] != '.gds':
        if os.path.splitext(gds_filepath)[1] == '':
            gds_filepath += '.gds'
        else:
            print('Error:  Project is not a GDS file!')
            sys.exit(1)
    
    gdsname = os.path.split(gds_filepath)[1]
    gdsroot = os.path.splitext(gdsname)[0]

    # Check for valid path to the GDS file

    if not os.path.isdir(gdspath):
        print('Error:  Project path "' + gds_filepath + '" does not exist or is not readable.')
        sys.exit(1)
        
    if not os.path.isfile(gdspath+gds_filepath):
        print('Error:  Project "' + gdspath+gds_filepath + '" does not exist or is not readable.')
        sys.exit(1)

    if '-debug' in optionlist:
        debugmode = True
    if '-keep' in optionlist:
        keepmode = True

    # NOTE:  There should be some attempt to find the installed PDK magicrc file
    # if there is no mag/ directory.
    
    # Searching for rcfile
    
    rcfile_paths=[gdspath+'/.magicrc','/$PDK_PATH/libs.tech/magic/TECHNAME.magicrc','/usr/share/pdk/TECHNAME/libs.tech/magic/TECHNAME.magicrc']
    
    rcfile=''
    
    for rc_path in rcfile_paths:
        if os.path.isfile(rc_path):
            rcfile=rc_path
            break
    
    if rcfile=='':
        print('Error: .magicrc file not found.')
        sys.exit(1)

    
    with open(gdspath + '/check_density.tcl', 'w') as ofile:
        print('#!/bin/env wish', file=ofile)
        print('crashbackups stop', file=ofile)
        print('drc off', file=ofile)
        print('snap internal', file=ofile)

        print('set starttime [orig_clock format [orig_clock seconds] -format "%D %T"]', file=ofile)
        print('puts stdout "Started reading GDS: $starttime"', file=ofile)
        print('', file=ofile)
        print('flush stdout', file=ofile)
        print('update idletasks', file=ofile)

        # Read GDS file
        print('gds readonly true', file=ofile)
        print('gds rescale false', file=ofile)
        print('gds read ' + gds_filepath, file=ofile)
        print('', file=ofile)

        # NOTE:  This assumes that the name of the GDS file is the name of the
        # topmost cell (which should be passed as an option)
        print('load ' + gdsroot, file=ofile)
        print('', file=ofile)

        print('set midtime [orig_clock format [orig_clock seconds] -format "%D %T"]', file=ofile)
        print('puts stdout "Starting density checks: $midtime"', file=ofile)
        print('', file=ofile)
        print('flush stdout', file=ofile)
        print('update idletasks', file=ofile)

        # Get step box dimensions (800um for size and 400um for step)
        print('box values 0 0 0 0', file=ofile)
        # print('box size 800um 800um', file=ofile)
        # print('set stepbox [box values]', file=ofile)
        # print('set stepwidth [lindex $stepbox 2]', file=ofile)
        # print('set stepheight [lindex $stepbox 3]', file=ofile)

        print('box size 400um 400um', file=ofile)
        print('set stepbox [box values]', file=ofile)
        print('set stepsizex [lindex $stepbox 2]', file=ofile)
        print('set stepsizey [lindex $stepbox 3]', file=ofile)

        print('select top cell', file=ofile)
        print('expand', file=ofile)
        print('set fullbox [box values]', file=ofile)
        print('set xmax [lindex $fullbox 2]', file=ofile)
        print('set xmin [lindex $fullbox 0]', file=ofile)
        print('set fullwidth [expr {$xmax - $xmin}]', file=ofile)
        print('set xtiles [expr {int(ceil(($fullwidth + 0.0) / $stepsizex))}]', file=ofile)
        print('set ymax [lindex $fullbox 3]', file=ofile)
        print('set ymin [lindex $fullbox 1]', file=ofile)
        print('set fullheight [expr {$ymax - $ymin}]', file=ofile)
        print('set ytiles [expr {int(ceil(($fullheight + 0.0) / $stepsizey))}]', file=ofile)
        print('box size $stepsizex $stepsizey', file=ofile)
        print('set xbase [lindex $fullbox 0]', file=ofile)
        print('set ybase [lindex $fullbox 1]', file=ofile)
        print('', file=ofile)

        print('puts stdout "XTILES: $xtiles"', file=ofile)
        print('puts stdout "YTILES: $ytiles"', file=ofile)
        print('', file=ofile)

        # Need to know what fraction of a full tile is the last row and column
        print('set xfrac [expr {($xtiles * $stepsizex - $fullwidth + 0.0) / $stepsizex}]', file=ofile)
        print('set yfrac [expr {($ytiles * $stepsizey - $fullheight + 0.0) / $stepsizey}]', file=ofile)

        # If the last row/column fraction is zero, then set to 1
        print('if {$xfrac == 0.0} {set xfrac 1.0}', file=ofile)
        print('if {$yfrac == 0.0} {set yfrac 1.0}', file=ofile)

        print('puts stdout "XFRAC: $xfrac"', file=ofile)
        print('puts stdout "YFRAC: $yfrac"', file=ofile)

        print('cif ostyle density', file=ofile)

        # Process density at steps.  For efficiency, this is done in 400x400 um
        # areas, dumped to a file, and then aggregated into the 800x800 areas.

        print('for {set y 0} {$y < $ytiles} {incr y} {', file=ofile)
        print('    for {set x 0} {$x < $xtiles} {incr x} {', file=ofile)
        print('        set xlo [expr $xbase + $x * $stepsizex]', file=ofile)
        print('        set ylo [expr $ybase + $y * $stepsizey]', file=ofile)
        print('        set xhi [expr $xlo + $stepsizex]', file=ofile)
        print('        set yhi [expr $ylo + $stepsizey]', file=ofile)
        print('        box values $xlo $ylo $xhi $yhi', file=ofile)

        # Flatten this area
        print('        flatten -dobbox -nolabels tile', file=ofile)
        print('        load tile', file=ofile)
        print('        select top cell', file=ofile)

        # Run density check for each layer.  Note that only active (diffusion)
        # and metal layers 1 to 5 are checked over tiles.  Poly and top metals
        # are also checked in tiles, but only the aggregated results are used.
        print('        puts stdout "Density results for tile x=$x y=$y"', file=ofile)

        print('        set fdens  [cif list cover diff_all]', file=ofile)
        print('        set pdens  [cif list cover poly_all]', file=ofile)
        print('        set m1dens [cif list cover m1_all]', file=ofile)
        print('        set m2dens [cif list cover m2_all]', file=ofile)
        print('        set m3dens [cif list cover m3_all]', file=ofile)
        print('        set m4dens [cif list cover m4_all]', file=ofile)
        print('        set m5dens [cif list cover m5_all]', file=ofile)
        print('        set m6dens [cif list cover m6_all]', file=ofile)
        print('        set m7dens [cif list cover m7_all]', file=ofile)
        print('        puts stdout "ACTIVE: $fdens"', file=ofile)
        print('        puts stdout "POLY: $pdens"', file=ofile)
        print('        puts stdout "MET1: $m1dens"', file=ofile)
        print('        puts stdout "MET2: $m2dens"', file=ofile)
        print('        puts stdout "MET3: $m3dens"', file=ofile)
        print('        puts stdout "MET4: $m4dens"', file=ofile)
        print('        puts stdout "MET5: $m5dens"', file=ofile)
        print('        puts stdout "TOP1: $m6dens"', file=ofile)
        print('        puts stdout "TOP2: $m7dens"', file=ofile)
        print('        flush stdout', file=ofile)
        print('        update idletasks', file=ofile)

        print('        load ' + gdsroot, file=ofile)
        print('        cellname delete tile', file=ofile)

        print('    }', file=ofile)
        print('}', file=ofile)

        print('set endtime [orig_clock format [orig_clock seconds] -format "%D %T"]', file=ofile)
        print('puts stdout "Ended: $endtime"', file=ofile)
        print('quit -noprompt', file=ofile)
        print('', file=ofile)


    myenv = os.environ.copy()
    myenv['MAGTYPE'] = 'mag'

    print('Running density checks on file ' + gds_filepath, flush=True)
    
    mproc = subprocess.Popen(['magic', '-dnull', '-noconsole',
		'-rcfile', rcfile, gdspath + '/check_density.tcl'],
		stdin = subprocess.DEVNULL,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		cwd = gdspath,
		env = myenv,
		universal_newlines = True)

    # Use signal to poll the process and generate any output as it arrives

    dlines = []

    while mproc:
        status = mproc.poll()
        if status != None:
            try:
                output = mproc.communicate(timeout=1)
            except ValueError:
                print('Magic forced stop, status ' + str(status))
                sys.exit(1)
            else:
                outlines = output[0]
                errlines = output[1]
                for line in outlines.splitlines():
                    dlines.append(line)
                    print(line)
                for line in errlines.splitlines():
                    print(line)
                print('Magic exited with status ' + str(status))
                if int(status) != 0:
                    sys.exit(int(status))
                else:
                    break
        else:
            n = 0
            while True:
                n += 1
                if n > 100:
                    n = 0
                    status = mproc.poll()
                    if status != None:
                        break
                sresult = select.select([mproc.stdout, mproc.stderr], [], [], 0)[0]
                if mproc.stdout in sresult:
                    outstring = mproc.stdout.readline().strip()
                    dlines.append(outstring)
                    print(outstring)
                elif mproc.stderr in sresult:
                    outstring = mproc.stderr.readline().strip()
                    print(outstring)
                else:
                    break

    difffill  = []
    polyfill = []
    met1fill = []
    met2fill = []
    met3fill = []
    met4fill = []
    met5fill = []
    met6fill = []
    met7fill = []
    xtiles = 0
    ytiles = 0
    xfrac = 0.0
    yfrac = 0.0

    for line in dlines:
        dpair = line.split(':')
        if len(dpair) == 2:
            layer = dpair[0]
            try:
                density = float(dpair[1].strip())
            except:
                continue
            if layer == 'DIFF':
                difffill.append(density)
            elif layer == 'POLY':
                polyfill.append(density)
            elif layer == 'MET1':
                met1fill.append(density)
            elif layer == 'MET2':
                met2fill.append(density)
            elif layer == 'MET3':
                met3fill.append(density)
            elif layer == 'MET4':
                met4fill.append(density)
            elif layer == 'MET5':
                met5fill.append(density)
            elif layer == 'TOP1':
                met6fill.append(density)
            elif layer == 'TOP2':
                met7fill.append(density)
            elif layer == 'XTILES':
                xtiles = int(dpair[1].strip())
            elif layer == 'YTILES':
                ytiles = int(dpair[1].strip())
            elif layer == 'XFRAC':
                xfrac = float(dpair[1].strip())
            elif layer == 'YFRAC':
                yfrac = float(dpair[1].strip())

    if ytiles == 0 or xtiles == 0:
        print('Failed to read XTILES or YTILES from output.')
        sys.exit(1)

    if xtiles < 2 or ytiles < 2:
        print('Layout is < 800um x 800um;  cannot run density checks.')
        sys.exit(1)

    total_tiles = (ytiles - 1) * (xtiles - 1)

    print('')
    print('Density results (total tiles = ' + str(total_tiles) + '):')

    # Full areas are 2 x 2 tiles = 4.  But the right and top sides are
    # not full tiles, so the full area must be prorated.

    sideadjust = 50.0 + (50.0 * xfrac)
    topadjust = 50.0 + (50.0 * yfrac)

    corneradjust = 50.0 + (50.0 * xfrac) + (50.0 * yfrac) + (xfrac * yfrac)

    print('Side adjustment = ' + str(sideadjust))
    print('Top adjustment = ' + str(topadjust))
    print('Corner adjustment = ' + str(corneradjust))

    print('')
    print('Active (Diffusion) Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            diffaccum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                diffaccum += sum(difffill[base : base + 2])
                    
            diffaccum /= atotal
            print('Tile (' + str(x) + ', ' + str(y) + '):   ' + str(diffaccum))
            if diffaccum < 0.33:
                print('***Error:  Active Density < 25% (AFil.g2)')
            elif diffaccum > 0.65:
                print('***Error:  Active Density > 65% (AFil.g3)')

    print('')
    # print('POLY Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            polyaccum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                polyaccum += sum(polyfill[base : base + 2])
                    
            polyaccum /= atotal

    print('')
    print('MET1 Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            met1accum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                met1accum += sum(met1fill[base : base + 2])
                    
            met1accum /= atotal
            print('Tile (' + str(x) + ', ' + str(y) + '):   ' + str(met1accum))
            if met1accum < 0.25:
                print('***Error:  MET1 Density < 25% (MFil.h)')
            elif met1accum > 0.75:
                print('***Error:  MET1 Density > 75% (MFil.k)')

    print('')
    print('MET2 Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            met2accum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                met2accum += sum(met2fill[base : base + 2])
                    
            met2accum /= atotal
            print('Tile (' + str(x) + ', ' + str(y) + '):   ' + str(met2accum))
            if met2accum < 0.25:
                print('***Error:  MET2 Density < 25% (Mil.h)')
            elif met2accum > 0.75:
                print('***Error:  MET2 Density > 75% (MFil.k)')

    print('')
    print('MET3 Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            met3accum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                met3accum += sum(met3fill[base : base + 2])
                    
            met3accum /= atotal
            print('Tile (' + str(x) + ', ' + str(y) + '):   ' + str(met3accum))
            if met3accum < 0.25:
                print('***Error:  MET3 Density < 25% (MFil.h)')
            elif met3accum > 0.75:
                print('***Error:  MET3 Density > 75% (MFil.k)')

    print('')
    print('MET4 Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            met4accum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                met4accum += sum(met4fill[base : base + 2])
                    
            met4accum /= atotal
            print('Tile (' + str(x) + ', ' + str(y) + '):   ' + str(met4accum))
            if met4accum < 0.25:
                print('***Error:  MET4 Density < 25% (MFil.h)')
            elif met4accum > 0.75:
                print('***Error:  MET4 Density > 75% (MFil.k)')

    print('')
    print('MET5 Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            met5accum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                met5accum += sum(met5fill[base : base + 2])
                    
            met5accum /= atotal
            print('Tile (' + str(x) + ', ' + str(y) + '):   ' + str(met5accum))
            if met5accum < 0.25:
                print('***Error:  MET5 Density < 25% (MFil.h)')
            elif met5accum > 0.75:
                print('***Error:  MET5 Density > 75% (MFil.k)')

    print('')
    # print('TOP1 Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            met6accum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                met6accum += sum(met6fill[base : base + 2])
            met6accum /= atotal

    print('')
    # print('TOP2 Density:')
    for y in range(0, ytiles - 1):
        if y == ytiles - 2:
            atotal = topadjust
        else:
            atotal = 100.0
        for x in range(0, xtiles - 1):
            if x == xtiles - 2:
                if y == ytiles - 2:
                    atotal = corneradjust
                else:
                    atotal = sideadjust
            met7accum = 0
            for w in range(y, y + 2):
                base = xtiles * w + x
                met7accum += sum(met7fill[base : base + 2])
            met7accum /= atotal

    print('')
    print('Whole-chip density results:')

    atotal = ((xtiles - 1.0) * (ytiles - 1.0)) + ((ytiles - 1.0) * xfrac) + ((xtiles - 1.0) * yfrac) + (xfrac * yfrac)

    diffaccum = sum(difffill) / atotal
    print('')
    print('Active (Diffusion) Density: ' + str(diffaccum))
    if diffaccum < 0.35:
        print('***Error:  Active Density < 35% (aFil.g)')
    elif diffaccum > 0.55:
        print('***Error:  Active Density > 55% (AFil.g1)')

    polyaccum = sum(polyfill) / atotal
    print('')
    print('POLY Density: ' + str(polyaccum))
    if polyaccum < 0.15:
        print('***Error:  Poly Density < 15% (GFil.g)')

    met1accum = sum(met1fill) / atotal
    print('')
    print('MET1 Density: ' + str(met1accum))
    if met1accum < 0.35:
        print('***Error:  MET1 Density < 35% (M1.j)')
    elif met1accum > 0.60:
        print('***Error:  MET1 Density > 60% (M1.k)')

    met2accum = sum(met2fill) / atotal
    print('')
    print('MET2 Density: ' + str(met2accum))
    if met2accum < 0.35:
        print('***Error:  MET2 Density < 35% (M2.j)')
    elif met2accum > 0.60:
        print('***Error:  MET2 Density > 60% (M2.k)')

    met3accum = sum(met3fill) / atotal
    print('')
    print('MET3 Density: ' + str(met3accum))
    if met3accum < 0.35:
        print('***Error:  MET3 Density < 35% (M3.j)')
    elif met3accum > 0.60:
        print('***Error:  MET3 Density > 60% (M3.k)')

    met4accum = sum(met4fill) / atotal
    print('')
    print('MET4 Density: ' + str(met4accum))
    if met4accum < 0.35:
        print('***Error:  MET4 Density < 35% (M4.j)')
    elif met4accum > 0.60:
        print('***Error:  MET4 Density > 60% (M4.k)')

    met5accum = sum(met5fill) / atotal
    print('')
    print('MET5 Density: ' + str(met5accum))
    if met5accum < 0.35:
        print('***Error:  MET5 Density < 35% (M5.j)')
    elif met5accum > 0.60:
        print('***Error:  MET5 Density > 60% (M5.k)')

    met6accum = sum(met6fill) / atotal
    print('')
    print('TOP1 Density: ' + str(met6accum))
    if met6accum < 0.25:
        print('***Error:  TOP1 Density < 25% (TM1.c)')
    elif met6accum > 0.70:
        print('***Error:  TOP1 Density > 70% (TM1.d)')

    met7accum = sum(met7fill) / atotal
    print('')
    print('TOP2 Density: ' + str(met7accum))
    if met7accum < 0.25:
        print('***Error:  TOP2 Density < 25% (TM2.c)')
    elif met7accum > 0.70:
        print('***Error:  TOP2 Density > 70% (TM2.d)')

    if not keepmode:
        if os.path.isfile(gdspath + '/check_density.tcl'):
            os.remove(gdspath + '/check_density.tcl')

    print('')
    print('Done!')
    sys.exit(0)

