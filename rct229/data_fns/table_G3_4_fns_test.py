import pytest

from rct229.data import data
from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.schema.config import ureg

ip_u_value_units = ureg("Btu / (hr * ft2 * delta_degF)")


def test__table_G34_CZ0A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ0A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.124 * ip_u_value_units
    }


def test__table_G34_CZ1A_ABOVE_GRADE_WALL_EXTERIOR_NON_RESIDENTIAL():
    assert table_G34_lookup("CZ1A", "EXTERIOR NON-RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.124 * ip_u_value_units
    }


def test__table_G34_CZ2A_ABOVE_GRADE_WALL_SEMI_EXTERIOR():
    assert table_G34_lookup("CZ2A", "SEMI-EXTERIOR", "ABOVE-GRADE WALL") == {
        "u_value": 0.352 * ip_u_value_units
    }


def test__table_G34_CZ3A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ3A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.124 * ip_u_value_units
    }


def test__table_G34_CZ3A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ3A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.084 * ip_u_value_units
    }


def test__table_G34_CZ4A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ4A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.064 * ip_u_value_units
    }


def test__table_G34_CZ5A_ABOVE_GRADE_WALL_SEMI_EXTERIOR():
    assert table_G34_lookup("CZ5A", "SEMI-EXTERIOR", "ABOVE-GRADE WALL") == {
        "u_value": 0.124 * ip_u_value_units
    }


def test__table_G34_CZ6A_ABOVE_GRADE_WALL_EXTERIOR_RESIDENTIAL():
    assert table_G34_lookup("CZ6A", "EXTERIOR RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.064 * ip_u_value_units
    }


def test__table_G34_CZ7_ABOVE_GRADE_WALL_NON_RESIDENTIAL():
    assert table_G34_lookup("CZ7", "EXTERIOR NON-RESIDENTIAL", "ABOVE-GRADE WALL") == {
        "u_value": 0.064 * ip_u_value_units
    }


def test__table_CZ8_CZ0A_ABOVE_GRADE_WALL_SEMI_EXTERIOR():
    assert table_G34_lookup("CZ8", "SEMI-EXTERIOR", "ABOVE-GRADE WALL") == {
        "u_value": 0.124 * ip_u_value_units
    }
