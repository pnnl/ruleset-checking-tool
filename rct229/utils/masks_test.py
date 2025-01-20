import pytest
from rct229.utils.masks import invert_mask


def test__invert_mask():
    assert invert_mask([0, 1.0, 1, 0.0]) == [1, 0, 0, 1]


def test__invert_mask__fail_assert():
    with pytest.raises(Exception):
        invert_mask([0, 1 / 2, 1, 0])
