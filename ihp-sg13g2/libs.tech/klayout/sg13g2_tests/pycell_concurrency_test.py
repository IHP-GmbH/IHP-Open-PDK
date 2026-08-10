########################################################################
#
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
#
########################################################################

# Checks that several KLayout processes can load the SG13_dev PCell library at
# the same time without interfering with each other.
#
# The library preprocesses every PCell module that uses '#ifdef' into a file in
# the system temp directory before importing it. If that file name is shared
# between processes, concurrent loads overwrite and delete each other's file and
# the losing process ends up with an incomplete library, or with no library at
# all.
#
# To run this code, use (Sh/Bash syntax):
#
# (in the location of this file):
# python3 pycell_concurrency_test.py [number_of_processes]
#
# The same file is re-executed inside each KLayout process as the worker.

import os
import subprocess
import sys
import shutil
import tempfile

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TECH_DIR = os.path.dirname(TEST_DIR)

LIBRARY_NAME = 'SG13_dev'
TECHNOLOGY_NAME = 'sg13g2'

# A PCell whose module uses '#ifdef', so it goes through the preprocessed path.
PROBE_PCELL = 'rfnmos'

DEFAULT_PROCESSES = 8

# Tells the copy running inside KLayout that it is the worker. Checking for an
# importable 'pya' is not enough: the standalone KLayout Python module provides
# one outside of KLayout as well.
WORKER_ENV = 'IHP_PYCELL_CONCURRENCY_WORKER'


def runWorker():
    # Runs inside KLayout. Reports how many PCells the library registered.
    import pya

    # With an empty KLAYOUT_HOME the technology is not the current one, so it
    # has to be selected explicitly, otherwise no PCell resolves.
    layout = pya.Layout()
    layout.technology_name = TECHNOLOGY_NAME

    library = pya.Library.library_by_name(LIBRARY_NAME, TECHNOLOGY_NAME)
    if library is None:
        print('PCELLS 0')
        print('ERROR: library %s is not registered' % LIBRARY_NAME)
        return 1

    pcellNames = library.layout().pcell_names()
    print('PCELLS %d' % len(pcellNames))

    # A registered but unusable library is just as broken, so build one PCell
    # that goes through the preprocessed path.
    layout.create_cell(PROBE_PCELL, LIBRARY_NAME, {})

    return 0 if len(pcellNames) > 0 else 1


def parsePCellCount(output):
    for line in output.splitlines():
        if line.startswith('PCELLS '):
            return int(line.split()[1])
    return None


def runKLayout(env):
    return subprocess.Popen(
        ['klayout', '-zz', '-r', os.path.abspath(__file__)],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True)


def collect(process):
    output = process.communicate()[0]
    return {
        'returncode': process.returncode,
        'output': output,
        'pcells': parsePCellCount(output),
    }


def report(label, result, reference=None):
    ok = (result['returncode'] == 0 and result['pcells'] is not None
          and (reference is None or result['pcells'] == reference))
    print('  %-12s rc=%-3s pcells=%-5s %s'
          % (label, result['returncode'], result['pcells'],
             'ok' if ok else 'FAILED'))
    if not ok:
        for line in result['output'].splitlines():
            if 'Error' in line or 'error' in line or 'Traceback' in line:
                print('      | %s' % line)
    return ok


def runLauncher(processCount):
    # A clean KLAYOUT_HOME is mandatory: a salt-installed IHP PDK registers its
    # own SG13_dev technology and library and would win over the one under test.
    klayoutHome = tempfile.mkdtemp(prefix='klayout_home_')

    env = os.environ.copy()
    env['KLAYOUT_PATH'] = TECH_DIR
    env['KLAYOUT_HOME'] = klayoutHome
    env[WORKER_ENV] = '1'

    try:
        print('KLAYOUT_PATH = %s' % TECH_DIR)
        print('Reference run (single process):')
        reference = collect(runKLayout(env))
        if not report('reference', reference):
            print('Reference run already fails, nothing to compare against.')
            print(reference['output'])
            return 1

        expected = reference['pcells']
        print('Concurrent runs (%d processes, expecting %d PCells each):'
              % (processCount, expected))

        processes = [runKLayout(env) for _ in range(processCount)]
        results = [collect(process) for process in processes]

        failed = 0
        for i, result in enumerate(results):
            if not report('run %d' % i, result, expected):
                failed += 1

        if failed:
            print('FAILED: %d of %d concurrent loads did not register the '
                  'complete library.' % (failed, processCount))
            return 1

        print('PASSED: all %d concurrent loads registered %d PCells.'
              % (processCount, expected))
        return 0

    finally:
        shutil.rmtree(klayoutHome, ignore_errors=True)


def main():
    if os.getenv(WORKER_ENV) is not None:
        return runWorker()

    processCount = DEFAULT_PROCESSES
    if len(sys.argv) > 1:
        processCount = int(sys.argv[1])

    return runLauncher(processCount)


sys.exit(main())
