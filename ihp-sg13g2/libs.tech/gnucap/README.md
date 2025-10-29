# Gnucap support files

These Verilog-A files were converted from the Xyce SPICE files using [SpiceArmyKnife.jl](https://github.com/NyanCAD/SpiceArmyKnife.jl)

## Usage

- Install [gnucap](https://codeberg.org/gnucap/gnucap)
- Install [gnucap-modelgen-verilog](https://codeberg.org/gnucap/gnucap-modelgen-verilog)
- Run `make -j$(nproc)`
- run `gnucap example.gc`

## Development

To regenerate the Verilog-A files from the Xyce SPICE files:

- Install [Julia](https://julialang.org/)
- run `julia`
- press `]` to access the package shell
- run `app add https://github.com/NyanCAD/SpiceArmyKnife.jl:SpiceArmyKnife.jl`
- add `~/.julia/bin` to your `PATH`
- run `make distclean && make -j$(nproc) REGENERATE_VA=1` to regenerate the Verilog-A files

Note: Regular builds with `make` will use the existing `.va` files in the repository. Only use `REGENERATE_VA=1` when you need to regenerate them from the `.lib` files.