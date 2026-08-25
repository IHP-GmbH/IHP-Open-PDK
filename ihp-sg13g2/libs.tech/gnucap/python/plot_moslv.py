from plot_mos import *
from dirs import tests_dir_gc, tests_dir_sp, fig_dir

moslv_fig_dir = fig_dir / "moslv"
moslv_fig_dir.mkdir(parents=True, exist_ok=True)

ref_dir_gc = tests_dir_gc / "moslv" / "ref"
ref_dir_sp = tests_dir_sp / "moslv" / "ref"
assert ref_dir_gc.exists()
assert ref_dir_sp.exists()

def plot_tb_moslv_nmos_id_vd_ng(ng: int, rfmode: bool = False):

    test_name = f"tb_moslv_nmos_id_vd_ng{ng}"
    if rfmode: test_name += "_rf"

    plot_tb_mos_id_vd(
        test_name,
        f"id-vd curves sg13g2_lv_nmos_psp ng={ng}",
        ref_dir_gc,
        ref_dir_sp,
        moslv_fig_dir,
    )

def plot_tb_moslv_pmos_id_vd_ng(ng: int, rfmode: bool = False):

    test_name = f"tb_moslv_pmos_id_vd_ng{ng}"
    if rfmode == 1: test_name += "_rf"

    plot_tb_mos_id_vd(
        f"tb_moslv_pmos_id_vd_ng{ng}",
        f"id-vd curves sg13g2_lv_pmos_psp ng={ng}",
        ref_dir_gc,
        ref_dir_sp,
        moslv_fig_dir
    )

def plot_moslv_inv_corner(corner, rfmode: bool = False, show = False):

    test_name = f"tb_moslv_inv_{corner}"
    if rfmode: test_name + "_rf"

    plot_mos_inv(
        test_name,
        f"moslv CMOS inverter {corner}",
        ref_dir_gc,
        ref_dir_sp,
        moslv_fig_dir,
        show=show
    )
def plot_moslv_inv_all_corners(show=False):

    plot_mos_inv_all_corners(
        ref_dir_gc,
        moslv_fig_dir,
        'tb_moslv_inv_all_corners',
        show=show)

def plot_moslv_mc_stats(test_name, rf_mode = False, show=False):

    if rf_mode: test_name += "_rf"

    plot_mos_mc_stats(test_name, ref_dir_gc, ref_dir_sp, moslv_fig_dir, show=show)

def plot_moslv_mc_mm(corner, rfmode = False, plot_sp=True, show = False):

    test_name = f"tb_moslv_mc_mm_{corner}"
    if rfmode: test_name += "_rf"

    plot_mos_mc_mm(
        test_name,
        ref_dir_gc,
        ref_dir_sp,
        moslv_fig_dir,
        plot_sp=plot_sp,
        show=show
    )

def main():

    for ng in range(1, 5):
        plot_tb_moslv_nmos_id_vd_ng(ng, rfmode=False)
        plot_tb_moslv_nmos_id_vd_ng(ng, rfmode=True)
        plot_tb_moslv_pmos_id_vd_ng(ng, rfmode=False)
        plot_tb_moslv_pmos_id_vd_ng(ng, rfmode=True)

    for corner in ['tt', 'ss', 'ff', 'sf', 'fs']:
        plot_moslv_inv_corner(corner, rfmode=False)
        plot_moslv_inv_corner(corner, rfmode=True)
        plot_moslv_mc_mm(corner, rfmode=False)
        plot_moslv_mc_mm(corner, rfmode=True)

    plot_moslv_mc_stats('tb_moslv_mc_stat', rf_mode=False)
    plot_moslv_mc_stats('tb_moslv_mc_stat', rf_mode=True)

    print("Finished plotting moslv!")

if __name__ == "__main__":

    main()


