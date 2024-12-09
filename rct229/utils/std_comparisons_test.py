import operator
import pytest

from rct229.schema.config import ureg
from rct229.utils.compare_standard_val import (
    compare_standard_val,
    compare_standard_val_strict,
)
from rct229.utils.std_comparisons import (
    std_equal,
    std_equal_with_precision,
    std_conservative_outcome,
)

_M2 = ureg("m2")


def test__std_equal__true_with_units():
    assert std_equal(1.01 * _M2, 1.0101 * _M2, 0.05)


def test__std_equal__true_without_units():
    assert std_equal(1.01, 1.0101)


def test__std_equal__false_with_units():
    assert not std_equal(1.01 * _M2, 1.02 * _M2)


def test__std_equal__false_without_units():
    assert not std_equal(1.01, 1.011, 0.05)


def test__compare_standard_val_le__true_with_units():
    # case less equal -> equal
    assert compare_standard_val(
        val=1.0101 * _M2,
        std_val=1.0101 * _M2,
        operator=operator.le,
    )


def test__compare_standard_val_le__true_with_units_tolerance():
    # case less equal -> greater within tolerance
    assert compare_standard_val(
        val=1.0102 * _M2,
        std_val=1.0101 * _M2,
        operator=operator.le,
    )


def test__compare_standard_val_lt_true_with_units():
    # case less than -> less
    assert compare_standard_val(
        val=0.9 * _M2, std_val=1.0101 * _M2, operator=operator.lt
    )


def test__compare_standard_val_lt_true_with_units_tolerance():
    # case less than -> greater within tolerance
    assert compare_standard_val(
        val=1.0102 * _M2, std_val=1.0101 * _M2, operator=operator.lt
    )


def test__compare_standard_val_ge_true_with_units():
    # case greater equal -> equal
    assert compare_standard_val(
        val=1.0101 * _M2, std_val=1.0101 * _M2, operator=operator.ge
    )


def test__compare_standard_val_ge_true_with_units_tolerance():
    # case greater equal -> lesser within tolerance
    assert compare_standard_val(
        val=1.01 * _M2, std_val=1.0101 * _M2, operator=operator.ge
    )


def test__compare_standard_val_gt_true_with_units():
    # case greater equal -> greater
    assert compare_standard_val(
        val=1.1 * _M2, std_val=1.0101 * _M2, operator=operator.ge
    )


def test__compare_standard_val_gt_true_with_units_tolerance():
    # case greater equal -> lesser within tolerance
    assert compare_standard_val(
        val=1.01 * _M2, std_val=1.0101 * _M2, operator=operator.ge
    )


def test__compare_standard_val_strict_le__true_with_units():
    # case less equal strict -> equal
    assert compare_standard_val_strict(
        val=1.0101 * _M2,
        std_val=1.0101 * _M2,
        operator=operator.le,
    )


def test__compare_standard_val_strict_le__false_with_units():
    # case less equal strict -> greater within tolerance (fail due to strict)
    assert not compare_standard_val_strict(
        val=1.0102 * _M2,
        std_val=1.0101 * _M2,
        operator=operator.le,
    )


def test__compare_standard_val_strict_lt__true_with_units():
    # case less than strict -> less
    assert compare_standard_val_strict(
        val=1.010 * _M2, std_val=1.0101 * _M2, operator=operator.lt
    )


def test__compare_standard_val_strict_lt__false_with_units():
    # case less than strict -> equal within tolerance (fail)
    assert not compare_standard_val_strict(
        val=1.0101 * _M2,
        std_val=1.0101 * _M2,
        operator=operator.lt,
    )


def test__compare_standard_val_strict_ge__true_with_units():
    # case great equal strict -> equal
    assert compare_standard_val_strict(
        val=1.0101 * _M2,
        std_val=1.0101 * _M2,
        operator=operator.ge,
    )


def test__compare_standard_val_strict_ge__false_with_units():
    # case greater equal strict -> lesser within tolerance (fail)
    assert not compare_standard_val_strict(
        val=1.01 * _M2, std_val=1.0101 * _M2, operator=operator.ge
    )


def test__compare_standard_val_strict_gt__true_with_units():
    # case greater than strict -> greater
    assert compare_standard_val_strict(
        val=1.02 * _M2, std_val=1.0101 * _M2, operator=operator.gt
    )


def test__compare_standard_val_strict_gt__false_with_units():
    # case greater than strict -> equals within tolerance (fail)
    assert not compare_standard_val_strict(
        val=1.0101 * _M2,
        std_val=1.0101 * _M2,
        operator=operator.gt,
    )


def test__std_equal_with_precision__false_types_vary():
    with pytest.raises(TypeError):
        std_equal_with_precision(1.05 * _M2, 1.1, 0.1)


def test__std_equal_with_precision__true_with_units():
    assert std_equal_with_precision(1.05 * _M2, 1.1 * _M2, 0.1 * _M2)


def test__std_equal_with_precision__true_without_units():
    assert std_equal_with_precision(1.05, 1.1, 0.1)


def test__std_equal_with_precision__false_with_units():
    assert not std_equal_with_precision(1.15 * _M2, 1.1 * _M2, 0.1 * _M2)


def test__std_equal_with_precision__false_without_units():
    assert not std_equal_with_precision(1.15, 1.1, 0.1)


def test__std_equal_with_precision__10_true_with_units():
    assert std_equal_with_precision(145 * _M2, 150 * _M2, 10 * _M2)


def test__std_equal_with_precision__10_true_without_units():
    assert std_equal_with_precision(145, 150, 10)


def test__std_equal_with_precision__10_false_with_units():
    assert not std_equal_with_precision(155 * _M2, 150 * _M2, 10 * _M2)


def test__std_equal_with_precision__10_false_without_units():
    assert not std_equal_with_precision(155, 150, 10)


def test__std_conservative_outcome__true_with_units_gt():
    assert std_conservative_outcome(1.1 * _M2, 1.05 * _M2, operator.gt)


def test__std_conservative_outcome__true_with_units_lt():
    assert std_conservative_outcome(1.05 * _M2, 1.1 * _M2, operator.lt)


def test__std_conservative_outcome__false_with_units_gt():
    assert not std_conservative_outcome(1.09999 * _M2, 1.1 * _M2, operator.gt)


def test__std_conservative_outcome__false_with_units_lt():
    assert not std_conservative_outcome(1.05001 * _M2, 1.05 * _M2, operator.lt)


def test__std_conservative_outcome__true_without_units_gt():
    assert std_conservative_outcome(1.1, 1.05, operator.gt)


def test__std_conservative_outcome__true_without_units_lt():
    assert std_conservative_outcome(1.05, 1.1, operator.lt)


def test__std_conservative_outcome__false_without_units_gt():
    assert not std_conservative_outcome(1.09999, 1.1, operator.gt)


def test__std_conservative_outcome__false_without_units_lt():
    assert not std_conservative_outcome(1.05001, 1.05, operator.lt)
