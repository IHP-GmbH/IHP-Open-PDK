from io import StringIO

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from dirs import tests_dir_gc, tests_dir_sp, fig_dir
from parse import filter_data, split_mc_trials

svaricaphv_fig_dir = fig_dir / "svaricaphv"
svaricaphv_fig_dir.mkdir(parents=True, exist_ok=True)

ref_dir_gc = tests_dir_gc / "svaricaphv" / "ref"
ref_dir_sp = tests_dir_sp / "svaricaphv" / "ref"

assert ref_dir_gc.exists()
assert ref_dir_sp.exists()

def plot_test_svaricaphv_tran(corner: str, show: bool = False):

    test_name = f"test_svaricaphv_tran_{corner}"

    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")

    data_gc_str = filter_data(
        filepath_gc,
        ("#", "parameter", "open circuit", "Gnucap", "iterations:", "transient", "nodes:", "dctran"),
    )
    data_gc = pd.read_csv(StringIO(data_gc_str), sep=r"\s+", header=None, engine="python").values
    data_sp = pd.read_csv(filepath_sp, sep=r"\s+").values

    t_gc = data_gc[:, 0] / 1e-6
    vg1_gc = data_gc[:, 1]
    vg2_gc = data_gc[:, 2]
    assert(np.allclose(vg1_gc, vg2_gc, atol=1e-6))

    iv1_gc = data_gc[:, 3] * 1e9

    t_sp = data_sp[:, 0] / 1e-6
    v_sp = data_sp[:, 1]
    iv1_sp = data_sp[:, 2] * 1e9

    fig = plt.figure(figsize=(10, 8))
    gs = plt.GridSpec(2, 1, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)

    plt.suptitle(f"sg13_hv_svaricap - transient ramp ({corner.upper()} corner)", fontsize=14)

    ax0.plot(t_gc, vg1_gc, "-", color="blue", linewidth=2, label="Gnucap")
    ax0.plot(t_sp, v_sp, "--", color="orange", linewidth=1.5, label="Ngspice")
    ax0.set_ylabel("Voltage V(G1/G2) [V]", fontsize=12)
    ax0.legend()
    ax0.grid(True, alpha=0.3)

    ax1.plot(t_gc, iv1_gc, "-", color="blue", linewidth=2, label="Gnucap")
    ax1.plot(t_sp, iv1_sp, "--", color="orange", linewidth=1.5, label="Ngspice")
    ax1.set_xlabel("Time [us]", fontsize=12)
    ax1.set_ylabel("current i(G2) [nA]", fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    plt.savefig(svaricaphv_fig_dir / (test_name + ".png"), dpi=300)

    if show:
        plt.show()

    plt.close(fig)

def plot_test_svaricaphv_ac(corner: str, show=False):

    test_name = "test_svaricaphv_ac_" + corner

    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")

    data_gc_str = filter_data(
        filepath_gc,
        ("#", "parameter"),
    )
    data_gc = pd.read_csv(StringIO(data_gc_str), sep=r"\s+", skiprows=1, header=None, engine="python").values
    data_sp = pd.read_csv(filepath_sp, sep=r"\s+").values

    assert data_gc.shape[1] >= 3
    assert data_sp.shape[1] >= 3

    f_gc  = data_gc[:, 0]
    ir_gc = data_gc[:, 1]
    ii_gc = data_gc[:, 2]

    f_sp  = data_sp[:, 0]
    ir_sp = data_sp[:, 1]
    ii_sp = data_sp[:, 2]

    cap_gc = ii_gc / (2 * np.pi * f_gc)
    cap_sp = ii_sp / (2 * np.pi * f_sp)

    fig = plt.figure(figsize=(10, 8))
    gs = plt.GridSpec(2, 1, hspace=0.3, top=0.925)
    ax_ir = plt.subplot(gs[0])
    ax_ii = ax_ir.twinx()
    ax_cap = plt.subplot(gs[1], sharex=ax_ir)

    plt.suptitle("sg13g2_hv_svaricap — AC", fontsize=14)

    ax_ir.semilogx(f_gc, ir_gc * 1e6, "-",  color="blue",   linewidth=2,   label="Gnucap")
    ax_ir.semilogx(f_sp, ir_sp * 1e6, "--", color="black",  linewidth=1.5, label="Ngspice")
    ax_ir.set_ylabel("Real current [uA]", fontsize=12, color="blue")
    ax_ir.legend(loc="upper left")
    ax_ir.grid(True, which="both", alpha=0.3)

    ax_ii.semilogx(f_gc, ii_gc * 1e6, "-",  color="red",    linewidth=2,    label="Gnucap")
    ax_ii.semilogx(f_sp, ii_sp * 1e6, "--", color="black",  linewidth=1.5, label="Ngspice")
    ax_ii.set_ylabel("Imag current [uA]", fontsize=12, color="red")
    ax_ii.legend(loc="upper right")

    ax_cap.semilogx(f_gc, cap_gc * 1e15, "-",  color="blue",   linewidth=2,   label="Gnucap")
    ax_cap.semilogx(f_sp, cap_sp * 1e15, "--", color="orange", linewidth=1.5, label="Ngspice")
    ax_cap.set_xlabel("Frequency [Hz]", fontsize=12)
    ax_cap.set_ylabel("Capacitance [fF]", fontsize=12)
    ax_cap.legend()
    ax_cap.grid(True, which="both", alpha=0.3)

    plt.savefig(svaricaphv_fig_dir / (test_name + ".png"), dpi=300)

    if show:
        plt.show()

    plt.close(fig)

def plot_test_svaricaphv_mc_stat_ac(plot_sp=True, show=False):

    test_name = "test_svaricaphv_mc_stat_ac"

    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")

    data_gc = pd.read_csv(StringIO(filter_data(filepath_gc, ("#", "parameter"))),
        sep=r"\s+", header=None).values

    data_sp = pd.read_csv(StringIO(filter_data(filepath_sp, "frequency")),
        sep=r"\s+", header=None,).values

    # trials, f, out
    trials_gc = split_mc_trials(data_gc)
    trials_sp = split_mc_trials(data_sp)

    f_arr_gc = trials_gc[0, :, 0]
    f_arr_sp = trials_sp[0, :, 0]

    ii_gc = trials_gc[:, :, 1]
    cap_arr_gc = ii_gc / (2 * np.pi * f_arr_gc)
    cap_arr_sp = trials_sp[:, :, 1]

    mean_cap_gc = np.mean(cap_arr_gc, axis=0)
    mean_cap_sp = np.mean(cap_arr_sp, axis=0)

    std_cap_sp = np.std(cap_arr_sp, axis=0)
    std_cap_gc = np.std(cap_arr_gc, axis=0)

    fig = plt.figure(figsize=(10, 8))
    gs = plt.GridSpec(1, 1, top=0.925)
    ax = plt.subplot(gs[0])

    plt.suptitle("sg13g2_hv_svaricap_psp — Global process variation", fontsize=14)

    ax.semilogx(f_arr_gc, mean_cap_gc * 1e15, "-", color="blue", linewidth=2, label="Gnucap mean")
    ax.fill_between(f_arr_gc, (mean_cap_gc - 2*std_cap_gc) * 1e15, (mean_cap_gc + 2*std_cap_gc) * 1e15, color="blue", alpha=0.2, label=r"Gnucap $\pm 2\sigma$")

    ax.semilogx(f_arr_sp, mean_cap_sp * 1e15, "--", color="orange", linewidth=1, label="ngspice mean")
    ax.fill_between(f_arr_sp, (mean_cap_sp - 2*std_cap_sp) * 1e15, (mean_cap_sp + 2*std_cap_sp) * 1e15, color="orange", alpha=0.2, label=r"ngspice $\pm 2\sigma$")

    ax.set_xlabel("Frequency [Hz]", fontsize=12)
    ax.set_ylabel("Capacitance [fF]", fontsize=12)
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)

    plt.savefig(svaricaphv_fig_dir / (test_name + ".png"), dpi=300)

    if show:
        plt.show()

    plt.close(fig)

