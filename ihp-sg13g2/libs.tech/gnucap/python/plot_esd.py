from io import StringIO

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dirs import tests_dir_gc, tests_dir_sp, fig_dir
from parse import split_nested_sweep, filter_data
from util import pointwise_rel_err

diode_fig_dir = fig_dir / "esd"
diode_fig_dir.mkdir(parents=True, exist_ok=True)

ref_dir_gc = tests_dir_gc / "esd" / "ref"
ref_dir_sp = tests_dir_sp / "esd" / "ref"
assert ref_dir_gc.exists()
assert ref_dir_sp.exists()

def plot_test_dio_esd_diodes(show: bool = False) -> None:

    test_name = "test_esd_diodes_dc"

    ref_dir_gc_esd = tests_dir_gc / "esd" / "ref"
    ref_dir_sp_dio = tests_dir_sp / "esd" / "ref"

    filepath_gc = ref_dir_gc_esd / (test_name + ".gc.out")
    filepath_sp = ref_dir_sp_dio / (test_name + ".sp.out")

    data_gc_str = filter_data(filepath_gc,
("#", "parameter", "iterations", "transient", "nodes", "dctran", "Gnucap")
    )

    data_gc = pd.read_csv(StringIO(data_gc_str), sep=r"\s+", header=None, engine="python").values
    data_sp = pd.read_csv(filepath_sp, sep=r"\s+", engine="python").values

    vin_gc = data_gc[:, 0]
    m_gc = data_gc[:, 1:9]
    vin_sp = data_sp[:, 0]
    m_sp = data_sp[:, 2:10]

    n = min(vin_gc.shape[0], vin_sp.shape[0])
    vin_gc = vin_gc[:n]
    m_gc = m_gc[:n]
    vin_sp = vin_sp[:n]
    m_sp = m_sp[:n]
    assert np.allclose(vin_gc, vin_sp)

    diodes = [
        ("diodevdd_2kv", 0, 1),
        ("diodevdd_4kv", 2, 3),
        ("diodevss_2kv", 4, 5),
        ("diodevss_4kv", 6, 7),
    ]

    fig = plt.figure(figsize=(16, 12))
    gs = plt.GridSpec(4, 4, hspace=0.45, wspace=0.3)
    axes_pad_iv = [plt.subplot(gs[0, c]) for c in range(4)]
    axes_pad_err = [plt.subplot(gs[1, c], sharex=axes_pad_iv[c]) for c in range(4)]
    axes_rail_iv = [plt.subplot(gs[2, c], sharex=axes_pad_iv[c]) for c in range(4)]
    axes_rail_err = [plt.subplot(gs[3, c], sharex=axes_pad_iv[c]) for c in range(4)]

    plt.suptitle(
        "ESD clamp diodes I-V curves",
        fontsize=14,
    )

    for c, (name, pad_col, rail_col) in enumerate(diodes):

        axes_pad_iv[c].plot(vin_gc, m_gc[:, pad_col], "-", color="blue", linewidth=1.5, label="Gnucap")
        axes_pad_iv[c].plot(vin_sp, m_sp[:, pad_col], "--", color="orange", linewidth=1.0, label="Ngspice")
        axes_pad_iv[c].set_title(name, fontsize=14)
        axes_pad_iv[c].grid(True, alpha=0.3)
        if c == 0:
            axes_pad_iv[c].set_ylabel(r"$I_\mathrm{PAD}$ [A]", fontsize=14)
            axes_pad_iv[c].legend(fontsize=8)

        rel_err_pad = pointwise_rel_err(m_sp[:, pad_col], m_gc[:, pad_col], 1e-5)
        axes_pad_err[c].semilogy(vin_gc, rel_err_pad, "-", color="#4D4D4D", linewidth=1.0)
        axes_pad_err[c].grid(True, alpha=0.3)
        if c == 0:
            axes_pad_err[c].set_ylabel(r"$\varepsilon_{\mathrm{rel}}$", fontsize=14)

        axes_rail_iv[c].plot(vin_gc, m_gc[:, rail_col], "-", color="blue", linewidth=1.5)
        axes_rail_iv[c].plot(vin_sp, m_sp[:, rail_col], "--", color="orange", linewidth=1.0)
        axes_rail_iv[c].grid(True, alpha=0.3)
        if c == 0:
            axes_rail_iv[c].set_ylabel(r"$I_\mathrm{VSS}$ [A]", fontsize=14)

        rel_err_rail = pointwise_rel_err(m_sp[:, rail_col], m_gc[:, rail_col], 1e-5)
        axes_rail_err[c].semilogy(vin_gc, rel_err_rail, "-", color="#4D4D4D", linewidth=1.0)
        axes_rail_err[c].set_xlabel("V [V]", fontsize=14)
        axes_rail_err[c].grid(True, alpha=0.3)
        if c == 0:
            axes_rail_err[c].set_ylabel(r"$\varepsilon_{\mathrm{rel}}$", fontsize=14)

    plt.savefig(diode_fig_dir / (test_name + ".png"), dpi=300)

    if show:
        plt.show()

    plt.close()

