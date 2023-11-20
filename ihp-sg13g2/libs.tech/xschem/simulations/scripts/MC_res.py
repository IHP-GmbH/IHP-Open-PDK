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
# Select and keep only the first column

if os.path.exists(file_path):
    print(f"Reading file '{file_path}'")
    df = pd.read_csv(file_path, sep='\s+')
else:
    print(f"file '{file_path}' does not exists")
# Select and keep only the first column
# Plot the first column

rsil = df.iloc[:,1]
rppd = df.iloc[:,3]
rhigh = df.iloc[:,5]


no_bins = 200

# plotting
fig, axs = plt.subplots(1, 3)
axs[0].hist(rsil,  bins=no_bins)
axs[1].hist(rppd,  bins=no_bins)
axs[2].hist(rhigh, bins=no_bins)
axs[0].set_title("Rsil")
axs[1].set_title("Rppd")
axs[2].set_title("Rhigh")
axs[0].set_ylabel("counts")
axs[0].set_xlabel("value")
axs[1].set_xlabel("value")
axs[2].set_xlabel("value")


print("---------------------------------------" )
print(f"Mean value rsil: {rsil.mean()}" )
print(f"Std dev rsil:  {rsil.std()}" )
print("---------------------------------------" )
print(f"Mean value rppd: {rppd.mean()}" )
print(f"Std dev rppd:  {rppd.std()}" )
print("---------------------------------------" )
print(f"Mean value rhigh: {rhigh.mean()}" )
print(f"Std dev rhigh:  {rhigh.std()}" )
print("---------------------------------------" )

# Show the plot
basename = os.path.basename(file_path)
fig_file_name='../fig/' + basename + '.png'
print(fig_file_name)
plt.savefig(fig_file_name,dpi=600)
plt.show()
