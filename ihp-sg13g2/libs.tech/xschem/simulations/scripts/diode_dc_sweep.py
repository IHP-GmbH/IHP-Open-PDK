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

V1 = df.iloc[:, 0]
Ida_ng = df.iloc[:, 1]*10e+6
Idp_ng = df.iloc[:, 3]*10e+6


#print(f"N df={(temp)} ")

if os.path.exists(file_path_ref):
    print(f"Reading file '{file_path}'")
    dfref = pd.read_csv(file_path_ref, sep=',')
else:
    print(f"file '{file_path_ref}' does not exists")
# Select and keep only the first column
Ida_xy = dfref.iloc[:, 1]*10e+6
Idp_xy = dfref.iloc[:, 3]*10e+6


diffIda = (Ida_ng-Ida_xy)
diffIdp = (Idp_ng-Idp_xy)


# plotting
fig, axs = plt.subplots(3, 1)
axs[0].plot(V1.values, diffIda.values)
axs[1].plot(V1.values, diffIdp.values)
axs[2].plot(V1.values, Ida_ng.values, V1.values, Idp_ng.values, V1.values, Ida_xy.values, V1.values, Idp_xy.values)
axs[0].set_title("Dantenna difference")
axs[1].set_title("Dpantenna difference")
axs[2].set_title("Diode currents")
axs[0].set_ylabel("I [uA]")
axs[1].set_ylabel("I [uA]")
axs[2].set_ylabel("I [uA]")
axs[2].set_xlabel("Voltage [V]")
axs[2].legend(['Ida_ng', 'Idp_ng', 'Ida_xyce', 'Idp_xyce'])
# Show the 
basename = os.path.basename(file_path)
fig_file_name='../fig/' + basename + '.png'
print(fig_file_name)
plt.savefig(fig_file_name,dpi=600)
plt.show()
