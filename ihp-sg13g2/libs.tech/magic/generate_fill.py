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
# generate_fill.py ---
#
#    Run the fill generation on a layout top level.
#

import sys
import os
import re
import glob
import functools
import subprocess
import multiprocessing

def usage():
    print("Usage:")
    print("generate_fill.py <layout_name> [-keep] [-test] [-dist]")
    print("")
    print("where:")
    print("    <layout_name> is the path to the .mag or .gds file to be filled.")
    print("")
    print("  If '-keep' is specified, then keep the generation script.")
    print("  If '-test' is specified, then create but do not run the generation script.")
    print("  If '-dist' is specified, then run distributed (multi-processing).")
    return 0

def makegds(file, rcfile):
    # Procedure for multiprocessing only:  Run the distributed processing
    # script to load a .mag file of one flattened square area of the layout,
    # and run the fill generator to produce a .gds file output from it.

    layoutpath = os.path.split(file)[0]
    filename = os.path.split(file)[1]

    myenv = os.environ.copy()
    myenv['MAGTYPE'] = 'mag'

    magic_run_opts = [
		'magic',
		'-dnull',
		'-noconsole',
		'-rcfile', rcfile,
		layoutpath + '/generate_fill_dist.tcl',
		filename]

    mproc = subprocess.run(magic_run_opts,
		stdin = subprocess.DEVNULL,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		cwd = layoutpath,
		env = myenv,
		universal_newlines = True)
    if mproc.stdout:
        for line in mproc.stdout.splitlines():
            print(line)
    if mproc.stderr:
        print('Error message output from magic:')
        for line in mproc.stderr.splitlines():
            print(line)
        if mproc.returncode != 0:
            print('ERROR:  Magic exited with status ' + str(mproc.returncode))


