import os
import itertools
import subprocess
from multiprocessing import Pool
import re
import csv
import numpy as np
import time
from quantiphy import Quantity
import sys
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math
import pandas as pd

#begin/end tags
parameter_begin_tag = "**parameter_sweep_begin"
parameter_end_tag = "**parameter_sweep_end"
results_begin_tag = "results_sweep_begin"
results_end_tag = "results_sweep_end"
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
final_result_file = os.path.join(results_dir, netlist_name + "_sweep_results.csv")
final_result_file_sorted = os.path.join(results_dir, netlist_name + "_sweep_results_sorted.csv")
if not os.path.exists(netlist_path_name):
    print("Error: Netlist file " + netlist_path_name + " not found.")
    sys.exit(1)
with open(netlist_path_name, "r") as f:
    netlist = f.read()

os.makedirs(results_dir, exist_ok=True)
if os.path.exists(final_result_file):
    os.remove(final_result_file)
if os.path.exists(final_result_file_sorted):
    os.remove(final_result_file_sorted)

#get nr_workers from netlist
match = re.search(r"^[ \t]*\*\*nr_workers[ \t]*=[ \t]*(\d+)[ \t]*$", netlist, re.MULTILINE)
if match:
    nr_workers = int(match.group(1).strip())
else:
    print("Info: **nr_workers statement not found or erroneous, setting it to 10.")
    nr_workers = 10

#get sort_results_index from netlist
match = re.search(r"^[ \t]*\*\*sort_results_index[ \t]*=[ \t]*(\d+)[ \t]*$", netlist, re.MULTILINE)
if match:
    sort_results_index = int(match.group(1).strip())
else:
    print("Info: **sort_results_index statement not found or erroneous, setting it to index 0.")
    sort_results_index = 0

#get results_plot_contour_index from netlist
match = re.search(r"^[ \t]*\*\*results_plot_contour_index[ \t]*=[ \t]*(\d+(?:,[ \t]*\d+)*)[ \t]*$", netlist, re.MULTILINE)
if match:
    results_plot_contour_index_str = match.group(1).strip()
    results_plot_contour_index = [int(i.strip()) for i in results_plot_contour_index_str.split(',') if i.strip().isdigit()]
else:
    print("Info: **results_plot_contour_index statement not found or erroneous, setting it to be empty.")
    results_plot_contour_index = []

#get results_plot_logx_index from netlist
match = re.search(r"^[ \t]*\*\*results_plot_logx_index[ \t]*=[ \t]*(\d+(?:,[ \t]*\d+)*)[ \t]*$", netlist, re.MULTILINE)
if match:
    results_plot_logx_index_str = match.group(1).strip()
    results_plot_logx_index = [int(i.strip()) for i in results_plot_logx_index_str.split(',') if i.strip().isdigit()]
else:
    print("Info: **results_plot_logx_index statement not found or erroneous, setting it to be empty.")
    results_plot_logx_index = []

#get results_plot_logy_index from netlist
match = re.search(r"^[ \t]*\*\*results_plot_logy_index[ \t]*=[ \t]*(\d+(?:,[ \t]*\d+)*)[ \t]*$", netlist, re.MULTILINE)
if match:
    results_plot_logy_index_str = match.group(1).strip()
    results_plot_logy_index = [int(i.strip()) for i in results_plot_logy_index_str.split(',') if i.strip().isdigit()]
else:
    print("Info: **results_plot_logy_index statement not found or erroneous, setting it to be empty.")
    results_plot_logy_index = []

