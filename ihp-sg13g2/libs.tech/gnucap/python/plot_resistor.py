import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dirs import tests_dir_gc, tests_dir_sp, fig_dir

res_fig_dir = fig_dir / "resistor"
res_fig_dir.mkdir(parents=True, exist_ok=True)

ref_dir_gc = tests_dir_gc / "resistor" / "ref"
ref_dir_sp = tests_dir_sp / "resistor" / "ref"
assert ref_dir_gc.exists()
assert ref_dir_sp.exists()

r3_cmc_res_variants = ['rsil', 'rhigh', 'rppd']

def plot_tb_res_mc_stats(mc_trials ="", plot_sp = True, show = False):

    test_name = f'tb_res_mc_stat{mc_trials}'
    # Load gnucap data
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=4, engine="python").values
    # Load ngspice data
    filepath_ngspice = ref_dir_sp / f'tb_res_mc_stat{mc_trials}.sp.out'
    data_sp = pd.read_csv(filepath_ngspice, sep=r'\s+').values

    assert data_gc.shape == data_sp.shape, f"data_gc.shape {data_gc.shape} unequal data_gc.shape {data_sp.shape}"

    I = 0.001

    plt.figure(figsize=(20, 8))
    gs = plt.GridSpec(1, 3)

    for i, res_variant in enumerate(r3_cmc_res_variants):

        idx = 2*i + 1;
        res_gc = data_gc[:, idx] / I
        res_sp = data_sp[:, idx] / I
        # TODO: global variation is not global yet
        # assert np.allclose(res_gc, data_gc[:, idx+1] / I), "r1 and r2 do not match in gnucap"
        # assert np.allclose(res_gc,  data_sp[:, idx+1] / I), "r1 and r2 do not match in ngspice"

        mean_gc = np.mean(res_gc)
        mean_sp = np.mean(res_sp)
        std_gc = np.std(res_gc)
        std_sp = np.std(res_sp)

        ax = plt.subplot(gs[0, i])
        ax.set_title(res_variant, fontsize=13)
        # Plot resistance histogram
        ax.hist(res_gc, bins=50, alpha=0.5, density=True, label='Gnucap')
        ax.axvline(mean_gc, color='blue', linestyle='--', linewidth=1, label=f"Gnucap Mean={mean_gc:.5f}")
        ax.axvline(mean_gc + std_gc, color='blue', linestyle=':', linewidth=1, label=f"Gnucap STD={std_gc:.5f}")
        ax.axvline(mean_gc - std_gc, color='blue', linestyle=':', linewidth=1)

        if plot_sp:
            ax.hist(res_sp, bins=50, alpha=0.5, density=True, label='Ngspice')
            ax.axvline(mean_sp, color='orange', linestyle='--', linewidth=1, label=f"Ngspice Mean= {mean_sp:.5f}")
            ax.axvline(mean_sp + std_sp, color='orange', linestyle=':', linewidth=1, label=f"Ngspice STD={std_sp:.5f}")
            ax.axvline(mean_sp - std_sp, color='orange', linestyle=':', linewidth=1)

        ax.set_xlabel('Resistance (Ohms)')
        ax.set_ylabel('Probability Density')
        ax.legend(fontsize = 10)  # Add legend

    plt.suptitle(f'Global process variation', fontsize = 14)
    # Remove text annotations (moved to legend)
    plt.savefig(res_fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()

def plot_tb_res_mc_mm(corner ='typ', mc_trials="", plot_sp = True, show = False):

    test_name = f'tb_res_mc_mm{mc_trials}_{corner}'
    # Load gnucap data
    filepath_gc = ref_dir_gc / (test_name + '.gc.out')
    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=4, engine="python").values
    # Load ngspice data
    filepath_ngspice = ref_dir_sp / (test_name + '.sp.out')
    data_sp = np.abs(pd.read_csv(filepath_ngspice, sep=r'\s+').values)

    assert data_gc.shape == data_sp.shape, f"data_gc.shape {data_gc.shape} unequal data_gc.shape {data_sp.shape}"

    I = 0.001

    plt.figure(figsize=(20, 8))
    gs = plt.GridSpec(2, 3)

    for i, res_variant in enumerate(r3_cmc_res_variants):

        idx = 2*i + 1;
        res1_gc = data_gc[:, idx] / I
        res1_sp = data_sp[:, idx] / I
        res2_gc = data_gc[:, idx+1] / I
        res2_sp = data_sp[:, idx+1] / I

        mm_gc = 100 * (res1_gc - res2_gc) / (res1_gc + res2_gc)
        mm_sp = 100 * (res1_sp - res2_sp) / (res1_sp + res2_sp)

        mean_gc = np.mean(res1_gc)
        std_gc = np.std(res1_gc)
        mean_ngs = np.mean(res1_sp)
        std_ngs = np.std(res1_sp)

        mean_mm_gc = np.mean(mm_gc)
        std_mm_gc = np.std(mm_gc)
        mean_mm_ngs = np.mean(mm_sp)
        std_mm_ngs = np.std(mm_sp)

        ax0 = plt.subplot(gs[0, i])
        ax1 = plt.subplot(gs[1, i])
        ax0.set_title(res_variant)

        # Absolute resistance histograms
        ax0.hist(res1_gc, bins=50, density=True, alpha=0.5, color='blue')
        ax0.axvline(mean_gc, color='blue', linestyle='dashed', linewidth=1, label=f"Gnucap R1 Mean={mean_gc:.5f}")
        ax0.axvline(mean_gc + std_gc, color='blue', linestyle='dotted', linewidth=1, label=f"Gnucap R1 STD={std_gc:.5f}")
        ax0.axvline(mean_gc - std_gc, color='blue', linestyle='dotted', linewidth=1)

        if plot_sp:
            ax0.hist(res1_sp, bins=50, density=True, alpha=0.5, color='orange')
            ax0.axvline(mean_ngs, color='orange', linestyle='dashed', linewidth=1, label=f"Ngspice R1 Mean: {mean_ngs:.5f}")
            ax0.axvline(mean_ngs + std_ngs, color='orange', linestyle='dotted', linewidth=1, label=f"Ngspice R1 STD={std_ngs:.5f}")
            ax0.axvline(mean_ngs - std_ngs, color='orange', linestyle='dotted', linewidth=1)

        ax0.set_xlabel('Resistance (Ohms)')
        ax0.set_ylabel('Probability Density')
        ax0.legend()

        # Plot mismatch metric
        ax1.hist(mm_gc , bins=50, density=True, alpha=0.5, color='blue')
        ax1.axvline(mean_mm_gc, color='blue', linestyle='dashed', linewidth=1, label=f"Gnucap MM Mean={mean_mm_gc:.5f}")
        ax1.axvline(mean_mm_gc + std_mm_gc, color='blue', linestyle='dotted', linewidth=1, label=f"Gnucap MM STD={std_mm_gc:.5f}")
        ax1.axvline(mean_mm_gc - std_mm_gc, color='blue', linestyle='dotted', linewidth=1)

        if plot_sp:
            ax1.hist(mm_sp, bins=50, density=True, alpha=0.5, color='orange')
            ax1.axvline(mean_mm_ngs, color='orange', linestyle='dashed', linewidth=1, label=f"Ngspice MM Mean: {mean_mm_ngs:.5f}")
            ax1.axvline(mean_mm_ngs + std_mm_ngs, color='orange', linestyle='dotted', linewidth=1, label=f"Ngspice MM STD={std_mm_ngs:.5f}")
            ax1.axvline(mean_mm_ngs - std_mm_ngs, color='orange', linestyle='dotted', linewidth=1)

        ax1.set_xlabel(r'$(R1 - R2)/(R1 + R2)$ [%]')
        ax1.set_ylabel('Probability Density')
        ax1.legend()

    plt.suptitle(f'Local Mismatch Histograms at {corner} Corner', fontsize = 14)
    plt.savefig(res_fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()

    return

# def plot_tb_res_stats_convergence():
#
#     mean_list_gc, std_list_gc = [], []
#     mean_list_sp, std_list_sp = [], []
#
#     I = 0.001
#
#     mc_trials = np.array([10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 4000, 6000, 8000, 10000])
#
#     for N in mc_trials:
#         # Load gnucap data
#         filepath_gc = ref_dir_gc / f'tb_res_stats_mc{N}.gc.out'
#         data_gc = pd.read_csv(filepath_gc, sep=r'\s+').values
#         # Load ngspice data
#         filepath_ngspice = ref_dir_sp / f'tb_res_stats_mc{N}.sp.out'
#         data_sp = pd.read_csv(filepath_ngspice, sep=r'\s+').values
#
#         # assert data_gc.shape[0] == data_sp.shape[0], "Gnucap and ngspice results length mismatch"
#         # TODO: resistance of r1 and r2 do not match although global variations should be the same
#         # assert np.allclose(data_gc[:, 1], data_gc[:, 2]), "first and second resistor should match exactly"
#         # assert np.allclose(data_sp[:, 1], data_sp[:, 2]), "first and second resistor should match exactly"
#
#         res_gc = data_gc[:, 1] / I
#         res_sp = data_sp[:, 1] / I
#         # TODO: why is current sign negative?
#         res_sp = np.abs(res_sp)
#
#         mean_list_gc.append(np.mean(res_gc))
#         mean_list_sp.append(np.mean(res_sp))
#         std_list_gc.append(np.std(res_gc))
#         std_list_sp.append(np.std(res_sp))
#
#     mean_arr_gc, mean_arr_sp = np.array(mean_list_gc), np.array(mean_list_sp)
#     std_arr_gc, std_arr_sp = np.array(std_list_gc), np.array(std_list_sp)
#
#     mean_gc_ref = mean_arr_gc[-1]
#     rel_err = np.abs(mean_arr_gc[:-1] - mean_gc_ref) / mean_gc_ref
#
#     gs = plt.GridSpec(2, 1)
#     ax0 = plt.subplot(gs[0])
#     ax0.loglog(mc_trials[:-1], rel_err)
#
#     # rel_mean_err = np.abs(mean_arr_gc - mean_arr_sp) / mean_arr_sp
#     # rel_std_err = np.abs(std_arr_gc - std_arr_sp) / std_arr_sp
#
#     # ax1 = plt.subplot(gs[1], sharex=ax0)
#
#     # ax0.loglog(mc_trials, rel_mean_err, 'o-', color='k')
#     # ax1.loglog(mc_trials, rel_std_err, 'o-', color='k')
#     #
#     # ax0.set_ylabel('Relative Mean Error')
#     # ax1.set_ylabel('Relative Std Error')
#     # ax1.set_xlabel('Number of Monte Carlo Trials')
#     #
#     # plt.tight_layout()
#
#     plt.show()
#
#     return

def main():

    plot_tb_res_mc_stats()
    plot_tb_res_mc_mm(corner='typ')
    plot_tb_res_mc_mm(corner='bcs')
    plot_tb_res_mc_mm(corner='wcs')

    print('Finished plotting resistor!')

if __name__ == "__main__":

    main()
