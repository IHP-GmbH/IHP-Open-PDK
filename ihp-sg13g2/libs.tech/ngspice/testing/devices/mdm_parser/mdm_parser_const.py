import re

DESIGN_PARAMETERS = frozenset(
    {"W", "L", "NF", "M", "AD", "AS", "PD", "PS", "TEMP", "MASTER_SETUP_TYPE"}
)

UNIT_REGEX = re.compile(
    r"^(?P<num>[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)(?P<unit>[unpmkfµ]?)$"
)

UNIT_MULTIPLIERS = {
    "f": 1e-15,
    "p": 1e-12,
    "n": 1e-9,
    "µ": 1e-6,
    "u": 1e-6,
    "m": 1e-3,
    "k": 1e3,
}
