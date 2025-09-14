# IHP GDSFactory PDK 0.0.6

This repository contains a PDK (Process Design Kit) for the IHP CMOS technology, built using GDSFactory. It includes standard cell libraries, design rules, and example designs to facilitate the development of integrated circuits using this technology.

One of the advantages of using GDSFactory for PDK development is its modular and flexible approach to layout design. GDSFactory allows for easy creation and manipulation of layout components, making it straightforward to build and customize standard cells and other layout elements.

Advantages of using GDSFactory for PDK development:

- Programmatic layout generation: GDSFactory enables the creation of layout components using Python code, allowing for automation and easy modifications.
- Team collaboration: GDSFactory's code-based approach facilitates version control and collaboration among team members.
- Reproducibility: Designs can be easily reproduced and shared, ensuring that others can replicate the results.
- Modular design: Layout components can be reused and combined to create complex designs, promoting consistency and reducing errors.

## Installation

We recommend `uv`

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation for users

Use python 3.11, 3.12 or 3.13. We recommend [VSCode](https://code.visualstudio.com/) as an IDE.

```
uv pip install ihp-gdfactory --upgrade
```

Then you need to restart Klayout to make sure the new technology installed appears.

### Installation for contributors


Then you can install with:

```bash
git clone https://github.com/gdsfactory/ihp.git
cd ubc
uv venv --python 3.12
uv sync --extra docs --extra dev
```

## Documentation

- [gdsfactory docs](https://gdsfactory.github.io/gdsfactory/)
- [IHP docs](https://gdsfactory.github.io/ihp/) and [code](https://github.com/gdsfactory/ihp)
