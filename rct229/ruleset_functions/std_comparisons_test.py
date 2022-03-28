import pytest
from rct229.ruleset_functions.std_comparisons import std_equality
from rct229.schema.config import ureg

_M2 = ureg("m2")


def test__std_equality__true():
    assert std_equality(1.01 * _M2, 1.011 * _M2, "m2", 2)


def test__std_equality__false():
    assert not std_equality(1.01 * _M2, 1.011 * _M2, "m2", 3)