#get sweep parameters from netlist
pattern = re.compile(
    rf"{re.escape(parameter_begin_tag)}(.*?){re.escape(parameter_end_tag)}",
    re.DOTALL
)
match = pattern.search(netlist)
if match:
    block = match.group(1)
    # extract parameter name and value
    param_list = {}
    for line in block.strip().splitlines():
        if '=' in line:
            var_name, var_val = line.split('=')
            var_name = var_name[2:].strip()
            var_val = var_val.strip()
        else:
            print("Error: Incorrect parameter settings format.")
            sys.exit(1)
        values_splited = var_val.split(':')
        if len(values_splited) != 4:
            print("Error: Incorrect parameter settings list format.")
            sys.exit(1)
        list_type = values_splited[0].lower()

        if list_type == "auto":
           sweep_list = np.linspace(Quantity(values_splited[1]), Quantity(values_splited[3]), int(values_splited[2]))
        elif list_type == "lin":
            sweep_list = np.arange(Quantity(values_splited[1]), (Quantity(values_splited[3]) + Quantity(values_splited[2])*0.1), Quantity(values_splited[2]))
        elif list_type == "dec":
            total_points = int(int(values_splited[2]) * (np.log10(Quantity(values_splited[3]))-np.log10(Quantity(values_splited[1])))) + 1
            sweep_list =  np.logspace(np.log10(Quantity(values_splited[1])), np.log10(Quantity(values_splited[3])), total_points)
        elif list_type == "log":
            sweep_list =  np.logspace(np.log10(Quantity(values_splited[1])), np.log10(Quantity(values_splited[3])), int(values_splited[2]))
        else:
            print("Error: Incorrect parameter settings list format.")
        param_list[var_name] = sweep_list.astype(str)
else:
    print("Error: No sweep parameter settings found.")
    sys.exit(1)
    
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

#generate all combinations of params
param_value_combinations = list(itertools.product(*param_list.values()))
param_name_list = list(param_list.keys())
#split lst in n parts
def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

