import pytest

from interp import strict_linear_interpolation, strict_list_linear_interpolation

# Testing strict_linear_interpolation()
def test_strict_linear_interpolation_with_left_value():
    assert strict_linear_interpolation((1, 2), (3, 4), 1) == 2

def test_strict_linear_interpolation_with_right_value():
    assert strict_linear_interpolation((1, 2), (3, 4), 3) == 4

def test_strict_linear_interpolation_with_middle_value():
    assert strict_linear_interpolation((1, 2), (3, 4), 2) == 3

def test_strict_linear_interpolation_with_disordered_points():
    with pytest.raises(ValueError, match='pt0 pt1 out of order'):
        strict_linear_interpolation((3, 4),(1, 2),  0)

def test_strict_linear_interpolation_with_outside_values():
    with pytest.raises(ValueError, match='x out of range'):
        strict_linear_interpolation((1, 2), (3, 4), 0)
    with pytest.raises(ValueError, match='x out of range'):
        strict_linear_interpolation((1, 2), (3, 4), 4)



# Testing strict_list_linear_interpolation()
def test_strict_list_linear_interpolation_with_edge_value():
    assert strict_list_linear_interpolation([(1, 2), (3, 4), (5, 6)], 3) == 4

def test_strict_list_linear_interpolation_with_interior_value():
    assert strict_list_linear_interpolation([(1, 2), (3, 4), (5, 6)], 4) == 5

def test_strict_list_linear_interpolation_with_outside_values():
    with pytest.raises(ValueError, match='x out of range'):
        strict_list_linear_interpolation([(1, 2), (3, 4), (5, 6)], 0)
    with pytest.raises(ValueError, match='x out of range'):
        strict_list_linear_interpolation([(1, 2), (3, 4), (5, 6)], 6)
