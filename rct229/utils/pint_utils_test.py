import pytest
from pint_utils import pint_sum

from rct229.schema.config import ureg

FLOOR_AREA = 1 * ureg("m2")


def test__pint_sum__with_list_len_2():
    assert pint_sum([FLOOR_AREA, 2 * FLOOR_AREA]) == 3 * FLOOR_AREA


def test__pint_sum__with_empty_list_and_default():
    assert pint_sum([], 0 * FLOOR_AREA) == 0 * FLOOR_AREA


def test__pint_sum__with_empty_list_and_no_default():
    with pytest.raises(AssertionError):
        pint_sum([])
