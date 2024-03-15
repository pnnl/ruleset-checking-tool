import operator

from rct229.schema.config import ureg
from rct229.utils.compare_standard_val import (
    compare_standard_val,
    compare_standard_val_strict,
)

_M2 = ureg("m2")


def test__compare_standard_val_stringent_compare_gt():
    assert compare_standard_val(1.5 * _M2, 1.0 * _M2, operator.gt)


def test__compare_standard_val_stringent_compare_lt():
    assert compare_standard_val(1.0 * _M2, 1.5 * _M2, operator.lt)


def test__compare_standard_val_stringent_compare_gt_equal():
    """test equal when ahj flat set to True"""
    assert compare_standard_val(0.9999 * _M2, 1.0 * _M2, operator.gt)


def test__compare_standard_val_non_stringent_code_compare():
    assert compare_standard_val(0.9999 * _M2, 1.0 * _M2)


def test__compare_standard_val_strict_compare__gt():
    assert compare_standard_val_strict(1.2 * _M2, 1.0 * _M2, operator.gt)
