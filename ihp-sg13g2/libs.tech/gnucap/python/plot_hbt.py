import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from parse import split_nested_sweep
from dirs import tests_dir_gc, tests_dir_sp, fig_dir
from util import pointwise_rel_err

hbt_fig_dir = fig_dir / "hbt"
hbt_fig_dir.mkdir(parents=True, exist_ok=True)

ref_dir_gc = tests_dir_gc / "hbt" / "ref"
ref_dir_sp = tests_dir_sp / "hbt" / "ref"

def plot_tb_dc_hbt(device_variant: str, corner: str, show: bool = False):

    test_name = f"tb_dc_hbt_{device_variant}_" + corner

    filepath_gc = ref_dir_gc / (test_name + ".gc.out")

    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=5, engine="python").values
    i_vc_list_gc, vce_gc, i0_gc = split_nested_sweep(data_gc, [2])

    filepath_sp = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values
    i_vc_list_sp, vce_sp, i0_sp = split_nested_sweep(data_sp, [2])

    assert np.allclose(vce_gc, vce_sp)
    assert np.allclose(i0_gc, i0_sp)

    vce = vce_sp
    i0 = i0_sp

    fig = plt.figure(figsize=(8, 8))
    gs = plt.GridSpec(2, 1)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])

    cmap = plt.cm.spring
    norm = plt.Normalize(vmin=i0.min(), vmax=i0.max())

    for i, (i_vc_gc, i_vc_sp, i0_value) in enumerate(zip(i_vc_list_gc, i_vc_list_sp, i0)):

        color = cmap(norm(i0_value))
        i_vc_gc = np.abs(i_vc_gc)
        i_vc_sp = np.abs(i_vc_sp)

        ax0.plot(vce, i_vc_gc, '-', color=color)
        ax0.plot(vce, i_vc_sp, '--', c='k')

        if i > 0:
            rel_abs_err_arr = pointwise_rel_err(i_vc_gc, i_vc_sp)
            ax1.semilogy(vce, rel_abs_err_arr, c=color, ls='-')

    ax0.set_xlabel('V(C) [V]', fontsize = 14)
    ax0.set_ylabel('I(C) [A]', fontsize = 14)
    ax0.set_ylim(0, np.max(i_vc_list_sp) * 1.1)
    ax0.grid(True, alpha=0.3)
    ax1.set_ylabel(r'$\varepsilon_{\mathrm{rel}}$', fontsize=18)
    ax1.set_xlabel('V(C) [V]', fontsize = 14)
    ax1.grid(True, alpha=0.3)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=[ax0, ax1], orientation='vertical')
    cbar.set_label('I(B) [A]', fontsize = 14)

    plt.savefig(hbt_fig_dir / f"{test_name}.png")

    if show:
        plt.show()

    plt.close()

def plot_tb_dc_hbt_13g2(corner: str, show: bool = False):
    plot_tb_dc_hbt("13g2", corner)

def plot_tb_dc_hbt_13g2l(corner, show: bool = False):
    plot_tb_dc_hbt("13g2l", corner)

def plot_tb_dc_hbt_13g2v(corner, show: bool = False):
    plot_tb_dc_hbt("13g2v", corner)

def plot_tb_ac_hbt_13g2(corner: str, show: bool = False):

    test_name = f"tb_ac_hbt_13g2_{corner}"

    # Load Gnucap data
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skiprows=2, skipfooter=5, engine="python").values

    # Load Ngspice data
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+', skipfooter=1, engine="python").values

    f_gc  = data_gc[:, 0]
    vc_gc = data_gc[:, 1]
    vb_gc = data_gc[:, 2]

    f_sp  = data_sp[:, 0]
    vc_sp = data_sp[:, 1]
    vb_sp = data_sp[:, 2]

    gain_gc = 20 * np.log10(np.abs(vc_gc / vb_gc))
    gain_sp = 20 * np.log10(np.abs(vc_sp / vb_sp))

    fig = plt.figure(figsize=(8, 8))
    gs = plt.GridSpec(1, 1)
    ax0 = plt.subplot(gs[0])

    ax0.semilogx(f_gc, gain_gc, c = "blue", label="Gnucap")
    ax0.semilogx(f_sp, gain_sp, c = "orange", ls = "--", label="ngspice")

    ax0.set_xlabel("Frequency [Hz]", fontsize=14)
    ax0.set_ylabel(r"$|V(C) / V(B)|$ [dB]", fontsize=14)
    ax0.ticklabel_format(axis="y", style="plain", useOffset=False)
    ax0.grid(True, alpha=0.3)

    plt.savefig(hbt_fig_dir / f"{test_name}.png")

    if show:
        plt.show()

    plt.close()

def plot_tb_dc_mc_mm_hbt(device_variant: str, corner: str, title: str, show: bool = False):

    test_name = f"tb_dc_mc_mm_hbt_{device_variant}_{corner}"
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=7, engine="python").values
    ic_gc = data_gc[:, 1] * 1e6
    ic_gc = np.abs(ic_gc)

    mean_gc = np.mean(ic_gc)
    std_gc = np.std(ic_gc)

    ax = plt.subplot(111)
    ax.hist(ic_gc, bins=50, alpha=0.5, density=True, color="blue", label="Gnucap")
    ax.axvline(mean_gc, color="blue", linestyle="--", linewidth=3, label=f"Mean={mean_gc:.5e} uA")
    ax.axvline(mean_gc + std_gc, color="blue", linestyle=":", linewidth=2, label=f"STD={std_gc:.5e} uA")
    ax.axvline(mean_gc - std_gc, color="blue", linestyle=":", linewidth=2)

    ax.set_xlabel("I(C) [uA]")
    ax.set_ylabel("Probability Density")
    ax.set_title(title)
    ax.legend()

    plt.savefig(hbt_fig_dir / f"{test_name}.png", dpi=300)

    if show:
        plt.show()

    plt.close()

