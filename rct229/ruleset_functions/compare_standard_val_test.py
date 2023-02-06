import operator

import pytest

from rct229.ruleset_functions.compare_standard_val import compare_standard_val
from rct229.ruleset_functions.compare_standard_val import compare_standard_val_strict
from rct229.schema.config import ureg

_M2 = ureg("m2")


def test__compare_standard_val_stringent_compare_gt():
    assert compare_standard_val(True, 1.5 * _M2, 1.0 * _M2, operator.gt)


def test__compare_standard_val_stringent_compare_lt():
    assert compare_standard_val(True, 1.0 * _M2, 1.5 * _M2, operator.lt)


def test__compare_standard_val_stringent_compare_gt_equal():
    """test equal when ahj flat set to True"""
    assert compare_standard_val(True, 0.9999 * _M2, 1.0 * _M2, operator.gt)


def test__compare_standard_val_non_stringent_code_compare():
    assert compare_standard_val(False, 0.9999 * _M2, 1.0 * _M2)


def test__compare_standard_val_strict_compare_gt():
    assert compare_standard_val_strict(True, 1.2 * _M2, 1.0 * _M2, operator.gt)


def test__compare_standard_val_strict_code_compare():
    assert compare_standard_val_strict(False, 0.9999 * _M2, 1.0 * _M2) == False
