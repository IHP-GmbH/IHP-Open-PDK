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
    - compiles and places Verilog-A models in ../ngspice/osdi location. 
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
        source_directory=pdk_root + "/ihp-sg13g2/libs.tech/verilog-a"

    username = os.environ.get("USER")
    destination_directory = pdk_root + "/ihp-sg13g2/libs.tech/ngspice/osdi"
    
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")
    
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Find and set VerilogA compiler
    if is_program_installed("openvaf-r"):
        # Use OpenVAF-Reloaded
        compiler = "openvaf-r"
    elif is_program_installed("openvaf"):
        # Use OpenVAF
        compiler = "openvaf"
    else:
        compiler = None
        print("VerilogA compiler not found - install 'openvaf-r' or 'openvaf' to generate the necessary models")

    # Compile VerilogA models
    if compiler is not None:
        # Map modelfile to source directory:
        modelfile_map = {
            "psp103": "psp103",
            "psp103_nqs": "psp103",
            "r3_cmc": "r3_cmc",
            "mosvar": "mosvar"
        }
        num_models = len(modelfile_map)

        # Print header
        log_width = 70
        header = f"Compiling VerilogA models using: '{compiler}'"
        print(f"\n{'=' * log_width}")
        print(f"{header:^{log_width}}")
        print(f"{'=' * log_width}\n")

        for idx, (modelfile, model_dir) in enumerate(modelfile_map.items()):
            model_src_dir = f"{source_directory}/{model_dir}"
            command = f"{compiler} {modelfile}.va --output {destination_directory}/{modelfile}.osdi"

            # Output formatting
            print(f"\n[{idx+1}/{num_models}] Compiling {modelfile}.va...")
            print(f"  Command:           '{command}'")
            print(f"  Working directory: '{model_src_dir}'")
            print("-" * log_width)

            # Run the compiler
            exec_app_in_directory(command, model_src_dir)

            print("-" * log_width)

        # Print footer
        footer = "VerilogA compilation done"
        print(f"\n{'=' * log_width}")
        print(f"{footer:^{log_width}}")
        print(f"{'=' * log_width}\n")

    original_file =  pdk_root + "/ihp-sg13g2/libs.tech/ngspice/.spiceinit"
    symbolic_link = "/home/" + username + "/.spiceinit"
    # Create the symbolic link
    if not os.path.exists(symbolic_link):
        try:
            os.symlink(original_file, symbolic_link)
            print(f"Symbolic link '{symbolic_link}' created successfully.")
        except OSError as e:
            print(f"Failed to create symbolic link: {e}")


 	


