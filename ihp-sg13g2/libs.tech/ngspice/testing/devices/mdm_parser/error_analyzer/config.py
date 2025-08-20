from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Tolerance:
    """Inflate/deflate the envelope: lo' = lo - abs - rel*|lo|, hi' = hi + abs + rel*|hi|."""

    abs: float = 0.0  # absolute tolerance
    rel: float = 0.0  # relative (fraction of magnitude), e.g. 0.02 for 2%


@dataclass
class Threshold:
    """Pass/fail rule for each group. Use count OR percent (or both)."""

    max_out_of_range_count: Optional[int] = None
    max_out_of_range_percent: Optional[float] = None

    def check(self, n_oob: int, n_total: int) -> bool:
        ok = True
        if self.max_out_of_range_percent is not None and n_total > 0:
            ok &= 100.0 * n_oob / n_total <= self.max_out_of_range_percent
        elif self.max_out_of_range_count is not None:
            ok &= n_oob <= self.max_out_of_range_count
        return ok


@dataclass
class MetricSpec:
    """
    Defines how to find measured/typical/envelope for ONE metric.

    Provide either (ss, ff) OR (lower, upper). All names are DataFrame column names.

    Examples:
      MetricSpec(name="id", meas="id_meas", tt="id_sim_mos_tt", ss="id_sim_mos_ss", ff="id_sim_mos_ff")
      MetricSpec(name="cgg", meas="cgg_meas", lower="cgg_spec_min", upper="cgg_spec_max")
      MetricSpec(name="gm", tt="gm_tt", ss="gm_ss", ff="gm_ff")  # no measured comparison
    """

    name: str
    meas: Optional[str] = None
    tt: Optional[str] = None
    ss: Optional[str] = None
    ff: Optional[str] = None
    tolerance: Tolerance = field(default_factory=Tolerance)
