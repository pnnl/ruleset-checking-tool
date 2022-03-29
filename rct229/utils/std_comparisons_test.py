import pytest

from rct229.ruleset_functions.std_comparisons import std_equal
from rct229.schema.config import ureg

_M2 = ureg("m2")


def test__std_equal__true_with_units():
    assert std_equal(1.01 * _M2, 1.0101 * _M2, 0.05)


def test__std_equal__true_without_units():
    assert std_equal(1.01, 1.0101)


def test__std_equal__false_with_units():
    assert not std_equal(1.01 * _M2, 1.011 * _M2)


def test__std_equal__false_without_units():
    assert not std_equal(1.01, 1.011, 0.05)