#workers
def run_worker(args):
    sim_list, worker_id = args
    cir_file = os.path.join(simulations_dir, f"{netlist_name}_worker_{worker_id}.cir")
    result_file = os.path.join(results_dir, f"{netlist_name}_worker_{worker_id}_results.txt")
    writeHeadings = True
    with open(result_file, "w") as results:
        writer = csv.writer(results, delimiter=";")
        for param_set in sim_list:
            param_name_index = 0
            content = netlist
            for param_val in param_set:
                content = content.replace("{" + param_name_list[param_name_index] + "}", param_val)
                param_name_index = param_name_index + 1
            with open(cir_file, "w") as f:
                f.write(content)
            try:
                output = subprocess.check_output(["ngspice", "-b", cir_file],
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
                        writer.writerow(param_name_list + list(result.keys()))
                        writeHeadings = False
                    writer.writerow([str(x) for x in param_set] + list(result.values()))
                else:
                    if writeHeadings:
                        writer.writerow(param_name_list)
                        writeHeadings = False
                    writer.writerow([",".join(str(x) for x in param_set), 'N/A', 'ERROR in receiving results'])
            except subprocess.CalledProcessError:
                if writeHeadings:
                    writer.writerow(param_name_list)
                    writeHeadings = False
                writer.writerow([",".join(str(x) for x in param_set), 'N/A', 'ERROR in process handling'])
            os.remove(cir_file)

if __name__ == "__main__":
    start_time = time.time()
   
    chunks = chunkify(param_value_combinations, nr_workers)
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
                    error_lines = [line for line in lines[1:] if "ERROR" in line]
                    if error_lines:
                        print(f"Errors found in worker {i} results:")
                        print("".join(error_lines))
                os.remove(part_file)

    df = pd.read_csv(final_result_file, delimiter=';')
    df_sorted = df.sort_values(by=df.columns[sort_results_index], ascending=True)
    df_sorted.to_csv(final_result_file_sorted, sep=';', index=False)

    # plot results
    if len(results_plot_list) > 0:
        df_sorted = df.sort_values(by=param_name_list)

        # Set the number of columns for subplot grid
        n_cols = 2  # Change this to 1, 2, 3, etc.
        n_plots = len(results_plot_list)
        n_rows = math.ceil(n_plots / n_cols)

        # Create subplots
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 4 * n_rows))
        axs = axs.flatten()  # Flatten in case of multiple rows/columns
        i = 0
        if len(param_name_list) == 1:
            for var in results_plot_list:
                actual_size = len(df_sorted[var])
                expected_size = len(next(iter(param_list.values())))
                if actual_size != expected_size:
                    print(f"Error with variable {var}: Expected {expected_size} data points but got {actual_size}.")
                    print(f"Hint: This could be due to missing or failed simulations.")
                axs[i].set_title(var)
                axs[i].grid(True, which='both', linestyle='--', linewidth=0.5)
                axs[i].minorticks_on()
                axs[i].set_xlabel(f"{param_name_list[0]}")
                axs[i].set_ylabel(f"{var}")
                var = var.lower()
                if i in results_plot_logx_index and i in results_plot_logy_index:
                    axs[i].loglog(df_sorted[param_name_list[0]], df_sorted[var])
                elif i in results_plot_logx_index:
                    axs[i].semilogx(df_sorted[param_name_list[0]], df_sorted[var])
                elif i in results_plot_logy_index:
                    axs[i].semilogy(df_sorted[param_name_list[0]], df_sorted[var])
                else:
                    axs[i].plot(df_sorted[param_name_list[0]], df_sorted[var])
                i = i + 1
            # Hide unused subplots
            for j in range(i, len(axs)):
                axs[j].axis('off')
            plt.tight_layout()
            plt.show()
        elif len(param_name_list) == 2:
            for var in results_plot_list:
                axs[i].set_title(var)
                axs[i].set_xlabel(f"{param_name_list[0]}")              
                axs[i].grid(True, which='both', linestyle='--', alpha=0.5)
                axs[i].minorticks_on()
                x_raw = np.array(df_sorted[param_name_list[0]])
                y_raw = np.array(df_sorted[param_name_list[1]])
                z_raw = np.array(df_sorted[var.lower()])
                x = np.unique(x_raw)
                y = np.unique(y_raw)
                expected_size = len(x) * len(y)
                if z_raw.size != expected_size:
                    print(f"Error with variable {var}: Expected {expected_size} data points but got {z_raw.size}.")
                    print(f"Hint: This could be due to missing or failed simulations. Interpolating misssing points!")
                    Z = np.full((len(x), len(y)), np.nan)
                    for yi_index, yi in enumerate(y):
                        mask = (y_raw == yi)
                        xi_vals = x_raw[mask]
                        zi_vals = z_raw[mask]
                        if len(xi_vals) < 2:
                            print(f"Skipping interpolation at y={yi:.3g}: Not enough points.")
                            continue
                        try:
                            interp_fn = interp1d(xi_vals, zi_vals, kind='linear', bounds_error=False, fill_value=np.nan)
                            zi_interp = interp_fn(x)
                        except Exception as e:
                            print(f"Interpolation failed at y={yi:.3g}: {e}")
                            zi_interp = np.full_like(x, np.nan)
                        Z[:, yi_index] = zi_interp
                else:
                    Z = z_raw.reshape(len(x), len(y))
                Z_plot = Z.T  # shape (len(y), len(x))
                if i in results_plot_contour_index:
                    axs[i].set_ylabel(f"{param_name_list[1]}")
                    X, Y = np.meshgrid(x,y)
                    contour = axs[i].contourf(X, Y, Z_plot, levels=10, cmap='viridis')
                    cbar = fig.colorbar(contour, ax=axs[i])
                    cbar.set_label(var)
                else:
                    axs[i].set_ylabel(var)
                    if i in results_plot_logx_index and i in results_plot_logy_index:
                        for l, yl in enumerate(y):
                            axs[i].loglog(x, Z[:, l], label=f"{yl:.2g}")
                    elif i in results_plot_logx_index:
                        for l, yl in enumerate(y):
                            axs[i].semilogx(x, Z[:, l], label=f"{yl:.2g}")
                    elif i in results_plot_logy_index:
                        for l, yl in enumerate(y):
                            axs[i].semilogy(x, Z[:, l], label=f"{yl:.2g}")
                    else:
                        for l, yl in enumerate(y):
                            axs[i].plot(x, Z[:, l], label=f"{yl:.2g}")
                    axs[i].legend(title=param_name_list[1], loc='upper right')
                i = i + 1
            # Hide unused subplots
            for j in range(i, len(axs)):
                axs[j].axis('off')
            plt.tight_layout()
            plt.show()
        else:
            print("Warning: Plot not possible due to more than 2 parameter sweeps.")
        
    end_time = time.time()
    runtime = end_time - start_time
    hours = int(runtime // 3600)
    minutes = int((runtime % 3600) // 60)
    seconds = int(runtime % 60)
    print(f"Runtime: {hours:02}:{minutes:02}:{seconds:02}")
