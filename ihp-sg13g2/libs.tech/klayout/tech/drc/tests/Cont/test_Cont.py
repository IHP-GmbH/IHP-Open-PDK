"""Module to test specific layout rules."""
# pylint: disable=invalid-name, missing-function-docstring,redefined-outer-name
import pytest


@pytest.fixture(scope="module")
def drc_test_name():
    return "Cont"


@pytest.fixture(scope="module")
def drc_test_flags():
    return {'density': False}


testdata = [
    ("Cnt.a", 2),
    ("Cnt.b", 1),
    ("Cnt.c", 2),
    ("Cnt.g1", 0),  # should be 1 but rule doesn't work
    ("Cnt.g2", 1),
    ("Cnt.f", 1),
    ("Cnt.g", 1),
    ("Cnt.h", 1),
    ("Cnt.j", 1),
    ("M1.c", 1),
    ("M1.c1", 1),
]

@pytest.fixture(scope="module")
def get_valid_tests():
    return [t for t, _ in testdata]


@pytest.mark.parametrize("rule,value", testdata)
def test_rule_Cnt(rule, value, sg13g2_drc_maximal):
    print(f"Test Rule {rule}")
    assert sg13g2_drc_maximal[rule] == value

def test_invalid_issues_Cnt(sg13g2_drc_maximal_failed_tests, get_valid_tests):
    print(get_valid_tests)
    print(sg13g2_drc_maximal_failed_tests)
    invalid_issues = set(sg13g2_drc_maximal_failed_tests) - set(get_valid_tests)
    assert len(invalid_issues) == 0
