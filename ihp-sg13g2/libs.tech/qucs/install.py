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


def copy_files(source_dir, destination_dir):
    # Get a list of files in the source directory
    files = os.listdir(source_dir)
    
    # Copy each file from source to destination
    for file in files:
        source_file = os.path.join(source_dir, file)
        destination_file = os.path.join(destination_dir, file)
        shutil.copy(source_file, destination_file)
        print(f"File '{file}' copied to '{destination_dir}'.")

def info():
    msg = """
    This script copies the Qucs-S user library files into 
    /home/$USER/.qucs/user_lib directory. 
    It also creates a symbolic link there and compiles and places 
    PSP103 model in ~/.qucs/ location. 
    Please make sure that you have set up the PDK_ROOT env variable
    export PDK_ROOT=your_location/IHP-Open-PDK 
    """
    print(msg)


if __name__ == "__main__":
    # Example usage:
    info()
    pdk_root = os.environ.get("PDK_ROOT")
    if not pdk_root:
        print("setup PDK_ROOT environmental variable to IHP-Open-PDK location")
    else:
        source_directory=pdk_root + "/ihp-sg13g2/libs.tech/qucs/user_lib"

    username = os.environ.get("USER")
    destination_directory = "/home/" + username + "/.qucs/user_lib"
    
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")
    
    # Check if the destination directory exists, if not, create it
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        print(f"Destination directory '{destination_directory}' created.")
    
    copy_files(source_directory, destination_directory)
    
    # Copy examples to "Qucs Home" (/home/<username>/.qucs/)
    print("Copying examples into Qucs-S Home...")
    source_directory=pdk_root + "/ihp-sg13g2/libs.tech/qucs/examples"
    destination_directory = "/home/" + username + "/.qucs/IHP-Open-PDK-SG13G2-Examples_prj"
    
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        
    copy_files(source_directory, destination_directory)
    print("Examples copied")
    print("\n\n#############################################")
    print("              IMPORTANT NOTE")
    print("#############################################\n")
    print("Before using the PDK example schematics, you must add the PDK library path to the Qucs-S search path list.\n")
    print("Please read the instructions provided in " + destination_directory + "/README.txt\n")
    print("#############################################\n\n")

    original_file = pdk_root
    symbolic_link = "/home/" + username + "/.qucs/IHP-Open-PDK-main"
    # Create the symbolic link
    if not os.path.exists(symbolic_link):
        try:
            os.symlink(original_file, symbolic_link)
            print(f"Symbolic link '{symbolic_link}' created successfully.")
        except OSError as e:
            print(f"Failed to create symbolic link: {e}")

    program_name = "openvaf"
    if is_program_installed(program_name):
        command = "openvaf psp103_nqs.va --output " + "/home/" + username + "/.qucs/psp103_nqs.osdi"    
        directory = pdk_root + "/ihp-sg13g2/libs.tech/ngspice/openvaf"
        print(f"{program_name} is installed and about to run the command '{command}' in a location: {directory} ")	
        exec_app_in_directory(command, directory)
    else:
        print(f"{program_name} is not installed.")
    	



 	


