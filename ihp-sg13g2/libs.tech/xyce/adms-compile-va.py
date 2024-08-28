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


import shutil
import os
import subprocess


def exec_app_in_directory(command, directory):
    try:
        subprocess.run(command, cwd=directory, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command in directory {directory}: {e}")

def is_program_installed(program_name):
    try:
        subprocess.run([program_name, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False



def info():
    msg = """
    This script:
    - compiles and places PSP103 model in ../xyce/plugins/ location. 
    Please make sure that you have set up the PDK_ROOT env variable export PDK_ROOT=your_location/IHP-Open-PDK 
    """
    print(msg)


if __name__ == "__main__":
    # Example usage:
    info()
    pdk_root = os.environ.get("PDK_ROOT")
    if not pdk_root:
        print("setup PDK_ROOT environmental variable to IHP-Open-PDK location")
    else:
        source_directory=pdk_root + "/ihp-sg13g2/libs.tech/xyce/adms/psp103"

    destination_directory = pdk_root + "/ihp-sg13g2/libs.tech/xyce/plugins"
    
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")
    
    
    program_name = "buildxyceplugin"
    if is_program_installed(program_name):
        command = f"{program_name} psp103_nqs.va " + destination_directory    
        print(f"{program_name} is installed and about to run the command '{command}' in a location: {source_directory} ")	
        exec_app_in_directory(command, source_directory)
    else:
        print(f"{program_name} is not installed.")
    	
    exec_app_in_directory("rm *.log", source_directory)
    exec_app_in_directory("rm *.la", source_directory)
    exec_app_in_directory("rm -rf .libs", source_directory)
