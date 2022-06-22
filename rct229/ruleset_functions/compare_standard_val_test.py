import pytest
import operator

from rct229.ruleset_functions.compare_standard_val import compare_standard_val
from rct229.schema.config import ureg

_M2 = ureg("m2")


def test__compare_standard_val_stringent_compare_gt():
    assert compare_standard_val(1.5 * _M2, 1.0 * _M2, operator.gt, ahj_ra_compare=True)


def test__compare_standard_val_stringent_compare_lt():
    assert compare_standard_val(1.0 * _M2, 1.5 * _M2, operator.lt, ahj_ra_compare=True)


def test__compare_standard_val_stringent_compare_gt_equal():
    """test equal when ahj flat set to True"""
    assert compare_standard_val(0.9999 * _M2, 1.0 * _M2, operator.gt, ahj_ra_compare=True)


def test__compare_standard_val_non_stringent_code_compare():
    assert compare_standard_val(0.9999 * _M2, 1.0 * _M2)
