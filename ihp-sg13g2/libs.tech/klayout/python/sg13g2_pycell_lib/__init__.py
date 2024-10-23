########################################################################
#
# Copyright 2024 IHP PDK Authors
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

import pya
import os
import sys

from cni.tech import Tech
from cni.dlo import PCellWrapper

# Creates the SG13_dev technology
from .sg13_tech import *

from pypreprocessor.pypreprocessor import preprocessor as preProcessor

import pya

import os
import io
import sys
import inspect
import re
import importlib
import importlib.util
import pathlib
import tempfile
import traceback

moduleNames = [
        'nmos_code',
        'nmosHV_code',
        'pmos_code',
        'pmosHV_code',
        'cmim_code',
        'rsil_code',
        'rhigh_code',
        'rppd_code',
        'sealring_code',
        'npn13G2_base_code',
        'npn13G2_code',
        'npn13G2L_code',
        'npn13G2V_code',
        'inductor2_code',
        'inductor2_sc_code',
        'inductor2_sp_code',
        'inductor3_code',
        'inductor3_sc_code',
        'inductor3_sp_code',
        'dantenna_code',
        'dpantenna_code'
]

def getProcessNames():
    processNames = []
    maxDepth = 10

    if sys.platform.startswith('win'):
        process = pya.QProcess()
        powershellCmd = (
            "Get-CimInstance Win32_Process | "
            "Select-Object ProcessId, ParentProcessId, Name | "
            "Format-Table -HideTableHeaders"
        )
        process.start("powershell", ["-Command", powershellCmd])
        process.waitForFinished()
        output = process.readAllStandardOutput().decode()

        # Parse the output into a list of tuples (pid, ppid, name)
        processList = []
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 3:
                pid = int(parts[0])
                ppid = int(parts[1])
                name = ' '.join(parts[2:])
                processList.append((pid, ppid, name))

        processDict = {pid: (ppid, name) for pid, ppid, name in processList}
        currentPid = os.getpid()

        while currentPid in processDict and maxDepth > 0:
            maxDepth -= 1
            ppid, name = processDict[currentPid]
            processNames.append(name.lower())
            if ppid == currentPid or ppid == 0:
                break
            currentPid = ppid

    else:
        import psutil

        parent = None

        p = psutil.Process()
        with p.oneshot():
            processNames.append(p.name().lower())
            parent = p.parent()

        while parent is not None and maxDepth > 0:
            maxDepth -= 1
            with parent.oneshot():
                processNames.append(parent.name().lower())
                parent = parent.parent()

    return processNames


"""
Support for 'conditional compilation' in a C-style manner of PyCell code:

#ifdef name
    ...some_code...
#else
    ...some_other_code...
#endif

The #ifdef-block is executed (name is considered as defined) if
  1. An environment variable 'name' can be found case-insentive, or
  2. The name can be found case-insentive as part of a process name of the process chain beginnig at
     the current process upwards through all parent processes.
otherwise the #else-block is executed

The current process chain will be dumped if the environment variable 'IHP_PYCELL_LIB_PRINT_PROCESS_TREE'
is set.

The list of names which are used in an #ifdef-statement and are considered as 'defined' will be dumped
if the environment variable 'IHP_PYCELL_LIB_PRINT_DEFINES_SET' is set.

"""
class PyCellLib(pya.Library):
    def __init__(self):
        self.description = "IHP SG13G2 Pcells"

        tech = Tech.get('SG13_dev')

        processNames = getProcessNames()

        if os.getenv('IHP_PYCELL_LIB_PRINT_PROCESS_TREE') is not None:
            processChain = ''
            isFirst = True
            for processName in reversed(processNames):
                if not isFirst:
                    processChain += ' <- '
                processChain += "'" + processName + "'"
                isFirst = False
            print(f'Current process chain: {processChain}')

        module = importlib.import_module(f"{__name__}.ihp.pypreprocessor")
        preProcessor = getattr(module, "preprocessor")

        definesSetToPrint = []

        for moduleName in moduleNames:
            defines = []
            definesSet = []

            modulePath = os.path.join(os.path.dirname(__file__), 'ihp', f"{moduleName}.py")
            moduleFile = io.open(modulePath, 'r', encoding=sys.stdin.encoding)

            try:
                for line in moduleFile:
                    match = re.match(r'^#ifdef\s+\w+', line)
                    if match:
                        splittedLine = line.split()
                        for i, define in enumerate(splittedLine):
                            if i % 2 == 1:
                                if define not in defines:
                                    defines.append(define)

            finally:
                moduleFile.close()

            envs = []
            for env in os.environ:
                envs.append(env.lower())

            for define in defines:
                locDefine = define.lower()
                for processName in processNames:
                    if processName.find(locDefine) != -1:
                        definesSet.append(define)
                else:
                    if locDefine in envs:
                        definesSet.append(define)

            for defineSet in definesSet:
                definesSetToPrint.append(defineSet)

            modulePreProcPath = None

            if len(defines) > 0:
                modulePreProcPath = os.path.join(tempfile.gettempdir(), f"{moduleName}_pre.py")

                pyPreProcessor = preProcessor(modulePath, modulePreProcPath, definesSet, removeMeta=False, resume=True, run=False)
                pyPreProcessor.parse()

                spec = importlib.util.spec_from_file_location(f"{__name__}.ihp.{moduleName}", modulePreProcPath)
                module = importlib.util.module_from_spec(spec)
                sys.modules[moduleName] = module

                try:
                    spec.loader.exec_module(module)
                except:
                    trace = traceback.format_exc().splitlines()
                    for line in trace:
                        print(line.replace(modulePreProcPath, modulePath))

                    sys.exit(1)

                os.remove(modulePreProcPath)
            else:
                module = importlib.import_module(f"{__name__}.ihp." + moduleName)

            match = re.fullmatch(r'^(\S+)_code$', moduleName)
            if match:
                func = getattr(module, f"{match.group(1)}")
                self.layout().register_pcell(match.group(1), PCellWrapper(func(), tech, modulePreProcPath, modulePath))

        if os.getenv('IHP_PYCELL_LIB_PRINT_DEFINES_SET') is not None:
            print(f"Current defines set: {definesSetToPrint}")

        self.register("SG13_dev")

# instantiate and register the library
PyCellLib()

