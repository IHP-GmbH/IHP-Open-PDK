from pathlib import Path

libs_tech_dir = Path(__file__).parent.parent.parent

dir_gc = libs_tech_dir / "gnucap"
dir_sp = libs_tech_dir / "ngspice"

test_dir = dir_gc / "tests"

tests_dir_gc = test_dir / "gnucap"
tests_dir_sp = test_dir / "ngspice"

fig_dir = dir_gc / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)

assert dir_gc.exists()
assert dir_sp.exists()
assert tests_dir_gc.exists()
assert tests_dir_sp.exists()
