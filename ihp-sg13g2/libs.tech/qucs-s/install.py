#!/usr/bin/env python3

########################################################################
#
# Copyright 2024-2026 IHP PDK Authors
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
import argparse

def exec_app_in_directory(cmd, directory):
    try:
        subprocess.run(cmd, cwd=directory, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command in directory {directory}: {e}")

def is_program_installed(program):
    try:
        subprocess.run(
            [program, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
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

def create_symlinks(source_dir, destination_dir):
    """
    Creates symbolic links for all files in source_dir inside destination_dir.
    """
    # Ensure both directories exist
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate over files in the source directory
    for file_name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, file_name)
        dest_path = os.path.join(destination_dir, file_name)

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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Install Qucs-S PDK files")
    parser.add_argument(
        "--no-model-compile",
        action="store_true",
        help="Skip Verilog-A model compilation step",
    )
    parser.add_argument(
        "--no-qucs-check",
        action="store_true",
        help="Skip check if qucs-s binary exists",
    )
    workspace_group = parser.add_mutually_exclusive_group()
    workspace_group.add_argument(
        "--no-qucs-workspace",
        action="store_true",
        help="Skip QucsWorkspace directory setup, only setup .qucs",
    )
    workspace_group.add_argument(
        "--no-qucs-dir",
        action="store_true",
        help="Skip .qucs directory setup, only setup QucsWorkspace",
    )
    args = parser.parse_args()

    # Example usage:
    info()

    # Check if 'Qucs-S' tool is available
    if not args.no_qucs_check:
        PROGRAM_NAME = "qucs-s"
        if not is_program_installed(PROGRAM_NAME):
            logging.error("%s is not installed.", PROGRAM_NAME)
            exit(1)

    # Check if PDK_ROOT env variable exists
    pdk_root = os.environ.get("PDK_ROOT")
    if pdk_root is None:
        logging.error("Setup PDK_ROOT environment variable to IHP-Open-PDK location")
        exit(1)

    userhome = os.environ.get("HOME")

    # Supporting two variants of Qucs-S default workspace
    workspaces = ["/.qucs/", "/QucsWorkspace/"]
    if args.no_qucs_workspace:
        workspaces = ["/.qucs/"]
    if args.no_qucs_dir:
        workspaces = ["/QucsWorkspace/"]

    for qucs_workspace in workspaces:

        print(f"Preparing $HOME{qucs_workspace} directory ...")
        print("#############################################\n")
        source_directory = pdk_root + "/ihp-sg13g2/libs.tech/qucs-s/user_lib"
        # Check if the source directory exists
        if not os.path.exists(source_directory):
            logging.error("Source directory '%s' does not exist.", source_directory)
            exit(1)

        destination_directory = userhome + qucs_workspace + "user_lib"

        # Check if the destination directory exists, if not, create it
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
            print(f"Destination directory '{destination_directory}' created.")

        create_symlinks(source_directory, destination_directory)

        # Copy examples to "Qucs Home" (<userhome>/[.qucs|QucsWorkspace]/)
        print("Copying examples into Qucs-S Home...")
        source_directory = pdk_root + "/ihp-sg13g2/libs.tech/qucs-s/examples"
        destination_directory = (
            userhome + qucs_workspace + "IHP-Open-PDK-SG13G2-Examples_prj"
        )

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        copy_files(source_directory, destination_directory)

        print("Examples copied")
        print("\n\n#############################################")
        print("              IMPORTANT NOTE")
        print("#############################################\n")
        print(
            "Before using the PDK example schematics, you must add the PDK library path to the Qucs-S search path list.\n"
        )
        print(
            "Please read the instructions provided in "
            + destination_directory
            + "/README.md\n"
        )
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
                print(f"Symbolic link '{symbolic_link}' created successfully.\n")
            except OSError as e:
                print(f"Failed to create symbolic link: {e}")

        # Post-processing example schematics
        PROGRAM_NAME = "sed"
        if is_program_installed(PROGRAM_NAME):
            COMMAND = f"sed -i 's/<qucs_workspace>{qucs_workspace}' *.sch"
            exec_app_in_directory(COMMAND, destination_directory)
        else:
            logging.error("%s is not installed.", PROGRAM_NAME)
            exit(1)

    # Compiling Verilog-A models
    if args.no_model_compile:
        print("Skipping Verilog-A model compilation (--no-model-compile specified)")
    else:
        print("Compiling Verilog-A models ...")
        destination_directory = pdk_root + "/ihp-sg13g2/libs.tech/ngspice/osdi"

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        PROGRAM_NAME = "openvaf"
        if is_program_installed(PROGRAM_NAME):
            source_directory = pdk_root + "/ihp-sg13g2/libs.tech/verilog-a/psp103"
            command = (
                "openvaf psp103_nqs.va --output "
                + destination_directory
                + "/psp103_nqs.osdi"
            )
            print(
                f"{PROGRAM_NAME} is available and about to run the command '{command}' in a location: {source_directory} "
            )
            exec_app_in_directory(command, source_directory)
            command = (
                "openvaf psp103.va --output " + destination_directory + "/psp103.osdi"
            )
            print(
                f"{PROGRAM_NAME} is available and about to run the command '{command}' in a location: {source_directory} "
            )
            exec_app_in_directory(command, source_directory)
            source_directory = pdk_root + "/ihp-sg13g2/libs.tech/verilog-a/r3_cmc"
            command = (
                "openvaf r3_cmc.va --output " + destination_directory + "/r3_cmc.osdi"
            )
            print(
                f"{PROGRAM_NAME} is available and about to run the command '{command}' in a location: {source_directory} "
            )
            exec_app_in_directory(command, source_directory)
            source_directory = pdk_root + "/ihp-sg13g2/libs.tech/verilog-a/mosvar"
            command = (
                "openvaf mosvar.va --output " + destination_directory + "/mosvar.osdi"
            )
            print(
                f"{PROGRAM_NAME} is available and about to run the command '{command}' in a location: {source_directory} "
            )
            exec_app_in_directory(command, source_directory)
        else:
            logging.error("%s is not installed.", PROGRAM_NAME)
            exit(1)
