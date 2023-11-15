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
# Import CSV into a Pandas DataFrame with variable spaces as separator
if os.path.exists(file_path):
    print(f"Reading file '{file_path}'")
    df = pd.read_csv(file_path, sep='\s+')
else:
    print(f"file '{file_path}' does not exists")
# Select and keep only the first column
df = df.astype(float)

freq = df.iloc[:, 0]
s21_re = df.iloc[:, 1]
s21_im = df.iloc[:, 2]


#print(f"N df={(temp)} ")

# plotting
fig, axs = plt.subplots(2, 1)
axs[0].semilogx(freq.values, s21_re.values)
axs[1].semilogx(freq.values, s21_im.values)
#axs[0].set_title("NMOS LV")
#axs[1].set_title("NMOS HV")
#axs[0].set_title("PMOS LV")
#axs[1].set_title("PMOS HV")
#axs[0,0].set_ylabel("relative diff %")
#axs[1,0].set_ylabel("relative diff %")
#axs[1,0].set_xlabel("temperature")
#axs[1,1].set_xlabel("temperature")

# Show the plot
fig_file_name='./' + 'cap_s21' + '.png'
print(fig_file_name)
plt.savefig(fig_file_name,dpi=600)
plt.show()
