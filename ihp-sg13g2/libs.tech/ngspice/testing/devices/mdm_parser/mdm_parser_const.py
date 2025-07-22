import re

# Design parameters to extract from ICCAP_VALUES
DESIGN_PARAMETERS = frozenset(
    {
        "W",
        "L",
        "NF",
        "M",
        "AD",
        "AS",
        "PD",
        "PS",
        "NRD",
        "NRS",
        "LDRIFT1",
        "LDRIFT2",
        "SA",
        "SB",
        "SD",
        "SCA",
        "SCB",
        "SCC",
        "SC",
        "TEMP",
    }
)

# Pre-compiled regex for better performance
UNIT_REGEX = re.compile(
    r"^(?P<num>[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)(?P<unit>[unpmkfµ]?)$"
)

# Unit multipliers
UNIT_MULTIPLIERS = {
    "f": 1e-15,
    "p": 1e-12,
    "n": 1e-9,
    "µ": 1e-6,
    "u": 1e-6,
    "m": 1e-3,
    "k": 1e3,
}