def plot_tb_dc_mc_mm_hbt_13g2(corner: str, show: bool = False):
    plot_tb_dc_mc_mm_hbt("13g2", corner, f"HBT G2 MM Monte Carlo ({corner.upper()} Corner)", show)

def plot_tb_dc_mc_mm_hbt_13g2l(corner: str, show: bool = False):
    plot_tb_dc_mc_mm_hbt("13g2l", corner, f"HBT G2L MM Monte Carlo ({corner.upper()} Corner)", show)

def plot_tb_dc_mc_mm_hbt_13g2v(corner: str, show: bool = False):
    plot_tb_dc_mc_mm_hbt("13g2v", corner, f"HBT G2V MM Monte Carlo ({corner.upper()} Corner)", show)

def plot_tb_dc_mc_stat_hbt(device_variant: str, title: str, show: bool = False):

    test_name = f"tb_dc_mc_stat_hbt_{device_variant}"
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data_gc = pd.read_csv(filepath_gc, sep=r'\s+', skipfooter=7, engine="python").values
    ic_gc = data_gc[:, 1] * 1e6
    ic_gc = np.abs(ic_gc)

    filepath_sp = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values
    ic_sp = data_sp[:, 1] * 1e6

    mean_gc = np.mean(ic_gc)
    std_gc = np.std(ic_gc)
    mean_sp = np.mean(ic_sp)
    std_sp = np.std(ic_sp)

    ax = plt.subplot(111)
    ax.hist(ic_gc, bins=50, alpha=0.5, density=True, color="blue", label="Gnucap")
    ax.axvline(mean_gc, color="blue", linestyle="--", linewidth=3, label=f"Gnucap Mean={mean_gc:.5e} uA")
    ax.axvline(mean_gc + std_gc, color="blue", linestyle=":", linewidth=2, label=f"Gnucap STD={std_gc:.5e} uA")
    ax.axvline(mean_gc - std_gc, color="blue", linestyle=":", linewidth=2)
    ax.hist(ic_sp, bins=50, alpha=0.5, density=True, color="orange", label="Ngspice")
    ax.axvline(mean_sp, color="orange", linestyle="--", linewidth=3, label=f"Ngspice Mean={mean_sp:.5e} uA")
    ax.axvline(mean_sp + std_sp, color="orange", linestyle=":", linewidth=2, label=f"Ngspice STD={std_sp:.5e} uA")
    ax.axvline(mean_sp - std_sp, color="orange", linestyle=":", linewidth=2)

    ax.set_xlabel("I(C) [uA]")
    ax.set_ylabel("Probability Density")
    ax.set_title(title)
    ax.legend()

    plt.savefig(hbt_fig_dir / f"{test_name}.png", dpi=300)

    if show:
        plt.show()

    plt.close()

def plot_tb_dc_mc_stat_hbt_13g2(show: bool = False):
    plot_tb_dc_mc_stat_hbt("13g2", "HBT G2 Global Monte Carlo ", show)

def plot_tb_dc_mc_stat_hbt_13g2l(show: bool = False):
    plot_tb_dc_mc_stat_hbt("13g2l", "HBT G2L Global Monte Carlo", show)

def plot_tb_dc_mc_stat_hbt_13g2v(show: bool = False):
    plot_tb_dc_mc_stat_hbt("13g2v", "HBT G2V Global Monte Carlo", show)

# def plot_tb_dc_pnpMPA(corner: str, show: bool = False):
#
#     test_name = "tb_dc_pnpMPA" + "_" + corner
#     filepath_sp = ref_dir_sp / (test_name + ".sp.out")
#     data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values
#
#     i0_sp = data_sp[:, 0]
#     i_vc_sp = data_sp[:, 1]
#     i_vb_sp = data_sp[:, 2]
#
#     ax = plt.subplot(111)
#     ax.plot(i0_sp, i_vc_sp, label="I(C)")
#     ax.plot(i0_sp, i_vb_sp, label="I(B)")
#     ax.set_xlabel("I0 [A]")
#     ax.set_ylabel("Current [A]")
#     ax.set_title("pnpMPA DC currents")
#     ax.legend()
#
#     plt.savefig(hbt_fig_dir / f"{test_name}.png")
#
#     if show:
#         plt.show()
#
#     plt.close()

def main():


    for corner in ["typ", "bcs", "wcs"]:
        # hbt_13g2
        plot_tb_dc_hbt_13g2(corner)
        plot_tb_ac_hbt_13g2(corner)
        plot_tb_dc_mc_mm_hbt_13g2(corner)
        # hbt_13g2l
        plot_tb_dc_hbt_13g2l(corner)
        plot_tb_dc_mc_mm_hbt_13g2l(corner)
        # hbt_13g2v
        plot_tb_dc_hbt_13g2v(corner)
        plot_tb_dc_mc_mm_hbt_13g2v(corner)

    plot_tb_dc_mc_stat_hbt_13g2()
    plot_tb_dc_mc_stat_hbt_13g2l()
    plot_tb_dc_mc_stat_hbt_13g2v()

    print('Finished plotting hbt!')


if __name__ == "__main__":

    main()
