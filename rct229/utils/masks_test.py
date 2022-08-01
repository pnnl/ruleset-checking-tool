import pytest
from masks import invert_mask


def test__invert_mask():
    assert invert_mask([0, 1, 1, 0]) == [1, 0, 0, 1]