def plot_test_svaricaphv_mc_mm_ac(corner: str, show: bool = False):

    test_name = f"test_svaricaphv_mc_mm_ac_{corner}"
    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")

    data_gc = pd.read_csv(StringIO(filter_data(filepath_gc, ("#", "parameter"))),
        sep=r"\s+", header=None).values

    data_sp = pd.read_csv(StringIO(filter_data(filepath_sp, "frequency")),
        sep=r"\s+", header=None).values

    trials_gc = split_mc_trials(data_gc)
    trials_sp = split_mc_trials(data_sp)

    # trials, f, ii1, ii2
    f_gc = trials_gc[0, :, 0]
    # trials, f, c1r, c1i, c2r, c2i
    f_sp = trials_sp[0, :, 0]

    cap1_gc = trials_gc[:, :, 1] / (2 * np.pi * f_gc[None, :])
    cap2_gc = trials_gc[:, :, 2] / (2 * np.pi * f_gc[None, :])

    cap1_sp = trials_sp[:, :, 1]
    cap2_sp = trials_sp[:, :, 3]

    mm_gc = 200 * (cap1_gc - cap2_gc) / (cap1_gc + cap2_gc)
    mm_sp = 200 * (cap1_sp - cap2_sp) / (cap1_sp + cap2_sp)

    mean_mm_gc = np.mean(mm_gc, axis=0)
    std_mm_gc = np.std(mm_gc, axis=0)

    mean_mm_sp = np.mean(mm_sp, axis=0)
    std_mm_sp = np.std(mm_sp, axis=0)

    fig = plt.figure(figsize=(10, 8))
    ax = plt.subplot(111)
    plt.suptitle(f"sg13g2_hv_svaricap — AC MC mismatch ({corner.upper()} corner)", fontsize=14)

    ax.semilogx(f_gc, mean_mm_gc, "-", color="blue", linewidth=2, label="Gnucap mean")
    ax.fill_between(f_gc, mean_mm_gc - std_mm_gc, mean_mm_gc + std_mm_gc, color="blue", alpha=0.2,
        label=r"Gnucap $\pm 1\sigma$",
    )
    ax.semilogx(f_sp, mean_mm_sp, "--", color="orange", linewidth=2, label="Ngspice mean")
    ax.fill_between(f_sp, mean_mm_sp - std_mm_sp, mean_mm_sp + std_mm_sp, color="orange", alpha=0.2,
        label=r"Ngspice $\pm 1\sigma$",
    )

    ax.set_xlabel("Frequency [Hz]", fontsize=12)
    ax.set_ylabel(r"Capacitance mismatch $2(C_1 - C_2) /(C_1 + C_2)$ [%]", fontsize=12)
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)

    plt.savefig(svaricaphv_fig_dir / (test_name + ".png"), dpi=300)

    if show:
        plt.show()

    plt.close(fig)

def main():

    for corner in ["tt", "ss", "ff", "sf", "fs"]:
        plot_test_svaricaphv_tran(corner)
        plot_test_svaricaphv_ac(corner)
        plot_test_svaricaphv_mc_mm_ac(corner)

    plot_test_svaricaphv_mc_stat_ac()

    print("Finished plotting svaricaphv!")

if __name__ == "__main__":

    main()
