# Gnucap support files

These Verilog-A files were converted from the Xyce SPICE files using [SpiceArmyKnife.jl](https://github.com/NyanCAD/SpiceArmyKnife.jl)

## Usage

- Install [gnucap](https://codeberg.org/gnucap/gnucap)
- Install [gnucap-modelgen-verilog](https://codeberg.org/gnucap/gnucap-modelgen-verilog)
- Run `make -j$(nproc)`
- run `gnucap example.gc`

## Development

- Install [Julia](https://julialang.org/)
- run `julia`
- press `]` to access the package shell
- run `app add https://github.com/NyanCAD/SpiceArmyKnife.jl:SpiceArmyKnife.jl`
- add `~/.julia/bin` to your `PATH`
- run `make distclean && make -j$(nproc)` to regenerate the Verilog-A files