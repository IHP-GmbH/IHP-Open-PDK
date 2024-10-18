#!/usr/bin/env python3

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
    - compiles and places PSP103 model in ../ngspice/openvaf/ location. 
    - creates a symlink to the ../ngspice/.spiceinit file in your $HOME directory
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
        source_directory=pdk_root + "/ihp-sg13g2/libs.tech/ngspice/openvaf"

    username = os.environ.get("USER")
    destination_directory = pdk_root + "/ihp-sg13g2/libs.tech/ngspice/openvaf"
    
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")
    
    
    program_name = "openvaf"
    if is_program_installed(program_name):
        command = "openvaf psp103_nqs.va --output " + destination_directory + "/psp103_nqs.osdi"    
        print(f"{program_name} is installed and about to run the command '{command}' in a location: {source_directory} ")	
        exec_app_in_directory(command, source_directory)
    else:
        print(f"{program_name} is not installed.")
    	

    original_file =  pdk_root + "/ihp-sg13g2/libs.tech/ngspice/.spiceinit"
    symbolic_link = "/home/" + username + "/.spiceinit"
    # Create the symbolic link
    if not os.path.exists(symbolic_link):
        try:
            os.symlink(original_file, symbolic_link)
            print(f"Symbolic link '{symbolic_link}' created successfully.")
        except OSError as e:
            print(f"Failed to create symbolic link: {e}")


 	


