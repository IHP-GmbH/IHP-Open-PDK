# Monte Carlo data processing script
import os
import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
# Replace 'your_file.csv' with the path to your CSV file

if len(sys.argv) != 0:
    arg = sys.argv[1]
    print(f"The CSV file to read is: '{arg}' ")
else:
    print("No argument specified")

file_path = arg
file_path_ref = sys.argv[2]
# Import CSV into a Pandas DataFrame with variable spaces as separator
if os.path.exists(file_path):
    print(f"Reading file '{file_path}'")
    df = pd.read_csv(file_path, sep='\s+')
else:
    print(f"file '{file_path}' does not exists")
# Select and keep only the first column
df = df.astype(float)

Inlv = df.iloc[:, 1]
Inhv = df.iloc[:, 3]
Iplv = df.iloc[:, 5]
Iphv = df.iloc[:, 7]

temp = df.iloc[:, 0]

#print(f"N df={(temp)} ")

if os.path.exists(file_path_ref):
    print(f"Reading file '{file_path}'")
    dfref = pd.read_csv(file_path_ref, sep=',')
else:
    print(f"file '{file_path_ref}' does not exists")
# Select and keep only the first column
Inlv_ref = dfref.iloc[:, 1]
Inhv_ref = dfref.iloc[:, 3]
Iplv_ref = dfref.iloc[:, 5]
Iphv_ref = dfref.iloc[:, 7]


diffnlv = (Inlv-Inlv_ref)/Inlv_ref*100
diffnhv = (Inhv-Inhv_ref)/Inhv_ref*100
diffplv = (Iplv-Iplv_ref)/Iplv_ref*100
diffphv = (Iphv-Iphv_ref)/Iphv_ref*100


# plotting
fig, axs = plt.subplots(2, 2)
axs[0,0].plot(temp.values, diffnlv.values)
axs[0,1].plot(temp.values, diffnhv.values)
axs[1,0].plot(temp.values, diffplv.values)
axs[1,1].plot(temp.values, diffphv.values)
axs[0,0].set_title("NMOS LV")
axs[0,1].set_title("NMOS HV")
axs[1,0].set_title("PMOS LV")
axs[1,1].set_title("PMOS HV")
axs[0,0].set_ylabel("relative diff %")
axs[1,0].set_ylabel("relative diff %")
axs[1,0].set_xlabel("temperature")
axs[1,1].set_xlabel("temperature")

# Show the plot
fig_file_name='./' + 'spectre_ngspice_temp_diff' + '.png'
print(fig_file_name)
plt.savefig(fig_file_name,dpi=600)
plt.show()
