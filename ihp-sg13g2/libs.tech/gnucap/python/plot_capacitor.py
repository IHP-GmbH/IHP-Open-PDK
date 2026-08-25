from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dirs import tests_dir_gc, tests_dir_sp, fig_dir

cap_fig_dir = fig_dir / "capacitor"
cap_fig_dir.mkdir(parents=True, exist_ok=True)

ref_dir_gc = tests_dir_gc / "capacitor" / "ref"
assert ref_dir_gc.exists()

ref_dir_sp = tests_dir_sp / "capacitor" / "ref"
assert ref_dir_gc.exists()

# Find cutoff frequency where |H| = 0.707 (or closest to it)
# For high-pass filter: magnitude rises from low to high
# Cutoff is where it crosses 0.707 from below
cutoff_level = 0.707

mc_trials = 1000 # number of mc trials
num_ac_samples = 1001 # number of frequency samples in each mc trial

def calculate_cap_from_f_cutoff(freq, H):

    # Find index where magnitude crosses 0.707
    idx_below = np.where(H < cutoff_level)[0]
    idx_above = np.where(H >= cutoff_level)[0]

    if len(idx_below) > 0 and len(idx_above) > 0:
        # Use linear interpolation to approx cutoff frequency
        i1 = idx_below[-1]
        i2 = idx_above[0]
        f1, f2 = freq[i1], freq[i2]
        h1, h2 = H[i1], H[i2]
        # Interpolate
        f_cutoff = f1 + (f2 - f1) * (cutoff_level - h1) / (h2 - h1)
    else:
        f_cutoff = 1.5*1e6
    # Calculate capacitance from cutoff frequency
    R = 100e3
    C = 1 / (2 * np.pi * R * f_cutoff)
    return f_cutoff, C

def calculate_cap_from_model_equation(corner):

    w, l = 10e-6, 70e-6,
    short, narrow = 0.0, 0.0

    cj_corners = {
        'typ': 1.5E-15 *  1e12,
        'bcs': 0.9 * 1.5E-15 * 1e12,
        'wcs': 1.1 * 1.5E-15 * 1e12}

    cj = cj_corners[corner]
    cjsw = 40E-18 * 1e6

    C = cj * (w - narrow) * (l - short) + cjsw * 2 * (l - short + w - narrow)

    return C

def parse_ac_data_gc(filepath_gc):

    raw = pd.read_csv(
        filepath_gc,
        sep=r"\s*=\s*",
        engine="python",
        names=["name", "value"],
        comment="#",
    )

    raw = raw.dropna()
    raw["value"] = raw["value"].astype(float)

    df = (
        raw.assign(run=raw.groupby("name").cumcount() + 1)
        .pivot(index="run", columns="name", values="value")
        .reset_index()
    )

    df.columns.name = None

    return df