if __name__ == '__main__':

    optionlist = []
    arguments = []

    debugmode = False
    keepmode = False
    testmode = False
    distmode = False

    for option in sys.argv[1:]:
        if option.find('-', 0) == 0:
            optionlist.append(option)
        else:
            arguments.append(option)

    if len(arguments) != 1:
        print("Wrong number of arguments given to generate_fill.py.")
        usage()
        sys.exit(1)

    # Process options

    if '-debug' in optionlist:
        debugmode = True
        print('Running in debug mode.')
    if '-keep' in optionlist:
        keepmode = True
        if debugmode:
            print('Keeping all files after running.')
    elif debugmode:
        print('Files other than final layout will be removed after running.')
    if '-test' in optionlist:
        testmode = True
        if debugmode:
            print('Running in test mode:  No output files will be created.')
    if '-dist' in optionlist:
        distmode = True
        if debugmode:
            print('Running in distributed (multi-processing) mode.')
    elif debugmode:
        print('Running in single-processor mode.')

    # Find layout from command-line argument

    user_project_path = arguments[0]

    if os.path.split(user_project_path)[0] == '':
        layoutpath = os.getcwd()
    else:
        layoutpath = os.getcwd() + '/' + os.path.split(user_project_path)[0]
    
    # Use os.extsep, not os.path.splitext(), because gzipped files have
    # multiple periods (e.g., "layout.gds.gz")

    project = user_project_path.split(os.extsep, 1)

    if len(project) == 1:
        # No file extension given;  figure it out
        layoutfiles = glob.glob(user_project_path + '.*')
        if len(layoutfiles) == 1:
            proj_extension = '.' + layoutfiles[0].split(os.extsep, 1)[1]
            user_project_path = layoutfiles[0]
        elif len(layoutfiles) == 0:
            print('Error:  Project is not a magic database or GDS file!')
            sys.exit(1)
        else:
            print('Error:  Project name is ambiguous!')
            sys.exit(1)
    else:
        proj_extension = '.' + project[1]

    is_mag = False
    is_gds = False

    if proj_extension == '.mag' or proj_extension == '.mag.gz':
        is_mag = True
    elif proj_extension == '.gds' or proj_extension == '.gds.gz':
        is_gds = True
    else:
        print('Error:  Project is not a magic database or GDS file!')
        sys.exit(1)
 
    if not os.path.isfile(user_project_path):
        print('Error:  Project "' + user_project_path + '" does not exist or is not readable.')
        sys.exit(1)

    # The path where the fill generation script resides should be the same
    # path where the magic startup script resides, for the same PDK
    scriptpath = os.path.dirname(os.path.realpath(__file__))

    # Search for magic startup script.  Order of precedence:
    #  1. PDK_ROOT environment variable
    #  2. Local .magicrc
    #  3. The location of this script

    if os.environ.get('PDK_ROOT'):
        rcfile_path = os.environ.get('PDK_ROOT') + '/ihp-sg13g2/libs.tech/magic/ihp-sg13g2.magicrc'
    elif os.path.isfile(layoutpath + '/.magicrc'):
        rcfile_path = layoutpath + '/.magicrc'
    elif os.path.isfile(scriptpath + '/ihp-sg13g2.magicrc'):
        rcfile_path = scriptpath + '/ihp-sg13g2.magicrc'
    else:
        print('Unknown path to magic startup script.  Please set $PDK_ROOT')
        sys.exit(1)

    if os.path.isdir(layoutpath + '/gds'):
        gdspath = layoutpath + '/gds'
    elif os.path.isdir(layoutpath + '/../gds'):
        gdspath = layoutpath + '/../gds'
    else:
        gdspath = layoutpath
    
    project_file = os.path.split(user_project_path)[1]
    project = project_file.split(os.extsep, 1)[0]
    
    ofile = open(layoutpath + '/generate_fill.tcl', 'w') 
	
    print('#!/usr/bin/env wish', file=ofile)
    print('drc off', file=ofile)
    print('crashbackups stop', file=ofile)
    print('tech unlock *', file=ofile)
    print('snap internal', file=ofile)
    print('box values 0 0 0 0', file=ofile)
    print('box size 800um 800um', file=ofile)
    print('set stepbox [box values]', file=ofile)
    print('set stepwidth [lindex $stepbox 2]', file=ofile)
    print('set stepheight [lindex $stepbox 3]', file=ofile)
    print('', file=ofile)
    print('set starttime [orig_clock format [orig_clock seconds] -format "%D %T"]', file=ofile)
    print('puts stdout "Started: $starttime"', file=ofile)
    print('', file=ofile)
    if is_gds:
        print('gds read ' + project_file, file=ofile)
    # NOTE:  No guarantee that the filename matches the top level cell name;
    # might want to query using "cellname list top"
    print('load ' + project + ' -dereference', file=ofile)
    print('select top cell', file=ofile)
    print('expand', file=ofile)
    if not distmode:
        print('cif ostyle patternfill(tiled)', file=ofile)
    print('', file=ofile)
    # Use FIXED_BBOX as the boundary if it exists
    # (Note:  Actual boundary should be computed by position of SEALBOUND.)
    print('select top cell', file=ofile)
    print('catch {box values {*}[property FIXED_BBOX]}', file=ofile)
    print('set fullbox [box values]', file=ofile)
    print('set xmax [lindex $fullbox 2]', file=ofile)
    print('set xmin [lindex $fullbox 0]', file=ofile)
    print('set fullwidth [expr {$xmax - $xmin}]', file=ofile)
    print('set xtiles [expr {int(ceil(($fullwidth + 0.0) / $stepwidth))}]', file=ofile)
    print('set ymax [lindex $fullbox 3]', file=ofile)
    print('set ymin [lindex $fullbox 1]', file=ofile)
    print('set fullheight [expr {$ymax - $ymin}]', file=ofile)
    print('set ytiles [expr {int(ceil(($fullheight + 0.0) / $stepheight))}]', file=ofile)
    print('box size $stepwidth $stepheight', file=ofile)
    print('set xbase [lindex $fullbox 0]', file=ofile)
    print('set ybase [lindex $fullbox 1]', file=ofile)
    print('', file=ofile)

    # Protect the boundary between the layout border and the seal ring
    # If a seal ring does not exist, then the exclusion area will encompass
    # the entire layout, so ensure that doesn't happen.
    print('select top cell', file=ofile)
    print('select area sealvia6', file=ofile)
    print('set found [what -list]', file=ofile)
    print('if {[lindex $found 0] == "sealvia6"} {', file=ofile)
    print('    box select', file=ofile)
    print('    set sealbox [box values]', file=ofile)
    print('    set seallx [lindex $sealbox 0]', file=ofile)
    print('    set seally [lindex $sealbox 1]', file=ofile)
    print('    set sealux [lindex $sealbox 2]', file=ofile)
    print('    set sealuy [lindex $sealbox 3]', file=ofile)
    print('    box values $xmin $ymin $seallx $ymax', file=ofile)
    print('    paint fillblock; paint obsactive', file=ofile)
    print('    box values $xmin $ymin $xmax $seallx', file=ofile)
    print('    paint fillblock; paint obsactive', file=ofile)
    print('    box values $sealux $ymin $xmax $ymax', file=ofile)
    print('    paint fillblock; paint obsactive', file=ofile)
    print('    box values $xmin $sealuy $xmax $ymax', file=ofile)
    print('    paint fillblock; paint obsactive', file=ofile)
    # Block fill in the corners
    print('    box position $seallx $seally', file=ofile)
    print('    box size 21um 21um', file=ofile)
    print('    splitpaint sw fillblock,obsactive', file=ofile)
    print('    box position $sealux $seally', file=ofile)
    print('    box move w 21um', file=ofile)
    print('    splitpaint se fillblock,obsactive', file=ofile)
    print('    box position $seallx $sealuy', file=ofile)
    print('    box move s 21um', file=ofile)
    print('    splitpaint nw fillblock,obsactive', file=ofile)
    print('    box position $sealux $sealuy', file=ofile)
    print('    box move sw 21um', file=ofile)
    print('    splitpaint ne fillblock,obsactive', file=ofile)
    print('}', file=ofile) 

    # Break layout into tiles and process each separately
    print('for {set y 0} {$y < $ytiles} {incr y} {', file=ofile)
    print('    for {set x 0} {$x < $xtiles} {incr x} {', file=ofile)
    print('        set xlo [expr $xbase + $x * $stepwidth]', file=ofile)
    print('        set ylo [expr $ybase + $y * $stepheight]', file=ofile)
    print('        set xhi [expr $xlo + $stepwidth]', file=ofile)
    print('        set yhi [expr $ylo + $stepheight]', file=ofile)
    print('        if {$xhi > $fullwidth} {set xhi $fullwidth}', file=ofile)
    print('        if {$yhi > $fullheight} {set yhi $fullheight}', file=ofile)
    print('        box values $xlo $ylo $xhi $yhi', file=ofile)
    # The flattened area must be larger than the fill tile by >1.5um
    print('        box grow c 1.6um', file=ofile)

    # Flatten into a cell with a new name
    print('        puts stdout "Flattening layout of tile x=$x y=$y. . . "', file=ofile)
    print('        flush stdout', file=ofile)
    print('        update idletasks', file=ofile)
    print('        flatten -dobox -nolabels ' + project + '_fill_pattern_${x}_$y', file=ofile)
    print('        load ' + project + '_fill_pattern_${x}_$y', file=ofile)

    # Remove any GDS_FILE reference (there should not be any?)
    print('        property GDS_FILE ""', file=ofile)
    # Set boundary using comment layer, to the size of the step box
    # This corresponds to the "topbox" rule in the patternfill(tiled) style
    print('        select top cell', file=ofile)
    print('        erase comment', file=ofile)
    print('        box values $xlo $ylo $xhi $yhi', file=ofile)
    print('        paint comment', file=ofile)

    if not distmode:
        print('        puts stdout "Writing GDS. . . "', file=ofile)

    print('        flush stdout', file=ofile)
    print('        update idletasks', file=ofile)

    if distmode:
        print('        writeall force ' + project + '_fill_pattern_${x}_$y', file=ofile)
    else:
        print('        gds write ' + project + '_fill_pattern_${x}_$y.gds', file=ofile)

    # Reload project top
    print('        load ' + project, file=ofile)

    # Remove last generated cell to save memory
    print('        cellname delete ' + project + '_fill_pattern_${x}_$y', file=ofile)

    print('    }', file=ofile)
    print('}', file=ofile)

    if distmode:
        print('set ofile [open fill_gen_info.txt w]', file=ofile)
        print('puts $ofile "$stepwidth"', file=ofile)
        print('puts $ofile "$stepheight"', file=ofile)
        print('puts $ofile "$xtiles"', file=ofile)
        print('puts $ofile "$ytiles"', file=ofile)
        print('puts $ofile "$xbase"', file=ofile)
        print('puts $ofile "$ybase"', file=ofile)
        print('close $ofile', file=ofile)
        print('quit -noprompt', file=ofile)
        ofile.close()

        with open(layoutpath + '/generate_fill_dist.tcl', 'w') as ofile:
            print('#!/usr/bin/env wish', file=ofile)
            print('drc off', file=ofile)
            print('tech unlock *', file=ofile)
            print('snap internal', file=ofile)
            print('box values 0 0 0 0', file=ofile)
            print('set filename [file root [lindex $argv $argc-1]]', file=ofile)
            print('load $filename', file=ofile)
            print('cif ostyle patternfill(tiled)', file=ofile)
            print('gds write [file root $filename].gds', file=ofile)
            print('quit -noprompt', file=ofile)

        ofile = open(layoutpath + '/generate_fill_final.tcl', 'w')
        print('#!/usr/bin/env wish', file=ofile)
        print('drc off', file=ofile)
        print('tech unlock *', file=ofile)
        print('snap internal', file=ofile)
        print('box values 0 0 0 0', file=ofile)

        print('set ifile [open fill_gen_info.txt r]', file=ofile)
        print('gets $ifile stepwidth', file=ofile)
        print('gets $ifile stepheight', file=ofile)
        print('gets $ifile xtiles', file=ofile)
        print('gets $ifile ytiles', file=ofile)
        print('gets $ifile xbase', file=ofile)
        print('gets $ifile ybase', file=ofile)
        print('close $ifile', file=ofile)
        print('cif ostyle patternfill(tiled)', file=ofile)

    # Now create simple "fake" views of all the tiles.
    print('gds readonly true', file=ofile)
    print('gds rescale false', file=ofile)
    print('for {set y 0} {$y < $ytiles} {incr y} {', file=ofile)
    print('    for {set x 0} {$x < $xtiles} {incr x} {', file=ofile)
    print('        set xlo [expr $xbase + $x * $stepwidth]', file=ofile)
    print('        set ylo [expr $ybase + $y * $stepheight]', file=ofile)
    print('        set xhi [expr $xlo + $stepwidth]', file=ofile)
    print('        set yhi [expr $ylo + $stepheight]', file=ofile)
    print('        load ' + project + '_fill_pattern_${x}_$y -silent', file=ofile)
    print('        box values $xlo $ylo $xhi $yhi', file=ofile)
    print('        paint comment', file=ofile)
    print('        property FIXED_BBOX "$xlo $ylo $xhi $yhi"', file=ofile)
    print('        property GDS_FILE ' + project + '_fill_pattern_${x}_${y}.gds', file=ofile)
    print('        property GDS_START 0', file=ofile)
    print('    }', file=ofile)
    print('}', file=ofile)

    # Now tile everything back together
    print('load ' + project + '_fill_pattern -silent', file=ofile)
    print('for {set y 0} {$y < $ytiles} {incr y} {', file=ofile)
    print('    for {set x 0} {$x < $xtiles} {incr x} {', file=ofile)
    print('        box values 0 0 0 0', file=ofile)
    print('        getcell ' + project + '_fill_pattern_${x}_$y child 0 0', file=ofile)
    print('    }', file=ofile)
    print('}', file=ofile)

    # And write final GDS
    print('puts stdout "Writing final GDS"', file=ofile)

    print('cif *hier write disable', file=ofile)
    print('cif *array write disable', file=ofile)
    print('gds compress 9', file=ofile)
    print('gds write ' + gdspath + '/' + project + '_fill_pattern.gds.gz', file=ofile)
    print('set endtime [orig_clock format [orig_clock seconds] -format "%D %T"]', file=ofile)
    print('puts stdout "Ended: $endtime"', file=ofile)
    print('quit -noprompt', file=ofile)
    ofile.close()
    
    myenv = os.environ.copy()
    myenv['MAGTYPE'] = 'mag'

    if not testmode:
        # Diagnostic
        # print('This script will generate file ' + project + '_fill_pattern.gds.gz')
        print('This script will generate files ' + project + '_fill_pattern_x_y.gds')
        print('Now generating fill patterns.  This may take. . . quite. . . a while.', flush=True)
        
        magic_run_opts = [
		'magic',
		'-dnull',
		'-noconsole',
		'-rcfile', rcfile_path,
		layoutpath + '/generate_fill.tcl']

        if debugmode:
            print('Running: ' + ' '.join(magic_run_opts))

        mproc = subprocess.run(magic_run_opts,
		stdin = subprocess.DEVNULL,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		cwd = layoutpath,
		env = myenv,
		universal_newlines = True)

        if mproc.stdout:
            for line in mproc.stdout.splitlines():
                print(line)
        if mproc.stderr:
            print('Error message output from magic:')
            for line in mproc.stderr.splitlines():
                print(line)
            if mproc.returncode != 0:
                print('ERROR:  Magic exited with status ' + str(mproc.returncode))
	
        if distmode:
            # If using distributed mode, then run magic on each of the generated
            # layout files
            pool = multiprocessing.Pool()
            magfiles = glob.glob(layoutpath + '/' + project + '_fill_pattern_*.mag')
            # NOTE:  Adding 'x' to the end of each filename, or else magic will
            # try to read it from the command line as well as passing it as an
            # argument to the script.  We only want it passed as an argument.
            magxfiles = list(item + 'x' for item in magfiles)
            makegdsfunc = functools.partial(makegds, rcfile=rcfile_path)
            pool.map(makegdsfunc, magxfiles)

            # If using distributed mode, then remove all of the temporary .mag files
            # and then run the final generation script.
            for file in magfiles:
                os.remove(file)

            mproc = subprocess.run(['magic', '-dnull', '-noconsole',
			'-rcfile', rcfile_path, layoutpath + '/generate_fill_final.tcl'],
			stdin = subprocess.DEVNULL,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			cwd = layoutpath,
			env = myenv,
			universal_newlines = True)
            if mproc.stdout:
                for line in mproc.stdout.splitlines():
                    print(line)
            if mproc.stderr:
                print('Error message output from magic:')
                for line in mproc.stderr.splitlines():
                    print(line)
                if mproc.returncode != 0:
                    print('ERROR:  Magic exited with status ' + str(mproc.returncode))

    if not keepmode:
        # Remove fill generation script
        os.remove(layoutpath + '/generate_fill.tcl')
        # Remove all individual fill tiles, leaving only the composite GDS.
        filelist = os.listdir(layoutpath)
        for file in filelist:
            if os.path.splitext(layoutpath + '/' + file)[1] == '.gds':
                if file.startswith(project + '_fill_pattern_'):
                    os.remove(layoutpath + '/' + file)

        if distmode:
            os.remove(layoutpath + '/generate_fill_dist.tcl')
            os.remove(layoutpath + '/generate_fill_final.tcl')
            os.remove(layoutpath + '/fill_gen_info.txt')
            if testmode:
                magfiles = glob.glob(layoutpath + '/' + project + '_fill_pattern_*.mag')
                for file in magfiles:
                    os.remove(file)

    print('Done!')
    exit(0)
