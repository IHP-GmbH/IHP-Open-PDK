"""Module with common fixtures."""
# pylint: disable=redefined-outer-name
import pathlib
import re
import subprocess
from typing import cast
import pytest

RULE_REGEX = r"Rule (?P<rule>(\w|\.)+): (?P<issues>\d+) error\(s\)"

@pytest.fixture(scope="module")
def sg13g2_drc_maximal(drc_test_name, drc_test_flags):
    """Returns a dict of rule name and number of violations."""
    cur_dir = pathlib.Path().resolve() / "ihp-sg13g2/libs.tech/klayout/tech/"
    cmd = f"klayout -n sg13g2 -b -r {cur_dir}/drc/sg13g2_maximal.lydrc " \
          f"-rd cell=sg13g2_test_{drc_test_name} " \
          f"{cur_dir}/drc/tests/{drc_test_name}/sg13g2_test_{drc_test_name}.gds.gz"
    if not drc_test_flags.get('density', True):
        cmd += " -rd density=false"
    result = subprocess.run(cmd, shell=True, capture_output=True, check=True)

    pattern = re.compile(RULE_REGEX)
    matches = (pattern.match(r) for r in result.stdout.decode('utf-8').split('\n'))
    matches_ = (cast(re.Match, x) for x in matches if x is not None)
    return {x.groupdict()['rule']: int(x.groupdict()['issues']) for x in matches_}


@pytest.fixture(scope="module")
def sg13g2_drc_maximal_failed_tests(sg13g2_drc_maximal):
    """Returns a list of all failed checks."""
    return [k for k,v in sg13g2_drc_maximal.items() if v > 0]
