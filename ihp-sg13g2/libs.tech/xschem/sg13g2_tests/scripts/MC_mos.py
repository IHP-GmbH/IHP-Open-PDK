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

Vgs = df.iloc[:,1]


print(f"Mean value of Vgs: {Vgs.mean()}" )
print(f"Std dev of Vgs:  {Vgs.std()}" )

plt.hist(Vgs, bins=50)
plt.title('Monte Carlo simulation of the $V_{GS}$ voltage of sg13 mosfet')  # Replace with your X-axis label
plt.ylabel('Counts')  # Replace with your Y-axis label
plt.xlabel('$V_{GS}$ voltage [V]')  # Replace with your plot title
# Show the plot
basename = os.path.basename(file_path)
fig_file_name='../fig/' + basename + '.png'
print(fig_file_name)
plt.savefig(fig_file_name,dpi=600)
plt.show()
