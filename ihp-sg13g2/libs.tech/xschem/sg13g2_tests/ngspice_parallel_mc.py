import os
import itertools
import subprocess
from multiprocessing import Pool
import re
import csv
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import math

#begin/end tags
results_begin_tag = "results_save_begin"
results_end_tag = "results_save_end"
plot_begin_tag = "**results_plot_begin"
plot_end_tag = "**results_plot_end"

simulations_dir = "./simulations"
results_dir = os.path.join(simulations_dir, "results")

if len(sys.argv) < 2:
    print("Error: Incorrect number of arguments.")
    print("Usage: python3 " + sys.argv[0] + " <netlist_name>")
    print("Example: python3 " + sys.argv[0] + " inv_tb.sch")
    sys.exit(1)

#get netlist 
netlist_name, _ = os.path.splitext(sys.argv[1])
netlist_path_name = os.path.join(simulations_dir, netlist_name + ".spice")
final_result_file = os.path.join(results_dir, netlist_name + "_mc_results.csv")
if not os.path.exists(netlist_path_name):
    print("Error: Netlist file " + netlist_path_name + " not found.")
    sys.exit(1)
with open(netlist_path_name, "r") as f:
    netlist = f.read()

os.makedirs(results_dir, exist_ok=True)
if os.path.exists(final_result_file):
    os.remove(final_result_file)

#get nr_workers from netlist
match = re.search(r"^\s*(\*\*nr_workers)\s*=\s*(.+)$", netlist, re.MULTILINE)
if match:
    nr_workers = int(match.group(2).strip())
else:
    print("Info: **nr_workers statement not found, setting it to 10.")
    nr_workers = 10

#get nr_mc_sims from netlist
match = re.search(r"^\s*(\*\*nr_mc_sims)\s*=\s*(.+)$", netlist, re.MULTILINE)
if match:
    nr_mc_sims = int(match.group(2).strip())
else:
    print("Info: **nr_mc_sims statement not found, setting it 100.")
    nr_mc_sims = 100

#get plot parameters from netlist
pattern = re.compile(
    rf"{re.escape(plot_begin_tag)}(.*?){re.escape(plot_end_tag)}",
    re.DOTALL
)
match = pattern.search(netlist)
results_plot_list = []
if match:
    block = match.group(1)
    for line in block.strip().splitlines():
        results_plot_list.append(line[2:].strip())
else:
    print("Info: No results plot parameter settings found.")

#generate list of mc_sims
mc_sims_list = list(range(nr_mc_sims))
#split lst in n parts
def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

#workers
def run_worker(args):
    sim_list, worker_id = args
    result_file = os.path.join(results_dir, f"{netlist_name}_worker_{worker_id}_results.txt")
    writeHeadings = True
    with open(result_file, "w") as results:
        writer = csv.writer(results, delimiter=";")
        for sim_nr in sim_list:
            try:
                output = subprocess.check_output(["ngspice", "-b", netlist_path_name],
                                                 stderr=subprocess.STDOUT, text=True)
                #extract results between results_begin_tag and results_end_tag
                pattern = re.compile(
                    rf"{re.escape(results_begin_tag)}(.*?){re.escape(results_end_tag)}",
                    re.DOTALL
                )
                match = pattern.search(output)
                if match:
                    block = match.group(1)
                    # extract variable name and value
                    result = {}
                    for line in block.strip().splitlines():
                        if '=' in line:
                            result_name, result_value = line.split('=')
                            result[result_name.strip()] = float(result_value.strip())
                    # write in csv file
                    if writeHeadings:
                        writer.writerow(list(result.keys()))
                        writeHeadings = False
                    writer.writerow(list(result.values()))
                else:
                    writer.writerow(['N/A', 'ERROR in receiving results'])
            except subprocess.CalledProcessError:
                if writeHeadings:
                    writer.writerow(['N/A', 'ERROR'])
                writer.writerow(['N/A', 'ERROR in process handling'])

if __name__ == "__main__":
    start_time = time.time()
   
    chunks = chunkify(mc_sims_list, nr_workers)
    worker_inputs = [(chunk, i) for i, chunk in enumerate(chunks) if chunk]
    with Pool(nr_workers) as pool:
        pool.map(run_worker, worker_inputs)

    # merge results of workers into a single file
    with open(final_result_file, "w") as out:
        for i in range(nr_workers):
            part_file = os.path.join(results_dir, f"{netlist_name}_worker_{i}_results.txt")
            if os.path.exists(part_file):
                with open(part_file, "r") as part:
                    lines = part.readlines()
                    if i == 0:
                        out.writelines([line for line in lines if "ERROR" not in line])
                    else: # skip the header
                        out.writelines([line for line in lines[1:] if "ERROR" not in line])
                os.remove(part_file)

    # plot results
    if len(results_plot_list) > 0:
        # make dictionary with results
        results_dict = {}
        with open(final_result_file, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
    
            # Initialize dictionary with keys from the header
            for header in reader.fieldnames:
                results_dict[header] = []

            # Fill the dictionary
            for row in reader:
                for header in reader.fieldnames:
                    results_dict[header].append(float(row[header]))
            # Set the number of columns for subplot grid
            n_cols = 2  # Change this to 1, 2, 3, etc.
            n_plots = len(results_plot_list)
            n_rows = math.ceil(n_plots / n_cols)

            # Create subplots
            fig, axs = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 4 * n_rows))
            axs = axs.flatten()  # Flatten in case of multiple rows/columns
            i = 0
            for var in results_plot_list:
                data = np.array(results_dict[var.lower()])
                mean = data.mean()
                std = data.std()
                axs[i].hist(data, bins=50, color='skyblue', edgecolor='black')
                axs[i].set_title(f"Histogram of {var}")
                axs[i].set_xlabel(f"{var}")
                axs[i].set_ylabel("Count")
                ymax = axs[i].get_ylim()[1]

                # Plot mean line (solid green)
                axs[i].axvline(mean, color='green', linestyle='-', linewidth=2)
                axs[i].text(mean, ymax * 0.95, 'Mean', color='green', rotation=90,
                            verticalalignment='top', horizontalalignment='center')

                # Plot sigma lines (dashed red)
                for sigma_mult in [1, 2, 3]:
                    pos = mean + sigma_mult * std
                    neg = mean - sigma_mult * std

                    axs[i].axvline(pos, color='red', linestyle='--', linewidth=1)
                    axs[i].axvline(neg, color='red', linestyle='--', linewidth=1)

                    # Labels for sigma lines with a slight vertical offset to avoid overlap
                    y_pos = ymax * (1 - 0.1 * sigma_mult)

                    axs[i].text(pos, y_pos, f'+{sigma_mult}σ', color='red', rotation=90,
                                verticalalignment='top', horizontalalignment='right')
                    axs[i].text(neg, y_pos, f'-{sigma_mult}σ', color='red', rotation=90,
                                verticalalignment='top', horizontalalignment='left')

                # Set more x-axis ticks for better readability
                x_min = mean - 4 * std
                x_max = mean + 4 * std
                ticks = np.arange(x_min, x_max + std/2, std/2)
                axs[i].set_xticks(ticks)
                i = i + 1

            # Hide unused subplots
            for j in range(i, len(axs)):
                axs[j].axis('off')
            plt.tight_layout()
            plt.show()
        
    end_time = time.time()
    runtime = end_time - start_time
    hours = int(runtime // 3600)
    minutes = int((runtime % 3600) // 60)
    seconds = int(runtime % 60)
    print(f"Runtime: {hours:02}:{minutes:02}:{seconds:02}")
