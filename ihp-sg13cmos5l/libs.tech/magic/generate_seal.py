#!/usr/bin/env python3
########################################################################
#
# Copyright 2025 IHP PDK Authors
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
#
########################################################################

#
# generate_seal.py ---
#
#    Run the seal ring generation to create cell "sealring_complete"
#    with the specified padframe dimensions.
#
#    Arguments:  width and height (height is optional if width = height).
#
#    The location of the corner and side source files is the same as
#    the location of generate_seal.py, in the PDK.  The resulting cells
#    are placed in the current working directory from which the script
#    is invoked.
#
#----------------------------------------------------------------------
# Written by Tim Edwards, Open Circuit Design LLC, for IHP GmbH
# September 8, 2025
#

import sys
import os
import subprocess

def usage():
    print("Usage:")
    print("generate_seal.py <width> [<height> [<extra_separation>]]")
    print("")
    print("where:")
    print("    <width> and <height> are the padframe dimensions, in microns.")
    print("    <extra_separation> is the distance from padframe to seal ring")
    print("    in addition to the 5.4um absolute minimum.")
    print("")
    return 0


if __name__ == '__main__':

    optionlist = []
    arguments = []

    debugmode = False

    for option in sys.argv[1:]:
        if option.find('-', 0) == 0:
            optionlist.append(option)
        else:
            arguments.append(option)

    if len(arguments) == 0 or len(arguments) > 3:
        print("Wrong number of arguments given to generate_seal.py.")
        usage()
        sys.exit(1)

    # Process options

    if '-debug' in optionlist:
        debugmode = True
        print('Running in debug mode.')

    # Find width and height values in microns from the argument list
    # If only one dimension is given, assume that the layout is square.
    # If no dimensions are given, print an error.

    if len(arguments) < 1:
        print('Error:  At least one dimension is required.')
        usage()
        sys.exit(1)
    else:
        frame_width = arguments[0]

    if len(arguments) < 2:
        frame_height = arguments[0]
    else:
        frame_height = arguments[1]

    if len(arguments) == 3:
        extra_sep = 2.0 * float(arguments[2])
    else:
        extra_sep = 0.0

    if os.environ.get('PDK_ROOT'):
        magic_path = os.environ.get('PDK_ROOT') + '/ihp-sg13g2/libs.tech/magic/'
    else:
        print('Unknown path to magic files.  Please set $PDK_ROOT')
        sys.exit(1)

    rcfile_path = magic_path + 'ihp-sg13g2.magicrc'

    curpath = os.getcwd()
    ofile = open(curpath + '/generate_seal.tcl', 'w') 
	
    print('#!/usr/bin/env wish', file=ofile)
    print('drc off', file=ofile)
    print('crashbackups stop', file=ofile)
    print('locking disable', file=ofile)
    print('tech unlock *', file=ofile)
    print('snap internal', file=ofile)
    print('source ' + magic_path + 'sealring_corner.tcl', file=ofile)
    # Note:  Total width includes the separation on both sides
    print('set separation [magic::u2i [expr {10.8 + ' + str(extra_sep) + '}]]',
		file=ofile)

    print('set sealring_iwidth [magic::u2i ' + frame_width + ']', file=ofile)
    # The corners are part of the frame dimension, so subtract off the
    # amount of distance the side shares with the corner cell.
    print('set sealring_iwidth [expr {$sealring_iwidth + $separation}]', file=ofile)
    print('set sealring_width [expr {$sealring_iwidth - 7000}]', file=ofile)

    if frame_width != frame_height:
        print('set sealring_suffix _topbottom', file=ofile)
    print('source ' + magic_path + 'sealring_side.tcl', file=ofile)

    if frame_width != frame_height:
        print('set sealring_iheight [magic::u2i ' + frame_height + ']', file=ofile)
        print('set sealring_iheight [expr {$sealring_iheight + $separation}]', file=ofile)
        print('set sealring_width [expr {$sealring_iheight - 7000}]', file=ofile)
        print('set sealring_suffix _leftright', file=ofile)
        print('source ' + magic_path + 'sealring_side.tcl', file=ofile)
    else:
        print('set sealring_iheight $sealring_iwidth', file=ofile)
        print('set sealring_iheight [expr {$sealring_iheight + $separation}]', file=ofile)

    # Now we have either one cell called sealring_side or two cells called
    # sealring_side_topbottom and sealring_side_leftright, plus one cell
    # called sealring_corner.  So the sealring can be assembled.

    print('cellname create sealring_complete', file=ofile)
    print('load sealring_complete', file=ofile)
    print('box values 0 0 0 0', file=ofile)
    print('getcell sealring_corner', file=ofile)
    print('identify sealring_corner_sw', file=ofile)
    print('box position 5640 0', file=ofile)
    if frame_width != frame_height:
        print('getcell sealring_side_topbottom', file=ofile)
    else:
        print('getcell sealring_side', file=ofile)
    print('identify sealring_side_s', file=ofile)

    print('box position 0 5640', file=ofile)
    if frame_width != frame_height:
        print('getcell sealring_side_leftright 90', file=ofile)
    else:
        print('getcell sealring_side 90', file=ofile)
    print('identify sealring_side_w', file=ofile)

    print('box position [expr {$sealring_iwidth - 1360}] 0', file=ofile)
    print('getcell sealring_corner 270', file=ofile)
    print('identify sealring_corner_se', file=ofile)

    print('box position [expr {$sealring_iwidth + 2140}] 5640', file=ofile)
    if frame_width != frame_height:
        print('getcell sealring_side_leftright 270', file=ofile)
    else:
        print('getcell sealring_side 270', file=ofile)
    print('identify sealring_side_e', file=ofile)

    print('box position 0 [expr {$sealring_iheight - 1360}]', file=ofile)
    print('getcell sealring_corner 90', file=ofile)
    print('identify sealring_corner_nw', file=ofile)

    print('box position 5640 [expr {$sealring_iheight + 2140}]', file=ofile)
    if frame_width != frame_height:
        print('getcell sealring_side_topbottom 180', file=ofile)
    else:
        print('getcell sealring_side 180', file=ofile)
    print('identify sealring_side_n', file=ofile)

    print('box position [expr {$sealring_iwidth - 1360}] [expr {$sealring_iheight - 1360}]', file=ofile)
    print('getcell sealring_corner 180', file=ofile)
    print('identify sealring_corner_ne', file=ofile)

    if frame_width != frame_height:
        print('writeall force sealring_side_topbottom', file=ofile)
        print('writeall force sealring_side_leftright', file=ofile)
    else:
        print('writeall force sealring_side', file=ofile)
    print('writeall force sealring_corner', file=ofile)
    print('writeall force sealring_complete', file=ofile)

    print('quit -noprompt', file=ofile)
    ofile.close()

    myenv = os.environ.copy()
    myenv['MAGTYPE'] = 'mag'

    magic_run_opts = [
	'magic',
	'-dnull',
	'-noconsole',
	'-rcfile', rcfile_path,
	curpath + '/generate_seal.tcl']

    if debugmode:
        print('Running: ' + ' '.join(magic_run_opts))

    mproc = subprocess.run(magic_run_opts,
		stdin = subprocess.DEVNULL,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		cwd = curpath,
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
	

    # Remove fill generation script
    if not debugmode:
        os.remove(curpath + '/generate_seal.tcl')

    print('Done!')
    exit(0)
