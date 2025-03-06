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
import logging


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
    This script:
    - copies the Qucs-S user library files into $HOME/[.qucs|QucsWorkspace]/user_lib directory. 
    - compiles and copies Verilog-A models in ../ngspice/osdi location
    Please make sure that you have set up the PDK_ROOT env variable
    export PDK_ROOT=<path_to_IHP-Open-PDK>
    """
    print(msg)


def create_symlinks(source_directory, destination_directory):
    """
    Creates symbolic links for all files in source_directory inside destination_directory.
    """
    # Ensure both directories exist
    if not os.path.exists(source_directory):
        print(f"Error: Source directory '{source_directory}' does not exist.")
        return
    
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Iterate over files in the source directory
    for file_name in os.listdir(source_directory):
        source_path = os.path.join(source_directory, file_name)
        dest_path = os.path.join(destination_directory, file_name)

        # Only create symlinks for files
        if os.path.isfile(source_path):
            try:
                if os.path.exists(dest_path) or os.path.islink(dest_path):
                    print(f"Skipping existing: {dest_path}")
                else:
                    os.symlink(source_path, dest_path)
                    print(f"Linked: {source_path} -> {dest_path}")
            except OSError as e:
                print(f"Error creating symlink for {source_path}: {e}")


if __name__ == "__main__":
    # Example usage:
    info()
    
    # Check if 'Qucs-S' tool is available
    program_name = "qucs-s"
    if not is_program_installed(program_name):
        logging.error(f"{program_name} is not installed.")
        exit(1)
    
    # Check if PDK_ROOT env variable exists
    pdk_root = os.environ.get("PDK_ROOT")
    if pdk_root == None:
        logging.error("Setup PDK_ROOT environment variable to IHP-Open-PDK location")
        exit(1)
    else:
        source_directory = pdk_root + "/ihp-sg13g2/libs.tech/qucs/user_lib"

    userhome = os.environ.get("HOME")
    
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        logging.error(f"Source directory '{source_directory}' does not exist.")
        exit(1)    
    
    # Supporting two variants of Qucs-S default workspace
    for qucs_workspace in ['/.qucs/', '/QucsWorkspace/']:
    
        print(f"Preparing $HOME{qucs_workspace} directory ...")
        print("#############################################\n")
        
        destination_directory = userhome + qucs_workspace + "user_lib"
        
        # Check if the destination directory exists, if not, create it
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
            print(f"Destination directory '{destination_directory}' created.")
        
        #copy_files(source_directory, destination_directory)
        create_symlinks(source_directory, destination_directory)
        # Copy examples to "Qucs Home" (<userhome>/[.qucs|QucsWorkspace]/)
        print("Copying examples into Qucs-S Home...")
        source_directory = pdk_root + "/ihp-sg13g2/libs.tech/qucs/examples"
        destination_directory = userhome + qucs_workspace + "IHP-Open-PDK-SG13G2-Examples_prj"

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        copy_files(source_directory, destination_directory)
        print("Examples copied")
        print("\n\n#############################################")
        print("              IMPORTANT NOTE")
        print("#############################################\n")
        print("Before using the PDK example schematics, you must add the PDK library path to the Qucs-S search path list.\n")
        print("Please read the instructions provided in " + destination_directory + "/README.md\n")
        print("#############################################\n")
       
        original_file = pdk_root + "/ihp-sg13g2/libs.tech/ngspice/.spiceinit"
        symbolic_link = userhome + "/.spiceinit"
        # Create the symbolic link to ngspice global settings file
        if not os.path.exists(symbolic_link):
            try:
                os.symlink(original_file, symbolic_link)
                print(f"Symbolic link '{symbolic_link}' created successfully.")
            except OSError as e:
                print(f"Failed to create symbolic link: {e}")

        original_file = pdk_root
        symbolic_link = userhome + qucs_workspace + "IHP-Open-PDK"
        # Create the symbolic link to IHP OpenPDK directory
        if not os.path.exists(symbolic_link):
            try:
                os.symlink(original_file, symbolic_link)
                print(f"Symbolic link '{symbolic_link}' created successfully.")
            except OSError as e:
                print(f"Failed to create symbolic link: {e}")
        
        # Post-processing example schematics
        program_name = "sed"
        if is_program_installed(program_name):
            userhome_escaped = userhome.replace('/', '\\/')
            command = f"sed -i 's/<userhome>/{userhome_escaped}/;s/<qucs_workspace>{qucs_workspace}' *.sch"
            exec_app_in_directory(command, destination_directory)
        else:
            logging.error(f"{program_name} is not installed.")
            exit(1)
                
    # Compiling Verilog-A models
    print("\nCompiling Verilog-A models ...")
    destination_directory = pdk_root + "/ihp-sg13g2/libs.tech/ngspice/osdi"
    
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    
    program_name = "openvaf"
    if is_program_installed(program_name):
        source_directory = pdk_root + "/ihp-sg13g2/libs.tech/verilog-a/psp103"
        command = "openvaf psp103_nqs.va --output " + destination_directory + "/psp103_nqs.osdi"    
        print(f"{program_name} is available and about to run the command '{command}' in a location: {source_directory} ")	
        exec_app_in_directory(command, source_directory)
        source_directory = pdk_root + "/ihp-sg13g2/libs.tech/verilog-a/r3_cmc"
        command = "openvaf r3_cmc.va --output " + destination_directory + "/r3_cmc.osdi"    
        print(f"{program_name} is available and about to run the command '{command}' in a location: {source_directory} ")	
        exec_app_in_directory(command, source_directory)
        source_directory = pdk_root + "/ihp-sg13g2/libs.tech/verilog-a/mosvar"
        command = "openvaf mosvar.va --output " + destination_directory + "/mosvar.osdi"    
        print(f"{program_name} is available and about to run the command '{command}' in a location: {source_directory} ")	
        exec_app_in_directory(command, source_directory)
    else:
        logging.error(f"{program_name} is not installed.")
        exit(1)
                
                
                
                
                
                
