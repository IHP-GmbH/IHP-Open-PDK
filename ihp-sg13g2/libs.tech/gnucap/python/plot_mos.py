from io import StringIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.pyplot import colormaps

from parse import split_nested_sweep, filter_data
from util import pointwise_rel_err

def plot_tb_mos_id_vd(
        test_name,
        title,
        ref_dir_gc,
        ref_dir_sp,
        fig_dir,
        skip_patterns_gc = None,
        rel_err_ylim_min = None,
        show = False
    ):

    filepath_gc = ref_dir_gc / (test_name + '.gc.out')
    filepath_sp = ref_dir_sp / (test_name + '.sp.out')

    if skip_patterns_gc:
        data_gc_filt = filter_data(filepath_gc, skip_prefixes=skip_patterns_gc)
        data_gc = pd.read_csv(StringIO(data_gc_filt), sep=r'\s+', skipfooter=5, engine="python").values
    else:
        data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=5, engine="python").values

    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values

    id_curves_gc, vd_arr_gc, vg_arr_gc = split_nested_sweep(data_gc, [2])
    id_curves_sp, vd_arr_sp, vg_arr_sp = split_nested_sweep(data_sp, [2])
    assert np.allclose(vg_arr_gc, vg_arr_sp)
    assert np.allclose(vd_arr_gc, vd_arr_sp)
    vg_arr = vg_arr_gc
    vd_arr = vd_arr_gc

    fig = plt.figure(figsize=(8, 8))
    gs = plt.GridSpec(2, 1, bottom=0.2, left=0.2, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)
    ax0.set_title(test_name)

    cmap = colormaps["spring"]
    norm = Normalize(vmin=vg_arr.min(), vmax=vg_arr.max())

    colors = cmap(norm(vg_arr))

    for i, (id_arr_gc, id_arr_sp, vg) in enumerate(zip(id_curves_gc, id_curves_sp, vg_arr)):

        ax0.plot(vd_arr, id_arr_gc, c=colors[i], ls='-', label=f'{vg}')
        ax0.plot(vd_arr, id_arr_sp, c='k', ls='--', label=f'ngspice' if i == len(vg_arr) - 1 else None)

        rel_abs_err_arr = pointwise_rel_err(id_arr_sp, id_arr_gc)
        ax1.semilogy(vd_arr, rel_abs_err_arr, c=colors[i], ls='-')

    fig.legend(title='V(g) [V]', ncol=len(vg_arr) + 1, bbox_to_anchor=(0.95, 0.1))

    ax0.set_title(title, fontsize=14)
    ax0.set_xlabel('V(d) [V]', fontsize=14)
    ax0.set_ylabel('I(d) [A]', fontsize=14)

    ax1.set_ylabel(r'$\varepsilon_{\mathrm{rel}}$', fontsize=18)
    ax1.set_xlabel('V(d) [V]', fontsize=14)

    if rel_err_ylim_min:
        ax1.set_ylim(ymin=rel_err_ylim_min)

    fig.align_ylabels()

    plt.savefig(fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()

    return

def plot_mos_mc_stats(test_name, ref_dir_gc, ref_dir_sp, fig_dir, plot_sp=True, show=False):

    filepath_gc = ref_dir_gc / (test_name + '.gc.out')
    filepath_sp = ref_dir_sp / (test_name + '.sp.out')

    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=4, engine="python").values
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values

    assert data_gc.shape == data_sp.shape, f"data_gc.shape {data_gc.shape} unequal data_sp.shape {data_sp.shape}"

    vg_nmos_gc = data_gc[:, 1]
    vg_nmos_sp = data_sp[:, 1]
    vg_pmos_gc = data_gc[:, 2]
    vg_pmos_sp = data_sp[:, 2]

    mean_nmos_gc = np.mean(vg_nmos_gc)
    mean_nmos_sp = np.mean(vg_nmos_sp)
    std_nmos_gc = np.std(vg_nmos_gc)
    std_nmos_sp = np.std(vg_nmos_sp)

    mean_pmos_gc = np.mean(vg_pmos_gc)
    mean_pmos_sp = np.mean(vg_pmos_sp)
    std_pmos_gc = np.std(vg_pmos_gc)
    std_pmos_sp = np.std(vg_pmos_sp)

    plt.figure(figsize=(14, 8))
    gs = plt.GridSpec(1, 2)

    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])

    plt.suptitle("Moslv Global Process Variation", fontsize=20)
    ax0.set_title('NMOS', fontsize=18)
    ax1.set_title('PMOS', fontsize=18)

    # Plot vg histogram for NMOS gnucap
    ax0.hist(vg_nmos_gc, bins=50, alpha=0.5, density=True, label='Gnucap', color='blue')
    ax0.axvline(mean_nmos_gc, color='blue', linestyle='--', linewidth=1, label=f"Gnucap Mean={mean_nmos_gc:.5f}")
    ax0.axvline(mean_nmos_gc + std_nmos_gc, color='blue', linestyle=':', linewidth=1,label=f"Gnucap STD={std_nmos_gc:.5f}")
    ax0.axvline(mean_nmos_gc - std_nmos_gc, color='blue', linestyle=':', linewidth=1)

    if plot_sp:
        ax0.hist(vg_nmos_sp, bins=50, alpha=0.5, density=True, label='Ngspice', color='orange')
        ax0.axvline(mean_nmos_sp, color='orange', linestyle='--', linewidth=1,label=f"Ngspice Mean={mean_nmos_sp:.5f}")
        ax0.axvline(mean_nmos_sp + std_nmos_sp, color='orange', linestyle=':', linewidth=1, label=f"Ngspice STD={std_nmos_sp:.5f}")
        ax0.axvline(mean_nmos_sp - std_nmos_sp, color='orange', linestyle=':', linewidth=1)

    ax0.set_xlabel('V(g) [V] ', fontsize=16)
    ax0.set_ylabel('Probability Density', fontsize=16)
    ax0.legend()

    # Plot vg histogram for NMOS gnucap
    ax1.hist(vg_pmos_gc, bins=50, alpha=0.5, density=True, label='Gnucap', color='blue')
    ax1.axvline(mean_pmos_gc, color='blue', linestyle='--', linewidth=1, label=f"Gnucap Mean={mean_pmos_gc:.5f}")
    ax1.axvline(mean_pmos_gc + std_pmos_gc, color='blue', linestyle=':', linewidth=1,label=f"Gnucap STD={std_pmos_gc:.5f}")
    ax1.axvline(mean_pmos_gc - std_pmos_gc, color='blue', linestyle=':', linewidth=1)

    if plot_sp:
        ax1.hist(vg_pmos_sp, bins=50, alpha=0.5, density=True, label='Ngspice', color='orange')
        ax1.axvline(mean_pmos_sp, color='orange', linestyle='--', linewidth=1,label=f"Ngspice Mean={mean_pmos_sp:.5f}")
        ax1.axvline(mean_pmos_sp + std_pmos_sp, color='orange', linestyle=':', linewidth=1, label=f"Ngspice STD={std_pmos_sp:.5f}")
        ax1.axvline(mean_pmos_sp - std_pmos_sp, color='orange', linestyle=':', linewidth=1)

    ax1.set_xlabel('V(g) [V] ', fontsize=16)
    ax1.set_ylabel('Probability Density', fontsize=16)
    ax1.legend()

    plt.savefig(fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()

    return

def plot_mos_mc_mm(test_name, ref_dir_gc, ref_dir_sp, fig_dir, plot_sp=True, show=False):

    filepath_gc = ref_dir_gc / (test_name + '.gc.out')
    filepath_sp = ref_dir_sp / (test_name + '.sp.out')

    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=4, engine="python").values
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values

    assert data_gc.shape == data_sp.shape, f"data_gc.shape {data_gc.shape} unequal to data_sp.shape {data_sp.shape}"

    # nmos
    vg1_nmos_gc = data_gc[:, 1]
    vg2_nmos_gc = data_gc[:, 2]
    vg1_nmos_sp = data_sp[:, 1]
    vg2_nmos_sp = data_sp[:, 2]

    mean_nmos_gc = np.mean(vg1_nmos_gc)
    mean_nmos_sp = np.mean(vg1_nmos_sp)
    std_nmos_gc = np.std(vg1_nmos_gc)
    std_nmos_sp = np.std(vg1_nmos_sp)

    mm_nmos_gc = 200 * (vg1_nmos_gc - vg2_nmos_gc) / (vg1_nmos_gc + vg2_nmos_gc)
    mm_nmos_sp = 200 * (vg1_nmos_sp - vg2_nmos_sp) / (vg1_nmos_sp + vg2_nmos_sp)

    mean_mm_nmos_gc = np.mean(mm_nmos_gc)
    mean_mm_nmos_sp = np.mean(mm_nmos_sp)
    std_mm_nmos_gc = np.std(mm_nmos_gc)
    std_mm_nmos_sp = np.std(mm_nmos_sp)

    # pmos
    vg1_pmos_gc = data_gc[:, 3]
    vg2_pmos_gc = data_gc[:, 4]
    vg1_pmos_sp = data_sp[:, 3]
    vg2_pmos_sp = data_sp[:, 4]

    mean_pmos_gc = np.mean(vg1_pmos_gc)
    mean_pmos_sp = np.mean(vg1_pmos_sp)
    std_pmos_gc = np.std(vg1_pmos_gc)
    std_pmos_sp = np.std(vg1_pmos_sp)

    mm_pmos_gc = 200 * (vg1_pmos_gc - vg2_pmos_gc) / (vg1_pmos_gc + vg2_pmos_gc)
    mm_pmos_sp = 200 * (vg1_pmos_sp - vg2_pmos_sp) / (vg1_pmos_sp + vg2_pmos_sp)

    mean_mm_pmos_gc = np.mean(mm_pmos_gc)
    mean_mm_pmos_sp = np.mean(mm_pmos_sp)
    std_mm_pmos_gc = np.std(mm_pmos_gc)
    std_mm_pmos_sp = np.std(mm_pmos_sp)

    plt.figure(figsize=(14, 16))

    gs = plt.GridSpec(2, 2)
    ax00 = plt.subplot(gs[0, 0])
    ax01 = plt.subplot(gs[0, 1])
    ax10 = plt.subplot(gs[1, 0])
    ax11 = plt.subplot(gs[1, 1])

    corner = test_name.rsplit('_', 1)[1]
    plt.suptitle(f"Moslv Local Mismatch at {corner} corner", fontsize=20)
    ax00.set_title('NMOS', fontsize=18)
    ax01.set_title('PMOS', fontsize=18)

    # NMOS
    ax00.hist(vg1_nmos_gc, bins=50, density=True, alpha=0.5, color='blue')
    ax00.axvline(mean_nmos_gc, color='blue', linestyle='dashed', linewidth=1, label=f"Gnucap Mean={mean_nmos_gc:.5f}")
    ax00.axvline(mean_nmos_gc + std_nmos_gc, color='blue', linestyle='dotted', linewidth=1, label=f"Gnucap STD={std_nmos_gc:.5f}")
    ax00.axvline(mean_nmos_gc - std_nmos_gc, color='blue', linestyle='dotted', linewidth=1)

    if plot_sp:
        ax00.hist(vg1_nmos_sp, bins=50, density=True, alpha=0.5, color='orange')
        ax00.axvline(mean_nmos_sp, color='orange', linestyle='dashed', linewidth=1, label=f"Ngspice Mean: {mean_nmos_sp:.5f}")
        ax00.axvline(mean_nmos_sp + std_nmos_sp, color='orange', linestyle='dotted', linewidth=1, label=f"Ngspice STD={std_nmos_sp:.5f}")
        ax00.axvline(mean_nmos_sp - std_nmos_sp, color='orange', linestyle='dotted', linewidth=1)

    ax00.set_xlabel(r'$V_1(g)$ [V] ', fontsize=16)
    ax00.set_ylabel('Probability Density', fontsize=16)
    ax00.legend()

    ax10.hist(mm_nmos_gc, bins=50, density=True, alpha=0.5, color='blue')
    ax10.axvline(mean_mm_nmos_gc, color='blue', linestyle='dashed', linewidth=1, label=f"Gnucap Mean={mean_mm_nmos_gc:.5f}")
    ax10.axvline(mean_mm_nmos_gc + std_mm_nmos_gc, color='blue', linestyle='dotted', linewidth=1, label=f"Gnucap STD={std_mm_nmos_gc:.5f}")
    ax10.axvline(mean_mm_nmos_gc - std_mm_nmos_gc, color='blue', linestyle='dotted', linewidth=1)

    if plot_sp:
        ax10.hist(mm_nmos_sp, bins=50, density=True, alpha=0.5, color='orange')
        ax10.axvline(mean_mm_nmos_sp, color='orange', linestyle='dashed', linewidth=1, label=f"Ngspice Mean: {mean_mm_nmos_sp:.5f}")
        ax10.axvline(mean_mm_nmos_sp + std_mm_nmos_sp, color='orange', linestyle='dotted', linewidth=1, label=f"Ngspice STD={std_mm_nmos_sp:.5f}")
        ax10.axvline(mean_mm_nmos_sp - std_mm_nmos_sp, color='orange', linestyle='dotted', linewidth=1)

    ax10.set_xlabel(r'$2 \frac{V_1(g) - V_2(g)}{V_1(g) - V_2(g)}$ [%]', fontsize=16)
    ax10.set_ylabel('Probability Density', fontsize=16)
    ax10.legend()

    # PMOS
    ax01.hist(vg1_pmos_gc, bins=50, density=True, alpha=0.5, color='blue')
    ax01.axvline(mean_pmos_gc, color='blue', linestyle='dashed', linewidth=1, label=f"Gnucap Mean={mean_pmos_gc:.5f}")
    ax01.axvline(mean_pmos_gc + std_pmos_gc, color='blue', linestyle='dotted', linewidth=1, label=f"Gnucap STD={std_pmos_gc:.5f}")
    ax01.axvline(mean_pmos_gc - std_pmos_gc, color='blue', linestyle='dotted', linewidth=1)

    if plot_sp:
        ax01.hist(vg1_pmos_sp, bins=50, density=True, alpha=0.5, color='orange')
        ax01.axvline(mean_pmos_sp, color='orange', linestyle='dashed', linewidth=1, label=f"Ngspice Mean: {mean_pmos_sp:.5f}")
        ax01.axvline(mean_pmos_sp + std_pmos_sp, color='orange', linestyle='dotted', linewidth=1, label=f"Ngspice STD={std_pmos_sp:.5f}")
        ax01.axvline(mean_pmos_sp - std_pmos_sp, color='orange', linestyle='dotted', linewidth=1)

    ax01.set_xlabel(r'$V_1(g)$ [V] ', fontsize=16)
    ax01.set_ylabel('Probability Density', fontsize=16)
    ax01.legend()

    ax11.hist(mm_pmos_gc, bins=50, density=True, alpha=0.5, color='blue')
    ax11.axvline(mean_mm_pmos_gc, color='blue', linestyle='dashed', linewidth=1, label=f"Gnucap Mean={mean_mm_pmos_gc:.5f}")
    ax11.axvline(mean_mm_pmos_gc + std_mm_pmos_gc, color='blue', linestyle='dotted', linewidth=1, label=f"Gnucap STD={std_mm_pmos_gc:.5f}")
    ax11.axvline(mean_mm_pmos_gc - std_mm_pmos_gc, color='blue', linestyle='dotted', linewidth=1)

    if plot_sp:
        ax11.hist(mm_pmos_sp, bins=50, density=True, alpha=0.5, color='orange')
        ax11.axvline(mean_mm_pmos_sp, color='orange', linestyle='dashed', linewidth=1, label=f"Ngspice Mean: {mean_mm_nmos_sp:.5f}")
        ax11.axvline(mean_mm_pmos_sp + std_mm_pmos_sp, color='orange', linestyle='dotted', linewidth=1, label=f"Ngspice STD={std_mm_nmos_sp:.5f}")
        ax11.axvline(mean_mm_pmos_sp - std_mm_pmos_sp, color='orange', linestyle='dotted', linewidth=1)

    ax11.set_xlabel(r'$2 \frac{V_1(g) - V_2(g)}{V_1(g) - V_2(g)}$ [%]', fontsize=16)
    ax11.set_ylabel('Probability Density', fontsize=16)
    ax11.legend()

    plt.savefig(fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()


    return

def plot_mos_inv(test_name, title, ref_dir_gc, ref_dir_sp, fig_dir, show=False):

    filepath_gc = ref_dir_gc / (test_name + '.gc.out')
    filepath_sp = ref_dir_sp / (test_name + '.sp.out')

    data_gc_filt = filter_data(filepath_gc, skip_prefixes=('did not converge', 'open circuit'))
    data_gc = pd.read_csv(StringIO(data_gc_filt), sep=r'\s+', skipfooter=5, engine="python").values
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values

    vin_gc, vout_gc, idd_gc = data_gc[:, 0], data_gc[:, 1], data_gc[:, 2]
    vin_sp, vout_sp, idd_sp = data_sp[:, 0], data_sp[:, 1], data_sp[:, 2]

    assert np.allclose(vin_gc, vin_sp), "v(in) mismatch between gnucap and ngspice datasets"

    # Plotting setup
    plt.figure(figsize=(10, 8))
    gs = plt.GridSpec(2, 2)
    ax00 = plt.subplot(gs[0, 0])
    ax10 = plt.subplot(gs[1, 0])
    ax10.sharex(ax00)
    ax01 = plt.subplot(gs[0, 1])
    ax11 = plt.subplot(gs[1, 1])
    ax11.sharex(ax01)

    plt.suptitle(title, fontsize=14)

    ax00.plot(vin_gc, vout_gc, ls='-', color="blue" , label="Gnucap")
    ax00.plot(vin_sp, vout_sp, ls='--', color='k', label="Ngspice")
    ax00.set_ylabel("V(out) [V]", fontsize=12)
    ax00.legend()

    ax01.plot(vin_gc, -idd_gc, ls='-', color="red"  , label="Gnucap")
    ax01.plot(vin_sp, -idd_sp, ls='--', color='k', label="Ngspice")
    ax01.set_ylabel("I(DD) [A]", fontsize=12)
    ax01.legend()

    rel_abs_err = pointwise_rel_err(vout_gc, vout_sp)
    ax10.semilogy(vin_gc, rel_abs_err, ls='-', color='k')
    ax10.set_xlabel("V(in) [V]", fontsize=12)
    ax10.set_ylabel(r"$\varepsilon_{\mathrm{rel}}$", fontsize=14)

    rel_abs_err = pointwise_rel_err(-idd_sp, -idd_gc)
    ax11.semilogy(vin_gc, rel_abs_err, ls='-', color='k')
    ax11.set_xlabel("V(in) [V]", fontsize=12)
    ax11.set_ylabel(r"$\varepsilon_{\mathrm{rel}}$", fontsize=14)

    # Save and/or show the plot
    plt.tight_layout()
    plt.savefig(fig_dir / f"{test_name}.png", dpi=300)

    if show:
        plt.show()

    plt.close()

    return

def plot_mos_inv_all_corners(ref_dir_gc, fig_dir, fig_name, show=False):

    corners = ['tt', 'ss', 'ff', 'sf', 'fs']
    fig, ax = plt.subplots(figsize=(10, 6))

    for corner in corners:
        filepath_gc = ref_dir_gc / f"tb_moslv_inv_{corner}.gc.out"

        data_gc_filt = filter_data(filepath_gc, skip_prefixes=('did not converge', 'open circuit'))
        data_gc = pd.read_csv(StringIO(data_gc_filt), sep=r'\s+', skipfooter=5, engine="python").values
        vin_gc, vout_gc = data_gc[:, 0], data_gc[:, 1]

        ax.plot(vin_gc, vout_gc, label=f'{corner.upper()}')

    ax.set_xlabel('V(in) [V]', fontsize=12)
    ax.set_ylabel('V(out) [V]', fontsize=12)
    ax.set_title('moslv CMOS inverter All Corners (Gnucap)', fontsize=14)
    ax.legend(title="Corners", fontsize=10)

    plt.tight_layout()
    plt.savefig(fig_dir / (fig_name + ".png"), dpi=300)

    if show:
        plt.show()

    plt.close()

    return
