"""Description: Test netlists for all cells in the PDK."""

from __future__ import annotations

import pathlib

import gdsfactory as gf
import jsondiff
import numpy as np
import pytest
from gdsfactory.difftest import difftest
from pytest_regressions.data_regression import DataRegressionFixture
from pytest_regressions.ndarrays_regression import NDArraysRegressionFixture

from ihp import PDK


@pytest.fixture(autouse=True)
def activate_pdk() -> None:
    """Activate PDK."""
    PDK.activate()


cells = PDK.cells
skip_test = {
    "wire_corner",
    "die",
    "pack_doe",
    "pack_doe_grid",
    "import_gds",
    "nmos_hv",
    "pmos_hv",
    "rfpmos",
    "rfnmos",
    "svaricap",
    "SVaricap",
}


cell_names = cells.keys() - skip_test
cell_names = [name for name in cell_names if not name.startswith("_")]
dirpath = pathlib.Path(__file__).absolute().with_suffix(".gds").parent / "gds_ref_si220"
dirpath.mkdir(exist_ok=True, parents=True)


def get_minimal_netlist(comp: gf.Component):
    """Get minimal netlist from a component."""
    net = comp.get_netlist()

    def _get_instance(inst):
        return {
            "component": inst["component"],
            "settings": inst["settings"],
        }

    return {"instances": {i: _get_instance(c) for i, c in net["instances"].items()}}


def instances_without_info(net):
    """Get instances without info."""
    return {
        k: {
            "component": v.get("component", ""),
            "settings": v.get("settings", {}),
        }
        for k, v in net.get("instances", {}).items()
    }


@pytest.mark.parametrize("name", cell_names)
def test_cell_in_pdk(name):
    """Test that cell is in the PDK."""
    c1 = gf.Component()
    c1.add_ref(gf.get_component(name))
    net1 = get_minimal_netlist(c1)

    c2 = gf.read.from_yaml(net1)
    net2 = get_minimal_netlist(c2)

    instances1 = instances_without_info(net1)
    instances2 = instances_without_info(net2)
    assert instances1 == instances2


@pytest.mark.parametrize("component_name", cell_names)
def test_gds(component_name: str) -> None:
    """Avoid regressions in GDS geometry shapes and layers."""
    component = cells[component_name]()
    difftest(component, test_name=component_name, dirpath=dirpath)


@pytest.mark.parametrize("component_name", cell_names)
def test_settings(component_name: str, data_regression: DataRegressionFixture) -> None:
    """Avoid regressions when exporting settings."""
    component = cells[component_name]()
    data_regression.check(component.to_dict())


skip_test_models = {}


models = PDK.models
model_names = sorted(
    [
        name
        for name in set(models.keys()) - set(skip_test_models)
        if not name.startswith("_")
    ]
)


@pytest.mark.parametrize("model_name", model_names)
def test_models_with_wavelength_sweep(
    model_name: str, ndarrays_regression: NDArraysRegressionFixture
) -> None:
    """Test models with different wavelengths to avoid regressions in frequency response."""
    # Test at different wavelengths
    wl = [1.53, 1.55, 1.57]
    try:
        model = models[model_name]
        s_params = model(wl=wl)
    except TypeError:
        pytest.skip(f"{model_name} does not accept a wl argument")

    # Convert s_params dictionary to arrays for regression testing
    # s_params is a dict with tuple keys (port pairs) and JAX array values
    arrays_to_check = {}
    for key, value in sorted(s_params.items()):
        # Convert tuple key to string for regression test compatibility
        key_str = f"s_{key[0]}_{key[1]}"
        # Convert JAX arrays to numpy and separate real/imag parts

        value_np = np.array(value)
        arrays_to_check[f"{key_str}_real"] = np.real(value_np)
        arrays_to_check[f"{key_str}_imag"] = np.imag(value_np)

    ndarrays_regression.check(
        arrays_to_check,
        default_tolerance={"atol": 1e-2, "rtol": 1e-2},
    )


if __name__ == "__main__":
    component_type = "coupler_symmetric"
    c = cells[component_type]()
    n = c.get_netlist()
    n.pop("connections", None)
    print(n)
    c2 = gf.read.from_yaml(n)
    n2 = c2.get_netlist()
    d = jsondiff.diff(n, n2)
    assert len(d) == 0, d
