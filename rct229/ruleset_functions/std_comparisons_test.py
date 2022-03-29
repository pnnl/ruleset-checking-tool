import pytest

from rct229.ruleset_functions.std_comparisons import std_equal
from rct229.schema.config import ureg

_M2 = ureg("m2")


def test__std_equal__true():
    assert std_equal(1.01 * _M2, 1.011 * _M2, "m2", 2)


def test__std_equal__false():
    assert not std_equal(1.01 * _M2, 1.011 * _M2, "m2", 3)