def plot_tb_cap_cutoff(corner, show=False):

    test_name = f'tb_cap_cutoff_{corner}'

    # Load gnucap data
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skiprows=2, skipfooter=4, engine='python').values

    # Load ngspice data
    filepath_ngspice = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_ngspice, sep=r'\s+').values

    assert data_gc.shape == data_sp.shape, f"data_gc.shape {data_gc.shape} unequal data_sp.shape {data_sp.shape}"

    freq_gc = data_gc[:, 0]
    vout1_gc = data_gc[:, 1]
    vout2_gc = data_gc[:, 2]

    freq_sp = data_sp[:, 0]
    vout1_sp = data_sp[:, 1]
    vout2_sp = data_sp[:, 2]
    # Transfer functions
    H_gc_vout1 = vout1_gc
    H_sp_vout1 = vout1_sp
    H_gc_vout2 = vout2_gc
    H_sp_vout2 = vout2_sp
    # Cutoff frequency and capacitance
    f_cutoff_cmim_gc, C_cmim_gc = calculate_cap_from_f_cutoff(freq_gc, H_gc_vout1)
    f_cutoff_cmim_sp, C_cmim_sp = calculate_cap_from_f_cutoff(freq_sp, H_sp_vout1)
    f_cutoff_rfcmim_gc, C_rfcmim_gc = calculate_cap_from_f_cutoff(freq_gc, H_gc_vout2)
    f_cutoff_rfcmim_sp, C_rfcmim_sp = calculate_cap_from_f_cutoff(freq_sp, H_sp_vout2)

    C = calculate_cap_from_model_equation(corner)

    # Plotting
    plt.figure(figsize=(14, 8))
    gs = plt.GridSpec(1, 2)  # Adjusted to create two subplots
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    plt.suptitle(f'Frequency Response ({corner} Corner)', fontsize=16)

    # Plot cap_cmim
    ax1.set_title('cap_cmim')
    ax1.semilogx(freq_gc, H_gc_vout1, '-', color='r', linewidth=2, label='Gnucap |H(f)|')
    ax1.semilogx(freq_sp, H_sp_vout1, '--', color='k', linewidth=1.5, label='Ngspice |H(f)|')

    # Mark cutoff frequency for vout1
    ax1.axhline(y=cutoff_level, color='cyan', linestyle='--', linewidth=1.5, label=f'-3dB level = 0.707')
    ax1.axvline(x=f_cutoff_cmim_gc, color='r', linestyle='-', linewidth=2.0, label=f'Gnucap fcut = {f_cutoff_cmim_gc / 1e6:.3f} MHz')
    ax1.axvline(x=f_cutoff_cmim_sp, color='k', linestyle='--', linewidth=1.5,label=f'Ngspice fcut = {f_cutoff_cmim_sp / 1e6:.3f} MHz')

    # Mark cutoff point for vout1
    ax1.plot(f_cutoff_cmim_gc, cutoff_level, 'ro', markersize=8)

    # Add text box with capacitance results
    textstr = f'Gnucap C: {C_cmim_gc*1e12:.3f} pF\n' + \
              f'Ngspice C: {C_cmim_sp*1e12:.3f} pF\n' + \
              f'Model C: {C*1e12:.3f} pF'

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax1.text(0.125, 0.3, textstr, transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)

    ax1.set_xlabel('Frequency [Hz]', fontsize=14)
    ax1.set_ylabel('|H(f)| = |V_out / V_in|', fontsize=14)
    ax1.grid(True, which='both', alpha=0.3)
    ax1.legend(fontsize=12, loc='best')

    # Plot cap_rfcmim
    ax2.set_title('cap_rfcmim')
    ax2.semilogx(freq_gc, H_gc_vout2, '-', color='r', linewidth=2, label='Gnucap |H(f)|')
    ax2.semilogx(freq_sp, H_sp_vout2, '--', color='k', linewidth=1.5, label='Ngspice |H(f)|')

    # Mark cutoff frequency for vout2
    ax2.axhline(y=cutoff_level, color='cyan', linestyle='--', linewidth=1.5, label=f'-3dB level = 0.707')
    ax2.axvline(x=f_cutoff_rfcmim_gc, color='r', linestyle='-', linewidth=2.0, label=f'Gnucap fcut = {f_cutoff_rfcmim_gc / 1e6:.3f} MHz')
    ax2.axvline(x=f_cutoff_rfcmim_sp, color='k', linestyle='--', linewidth=1.5, label=f'Ngspice fcut = {f_cutoff_rfcmim_sp / 1e6:.3f} MHz')
    # Mark cutoff point for vout2
    ax2.plot(f_cutoff_rfcmim_gc, cutoff_level, 'ro', markersize=8)

    ax2.set_xlabel('Frequency [Hz]', fontsize=14)
    ax2.set_ylabel('|H(f)| = |V_out / V_in|', fontsize=14)

    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend(fontsize=12, loc='best')

    # Add text box with capacitance results
    textstr = f'Gnucap C: {C_rfcmim_gc*1e12:.3f} pF\n' + \
              f'Ngspice C: {C_rfcmim_sp*1e12:.3f} pF\n' + \
              f'Model C: {C*1e12:.3f} pF'

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax2.text(0.125, 0.3, textstr, transform=ax2.transAxes, fontsize=14, verticalalignment='top', bbox=props)

    # Save figure
    plt.tight_layout()
    plt.savefig(cap_fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()

    return

def plot_tb_cap_cutoff_mc_stat(plot_sp = True, show=False):

    test_name = f'tb_cap_cutoff_mc_stat'

    # load gnucap data
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data_gc = parse_ac_data_gc(filepath_gc)
    C1_arr_gc = data_gc["C1"].to_numpy(copy=True)
    C2_arr_gc = data_gc["C2"].to_numpy(copy=True)

    assert np.allclose(C1_arr_gc, C2_arr_gc), "C1_arr_gc and C2_arr_gc because process variation is global "

    # load ngspice data
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values
    C_arr_sp = data_sp[:, 1]

    # to pF
    C_arr_gc = C1_arr_gc * 1e12
    C_arr_sp = C_arr_sp * 1e12

    C = calculate_cap_from_model_equation("typ") * 1e12

    # Compute statistics
    mean_gc = np.mean(C_arr_gc)
    mean_sp = np.mean(C_arr_sp)
    std_gc = np.std(C_arr_gc)
    std_sp = np.std(C_arr_sp)

    ax0 = plt.subplot(111)

    # Plot capatitance histogram and stats

    # Gnucap
    ax0.hist(C_arr_gc, bins=50, alpha=0.5, color = "blue", density=True, label='Gnucap')
    ax0.axvline(mean_gc, color='blue', linestyle='--', linewidth=1, label=f"Gnucap C Mean={mean_gc:.5f}")
    ax0.axvline(mean_gc + std_gc, color='blue', linestyle=':', linewidth=1, label=f"Gnucap C STD={std_gc:.5f}")
    ax0.axvline(mean_gc - std_gc, color='blue', linestyle=':', linewidth=1)
    if plot_sp: # Ngspice
        ax0.hist(C_arr_sp, bins=50, alpha=0.5, color = "orange", density=True, label='Ngspice')
        ax0.axvline(mean_sp, color='orange', linestyle='--', linewidth=1, label=f"Ngspice C Mean={mean_sp:.5f}")
        ax0.axvline(mean_sp + std_sp, color='orange', linestyle=':', linewidth=1, label=f"Ngspice C STD={std_sp:.5f}")
        ax0.axvline(mean_sp - std_sp, color='orange', linestyle=':', linewidth=1)

    # Plot capatitance from model equations
    ax0.axvline(C, color='red', linestyle='--', linewidth=1, label=f"Model C={C:.5f}")

    ax0.set_xlabel('Capacitance (pF)')
    ax0.set_ylabel('Probability Density')
    ax0.legend(fontsize=10)  # Add legend

    plt.suptitle(f'cap_cmim global process variation ', fontsize=14)
    plt.savefig(cap_fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()

def plot_tb_cap_cutoff_mc_mm(corner, plot_sp=True, show=False):

    test_name = f'tb_cap_cutoff_mc_mm_{corner}'

    # Load gnucap data
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data_gc = parse_ac_data_gc(filepath_gc)
    C1_arr_gc = data_gc["C1"].to_numpy(copy=True)
    C2_arr_gc = data_gc["C2"].to_numpy(copy=True)

    # Load ngspice data
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values
    C1_arr_sp = data_sp[:, 1]
    C2_arr_sp = data_sp[:, 2]

    # to pF
    C1_arr_gc *= 1e12
    C1_arr_sp *= 1e12
    C2_arr_gc *= 1e12
    C2_arr_sp *= 1e12

    # Compute statistics
    mean_gc = np.mean(C1_arr_gc)
    mean_sp = np.mean(C1_arr_sp)
    std_gc = np.std(C2_arr_gc)
    std_sp = np.std(C2_arr_sp)

    # Mismatch metric
    mm_gc = 200 * (C1_arr_gc - C2_arr_gc) / (C1_arr_gc + C2_arr_gc)
    mean_mm_gc = np.mean(mm_gc)
    std_mm_gc = np.std(mm_gc)

    # Mismatch metric
    mm_sp = 200 * (C1_arr_sp - C2_arr_sp) / (C1_arr_sp + C2_arr_sp)
    mean_mm_sp = np.mean(mm_sp)
    std_mm_sp = np.std(mm_sp)

    C = calculate_cap_from_model_equation(corner) * 1e12

    plt.figure(figsize=(8, 8))
    gs = plt.GridSpec(2, 1)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])

    # Plot capacitancce histogram and stats

    # Gnucap
    ax0.hist(C1_arr_gc, bins=50, color = "blue", alpha=0.5, density=True, label='Gnucap')
    ax0.axvline(mean_gc, color='blue', linestyle='--', linewidth=1, label=f"Gnucap C Mean={mean_gc:.5f}")
    ax0.axvline(mean_gc + std_gc, color='blue', linestyle=':', linewidth=1, label=f"Gnucap C STD={std_gc:.5f}")
    ax0.axvline(mean_gc - std_gc, color='blue', linestyle=':', linewidth=1)
    if plot_sp: # Ngspice
        ax0.hist(C1_arr_sp, bins=50, color="orange", alpha=0.5, density=True, label='Ngspice')
        ax0.axvline(mean_sp, color='orange', linestyle='--', linewidth=1, label=f"Ngspice C Mean={mean_sp:.5f}")
        ax0.axvline(mean_sp + std_sp, color='orange', linestyle=':', linewidth=1, label=f"Ngspice C STD={std_sp:.5f}")
        ax0.axvline(mean_sp - std_sp, color='orange', linestyle=':', linewidth=1)
        ax0.axvline(C, color='red', linestyle='--', linewidth=1, label=f"Model ={C:.5f}")

    ax0.set_xlabel('Capacitance (pF)')
    ax0.set_ylabel('Probability Density')
    ax0.legend(fontsize=10)  # Add legend

    # Plot mismatch metric and stats
    # Gnucap
    ax1.hist(mm_gc, bins=50, density=True, alpha=0.5, color='blue')
    ax1.axvline(mean_mm_gc, color='blue', linestyle='dashed', linewidth=1, label=f"Gnucap MM Mean={mean_mm_gc:.5f}")
    ax1.axvline(mean_mm_gc + std_mm_gc, color='blue', linestyle='dotted', linewidth=1, label=f"Gnucap MM STD={std_mm_gc:.5f}")
    ax1.axvline(mean_mm_gc - std_mm_gc, color='blue', linestyle='dotted', linewidth=1)
    if plot_sp: # Ngspcie
        ax1.hist(mm_sp, bins=50, density=True, alpha=0.5, color='orange')
        ax1.axvline(mean_mm_sp, color='orange', linestyle='dashed', linewidth=1, label=f"Ngspice MM Mean={mean_mm_sp:.5f}")
        ax1.axvline(mean_mm_sp + std_mm_sp, color='orange', linestyle='dotted', linewidth=1, label=f"Ngspice MM STD={std_mm_sp:.5f}")
        ax1.axvline(mean_mm_sp - std_mm_sp, color='orange', linestyle='dotted', linewidth=1)


    plt.suptitle(f'Local Mismatch Histograms at {corner} Corner', fontsize = 14)
    plt.savefig(cap_fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()
    plt.close()

    return

def plot_tb_cparasitic(corner, plot_sp=True, show=False):

    test_name = f'tb_cap_parasitic_{corner}'

    # Load gnucap data
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=7, engine='python').values

    # Load ngspice data
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+', skipfooter=3, engine='python').values

    t_gc = data_gc[:, 0] / 1e-6
    t_sp = data_sp[:, 0] / 1e-6

    v_pulse = data_gc[:, 1]

    v_c1_gc = data_gc[:, 2]
    v_c2_gc = data_gc[:, 3]
    v_c3_gc = data_gc[:, 4]

    v_c1_sp = data_sp[:, 2]
    v_c2_sp = data_sp[:, 3]
    v_c3_sp = data_sp[:, 4]

    plt.figure(figsize=(8, 10))
    gs = plt.GridSpec(3, 1, hspace = 0.3)

    plt.suptitle(f'Parasitic Capacitor RC Step Response {corner} Corner', fontsize = 14)

    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax2 = plt.subplot(gs[2], sharex=ax1)

    # Plot voltage v1 over time in ax0
    ax0.set_title('Cnom=100 fF', fontsize = 12)
    l1, = ax0.plot(t_gc, v_c1_gc, color='blue', linewidth=2.0, label = 'Gnucap')
    ax0.plot(t_sp, v_c1_sp, color='k', linestyle='--')
    ax0.plot(t_gc, v_pulse, linestyle='--', color='grey', alpha=0.5)
    ax0.set_ylabel('Voltage [V]', fontsize = 12)
    ax0.grid(True, alpha=0.3)
    ax0.set_ylabel('Voltage [V]', fontsize = 12)
    ax0.grid(True, alpha=0.3)

    # Plot voltage v2 over time in ax1
    ax1.set_title('Cnom=5 pF', fontsize=12)
    l2, = ax1.plot(t_gc, v_c2_gc, color='green', linewidth=2.0, label = 'Gnucap')
    ax1.plot(t_sp, v_c2_sp, color='k', linestyle='--')
    ax1.plot(t_gc, v_pulse, linestyle='--', color='grey', alpha=0.5)

    ax1.set_ylabel('Voltage [V]', fontsize = 12)
    ax1.grid(True, alpha=0.3)

    # Plot voltage v3 over time in ax2
    ax2.set_title('Cnom=10 pF', fontsize=12)
    l3, = ax2.plot(t_gc, v_c3_gc, color='red', linewidth=2.0, label = 'Gnucap')
    l4, = ax2.plot(t_sp, v_c3_sp, color='k', linestyle='--', label = 'Ngspice')
    l5, = ax2.plot(t_gc, v_pulse, linestyle='--', color='grey', alpha=0.5, label='VPulse')
    ax2.set_xlabel('Time [us]',  fontsize = 12)
    ax2.set_ylabel('Voltage [V]', fontsize = 12)
    ax2.grid(True, alpha=0.3)

    handles = [l1, l2, l3, l4, l5]
    ax2.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=10, ncol=len(handles))

    ceffs = { 'typ': ['100 fF', '5 pF', '10 pF'],
             'bcs': ['0.9 fF', '4.5 pF', '9 pF'],
             'wcs': ['110 fF', '5.5 pF', '11 pF']
    }
    taus = {
        'typ': ['1 ns', '50 ns', '100 ns'],
        'bcs': ['0.9 ns', '45 ns', '90 ns'],
        'wcs': ['1.1 ns', '55 ns', '110 ns']
    }

    res = '10 kΩ'

    axes = [ax0, ax1, ax2]
    for ax, ceff, tau in zip(axes, ceffs[corner], taus[corner]):
        info = (
            rf'$Ceff = {ceff}$' '\n'            
            rf'$R = {res}$' '\n'
            rf'$\tau = {tau}$'
        )

        ax.text(
            0.8, 0.82,
            info,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )

    plt.savefig(cap_fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()
    plt.close()

    return

def main():

    # for corner in['typ', 'bcs', 'wcs']:
        # plot_tb_cap_cutoff(corner)
        # plot_tb_cap_cutoff_mc_mm(corner)
        # plot_tb_cparasitic(corner)

    plot_tb_cap_cutoff_mc_stat()

    print('Finished plotting capactior!')

if __name__ == "__main__":

    main()

