import io
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dirs import tests_dir_gc, tests_dir_sp, fig_dir
from parse import filter_data

moscap_fig_dir = fig_dir / "moscap"
moscap_fig_dir.mkdir(parents=True, exist_ok=True)

ref_dir_gc = tests_dir_gc / "moscap" / "ref"
ref_dir_sp = tests_dir_sp / "moscap" / "ref"
assert ref_dir_gc.exists()
assert ref_dir_sp.exists()

def plot_test_moscap_nmos_tran(show=False):

    test_name = "test_moscap_nmos_tran"

    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data = filter_data(filepath_gc, "open circuit")
    data_gc = pd.read_csv(io.StringIO(data), sep=r'\s+', comment="#", engine='python').values

    filepath_sp = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values

    t_gc = data_gc[:, 0] / 1e-9
    vg_gc = data_gc[:, 1]
    iv1_gc = data_gc[:, 2] * 1e9

    t_sp = data_sp[:, 0] / 1e-9
    vp_sp = data_sp[:, 1]
    iv1_sp = data_sp[:, 2] * 1e9

    fig = plt.figure(figsize=(10, 8))
    gs = plt.GridSpec(2, 1, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)

    plt.suptitle("NMOS Capacitor transient ramp (raw data)", fontsize=14)

    l1, = ax0.plot(t_gc, vg_gc, '-', color='r', linewidth=2, label='Gnucap')
    l2, = ax0.plot(t_sp, vp_sp, '--', color='k', linewidth=1.5, label='Ngspice')
    ax0.set_ylabel('Gate Voltage [V]', fontsize=12)
    ax0.legend()
    ax0.grid(True, alpha=0.3)

    l3, = ax1.plot(t_gc[::11], iv1_gc[::11], '-', color='r', marker = 'o', markersize = 1, linewidth=2, label='Gnucap')
    l4, = ax1.plot(t_sp, iv1_sp, '--', color='k', linewidth=1.5, label='Ngspice')
    ax1.set_xlabel('Time [ns]', fontsize=12)
    ax1.set_ylabel('i(tb.V1) [nA]', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)


    plt.savefig(moscap_fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()

def plot_test_moscap_pmos_tran(show=False):

    test_name = "test_moscap_pmos_tran"

    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    data = filter_data(filepath_gc, ("print", "^"))
    data_gc = pd.read_csv(io.StringIO(data), sep=r'\s+', comment="#", engine='python').values

    filepath_sp = ref_dir_sp / (test_name + ".sp.out")
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values

    t_gc = data_gc[:, 0] / 1e-9
    vg_gc = data_gc[:, 1]
    iv1_gc = data_gc[:, 2] * 1e9

    t_sp = data_sp[:, 0] / 1e-9
    vm_sp = data_sp[:, 1]
    iv1_sp = data_sp[:, 2] * 1e9

    fig = plt.figure(figsize=(10, 8))
    gs = plt.GridSpec(2, 1, hspace=0.3)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1], sharex=ax0)

    plt.suptitle("PMOS Capacitor transient ramp (raw data)", fontsize=14)

    l1, = ax0.plot(t_gc, vg_gc, '-', color='r', linewidth=2, label='Gnucap')
    l2, = ax0.plot(t_sp, vm_sp, '--', color='k', linewidth=1.5, label='Ngspice)')
    ax0.set_ylabel('Gate Voltage [V]', fontsize=12)
    ax0.legend()
    ax0.grid(True, alpha=0.3)

    l3, = ax1.plot(t_gc[::11], iv1_gc[::11], '-', color='r', marker = 'o', markersize = 1, linewidth=2, label='Gnucap')
    l4, = ax1.plot(t_sp, iv1_sp, '--', color='k', linewidth=1.5, label='Ngspice')
    ax1.set_xlabel('Time [ns]', fontsize=12)
    ax1.set_ylabel('i(tb.V1) [nA]', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    plt.savefig(moscap_fig_dir / (test_name + '.png'), dpi=300)

    if show:
        plt.show()

    plt.close()

def _parse_gc_capacitance(filepath, names=("Cn", "Cp")):

    pattern = re.compile(r"\b(" + "|".join(names) + r")=\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)")
    vals = []
    with open(filepath, "r") as f:
        for line in f:
            m = pattern.search(line)
            if m is None:
                continue
            try:
                v = float(m.group(2))
            except ValueError:
                continue
            if np.isfinite(v):
                vals.append(v)

    return np.array(vals) if vals else None


def plot_test_moscap_mc(test_name, device, ref_dir_gc, ref_dir_sp, fig_dir, show=False):

    filepath_gc = ref_dir_gc / (test_name + ".gc.out")
    filepath_sp = ref_dir_sp / (test_name + ".sp.out")

    c_gc = _parse_gc_capacitance(filepath_gc)
    data_sp = pd.read_csv(filepath_sp, sep=r'\s+').values
    c_sp = data_sp[:, 1]

    is_mm = test_name.endswith("_mc_mm")
    title_kind = "mismatch" if is_mm else "statistic"

    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot(111)
    ax.set_title(f"{device} moscap MC {title_kind}", fontsize=14)

    if c_gc is not None and c_gc.size > 0:
        m_gc = float(np.mean(c_gc))
        s_gc = float(np.std(c_gc))
        ax.hist(c_gc, bins=50, density=True, alpha=0.5, label="Gnucap", color="blue")
        ax.axvline(m_gc, color="blue", linestyle="--", linewidth=1, label=f"Gnucap Mean={m_gc:.5e}")
        ax.axvline(m_gc + s_gc, color="blue", linestyle=":", linewidth=1, label=f"Gnucap STD={s_gc:.5e}")
        ax.axvline(m_gc - s_gc, color="blue", linestyle=":", linewidth=1)

    m_sp = float(np.mean(c_sp))
    s_sp = float(np.std(c_sp))
    ax.hist(c_sp, bins=50, density=True, alpha=0.5, label="Ngspice C1", color="orange")
    ax.axvline(m_sp, color="orange", linestyle="--", linewidth=1, label=f"Ngspice C1 Mean={m_sp:.5e}")
    ax.axvline(m_sp + s_sp, color="orange", linestyle=":", linewidth=1, label=f"Ngspice C1 STD={s_sp:.5e}")
    ax.axvline(m_sp - s_sp, color="orange", linestyle=":", linewidth=1)

    ax.set_xlabel("Capacitance [F]", fontsize=14)
    ax.set_ylabel("Probability Density", fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig(fig_dir / (test_name + ".png"), dpi=300)

    if show:
        plt.show()

    plt.close()


def plot_test_moscap_nmos_mc_mm(show=False):

    plot_test_moscap_mc(
        "test_moscap_nmos_mc_mm",
        "NMOS",
        ref_dir_gc,
        ref_dir_sp,
        moscap_fig_dir,
        show=show,
    )


def plot_test_moscap_pmos_mc_mm(show=False):

    plot_test_moscap_mc(
        "test_moscap_pmos_mc_mm",
        "PMOS",
        ref_dir_gc,
        ref_dir_sp,
        moscap_fig_dir,
        show=show,
    )


def plot_test_moscap_nmos_mc_stat(show=False):

    plot_test_moscap_mc(
        "test_moscap_nmos_mc_stat",
        "NMOS",
        ref_dir_gc,
        ref_dir_sp,
        moscap_fig_dir,
        show=show,
    )


def plot_test_moscap_pmos_mc_stat(show=False):

    plot_test_moscap_mc(
        "test_moscap_pmos_mc_stat",
        "PMOS",
        ref_dir_gc,
        ref_dir_sp,
        moscap_fig_dir,
        show=show,
    )


def main():

    plot_test_moscap_nmos_tran()
    plot_test_moscap_pmos_tran()
    plot_test_moscap_nmos_mc_stat()
    plot_test_moscap_pmos_mc_stat()
    plot_test_moscap_nmos_mc_mm()
    plot_test_moscap_pmos_mc_mm()


if __name__ == "__main__":

    main()