def plot_test_esd_nmos_cl_dc(show: bool = False, rfmode: bool = False) -> None:

    if not rfmode:
        test_name = "test_esd_nmos_cl_dc"
    else:
        test_name = "test_esd_nmos_cl_dc_rf"

    ref_dir_gc_esd = tests_dir_gc / "esd" / "ref"
    ref_dir_sp_esd = tests_dir_sp / "esd" / "ref"

    filepath_gc = ref_dir_gc_esd / (test_name + ".gc.out")
    filepath_sp = ref_dir_sp_esd / (test_name + ".sp.out")

    data_gc_str = filter_data(
        filepath_gc, ("#", "iterations", "transient", "nodes", "dctran", "Gnucap")
    )

    data_gc = pd.read_csv(
        StringIO(data_gc_str), sep=r"\s+", header=None, engine="python"
    ).values

    data_sp = pd.read_csv(filepath_sp, sep=r"\s+", engine="python").values

    assert data_gc.shape[0] == data_sp.shape[0]

    ibias_gc = data_gc[:, 0] * 1e3
    vin1_gc = data_gc[:, 1]
    vin2_gc = data_gc[:, 2]

    ibias_sp = data_sp[:, 0] * 1e3
    vin1_sp = data_sp[:, 1]
    vin2_sp = data_sp[:, 2]

    fig = plt.figure(figsize=(12, 8))
    gs = plt.GridSpec(2, 2, hspace=0.35, wspace=0.3)
    axes_iv = [plt.subplot(gs[0, c]) for c in range(2)]
    axes_err = [plt.subplot(gs[1, c], sharex=axes_iv[c]) for c in range(2)]

    plt.suptitle(
        "ESD NMOS clamp I-V curves" if rfmode else "ESD NMOS (RF) clamp I-V curves",
        fontsize=14,
    )

    variants = [
        ("nmoscl_2", vin1_gc, vin1_sp, 1e-16),
        ("nmoscl_4", vin2_gc, vin2_sp, 1e-3),
    ]

    for c, (name, v_gc, v_sp, atol) in enumerate(variants):

        axes_iv[c].plot(ibias_gc, v_gc, "-", color="blue", linewidth=2, label="Gnucap")
        axes_iv[c].plot(ibias_sp, v_sp, "--", color="orange", linewidth=1.5, label="ngspice")
        axes_iv[c].set_title(name, fontsize=12)
        axes_iv[c].grid(True, alpha=0.3)
        axes_iv[c].set_xlabel("I(bias) [mA]", fontsize=12)
        if c == 0:
            axes_iv[c].set_ylabel("V(Vin) [V]", fontsize=12)
            axes_iv[c].legend()

        rel_err = pointwise_rel_err(v_sp, v_gc, atol)
        axes_err[c].semilogy(ibias_gc[::10], rel_err[::10], "-", color="#4D4D4D", linewidth=1.0)
        axes_err[c].set_xlabel("I(bias) [mA]", fontsize=12)
        axes_err[c].grid(True, alpha=0.3)
        if c == 0:
            axes_err[c].set_ylabel(r"$\varepsilon_{\mathrm{rel}}$", fontsize=12)

    plt.savefig(diode_fig_dir / (test_name + ".png"), dpi=300)

    if show:
        plt.show()

    plt.close()

def main():

    plot_test_dio_esd_diodes()
    plot_test_esd_nmos_cl_dc(rfmode=False)
    plot_test_esd_nmos_cl_dc(rfmode=True)

    print("Finished plotting esd!")

if __name__ == "__main__":

    main()
