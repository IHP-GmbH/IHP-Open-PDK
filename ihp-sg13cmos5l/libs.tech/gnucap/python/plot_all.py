"""Plot the reference test data, for every test directory or a chosen few.

This is the only plotting entry point that should be run as a script. The
per-directory modules next to it are symlinks into the sibling ihp-sg13g2, and
Python sets sys.path[0] to the *resolved* directory of the script it runs, so
running one of them directly would import that PDK's dirs.py and write its
figures into ihp-sg13g2 instead of here. Importing them, as below, keeps
sys.path[0] on this tree.
"""

import sys

import plot_resistor
import plot_moslv
import plot_moshv

PLOTTERS = {
    "resistor": plot_resistor.main,
    "moslv": plot_moslv.main,
    "moshv": plot_moshv.main,
}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    selected = argv or list(PLOTTERS)

    unknown = [name for name in selected if name not in PLOTTERS]
    if unknown:
        print(f"unknown test directory: {', '.join(unknown)}", file=sys.stderr)
        print(f"available: {', '.join(PLOTTERS)}", file=sys.stderr)
        return 1

    for name in selected:
        PLOTTERS[name]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
