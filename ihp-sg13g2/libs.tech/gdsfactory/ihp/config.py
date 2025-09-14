"""Loads a default_config from this file.

Can overwrite config with an optional `config.yml` file in the current working directory.
"""

import pathlib


cwd = pathlib.Path.cwd()
cwd_config = cwd / "config.yml"
module = pathlib.Path(__file__).parent.absolute()
repo = module.parent


class Path:
    module = module
    repo = repo
    cells = module / "cells"
    samples = module / "samples"
    data = samples / "data"
    gds = module / "gds"

    lyp = module / "klayout" / "tech" / "layers.lyp"
    lyt = module / "klayout" / "tech" / "tech.lyt"
    layers_yaml = module / "layers.yaml"
    tech = module / "klayout" / "tech"


PATH = Path()
__all__ = ["PATH"]
